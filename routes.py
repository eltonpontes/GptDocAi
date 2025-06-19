import logging
from flask import render_template, request, jsonify, session
from app import app, db
from models import ChatMessage, GoogleDocument
from agent_service import get_ai_response
from google_docs_service import get_document_content, get_document_info
import uuid

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI responses"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        user_message = data.get('message', '')
        document_id = data.get('document_id', '')
        
        # Handle None values
        if user_message is None:
            user_message = ''
        if document_id is None:
            document_id = ''
            
        user_message = user_message.strip()
        document_id = document_id.strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Get document context if document_id is provided
        document_context = ""
        if document_id:
            try:
                document_context = get_document_content(document_id)
                logging.info(f"Retrieved document context: {len(document_context)} characters")
            except Exception as e:
                logging.error(f"Error retrieving document: {str(e)}")
                return jsonify({'error': f'Failed to retrieve document: {str(e)}'}), 400
        
        # Get AI response
        try:
            ai_response = get_ai_response(user_message, document_context)
        except Exception as e:
            logging.error(f"Error getting AI response: {str(e)}")
            return jsonify({'error': f'Failed to get AI response: {str(e)}'}), 500
        
        # Save to database
        chat_message = ChatMessage(
            user_message=user_message,
            ai_response=ai_response,
            session_id=session_id
        )
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'message_id': chat_message.id
        })
        
    except Exception as e:
        logging.error(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/chat/history')
def get_chat_history():
    """Get chat history for current session"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'messages': []})
        
        messages = ChatMessage.query.filter_by(session_id=session_id)\
                                  .order_by(ChatMessage.timestamp.asc())\
                                  .all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages]
        })
        
    except Exception as e:
        logging.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({'error': 'Failed to retrieve chat history'}), 500

@app.route('/api/documents', methods=['POST'])
def add_document():
    """Add a Google Document to the knowledge base"""
    try:
        data = request.get_json()
        document_id = data.get('document_id', '').strip()
        
        if not document_id:
            return jsonify({'error': 'Document ID is required'}), 400
        
        # Check if document already exists
        existing_doc = GoogleDocument.query.filter_by(document_id=document_id).first()
        if existing_doc:
            return jsonify({'error': 'Document already exists in knowledge base'}), 400
        
        # Get document info
        try:
            doc_info = get_document_info(document_id)
            content = get_document_content(document_id)
        except Exception as e:
            logging.error(f"Error retrieving document info: {str(e)}")
            return jsonify({'error': f'Failed to retrieve document: {str(e)}'}), 400
        
        # Save to database
        document = GoogleDocument(
            document_id=document_id,
            title=doc_info.get('title', 'Untitled Document'),
            content=content
        )
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document added successfully',
            'document': document.to_dict()
        })
        
    except Exception as e:
        logging.error(f"Error adding document: {str(e)}")
        return jsonify({'error': 'Failed to add document'}), 500

@app.route('/api/documents')
def list_documents():
    """List all documents in the knowledge base"""
    try:
        documents = GoogleDocument.query.order_by(GoogleDocument.last_updated.desc()).all()
        return jsonify({
            'documents': [doc.to_dict() for doc in documents]
        })
        
    except Exception as e:
        logging.error(f"Error listing documents: {str(e)}")
        return jsonify({'error': 'Failed to retrieve documents'}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history for current session"""
    try:
        session_id = session.get('session_id')
        if session_id:
            ChatMessage.query.filter_by(session_id=session_id).delete()
            db.session.commit()
        
        return jsonify({'message': 'Chat history cleared'})
        
    except Exception as e:
        logging.error(f"Error clearing history: {str(e)}")
        return jsonify({'error': 'Failed to clear history'}), 500
