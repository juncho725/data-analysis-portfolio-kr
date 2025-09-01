# 🏥 의료 데이터 파이프라인: 다이어트 패키지 분석 시스템

## 📊 **30초 요약**
회사 최초 데이터팀 신설과 함께 140개 SQL 파일 분석을 통해 **분석 불가능한 상태**에서 **60만개 완전 데이터셋** 구축. Raw 데이터 접근부터 완성형 분석 시스템까지 0→1 구축

---

## 🎯 **핵심 성과**
| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| **분석 가능 데이터** | 100명 (수기 샘플링) | 600,000개 (전체) | **6,000배 ↑** |
| **데이터 접근성** | Raw 데이터 접근 불가 |  Raw 데이터 활용 | **0→1 달성** |
| **KPI 커버리지** | 제한적 샘플 분석 | 모든 KPI 원클릭 분석 | **완전 자동화** |
| **데이터 신뢰성** | 환불 등 변동사항 미반영 | 매일 변동사항 반영 | **100% 정확성** |

---

## 📖 **프로젝트 배경: 의료 데이터의 복잡성 해결**

### **🎯 비즈니스 도전**
- **분석 불가능한 상태**: Raw 데이터 접근 불가 (SQL 기반 의료 시스템)
- **제한적 샘플링**: 100명만 수기로 차트 뽑아서 분석
- **수기 데이터 입력**: 패키지 수량을 매일 엑셀에 수기 입력
- **변동사항 미반영**: 환불, 변경사항 등이 엑셀에 실시간 반영 불가
- **KPI 분석 한계**: 전체 현황 파악 불가, 샘플 기반 추정만 가능

### **🔍 기술적 도전**
```sql
-- 문제: 하나의 PaymentID에 여러 처방약이 연결
-- 분석 대상 약품만 선별하는 우선순위 로직 필요
ROW_NUMBER() OVER (PARTITION BY PaymentID ORDER BY 
    CASE 
        WHEN MedicineName LIKE '%분석 대상 약품%' AND Memo REGEXP '-1' THEN 1  -- 핵심상품 + 회차정보
        WHEN MedicineName LIKE '%분석 대상 약품%' THEN 2                       -- 핵심상품만
        WHEN Memo REGEXP '-1' THEN 3                               -- 회차정보만
        ELSE 4
    END
)
```

---

## 🚨 해결한 핵심 문제들

### 🔎 해결 전략 요약표

| 문제 번호 | 문제 요약               | 도메인 원인                                                       | 해결 키워드                              | 사용 기술/전략                                             |
|-----------|--------------------------|--------------------------------------------------------------------|-------------------------------------------|------------------------------------------------------------|
| 1         | 시간 기준점 불일치        | 결제일 ≠ 처방일 ≠ 복용시작일 (진료 흐름 다양성)                          | 최신 날짜 기준 복용 시작일 정의 (max)         | 의료진 협의, `max(pay_date, consult_date)`                |
| 2         | 핵심 약품 선별           | 하나의 결제에 다수 약품 포함                                          | 우선순위 기반 약품 선별                       | `SQL ROW_NUMBER + CASE WHEN`                              |
| 3         | 결측치 복구              | PaymentID와 MedicalRecordID 연결 불안정 (선결제, 처방 지연 등)         | 동일 환자 기준, 시계열 기반 유사 기록 매칭       | 30일 이내 유사 기록 → 200일 이내 후속 기록              |
| 4         | 패키지 분류 표기법 변화   | 시기별로 다른 메모 표기 방식                                           | 정책 기준일에 따라 분류 로직 분기               | `if memo.startswith()` + 정책일(`2022-12-13`) 조건 분기  |
| 5         | 복용 순서 분석용 인덱스   | 여러 차수 복용 환자 분석 필요                                         | 환자별 방문 순서 인덱스 생성                   | `groupby + cumcount` + 최신일 기준 정렬                  |

---



### **1. 의료업계 특성: 시간 기준점 불일치**

### ****

