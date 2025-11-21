좋습니다. 올려주신 코드, 핵심 버그만 정확히 고쳐 **그대로 이어서 쓸 수 있게** 패치했습니다. (SciPy 유지·2D/3D RGI 정확 적용)

# 핵심 수정 포인트

* **RGI 입력 형식**: `RegularGridInterpolator`는 **(n_points, ndim)** 형태의 입력을 요구합니다. 단일 점은 `[[disp, trim]]`처럼 2차원으로 넣고, 결과는 `np.asarray(...).squeeze()`로 스칼라/벡터 정리.
* **불필요한 `[0]` 인덱싱 제거**: `interpolator(point)[0]` 때문에 **스칼라만** 뽑히며 KN 7개 각도가 잘립니다. → 벡터 전체를 사용하도록 수정.
* **피벗 그리드 정렬**: `pivot()` 후 **index(Disp), columns(Trim)**을 **정렬한 축**에 `reindex`하여 보간 축과 값 행렬 정렬 일치.
* **Trim 공식 단위**: `MTC`가 **t·m/cm**이면 `trim_m = Δ * (LCB - LCG) / (MTC / 100)` (후미 양(+) 기준)으로 일관화.
* **예외/경고**: 보간 경계 밖(NaN)·비현실 Trim에 대한 안전 경고 추가.

---

## 패치된 전체 코드 (드롭인 교체)

