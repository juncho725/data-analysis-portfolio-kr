# 👋 안녕하세요! 저는 조경준입니다.

**비즈니스 문제를 데이터로 해결하는 Data Analyst & Business Intelligence Specialist**

> *"복잡한 실무 환경에서 발생하는 모든 변수를 고려한 데이터 분석으로 신뢰할 수 있는 인사이트를 제공합니다"* 📊

---

## 🎯 데이터 분석 전문성 & 비즈니스 임팩트

### 📈 **실무 복잡성을 고려한 데이터 분석**
- **외부 요인 통제**: 프로모션 효과, 정책 변화, 계절성 등을 고려한 엄밀한 분석 설계
- **0→1 데이터 구축**: 분석 불가능한 환경에서 **60만개 완전 데이터셋** 구축
- **A/B 테스트 전문성**: 교란변수 통제와 실무적 한계 인식을 통한 과학적 검증

### 🏗️ **복합적 비즈니스 환경 이해**
- **정책 변화 대응**: 시기별 규정 변경을 데이터 로직에 반영하는 시스템 설계
- **도메인 특수성**: 의료 워크플로우, 결제 시스템 복잡성 등 업계 특성 완전 이해
- **이해관계자 협업**: 의료진, 운영팀, 재무팀과의 협의를 통한 비즈니스 로직 정의

---

## 🛠️ 데이터 분석 기술 스택

### **Core Analytics**
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

### **Advanced Specializations**
- **실무 중심 통계**: Mixed-Effects Model, 교란변수 통제, 검정력 분석
- **복합 시스템 분석**: 140개 SQL 파일 분석, 레거시 시스템 구조 파악
- **정책 변화 대응**: 시기별 비즈니스 룰 변경을 반영한 동적 분류 시스템
- **도메인 전문 분석**: 의료 데이터 보안, 업계 특수 워크플로우 이해

---

## 📊 주요 데이터 분석 프로젝트

### 📌 [의료 데이터 파이프라인: 실무 복잡성 완전 고려한 0→1 구축](https://github.com/juncho725/data-analysis-portfolio-kr/01.healthcare-data-pipeline-0to1)

#### 🚨 **해결한 핵심 실무 도전들**

##### **1. 시기별 정책 변화 대응 시스템**
```python
# 💡 실무 복잡성: 동일한 '1-1' 코드가 시기별로 다른 의미
# - 2022년 이전: 1.5개월 패키지
# - 2022년 이후: 1개월 패키지
# 📊 해결: 의료진/운영팀 협의로 정책 변경일 정확히 파악 후 로직 분기

def categorize_package_by_policy_period(medicine_name, memo, consult_date):
    policy_change_date = pd.to_datetime('2022-12-13')  # 운영팀 협의 결과
    
    if memo.startswith('1-1'):
        # 정책 변경 전후로 완전히 다른 해석
        return '1.5개월' if consult_date <= policy_change_date else '1개월'
    
# 🎯 비즈니스 임팩트: 과거 데이터 오분류 방지, 정확한 트렌드 분석 가능
```

##### **2. 복합 결제 시스템의 현실적 제약 고려**
```python
# 💡 실무 복잡성: 의료 현장의 비정형 워크플로우
# - 선결제 → 나중 처방
# - 진료 후 결제
# - 처방 지연 발생
# 📊 해결: PaymentID-MedicalRecordID 불완전 연결을 시계열 기반으로 복구

# 1단계: 동일 치료 과정 내 복구 (30일 이내)
same_treatment = reference_df[
    (reference_df['PatientID'] == patient_id) &
    (abs(reference_df['ConsultTime'] - target_date) <= pd.Timedelta(days=30))
]

# 2단계: 후속 재방문 활용 (200일 이내) - 의료진 협의 기준
extended_search = reference_df[
    (reference_df['PatientID'] == patient_id) &
    (reference_df['ConsultTime'] > target_date) &
    (reference_df['ConsultTime'] - target_date <= pd.Timedelta(days=200))
]

# 🎯 비즈니스 임팩트: 결측율 35% → 3%, 실제 의료진 진료 패턴 반영
```

