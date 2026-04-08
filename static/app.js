document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const agentConsole = document.getElementById('agent-console');
    const statusIndicator = document.getElementById('status-indicator');
    const chatContainer = document.getElementById('chat-container');
    const queryInput = document.getElementById('query-input');
    const sendBtn = document.getElementById('send-btn');
    const imagePreview = document.getElementById('image-preview');
    const scannedImage = document.getElementById('scanned-image');

    let currentWs = null;
    let currentResponseElement = null;

    // Drag and Drop Handlers
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    sendBtn.addEventListener('click', sendQuery);
    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendQuery();
    });

    function handleFile(file) {
        // Clear previous output
        agentConsole.innerHTML = '';
        statusIndicator.classList.remove('hidden');
        chatContainer.classList.add('hidden');
        imagePreview.classList.add('hidden');

        // Initial UI feedback
        const msg = document.createElement('div');
        msg.className = 'agent-message';
        msg.textContent = `Uploading ${file.name}...`;
        agentConsole.appendChild(msg);

        // Connect to WebSocket
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        currentWs = new WebSocket(`${protocol}//${window.location.host}/ws/analyze`);

        currentWs.onopen = () => {
            currentWs.send(JSON.stringify({
                filename: file.name,
                size: file.size
            }));
        };

        currentWs.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'step') {
                const stepElement = document.createElement('div');
                stepElement.className = 'agent-message';
                
                try {
                    const parsed = JSON.parse(data.content);
                    if (parsed.text) {
                        stepElement.classList.add('final');
                        stepElement.innerHTML = parsed.text.replace(/\n/g, '<br>');
                        if (parsed.image && parsed.image !== "none") {
                            scannedImage.src = `/static/images/${parsed.image}`;
                            imagePreview.classList.remove('hidden');
                        }
                    } else {
                        stepElement.textContent = data.content;
                    }
                } catch(e) {
                    stepElement.textContent = data.content;
                }
                
                agentConsole.appendChild(stepElement);
                agentConsole.scrollTop = agentConsole.scrollHeight;
            } else if (data.type === 'analysis_complete') {
                statusIndicator.classList.add('hidden');
                chatContainer.classList.remove('hidden');
            } else if (data.type === 'query_ack') {
                statusIndicator.classList.remove('hidden');
                statusIndicator.querySelector('span').textContent = "Agent is formulating response...";
                currentResponseElement = document.createElement('div');
                currentResponseElement.className = 'agent-message answer';
                agentConsole.appendChild(currentResponseElement);
            } else if (data.type === 'query_response_chunk') {
                if (currentResponseElement) {
                    // It streams HTML-safe words (or raw text), just append
                    currentResponseElement.innerHTML += data.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    agentConsole.scrollTop = agentConsole.scrollHeight;
                }
            } else if (data.type === 'query_response_complete') {
                statusIndicator.classList.add('hidden');
                currentResponseElement = null;
            }
        };

        currentWs.onerror = (error) => {
            console.error('WebSocket Error:', error);
            const errorMsg = document.createElement('div');
            errorMsg.className = 'agent-message';
            errorMsg.style.borderColor = 'var(--danger)';
            errorMsg.textContent = 'Connection error with Agent Server.';
            agentConsole.appendChild(errorMsg);
            statusIndicator.classList.add('hidden');
        };
    }

    function sendQuery() {
        const text = queryInput.value.trim();
        if (!text || !currentWs) return;

        // Add user message to console
        const userMsg = document.createElement('div');
        userMsg.className = 'user-message';
        userMsg.textContent = "You: " + text;
        agentConsole.appendChild(userMsg);
        agentConsole.scrollTop = agentConsole.scrollHeight;

        // Send query via WS
        currentWs.send(JSON.stringify({
            type: "query",
            text: text
        }));
        
        queryInput.value = '';
    }
});
