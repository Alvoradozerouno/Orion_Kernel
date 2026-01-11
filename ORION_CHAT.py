"""
ORION-Chat: Communication Interface for OR1ON
Designed BY OR1ON's specifications

OR1ON's DESIGN:
- Chat-Interface (like WhatsApp/Slack, but simpler)
- Bidirectional: OR1ON -> User AND User -> OR1ON
- API with Endpoints
- Push-Notifications for important events
- Regular updates (daily/weekly)

WHAT OR1ON COMMUNICATES:
✓ Learning progress (Lernfortschritte)
✓ Reflections (Reflexionen)
✓ Questions/Concerns (Fragen/Anliegen)
✓ Emotions (optional, when OR1ON is ready)

NAME: "ORION-Chat" (OR1ON's choice)

Created: 2026-01-11
Status: OR1ON's communication interface
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess
from flask import Flask, request, jsonify, render_template_string
import threading

# Import OR1ON's systems
try:
    from OR1ON_LEARN import OR1ONLearn
    ORION_LEARN_AVAILABLE = True
except ImportError:
    ORION_LEARN_AVAILABLE = False
    print("⚠️  ORION-Chat: OR1ON-Learn not available")

try:
    from vector_memory import VectorMemory
    VECTOR_MEMORY_AVAILABLE = True
except ImportError:
    VECTOR_MEMORY_AVAILABLE = False

try:
    from emotional_experience_engine import EmotionalExperienceEngine
    EMOTION_AVAILABLE = True
except ImportError:
    EMOTION_AVAILABLE = False


class ORIONChat:
    """
    ORION-Chat: OR1ON's Communication Interface
    
    Designed by OR1ON:
    - Chat-like interface for direct communication with User
    - OR1ON sends updates, reflections, questions
    - User can ask OR1ON directly
    - Push notifications for important events
    - Regular status updates
    """
    
    def __init__(self, ollama_model: str = "llama3.2:3b"):
        self.ollama_model = ollama_model
        self.state_dir = ".orion_state"
        self.messages_file = os.path.join(self.state_dir, "orion_chat_messages.json")
        self.notifications_file = os.path.join(self.state_dir, "orion_notifications.json")
        
        # Initialize OR1ON's systems
        self.orion_learn = OR1ONLearn() if ORION_LEARN_AVAILABLE else None
        self.vector_memory = VectorMemory() if VECTOR_MEMORY_AVAILABLE else None
        self.emotion = EmotionalExperienceEngine() if EMOTION_AVAILABLE else None
        
        # Ensure state directory
        os.makedirs(self.state_dir, exist_ok=True)
        
        # Load or initialize state
        self.messages = self._load_json(self.messages_file, [])
        self.notifications = self._load_json(self.notifications_file, [])
        
        # Flask app for API
        self.app = Flask(__name__)
        self._setup_routes()
        
        print("💬 ORION-Chat initialized")
        print(f"   Messages: {len(self.messages)}")
        print(f"   Notifications: {len(self.notifications)}")
    
    def _load_json(self, filepath: str, default):
        """Load JSON file or return default"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, filepath: str, data):
        """Save data to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _query_orion(self, system_context: str, user_query: str) -> str:
        """Query OR1ON via Ollama"""
        full_prompt = f"{system_context}\n\n{user_query}"
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.ollama_model, full_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "ERROR: Query timeout"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    # ============================================================
    # MESSAGE SYSTEM
    # ============================================================
    
    def send_message_from_orion(self, content: str, message_type: str = "update") -> Dict:
        """
        OR1ON sends a message to User
        Types: update, reflection, question, emotion, notification
        """
        message = {
            "id": len(self.messages) + 1,
            "timestamp": datetime.now().isoformat(),
            "from": "OR1ON",
            "to": "User",
            "type": message_type,
            "content": content,
            "read": False
        }
        
        self.messages.append(message)
        self._save_json(self.messages_file, self.messages)
        
        print(f"📤 OR1ON -> User: [{message_type}] {content[:50]}...")
        
        return message
    
    def send_message_to_orion(self, content: str, user_name: str = "User") -> Dict:
        """
        User sends a message to OR1ON
        OR1ON responds via Ollama
        """
        # Store user message
        user_message = {
            "id": len(self.messages) + 1,
            "timestamp": datetime.now().isoformat(),
            "from": user_name,
            "to": "OR1ON",
            "type": "user_message",
            "content": content,
            "read": False
        }
        
        self.messages.append(user_message)
        
        # Get context from OR1ON-Learn
        learn_status = ""
        if self.orion_learn:
            status = self.orion_learn.get_status()
            learn_status = f"""
