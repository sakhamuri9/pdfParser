from sqlalchemy.orm import Session
from typing import Dict, List, Optional

from app.models.pdf_content import Topic, Heading, Subheading

class DBService:
    def __init__(self, db: Session):
        self.db = db
    
    def store_parsed_content(self, parsed_data: Dict) -> Dict:
        """
        Store the parsed PDF content in the database.
        Returns a dictionary with the stored data IDs.
        """
        result = {"topics": []}
        
        for topic_data in parsed_data.get("topics", []):
            topic = Topic(title=topic_data["title"])
            self.db.add(topic)
            self.db.flush()  # Flush to get the ID
            
            topic_result = {
                "id": topic.id,
                "title": topic.title,
                "headings": []
            }
            
            for heading_data in topic_data.get("headings", []):
                heading = Heading(title=heading_data["title"], topic_id=topic.id)
                self.db.add(heading)
                self.db.flush()  # Flush to get the ID
                
                heading_result = {
                    "id": heading.id,
                    "title": heading.title,
                    "subheadings": []
                }
                
                for subheading_data in heading_data.get("subheadings", []):
                    subheading = Subheading(
                        title=subheading_data["title"],
                        content=subheading_data["content"],
                        heading_id=heading.id
                    )
                    self.db.add(subheading)
                    self.db.flush()  # Flush to get the ID
                    
                    subheading_result = {
                        "id": subheading.id,
                        "title": subheading.title,
                        "content": subheading.content
                    }
                    
                    heading_result["subheadings"].append(subheading_result)
                
                topic_result["headings"].append(heading_result)
            
            result["topics"].append(topic_result)
        
        self.db.commit()
        return result
    
    def get_all_topics(self) -> List[Topic]:
        """Get all topics from the database."""
        return self.db.query(Topic).all()
    
    def get_topic_by_id(self, topic_id: int) -> Optional[Topic]:
        """Get a topic by ID."""
        return self.db.query(Topic).filter(Topic.id == topic_id).first()
    
    def get_heading_by_id(self, heading_id: int) -> Optional[Heading]:
        """Get a heading by ID."""
        return self.db.query(Heading).filter(Heading.id == heading_id).first()
    
    def get_subheading_by_id(self, subheading_id: int) -> Optional[Subheading]:
        """Get a subheading by ID."""
        return self.db.query(Subheading).filter(Subheading.id == subheading_id).first()
