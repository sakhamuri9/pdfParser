import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key)
    
    def extract_useful_information(self, content: str, topic_title: str) -> Dict:
        """
        Extract useful information from the content using OpenAI API.
        
        Args:
            content: The text content to analyze
            topic_title: The title of the topic
            
        Returns:
            Dict containing structured information with theory and examples
        """
        prompt = f"""
        Analyze the following content about '{topic_title}' from a Java Collections Framework tutorial:
        
        {content}
        
        Extract and organize the information into the following structure:
        1. Key concepts and theory
        2. Java code examples (if any)
        3. Usage examples and best practices
        
        Format your response as a JSON object with the following structure:
        {{
            "key_concepts": [list of key concepts and theoretical information],
            "code_examples": [list of Java code examples with explanations],
            "usage_examples": [list of usage examples and best practices]
        }}
        
        If any section doesn't have relevant information, return an empty list for that section.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts and organizes information from Java programming tutorials."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "key_concepts": [],
                "code_examples": [],
                "usage_examples": []
            }
    
    def analyze_topic(self, topic_data: Dict) -> Dict:
        """
        Analyze a complete topic with its headings and subheadings.
        
        Args:
            topic_data: Dictionary containing topic data with headings and subheadings
            
        Returns:
            Enhanced topic data with extracted useful information
        """
        topic_title = topic_data.get("title", "Unknown Topic")
        result = {
            "id": topic_data.get("id"),
            "title": topic_title,
            "headings": [],
            "analysis": {}
        }
        
        all_content = ""
        
        for heading in topic_data.get("headings", []):
            heading_result = {
                "id": heading.get("id"),
                "title": heading.get("title"),
                "subheadings": []
            }
            
            for subheading in heading.get("subheadings", []):
                content = subheading.get("content", "")
                all_content += f"\n\n{heading.get('title')} - {subheading.get('title')}:\n{content}"
                
                heading_result["subheadings"].append({
                    "id": subheading.get("id"),
                    "title": subheading.get("title"),
                    "content": content
                })
            
            result["headings"].append(heading_result)
        
        if all_content:
            result["analysis"] = self.extract_useful_information(all_content, topic_title)
        
        return result
