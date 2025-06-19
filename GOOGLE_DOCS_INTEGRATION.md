# Integração com Google Docs API

## Visão Geral

Esta aplicação integra-se com a Google Docs API para permitir que os usuários adicionem documentos do Google Docs como fonte de conhecimento para o assistente de IA. O sistema extrai o conteúdo dos documentos e o utiliza como contexto para gerar respostas mais precisas e informadas.

## Arquitetura da Integração

### Componentes Principais

1. **agent_service.py** - Serviço de IA que processa mensagens com contexto de documentos
2. **google_docs_service.py** - Serviço para autenticação e extração de conteúdo do Google Docs
3. **models.py** - Modelo de dados para armazenar informações dos documentos
4. **routes.py** - Endpoints da API para gerenciar documentos

### Fluxo de Integração

```
1. Usuário fornece URL/ID do Google Docs
   ↓
2. Sistema autentica com Google OAuth2
   ↓
3. Extrai conteúdo e metadados do documento
   ↓
4. Armazena informações no banco de dados
   ↓
5. Utiliza conteúdo como contexto para respostas da IA
```

## Configuração Necessária

### Variáveis de Ambiente

```bash
# Chave da API do Google Gemini (obrigatória)
GOOGLE_API_KEY=sua_chave_aqui

# Credenciais OAuth2 do Google (opcionais para integração com Docs)
GOOGLE_CLIENT_ID=seu_client_id_aqui
GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
```

### Setup no Google Cloud Console

1. **Criar Projeto no Google Cloud Console**
   - Acesse https://console.cloud.google.com/
   - Crie um novo projeto ou selecione um existente

2. **Habilitar APIs Necessárias**
   ```
   - Google Docs API
   - Google Drive API (opcional, para melhor acesso)
   ```

3. **Configurar Credenciais OAuth2**
   - Vá para "APIs e Serviços" > "Credenciais"
   - Clique em "Criar Credenciais" > "ID do cliente OAuth 2.0"
   - Configure as URLs de redirecionamento autorizadas:
     ```
     http://localhost:5000/oauth/callback
     https://seu-dominio.replit.app/oauth/callback
     ```

4. **Configurar Tela de Consentimento**
   - Configure informações básicas do aplicativo
   - Adicione escopos necessários:
     ```
     https://www.googleapis.com/auth/documents.readonly
     https://www.googleapis.com/auth/drive.readonly
     ```

## Funcionalidades Implementadas

### 1. Extração de Conteúdo de Documentos

```python
def get_document_content(document_id):
    """
    Extrai texto completo de um documento do Google Docs
    
    Args:
        document_id (str): ID do documento do Google Docs
    
    Returns:
        str: Conteúdo textual do documento
    """
```

**Recursos:**
- Extração recursiva de texto de todos os elementos do documento
- Tratamento de diferentes tipos de conteúdo (parágrafos, listas, tabelas)
- Preservação da estrutura básica do texto

### 2. Obtenção de Metadados

```python
def get_document_info(document_id):
    """
    Obtém informações básicas sobre um documento
    
    Args:
        document_id (str): ID do documento
    
    Returns:
        dict: Informações do documento (título, etc.)
    """
```

**Informações Coletadas:**
- Título do documento
- ID único do documento
- Data de última modificação (quando disponível)

### 3. Gerenciamento de Documentos

#### Adicionar Documento
```http
POST /api/documents
Content-Type: application/json

{
  "document_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
}
```

#### Listar Documentos
```http
GET /api/documents/list
```

#### Integração com Chat
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Qual é o conteúdo principal do documento?",
  "document_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
}
```

## Modelos de Dados

### GoogleDocument

```python
class GoogleDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.String(128), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
```

**Campos:**
- `document_id`: ID único do documento no Google Docs
- `title`: Título do documento
- `content`: Conteúdo textual extraído
- `last_updated`: Timestamp da última atualização

## Tratamento de Erros

### Erros Comuns e Soluções

1. **Credenciais Não Configuradas**
   ```
   Erro: "Google API credentials not found"
   Solução: Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET
   ```

2. **Documento Inacessível**
   ```
   Erro: "Document not accessible"
   Solução: Verifique se o documento é público ou se as permissões estão corretas
   ```

3. **ID de Documento Inválido**
   ```
   Erro: "Invalid document ID"
   Solução: Verifique se o ID do documento está correto
   ```

4. **Limite de API Excedido**
   ```
   Erro: "Quota exceeded"
   Solução: Verifique os limites da API no Google Cloud Console
   ```

## Segurança

### Controle de Acesso
- A aplicação só acessa documentos públicos ou com permissões adequadas
- Utiliza OAuth2 para autenticação segura
- Não armazena credenciais do usuário permanentemente

### Privacidade
- Conteúdo dos documentos é armazenado localmente apenas para cache
- Dados podem ser removidos a qualquer momento
- Não compartilha informações dos documentos com terceiros

## Limitações Atuais

1. **Tipos de Conteúdo Suportados**
   - Texto simples
   - Parágrafos formatados
   - Listas básicas
   - Não suporta: imagens, gráficos, tabelas complexas

2. **Tamanho dos Documentos**
   - Documentos muito grandes podem demorar para processar
   - Conteúdo é limitado pelo tamanho máximo de contexto da IA

3. **Atualizações em Tempo Real**
   - Mudanças no documento original não são refletidas automaticamente
   - Necessário re-adicionar o documento para atualizar o conteúdo

## Melhorias Futuras

1. **Sincronização Automática**
   - Verificação periódica de atualizações nos documentos
   - Webhook para notificações de mudanças

2. **Suporte a Mais Tipos de Conteúdo**
   - Extração de texto de imagens (OCR)
   - Processamento de tabelas complexas
   - Suporte a comentários e sugestões

3. **Cache Inteligente**
   - Sistema de cache mais eficiente
   - Compressão de conteúdo para documentos grandes

4. **Interface Melhorada**
   - Preview dos documentos antes de adicionar
   - Gestão visual dos documentos no conhecimento base
   - Estatísticas de uso dos documentos

## Exemplo de Uso Completo

```javascript
// 1. Adicionar documento
fetch('/api/documents', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    document_id: '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
  })
});

// 2. Usar documento no chat
fetch('/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Resuma os pontos principais deste documento',
    document_id: '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
  })
});
```

## Logs e Debugging

### Logs Importantes
```python
# Sucesso na extração de conteúdo
INFO:root:Retrieved document context: 1234 characters

# Erro de autenticação
ERROR:root:Google API credentials not found

# Erro de acesso ao documento
ERROR:root:Error retrieving document: Document not accessible
```

### Debugging
- Verifique os logs do servidor para erros de API
- Confirme se as credenciais estão configuradas corretamente
- Teste com documentos públicos primeiro
- Verifique se as APIs estão habilitadas no Google Cloud Console