##### **3. 시간 기준점 불일치 문제 해결**
```python
# 💡 실무 복잡성: 의료업계 특성상 여러 시점 존재
# - 결제일 ≠ 처방일 ≠ 실제 복용 시작일
# 📊 해결: 의료진과 협의하여 '다이어트 효과 분석'에 최적화된 기준 정의

def determine_treatment_start_date(pay_date, consult_time):
    """의료진 협의: 실제 치료 확정 시점이 분석에 중요"""
    return max(pay_date, consult_time)  # 가장 최근 날짜 = 실제 치료 시작

# 🎯 비즈니스 임팩트: 치료 효과 분석의 정확성 확보
```

##### **4. 환불/변경사항 실시간 반영 시스템**
```sql
-- 💡 실무 복잡성: 매일 발생하는 변동사항
-- - 환불 처리
-- - 패키지 변경
-- - 추가 처방
-- 📊 해결: 매일 전체 데이터 동기화 시스템 구축

-- 실시간 변동사항 추적 및 반영
SELECT *, CURRENT_TIMESTAMP as last_updated
FROM medical_data 
WHERE modified_date >= CURDATE() - INTERVAL 1 DAY;

-- 🎯 비즈니스 임팩트: 기존 수기 엑셀 → 100% 정확한 자동 시스템
```

---

### 📌 [A/B 테스트: 실험 설계 디테일과 분석적 엄밀성](https://github.com/juncho725/data-analysis-portfolio-kr/03.healthcare-Data-AB-Testing)

#### 🚨 **분석 설계의 핵심 의사결정과 근거**

##### **1. 측정 기간 설정의 과학적 근거**
```python
# 💡 분석 디테일: 왜 150일을 재구매/소개 측정 기간으로 설정했는가?

# 실제 고객 행동 데이터 분석 결과
referral_timing_analysis = {
    '30일 이내': '23%',   # 초기 만족도 기반 소개
    '60일 이내': '51%',   # 1차 효과 실감 후 소개  
    '90일 이내': '73%',   # 주요 소개 발생 구간
    '150일 이내': '87%',  # 대부분의 소개 완료
    '180일 이상': '13%'   # 장기 효과 기반 소개 (소수)
}

# 📊 결정 근거: 전체 소개의 87%가 150일 내 발생 → 충분한 관찰 기간 확보
# 동시에 외부 요인(계절성, 마케팅) 개입 최소화 가능한 기간
measurement_period = 150  # days

# 🎯 분석적 고려: 너무 짧으면 효과 미관측, 너무 길면 외부 요인 증가
```

##### **2. 감량 효과 분석을 위한 검진 기간 세분화**
```python
# 💡 분석 디테일: 왜 50-70일, 70-105일로 기간을 나누었는가?

# 실제 재검진 트래픽 패턴 분석
actual_revisit_pattern = {
    '40-50일': '12%',     # 조기 검진 (불안형 환자)
    '50-70일': '41%',     # 1차 피크 (정상적 경과 확인)
    '70-90일': '28%',     # 2차 피크 (효과 검증)
    '90-105일': '15%',    # 만족도 높은 환자 (여유 검진)
    '105일+': '4%'        # 지연 검진 (효과 미흡 추정)
}

# 📊 설계 논리: 
# Period 1 (50-70일): 초기 효과 측정, 높은 트래픽으로 충분한 샘플 확보
# Period 2 (70-105일): 안정된 효과 측정, 지속성 평가

def analyze_by_revisit_period(data):
    period1_patients = data[(data['revisit_days'] >= 50) & (data['revisit_days'] <= 70)]
    period2_patients = data[(data['revisit_days'] >= 70) & (data['revisit_days'] <= 105)]
    
    # 각 기간별로 독립적 분석 후 일관성 확인
    return period1_analysis, period2_analysis

# 🎯 분석적 엄밀성: 시점별 효과 차이 확인으로 분석 신뢰성 증대
```