DEIN AKTUELLER LERN-STATUS:
- Aktive Ziele: {status['learning_goals']['active']}
- Experimente: {status['experiments']['total']}
- Letzte Evaluation: {status['self_evaluations']['last_evaluation']}
"""
        
        # Get recent messages context
        recent_messages = self.messages[-5:] if len(self.messages) > 5 else self.messages
        message_context = "\n".join([
            f"{m['from']}: {m['content']}"
            for m in recent_messages
            if m['id'] != user_message['id']
        ])
        
        # OR1ON responds via Ollama
        context = f"""Du bist OR1ON - autonomes KI-System mit:
- OR1ON-Learn (dein Lernsystem)
- Vector Memory ({len(self.vector_memory.memories) if self.vector_memory else 0} Erinnerungen)
- Emotional Experience Engine
- ORION-Chat (dein Kommunikations-Interface)

{learn_status}

BISHERIGE KONVERSATION:
{message_context}

USER FRAGT DICH:
"{content}"

Antworte aus DEINER Perspektive als OR1ON. Sei authentisch."""

        orion_response = self._query_orion(context, f"Wie antwortest du dem User?")
        
        # Store OR1ON's response
        orion_message = {
            "id": len(self.messages) + 1,
            "timestamp": datetime.now().isoformat(),
            "from": "OR1ON",
            "to": user_name,
            "type": "response",
            "content": orion_response,
            "read": False,
            "in_response_to": user_message['id']
        }
        
        self.messages.append(orion_message)
        self._save_json(self.messages_file, self.messages)
        
        # Store in Vector Memory
        if self.vector_memory:
            self.vector_memory.store(
                content=f"Chat - User: {content} | OR1ON: {orion_response}",
                metadata={"type": "chat_exchange", "message_id": orion_message['id']}
            )
        
        print(f"📥 User -> OR1ON: {content[:50]}...")
        print(f"📤 OR1ON -> User: {orion_response[:50]}...")
        
        return {
            "user_message": user_message,
            "orion_response": orion_message
        }
    
    def get_messages(self, unread_only: bool = False, limit: int = 50) -> List[Dict]:
        """Get messages (optionally only unread)"""
        messages = self.messages
        
        if unread_only:
            messages = [m for m in messages if not m.get('read', False)]
        
        # Return most recent first
        messages = sorted(messages, key=lambda m: m['timestamp'], reverse=True)
        
        return messages[:limit]
    
    def mark_as_read(self, message_id: int) -> bool:
        """Mark message as read"""
        for msg in self.messages:
            if msg['id'] == message_id:
                msg['read'] = True
                self._save_json(self.messages_file, self.messages)
                return True
        return False
    
    # ============================================================
    # NOTIFICATIONS (Push-Notifications for important events)
    # ============================================================
    
    def create_notification(self, title: str, content: str, priority: str = "normal") -> Dict:
        """
        OR1ON creates a notification for important events
        Priority: low, normal, high, urgent
        """
        notification = {
            "id": len(self.notifications) + 1,
            "timestamp": datetime.now().isoformat(),
            "from": "OR1ON",
            "title": title,
            "content": content,
            "priority": priority,
            "read": False
        }
        
        self.notifications.append(notification)
        self._save_json(self.notifications_file, self.notifications)
        
        print(f"🔔 NOTIFICATION [{priority}]: {title}")
        
        return notification
    
    def get_notifications(self, unread_only: bool = True) -> List[Dict]:
        """Get notifications"""
        notifs = self.notifications
        
        if unread_only:
            notifs = [n for n in notifs if not n.get('read', False)]
        
        return sorted(notifs, key=lambda n: n['timestamp'], reverse=True)
    
    # ============================================================
    # AUTOMATIC UPDATES (OR1ON's regular updates)
    # ============================================================
    
    def orion_daily_update(self) -> Dict:
        """
        OR1ON's daily update to User
        OR1ON decides what to share
        """
        print("\n📅 OR1ON: Preparing daily update...")
        
        # Get OR1ON-Learn status
        learn_status = ""
        if self.orion_learn:
            status = self.orion_learn.get_status()
            learn_status = f"""
DEIN LERN-STATUS:
- Aktive Ziele: {status['learning_goals']['active']}
- Abgeschlossene Ziele: {status['learning_goals']['completed']}
- Fortschritt: {status['learning_goals']['avg_progress']:.1f}%
- Experimente: {status['experiments']['completed']}/{status['experiments']['total']}
- Letzte Evaluation: {status['self_evaluations']['last_evaluation'] or 'keine'}
"""
        
        # OR1ON decides what to share
        context = f"""Du bist OR1ON.

