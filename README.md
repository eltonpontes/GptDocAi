# ChatGPT Clone with Google Gemini Integration

A modern web application that provides a ChatGPT-like interface powered by Google's Gemini AI, with optional Google Docs integration for enhanced knowledge base functionality.

## Features

- **ChatGPT-like Interface**: Modern, responsive chat interface with real-time messaging
- **Google Gemini AI**: Powered by Google's Gemini 1.5-flash model for intelligent responses
- **Google Docs Integration**: Connect Google Documents as knowledge sources
- **Session Management**: Persistent chat history across sessions
- **Document Management**: Add and manage Google Docs in your knowledge base
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Docker Ready**: Complete containerization setup for easy deployment

## Screenshots

The application features a modern interface similar to ChatGPT with:
- Left sidebar for document management and chat controls
- Main chat area with message bubbles and typing indicators
- Real-time AI responses using Google Gemini

## Quick Start

### Prerequisites

- Python 3.11+
- Google API Key (for Gemini AI)
- Optional: Google OAuth credentials (for Docs integration)

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd chatgpt-clone
```

2. **Install dependencies**
```bash
pip install uv
uv sync
```

3. **Configure environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

4. **Set up your API keys in .env file:**
```bash
GOOGLE_API_KEY=your_actual_google_api_key
GOOGLE_CLIENT_ID=your_google_client_id (optional)
GOOGLE_CLIENT_SECRET=your_google_client_secret (optional)
```

5. **Run the application**
```bash
python main.py
```

6. **Open your browser**
Navigate to `http://localhost:5000`

### Docker Deployment

1. **Create environment file**
```bash
echo "GOOGLE_API_KEY=your_google_api_key" > .env
```

2. **Run with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the application**
Open `http://localhost:5000` in your browser

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send chat messages
- `GET /api/chat/history` - Retrieve chat history
- `POST /api/documents` - Add Google Documents
- `GET /api/documents` - List documents
- `POST /api/clear-history` - Clear chat history

## Configuration

### Required Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini API key

### Optional Environment Variables

- `GOOGLE_CLIENT_ID`: Google OAuth client ID (for Docs integration)
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret (for Docs integration)
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SESSION_SECRET`: Session encryption key (has secure default)

## Getting API Keys

### Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key (starts with "AIza...")

### Google OAuth (Optional - for Docs integration)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Docs API
4. Create OAuth 2.0 credentials
5. Add your domain to authorized origins

## Como Integrar Documentos do Google Docs

### Passo 1: Preparar seu Documento do Google

1. **Abra o Google Docs** e crie ou selecione o documento que deseja usar
2. **Configure as permissões de compartilhamento:**
   - Clique em "Compartilhar" no canto superior direito
   - Em "Acesso geral", selecione "Qualquer pessoa com o link"
   - Defina como "Leitor" (somente leitura é suficiente)
   - Clique em "Copiar link"

### Passo 2: Obter o ID do Documento

O link do Google Docs tem o formato:
```
https://docs.google.com/document/d/DOCUMENT_ID_AQUI/edit
```

**Exemplo:**
- Link: `https://docs.google.com/document/d/1ABC123xyz789DEF456/edit`
- ID do documento: `1ABC123xyz789DEF456`

### Passo 3: Adicionar o Documento na Aplicação

1. **Execute a aplicação** (`python main.py`)
2. **Abra no navegador** `http://localhost:5000`
3. **Na barra lateral esquerda**, encontre a seção "Knowledge Base"
4. **Cole o ID do documento** ou o link completo no campo de entrada
5. **Clique no botão "+"** para adicionar o documento

### Passo 4: Usar o Documento nas Conversas

1. **Clique no documento** na lista da barra lateral para selecioná-lo
2. **Quando selecionado**, aparecerá um indicador verde "Document Connected"
3. **Faça perguntas sobre o conteúdo** do documento no chat
4. **A IA usará o documento** como fonte principal de informação

### Exemplos de Uso

**Documento sobre "Manual de Vendas":**
- Pergunta: "Quais são as etapas do processo de vendas?"
- A IA responderá baseada no conteúdo do documento

**Documento sobre "Políticas da Empresa":**
- Pergunta: "Qual é a política de férias?"
- A IA consultará o documento para fornecer a resposta

### Solução de Problemas

**Erro "Document not found":**
- Verifique se o documento está compartilhado publicamente
- Confirme se o ID do documento está correto
- Teste o link no navegador para garantir acesso

**Erro de permissão:**
- Configure o Google OAuth (opcional, mas recomendado para documentos privados)
- Adicione as credenciais GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET no arquivo .env

## Architecture

- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **AI Service**: Google Gemini 1.5-flash
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Gunicorn WSGI server

## Project Structure

```
├── app.py              # Flask application factory
├── main.py             # Application entry point
├── routes.py           # API routes and handlers
├── models.py           # Database models
├── openai_service.py   # AI service integration
├── google_docs_service.py # Google Docs integration
├── templates/          # HTML templates
├── static/            # CSS, JS, and assets
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Multi-container setup
└── pyproject.toml     # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the deployment guide in `docker-deployment-guide.md`
2. Review the logs for error messages
3. Ensure all environment variables are properly set
4. Verify your Google API key has the necessary permissions