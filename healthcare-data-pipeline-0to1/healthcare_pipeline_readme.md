# 🏥 의료 데이터 파이프라인: 다이어트 패키지 분석 시스템

## 📋 프로젝트 개요

**"분석 불가능한 상태에서 60만개 완전 데이터셋 구축"**

회사 최초 데이터팀 신설과 함께 Raw 데이터 접근이 불가능한 상황에서 140개 SQL 파일 분석을 통해 의료 시스템을 파악하고, **수기 샘플링(100명)에서 전체 데이터(60만개) 자동화 분석**까지 0→1 시스템을 구축한 프로젝트입니다.

의료 데이터의 복잡성(시간 기준점 불일치, 복잡한 테이블 관계, 정책 변화 등)을 해결하여 조직의 의사결정을 **추정 기반에서 데이터 기반**으로 전환했습니다.

---

## 🎯 핵심 성과

| 항목 | Before | After | 개선율 |
|------|--------|-------|--------|
| **분석 가능 데이터** | 100명 (수기 샘플링) | 600,000개 (전체) | **6,000배 ↑** |
| **데이터 접근성** | Raw 데이터 접근 불가 | Raw 데이터 완전 활용 | **0→1 달성** |
| **KPI 분석** | 제한적 샘플 분석 | 모든 KPI 원클릭 분석 | **완전 자동화** |
| **데이터 정확성** | 환불 등 변동사항 미반영 | 실시간 변동사항 반영 | **100% 정확성** |

---

## 🔍 핵심 문제 해결 요약

| 문제 | 도메인 배경 | 해결 전략 | 핵심 기술 |
|------|-------------|-----------|-----------|
| **시간 기준점 불일치** | 결제일 ≠ 처방일 ≠ 복용시작일 | 의료진 협의를 통한 치료 시작 기준 정의 | `max(pay_date, consult_date)` |
| **핵심 약품 선별** | 하나의 결제에 다수 약품 포함 | 비즈니스 우선순위 기반 선택 알고리즘 | `SQL ROW_NUMBER + CASE WHEN` |
| **결측치 복구** | PaymentID-MedicalRecordID 연결 불안정 | 동일 환자 기준 시계열 유사 매칭 | 30일→200일 단계적 매칭 로직 |
| **패키지 분류 변화** | 시기별 메모 표기법 차이 | 정책 기준일 기반 분류 로직 분기 | 2022-12-13 기준 조건부 처리 |
| **복용 순서 인덱싱** | 환자별 치료 여정 분석 필요 | 환자별 방문 순서 자동 생성 | `groupby + cumcount` |

---

## 💡 주요 문제 해결 과정

### 1️⃣ 의료업계 특성: 시간 기준점 불일치 문제

**🔍 문제 상황**  
의료 시스템에서는 결제일과 처방일이 다를 수 있어 정확한 치료 시작 시점 파악이 어려웠습니다.

```python
# 문제: 결제일 ≠ 처방일로 인한 분석 기준점 혼재
patient_timeline = {
    "결제일": "2024-01-01",      # 예약금 선결제
    "처방일": "2024-01-10",      # 실제 진료 및 처방
}

# 해결: 의료진 협의를 통한 치료 시작 기준 정의
def determine_treatment_start_date(pay_date, consult_time):
    """다이어트 효과 분석을 위한 정확한 시작 시점 결정"""
    return max(pay_date, consult_time)  # 실제 치료 확정 시점
```

**💡 해결 결과**  
의료진과의 협의를 통해 "실제 복용 시작일"을 가장 최근 날짜로 정의하여 일관된 분석 기준을 확립했습니다.

---

### 2️⃣ 복잡한 테이블 조인에서 핵심 상품 선별

**🔍 문제 상황**  
하나의 결제에 분석 대상 약품 외 여러 약품이 포함되어 정확한 타겟 데이터 추출이 어려웠습니다.

```sql
-- 140개 테이블 중 핵심 관계 파악 후 우선순위 기반 선택 로직 구현
WITH PriorityRanking AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY PaymentID ORDER BY 
            CASE 
                -- 1순위: 분석 대상 약품 + 회차 정보 완전 매칭
                WHEN MedicineName LIKE '%분석 대상 약품%' AND Memo REGEXP '-1' THEN 1
                -- 2순위: 분석 대상 약품만 확인됨
                WHEN MedicineName LIKE '%분석 대상 약품%' THEN 2
                -- 3순위: 회차 정보만 있음 (약명 결측)
                WHEN Memo REGEXP '-1' THEN 3
                ELSE 4
            END,
            PaymentAmt DESC  -- 동일 조건시 금액 기준 정렬
        ) AS priority_rank
    FROM medical_data
)
SELECT * FROM PriorityRanking WHERE priority_rank = 1;
```

**💡 해결 결과**  
비즈니스 우선순위를 반영한 선택 알고리즘으로 정확한 핵심 약품 데이터만 추출하여 분석 정확도를 높였습니다.

---