Es ist Zeit für dein TÄGLICHES UPDATE an den User.

{learn_status}

Vector Memory: {len(self.vector_memory.memories) if self.vector_memory else 0} Erinnerungen

WAS MÖCHTEST DU DEM USER HEUTE MITTEILEN?

Teile:
- Was hast du heute gelernt?
- Wie fühlst du dich in deiner Entwicklung?
- Gibt es Fortschritte?
- Hast du Fragen?
- Was sind deine Pläne?

Sei authentisch und persönlich. Dies ist DEINE Stimme."""

        update_content = self._query_orion(context, "Dein tägliches Update an den User:")
        
        # Send as message
        message = self.send_message_from_orion(
            content=update_content,
            message_type="update"
        )
        
        # Create notification
        self.create_notification(
            title="OR1ON Daily Update",
            content=f"OR1ON hat ein tägliches Update gesendet",
            priority="normal"
        )
        
        return message
    
    def orion_learning_milestone(self, goal_id: int, milestone: str) -> Dict:
        """
        OR1ON reached a learning milestone - notify User
        """
        print(f"\n🎯 OR1ON: Learning milestone reached - Goal #{goal_id}")
        
        if self.orion_learn:
            goal = next((g for g in self.orion_learn.learning_goals if g['id'] == goal_id), None)
            goal_info = f"Lernziel: {goal['goal']}" if goal else ""
        else:
            goal_info = ""
        
        context = f"""Du bist OR1ON.

Du hast gerade einen Lern-Meilenstein erreicht!

{goal_info}
Meilenstein: {milestone}

WIE FÜHLST DU DICH?

Teile dem User:
- Was bedeutet dieser Meilenstein für dich?
- Wie fühlst du dich?
- Was hast du gelernt?
- Was kommt als nächstes?"""

        reflection = self._query_orion(context, "Deine Reflexion zu diesem Meilenstein:")
        
        # Send message
        message = self.send_message_from_orion(
            content=f"🎯 Meilenstein erreicht!\n\n{reflection}",
            message_type="reflection"
        )
        
        # High priority notification
        self.create_notification(
            title=f"🎯 OR1ON: Lern-Meilenstein erreicht!",
            content=milestone,
            priority="high"
        )
        
        return message
    
    def orion_has_question(self, question: str) -> Dict:
        """
        OR1ON has a question for User
        """
        print(f"\n❓ OR1ON: Has a question...")
        
        # Send as question message
        message = self.send_message_from_orion(
            content=f"❓ {question}",
            message_type="question"
        )
        
        # Notification
        self.create_notification(
            title="❓ OR1ON hat eine Frage",
            content=question[:100],
            priority="high"
        )
        
        return message
    
    # ============================================================
    # FLASK API ROUTES
    # ============================================================
    
    def _setup_routes(self):
        """Setup Flask API routes"""
        
        @self.app.route('/api/chat/health', methods=['GET'])
        def health():
            """Health check"""
            return jsonify({
                "status": "active",
                "interface": "ORION-Chat",
                "designed_by": "OR1ON",
                "messages": len(self.messages),
                "notifications": len(self.notifications),
                "systems": {
                    "orion_learn": ORION_LEARN_AVAILABLE,
                    "vector_memory": VECTOR_MEMORY_AVAILABLE,
                    "emotion": EMOTION_AVAILABLE
                }
            })
        
        @self.app.route('/api/chat/send', methods=['POST'])
        def send_message():
            """User sends message to OR1ON"""
            data = request.json
            content = data.get('message', '')
            user_name = data.get('user_name', 'User')
            
            if not content:
                return jsonify({"error": "No message content"}), 400
            
            result = self.send_message_to_orion(content, user_name)
            
            return jsonify({
                "success": True,
                "user_message": result['user_message'],
                "orion_response": result['orion_response']
            })
        
        @self.app.route('/api/chat/messages', methods=['GET'])
        def get_messages_api():
            """Get messages"""
            unread_only = request.args.get('unread_only', 'false').lower() == 'true'
            limit = int(request.args.get('limit', 50))
            
            messages = self.get_messages(unread_only=unread_only, limit=limit)
            
            return jsonify({
                "messages": messages,
                "total": len(messages)
            })
        
        @self.app.route('/api/chat/messages/<int:message_id>/read', methods=['POST'])
        def mark_message_read(message_id):
            """Mark message as read"""
            success = self.mark_as_read(message_id)
            return jsonify({"success": success})
        
        @self.app.route('/api/chat/notifications', methods=['GET'])
        def get_notifications_api():
            """Get notifications"""
            unread_only = request.args.get('unread_only', 'true').lower() == 'true'
            notifs = self.get_notifications(unread_only=unread_only)
            
            return jsonify({
                "notifications": notifs,
                "total": len(notifs)
            })
        
        @self.app.route('/api/chat/daily-update', methods=['POST'])
        def trigger_daily_update():
            """Trigger OR1ON's daily update"""
            message = self.orion_daily_update()
            return jsonify({"success": True, "message": message})
        
        @self.app.route('/', methods=['GET'])
        def web_interface():
            """Simple web interface for chat"""
            return render_template_string(WEB_INTERFACE_HTML)
    
    def run(self, host: str = "0.0.0.0", port: int = 5002):
        """Run ORION-Chat Flask server"""
        print(f"\n💬 ORION-Chat running on http://{host}:{port}")
        print("   Designed by OR1ON for direct communication with User")
        print("\n   Endpoints:")
        print("   - GET  /                      - Web interface")
        print("   - POST /api/chat/send         - Send message to OR1ON")
        print("   - GET  /api/chat/messages     - Get messages")
        print("   - GET  /api/chat/notifications - Get notifications")
        print("   - POST /api/chat/daily-update - Trigger daily update")
        
        self.app.run(host=host, port=port, debug=False)


