import os
import logging
import google.generativeai as genini

# Initialize Google Gemini client
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    gemini.configure(api_key=GOOGLE_API_KEY)
else:
    # For development, we'll create a fallback that shows an error message
    GOOGLE_API_KEY = None

def get_ai_response(user_message, document_context=""):
    """
    Get AI response using Google Gemini API with optional document context
    
    Args:
        user_message (str): The user's question or message
        document_context (str): Optional context from Google Docs
    
    Returns:
        str: AI response
    """
    try:
        # Check if API key is available
        if not GOOGLE_API_KEY:
            return "I need a Google API key to provide AI responses. Please set the GOOGLE_API_KEY environment variable."
        
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
        
        # Initialize Gemini model
        model = gemini.GenerativeModel('gemini-1.5-flash')
        
        # Combine system prompt and user message
        full_prompt = f"{system_prompt}\n\nUser: {user_message}"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
        
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
        if not GOOGLE_API_KEY:
            return "I need a Google API key to provide document summaries. Please set the GOOGLE_API_KEY environment variable."
            
        prompt = f"""Please provide a concise summary of the following document content, highlighting the key points and main topics:

{document_content}"""
        
        # Initialize Gemini model for summarization
        model = gemini.GenerativeModel('gemini-1.5-flash')
        
        # Generate summary
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        logging.error(f"Error summarizing document: {str(e)}")
        raise Exception(f"Failed to summarize document: {str(e)}")