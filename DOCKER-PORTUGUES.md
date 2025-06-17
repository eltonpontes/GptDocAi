# Guia de Deploy com Docker

## Início Rápido

1. **Criar arquivo de ambiente:**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas chaves de API
nano .env
```

2. **Configure as variáveis no arquivo .env:**
```bash
# Obrigatório - Chave da API do Google Gemini
GOOGLE_API_KEY=sua_chave_do_google_aqui

# Opcional - Para integração com Google Docs
GOOGLE_CLIENT_ID=seu_google_client_id
GOOGLE_CLIENT_SECRET=seu_google_client_secret

# Opcional - Chave de sessão personalizada
SESSION_SECRET=sua_chave_secreta_aleatoria
```

3. **Executar com Docker Compose:**
```bash
docker-compose up --build
```

4. **Acessar a aplicação:**
   - Abra http://localhost:5000 no seu navegador
   - Sua interface tipo ChatGPT estará pronta

## O que está incluído

- **Aplicação Web**: Clone do ChatGPT com IA Google Gemini
- **Banco de Dados**: PostgreSQL para armazenar histórico de conversas e documentos
- **Auto-reinício**: Containers reiniciam automaticamente se travarem
- **Verificação de saúde**: Monitoramento integrado da aplicação web

## Variáveis de Ambiente

### Obrigatórias:
- `GOOGLE_API_KEY`: Sua chave da API Google Gemini

### Opcionais:
- `GOOGLE_CLIENT_ID`: Para integração com Google Docs
- `GOOGLE_CLIENT_SECRET`: Para integração com Google Docs  
- `SESSION_SECRET`: Chave personalizada de criptografia de sessão

## Banco de Dados

O PostgreSQL automaticamente:
- Cria tabelas na primeira execução
- Persiste dados em volumes Docker
- Mantém backup dos dados entre reinicializações

## Personalização

Para modificar a aplicação:
1. Edite os arquivos fonte
2. Reconstrua: `docker-compose up --build`
3. Mudanças no banco de dados persistem automaticamente

## Deploy em Produção

Para produção, considere:
- Usar um serviço de banco gerenciado
- Adicionar certificados SSL/TLS
- Configurar logs adequados
- Configurar limites de recursos
- Usar Docker secrets para chaves de API

## Solução de Problemas

### Erro "API key não encontrada":
- Verifique se o arquivo .env está na pasta raiz
- Confirme se GOOGLE_API_KEY está definida corretamente
- Teste a chave no Google AI Studio

### Erro de conexão com banco:
- Execute: `docker-compose down && docker-compose up --build`
- Verifique se a porta 5432 não está sendo usada

### Container não inicia:
- Verifique os logs: `docker-compose logs`
- Confirme se todas as dependências foram instaladas

## Comandos Úteis

```bash
# Ver logs da aplicação
docker-compose logs -f web

# Ver logs do banco de dados
docker-compose logs -f db

# Parar todos os containers
docker-compose down

# Remover volumes (dados serão perdidos)
docker-compose down -v

# Reconstruir apenas a aplicação
docker-compose up --build web
```