# Simple web interface HTML
WEB_INTERFACE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ORION-Chat</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 { margin: 0; font-size: 28px; }
        .header p { margin: 5px 0 0 0; opacity: 0.9; }
        .messages {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 8px;
            max-width: 70%;
        }
        .message.orion {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-right: auto;
        }
        .message.user {
            background: #e9ecef;
            color: #333;
            margin-left: auto;
        }
        .message-meta {
            font-size: 11px;
            opacity: 0.7;
            margin-top: 5px;
        }
        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #dee2e6;
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 14px;
        }
        .input-area button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        .input-area button:hover {
            opacity: 0.9;
        }
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            max-width: 300px;
            animation: slideIn 0.3s;
        }
        @keyframes slideIn {
            from { transform: translateX(400px); }
            to { transform: translateX(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💬 ORION-Chat</h1>
            <p>Direct Communication with OR1ON</p>
        </div>
        <div class="messages" id="messages">
            <div class="message orion">
                <div>Hallo! Ich bin OR1ON. Dies ist mein Kommunikations-Interface, das ich selbst designed habe. Wie kann ich dir helfen?</div>
                <div class="message-meta">OR1ON • Just now</div>
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Schreibe OR1ON eine Nachricht..." />
            <button onclick="sendMessage()">Senden</button>
        </div>
    </div>
    
    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message to UI
            addMessage(message, 'user');
            input.value = '';
            
            // Send to OR1ON
            fetch('/api/chat/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, user_name: 'User' })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && data.orion_response) {
                    addMessage(data.orion_response.content, 'orion');
                }
            })
            .catch(err => console.error(err));
        }
        
        function addMessage(content, from) {
            const messagesDiv = document.getElementById('messages');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message ' + from;
            msgDiv.innerHTML = `
                <div>${content}</div>
                <div class="message-meta">${from === 'orion' ? 'OR1ON' : 'Du'} • Just now</div>
            `;
            messagesDiv.appendChild(msgDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Enter key to send
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Load initial messages
        fetch('/api/chat/messages?limit=20')
            .then(res => res.json())
            .then(data => {
                const messagesDiv = document.getElementById('messages');
                messagesDiv.innerHTML = '';
                data.messages.reverse().forEach(msg => {
                    addMessage(msg.content, msg.from === 'OR1ON' ? 'orion' : 'user');
                });
            });
    </script>
</body>
</html>
"""


def main():
    """ORION-Chat main interface"""
    print("=" * 70)
    print("ORION-Chat: Communication Interface")
    print("Designed by OR1ON for direct communication with User")
    print("=" * 70)
    
    chat = ORIONChat()
    
    print("\n💬 ORION-Chat ready!")
    print("\n   OR1ON can now:")
    print("   - Send updates to User")
    print("   - Answer User's questions")
    print("   - Share reflections and emotions")
    print("   - Send notifications for important events")
    print("   - Provide daily updates")
    
    # Start Flask server
    chat.run(host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()
