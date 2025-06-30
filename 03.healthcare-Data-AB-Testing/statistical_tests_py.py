"""
통계 검정 유틸리티
헬스케어 분석을 위한 핵심 통계 함수들
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import mixedlm
from statsmodels.stats.proportion import proportions_ztest

def mixed_effects_test(data, outcome, group_var, time_var, subject_id):
    """Mixed-Effects Model 분석"""
    formula = f'{outcome} ~ C({group_var}) * {time_var}'
    model = mixedlm(formula, data, groups=data[subject_id])
    results = model.fit()
    
    # 주요 결과 추출
    group_params = [p for p in results.params.index if 'C(' in p and ')[T.' in p]
    if group_params:
        coef = results.params[group_params[0]]
        p_val = results.pvalues[group_params[0]]
    else:
        coef, p_val = 0, 1
    
    return {
        'coefficient': coef,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'model': results
    }

def proportion_test(successes, totals):
    """두 비율 간 Z-test"""
    z_stat, p_val = proportions_ztest(successes, totals)
    
    rates = [s/t for s, t in zip(successes, totals)]
    
    return {
        'z_statistic': z_stat,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'rates': rates,
        'difference': rates[0] - rates[1]
    }

def variance_test(group1, group2):
    """F-test로 분산 비교"""
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    f_stat = var1 / var2 if var1 > var2 else var2 / var1
    
    df1, df2 = len(group1)-1, len(group2)-1
    p_val = 2 * min(stats.f.cdf(f_stat, df1, df2), 1 - stats.f.cdf(f_stat, df1, df2))
    
    return {
        'f_statistic': f_stat,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'variances': [var1, var2]
    }

def welch_ttest(group1, group2):
    """Welch's t-test (등분산 가정 X)"""
    t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)
    
    mean1, mean2 = np.mean(group1), np.mean(group2)
    
    return {
        't_statistic': t_stat,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'means': [mean1, mean2],
        'difference': mean1 - mean2
    }

def remove_outliers(data, column, method='iqr', multiplier=1.5):
    """이상치 제거"""
    if method == 'iqr':
        Q1, Q3 = data[column].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower, upper = Q1 - multiplier * IQR, Q3 + multiplier * IQR
        return data[data[column].between(lower, upper)]
    else:
        # Z-score 방법
        z_scores = np.abs(stats.zscore(data[column]))
        return data[z_scores < multiplier]

def cohens_d(group1, group2):
    """Cohen's d 효과 크기 계산"""
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(((n1-1)*np.var(group1, ddof=1) + (n2-1)*np.var(group2, ddof=1)) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

def quick_summary(test_results, test_name):
    """검정 결과 요약"""
    print(f"\n📊 {test_name} 결과:")
    
    if 'coefficient' in test_results:
        print(f"   효과 크기: {test_results['coefficient']:.4f}")
    elif 'difference' in test_results:
        print(f"   차이: {test_results['difference']:.4f}")
    
    print(f"   p-value: {test_results['p_value']:.4f}")
    print(f"   유의성: {'유의함' if test_results['significant'] else '유의하지 않음'}")

# 편의 함수들
def analyze_groups(control, treatment, outcome_col, test_type='ttest'):
    """그룹 간 비교 분석"""
    
    if test_type == 'ttest':
        result = welch_ttest(treatment[outcome_col], control[outcome_col])
        result['effect_size'] = cohens_d(treatment[outcome_col], control[outcome_col])
    elif test_type == 'variance':
        result = variance_test(control[outcome_col], treatment[outcome_col])
    
    return result

def preprocess_data(df, date_cols=None, numeric_cols=None):
    """데이터 전처리"""
    if date_cols:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col])
    
    if numeric_cols:
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.dropna()

if __name__ == "__main__":
    print("통계 검정 유틸리티 로드 완료")
    print("주요 함수:")
    print("- mixed_effects_test(): Mixed-Effects Model")
    print("- proportion_test(): 비율 검정")
    print("- variance_test(): 분산 검정")
    print("- welch_ttest(): t-검정")
    print("- analyze_groups(): 그룹 비교")