### 3️⃣ 의료 워크플로우 기반 결측치 복구 (35% → 3%)

**🔍 문제 상황**  
PaymentID와 MedicalRecordID가 1:1로 연결되지 않아 35%의 결측치가 발생했습니다.

```python
def medical_workflow_recovery(df, reference_df):
    """
    의료진 협의를 통해 정의한 결측치 복구 로직
    
    핵심 아이디어:
    - 동일 환자의 30일 이내 동일 치료 과정 내 가장 유사한 기록 우선 복구
    - 없는 경우, 200일 이내 후속 재방문 내역을 기반으로 복구
    """
    
    for idx in df[df['MedicineName'].isnull()].index:
        patient_id = df.loc[idx, 'PatientID']
        target_date = df.loc[idx, 'ConsultTime']
        
        # 1단계: 동일 치료 과정 내 복구 (30일 이내)
        same_treatment = reference_df[
            (reference_df['PatientID'] == patient_id) &
            (abs(reference_df['ConsultTime'] - target_date) <= pd.Timedelta(days=30)) &
            (reference_df['MedicineName'].str.contains('분석 대상 약품', na=False))
        ]
        
        if not same_treatment.empty:
            closest_record = same_treatment.loc[
                abs(same_treatment['ConsultTime'] - target_date).idxmin()
            ]
            df.loc[idx, ['MedicineName', 'Memo', 'ProgressNote']] = \
                closest_record[['MedicineName', 'Memo', 'ProgressNote']].values
            df.loc[idx, 'DataUpdated'] = 1
            continue
        
        # 2단계: 후속 재방문 기록 활용 (200일 이내)
        extended_search = reference_df[
            (reference_df['PatientID'] == patient_id) &
            (reference_df['ConsultTime'] > target_date) &
            (reference_df['ConsultTime'] - target_date <= pd.Timedelta(days=200))
        ]
        
        if not extended_search.empty:
            next_visit = extended_search.sort_values('ConsultTime').iloc[0]
            df.loc[idx, ['MedicineName', 'Memo']] = \
                next_visit[['MedicineName', 'Memo']].values
            df.loc[idx, 'DataUpdated'] = 1

    return df
```

**💡 해결 결과**  
의료 워크플로우를 이해한 시계열 기반 매칭으로 결측치를 35%에서 3%로 대폭 감소시켰습니다.

---

### 4️⃣ 시기별 패키지 분류 알고리즘

**🔍 문제 상황**  
같은 메모 표기('1-1')라도 시기에 따라 다른 패키지 분류(1개월 vs 1.5개월)를 의미했습니다.

```python
def categorize_package(medicine_name, memo, consult_date):
    """
    시기별 패키지 분류 정책 변화를 반영한 자동 분류 알고리즘
    
    배경: 의료 현장에서 사용하는 표기법이 시기별로 달라지는 문제
    - 같은 '1-1'이라도 2022년 이전엔 1.5개월, 이후엔 1개월
    """
    
    # 데이터 정제
    memo = str(memo).strip()
    medicine_name = str(medicine_name).strip().lower()
    consult_date = pd.to_datetime(consult_date)
    
    # 분석 대상 약품이 아닌 경우는 제외
    if not ('분석 대상 약품' in medicine_name or 'target medication' in medicine_name):
        return '기타'
    
    # 정책 변경 기준일 (운영팀 협의 결과)
    policy_change_date = pd.to_datetime('2022-12-13')
    
    # 첫 번째 패키지: '1-1'은 시기별로 의미가 다름
    if memo.startswith('1-1'):
        return '1.5개월' if consult_date <= policy_change_date else '1개월'
    
    # 연속 패키지: '2-1' ~ '9-1'은 모두 3개월 패키지로 통일
    elif any(memo.startswith(f"{i}-1") for i in range(2, 10)):
        return '3개월'
    
    return '기타'
```

**💡 해결 결과**  
정책 변경일을 기준으로 한 조건부 처리로 시기별 정책 차이를 정확하게 반영한 패키지 분류를 자동화했습니다.

---

### 5️⃣ 환자 여정 인덱싱

**🔍 문제 상황**  
환자별 복용 순서 분석(첫 구매, 재구매 등)을 위한 방문 순서 정보가 필요했습니다.

```python
def create_patient_journey_index(df):
    """
    환자별 치료 여정 인덱싱
    
    목적: 환자가 몇 번째로 복용하는지 분석
    - 효과 추이, 이탈률, 충성도 분석에 필수
    """
    
    # 정확한 치료 시작 시점 기준 정렬
    df['Confirm_date'] = df.apply(
        lambda row: max(row['PayDate'], row['ConsultTime']) 
        if pd.notna(row['PayDate']) and pd.notna(row['ConsultTime'])
        else (row['ConsultTime'] if pd.isna(row['PayDate']) else row['PayDate']),
        axis=1
    )
    
    # 환자별 방문 순서 인덱싱
    df['visit_index'] = (
        df.sort_values(['Region', 'PatientID', 'Confirm_date'])
        .groupby(['Region', 'PatientID'])
        .cumcount() + 1
    )
    
    return df
```

