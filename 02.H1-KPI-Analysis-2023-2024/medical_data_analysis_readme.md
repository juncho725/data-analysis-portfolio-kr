# Healthcare Data Analysis (2023 vs 2024)

의료 서비스 데이터 2년간 비교 분석으로 핵심 KPI 변화 파악

## 🎯 분석 목적
2023년 vs 2024년 상반기 의료 서비스 운영 지표 비교를 통한 비즈니스 인사이트 도출

## 📊 핵심 KPI 비교

### 1. 환자 유입량
- **월별 신규 환자 수** 변화 추이

<img src="https://github.com/user-attachments/assets/fd81dcd8-9d34-47ac-b2c0-586c59ec994f" width="500px">
 
- **지점별 유입량** 비교


### 2. 고객 프로필 변화  
- **연령대별 분포** 변화

<img src="https://github.com/user-attachments/assets/49508c05-2051-4ae0-892c-303e3b0f8f79" width="500px">
 
- **성별 비율** 변화

<img src="https://github.com/user-attachments/assets/c00f032d-9eea-4f23-8a9d-548c3857604f" width="500px">

### 3. 매출 성과
- **지점별 월별 매출** 비교
- **환자당 평균 구매액** 변화

### 4. 고객 유지율
- **재구매 고객 비율** 분석

<img src="https://github.com/user-attachments/assets/00cb4950-646f-48e5-a39c-082ee494a8f1" width="500px">

- **이탈율** 비교

## 🔍 주요 발견

| KPI | 2023 | 2024 | 변화율 |
|-----|------|------|--------|
| 총 환자 수 | 25,430명 | 22,850명 | **-10.1%** ↓ |
| 평균 구매액 | 285,000원 | 295,000원 | **+3.5%** ↑ |
| 재구매율 | 32% | 36% | **+4%p** ↑ |
| 30-40대 비율 | 38.2% | 35.1% | **-3.1%p** ↓ |

## 🛠 기술 스택
- **Python** (pandas, matplotlib, seaborn)
- **통계 분석** (scipy - T-검정)

## 📈 통계 검증
- **T-검정**: 연도별 유의미한 차이 확인 (p < 0.05)
- **신뢰구간**: 95% 신뢰도로 분석 수행
- **표본크기**: 충분한 데이터로 통계적 타당성 확보
- **검정 결과**: 환자 유입량 감소, 재구매율 개선 모두 통계적 유의성 입증



## 🚀 실행
```bash
pip install pandas matplotlib seaborn scipy
python analysis.py
```

## 💡 핵심 인사이트
- **환자 수 감소**하지만 **고객 질 개선** (재구매율↑, 구매액↑)  
- **30-40대 주력 고객층 감소** → 마케팅 전략 재검토 필요
- **지점별 성과 편차** 존재 → 우수 지점 성공 요인 분석 필요
