# PDF Parser Microservice

A Python microservice that parses PDF files and organizes content by topics, headings, and subheadings.

## Features

- Upload and parse PDF files using PDFPlumber
- Extract and organize content by topics, headings, and subheadings
- Store parsed data in a structured format
- RESTful API to access all parsed data

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy (with SQLite in-memory database)
- PDFPlumber for PDF parsing

## API Endpoints

- `POST /api/upload-pdf/`: Upload and parse a PDF file
- `GET /api/topics/`: Get all topics with their headings and subheadings
- `GET /api/topics/{topic_id}`: Get a specific topic by ID

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/sakhamuri9/pdfParser.git
cd pdfParser
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Run the application:
```bash
poetry run python -m app.main
```

The API will be available at `http://localhost:8000`.

## Usage Example

### Upload a PDF file for parsing:

```bash
curl -X POST -F "file=@your_file.pdf" http://localhost:8000/api/upload-pdf/
```

### Get all parsed topics:

```bash
curl http://localhost:8000/api/topics/
```

### Get a specific topic by ID:

```bash
curl http://localhost:8000/api/topics/1
```

## Notes

- The service uses an in-memory SQLite database, so data will be lost when the service is restarted.
- For production use, consider configuring a persistent database.
