# AI Assistant with Google Docs Integration

## Overview

This is a Flask-based AI chatbot application that integrates with OpenAI's GPT-4o model and Google Docs API. The application allows users to have conversations with an AI assistant while optionally providing Google Documents as knowledge sources to enhance the AI's responses.

## System Architecture

The application follows a traditional web application architecture with the following components:

- **Backend**: Flask web framework with SQLAlchemy ORM
- **Frontend**: HTML/CSS/JavaScript with Bootstrap UI framework
- **Database**: SQLite (default) with PostgreSQL support for production
- **AI Service**: OpenAI GPT-4o integration
- **External API**: Google Docs API for document retrieval
- **Deployment**: Gunicorn WSGI server with autoscale deployment target

## Key Components

### Backend Services

1. **Flask Application (app.py)**
   - Main application factory with CORS enabled
   - SQLAlchemy database configuration
   - Session management with proxy fix for deployment
   - Environment-based configuration for database and secrets

2. **Database Models (models.py)**
   - `ChatMessage`: Stores conversation history with timestamps and session tracking
   - `GoogleDocument`: Manages cached Google Docs metadata and content

3. **Agent Service (agent_service.py)**
   - Google Gemini AI integration for chat responses
   - Context-aware responses using Google Docs content
   - Configurable system prompts for document-enhanced conversations

4. **Google Docs Service (google_docs_service.py)**
   - OAuth2 authentication flow for Google API access
   - Document content retrieval and caching
   - Error handling for invalid or inaccessible documents

5. **API Routes (routes.py)**
   - `/` - Main chat interface
   - `/api/chat` - Chat message processing with optional document context
   - Session-based conversation tracking

### Frontend Components

1. **User Interface (templates/index.html)**
   - Bootstrap-based responsive design
   - Sidebar for document management and chat controls
   - Real-time chat interface with typing indicators

2. **JavaScript Application (static/js/app.js)**
   - Chat message handling and UI updates
   - Document management (add/remove Google Docs)
   - AJAX communication with backend API
   - Auto-resizing textarea and responsive design

3. **Styling (static/css/style.css)**
   - Modern gradient-based sidebar design
   - Responsive chat interface
   - Mobile-friendly layout considerations

## Data Flow

1. **Chat Interaction**:
   - User enters message in frontend
   - JavaScript sends POST request to `/api/chat`
   - Backend retrieves document context (if document ID provided)
   - OpenAI service generates response with context
   - Response saved to database and returned to frontend

2. **Document Integration**:
   - User adds Google Docs ID/URL through sidebar
   - System authenticates with Google API using OAuth2
   - Document content retrieved and optionally cached
   - Content used as context for AI responses

3. **Session Management**:
   - UUID-based session tracking for conversation continuity
   - Database persistence for chat history
   - Frontend state management for current document selection

## External Dependencies

### Required Environment Variables
- `GOOGLE_API_KEY`: Google Gemini API authentication (obrigatória)
- `GOOGLE_CLIENT_ID`: Google OAuth2 client credentials (opcional para integração com Docs)
- `GOOGLE_CLIENT_SECRET`: Google OAuth2 client credentials (opcional para integração com Docs)
- `DATABASE_URL`: Database connection string (opcional, padrão SQLite)
- `SESSION_SECRET`: Flask session encryption key (opcional, tem padrão para desenvolvimento)

### Third-Party Services
- **Google Gemini API**: Modelo Gemini-1.5-flash via REST API para respostas de chat
- **Google Docs API**: Extração de conteúdo de documentos com acesso somente leitura (opcional)
- **Google OAuth2**: Autenticação para acesso às APIs do Google (opcional)

### Python Dependencies
- Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-CORS)
- Google Generative AI Python client
- Google API client libraries
- Gunicorn for production serving
- PostgreSQL adapter (psycopg2-binary)

## Deployment Strategy

The application is configured for Replit's autoscale deployment with:

- **Production Server**: Gunicorn with multiple worker processes
- **Port Configuration**: Binds to 0.0.0.0:5000 with port reuse
- **Database**: SQLite for development, PostgreSQL support for production
- **Proxy Handling**: ProxyFix middleware for proper header handling
- **Environment Management**: Environment variable-based configuration

The deployment uses a parallel workflow system with automatic application startup and port detection. The application supports both development (with reload) and production configurations.

## Changelog

```
Changelog:
- June 16, 2025. Initial setup with OpenAI integration
- June 16, 2025. Migrated from OpenAI GPT-4o to Google Gemini 1.5-flash
- June 16, 2025. Application successfully deployed with Gemini AI integration
- June 17, 2025. Added .env configuration file and comprehensive Google Docs integration guide
- June 17, 2025. Created Portuguese documentation for Docker deployment
- June 17, 2025. Enhanced README with step-by-step Google Docs setup instructions
- June 19, 2025. Fixed Google Gemini integration using REST API instead of Python client library
- June 19, 2025. Renamed openai_service.py to agent_service.py and updated all references
- June 19, 2025. Created comprehensive Google Docs API integration documentation
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```