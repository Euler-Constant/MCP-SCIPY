import pandas as pd
import scipy.stats as stats
from .utils.data_parser import dataframe_to_json

class StatsEngine:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_dataset(self, file_name):
        try:
            return pd.read_csv(f"{self.data_dir}/{file_name}", nrows=10000)
        except Exception as e:
            return {"error": f"Failed to load dataset: {str(e)}"}

    def run_ttest(self, file_name, column, group_col, group1, group2):
        df = self.load_dataset(file_name)
        if isinstance(df, dict) and "error" in df:
            return df
        try:
            group1_data = df[df[group_col] == group1][column]
            group2_data = df[df[group_col] == group2][column]
            if len(group1_data) < 2 or len(group2_data) < 2:
                return {"error": "Insufficient data for t-test (need at least 2 samples per group)"}
            t_stat, p_value = stats.ttest_ind(group1_data, group2_data, nan_policy="omit")
            return dataframe_to_json(pd.Series({"t_stat": t_stat, "p_value": p_value}))
        except Exception as e:
            return {"error": f"T-test failed: {str(e)}"}