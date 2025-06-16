import os
import logging
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY environment variable is required")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_ai_response(user_message, document_context=""):
    """
    Get AI response using OpenAI API with optional document context
    
    Args:
        user_message (str): The user's question or message
        document_context (str): Optional context from Google Docs
    
    Returns:
        str: AI response
    """
    try:
        # Build the system prompt
        system_prompt = """You are a helpful AI assistant. You can answer questions and have conversations with users."""
        
        if document_context:
            system_prompt += f"""
            
You have access to the following document content as your primary knowledge source:

--- DOCUMENT CONTENT ---
{document_context}
--- END DOCUMENT CONTENT ---

When answering questions, prioritize information from the provided document. If the document doesn't contain relevant information, you can use your general knowledge but clearly indicate when you're doing so.
"""
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error getting AI response: {str(e)}")
        raise Exception(f"Failed to get AI response: {str(e)}")

def summarize_document(document_content):
    """
    Create a summary of the document content
    
    Args:
        document_content (str): The document content to summarize
    
    Returns:
        str: Summary of the document
    """
    try:
        prompt = f"""Please provide a concise summary of the following document content, highlighting the key points and main topics:

{document_content}"""
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error summarizing document: {str(e)}")
        raise Exception(f"Failed to summarize document: {str(e)}")
