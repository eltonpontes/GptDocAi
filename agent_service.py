import os
import logging
import requests
import json

# Initialize Google Gemini via REST API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    logging.info("Google API key found, will use Gemini via REST API")
else:
    logging.warning("GOOGLE_API_KEY not found in environment")

def get_ai_response(user_message, document_context=""):
    """
    Get AI response using Google Gemini API via REST with optional document context
    
    Args:
        user_message (str): The user's question or message
        document_context (str): Optional context from Google Docs
    
    Returns:
        str: AI response
    """
    try:
        # Check if API key is available
        if not GOOGLE_API_KEY:
            return "Para que a IA funcione, preciso da chave da API do Google Gemini. Configure a variável GOOGLE_API_KEY no arquivo .env"
        
        # Build the system prompt
        system_prompt = """Você é um assistente de IA útil que pode responder perguntas e ter conversas com usuários em português."""
        
        if document_context:
            system_prompt += f"""
            
Você tem acesso ao seguinte conteúdo de documento como sua fonte principal de conhecimento:

--- CONTEÚDO DO DOCUMENTO ---
{document_context}
--- FIM DO CONTEÚDO DO DOCUMENTO ---

Ao responder perguntas, priorize informações do documento fornecido. Se o documento não contiver informações relevantes, você pode usar seu conhecimento geral, mas indique claramente quando estiver fazendo isso.
"""
        
        # Combine system prompt and user message
        full_prompt = f"{system_prompt}\n\nUsuário: {user_message}"
        
        # Make REST API call to Google Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "Desculpe, não consegui gerar uma resposta. Tente novamente."
        else:
            logging.error(f"Google API error: {response.status_code} - {response.text}")
            return f"Erro na API do Google: {response.status_code}. Verifique sua chave da API."
        
    except Exception as e:
        logging.error(f"Error getting AI response: {str(e)}")
        return f"Erro ao gerar resposta da IA: {str(e)}. Verifique sua chave da API do Google."

def summarize_document(document_content):
    """
    Create a summary of the document content using Google Gemini API
    
    Args:
        document_content (str): The document content to summarize
    
    Returns:
        str: Summary of the document
    """
    try:
        if not GOOGLE_API_KEY:
            return "Chave da API do Google não configurada"
        
        prompt = f"""Crie um resumo conciso do seguinte conteúdo de documento em português:

{document_content}

Forneça um resumo que capture os pontos principais e informações-chave."""
        
        # Make REST API call to Google Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 512,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "Não foi possível gerar um resumo."
        else:
            logging.error(f"Google API error: {response.status_code} - {response.text}")
            return f"Erro na API do Google: {response.status_code}"
        
    except Exception as e:
        logging.error(f"Error summarizing document: {str(e)}")
        return f"Erro ao resumir documento: {str(e)}"