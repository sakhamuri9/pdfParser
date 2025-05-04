from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from app.core.database import get_db
from app.services.pdf_parser import PDFParser
from app.services.db_service import DBService
from app.models.pdf_content import Topic, Heading, Subheading

router = APIRouter()

@router.post("/upload-pdf/", response_model=Dict)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF file and parse its content.
    Returns the parsed content structure with topics, headings, and subheadings.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        contents = await file.read()
        with open(f"/tmp/{file.filename}", "wb") as f:
            f.write(contents)
        
        pdf_parser = PDFParser(f"/tmp/{file.filename}")
        parsed_data = pdf_parser.parse_content()
        pdf_parser.close()
        
        db_service = DBService(db)
        result = db_service.store_parsed_content(parsed_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@router.get("/topics/", response_model=List[Dict])
def get_all_topics(db: Session = Depends(get_db)):
    """
    Get all topics with their headings and subheadings.
    """
    db_service = DBService(db)
    topics = db_service.get_all_topics()
    
    result = []
    for topic in topics:
        topic_data = {
            "id": topic.id,
            "title": topic.title,
            "headings": []
        }
        
        for heading in topic.headings:
            heading_data = {
                "id": heading.id,
                "title": heading.title,
                "subheadings": []
            }
            
            for subheading in heading.subheadings:
                subheading_data = {
                    "id": subheading.id,
                    "title": subheading.title,
                    "content": subheading.content
                }
                heading_data["subheadings"].append(subheading_data)
            
            topic_data["headings"].append(heading_data)
        
        result.append(topic_data)
    
    return result

@router.get("/topics/{topic_id}", response_model=Dict)
def get_topic_by_id(topic_id: int, db: Session = Depends(get_db)):
    """
    Get a specific topic by ID with its headings and subheadings.
    """
    db_service = DBService(db)
    topic = db_service.get_topic_by_id(topic_id)
    
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    topic_data = {
        "id": topic.id,
        "title": topic.title,
        "headings": []
    }
    
    for heading in topic.headings:
        heading_data = {
            "id": heading.id,
            "title": heading.title,
            "subheadings": []
        }
        
        for subheading in heading.subheadings:
            subheading_data = {
                "id": subheading.id,
                "title": subheading.title,
                "content": subheading.content
            }
            heading_data["subheadings"].append(subheading_data)
        
        topic_data["headings"].append(heading_data)
    
    return topic_data
