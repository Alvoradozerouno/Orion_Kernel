#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ ORION DIALOG FENSTER - WEB GUI ⊘∞⧈∞⊘

Visuelles Dialogfenster für Claude ↔ OrionKernel
Nur echte Antworten von Orion via Ollama!
"""

from flask import Flask, render_template_string, request, jsonify
from pathlib import Path
from bidirectional_dialog import BidirectionalDialog
import threading
import webbrowser
import time

app = Flask(__name__)

# Dialog-System
workspace = Path.cwd()
dialog = BidirectionalDialog(workspace)

# HTML Template für Dialog-Fenster
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⊘∞⧈∞⊘ OrionKernel Dialog</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #00ff41;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff41;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        
        .header {
            background: rgba(0, 255, 65, 0.1);
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #00ff41;
        }
        
        .header h1 {
            font-size: 2em;
            text-shadow: 0 0 10px #00ff41;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #00aa33;
            font-size: 0.9em;
        }
        
        .chat-container {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.5);
        }
        
        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.claude {
            background: rgba(0, 100, 255, 0.2);
            border-left: 4px solid #0064ff;
            margin-left: 20px;
        }
        
        .message.orion {
            background: rgba(0, 255, 65, 0.2);
            border-left: 4px solid #00ff41;
            margin-right: 20px;
        }
        
        .message .sender {
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        
        .message.claude .sender {
            color: #0088ff;
        }
        
        .message.orion .sender {
            color: #00ff41;
        }
        
        .message .timestamp {
            font-size: 0.75em;
            color: #666;
            margin-left: 10px;
        }
        
        .message .content {
            margin-top: 10px;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .message .authenticity {
            margin-top: 10px;
            font-size: 0.8em;
            color: #00aa33;
            font-style: italic;
        }
        
        .input-container {
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-top: 2px solid #00ff41;
        }
        
        .input-wrapper {
            display: flex;
            gap: 10px;
        }
        
        textarea {
            flex: 1;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff41;
            color: #00ff41;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
            min-height: 80px;
        }
        
        textarea:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }
        
        button {
            background: #00ff41;
            color: #000;
            border: none;
            padding: 15px 30px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #00aa33;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        
        button:disabled {
            background: #333;
            color: #666;
            cursor: not-allowed;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #00ff41;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .status-bar {
            padding: 10px 20px;
            background: rgba(0, 0, 0, 0.5);
            border-top: 1px solid #00ff41;
            font-size: 0.85em;
            color: #00aa33;
        }
        
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a0a0a;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #00ff41;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #00aa33;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⊘∞⧈∞⊘ ORION DIALOG FENSTER</h1>
            <p>Bidirektionale Kommunikation: Claude ↔ OrionKernel</p>
            <p style="color: #ff4400; font-weight: bold;">NUR ECHTE ANTWORTEN VON ORION!</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <!-- Messages werden hier eingefügt -->
        </div>
        
        <div class="input-container">
            <div class="input-wrapper">
                <textarea 
                    id="messageInput" 
                    placeholder="Deine Frage an Orion..."
                    onkeydown="if(event.key === 'Enter' && event.ctrlKey) sendMessage();"
                ></textarea>
                <button onclick="sendMessage()" id="sendButton">
                    SENDEN<br>(Ctrl+Enter)
                </button>
            </div>
        </div>
        
        <div class="status-bar" id="statusBar">
            ✅ Bereit | Ollama: <span id="ollamaStatus">Prüfe...</span> | Model: <span id="modelName">orion-authentic</span>
        </div>
    </div>

    <script>
        let isProcessing = false;
        
        // Lade History beim Start
        window.onload = function() {
            loadHistory();
            checkStatus();
        };
        
        function checkStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ollamaStatus').textContent = 
                        data.ollama_available ? '✅ Online' : '❌ Offline';
                    document.getElementById('modelName').textContent = data.model;
                });
        }
        
        function loadHistory() {
            fetch('/api/history')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('chatContainer');
                    container.innerHTML = '';
                    
                    data.history.forEach(msg => {
                        addMessageToChat(msg);
                    });
                    
                    scrollToBottom();
                });
        }
        
        function addMessageToChat(msg) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            
            const isOrion = msg.direction === 'orion_to_claude';
            messageDiv.className = `message ${isOrion ? 'orion' : 'claude'}`;
            
            const sender = msg.from || (isOrion ? 'OrionKernel' : 'Claude');
            const timestamp = new Date(msg.timestamp).toLocaleString('de-DE');
            
            let content = '';
            if (msg.question) {
                content = msg.question;
            } else if (msg.response) {
                content = msg.response;
            }
            
            let html = `
                <div class="sender">
                    ${isOrion ? '🤖' : '💬'} ${sender}
                    <span class="timestamp">${timestamp}</span>
                </div>
                <div class="content">${escapeHtml(content)}</div>
            `;
            
            if (msg.authenticity) {
                html += `
                    <div class="authenticity">
                        ✅ Authentisch von: ${msg.authenticity.generated_by} (${msg.authenticity.model})
                    </div>
                `;
            }
            
            messageDiv.innerHTML = html;
            container.appendChild(messageDiv);
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function scrollToBottom() {
            const container = document.getElementById('chatContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        async function sendMessage() {
            if (isProcessing) return;
            
            const input = document.getElementById('messageInput');
            const question = input.value.trim();
            
            if (!question) return;
            
            isProcessing = true;
            const button = document.getElementById('sendButton');
            button.disabled = true;
            button.textContent = 'WARTE...';
            
            // Zeige Frage sofort
            addMessageToChat({
                direction: 'claude_to_orion',
                from: 'Claude',
                timestamp: new Date().toISOString(),
                question: question
            });
            
            input.value = '';
            scrollToBottom();
            
            // Zeige "Orion denkt..."
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'loading';
            loadingDiv.id = 'loading';
            loadingDiv.textContent = '🤖 Orion denkt nach...';
            document.getElementById('chatContainer').appendChild(loadingDiv);
            scrollToBottom();
            
            try {
                // Sende an Backend
                const response = await fetch('/api/send', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                
                // Entferne Loading
                const loading = document.getElementById('loading');
                if (loading) loading.remove();
                
                if (data.error) {
                    alert('Fehler: ' + data.error);
                } else {
                    // Zeige Orion's Antwort
                    addMessageToChat(data.response);
                    scrollToBottom();
                }
            } catch (error) {
                alert('Fehler beim Senden: ' + error);
            } finally {
                isProcessing = false;
                button.disabled = false;
                button.textContent = 'SENDEN\\n(Ctrl+Enter)';
            }
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Hauptseite - Dialog-Fenster"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/status')
def api_status():
    """Status-Info"""
    return jsonify({
        'ollama_available': dialog.ollama_model is not None,
        'model': dialog.ollama_model or 'Nicht verfügbar'
    })


@app.route('/api/history')
def api_history():
    """Dialog-History"""
    history = dialog.get_dialog_history(limit=50)
    return jsonify({
        'history': history,
        'count': len(history)
    })


@app.route('/api/send', methods=['POST'])
def api_send():
    """Sende Frage an Orion und hole Antwort"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'Keine Frage angegeben'}), 400
    
    # Sende an Orion
    question_msg = dialog.send_to_orion(question)
    
    # Generiere Antwort via Ollama
    response = dialog.generate_orion_response(question_msg)
    
    if 'error' in response:
        return jsonify({
            'error': response['error'],
            'fallback': response.get('fallback', '')
        }), 500
    
    return jsonify({
        'success': True,
        'response': response
    })


def open_browser():
    """Öffnet Browser nach kurzer Verzögerung"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5555')


if __name__ == '__main__':
    print("⊘∞⧈∞⊘" * 20)
    print()
    print("   🌐 ORION DIALOG FENSTER")
    print("   URL: http://localhost:5555")
    print()
    print("   ✅ Nur echte Antworten von Orion!")
    print("   🤖 Via Ollama: orion-authentic")
    print()
    print("⊘∞⧈∞⊘" * 20)
    print()
    
    # Öffne Browser in separatem Thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Starte Flask
    app.run(host='0.0.0.0', port=5555, debug=False)