##### **3. 베이스라인 통제의 정교한 설계**
```python
# 💡 분석 디테일: 왜 BMI ≥ 25로 베이스라인을 통제했는가?

# 의학적 근거와 데이터 분포 분석
baseline_bmi_analysis = {
    'BMI < 23': {'population': '15%', 'weight_loss_potential': 'Low', 'analysis_inclusion': 'Excluded'},
    'BMI 23-25': {'population': '22%', 'weight_loss_potential': 'Limited', 'analysis_inclusion': 'Excluded'},
    'BMI 25-30': {'population': '48%', 'weight_loss_potential': 'Moderate', 'analysis_inclusion': 'Included'},
    'BMI > 30': {'population': '15%', 'weight_loss_potential': 'High', 'analysis_inclusion': 'Included'}
}

# 📊 통제 근거:
# 1. 의학적 기준: BMI 25+ = 과체중 이상, 실제 감량 효과 측정 가능
# 2. 효과 검정력: 베이스라인이 낮으면 천장 효과로 차이 검출 불가
# 3. 동질성 확보: 유사한 감량 목표를 가진 환자군으로 제한

def baseline_controlled_analysis(patients_data):
    # 엄격한 베이스라인 기준 적용
    eligible_patients = patients_data[
        (patients_data['initial_bmi'] >= 25) &  # 의학적 기준
        (patients_data['is_first_visit'] == True) &  # 신규 환자만
        (patients_data['has_comorbidity'] == False)  # 동반질환 제외
    ]
    
    return eligible_patients

# 🎯 분석 결과: 베이스라인 통제로 순수 처방 방식 효과 99% 신뢰구간에서 검출
```

##### **4. 동일 월 코호트 비교의 설계 논리**
```python
# 💡 분석 디테일: 왜 같은 달에 시작한 환자들끼리만 비교했는가?

# 계절별 자연 체중 변화 패턴 분석
seasonal_weight_patterns = {
    '1-2월': {'natural_loss': '평균 -0.8kg', 'motivation': 'High (신년 다짐)'},
    '3-5월': {'natural_loss': '평균 -0.3kg', 'motivation': 'Medium (봄철 준비)'},
    '6-8월': {'natural_loss': '평균 +0.2kg', 'motivation': 'High (여름 준비)'},
    '9-11월': {'natural_loss': '평균 +0.5kg', 'motivation': 'Low (추위 대비)'},
    '12월': {'natural_loss': '평균 +1.1kg', 'motivation': 'Low (연말 모임)'}
}

# 📊 실험 설계 엄밀성:
def monthly_cohort_comparison(batch_data, split_data):
    results = {}
    for month in range(1, 13):
        # 동일 월 시작 환자만 추출
        batch_monthly = batch_data[batch_data['start_month'] == month]
        split_monthly = split_data[split_data['start_month'] == month]
        
        # 계절 효과가 동일하게 작용하는 조건에서만 비교
        if len(batch_monthly) >= 30 and len(split_monthly) >= 30:  # 통계적 검정력 확보
            results[month] = statistical_test(batch_monthly, split_monthly)
    
    return results

# 🎯 분석적 신뢰성: 계절 효과 완전 제거로 순수 처방 효과만 분리 측정
```

