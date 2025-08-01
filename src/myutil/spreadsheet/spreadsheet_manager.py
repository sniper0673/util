import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from myutil.spreadsheet.functions.type_convert import df_fast_convert

class SpreadsheetManager:
    def __init__(self, creds_json_path: str, sheet_id: str):
        self.creds_json_path = creds_json_path
        self.sheet_id = sheet_id
        self.client = self._authorize()

    def _authorize(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = gspread.service_account(filename=self.creds_json_path, scopes=scope)
        return creds

    def upload_df(self, df: pd.DataFrame, worksheet_name: str, index: bool = True) -> None:
        spreadsheet = self.client.open_by_key(self.sheet_id)
        worksheet = self._get_or_create_worksheet(spreadsheet, worksheet_name)
        worksheet.clear()
        set_with_dataframe(worksheet, df, include_index=index)

    def download_df(self, worksheet_name: str, header=0, index_col=None, auto_type_convert:bool=True) -> pd.DataFrame:
        spreadsheet = self.client.open_by_key(self.sheet_id)
        worksheet = self._get_or_create_worksheet(spreadsheet, worksheet_name)
        df = get_as_dataframe(
            worksheet, 
            evaluate_formulas=True,      # ← 수식 대신 계산된 값 사용
            drop_empty_rows=True, 
            drop_empty_columns=True,
            header=header, 
            index_col=index_col, 
            dtype=str,
            )
        if auto_type_convert:
            # 자동 형변환을 적용하여 DataFrame 반환
            # 숫자형, 날짜형, 문자열형으로 변환
            # 숫자형은 int, float로 변환
            # 날짜형은 datetime으로 변환
            # 나머지는 문자열로 유지
            df = df_fast_convert(df)
        return df

    def _get_or_create_worksheet(self, spreadsheet, worksheet_name: str):
        try:
            return spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            return spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")
        
def test():
    creds_json_path = r'./credentials/vertical-album-400707-49b25aaf32d5.json'
    sheet_id = "1iK7UY7g_fSRSAOpIEYrFR41p_qK68LhkcIfqr7NUxug"
    sheet_manager = SpreadsheetManager(creds_json_path, sheet_id)

    # Test uploading a DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    sheet_manager.upload_df(df, "TestWorksheet")

    # Test downloading a DataFrame
    downloaded_df = sheet_manager.download_df("TestWorksheet")
    print_df(downloaded_df)

if __name__ == "__main__":
    from utility.df.format import print_df
    test()
    print("SpreadsheetManager test completed successfully.")