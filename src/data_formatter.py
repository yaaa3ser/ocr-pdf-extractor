import pandas as pd
from dateutil.parser import parse
import re
from .models import Metadata

class DataFormatter:
    def __init__(self, metadata: Metadata, claims_df: pd.DataFrame, benefits_df: pd.DataFrame):
        self.metadata = metadata
        self.claims_df = claims_df
        self.benefits_df = benefits_df

    def format_dataframes(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        claims_df = self._format_claims()
        benefits_df = self._format_benefits()
        
        return claims_df, benefits_df

    def _format_claims(self) -> pd.DataFrame:
        claims_df = self.claims_df.copy()
        claims_df['Policy Year'] = ''
        
        # Identify policy years
        prior_2_year_start = claims_df[claims_df['Monthly Claims'] == 'Policy Year - 2 years prior: Number of lives at start 0'].index[0]
        prior_year_start = claims_df[claims_df['Monthly Claims'] == 'Prior Policy Year: Number of lives at start 13'].index[0]
        last_year_start = claims_df[claims_df['Monthly Claims'] == 'Last Policy Year: Number of lives at start 27'].index[0]
        
        claims_df.loc[prior_2_year_start : prior_year_start-1, 'Policy Year'] = '2 years Prior'
        claims_df.loc[prior_year_start : last_year_start-1, 'Policy Year'] = 'Prior Policy Year'
        claims_df.loc[last_year_start: , 'Policy Year'] = 'Last Policy Year'
        
        # Clean and rename columns
        claims_df = claims_df[claims_df['Monthly Claims'].str.match(r'^\d+$|^202[0-2]\d{2}$')] 
        claims_df = claims_df.rename(columns={
            'Monthly Claims': 'Monthly claims',
            'Number of Lives Insured': 'Number of insured lives',
            'Number of Paid Claims': 'Number of claims',
            'Amount of Paid Claims': 'Amount of paid claims',
            'Amount of Paid Claims with VAT': 'Amount of paid claims (with VAT)'
        })
        
        # Add metadata columns
        end_date = parse(self.metadata.policy_expiry_date).strftime('%Y-%m-%d')
        claims_df['End date'] = end_date
        claims_df['Class'] = self.metadata.class_val
        claims_df['Overall Limit'] = self.metadata.overall_benefit_limit.replace(',', '')
        
        # Convert numeric columns
        numeric_cols = [
            'Number of insured lives', 'Number of claims', 
            'Amount of paid claims', 'Amount of paid claims (with VAT)'
        ]
        for col in numeric_cols:
            claims_df[col] = self._convert_to_numeric(claims_df[col])
        
        return claims_df

    def _format_benefits(self) -> pd.DataFrame:
        benefits_df = self.benefits_df.copy()
        benefits_df = benefits_df.rename(columns={
            'Benefit_Sama': 'Benefit_Sama',
            'Number of Paid Claims': 'Number of Claims',
            'Amount of Paid Claims': 'Amount of Claims',
            'Amt of Claims (VAT)': 'Amount of Claims with VAT',
            'Notes': 'Notes'
        })
        
        # Notes column
        def process_notes(note):
            if not note or note.strip() == '':
                return 'No info'
            
            if 'Cesarean' in note:
                if 'is covered' in note:
                    return 'Yes'
                else:
                    return 'No'
            
            match = re.search(r'\d+\s*%', note)
            return match.group(0) if match else 'No info'
        
        benefits_df['Notes'] = benefits_df['Notes'].apply(process_notes)
        
        # Add metadata columns
        end_date = parse(self.metadata.policy_expiry_date).strftime('%Y-%m-%d')
        benefits_df['Policy Year'] = 'Last Policy Year'
        benefits_df['End date'] = end_date
        benefits_df['Class'] = self.metadata.class_val
        benefits_df['Overall Limit'] = self.metadata.overall_benefit_limit.replace(',', '')
        
        # Convert numeric columns
        numeric_cols = ['Number of Claims', 'Amount of Claims', 'Amount of Claims with VAT']
        for col in numeric_cols:
            benefits_df[col] = self._convert_to_numeric(benefits_df[col])
        
        return benefits_df
    
    def _convert_to_numeric(self, cell):
        return pd.to_numeric(cell.str.replace(',', ''), errors='coerce')