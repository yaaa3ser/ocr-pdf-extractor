# OCR PDF Table Extraction Project

## Overview
This project provides a Docker-based solution for extracting tabulated data from a PDF file and converting it into machine-readable pandas DataFrames, stored in Redis.

## Features
- Extracts metadata, claims, and benefits tables from a single-page PDF
- Processes data into structured pandas DataFrames
- Formats data according to specified requirements
- Saves results to both a pickle file and Redis
- Uses Docker Compose to manage application and Redis services

## Requirements
- Docker
- Docker Compose
- Input PDF file: `OCR Test Template.pdf`

## Setup and Installation
1. Clone the repository:
```bash
git clone https://github.com/yaaa3ser/ocr-pdf-extractor.git
cd ocr-pdf-extractor
```

2. Place the input PDF file in the `input/` directory, I've already added a test one.

3. Build and run the services:
```bash
docker-compose up --build
```

4. Access the output in the `output/` directory or query Redis:
```bash
docker-compose exec redis redis-cli
> GET claim_experiences
```

## Project Structure
- `docker-compose.yml`: Defines application and Redis services
- `Dockerfile`: Configures the application container
- `requirements.txt`: Lists Python dependencies
- `src/`: Contains the application code
    - `models.py`: Defines data models
    - `main.py`: Application entry point
    - `pdf_processor.py`: Handles PDF table extraction
    - `data_formatter.py`: Formats extracted data
    - `redis_client.py`: Manages Redis interactions

- `input/`: Directory for input PDF files
- `output/`: Directory for the output pickle file
- `README.md`: Project documentation

## Output
- A pickle file (`dataframes.txt`) containing:
  - `claim_experiences.claims`: Claims DataFrame
  - `claim_experiences.benefits`: Benefits DataFrame
- Data stored in Redis under the key `claim_experiences`


## Samples displaying DataFrames
![Sample Output](./samples/Screenshot%20from%202025-06-22%2019-54-56.png)
![Sample Output 2](./samples/Screenshot%20from%202025-06-22%2019-55-18.png)