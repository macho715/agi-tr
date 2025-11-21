# Patch Guides Index

이 디렉토리에는 `agi tr.py` 스크립트의 패치 가이드 문서들이 보관되어 있습니다.

## 패치 가이드 문서

### 주요 패치 가이드

1. **sdsdds.md** - Stage별 Trim_target 컬럼 추가 가이드
   - Version 3.9 (2025-11-19) 적용
   - Q열(17) Trim_target_stage_cm 컬럼 추가
   - H열(8) ΔTM_cm_tm 수식 업데이트
   - 컬럼 구조 변경 (Q열 추가로 인한 한 칸씩 밀림)

2. **zzzzz.md** - Trim_target 기반 Ballast Fix 수식 패치 가이드
   - Version 3.8 (2025-11-19) 적용
   - H/J/K/AM~AP 컬럼 업데이트
   - Trim_target_cm(B6) 기준 계산 통일

3. **aaaa.md** - LCF 기반 정밀 Draft 보정 모듈 패치 가이드
   - Version 3.7 (2025-11-19) 적용
   - Python 함수 수정
   - Excel 수식 수정
   - AS 컬럼 제거

4. **patcaah.md** - CAPTAIN_REPORT 시트 구조 가이드
   - CAPTAIN_REPORT 시트 설계 및 구현 가이드

5. **wewewewe.md** - Stage Evaluation Functions 가이드
   - agi tr.py line 2183에서 참조
   - Stage 평가 함수 관련 가이드

## CHANGELOG 참조

각 패치 가이드의 상세 내용은 [`../CHANGELOG.md`](../CHANGELOG.md)에서 확인할 수 있습니다:

- [Version 3.9](../CHANGELOG.md#version-39-2025-11-19) - sdsdds.md 가이드
- [Version 3.8](../CHANGELOG.md#version-38-2025-11-19) - zzzzz.md 가이드
- [Version 3.7](../CHANGELOG.md#version-37-2025-11-19) - aaaa.md 가이드

## 코드 참조

`agi tr.py` 스크립트 내에서 이 문서들은 주석으로 참조됩니다:

```python
# sdsdds.md: Q열 추가 (Stage별 타깃, 없으면 B6 사용)
# zzzzz.md 가이드: ΔTM(H) / Lever_arm(I) = 이론상 필요한 Ballast_t
# aaaa.md 가이드 준수
# wewewewe.md 가이드
```

## 사용 방법

패치를 적용할 때는 해당 가이드 문서를 참조하여 단계별로 진행하세요.