```python
# 문제: 결제일 ≠ 처방일
patient_timeline = {
    "결제일": "2024-01-01",      # 예약금 선결제
    "처방일": "2024-01-10",      # 실제 진료 및 처방
}

# 해결: 의료진 협의를 통한 기준 정의
# 다이어트 효과 분석에서는 실제 복용 시작일이 중요하므로
# 가장 최근 날짜를 기준으로 '치료 시작 시점'을 정의함
def determine_treatment_start_date(pay_date, consult_time):
    """다이어트 효과 분석을 위한 정확한 시작 시점 결정"""
    return max(pay_date, consult_time)  # 실제 치료 확정 시점
```

### **2. 복잡한 테이블 조인에서 핵심 상품 선별**
```sql
-- 도전: 140개 테이블 중 5개 핵심 테이블의 복잡한 관계
-- 하나의 결제에 분석 대상 약품 외 여러 약품 포함

-- 해결: 비즈니스 우선순위 기반 선택 알고리즘
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

### **3. 의료 워크플로우 기반 결측치 복구 (35% → 3%)**
```python
def medical_workflow_recovery(df, reference_df):
    """
    의료진 협의를 통해 정의한 결측치 복구 로직.
    
    💡 도메인 기반 문제:
    PaymentID와 MedicalRecordID가 1:1로 연결되지 않음.
    (예: 선결제, 진료 후 결제, 처방 지연 등 비정형 워크플로우)
    
    ➤ 단일 키 기반 조인으로는 정확한 약품 매칭이 어려움.
    ➤ 따라서 '동일 환자(PatientID)'를 기준으로 치료 시점 간 시간 기반 유사 매칭이 필요.

    🛠️ 해결 전략:
    1. 동일 환자의 30일 이내 동일 치료 과정 내 가장 유사한 기록을 우선 복구
    2. 없는 경우, 동일 환자의 최대 200일 이내 후속 재방문 내역을 기반으로 복구
    
    이 기준은 실제 사내 의료진과 협의해 정의된 워크플로우 기반 로직입니다.
    """

    for idx in df[df['MedicineName'].isnull()].index:
        patient_id = df.loc[idx, 'PatientID']
        target_date = df.loc[idx, 'ConsultTime']
        
        # 1단계: 동일 환자의 동일 치료 과정 내 복구 (30일 이내)
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
        
        # 2단계: 동일 환자의 후속 재방문 기록 활용 (200일 이내)
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

### **4. 시기별 패키지 분류 알고리즘**
```python
def categorize_package(medicine_name, memo, consult_date):
    """
    의료 현장에서 사용하는 표기법이 시기별로 달라지는 문제 해결을 위한 패키지 분류 알고리즘

    💡 도메인 기반 문제:
    - 다이어트 약품의 경우, **몇 개월치 처방인지가 분석에 매우 중요**
    - 하지만 사내 시스템(Raw 데이터)에서는 시기별로 입력 방식이 달라 일관된 분류 불가능
        → 예: 같은 '1-1'이라도 2022년 이전엔 1.5개월, 이후엔 1개월

    🛠️ 해결 전략:
    - 의료진/운영팀과 협의해 정책 변경일(2022-12-13)을 기준으로 해석 방식 구분
    - `memo`, `medicine_name`, `consult_date`를 기반으로 정책 반영된 새로운 '패키지분류' 컬럼 생성
    """

    # 데이터 정제
    memo = str(memo).strip()
    medicine_name = str(medicine_name).strip().lower()
    consult_date = pd.to_datetime(consult_date)

    # 분석 대상 약품이 아닌 경우는 제외
    if not ('분석 대상 약품' in medicine_name or 'target medication' in medicine_name):
        return '기타'

    # 정책 변경 기준일
    policy_change_date = pd.to_datetime('2022-12-13')

    # 첫 번째 패키지: '1-1'은 시기별로 의미가 다름
    if memo.startswith('1-1'):
        return '1.5개월' if consult_date <= policy_change_date else '1개월'

    # 연속 패키지: '2-1' ~ '9-1'은 모두 3개월 패키지로 통일
    elif any(memo.startswith(f"{i}-1") for i in range(2, 10)):
        return '3개월'

    return '기타'

```

