# 헬스케어 제품 분할처방 효과 분석

## 📋 프로젝트 개요

### 비즈니스 문제
- **기존 방식**: 3개월치 헬스케어 제품을 한 번에 처방
- **문제점**: 환자의 제품 복용 순응도 및 효과 모니터링 어려움
- **해결책**: 1.5개월씩 2번 나누어 처방하여 중간에 의료진이 체크

### 분석 목적
**분할처방을 통한 환자 케어 강화가 치료 효과를 높였는지 A/B 테스트로 검증**

## 🎯 핵심 성과지표 (KPI)

### 1️⃣ 체중 감소 효과 (BMI 변화)
- **측정**: 의료기관에서 직접 측정한 체중/신장 데이터
- **비교**: 제품 복용 전 vs 후 BMI 변화
- **기대효과**: 중간 체크를 통한 더 나은 체중 감량

### 2️⃣ 재구매율
- **측정**: 150일 이내 재구매 비율
- **의미**: 환자 만족도 및 치료 지속성
- **기대효과**: 케어 강화로 인한 재구매 증가

### 3️⃣ 추천율 (고객 만족도)
- **측정**: 추천 인센티브 프로그램 참여율
- **의미**: 환자의 제품 만족도 및 추천 의향
- **기대효과**: 향상된 케어로 인한 추천 증가

## 📊 데이터 구조

### 실험 설계
- **Control Group (2023년)**: 3개월 일괄 처방
- **Treatment Group (2024년)**: 1.5개월씩 분할 처방

### 데이터 특성
- **BMI 데이터**: 환자별 시계열 데이터 (방문 시점이 불규칙하여 주차별 분석)
- **구매 데이터**: 첫 구매일, 재구매일 정보
- **추천 데이터**: 인센티브 프로그램 참여 내역

## 🔬 분석 방법론

### 1. BMI 감소 분석
- **모델**: Mixed-Effects Model (환자별 개인차 고려)
- **통계검정**: F-test (분산 동질성 검정)
- **기간 분석**: 30-105일 구간별 효과 측정

### 2. 재구매율 분석
- **통계검정**: Z-test (두 비율 간 차이 검정)
- **세부 분석**: 기간별 재구매 패턴 분석

### 3. 추천율 분석
- **매칭**: 환자별 첫 구매 후 150일 이내 인센티브 프로그램 참여 여부
- **통계검정**: Z-test (월별 추천율 비교)

## 📈 기대 결과

분할처방을 통한 **의료진 케어 강화**가 다음과 같은 효과를 가져올 것으로 예상:

1. **더 나은 BMI 감소**: 중간 모니터링을 통한 복용 지도 효과
2. **높은 재구매율**: 환자 만족도 증가로 인한 지속 치료
3. **증가한 추천율**: 케어 품질 향상으로 인한 추천 의향 증가

## 🛠 기술 스택

- **Python**: 데이터 분석 및 통계 검정
- **pandas**: 데이터 전처리
- **statsmodels**: Mixed-Effects Model, ANOVA
- **scipy**: 통계 검정 (F-test, Z-test)
- **matplotlib**: 시각화

## 📁 파일 구조

```
├── README.md
├── healthcare_analysis.py        # 핵심 분석 코드
├── statistical_utils.py          # 통계 검정 유틸리티
└── sample_data/
    ├── bmi_measurements/         # BMI 측정 데이터
    ├── purchase_records/         # 구매/재구매 데이터
    └── referral_data/           # 추천/인센티브 데이터
```

## 🚀 실행 방법

```python
from healthcare_analysis import HealthcareAnalyzer

# 분석 실행
analyzer = HealthcareAnalyzer()
results = analyzer.run_full_analysis()

# 결과 요약
analyzer.print_summary()
```

## 💡 비즈니스 임팩트

이 분석을 통해 **분할처방의 ROI**를 정량적으로 측정하고, 향후 처방 정책 결정에 데이터 기반 근거를 제공합니다.

### 주요 인사이트
- 환자 케어 강화의 정량적 효과 측정
- 의료 서비스 품질과 비즈니스 성과의 상관관계 분석
- A/B 테스트를 통한 과학적 의사결정 지원

---

*본 프로젝트는 헬스케어 데이터를 활용한 A/B 테스트 분석 사례입니다.*