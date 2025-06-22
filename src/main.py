import os
from .pdf_processor import PDFProcessor
from .data_formatter import DataFormatter
from .redis_client import RedisClient
import pickle

class OCRProcessor:
    def __init__(self, pdf_path: str = None, output_path: str = None):
        self.pdf_path = pdf_path or os.getenv('PDF_INPUT_PATH', os.path.join(os.path.dirname(__file__), '..', 'input', 'OCR Test Template.pdf'))
        self.output_path = output_path or os.getenv('OUTPUT_PATH', '/app/output/dataframes.txt')
        self.redis_client = RedisClient(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379))
        )

    def process(self):
        # Extract tables
        pdf_processor = PDFProcessor(self.pdf_path)
        extracted_data = pdf_processor.extract_tables()
        
        # Format data
        formatter = DataFormatter(
            extracted_data.metadata,
            extracted_data.claims,
            extracted_data.benefits
        )
        claims_df, benefits_df = formatter.format_dataframes()
        
        # Prepare output
        output_data = {
            "claim_experiences": {
                "claims": claims_df,
                "benefits": benefits_df
            }
        }
        
        # Save to pickle file
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'wb') as f:
            pickle.dump(output_data, f)
        
        # Save to Redis
        self.redis_client.save_data(output_data)

def main():
    processor = OCRProcessor()
    processor.process()

if __name__ == "__main__":
    main()