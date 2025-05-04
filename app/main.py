from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.endpoints import router
from app.core.database import Base, engine
from app.models.pdf_content import Topic, Heading, Subheading

app = FastAPI(title="PDF Parser API", description="API for parsing PDF files and storing content by topics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to PDF Parser API. Use /api/upload-pdf/ to upload and parse a PDF file."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