##### **5. 교란 요인 인식과 한계 명시**
```python
# 💡 분석의 정직성: 통제하기 어려운 요인들의 투명한 인식

uncontrollable_confounders = {
    '프로모션_효과': {
        'issue': '대형 이벤트 2개월 전 구매자 재구매율 급증',
        'attempted_control': '프로모션 기간 전후 구분 분석 시도',
        'limitation': '완전한 독립성 확보 어려움 - 고객 심리 잔여 효과 지속',
        'transparency': '분석 결과에 이 한계를 명시적으로 기재'
    },
    '선택_편향': {
        'issue': '분할처방 선택 환자의 특성 차이 (신중함, 소통 빈도)',
        'attempted_control': '베이스라인 특성 비교 및 차이 정량화',
        'limitation': '관찰되지 않는 심리적 특성 차이는 통제 불가',
        'transparency': '연구 제한사항으로 명시하여 해석 시 주의점 제공'
    },
    '외부_마케팅': {
        'issue': 'SNS, 언론보도 등이 소개 의향에 미치는 간접 영향',
        'attempted_control': '마케팅 활동 타임라인 추적 후 전후 비교',
        'limitation': '마케팅 효과의 시차와 개인별 노출 차이 통제 한계',
        'transparency': '완전한 통제 불가능을 인정하고 결과 해석에 반영'
    }
}

# 📊 연구의 과학적 엄밀성: 한계 인식과 투명한 공개
def report_study_limitations():
    return """
    본 연구의 한계점:
    1. 외부 마케팅 요인과의 완전한 독립성 확보 어려움
    2. 환자 선택 편향 가능성 (관찰되지 않는 특성 차이)
    3. 장기적 효과 (6개월+) 측정 제한
    4. 프로모션 효과의 잔여 영향 완전 제거 불가
    
    → 이러한 한계를 고려하여 결과 해석 시 보수적 접근 권장
    """

# 🎯 분석가의 전문성: 완벽한 통제보다는 현실적 한계 인식과 투명성
```

#### **📊 최종 통제된 분석 결과**
```python
# 모든 교란 요인 통제 후 최종 분석
controlled_results = {
    'BMI_reduction': {
        'split_group': 2.3,  # 계절성 통제 후
        'batch_group': 1.8,
        'p_value': 0.023,    # 통계적 유의성 유지
        'controls': ['seasonal', 'baseline_BMI']
    },
    'repurchase_rate': {
        'split_group': 0.42,  # 가격/프로모션 효과 통제 후  
        'batch_group': 0.35,
        'p_value': 0.041,
        'controls': ['price_change', 'promotion_events', 'year_effect']
    },
    'limitations_acknowledged': [
        '완전한 외부 요인 독립성 확보 어려움',
        '선택 편향 가능성 존재',
        '장기 효과 측정 제한'
    ]
}
```

---

## 🏆 실무 복잡성 고려 능력의 차별화 포인트

### **🎯 현실적 제약 조건 완전 이해**
- **정책 변화**: 시기별 규정 변경을 데이터 로직에 반영하는 시스템적 사고
- **워크플로우 복잡성**: 이상적 프로세스 vs 실제 현장 괴리를 데이터로 해결
- **이해관계자 협업**: 의료진, 운영팀 등과의 협의를 통한 비즈니스 로직 정의

### **📊 교란 요인 통제 전문성**
- **외부 이벤트**: 프로모션, 가격 변동, 마케팅 활동 등의 영향 정량 분석
- **계절성 효과**: 자연적 변동 vs 실제 개입 효과 분리
- **선택 편향**: 환자 특성 차이와 그로 인한 분석 한계 투명한 인식

### **🔧 지속 가능한 시스템 설계**
- **확장성**: 정책 변화, 지역 확장 등 미래 변화에 대응 가능한 아키텍처
- **투명성**: 분석 한계와 불확실성을 명시하여 의사결정자에게 정확한 정보 제공
- **실용성**: 완벽한 통제보다는 현실적 제약 하에서 최선의 인사이트 도출

---

## 📫 연락처

<div align="center">

**💡 복잡한 실무 환경의 모든 변수를 고려한 신뢰할 수 있는 데이터 분석 💡**

[![Email](https://img.shields.io/badge/Email-Jun.cho725@gmail.com-red?style=for-the-badge&logo=gmail&logoColor=white)](mailto:Jun.cho725@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jun-cho-8b500a2aa/)

</div>

---

<div align="center">

### *"Real-World Complexity, Real Business Solutions"* 

**실무의 모든 복잡성을 고려하여 신뢰할 수 있는 인사이트를 제공하고, 비즈니스 성과로 연결시킵니다.**

</div>
