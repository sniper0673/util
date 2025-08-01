import pandas as pd
import numpy as np

def df_fast_convert(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrame의 모든 열을 빠르게 자동 형변환.
    - 숫자 문자열 → 숫자형
    - 날짜 문자열 → datetime (여러 포맷 지원)
    - 나머지는 그대로
    """
    converted = {}

    for col in df.columns:
        s = df[col]

        # 숫자 시도
        s_num = pd.to_numeric(s, errors='coerce')
        if s_num.notna().sum() >= len(s) * 0.8:
            converted[col] = s_num
            continue

        # 날짜 시도: 지정된 3가지 형식만 테스트
        date_formats = ['%Y-%m-%d', '%Y%m%d', '%Y/%m/%d']
        for fmt in date_formats:
            try:
                s_dt = pd.to_datetime(s, format=fmt, errors='coerce')
                if s_dt.notna().sum() >= len(s) * 0.8:
                    converted[col] = s_dt
                    break
            except Exception:
                continue
        else:
            converted[col] = s  # 날짜 변환 실패 시 원본 유지

    return pd.DataFrame(converted)

def series_convert(se:pd.Series):
    """
    Series의 데이터 타입을 자동으로 변환합니다.
    - 숫자형: int, float
    - 날짜형: datetime
    - 문자열: str
    """
    if se.dtype == 'object':
        # 문자열로 처리된 숫자형 데이터 변환
        se = pd.to_numeric(se, errors='coerce')
    
    # 날짜형 데이터 변환
    if pd.api.types.is_string_dtype(se):
        se = pd.to_datetime(se, errors='coerce')

    return se.convert_dtypes()

def df_convert(df:pd.DataFrame):
    """
    DataFrame의 모든 열을 자동으로 변환합니다.
    - 숫자형: int, float
    - 날짜형: datetime
    - 문자열: str
    """
    for col in df.columns:
        df[col] = series_convert(df[col])
    
    return df