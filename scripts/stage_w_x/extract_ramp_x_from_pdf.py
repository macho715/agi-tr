#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RoRo Ramp X-Extractor (Vectors Only)
- Semi-Anchor / Full-Geometry modes
- PDF vectors only: uses PyMuPDF Page.get_drawings(extended=True)
- No text/OCR. Midship-relative x(+Fwd/-Aft).
Requires: pymupdf (fitz)

Usage:
  python extract_ramp_x_from_pdf.py --pdf "../../RoRo Simulation_stowage plan_20251103.pdf" \
      --page 0 --mode semi --anchors anchors.yaml --out stage_x_w.csv
  python extract_ramp_x_from_pdf.py --pdf "../../RoRo Simulation_stowage plan_20251103.pdf" \
      --page 0 --mode full --out stage_x_w.csv
"""
from __future__ import annotations
import sys, math, json, argparse, csv, pathlib
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any

import fitz  # PyMuPDF

# ---------- Utils
Point = Tuple[float, float]

def dist(a: Point, b: Point) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])

def angle_deg(a: Point, b: Point) -> float:
    ang = math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))
    return ang

def proj_point_on_line(p: Point, a: Point, b: Point) -> Point:
    # Projection of p onto line a->b
    ax, ay, bx, by, px, py = a[0], a[1], b[0], b[1], p[0], p[1]
    abx, aby = bx-ax, by-ay
    ab2 = abx*abx + aby*aby
    if ab2 == 0:
        return a
    apx, apy = px-ax, py-ay
    t = (apx*abx + apy*aby)/ab2
    return (ax + t*abx, ay + t*aby)

def signed_longitudinal_x(p: Point, mid: Point, fwd_ref: Point, stern_ref: Point, meters_per_unit: float) -> float:
    # +x to FWD, -x to AFT relative to midship
    # build vessel longitudinal axis vector stern->bow
    vx, vy = fwd_ref[0]-stern_ref[0], fwd_ref[1]-stern_ref[1]
    vlen = math.hypot(vx, vy)
    if vlen == 0:
        raise ValueError("Invalid vessel axis.")
    ux, uy = vx/vlen, vy/vlen
    dx, dy = p[0]-mid[0], p[1]-mid[1]
    x_signed_units = dx*ux + dy*uy
    return x_signed_units * meters_per_unit

def polyline_length(poly: List[Point]) -> float:
    return sum(dist(poly[i], poly[i+1]) for i in range(len(poly)-1))

def bbox_of_points(points: List[Point]) -> fitz.Rect:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return fitz.Rect(min(xs), min(ys), max(xs), max(ys))

# ---------- Vector extraction (no text)
def iter_draw_lines(page: fitz.Page, min_seg_len: float = 1.0):
    """
    Yield polylines extracted from vector paths. We only consider stroked paths.
    Based on Page.get_drawings(extended=True) API (vectors only).  # docs: get_drawings
    """
    drawings = page.get_drawings(extended=True)  # vectors only
    for path in drawings:
        # Accept both stroked and filled paths (some PDFs use fill instead of stroke)
        if not path.get("stroke") and not path.get("fill"):
            continue
        items = path.get("items", [])
        poly: List[Point] = []
        pen_down = False
        for it in items:
            # it is a tuple like ('l', p1, p2) for line; or ('m', p); ('re', rect);('c', p1,p2,p3)
            op = it[0]
            if op == "m":  # move
                if poly:
                    if polyline_length(poly) >= min_seg_len:
                        yield poly, path
                poly = [ (it[1].x, it[1].y) ]
                pen_down = False
            elif op == "l":  # line
                p = (it[1].x, it[1].y)
                if not pen_down and poly:
                    pen_down = True
                poly.append(p)
            elif op == "re":  # rectangle -> 4 edges
                r: fitz.Rect = it[1]
                rect_pts = [(r.x0,r.y0),(r.x1,r.y0),(r.x1,r.y1),(r.x0,r.y1),(r.x0,r.y0)]
                if polyline_length(rect_pts) >= min_seg_len:
                    yield rect_pts, path
            elif op == "c":  # cubic bezier curve - approximate as line segments
                # Extract control points
                if len(it) >= 4:
                    p1 = (it[1].x, it[1].y) if hasattr(it[1], 'x') else it[1]
                    p2 = (it[2].x, it[2].y) if hasattr(it[2], 'x') else it[2]
                    p3 = (it[3].x, it[3].y) if hasattr(it[3], 'x') else it[3]
                    # Approximate bezier with line segments (simple: just add endpoints)
                    if poly:
                        poly.append(p3)
                    else:
                        poly = [p1, p3]
            else:
                # ignore other operations for robustness
                pass
        if poly:
            if polyline_length(poly) >= min_seg_len:
                yield poly, path

# ---------- Semi-Anchor mode
@dataclass
class Anchors:
    stern: Point     # stern reference point on baseline
    bow: Point       # bow reference point on baseline
    mid: Optional[Point] = None  # optional explicit midship point
    lpp_m: float = 64.0          # meters

def load_anchors(yaml_or_json: str) -> Anchors:
    import json, yaml  # pyyaml optional
    with open(yaml_or_json, "r", encoding="utf-8") as f:
        txt = f.read()
    try:
        data = json.loads(txt)
    except Exception:
        data = yaml.safe_load(txt)
    stern = tuple(data["stern"])
    bow = tuple(data["bow"])
    mid = tuple(data["mid"]) if data.get("mid") else None
    lpp_m = float(data.get("lpp_m", 64.0))
    return Anchors(stern, bow, mid, lpp_m)

def compute_scale_and_mid(anc: Anchors) -> Tuple[float, Point]:
    units = dist(anc.stern, anc.bow)  # PDF user-space units (points)
    if units == 0:
        raise ValueError("Anchor stern/bow are identical.")
    meters_per_unit = anc.lpp_m / units
    if anc.mid:
        mid = anc.mid
    else:
        mid = ((anc.stern[0]+anc.bow[0])/2.0, (anc.stern[1]+anc.bow[1])/2.0)
    return meters_per_unit, mid

# ---------- Full-Geometry mode
def infer_vessel_axis(page: fitz.Page, LPP_M: float = 64.0) -> Tuple[Tuple[Point, Point], float, Point]:
    """
    Enhanced vessel axis inference with scale sanity check
    """
    polys = list(iter_draw_lines(page, min_seg_len=5.0))
    if not polys:
        raise RuntimeError("No vector polylines found.")
    
    # 후보: bbox 폭이 큰 상위 20개 선분군
    cands = []
    for poly, _ in polys:
        if len(poly) < 2:
            continue
        Lunits = polyline_length(poly)
        x0, y0 = poly[0]
        x1, y1 = poly[-1]
        width = abs(x1 - x0)
        height = abs(y1 - y0)
        
        # 직선성(끝점 방향) & 수평성 점수
        ang = abs(angle_deg(poly[0], poly[-1]))
        horizontal_score = 1.0 / (1.0 + abs(ang))  # 0°가 최고
        straight_score = Lunits / (Lunits + (height + 1e-6))
        score = width * (0.7 * horizontal_score + 0.3 * straight_score)
        cands.append((score, poly))
    
    cands.sort(reverse=True)
    
    # 상위 후보 중 스케일 sanity로 선택
    for _, poly in cands[:20]:
        stern, bow = poly[0], poly[-1]
        units = dist(stern, bow)  # PDF user-units (pt)
        m_per_unit = LPP_M / units if units else None
        if not m_per_unit:
            continue
        if 0.03 <= m_per_unit <= 0.20:  # sane for A4/A3 도면
            mid = ((stern[0] + bow[0]) / 2, (stern[1] + bow[1]) / 2)
            return (stern, bow), m_per_unit, mid
    
    # 마지막 폴백: 페이지 폭 기반
    rect = page.rect
    stern = (rect.x0, rect.y0 + rect.height / 2)
    bow = (rect.x1, rect.y0 + rect.height / 2)
    units = dist(stern, bow)
    m_per_unit = LPP_M / units if units else 0.1
    mid = ((stern[0] + bow[0]) / 2, (stern[1] + bow[1]) / 2)
    return (stern, bow), m_per_unit, mid

def select_ramp_line(page: fitz.Page,
                     vessel_axis: Tuple[Point, Point],
                     meters_per_unit: float,
                     LPP_M: float = 64.0,
                     base_angle: Tuple[float, float] = (-15.0, -2.0),
                     min_len_ratio: float = 0.08,
                     max_angle_expansions: int = 3) -> List[Point]:
    """
    Enhanced ramp line selection with x pre-filter and progressive angle expansion
    """
    stern, bow = vessel_axis
    axis_ang = angle_deg(stern, bow)
    min_len_units = (LPP_M * min_len_ratio) / meters_per_unit
    angle_lo, angle_hi = base_angle
    
    def pick(angle_window: Tuple[float, float]) -> Optional[List[Point]]:
        cands = []
        for poly, _ in iter_draw_lines(page, min_seg_len=5.0):
            L = polyline_length(poly)
            if L < min_len_units:
                continue
            
            ang = angle_deg(poly[0], poly[-1]) - axis_ang
            while ang > 180:
                ang -= 360
            while ang < -180:
                ang += 360
            if not (angle_window[0] <= ang <= angle_window[1]):
                continue
            
            pm = poly_midpoint(poly)
            # x 사전필터: ramp는 선미 쪽 (음수)이며 과도한 원거리 제외
            x = signed_longitudinal_x(pm, ((stern[0] + bow[0]) / 2, (stern[1] + bow[1]) / 2),
                                     bow, stern, meters_per_unit)
            if not (-0.6 * LPP_M <= x <= 0.1 * LPP_M):
                continue
            
            cands.append((abs(x), L, poly))  # 선미에 가까울수록 |x| 크고, 길수록 우선
        
        if not cands:
            return None
        
        cands.sort(key=lambda t: (-t[1], -t[0]))  # 길이 우선, 다음 aftness
        return cands[0][2]
    
    # 단계적으로 각도창 확장
    for k in range(max_angle_expansions + 1):
        ang_win = (angle_lo - 2 * k, angle_hi + 2 * k)
        poly = pick(ang_win)
        if poly:
            return poly
    
    raise RuntimeError("Ramp line not found after expansions.")

def poly_midpoint(poly: List[Point]) -> Point:
    # approximate mid-point along length
    total = polyline_length(poly)
    if total == 0:
        return poly[0]
    acc = 0.0
    for i in range(len(poly)-1):
        seg = dist(poly[i], poly[i+1])
        if acc + seg >= total/2:
            ratio = (total/2 - acc)/seg if seg else 0
            x = poly[i][0] + ratio*(poly[i+1][0]-poly[i][0])
            y = poly[i][1] + ratio*(poly[i+1][1]-poly[i][1])
            return (x,y)
        acc += seg
    return poly[-1]

# ---------- Stage composer
def compose_stages(x_contact_m: float,
                   weights_rule: Dict[int,float],
                   unit_weight_t: float = 217.0,
                   combined_units: int = 2) -> List[Dict[str,Any]]:
    """
    Build standard 5-stage table. Only W_stage_t & x_stage_m; Trim은 사용자의 엑셀에서 계산.
    weight rule: {2:0.30, 3:0.50, 4:1.00, 5:2.00} (× 217t)
    Stage-5 x는 합성 CG가 되므로 x_contact에서 약간 Fwd로 이동하는 보수치(예: +1m) 옵션 가능.
    """
    rows = []
    placeholder = {
        1: (0.0,  0.00),
        2: (unit_weight_t*weights_rule.get(2,0.30), x_contact_m),
        3: (unit_weight_t*weights_rule.get(3,0.50), x_contact_m/2.0),  # half-on-ramp 보수치
        4: (unit_weight_t*weights_rule.get(4,1.00), x_contact_m*0.4),
        5: (unit_weight_t*weights_rule.get(5,2.00), x_contact_m*0.2),  # combined CG placeholder
    }
    for stage in range(1,6):
        w,x = placeholder[stage]
        rows.append({"stage":stage,"W_stage_t":round(w,2),"x_stage_m":round(x,2)})
    return rows

# ---------- Main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--page", type=int, default=0)
    ap.add_argument("--mode", choices=["semi","full"], required=True)
    ap.add_argument("--anchors", help="YAML/JSON with stern,bow[,mid],lpp_m=64")
    ap.add_argument("--angle", type=float, nargs=2, default=[-15.0,-2.0], help="deg vs vessel axis (base angle window)")
    ap.add_argument("--min-len-m", type=float, default=5.0, help="minimum ramp length in meters (default: 0.08*Lpp)")
    ap.add_argument("--out", default="stage_x_w.csv")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    page = doc[args.page]

    if args.mode == "semi":
        if not args.anchors:
            sys.exit("Semi mode requires --anchors YAML/JSON with stern,bow[,mid],lpp_m.")
        anc = load_anchors(args.anchors)
        meters_per_unit, mid = compute_scale_and_mid(anc)
        # ramp line: choose by proximity to a guide point if provided (optional)
        ramp_poly = select_ramp_line(page, (anc.stern, anc.bow), meters_per_unit, LPP_M=anc.lpp_m,
                                     base_angle=tuple(args.angle) if len(args.angle) == 2 else (-15.0, -2.0))
        ramp_mid = poly_midpoint(ramp_poly)
        x_contact_m = signed_longitudinal_x(ramp_mid, mid, anc.bow, anc.stern, meters_per_unit)
    else:
        # Full-Geometry mode with enhanced axis inference
        try:
            (stern, bow), m_per_unit, mid = infer_vessel_axis(page, LPP_M=64.0)
            print(f"[INFO] Vessel axis inferred: m_per_unit={m_per_unit:.4f}")
            ramp_poly = select_ramp_line(page, (stern, bow), m_per_unit, LPP_M=64.0,
                                        base_angle=tuple(args.angle) if len(args.angle) == 2 else (-15.0, -2.0))
            ramp_mid = poly_midpoint(ramp_poly)
            x_contact_m = signed_longitudinal_x(ramp_mid, mid, bow, stern, m_per_unit)
        except Exception as e:
            print(f"[WARN] Full-Geometry failed: {e}. Falling back to Semi-Anchor heuristic.")
            # 폴백: 페이지 가로중선 축 + 합리 스케일
            rect = page.rect
            stern = (rect.x0, rect.y0 + rect.height / 2)
            bow = (rect.x1, rect.y0 + rect.height / 2)
            units = dist(stern, bow)
            m_per_unit = 64.0 / units if units else 0.1
            mid = ((stern[0] + bow[0]) / 2, (stern[1] + bow[1]) / 2)
            ramp_poly = select_ramp_line(page, (stern, bow), m_per_unit, LPP_M=64.0,
                                        base_angle=tuple(args.angle) if len(args.angle) == 2 else (-15.0, -2.0))
            ramp_mid = poly_midpoint(ramp_poly)
            x_contact_m = signed_longitudinal_x(ramp_mid, mid, bow, stern, m_per_unit)

    # 산출 검증: x sanity
    if abs(x_contact_m) > 0.6 * 64.0:
        raise ValueError(f"x_contact out of range ({x_contact_m:.2f} m). Check axis/scale.")
    
    # Compose 5-stage table (W only; Trim은 시트에서 계산)
    weights_rule = {2:0.30, 3:0.50, 4:1.00, 5:2.00}
    rows = compose_stages(x_contact_m, weights_rule)

    # Write CSV
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["stage","W_stage_t","x_stage_m"])
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] saved {args.out}  contact_x={x_contact_m:.2f} m")

if __name__ == "__main__":
    main()
