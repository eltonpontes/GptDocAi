import os
import logging
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_google_docs_service():
    """Initialize and return Google Docs API service"""
    creds = None
    
    # Check if we have stored credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use credentials from environment or fall back to local auth
            client_config = {
                "web": {
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:5000/oauth2callback"]
                }
            }
            
            if not client_config["web"]["client_id"] or not client_config["web"]["client_secret"]:
                raise Exception("Google API credentials not found. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.")
            
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('docs', 'v1', credentials=creds)
    return service

def get_document_info(document_id):
    """Get basic information about a Google Document"""
    try:
        service = get_google_docs_service()
        document = service.documents().get(documentId=document_id).execute()
        
        return {
            'title': document.get('title', 'Untitled Document'),
            'document_id': document_id,
            'revision_id': document.get('revisionId')
        }
        
    except Exception as e:
        logging.error(f"Error getting document info: {str(e)}")
        raise Exception(f"Failed to retrieve document info: {str(e)}")

def get_document_content(document_id):
    """Extract text content from a Google Document"""
    try:
        service = get_google_docs_service()
        document = service.documents().get(documentId=document_id).execute()
        
        content = []
        
        def extract_text_from_element(element):
            """Recursively extract text from document elements"""
            if 'textRun' in element:
                return element['textRun']['content']
            elif 'paragraph' in element:
                paragraph_text = ""
                for elem in element['paragraph'].get('elements', []):
                    paragraph_text += extract_text_from_element(elem)
                return paragraph_text
            elif 'table' in element:
                table_text = ""
                for row in element['table'].get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        for cell_element in cell.get('content', []):
                            table_text += extract_text_from_element(cell_element)
                return table_text
            return ""
        
        # Extract text from document body
        for element in document.get('body', {}).get('content', []):
            text = extract_text_from_element(element)
            if text.strip():
                content.append(text.strip())
        
        return '\n'.join(content)
        
    except Exception as e:
        logging.error(f"Error extracting document content: {str(e)}")
        raise Exception(f"Failed to extract document content: {str(e)}")

def extract_document_id_from_url(url):
    """Extract document ID from Google Docs URL"""
    import re
    
    # Pattern to match Google Docs URL and extract document ID
    pattern = r'/document/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        # If it's already just a document ID
        if re.match(r'^[a-zA-Z0-9-_]+$', url):
            return url
        raise ValueError("Invalid Google Docs URL or document ID")
