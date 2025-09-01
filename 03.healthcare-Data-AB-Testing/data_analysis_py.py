# 다이어트 처방 A/B 테스트 분석
# 목적: 3개월 일괄처방 vs 1.5개월 분할처방 효과 비교

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest

# =============================================================================
# 1. BMI 감소 효과 분석
# =============================================================================
def analyze_weight_loss(batch_group_file, split_group_file):
    """
    일괄처방 그룹과 분할처방 그룹의 BMI 감소 효과를 비교하는 함수
    
    Args:
        batch_group_file: 일괄처방(3개월) 그룹 데이터 파일
        split_group_file: 분할처방(1.5개월x2) 그룹 데이터 파일
    
    Returns:
        True/False: 통계적으로 유의한 차이가 있는지 여부 (p<0.05)
    """
    print("=== BMI 감소 효과 분석 ===")
    
    # 엑셀 파일에서 데이터 읽어오기
    batch_group_data = pd.read_excel(batch_group_file)      # 일괄처방 그룹
    split_group_data = pd.read_excel(split_group_file)      # 분할처방 그룹
    
    # 일괄처방 그룹 BMI 계산
    batch_group_data['before_bmi'] = batch_group_data['weight_initial'] / (batch_group_data['height']/100)**2
    batch_group_data['after_bmi'] = batch_group_data['weight_followup'] / (batch_group_data['height']/100)**2
    batch_group_data['bmi_decrease'] = batch_group_data['before_bmi'] - batch_group_data['after_bmi']
    
    # 분할처방 그룹 BMI 계산
    split_group_data['before_bmi'] = split_group_data['weight_initial'] / (split_group_data['height']/100)**2
    split_group_data['after_bmi'] = split_group_data['weight_followup'] / (split_group_data['height']/100)**2
    split_group_data['bmi_decrease'] = split_group_data['before_bmi'] - split_group_data['after_bmi']
    
    # T-test로 두 그룹의 평균 BMI 감소량 비교
    test_statistic, p_value = stats.ttest_ind(split_group_data['bmi_decrease'], 
                                              batch_group_data['bmi_decrease'])
    
    # 각 그룹의 평균 BMI 감소량 계산
    split_group_average = split_group_data['bmi_decrease'].mean()
    batch_group_average = batch_group_data['bmi_decrease'].mean()
    
    # 결과 출력
    print(f"분할처방 그룹 평균 BMI 감소량: {split_group_average:.2f}")
    print(f"일괄처방 그룹 평균 BMI 감소량: {batch_group_average:.2f}")
    print(f"p-value (유의성 검정 결과): {p_value:.4f}")
    
    # 통계적 유의성 판단 (p<0.05이면 유의함)
    has_significant_difference = p_value < 0.05
    if has_significant_difference:
        print("결과: 두 그룹 간 BMI 감소 효과에 통계적으로 유의한 차이가 있습니다.")
    else:
        print("결과: 두 그룹 간 BMI 감소 효과에 통계적으로 유의한 차이가 없습니다.")
    
    return has_significant_difference

