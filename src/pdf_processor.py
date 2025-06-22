import pdfplumber
import pandas as pd
from .models import Metadata, ExtractedData
from typing import List

class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_tables(self) -> ExtractedData:
        with pdfplumber.open(self.pdf_path) as pdf:
            page = pdf.pages[0]
            
            # raw_text = page.extract_text()
            # print("Raw text from PDF:", raw_text)
            
            table_settings = {
                "text_tolerance": 2,
                "intersection_tolerance": 2,
            }
            tables = page.extract_tables(table_settings=table_settings)

            if not tables or len(tables) < 3:
                raise ValueError("Failed to extract expected number of tables from PDF.")

            # Metadata table
            metadata = self._extract_metadata(tables[0])

            # Claims table
            claims_data = tables[1][1:]  # Skip header row
            claims_headers = [cell.replace('\n', ' ').strip() if cell else '' for cell in tables[1][0]]
            claims_df = pd.DataFrame(claims_data, columns=claims_headers)
            
            # Benefits table
            benefits_data = tables[2][3:-1]  # Skip header and Overall row
            benefits_headers = [cell.replace('\n', ' ').strip() if cell else '' for cell in tables[2][2]]
            benefits_df = pd.DataFrame(benefits_data, columns=benefits_headers)
            
            return ExtractedData(metadata, claims_df, benefits_df)

    def _extract_metadata(self, table: List[List[str]]) -> Metadata:
        metadata_dict = {}
        for row in table:
                key_1 = row[0].strip() if row[0] else ''
                value_1 = row[1].strip() if row[1] else ''
                metadata_dict[key_1] = value_1

                key_2 = row[2].strip() if row[2] else ''
                value_2 = row[3].strip() if row[3] else ''
                metadata_dict[key_2] = value_2

        return Metadata(
            group_number=metadata_dict.get('Group Number', ''),
            policy_inception_date=metadata_dict.get('Policy Inception Date', ''),
            policy_expiry_date=metadata_dict.get('Policy Expiry Date', ''),
            class_val=metadata_dict.get('Class', ''),
            overall_benefit_limit=metadata_dict.get('Overall Benefit Limit', ''),
            inpatient_outpatient_limit=metadata_dict.get('Inpatient/Outpatient Limit', ''),
            dental_limit=metadata_dict.get('Dental Limit', ''),
            optical_limit=metadata_dict.get('Optical Limit', ''),
            deductible=metadata_dict.get('Deductible', ''),
            maternity_limit=metadata_dict.get('Maternity Limit', '')
        )