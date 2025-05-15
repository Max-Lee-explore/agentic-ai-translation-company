from typing import Dict, List, Optional
import json
import csv
import pandas as pd

class TerminologyHandler:
    def __init__(self):
        self.terminology_dict: Dict[str, str] = {}
        self.source_lang: Optional[str] = None
        self.target_lang: Optional[str] = None

    def load_terminology(self, file_path: str, source_lang: str, target_lang: str) -> None:
        """
        Load terminology from various file formats.
        Supported formats: CSV, JSON, Excel, TXT
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        file_ext = file_path.lower().split('.')[-1]
        
        if file_ext == 'csv':
            self._load_from_csv(file_path)
        elif file_ext == 'json':
            self._load_from_json(file_path)
        elif file_ext in ['xlsx', 'xls']:
            self._load_from_excel(file_path)
        elif file_ext == 'txt':
            self._load_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported terminology file format: {file_ext}")

    def _load_from_csv(self, file_path: str) -> None:
        """Load terminology from CSV file."""
        try:
            df = pd.read_csv(file_path)
            if len(df.columns) < 2:
                raise ValueError("CSV must have at least 2 columns: source term and target term")
            
            self.terminology_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        except Exception as e:
            raise ValueError(f"Error loading CSV terminology file: {str(e)}")

    def _load_from_json(self, file_path: str) -> None:
        """Load terminology from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.terminology_dict = data
                else:
                    raise ValueError("JSON must be a dictionary of terms")
        except Exception as e:
            raise ValueError(f"Error loading JSON terminology file: {str(e)}")

    def _load_from_excel(self, file_path: str) -> None:
        """Load terminology from Excel file."""
        try:
            df = pd.read_excel(file_path)
            if len(df.columns) < 2:
                raise ValueError("Excel must have at least 2 columns: source term and target term")
            
            self.terminology_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        except Exception as e:
            raise ValueError(f"Error loading Excel terminology file: {str(e)}")

    def _load_from_txt(self, file_path: str) -> None:
        """Load terminology from TXT file (tab-separated or colon-separated)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if '\t' in line:
                        source, target = line.split('\t', 1)
                    elif ':' in line:
                        source, target = line.split(':', 1)
                    else:
                        continue
                    
                    self.terminology_dict[source.strip()] = target.strip()
        except Exception as e:
            raise ValueError(f"Error loading TXT terminology file: {str(e)}")

    def get_translation(self, term: str) -> Optional[str]:
        """Get the translation for a term if it exists in the terminology."""
        return self.terminology_dict.get(term)

    def get_all_terms(self) -> Dict[str, str]:
        """Get all terminology pairs."""
        return self.terminology_dict.copy()

    def clear_terminology(self) -> None:
        """Clear all loaded terminology."""
        self.terminology_dict.clear()
        self.source_lang = None
        self.target_lang = None 