# =============================================================================
# 2. 재구매율 분석
# =============================================================================
def calculate_repurchase_rate(first_purchase_file, second_purchase_file):
    """
    150일 이내 재구매율을 계산하는 함수
    
    Args:
        first_purchase_file: 첫 번째 구매 데이터 파일
        second_purchase_file: 두 번째 구매 데이터 파일
    
    Returns:
        tuple: (전체 고객 수, 재구매한 고객 수, 재구매율)
    """
    # 데이터 파일 읽기
    first_purchase_data = pd.read_excel(first_purchase_file)
    second_purchase_data = pd.read_excel(second_purchase_file)
    
    # 첫 구매와 재구매 데이터를 환자 ID로 연결
    combined_purchase_data = pd.merge(first_purchase_data, second_purchase_data, on='patient_id')
    
    # 구매 날짜를 날짜 형식으로 변환
    combined_purchase_data['first_purchase_date'] = pd.to_datetime(combined_purchase_data['purchase_date_x'])
    combined_purchase_data['second_purchase_date'] = pd.to_datetime(combined_purchase_data['purchase_date_y'])
    
    # 첫 구매와 재구매 사이의 일수 계산
    combined_purchase_data['days_between_purchases'] = (
        combined_purchase_data['second_purchase_date'] - 
        combined_purchase_data['first_purchase_date']
    ).dt.days
    
    # 150일 이내에 재구매한 고객들만 선별
    customers_repurchased_within_150days = combined_purchase_data[
        combined_purchase_data['days_between_purchases'] <= 150
    ]
    
    # 재구매율 계산
    total_customers = len(first_purchase_data)  # 첫 구매한 총 고객 수
    repurchased_customers = len(customers_repurchased_within_150days)  # 재구매한 고객 수
    repurchase_rate = repurchased_customers / total_customers  # 재구매율 (비율)
    
    return total_customers, repurchased_customers, repurchase_rate

def compare_repurchase_rates(batch_group_files, split_group_files):
    """
    일괄처방 그룹과 분할처방 그룹의 재구매율을 비교하는 함수
    
    Args:
        batch_group_files: [첫구매파일, 재구매파일] - 일괄처방 그룹
        split_group_files: [첫구매파일, 재구매파일] - 분할처방 그룹
    """
    print("\n=== 재구매율 분석 ===")
    
    # 각 그룹의 재구매율 계산
    batch_total, batch_repurchased, batch_rate = calculate_repurchase_rate(
        batch_group_files[0], batch_group_files[1])
    
    split_total, split_repurchased, split_rate = calculate_repurchase_rate(
        split_group_files[0], split_group_files[1])
    
    # Z-test로 두 그룹의 재구매율 차이 검정
    z_test_statistic, p_value = proportions_ztest(
        [split_repurchased, batch_repurchased],  # 각 그룹의 재구매 고객 수
        [split_total, batch_total]  # 각 그룹의 전체 고객 수
    )
    
    # 결과 출력 (백분율로 변환하여 표시)
    print(f"분할처방 그룹 재구매율: {split_rate*100:.1f}% ({split_repurchased}명/{split_total}명)")
    print(f"일괄처방 그룹 재구매율: {batch_rate*100:.1f}% ({batch_repurchased}명/{batch_total}명)")
    print(f"p-value (유의성 검정 결과): {p_value:.4f}")
    
    # 통계적 유의성 판단
    has_significant_difference = p_value < 0.05
    if has_significant_difference:
        print("결과: 두 그룹 간 재구매율에 통계적으로 유의한 차이가 있습니다.")
    else:
        print("결과: 두 그룹 간 재구매율에 통계적으로 유의한 차이가 없습니다.")
    
    return has_significant_difference

# =============================================================================
# 3. 소개율 분석
# =============================================================================
def calculate_referral_rate(purchase_file, referral_file):
    """
    90일 이내 소개율을 계산하는 함수
    
    Args:
        purchase_file: 구매 고객 데이터 파일
        referral_file: 소개 발생 데이터 파일
    
    Returns:
        tuple: (전체 고객 수, 소개한 고객 수, 소개율)
    """
    # 데이터 파일 읽기
    purchase_customers_data = pd.read_excel(purchase_file)
    referral_data = pd.read_excel(referral_file)
    
    # 90일 이내에 다른 사람을 소개한 고객 찾기
    referrals_within_90days = referral_data[referral_data['within_90_days'] == 'Y']
    unique_referring_customers = referrals_within_90days['referrer_patient_id'].nunique()
    
    # 소개율 계산
    total_customers = len(purchase_customers_data)  # 전체 구매 고객 수
    referring_customers = unique_referring_customers  # 소개한 고객 수
    referral_rate = referring_customers / total_customers  # 소개율 (비율)
    
    return total_customers, referring_customers, referral_rate

