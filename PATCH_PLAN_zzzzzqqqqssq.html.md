# zzzzzqqqqssq.html 패치 계획

**작성일**: 2025-11-21
**대상 파일**: `zzzzzqqqqssq.html`
**백업 파일**: `zzzzzqqqqssq.html.backup_YYYYMMDD_HHMMSS`

---

## 현재 상태 분석

### 1. mapX_CAD 함수 (236-239줄)
```javascript
function mapX_CAD(metersFromAP) {
    if (metersFromAP === null) return 1500; 
    return AP_OFFSET + (metersFromAP * 15.0); 
}
```
- **현재 공식**: `AP_OFFSET + (metersFromAP * 15.0)`
- **AP_OFFSET**: 100
- **PX_PER_M**: 15.0

### 2. stages 배열 (242-291줄)
- **현재**: 8개 Stage (st1 ~ st7)
- **구조**: `{ id, label, day, tr1, tr2, dfwd, daft, bal, tug, desc }`
- **tug 속성**: 모든 Stage에 `tug: true/false` 명시적으로 존재

### 3. setStage 함수 (358-473줄)
- **tug 처리**: 376줄에서 `if (d.tug)` 직접 체크
- **day 처리**: 369줄에서 `d.day` 직접 사용

---

## 예상 패치 항목 (이전 tr1111.html 패치 패턴 기반)

### 패치 1: mapX_CAD 함수 교체
**위치**: 236-239줄
**변경사항**:
- 새 공식: `(cad_m_from_AP / 64.0) * 960 + 100`
- null/undefined 체크 추가

### 패치 2: stages 배열 교체
**위치**: 242-291줄
**변경사항**:
- 새로운 8개 Stage 데이터로 교체
- `tug` 속성 제거 (또는 선택적 속성으로 변경)

### 패치 3: setStage 함수 수정
**위치**: 376줄 (tug 처리), 369줄 (day 처리)
**변경사항**:
- `if (d.tug)` → `if (d.tug ?? false)`
- `d.day` → `d.day ?? "PRE-OP"` (fallback 추가)

---

## 주의사항

⚠️ **가이드 미제공**: 사용자가 "아래 가이드로"라고 했으나 구체적인 가이드가 제공되지 않았습니다.
- 이전 `tr1111.html` 패치 패턴을 참고하여 계획 작성
- 실제 패치 전 사용자 확인 필요

---

## 실행 순서

1. ✅ 백업 파일 생성 완료
2. ⏳ 패치 계획 문서 작성 (현재 단계)
3. ⏸️ 사용자 가이드 확인 대기
4. ⏸️ 패치 실행
5. ⏸️ 검증

---

## 백업 정보

- **원본 파일**: `zzzzzqqqqssq.html`
- **백업 파일**: `zzzzzqqqqssq.html.backup_YYYYMMDD_HHMMSS`
- **백업 위치**: 동일 디렉토리