```python
import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import simps
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class Vessel:
    def __init__(self, ls_weight, ls_lcg, ls_vcg, ls_tcg):
        self.lightship_weight = float(ls_weight)
        self.lightship_lcg_moment = float(ls_weight) * float(ls_lcg)
        self.lightship_vcg_moment = float(ls_weight) * float(ls_vcg)
        self.lightship_tcg_moment = float(ls_weight) * float(ls_tcg)

        self.master_df = pd.DataFrame()
        self.mapping_df = pd.DataFrame()
        
        self.hydro_interpolators = {}
        self.kn_interpolator = None

        self.heel_angles_deg = [0, 10, 20, 30, 40, 50, 60]
        self.heel_angles_rad = np.deg2rad(self.heel_angles_deg)

        print(f"Vessel 'BUSHRA' initialized. Lightship: {ls_weight:.2f} t")

    # ---------- P-1: 마스터/매핑 ----------
    def load_master_data(self, master_path="master_tanks.csv", mapping_path="tank_mapping.csv"):
        try:
            self.master_df = pd.read_csv(master_path)
            self.mapping_df = pd.read_csv(mapping_path)
            print(f"P-1: Loaded {len(self.master_df)} master tanks and {len(self.mapping_df)} mappings.")
        except FileNotFoundError as e:
            print(f"[Error P-1] File not found: {e}.")
            raise

    # ---------- P-2.6: 보간 엔진 ----------
    def load_hydrostatics(self, hydro_path="hydrostatics.csv", kn_path="kn_table.csv"):
        try:
            hydro_df = pd.read_csv(hydro_path)
            kn_df    = pd.read_csv(kn_path)

            # 축 정렬 (유니크 → 정렬)
            trims = np.unique(hydro_df['Trim'].values).astype(float)
            disps = np.unique(hydro_df['Displacement'].values).astype(float)
            trims.sort(); disps.sort()

            # 1) Hydro 2D 보간기 (각 열에 대해)
            def make_grid(col):
                # 피벗 → 정렬 축으로 재인덱스 (index=Displacement, columns=Trim)
                p = hydro_df.pivot(index='Displacement', columns='Trim', values=col)
                p = p.reindex(index=disps, columns=trims)
                if p.isnull().values.any():
                    # 결측은 양끝값/선형보간으로 보정(단순 방어)
                    p = p.interpolate(axis=0).ffill().bfill().interpolate(axis=1).ffill().bfill()
                return p.values  # shape: (len(disps), len(trims))

            for col in ['Draft', 'LCB', 'VCB', 'KMT', 'MTC', 'TCP']:
                grid_z = make_grid(col)
                self.hydro_interpolators[col] = RegularGridInterpolator(
                    (disps, trims),
                    grid_z,
                    bounds_error=False, fill_value=None
                )

            # 2) KN 3D 보간기 (Disp, Trim, Heel)
            kn_trims = np.unique(kn_df['Trim'].values).astype(float)
            kn_disps = np.unique(kn_df['Displacement'].values).astype(float)
            kn_trims.sort(); kn_disps.sort()

            # Heel 축
            kn_cols = [f"Heel_{h}" for h in self.heel_angles_deg]

            # 3D 텐서 구성: (ndisp, ntrim, nheel)
            # 축 일치 위해 pivot 후 재인덱스
            kn_tensor = np.empty((len(kn_disps), len(kn_trims), len(self.heel_angles_deg)), dtype=float)
            for j, hcol in enumerate(kn_cols):
                p = kn_df.pivot(index='Displacement', columns='Trim', values=hcol)
                p = p.reindex(index=kn_disps, columns=kn_trims)
                if p.isnull().values.any():
                    p = p.interpolate(axis=0).ffill().bfill().interpolate(axis=1).ffill().bfill()
                kn_tensor[:, :, j] = p.values

            self.kn_interpolator = RegularGridInterpolator(
                (kn_disps, kn_trims, np.array(self.heel_angles_deg, dtype=float)),
                kn_tensor,
                bounds_error=False, fill_value=None
            )

            # 축 저장(리포트/검증용)
            self._hydro_axes = (disps, trims)
            self._kn_axes    = (kn_disps, kn_trims)

            print("P-2.6: Hydro/KN interpolators created.")

        except FileNotFoundError as e:
            print(f"[Error P-2.6] File not found: {e}.")
            raise
        except Exception as e:
            print(f"[Error P-2.6] Failed to create interpolators: {e}")
            raise

    # ---------- P-2.7: 조건 병합 ----------
    def load_condition(self, condition_path):
        try:
            condition_df = pd.read_csv(condition_path)

            merged_cond = condition_df.merge(self.mapping_df, on='Condition_Name', how='left')
            if merged_cond['Tank_ID'].isnull().any():
                missing = merged_cond[merged_cond['Tank_ID'].isnull()]['Condition_Name'].unique()
                print(f"[Warning P-2.7] Unmapped tanks: {missing}. (ignored)")

            final_plan = self.master_df.merge(merged_cond, on='Tank_ID', how='left')

            # SG 결정
            final_plan['SG'] = final_plan['SG_Override'].fillna(final_plan['SG_Master'])
            final_plan['Percent_Fill'] = final_plan['Percent_Fill'].fillna(0.0)

            return final_plan

        except FileNotFoundError as e:
            print(f"[Error P-2.7] Condition file not found: {e}")
            return None
        except Exception as e:
            print(f"[Error P-2.7] Failed to load condition: {e}")
            return None

    # ---------- P-2.8: 안정성 계산 ----------
    def calculate_stability(self, condition_path, iterations=3, trim_limit_m=2.0):
        plan_df = self.load_condition(condition_path)
        if plan_df is None:
            return None

        # 중량/모멘트
        plan_df['Weight']     = plan_df['Capacity_m3'] * (plan_df['Percent_Fill'] / 100.0) * plan_df['SG']
        plan_df['Moment_LCG'] = plan_df['Weight'] * plan_df['LCG']
        plan_df['Moment_VCG'] = plan_df['Weight'] * plan_df['VCG']
        plan_df['Moment_TCG'] = plan_df['Weight'] * plan_df['TCG']

        # FSM (Slack + SG 보정)
        plan_df['Current_FSM'] = plan_df.apply(
            lambda r: (r['FSM_full_tm'] * (r['SG'] / r['SG_Master']))
                      if (1.0 < r['Percent_Fill'] < 99.0) else 0.0,
            axis=1
        )

        s = plan_df[['Weight','Moment_LCG','Moment_VCG','Moment_TCG','Current_FSM']].sum()
        Δ = self.lightship_weight + s['Weight']
        LCG = (self.lightship_lcg_moment + s['Moment_LCG']) / Δ
        VCG = (self.lightship_vcg_moment + s['Moment_VCG']) / Δ
        TCG = (self.lightship_tcg_moment + s['Moment_TCG']) / Δ
        FSM = s['Current_FSM']

        print(f"--- Pre-Trim --- Δ={Δ:.2f}t, LCG={LCG:.2f}m, VCG={VCG:.2f}m, TCG={TCG:.2f}m")

        # Trim 반복
        trim = 0.0
        for i in range(iterations):
            pt = np.array([[Δ, trim]])  # shape (1,2)
            lcb = float(np.asarray(self.hydro_interpolators['LCB'](pt)).squeeze())
            mtc = float(np.asarray(self.hydro_interpolators['MTC'](pt)).squeeze())  # t·m/cm

            if np.isnan(lcb) or np.isnan(mtc):
                print(f"[Warn] Interp out-of-bounds at Δ={Δ:.2f}, trim={trim:.3f}. Stop iteration.")
                break

            # 단위 일관: MTC t·m/cm → /100 → t·m/m
            new_trim = Δ * (lcb - LCG) / (mtc / 100.0)
            print(f"Iter {i+1}: LCB={lcb:.3f}, MTC={mtc:.2f} → Trim {trim:.3f} → {new_trim:.3f} (m)")
            trim = new_trim

            if abs(trim) > trim_limit_m:
                print(f"[Warn] Trim |{trim:.2f}| m exceeds limit {trim_limit_m:.2f} m (check MTC/LCB units).")
                break

        final_trim = trim
        pt_final = np.array([[Δ, final_trim]])

        # Hydro 지표
        KMT  = float(np.asarray(self.hydro_interpolators['KMT'](pt_final)).squeeze())
        mean = float(np.asarray(self.hydro_interpolators['Draft'](pt_final)).squeeze())
        draft_f = mean - final_trim/2.0
        draft_a = mean + final_trim/2.0

        KGc = VCG + (FSM / Δ if Δ else 0.0)
        GMc = KMT - KGc

        # KN → GZ(각도별)
        # 3D RGI: (Δ, Trim, Heel) → 스칼라, 각도 벡터로 반복 호출
        kn_vals = np.array([
            float(np.asarray(self.kn_interpolator([[Δ, final_trim, hd]])).squeeze())
            for hd in self.heel_angles_deg
        ])
        gz_vals = kn_vals - KGc * np.sin(self.heel_angles_rad)

        report = {
            "Condition": condition_path,
            "Displacement": round(Δ, 2),
            "Final_LCG": round(LCG, 2),
            "Final_VCG": round(VCG, 2),
            "Final_TCG": round(TCG, 2),
            "Final_Trim": round(final_trim, 2),
            "Mean_Draft": round(mean, 2),
            "Draft_Fwd": round(draft_f, 2),
            "Draft_Aft": round(draft_a, 2),
            "Total_FSM": round(FSM, 2),
            "VCG_Corrected": round(KGc, 2),
            "Final_KMT": round(KMT, 2),
            "GM_Corrected": round(GMc, 2),
            "KN_Curve_m": {h: round(v, 3) for h, v in zip(self.heel_angles_deg, kn_vals)},
            "GZ_Curve_m": {h: round(v, 3) for h, v in zip(self.heel_angles_deg, gz_vals)},
        }

        report["IMO_A749_Check"] = self.check_imo_a749(report)
        return report

    # ---------- P-3.9: IMO 체크 ----------
    def check_imo_a749(self, report):
        heels = np.array(self.heel_angles_deg, dtype=float)
        gz    = np.array(list(report["GZ_Curve_m"].values()), dtype=float)

        # 1° 간격 보간(0~40°)
        fine = np.arange(0.0, 41.0, 1.0)
        gz_i = np.interp(fine, heels, gz)
        rad  = np.deg2rad(fine)

        area_0_30 = float(simps(gz_i[:31], rad[:31]))  # 0–30
        area_0_40 = float(simps(gz_i, rad))            # 0–40
        area_30_40 = float(simps(gz_i[30:], rad[30:])) # 30–40
        gz_30      = float(np.interp(30.0, heels, gz))
        gz_max     = float(gz.max())
        ang_max    = float(heels[np.argmax(gz)])

        checks = {
            "GM >= 0.15m":        {"Value": round(report["GM_Corrected"], 2), "Required": 0.15, "Pass": report["GM_Corrected"] >= 0.15},
            "Area 0-30 (m-rad)":  {"Value": round(area_0_30, 3), "Required": 0.055, "Pass": area_0_30 >= 0.055},
            "Area 0-40 (m-rad)":  {"Value": round(area_0_40, 3), "Required": 0.090, "Pass": area_0_40 >= 0.090},
            "Area 30-40 (m-rad)": {"Value": round(area_30_40, 3), "Required": 0.030, "Pass": area_30_40 >= 0.030},
            "GZ at 30 (m)":       {"Value": round(gz_30, 2), "Required": 0.20,  "Pass": gz_30 >= 0.20},
            "GZmax (m)":          {"Value": round(gz_max, 2), "Required": 0.15,  "Pass": gz_max >= 0.15},
            "Angle@GZmax (deg)":  {"Value": round(ang_max, 1), "Required": None, "Pass": True},
        }
        checks["Overall_Pass"] = all(v["Pass"] for v in checks.values() if v["Pass"] is not None)
        return checks


# --- 실행 예시 ---
if __name__ == "__main__":
    bushra_vessel = Vessel(ls_weight=770.162, ls_lcg=26.349, ls_vcg=3.884, ls_tcg=0.0)
    bushra_vessel.load_master_data()        # master_tanks.csv, tank_mapping.csv
    bushra_vessel.load_hydrostatics()       # hydrostatics.csv, kn_table.csv

    print("\n" + "="*50)
    print("Executing Stability Calculation for 'condition_1658t.csv'")
    print("="*50)

    # 예시 입력 생성(필요 시 주석)
    condition_1658t_data = """Condition_Name,Percent_Fill,SG_Override
DAILY OIL TANK (P),28.6,0.820
DAILY OIL TANK (S),28.6,0.820
NO FO TANK (DBTM-P),25.3,0.820
NO 1 FO TANK (DBTM-S),25.3,0.820
NO 1 FO TANK (DBTM-C),15.8,0.820
NO.1 FW TANK (P),100.0,1.000
NO.1 FW TANK (S),73.3,1.000
NO. 2 FW TANK (P),100.0,1.000
NO 2 FW TANK (S),100.0,1.000
NO. 1 FW BALLAST TANK (P),100.0,1.025
NO. 1 FW BALLAST TANK (S),100.0,1.025
NO 2 FW BALLAST TANK (P),100.0,1.025
NO 2 FW BALLAST TANK (S),100.0,1.025
NO.3 VOID TANK (P),0.0,1.025
NO.3 VOID TANK (S),0.0,1.025
"""
    with open("condition_1658t.csv", "w", encoding="utf-8") as f:
        f.write(condition_1658t_data)

    report = bushra_vessel.calculate_stability(condition_path="condition_1658t.csv", iterations=3)

    if report:
        import json
        print("\n--- FINAL STABILITY REPORT (1658t) ---")
        print(json.dumps(report, indent=2, ensure_ascii=False))

        # 간단 검증 출력(타겟 수치 대비)
        print("\n--- Validation Targets ---")
        print(f"Δ ≈ 1658.71 t (if your condition matches)")
        print(f"GMcorr target ≈ 4.91 m; KGcorr target ≈ 4.21 m (예시)")
```

---

## 입력 CSV 스키마 체크(필수)

* **hydrostatics.csv**: `Displacement, Trim, Draft, LCB, VCB, KMT, MTC, TCP`

  * 단위: `MTC = t·m/cm` 가정(다르면 식 수정 필요)
* **kn_table.csv**: `Displacement, Trim, Heel_0, Heel_10, …, Heel_60` (KN 값 = m)
* **master_tanks.csv**: `Tank_ID, Capacity_m3, SG_Master, FSM_full_tm, LCG, VCG, TCG, ...`
* **tank_mapping.csv**: `Condition_Name, Tank_ID`
* **condition_xxx.csv**: `Condition_Name, Percent_Fill, SG_Override`

---

## 빠른 진단 가이드

* **Trim 폭주**: `|Trim| > 2.00 m` 경고 → **MTC 단위**, **LCB 기준점**, **LCG 계산** 확인.
* **보간 NaN**: Disp/Trim 범위 밖 → 테이블 범위 확대 또는 입력값 조정.
* **GZ 곡선 이상치**: `VCG_corrected` 과대/과소, KN 테이블 단위 확인(m).

필요하시면 이 버전에 **XLSX/PDF 리포트(export)** 모듈까지 바로 붙여드릴게요.

