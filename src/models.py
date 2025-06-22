from dataclasses import dataclass
import pandas as pd

@dataclass
class Metadata:
    group_number: str
    policy_inception_date: str
    policy_expiry_date: str
    class_val: str
    overall_benefit_limit: str
    inpatient_outpatient_limit: str
    dental_limit: str
    optical_limit: str
    deductible: str
    maternity_limit: str

@dataclass
class ExtractedData:
    metadata: Metadata
    claims: pd.DataFrame
    benefits: pd.DataFrame