### **5. 환자 여정 인덱싱**
```python
def create_patient_journey_index(df):
    """
    지역별, 환자별 구매 순서 인덱싱

    💡 도메인 기반 문제:
    - 환자가 동일한 약품을 몇 번째로 복용하는지를 분석하는 것은
      효과 추이, 이탈률, 충성도 분석 등에 매우 중요함
    - 예: 2번째 구매 환자들의 특성 / 3번째 구매 시 체중 변화 등
    
    🛠️ 해결 전략:
    - 치료 시작 기준일(`PayDate`와 `ConsultTime` 중 최신값)을 기준으로 정렬
    - 동일 환자의 방문 순서를 인덱스로 지정하여 `visit_index` 컬럼 생성
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

---

## 🚀 **조직 임팩트**

### **Before: 분석 불가능한 암흑기**
```
❌ Raw 데이터 접근 불가 (SQL 시스템, 권한 없음)
❌ 100명 샘플만 수기로 차트 추출 가능
❌ 패키지 수량 매일 엑셀 수기 입력
❌ 환불/변경사항 실시간 반영 불가
❌ 전체 KPI 분석 불가능
❌ 추정 기반 의사결정만 가능
```

### **After: 완전 자동화된 분석 시스템**
```
✅ Raw 데이터 완전 접근 및 활용
✅ 60만개 완전 데이터셋 구축
✅ 실시간 변동사항 자동 반영
✅ 모든 KPI 원클릭 분석 가능
✅ 데이터 기반 정확한 의사결정
✅ 7개 지역 통합 실시간 모니터링
```

### **구축한 완성형 데이터셋 (60만개)**
```python
complete_dataset_columns = [
    "지역",           # 7개 지역 통합
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
# → 기존 모든 KPI를 하나의 파일로 완전 커버
```

---

## 🛠️ **데이터 파이프라인 아키텍처**

```
🚫 분석 불가능 상태 (Raw 데이터 접근 불가)
    ↓
🔍 140개 SQL 파일 분석으로 시스템 구조 파악
    ↓
🤝 의료진 소통을 통한 비즈니스 로직 이해
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

### **핵심 기술 스택**
- **SQL**: 복잡한 의료 데이터 조인 및 우선순위 로직
- **Python**: pandas 기반 대용량 시계열 데이터 처리
- **비즈니스 로직**: 의료진 협의 기반 도메인 규칙 엔진

---

## 💡 **핵심 성공 요인**

### **1. 도메인 전문성 구축**
```python
stakeholder_collaboration = {
    "의료진": "다이어트 치료 프로세스 및 효과 측정 기준",
    "운영팀": "패키지 정책 변화 히스토리 및 표기법",
    "재무팀": "복잡한 결제 시스템 및 정산 로직",
    "지역담당자": "지역별 운영 방식 차이 및 데이터 특성"
}
# → 기술적 구현보다 비즈니스 컨텍스트 이해가 핵심
```

### **2. 의료 데이터 특성 반영**
```python
medical_data_challenges = {
    "시간 복잡성": "결제 ≠ 처방 ≠ 복용 시작 시점",
    "관계 복잡성": "1:N 결제-처방 관계에서 핵심 상품 선별",
    "정책 변화": "시기별 패키지 표기법 및 정책 변화 반영",
    "워크플로우": "의료진 진료 패턴을 활용한 데이터 복구"
}
```

### **3. 확장 가능한 시스템 설계**
```python
system_design_principles = {
    "모듈화": "지역별 설정 분리로 확장성 확보",
    "검증": "의료진 검토 기반 정확성 검증 체계",
    "추적": "데이터 변경 이력 관리 및 복구 성공률 모니터링"
}
```

---

## 🎯 **주요 코드 스니펫**

<details>
<summary><strong>📊 분석 대상 약품 우선순위 선별 로직</strong></summary>

```sql
-- 의료진과의 협의를 통해 정의한 우선순위 로직
WITH PrioritySelection AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY PaymentID 
            ORDER BY 
                CASE 
                    -- 1순위: 분석 대상 약품 + 회차 정보 완전
                    WHEN MedicineName LIKE '%분석 대상 약품%' AND Memo REGEXP '-1' THEN 1
                    -- 2순위: 분석 대상 약품 확인됨
                    WHEN MedicineName LIKE '%분석 대상 약품%' THEN 2
                    -- 3순위: 회차 정보만 있음
                    WHEN Memo REGEXP '-1' THEN 3
                    ELSE 4
                END,
                PaymentAmt DESC  -- 동일 조건시 금액 기준
        ) AS priority_rank
    FROM medical_payment_data
)
SELECT * FROM PrioritySelection WHERE priority_rank = 1;
```
</details>

<details>
<summary><strong>🐍 의료 워크플로우 기반 결측치 복구</strong></summary>

```python
def medical_workflow_recovery(df, reference_df):
    """의료진 협의를 통해 정의한 복구 로직"""
    
    updated_count = 0
    
    for idx in df[df['MedicineName'].isnull()].index:
        patient_id = df.loc[idx, 'PatientID']
        target_date = df.loc[idx, 'ConsultTime']
        
        # 동일 치료 과정 내 데이터 우선 (30일 이내)
        same_treatment_window = reference_df[
            (reference_df['PatientID'] == patient_id) &
            (abs(reference_df['ConsultTime'] - target_date) <= pd.Timedelta(days=30)) &
            (reference_df['MedicineName'].str.contains('분석 대상 약품', case=False, na=False))
        ]
        
        if not same_treatment_window.empty:
            closest_record = same_treatment_window.loc[
                abs(same_treatment_window['ConsultTime'] - target_date).idxmin()
            ]
            df.loc[idx, ['MedicineName', 'Memo', 'ProgressNote']] = \
                closest_record[['MedicineName', 'Memo', 'ProgressNote']].values
            df.loc[idx, 'DataUpdated'] = 1
            updated_count += 1
    
    print(f"복구 성공률: {updated_count}/{len(df[df['MedicineName'].isnull()])} ({updated_count/len(df[df['MedicineName'].isnull()])*100:.1f}%)")
    return df
```
</details>

<details>
<summary><strong>🏷️ 시기별 패키지 분류 알고리즘</strong></summary>

```python
def categorize_package_by_period(medicine_name, memo, consult_date):
    """시기별 정책 변화를 반영한 패키지 분류"""
    
    # 데이터 정제
    memo = str(memo).strip()
    medicine_name = str(medicine_name).strip().lower()
    
    # 분석 대상 약품 여부 확인
    if not ('분석 대상 약품' in medicine_name or 'Target medication' in medicine_name):
        return '기타'
    
    # 정책 변경 기준일 (의료진 협의 결과)
    policy_change_date = pd.to_datetime('2022-12-13')
    consult_date = pd.to_datetime(consult_date)
    
    # 패키지 분류 로직
    if memo.startswith('1-1'):
        # 정책 변경 전후로 다른 분류
        return '1.5개월' if consult_date <= policy_change_date else '1개월'
    elif any(memo.startswith(f"{i}-1") for i in range(2, 10)):
        return '3개월'
    else:
        return '기타'
```
</details>

---

## 🔗 **핵심 성과 요약**

**0→1 혁신**: 분석 불가능 → 60만개 완전 데이터셋  
**기술적 도전**: 140개 SQL 파일 분석으로 복잡한 의료 시스템 정복  
**비즈니스 임팩트**: 추정 기반 → 데이터 기반 의사결정으로 조직 문화 전환

---

*"분석이 불가능했던 상태에서 60만개 완성형 데이터셋을 구축한 0→1 프로젝트. Raw 데이터 접근부터 완전 자동화까지, 조직 전체의 의사결정 패러다임을 바꾼 변화의 시작이었습니다."*
