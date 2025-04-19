document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatForm = document.getElementById('chat-form');
    const promptInput = document.getElementById('prompt-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const imageUpload = document.getElementById('image-upload');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const loadingContainer = document.getElementById('loading-container');
    const threadsStatus = document.getElementById('threads-status');

    // Variables
    let selectedImage = null;

    // Initialize socket connection
    const socket = io();

    // Auto-resize textarea
    promptInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        
        // Enable/disable send button based on input
        sendBtn.disabled = this.value.trim() === '' && !selectedImage;
    });

    // Handle image upload
    imageUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            
            // Check if file is an image
            if (!file.type.match('image.*')) {
                alert('Please select an image file');
                return;
            }
            
            // Store the selected image
            selectedImage = file;
            
            // Display image preview
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreviewContainer.style.display = 'block';
            };
            reader.readAsDataURL(file);
            
            // Enable send button
            sendBtn.disabled = false;
        }
    });

    // Remove selected image
    removeImageBtn.addEventListener('click', function() {
        selectedImage = null;
        imageUpload.value = '';
        imagePreviewContainer.style.display = 'none';
        
        // Disable send button if text is also empty
        sendBtn.disabled = promptInput.value.trim() === '';
    });

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const prompt = promptInput.value.trim();
        
        // Don't submit if both prompt and image are empty
        if (prompt === '' && !selectedImage) {
            return;
        }
        
        // Show loading indicator
        loadingContainer.style.display = 'flex';
        
        // Add user message to chat
        addMessage('user', prompt, selectedImage ? URL.createObjectURL(selectedImage) : null);
        
        // Prepare form data for submission
        const formData = new FormData();
        formData.append('prompt', prompt);
        
        if (selectedImage) {
            formData.append('image', selectedImage);
        }
        
        try {
            // Send request to server
            const response = await fetch('/api/chat', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Add assistant message to chat
                addMessage('assistant', data.response);
                
                // Update Threads status
                updateThreadsStatus(data.threads_posted, data.threads_message);
            } else {
                // Handle error
                addMessage('assistant', `Error: ${data.error || 'Something went wrong'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('assistant', `Error: ${error.message}`);
        } finally {
            // Hide loading indicator
            loadingContainer.style.display = 'none';
            
            // Clear input
            promptInput.value = '';
            promptInput.style.height = 'auto';
            selectedImage = null;
            imageUpload.value = '';
            imagePreviewContainer.style.display = 'none';
            
            // Disable send button
            sendBtn.disabled = true;
            
            // Scroll to bottom
            scrollToBottom();
        }
    });

    // Clear chat
    clearChatBtn.addEventListener('click', async function() {
        if (confirm('Are you sure you want to clear the chat?')) {
            try {
                const response = await fetch('/api/clear', {
                    method: 'POST'
                });
                
                if (response.ok) {
                    // Clear chat messages (except the welcome message)
                    const welcomeMessage = chatMessages.firstElementChild;
                    chatMessages.innerHTML = '';
                    chatMessages.appendChild(welcomeMessage);
                }
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        }
    });

    // New chat
    newChatBtn.addEventListener('click', function() {
        // Same as clear chat for now
        clearChatBtn.click();
    });

    // Add message to chat
    function addMessage(role, content, imageUrl = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        if (role === 'assistant') {
            const avatarImg = document.createElement('img');
            avatarImg.src = '/static/images/claude-avatar.png';
            avatarImg.alt = 'Claude Avatar';
            avatarDiv.appendChild(avatarImg);
        } else {
            const userIcon = document.createElement('i');
            userIcon.className = 'fas fa-user';
            avatarDiv.appendChild(userIcon);
        }
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Add image if provided (for user messages)
        if (imageUrl) {
            const img = document.createElement('img');
            img.src = imageUrl;
            img.alt = 'Uploaded Image';
            img.style.maxWidth = '100%';
            img.style.maxHeight = '300px';
            img.style.borderRadius = '8px';
            img.style.marginBottom = '12px';
            contentDiv.appendChild(img);
        }
        
        // Add text content
        if (content) {
            const p = document.createElement('p');
            p.textContent = content;
            contentDiv.appendChild(p);
        }
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        scrollToBottom();
    }

    // Update Threads status
    function updateThreadsStatus(posted, message) {
        const statusIndicator = threadsStatus.querySelector('.status-indicator');
        
        if (posted) {
            statusIndicator.textContent = 'Posted';
            statusIndicator.style.color = 'var(--success-color)';
        } else {
            statusIndicator.textContent = 'Failed';
            statusIndicator.style.color = 'var(--error-color)';
            
            // Show error message
            console.error('Threads posting error:', message);
        }
        
        // Reset after 3 seconds
        setTimeout(() => {
            statusIndicator.textContent = 'Enabled';
            statusIndicator.style.color = 'var(--success-color)';
        }, 3000);
    }

    // Scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Load conversation history
    async function loadConversation() {
        try {
            const response = await fetch('/api/conversation');
            const data = await response.json();
            
            // Clear existing messages (except welcome message)
            const welcomeMessage = chatMessages.firstElementChild;
            chatMessages.innerHTML = '';
            chatMessages.appendChild(welcomeMessage);
            
            // Add messages from history
            for (let i = 0; i < data.length; i += 2) {
                const userMessage = data[i];
                const assistantMessage = data[i + 1];
                
                if (userMessage) {
                    addMessage('user', userMessage.content, userMessage.has_image ? null : null);
                }
                
                if (assistantMessage) {
                    addMessage('assistant', assistantMessage.content);
                }
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    }

    // Initial load
    loadConversation();
});
