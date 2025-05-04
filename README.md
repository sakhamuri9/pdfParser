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
- SQLAlchemy (with SQLite database)
- PDFPlumber for PDF parsing

## API Endpoints

### PDF Parsing Endpoints
- `POST /api/upload-pdf/`: Upload and parse a PDF file
- `GET /api/topics/`: Get all topics with their headings and subheadings
- `GET /api/topics/{topic_id}`: Get a specific topic by ID

### AI Analysis Endpoints
- `GET /api/ai/analyze/topics/`: Get all topics with AI-enhanced analysis separating theory from examples
- `GET /api/ai/analyze/topics/{topic_id}`: Get a specific topic with AI-enhanced analysis

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

3. Set up your OpenAI API key in the `.env` file:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. Initialize the database:
```bash
poetry run python -m app.init_db
```

5. Run the application:
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

### Get AI-enhanced analysis for a specific topic:

```bash
curl http://localhost:8000/api/ai/analyze/topics/1
```

This endpoint uses OpenAI to analyze the topic content and returns structured information with:
- Key concepts and theoretical information
- Java code examples (if any)
- Usage examples and best practices

### Get AI-enhanced analysis for all topics:

```bash
curl http://localhost:8000/api/ai/analyze/topics/
```

This endpoint analyzes all topics and returns structured information for each topic.

## Deployment

The microservice can be deployed to a cloud platform that supports Python applications:

1. Ensure all dependencies are listed in the `pyproject.toml` file
2. Initialize the database before starting the application
3. Configure environment variables for production settings if needed

## Notes

- The service uses a SQLite database file, which persists data between restarts
- For production use, consider configuring a more robust database like PostgreSQL