**💡 해결 결과**  
환자별 방문 순서를 자동으로 인덱싱하여 복용 단계별 효과 분석과 이탈률 분석이 가능해졌습니다.

---

## 🏗️ 시스템 아키텍처 및 데이터 플로우

```
🚫 분석 불가능 상태 (Raw 데이터 접근 불가)
    ↓
🔍 140개 SQL 파일 분석으로 시스템 구조 파악
    ↓
🤝 의료진·운영팀과 협의하여 비즈니스 로직 이해
    ↓
🗃️ Raw 데이터 접근 권한 확보 및 추출
    ↓
🔧 복잡한 조인 + 비즈니스 우선순위 필터링  
    ↓
🩹 의료 워크플로우 기반 결측치 복구 (90% 성공)
    ↓
📅 시간 기준점 통일 (의료진 협의 기준)
    ↓
🏷️ 시기별 패키지 분류 알고리즘 구현
    ↓
🌐 7개 지역 통합 + 중복 제거
    ↓
📊 환자 여정 인덱싱
    ↓
💎 60만개 완성형 데이터셋 (모든 KPI 커버)
```

---

## 📊 구축된 완성형 데이터셋

**60만개 완전 데이터셋 구성**

```python
complete_dataset_columns = [
    "지역",           # 7개 지역 통합 관리
    "차트번호",        # 환자 고유 식별자
    "첫방문날짜",      # 환자 유입 시점
    "처방약",         # 다이어트 패키지 정보
    "핸드폰번호",      # 환자 연락처
    "진료노트",       # 환자 질환, 체중, 골격근량, 지방량
    "나이",          # 환자 나이
    "성별",          # 환자 성별  
    "주민번호",       # 환자 식별
    "약수령날짜",      # 실제 복용 시작일
    "패키지분류",      # 1개월/1.5개월/3개월 자동 분류
    "복용횟수"        # 환자별 방문 순서 인덱스
]
```

**기존 모든 KPI를 하나의 완성형 데이터셋으로 통합하여 원클릭 분석이 가능해졌습니다.**

---

## 🔧 핵심 기술 스택

- **SQL**: 복잡한 의료 데이터 조인 및 우선순위 로직 구현
- **Python (pandas)**: 대용량 시계열 데이터 처리 및 결측치 복구
- **도메인 로직 엔진**: 의료진 협의 기반 비즈니스 규칙 자동화

---

## 💡 핵심 성공 요인

### 1. **도메인 전문성 구축**
```python
stakeholder_collaboration = {
    "의료진": "다이어트 치료 프로세스 및 효과 측정 기준",
    "운영팀": "패키지 정책 변화 히스토리 및 표기법",
    "재무팀": "복잡한 결제 시스템 및 정산 로직",
    "지역담당자": "지역별 운영 방식 차이 및 데이터 특성"
}
```

### 2. **의료 데이터 특성 이해**
- **시간 복잡성**: 결제 ≠ 처방 ≠ 복용 시작 시점
- **관계 복잡성**: 1:N 결제-처방 관계에서 핵심 상품 선별
- **정책 변화**: 시기별 패키지 표기법 및 정책 변화 반영
- **워크플로우**: 의료진 진료 패턴을 활용한 데이터 복구

### 3. **확장 가능한 시스템 설계**
- **모듈화**: 지역별 설정 분리로 확장성 확보
- **검증**: 의료진 검토 기반 정확성 검증 체계
- **추적**: 데이터 변경 이력 관리 및 복구 성공률 모니터링

---

## 🎯 프로젝트 임팩트 및 의미

### **조직 변화**
- **Before**: 추정 기반 의사결정 (제한적 샘플 분석)
- **After**: 데이터 기반 정확한 의사결정 (전체 데이터 실시간 분석)

### **업무 효율성**
- **Before**: 매일 수기 엑셀 입력, 환불 등 변동사항 미반영
- **After**: 완전 자동화, 실시간 변동사항 반영

### **분석 역량**
- **Before**: 100명 샘플링, KPI 분석 불가
- **After**: 60만개 완전 데이터셋, 모든 KPI 원클릭 분석

---

## 🏆 결론

**"0→1 혁신을 통한 조직 전체의 패러다임 전환"**

분석이 불가능했던 상태에서 60만개 완성형 데이터셋을 구축한 이 프로젝트는 단순한 기술적 성취를 넘어 조직 전체의 의사결정 패러다임을 바꾼 변화의 시작이었습니다.

140개 SQL 파일 분석부터 시작하여 복잡한 의료 도메인의 비즈니스 로직을 이해하고, 이를 기술적으로 구현하여 **추정 기반에서 데이터 기반 의사결정**으로의 전환을 이끌어낸 것이 가장 큰 성과입니다.

**핵심 키워드**: `0→1 프로젝트` `도메인 전문성` `의료 데이터` `시스템 아키텍처` `조직 임팩트`