def compare_referral_rates(batch_group_files, split_group_files):
    """
    일괄처방 그룹과 분할처방 그룹의 소개율을 비교하는 함수
    
    Args:
        batch_group_files: [구매파일, 소개파일] - 일괄처방 그룹
        split_group_files: [구매파일, 소개파일] - 분할처방 그룹
    """
    print("\n=== 소개율 분석 ===")
    
    # 각 그룹의 소개율 계산
    batch_total, batch_referring, batch_rate = calculate_referral_rate(
        batch_group_files[0], batch_group_files[1])
    
    split_total, split_referring, split_rate = calculate_referral_rate(
        split_group_files[0], split_group_files[1])
    
    # Z-test로 두 그룹의 소개율 차이 검정
    z_test_statistic, p_value = proportions_ztest(
        [split_referring, batch_referring],  # 각 그룹의 소개한 고객 수
        [split_total, batch_total]  # 각 그룹의 전체 고객 수
    )
    
    # 결과 출력 (백분율로 변환하여 표시)
    print(f"분할처방 그룹 소개율: {split_rate*100:.1f}% ({split_referring}명/{split_total}명)")
    print(f"일괄처방 그룹 소개율: {batch_rate*100:.1f}% ({batch_referring}명/{batch_total}명)")
    print(f"p-value (유의성 검정 결과): {p_value:.4f}")
    
    # 통계적 유의성 판단
    has_significant_difference = p_value < 0.05
    if has_significant_difference:
        print("결과: 두 그룹 간 소개율에 통계적으로 유의한 차이가 있습니다.")
    else:
        print("결과: 두 그룹 간 소개율에 통계적으로 유의한 차이가 없습니다.")
    
    return has_significant_difference

# =============================================================================
# 메인 실행 부분
# =============================================================================
if __name__ == "__main__":
    print("다이어트 처방 A/B 테스트 분석을 시작합니다.\n")
    
    # 1. BMI 감소 효과 분석
    weight_loss_result = analyze_weight_loss(
        "batch_group_weight_data.xlsx",    # 일괄처방 그룹 체중 데이터
        "split_group_weight_data.xlsx"     # 분할처방 그룹 체중 데이터
    )
    
    # 2. 재구매율 분석
    repurchase_result = compare_repurchase_rates(
        ["batch_group_first_purchase.xlsx", "batch_group_second_purchase.xlsx"],    # 일괄처방 그룹
        ["split_group_first_purchase.xlsx", "split_group_second_purchase.xlsx"]     # 분할처방 그룹
    )
    
    # 3. 소개율 분석
    referral_result = compare_referral_rates(
        ["batch_group_purchase.xlsx", "batch_group_referral.xlsx"],                 # 일괄처방 그룹
        ["split_group_purchase.xlsx", "split_group_referral.xlsx"]                  # 분할처방 그룹
    )
    
    # 최종 분석 결과 요약
    print("\n" + "="*60)
    print("                   최종 분석 결과 요약")
    print("="*60)
    print(f"BMI 감소 효과 차이:    {'통계적으로 유의함 ✓' if weight_loss_result else '통계적으로 유의하지 않음 ✗'}")
    print(f"재구매율 차이:        {'통계적으로 유의함 ✓' if repurchase_result else '통계적으로 유의하지 않음 ✗'}")
    print(f"소개율 차이:          {'통계적으로 유의함 ✓' if referral_result else '통계적으로 유의하지 않음 ✗'}")
    print("="*60)
    
    # 결론
    if any([weight_loss_result, repurchase_result, referral_result]):
        print("결론: 분할처방 방식이 최소 하나 이상의 지표에서 유의한 효과를 보였습니다.")
    else:
        print("결론: 분할처방 방식이 기존 일괄처방 방식과 통계적으로 유의한 차이를 보이지 않았습니다.")
