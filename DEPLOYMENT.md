# Deployment Guide

## GitHub Export Instructions

### Method 1: Direct Export from Replit

1. **Export to GitHub from Replit:**
   - Click the "Version control" tab in Replit
   - Select "Connect to GitHub"
   - Choose "Create new repository" or connect to existing
   - Push your code directly

### Method 2: Manual Git Setup

1. **Initialize Git repository:**
```bash
git init
git add .
git commit -m "Initial commit: ChatGPT clone with Google Gemini"
```

2. **Create GitHub repository:**
   - Go to GitHub.com
   - Click "New repository"
   - Name it (e.g., "chatgpt-gemini-clone")
   - Don't initialize with README (you already have one)

3. **Connect and push:**
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

## Environment Setup for New Deployments

1. **Required Environment Variables:**
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

2. **Optional Variables:**
```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SESSION_SECRET=your_random_secret_key
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

## Platform-Specific Deployment

### Replit (Current Platform)
- Already configured and running
- Uses workflow-based deployment
- Automatic restarts and scaling

### Heroku
```bash
# Add Heroku remote
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

### Railway
```bash
# Deploy with Railway CLI
railway login
railway init
railway up
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt  # or uv sync
# Set environment variables
export GOOGLE_API_KEY="your_key"
# Run application
python main.py
```

### Docker Deployment
```bash
# Build and run
docker-compose up --build

# Or build manually
docker build -t chatgpt-clone .
docker run -p 5000:5000 -e GOOGLE_API_KEY=your_key chatgpt-clone
```

## Production Considerations

1. **Security:**
   - Use environment variables for all secrets
   - Enable HTTPS in production
   - Set secure session cookies

2. **Database:**
   - Use PostgreSQL for production
   - Set up regular backups
   - Consider connection pooling

3. **Monitoring:**
   - Add logging and error tracking
   - Set up health checks
   - Monitor API usage and costs

4. **Performance:**
   - Configure caching for documents
   - Optimize database queries
   - Set up CDN for static assets