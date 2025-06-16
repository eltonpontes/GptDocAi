# Docker Deployment Guide

## Quick Start

1. **Create environment file:**
```bash
# Create .env file with your API keys
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
echo "GOOGLE_CLIENT_ID=your_google_client_id" >> .env
echo "GOOGLE_CLIENT_SECRET=your_google_client_secret" >> .env
echo "SESSION_SECRET=your_random_secret_key" >> .env
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access your application:**
   - Open http://localhost:5000 in your browser
   - Your ChatGPT-like interface will be ready

## What's Included

- **Web Application**: Flask-based ChatGPT clone with Google Gemini AI
- **Database**: PostgreSQL for storing chat history and documents
- **Auto-restart**: Containers restart automatically if they crash
- **Health checks**: Built-in monitoring for the web application

## Environment Variables

Required:
- `GOOGLE_API_KEY`: Your Google Gemini API key

Optional:
- `GOOGLE_CLIENT_ID`: For Google Docs integration
- `GOOGLE_CLIENT_SECRET`: For Google Docs integration  
- `SESSION_SECRET`: Custom session encryption key

## Database

The PostgreSQL database automatically:
- Creates tables on first run
- Persists data in Docker volumes
- Backs up data between container restarts

## Customization

To modify the application:
1. Edit source files
2. Rebuild: `docker-compose up --build`
3. Database changes persist automatically

## Production Deployment

For production, consider:
- Using a managed database service
- Adding SSL/TLS certificates
- Setting up proper logging
- Configuring resource limits
- Using Docker secrets for API keys