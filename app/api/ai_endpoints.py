from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from app.core.database import get_db
from app.services.db_service import DBService
from app.services.openai_service import OpenAIService

router = APIRouter()

@router.get("/analyze/topics/{topic_id}", response_model=Dict)
def analyze_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Analyze a specific topic by ID using OpenAI to extract useful information.
    Returns the topic with enhanced analysis separating theory from examples.
    """
    try:
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
        
        openai_service = OpenAIService()
        analyzed_topic = openai_service.analyze_topic(topic_data)
        
        return analyzed_topic
    
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API configuration error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing topic: {str(e)}")

@router.get("/analyze/topics/", response_model=List[Dict])
def analyze_all_topics(db: Session = Depends(get_db)):
    """
    Analyze all topics using OpenAI to extract useful information.
    Returns all topics with enhanced analysis separating theory from examples.
    """
    try:
        db_service = DBService(db)
        topics = db_service.get_all_topics()
        
        if not topics:
            return []
        
        openai_service = OpenAIService()
        analyzed_topics = []
        
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
            
            analyzed_topic = openai_service.analyze_topic(topic_data)
            analyzed_topics.append(analyzed_topic)
        
        return analyzed_topics
    
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API configuration error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing topics: {str(e)}")
