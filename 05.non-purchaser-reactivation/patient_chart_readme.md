# Patient Chart Number Analysis Project

## 프로젝트 개요
다이어트 약품 판매 회사의 첫 데이터 부서 구축 과정에서 발견한 중요한 비즈니스 인사이트를 바탕으로 한 데이터 분석 프로젝트입니다.

## 배경
- 회사 최초 데이터 부서 입사 후 데이터 시스템 구축 담당
- 데이터 클리닝 및 체계화 과정에서 **차트번호는 없지만 문의 기록은 남긴 환자들**이 상당수 존재함을 발견
- 이들은 문의만 하고 실제 구매로 이어지지 않은 잠재 고객층

## 문제 정의
**핵심 발견**: 문의만 하고 구매하지 않는 환자들의 데이터가 대량 축적되어 있음
- 이들은 구매 의향은 있으나 실행하지 않은 warm lead
- 적절한 마케팅 접근으로 구매 전환 가능성이 높은 타겟층

## 솔루션 제안
### 1. 법적 검토
- 의료법 검토를 통해 해당 고객들에게 이벤트/광고 푸시 발송이 가능함을 확인

### 2. 정교한 타겟 고객 식별 로직
**핵심 비즈니스 로직**: 진짜 "문의만 하고 구매 안 한 사람들"을 정확히 찾기
- **1단계**: SQL로 차트번호 없는 문의 고객 추출
- **2단계**: 전체 고객에서 차트번호 없는 고객 제외하여 "실제 구매 고객" 그룹 생성
- **3단계**: **교차 검증** - 문의 고객이 나중에 실제 구매했는지 휴대폰번호로 대조
  - **비즈니스 중요성**: 문의 후 구매한 고객을 마케팅 대상에서 제외해야 함
- **4단계**: 데이터 품질 검증으로 유효한 연락처만 추출

### 3. 최적 타이밍 데이터 분석
**핵심 인사이트 발굴**: 문의 후 나중에 구매하는 고객들의 구매 패턴 분석
- 문의 후 바로 구매하지 않고 나중에 구매하는 고객 명단 추출
- 문의부터 구매까지의 기간 분포 분석
- **데이터 기반 결론**: 2주 후 구매율이 최고점 → **최적 푸시 타이밍 = 2주**

## 기술적 구현

### 핵심 비즈니스 로직
```python
# 1. 정교한 타겟 고객 식별
# 차트번호 없는 문의 고객 vs 실제 구매 고객 교차 검증
no_chart_customers = set(zip(df_no_chart['Region'], df_no_chart['Patientid']))
purchased_customers = df_all[~df_all.apply(lambda row: (row['Region'], row['Patientid']) in no_chart_customers, axis=1)]

# 2. 중복 제거: 문의 후 나중에 구매한 고객 제외
true_prospects = df_no_chart[~df_no_chart['PatientCellphone'].isin(purchased_customers['PatientCellphone'])]

# 3. 마케팅 가능한 품질 데이터만 추출
def is_valid_phone(phone):
    return len(str(int(phone))) == 10 if isinstance(phone, (int, float)) else len(phone.strip()) == 10

final_targets = true_prospects[true_prospects['PatientCellphone'].apply(is_valid_phone)]
```

### 데이터 플로우
```
SQL 추출 → 교차 검증 → 중복 제거 → 품질 검증 → 마케팅 타겟 리스트
```

### 주요 파일
- `PatientChartNo_Blank.ipynb`: 전체 데이터 처리 파이프라인
- `All_Branch_No_Blank.xlsx`: 차트번호 없는 환자 데이터
- `All_Branch.xlsx`: 전체 환자 데이터  
- `Verified_Patient_Data1.xlsx`: 검증된 마케팅 대상 리스트
- `Outlier_Patient_Data1.xlsx`: 이상치 데이터

## 비즈니스 임팩트
- **새로운 수익 채널 발견**: 기존 미활용 데이터에서 마케팅 기회 창출
- **데이터 기반 타이밍 전략**: 고객 구매 패턴 분석으로 최적 푸시 시점(2주) 도출
- **정교한 타겟팅**: 교차검증을 통한 진짜 잠재 고객만 식별
- **체계적 접근**: 법적 검토부터 실행까지 전 과정 구조화

## 기술 스택
- **Python**: 데이터 처리 및 분석
- **Pandas**: 데이터 조작 및 필터링
- **Excel**: 데이터 저장 및 관리

## 학습 포인트
1. **정교한 고객 세분화**: 단순 필터링이 아닌 다단계 교차검증으로 정확한 타겟 식별
2. **비즈니스 로직 설계**: "문의만 하고 구매 안 한 사람"을 정의하고 구현하는 복잡한 로직
3. **데이터 품질 관리**: 마케팅 효과를 위한 연락처 유효성 검증
4. **법적 고려사항**: 의료 관련 마케팅의 법적 제약 검토
5. **실험 설계**: A/B 테스트를 통한 최적 전략 도출

## 결과
회사 최초로 잠재 고객 재활성화 전략을 데이터 기반으로 제안하여, 새로운 마케팅 채널을 구축하고 구매 전환율 향상에 기여했습니다.
