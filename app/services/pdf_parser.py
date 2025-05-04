import pdfplumber
import re
from typing import Dict, List, Tuple, Optional

class PDFParser:
    def __init__(self, pdf_file):
        self.pdf = pdfplumber.open(pdf_file)
        
    def extract_text(self) -> str:
        """Extract all text from the PDF."""
        text = ""
        for page in self.pdf.pages:
            text += page.extract_text() + "\n"
        return text
    
    def parse_content(self) -> Dict:
        """
        Parse PDF content into topics, headings, and subheadings.
        Returns a dictionary with the structured content.
        """
        text = self.extract_text()
        
        topics = self._identify_topics(text)
        
        result = {
            "topics": []
        }
        
        for topic_title, topic_content in topics.items():
            topic_data = {
                "title": topic_title,
                "headings": []
            }
            
            headings = self._identify_headings(topic_content)
            
            for heading_title, heading_content in headings.items():
                heading_data = {
                    "title": heading_title,
                    "subheadings": []
                }
                
                subheadings = self._identify_subheadings(heading_content)
                
                for subheading_title, subheading_content in subheadings.items():
                    subheading_data = {
                        "title": subheading_title,
                        "content": subheading_content
                    }
                    heading_data["subheadings"].append(subheading_data)
                
                topic_data["headings"].append(heading_data)
            
            result["topics"].append(topic_data)
        
        return result
    
    def _identify_topics(self, text: str) -> Dict[str, str]:
        """
        Identify topics in the text.
        This is a simplified implementation and should be adjusted based on actual PDF structure.
        """
        topic_pattern = r'(?:^|\n)(?:TOPIC|Chapter|SECTION)\s*\d*\s*[:\-]?\s*(.*?)(?=\n(?:TOPIC|Chapter|SECTION)|$)'
        topics = {}
        
        if not re.search(topic_pattern, text, re.IGNORECASE | re.MULTILINE):
            topics["Main Content"] = text
            return topics
        
        matches = re.finditer(topic_pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        last_end = 0
        prev_title = None
        
        for match in matches:
            topic_title = match.group(1).strip()
            start = match.start()
            
            if start > last_end:
                topic_content = text[last_end:start].strip()
                if topic_content and last_end > 0:  # Skip the first match which might be a header
                    topics[prev_title] = topic_content
            
            prev_title = topic_title
            last_end = match.end()
        
        if last_end < len(text):
            topics[prev_title] = text[last_end:].strip()
        
        return topics
    
    def _identify_headings(self, text: str) -> Dict[str, str]:
        """
        Identify headings within a topic.
        This is a simplified implementation and should be adjusted based on actual PDF structure.
        """
        heading_pattern = r'(?:^|\n)(?:\d+\.\d+|\d+\.)\s*(.*?)(?=\n(?:\d+\.\d+|\d+\.)|$)'
        headings = {}
        
        if not re.search(heading_pattern, text, re.IGNORECASE | re.MULTILINE):
            headings["Main Heading"] = text
            return headings
        
        matches = re.finditer(heading_pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        last_end = 0
        prev_title = None
        
        for match in matches:
            heading_title = match.group(1).strip()
            start = match.start()
            
            if start > last_end:
                heading_content = text[last_end:start].strip()
                if heading_content and last_end > 0:  # Skip the first match which might be a header
                    headings[prev_title] = heading_content
            
            prev_title = heading_title
            last_end = match.end()
        
        if last_end < len(text):
            headings[prev_title] = text[last_end:].strip()
        
        return headings
    
    def _identify_subheadings(self, text: str) -> Dict[str, str]:
        """
        Identify subheadings within a heading.
        This is a simplified implementation and should be adjusted based on actual PDF structure.
        """
        subheading_pattern = r'(?:^|\n)(?:\d+\.\d+\.\d+|\w\)|\(\w\))\s*(.*?)(?=\n(?:\d+\.\d+\.\d+|\w\)|\(\w\))|$)'
        subheadings = {}
        
        if not re.search(subheading_pattern, text, re.IGNORECASE | re.MULTILINE):
            subheadings["Main Subheading"] = text
            return subheadings
        
        matches = re.finditer(subheading_pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        last_end = 0
        prev_title = None
        
        for match in matches:
            subheading_title = match.group(1).strip()
            start = match.start()
            
            if start > last_end:
                subheading_content = text[last_end:start].strip()
                if subheading_content and last_end > 0:  # Skip the first match which might be a header
                    subheadings[prev_title] = subheading_content
            
            prev_title = subheading_title
            last_end = match.end()
        
        if last_end < len(text):
            subheadings[prev_title] = text[last_end:].strip()
        
        return subheadings
    
    def close(self):
        """Close the PDF file."""
        self.pdf.close()
