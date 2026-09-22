from pathlib import Path
import pandas as pd

class MortalityLoader:

    FILES = [
        ("2015 VBT Male RR80.xls", "preferred", "male"),
        ("2015 VBT Male RR60.xls", "superpreferred", "male"),
        ("2015 VBT Male RR100.xls", "standard", "male"),
        ("2015 VBT Female RR80.xls", "preferred", "female"),
        ("2015 VBT Female RR60.xls", "superpreferred", "female"),
        ("2015 VBT Female RR100.xls", "standard", "female"),
    ]
    @staticmethod
    def read_file(path: Path, risk_class: str, gender: str) -> pd.DataFrame:
        """
        Read a mortality table and append metadata.
        """
        df = pd.read_excel(path)
        
        df["risk_class"] = risk_class
        df["gender"] = gender
        
        return df
        
    @classmethod
    def load(cls, data_dir: Path) -> pd.DataFrame:
        """
        Load and combine all mortality tables.
        """
        dfs = []
        
        for filename, risk_class, gender in cls.FILES:
        
            file_path = data_dir / filename
            
            df = cls.read_file( path=file_path, risk_class=risk_class, gender=gender)
            
            dfs.append(df)
            
        return pd.concat(dfs,ignore_index=True)