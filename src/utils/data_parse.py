import pandas as pd
import json

def dataframe_to_json(data):
    """
    Convert a Pandas DataFrame or Series to a JSON-compatible dictionary.
    
    Args:
        data: Pandas DataFrame or Series object.
        
    Returns:
        dict: JSON-compatible dictionary representation of the data.
    """
    try:
        if isinstance(data, (pd.DataFrame, pd.Series)):
            return data.to_dict(orient="records" if isinstance(data, pd.DataFrame) else "index")
        return data
    except Exception as e:
        return {"error": f"Data conversion failed: {str(e)}"}