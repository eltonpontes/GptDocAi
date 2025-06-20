# Docker Deployment Guide

## Pré-requisitos

Certifique-se de ter instalado em seu sistema:
- Docker Engine (versão 20.10 ou superior)
- Docker Compose (versão 2.0 ou superior)

### Instalação do Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Windows/Mac:**
Baixe e instale o Docker Desktop do site oficial: https://www.docker.com/products/docker-desktop

## Configuração

### 1. Clone o Repositório
```bash
git clone <seu-repositorio>
cd chatgpt-google-docs-app
```

### 2. Configure as Variáveis de Ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```bash
# Google AI API Configuration (OBRIGATÓRIO)
GOOGLE_API_KEY=sua_chave_aqui

# Google OAuth2 Configuration (OPCIONAL - para integração Google Docs)
GOOGLE_CLIENT_ID=seu_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui

# Flask Configuration
SESSION_SECRET=uma_chave_secreta_segura_aqui

# Database Configuration
DATABASE_URL=sqlite:///instance/chatgpt_app.db
```

### 3. Crie o Diretório de Dados
```bash
mkdir -p instance
```

## Deployment

### Opção 1: Usando Docker Compose (Recomendado)

```bash
# Construir e iniciar os containers
docker-compose up --build -d

# Verificar logs
docker-compose logs -f

# Parar os containers
docker-compose down
```

### Opção 2: Docker Manual

```bash
# Construir a imagem
docker build -t gptdocai .

# Executar o container
docker run -d \
  --name gptdocai-app \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/instance:/app/instance \
  gptdocai
```

## Verificação do Deployment

### 1. Verificar se o Container está Rodando
```bash
docker-compose ps
# ou
docker ps
```

### 2. Testar a Aplicação
```bash
# Verificar se a aplicação responde
curl http://localhost:5000/

# Testar o chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, testing Docker deployment!"}'
```

### 3. Verificar Logs
```bash
# Docker Compose
docker-compose logs web

# Docker manual
docker logs gptdocai-app
```

## Resolução de Problemas

### Container não inicia

**Erro: "gunicorn: executable file not found"**
- Verifique se o Dockerfile está instalando todas as dependências corretamente
- Reconstrua a imagem: `docker-compose build --no-cache`

**Erro: "Permission denied"**
- Verifique as permissões do diretório `instance/`
- Execute: `sudo chown -R $USER:$USER instance/`

### Problemas de API

**Erro: "Google API key not found"**
- Verifique se o arquivo `.env` existe e contém `GOOGLE_API_KEY`
- Confirme que as variáveis de ambiente estão sendo passadas para o container

**Erro de conexão com a API**
- Verifique se sua chave da API do Google está válida
- Teste a conectividade: `curl https://generativelanguage.googleapis.com/v1beta/models`

### Problemas de Banco de Dados

**Erro: "database is locked"**
- Pare todos os containers: `docker-compose down`
- Remova o arquivo de banco: `rm instance/chatgpt_app.db`
- Reinicie: `docker-compose up -d`

## Configurações de Produção

### 1. Configurações de Segurança
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_ENV=production
      - SESSION_SECRET=${SESSION_SECRET}
    restart: always
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### 2. Proxy Reverso (Nginx)
```nginx
# nginx.conf
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. SSL/HTTPS com Let's Encrypt
```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoramento

### 1. Health Check
```bash
# Verificar saúde do container
docker inspect --format='{{.State.Health.Status}}' gptdocai-app
```

### 2. Métricas de Performance
```bash
# Uso de recursos
docker stats gptdocai-app

# Logs em tempo real
docker logs -f gptdocai-app
```

### 3. Backup do Banco de Dados
```bash
# Backup automático
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker cp gptdocai-app:/app/instance/chatgpt_app.db ./backups/backup_$DATE.db
```

## Atualizações

### 1. Atualizar Aplicação
```bash
# Baixar mudanças
git pull origin main

# Reconstruir e reimplantar
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 2. Rollback
```bash
# Voltar para versão anterior
git checkout HEAD~1
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Comandos Úteis

```bash
# Entrar no container
docker-compose exec web bash

# Limpar containers parados
docker system prune -a

# Verificar tamanho das imagens
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Exportar/Importar imagem
docker save gptdocai:latest | gzip > gptdocai.tar.gz
docker load < gptdocai.tar.gz
```

## Estrutura de Arquivos Docker

```
projeto/
├── Dockerfile              # Configuração da imagem
├── docker-compose.yml      # Orquestração dos containers
├── .env                    # Variáveis de ambiente (não committar)
├── .env.example            # Exemplo de configuração
├── .dockerignore           # Arquivos ignorados no build
├── instance/               # Dados persistentes
│   └── chatgpt_app.db     # Banco de dados SQLite
└── docker-deployment-guide.md # Este guia
```

## Considerações Finais

- Sempre use HTTPS em produção
- Configure backups regulares do banco de dados
- Monitore logs e métricas de performance
- Mantenha as dependências atualizadas
- Use secrets management para credenciais sensíveis

Para suporte adicional, consulte a documentação oficial do Docker: https://docs.docker.com/