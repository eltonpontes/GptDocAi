class ChatApp {
    constructor() {
        this.currentDocumentId = null;
        this.isTyping = false;
        this.messageHistory = [];
        
        this.initializeElements();
        this.bindEvents();
        this.loadDocuments();
        this.loadChatHistory();
        this.autoResizeTextarea();
    }
    
    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        // Sidebar elements
        this.newChatBtn = document.getElementById('newChatBtn');
        this.documentInput = document.getElementById('documentInput');
        this.addDocumentBtn = document.getElementById('addDocumentBtn');
        this.documentsList = document.getElementById('documentsList');
        this.clearHistoryBtn = document.getElementById('clearHistoryBtn');
        this.documentIndicator = document.getElementById('documentIndicator');
        
        // Modals
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        this.errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
        this.errorMessage = document.getElementById('errorMessage');
    }
    
    bindEvents() {
        // Send message events
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Sidebar events
        this.newChatBtn.addEventListener('click', () => this.newChat());
        this.addDocumentBtn.addEventListener('click', () => this.addDocument());
        this.documentInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.addDocument();
            }
        });
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        
        // Show typing indicator
        this.showTyping();
        
        try {
            const response = await axios.post('/api/chat', {
                message: message,
                document_id: this.currentDocumentId
            });
            
            this.hideTyping();
            this.addMessage(response.data.response, 'ai');
            
        } catch (error) {
            this.hideTyping();
            this.showError(error.response?.data?.error || 'Failed to send message. Please try again.');
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${sender === 'user' ? 'fa-user' : 'fa-robot'}"></i>
            </div>
            <div class="message-content">
                <div class="message-text">${this.formatMessage(text)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatMessage(text) {
        // Simple formatting for line breaks and basic HTML escaping
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
    }
    
    showTyping() {
        this.isTyping = true;
        this.typingIndicator.style.display = 'block';
        this.sendBtn.disabled = true;
        this.scrollToBottom();
    }
    
    hideTyping() {
        this.isTyping = false;
        this.typingIndicator.style.display = 'none';
        this.sendBtn.disabled = false;
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    newChat() {
        // Clear current chat
        const welcomeMessage = this.chatMessages.querySelector('.ai-message');
        this.chatMessages.innerHTML = '';
        this.chatMessages.appendChild(welcomeMessage);
        
        // Reset document selection
        this.currentDocumentId = null;
        this.updateDocumentIndicator();
        
        // Clear active document selection
        document.querySelectorAll('.document-item').forEach(item => {
            item.classList.remove('active');
        });
    }
    
    async addDocument() {
        const documentIdOrUrl = this.documentInput.value.trim();
        if (!documentIdOrUrl) return;
        
        this.loadingModal.show();
        
        try {
            const response = await axios.post('/api/documents', {
                document_id: this.extractDocumentId(documentIdOrUrl)
            });
            
            this.loadingModal.hide();
            this.documentInput.value = '';
            this.loadDocuments();
            this.showSuccess('Document added successfully!');
            
        } catch (error) {
            this.loadingModal.hide();
            this.showError(error.response?.data?.error || 'Failed to add document. Please check the document ID or URL.');
        }
    }
    
    extractDocumentId(input) {
        // Extract document ID from Google Docs URL or return as-is if already an ID
        const urlPattern = /\/document\/d\/([a-zA-Z0-9-_]+)/;
        const match = input.match(urlPattern);
        return match ? match[1] : input;
    }
    
    async loadDocuments() {
        try {
            const response = await axios.get('/api/documents');
            this.renderDocuments(response.data.documents);
        } catch (error) {
            console.error('Failed to load documents:', error);
        }
    }
    
    renderDocuments(documents) {
        if (documents.length === 0) {
            this.documentsList.innerHTML = '<div class="empty-state">No documents added yet</div>';
            return;
        }
        
        this.documentsList.innerHTML = documents.map(doc => `
            <div class="document-item" data-document-id="${doc.document_id}">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="fw-semibold">${this.truncateText(doc.title, 30)}</div>
                        <small class="text-muted">Added ${this.formatDate(doc.last_updated)}</small>
                    </div>
                    <i class="fas fa-file-alt ms-2"></i>
                </div>
            </div>
        `).join('');
        
        // Bind click events to document items
        document.querySelectorAll('.document-item').forEach(item => {
            item.addEventListener('click', () => {
                const documentId = item.dataset.documentId;
                this.selectDocument(documentId, item);
            });
        });
    }
    
    selectDocument(documentId, element) {
        // Remove active class from all items
        document.querySelectorAll('.document-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Add active class to selected item
        element.classList.add('active');
        
        // Set current document
        this.currentDocumentId = documentId;
        this.updateDocumentIndicator();
    }
    
    updateDocumentIndicator() {
        if (this.currentDocumentId) {
            this.documentIndicator.style.display = 'block';
        } else {
            this.documentIndicator.style.display = 'none';
        }
    }
    
    async loadChatHistory() {
        try {
            const response = await axios.get('/api/chat/history');
            this.renderChatHistory(response.data.messages);
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    }
    
    renderChatHistory(messages) {
        // Clear existing messages except welcome message
        const welcomeMessage = this.chatMessages.querySelector('.ai-message');
        this.chatMessages.innerHTML = '';
        this.chatMessages.appendChild(welcomeMessage);
        
        // Add historical messages
        messages.forEach(msg => {
            this.addMessage(msg.user_message, 'user');
            this.addMessage(msg.ai_response, 'ai');
        });
    }
    
    async clearHistory() {
        if (!confirm('Are you sure you want to clear your chat history?')) return;
        
        try {
            await axios.post('/api/clear-history');
            this.newChat();
            this.showSuccess('Chat history cleared successfully!');
        } catch (error) {
            this.showError('Failed to clear chat history. Please try again.');
        }
    }
    
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorModal.show();
    }
    
    showSuccess(message) {
        // Create a temporary success alert
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    }
    
    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) return 'today';
        if (diffDays === 2) return 'yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        
        return date.toLocaleDateString();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});

// Handle responsive sidebar toggle for mobile
document.addEventListener('DOMContentLoaded', () => {
    const createMobileToggle = () => {
        if (window.innerWidth <= 768) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'btn btn-primary position-fixed';
            toggleBtn.style.cssText = 'top: 10px; left: 10px; z-index: 1001;';
            toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            
            toggleBtn.addEventListener('click', () => {
                document.querySelector('.sidebar').classList.toggle('show');
            });
            
            document.body.appendChild(toggleBtn);
        }
    };
    
    createMobileToggle();
    window.addEventListener('resize', createMobileToggle);
});
