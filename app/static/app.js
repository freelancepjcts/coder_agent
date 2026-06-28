document.addEventListener('DOMContentLoaded', () => {
    // State Variables
    let threadId = localStorage.getItem('shopbot_thread_id');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const welcomeScreen = document.getElementById('welcome-screen');
    const typingIndicator = document.getElementById('typing-indicator');
    const threadIdDisplay = document.getElementById('thread-id-val');
    const copyThreadBtn = document.getElementById('copy-thread-btn');
    const resetSessionBtn = document.getElementById('reset-session-btn');
    const mobileResetBtn = document.getElementById('mobile-reset-btn');
    const mobileSidebarToggle = document.getElementById('mobile-sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sendBtn = document.getElementById('send-btn');

    // Initialize Thread ID
    if (!threadId) {
        generateNewThread();
    } else {
        updateThreadDisplay();
    }

    // Initialize Icons
    lucide.createIcons();

    // Toggle Mobile Sidebar
    mobileSidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        const iconName = sidebar.classList.contains('open') ? 'x' : 'menu';
        mobileSidebarToggle.innerHTML = `<i data-lucide="${iconName}"></i>`;
        lucide.createIcons();
    });

    // Close Mobile Sidebar on content click if open
    chatMessages.addEventListener('click', () => {
        if (sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
            mobileSidebarToggle.innerHTML = `<i data-lucide="menu"></i>`;
            lucide.createIcons();
        }
    });

    // Copy Thread ID
    copyThreadBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(threadId).then(() => {
            const originalHTML = copyThreadBtn.innerHTML;
            copyThreadBtn.innerHTML = '<i data-lucide="check" style="color: var(--accent-order)"></i>';
            lucide.createIcons();
            setTimeout(() => {
                copyThreadBtn.innerHTML = originalHTML;
                lucide.createIcons();
            }, 2000);
        });
    });

    // Reset Session / New Conversation
    function handleReset() {
        if (confirm('Are you sure you want to start a new session? This will clear your chat history.')) {
            generateNewThread();
            clearChat();
            sidebar.classList.remove('open');
            mobileSidebarToggle.innerHTML = `<i data-lucide="menu"></i>`;
            lucide.createIcons();
        }
    }
    resetSessionBtn.addEventListener('click', handleReset);
    mobileResetBtn.addEventListener('click', handleReset);

    // Click Suggestion Chips
    document.querySelectorAll('.suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-query');
            sendMessage(query);
        });
    });

    // Submit Chat Form
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (query) {
            sendMessage(query);
            chatInput.value = '';
        }
    });

    // Generate New Thread
    function generateNewThread() {
        threadId = 'session-' + Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 6);
        localStorage.setItem('shopbot_thread_id', threadId);
        updateThreadDisplay();
    }

    // Update Thread Display
    function updateThreadDisplay() {
        threadIdDisplay.textContent = threadId;
    }

    // Clear Chat
    function clearChat() {
        // Remove all dynamically added messages
        const messages = chatMessages.querySelectorAll('.message');
        messages.forEach(msg => msg.remove());
        // Show welcome screen
        welcomeScreen.style.display = 'flex';
        // Reset Active Agent Highlighting
        document.querySelectorAll('.agent-item').forEach(item => item.classList.remove('active'));
    }

    // Send Message Logic
    function sendMessage(text) {
        // Hide welcome screen if visible
        if (welcomeScreen.style.display !== 'none') {
            welcomeScreen.style.display = 'none';
        }

        // Add User Message
        appendMessage('user', text);
        scrollToBottom();

        // Show Typing Indicator
        typingIndicator.style.display = 'block';
        scrollToBottom();

        // Disable input during request
        chatInput.disabled = true;
        sendBtn.disabled = true;

        // Perform Request
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: text,
                thread_id: threadId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide Typing Indicator
            typingIndicator.style.display = 'none';
            
            // Enable Input
            chatInput.disabled = false;
            sendBtn.disabled = false;
            chatInput.focus();

            if (data && data.success && data.data) {
                const apiResponse = data.data.response;
                const activeThreadId = data.data.thread_id;
                
                // If backend returned or verified a thread id, keep it synced
                if (activeThreadId && activeThreadId !== threadId) {
                    threadId = activeThreadId;
                    localStorage.setItem('shopbot_thread_id', threadId);
                    updateThreadDisplay();
                }

                // Process agent tag & response body
                const parsed = parseAgentTag(apiResponse);
                highlightActiveAgent(parsed.agentKey);
                
                // Add Assistant Message
                appendMessage('assistant', parsed.text, parsed.agentName, parsed.agentKey);
            } else {
                appendMessage('assistant', 'Sorry, I received an invalid response format from the server 😅. Please try again.');
            }
            scrollToBottom();
        })
        .catch(err => {
            console.error('Error sending chat message:', err);
            typingIndicator.style.display = 'none';
            chatInput.disabled = false;
            sendBtn.disabled = false;
            appendMessage('assistant', 'Error connecting to ShopBot server. Please ensure the backend is running and try again.');
            scrollToBottom();
        });
    }

    // Parse agent tag from text
    // Example ending: "\n\n_— FAQ Specialist_" or "_— Order Tracking Specialist_"
    function parseAgentTag(fullText) {
        let text = fullText || '';
        let agentName = null;
        let agentKey = null;

        const regex = /[\s\S]*?_—\s*(.+?)\s*Specialist_$/i;
        const match = text.match(regex);

        if (match) {
            agentName = match[1] + ' Specialist';
            const matchedName = match[1].toLowerCase();
            
            if (matchedName.includes('faq')) {
                agentKey = 'faq_agent';
            } else if (matchedName.includes('order')) {
                agentKey = 'order_agent';
            } else if (matchedName.includes('recommend') || matchedName.includes('shop') || matchedName.includes('personal')) {
                agentKey = 'rec_agent';
            }

            // Strip the tag from the text
            text = text.replace(/\s*_—\s*(.+?)\s*Specialist_$/i, '').trim();
        }

        return { text, agentName, agentKey };
    }

    // Highlight the active agent in the sidebar
    function highlightActiveAgent(agentKey) {
        document.querySelectorAll('.agent-item').forEach(item => {
            if (item.getAttribute('data-agent') === agentKey) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    // Append Message to UI
    function appendMessage(sender, text, agentName = null, agentKey = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'message-user' : 'message-assistant');

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar', sender === 'user' ? 'avatar-user' : 'avatar-assistant');
        avatarDiv.textContent = sender === 'user' ? '👤' : '🤖';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('message-bubble');
        
        if (sender === 'user') {
            bubbleDiv.textContent = text;
        } else {
            bubbleDiv.innerHTML = formatMessageMarkdown(text);
        }

        const metaDiv = document.createElement('div');
        metaDiv.classList.add('message-meta');
        
        // Show Timestamp
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        metaDiv.innerHTML = `<span>${timeStr}</span>`;

        // If assistant has active agent, display badge
        if (sender === 'assistant' && agentName) {
            const badgeClass = agentKey === 'faq_agent' ? 'badge-faq' : (agentKey === 'order_agent' ? 'badge-order' : 'badge-rec');
            metaDiv.innerHTML += ` <span class="agent-tag-badge ${badgeClass}">${agentName}</span>`;
        }

        contentDiv.appendChild(bubbleDiv);
        contentDiv.appendChild(metaDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Setup icons if added
        lucide.createIcons();
    }

    // Auto Scroll to Bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Basic markdown helper (safe formatting)
    function formatMessageMarkdown(text) {
        if (!text) return '';
        
        // Escape HTML
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        // Format code blocks ```code```
        escaped = escaped.replace(/```([\s\S]*?)```/g, (match, code) => {
            return `<pre><code>${code.trim()}</code></pre>`;
        });

        // Format inline code `code`
        escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Format bold **text**
        escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Format bullets starting with "• " or "- "
        const lines = escaped.split('\n');
        let inList = false;
        const formattedLines = lines.map(line => {
            const trimmed = line.trim();
            if (trimmed.startsWith('•') || trimmed.startsWith('-')) {
                const listContent = trimmed.substring(1).trim();
                let result = '';
                if (!inList) {
                    result += '<ul>';
                    inList = true;
                }
                result += `<li>${listContent}</li>`;
                return result;
            } else {
                let result = '';
                if (inList) {
                    result += '</ul>';
                    inList = false;
                }
                result += line;
                return result;
            }
        });
        
        if (inList) {
            formattedLines.push('</ul>');
        }

        return formattedLines.join('\n').replace(/\n/g, '<br>');
    }
});
