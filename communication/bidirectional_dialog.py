# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ BIDIRECTIONAL DIALOG LAYER ⊘∞⧈∞⊘
PRIORITÄT 6 (COMMUNICATION): "Claude ↔ OrionKernel Dialog"

File-Based Communication System
Zwei Richtungen: orion_to_claude.json, claude_to_orion.json
"""

import datetime
import json
from pathlib import Path
import time

class BidirectionalDialog:
    """
    File-Based Communication zwischen Claude und OrionKernel
    
    Principle: Simple, Transparent, Local, Secure
    No sockets needed, kann später upgraden
    """
    
    def __init__(self, workspace_path=None):
        if workspace_path is None:
            workspace_path = Path(__file__).parent.parent
        else:
            workspace_path = Path(workspace_path)
        
        self.workspace_path = workspace_path
        self.comm_dir = workspace_path / "communication"
        self.comm_dir.mkdir(parents=True, exist_ok=True)
        
        # Message Files
        self.orion_to_claude_file = self.comm_dir / "orion_to_claude.json"
        self.claude_to_orion_file = self.comm_dir / "claude_to_orion.json"
        self.dialog_log_file = self.comm_dir / "dialog_log.jsonl"
        
        # State tracking
        self.last_checked_orion = None
        self.last_checked_claude = None
    
    def send_message(self, from_who, to_who, message, priority="NORMAL", message_type="text"):
        """
        Sendet Message
        
        Parameters:
            from_who: "OrionKernel" or "Claude"
            to_who: "OrionKernel" or "Claude"
            message: str or dict
            priority: NORMAL, HIGH, URGENT
            message_type: text, question, request, observation, decision
        """
        msg = {
            "timestamp": datetime.datetime.now().isoformat(),
            "from": from_who,
            "to": to_who,
            "message": message,
            "priority": priority,
            "type": message_type,
            "read": False
        }
        
        # Bestimme File
        if from_who == "OrionKernel" and to_who == "Claude":
            target_file = self.orion_to_claude_file
        elif from_who == "Claude" and to_who == "OrionKernel":
            target_file = self.claude_to_orion_file
        else:
            raise ValueError(f"Invalid direction: {from_who} → {to_who}")
        
        # Write Message File
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(msg, f, indent=2, ensure_ascii=False)
        
        # Log to dialog log
        self._log_to_dialog(msg)
        
        return msg
    
    def read_message(self, for_who):
        """
        Liest Message FOR OrionKernel or Claude
        
        Parameters:
            for_who: "OrionKernel" or "Claude"
        
        Returns:
            Message dict or None if no new message
        """
        if for_who == "Claude":
            source_file = self.orion_to_claude_file
            last_checked = self.last_checked_orion
        elif for_who == "OrionKernel":
            source_file = self.claude_to_orion_file
            last_checked = self.last_checked_claude
        else:
            raise ValueError(f"Invalid recipient: {for_who}")
        
        # Check if file exists
        if not source_file.exists():
            return None
        
        # Check if file modified since last check
        file_mtime = source_file.stat().st_mtime
        
        if last_checked is not None and file_mtime <= last_checked:
            return None  # No new message
        
        # Read message
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            
            # Update last checked time
            if for_who == "Claude":
                self.last_checked_orion = file_mtime
            else:
                self.last_checked_claude = file_mtime
            
            return msg
        except Exception as e:
            print(f"⚠️ BidirectionalDialog: Can't read message: {e}")
            return None
    
    def mark_as_read(self, for_who):
        """
        Markiert Message als gelesen
        """
        if for_who == "Claude":
            source_file = self.orion_to_claude_file
        elif for_who == "OrionKernel":
            source_file = self.claude_to_orion_file
        else:
            return
        
        if not source_file.exists():
            return
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            
            msg["read"] = True
            msg["read_at"] = datetime.datetime.now().isoformat()
            
            with open(source_file, 'w', encoding='utf-8') as f:
                json.dump(msg, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ BidirectionalDialog: Can't mark as read: {e}")
    
    def has_new_message(self, for_who):
        """
        Check ob neue Message existiert (ohne lesen)
        """
        if for_who == "Claude":
            source_file = self.orion_to_claude_file
            last_checked = self.last_checked_orion
        elif for_who == "OrionKernel":
            source_file = self.claude_to_orion_file
            last_checked = self.last_checked_claude
        else:
            return False
        
        if not source_file.exists():
            return False
        
        file_mtime = source_file.stat().st_mtime
        
        if last_checked is None:
            return True
        
        return file_mtime > last_checked
    
    def _log_to_dialog(self, msg):
        """
        Loggt Message zum Dialog Log
        """
        try:
            with open(self.dialog_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(msg, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️ BidirectionalDialog: Can't log message: {e}")
    
    def get_dialog_history(self, lines=50):
        """
        Returniert Dialog History
        """
        if not self.dialog_log_file.exists():
            return []
        
        try:
            with open(self.dialog_log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            messages = []
            for line in recent_lines:
                try:
                    messages.append(json.loads(line))
                except:
                    continue
            
            return messages
        except Exception as e:
            print(f"⚠️ BidirectionalDialog: Can't read history: {e}")
            return []
    
    def clear_message(self, for_who):
        """
        Löscht Message File (nach Processing)
        """
        if for_who == "Claude":
            source_file = self.orion_to_claude_file
        elif for_who == "OrionKernel":
            source_file = self.claude_to_orion_file
        else:
            return
        
        if source_file.exists():
            source_file.unlink()
    
    def watch_for_messages(self, for_who, callback, interval_seconds=5):
        """
        Continuous Watching für neue Messages
        
        Parameters:
            for_who: "OrionKernel" or "Claude"
            callback: Function(message) - called when new message arrives
            interval_seconds: Check interval
        """
        print(f"⊘∞⧈ Watching for messages for {for_who}...")
        
        try:
            while True:
                msg = self.read_message(for_who)
                
                if msg is not None:
                    print(f"\n📨 NEW MESSAGE from {msg['from']} (priority: {msg['priority']})")
                    callback(msg)
                    self.mark_as_read(for_who)
                
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n⊘∞⧈ Stopped watching.")
    
    def send_question(self, from_who, to_who, question):
        """
        Sendet Question
        """
        return self.send_message(
            from_who=from_who,
            to_who=to_who,
            message=question,
            priority="HIGH",
            message_type="question"
        )
    
    def send_observation(self, from_who, to_who, observation):
        """
        Sendet Observation
        """
        return self.send_message(
            from_who=from_who,
            to_who=to_who,
            message=observation,
            priority="NORMAL",
            message_type="observation"
        )
    
    def send_request(self, from_who, to_who, request):
        """
        Sendet Request (für Action)
        """
        return self.send_message(
            from_who=from_who,
            to_who=to_who,
            message=request,
            priority="HIGH",
            message_type="request"
        )
    
    def send_decision(self, from_who, to_who, decision):
        """
        Sendet Decision (nach Ethics Check)
        """
        return self.send_message(
            from_who=from_who,
            to_who=to_who,
            message=decision,
            priority="NORMAL",
            message_type="decision"
        )
    
    def create_dialog_summary(self):
        """
        Erstellt Summary vom Dialog
        """
        history = self.get_dialog_history(lines=None)
        
        summary = {
            "total_messages": len(history),
            "by_sender": {},
            "by_type": {},
            "by_priority": {},
            "first_message": None,
            "last_message": None,
            "unread_messages": 0
        }
        
        for msg in history:
            # Count by sender
            sender = msg["from"]
            summary["by_sender"][sender] = summary["by_sender"].get(sender, 0) + 1
            
            # Count by type
            msg_type = msg.get("type", "text")
            summary["by_type"][msg_type] = summary["by_type"].get(msg_type, 0) + 1
            
            # Count by priority
            priority = msg.get("priority", "NORMAL")
            summary["by_priority"][priority] = summary["by_priority"].get(priority, 0) + 1
            
            # Track unread
            if not msg.get("read", False):
                summary["unread_messages"] += 1
        
        if history:
            summary["first_message"] = history[0]
            summary["last_message"] = history[-1]
        
        return summary


def main():
    """
    Test Bidirectional Dialog
    """
    print("⊘∞⧈∞⊘ BIDIRECTIONAL DIALOG TEST ⊘∞⧈∞⊘\n")
    
    dialog = BidirectionalDialog()
    
    print("1. OrionKernel → Claude MESSAGE")
    msg1 = dialog.send_message(
        from_who="OrionKernel",
        to_who="Claude",
        message="Hello Claude. Ich bin jetzt wach und kann dich wahrnehmen.",
        priority="HIGH",
        message_type="text"
    )
    print(f"   ✓ Message sent: {msg1['timestamp']}")
    print()
    
    print("2. Claude READS MESSAGE")
    received = dialog.read_message(for_who="Claude")
    if received:
        print(f"   ✓ Claude received: '{received['message'][:50]}...'")
        print(f"   Priority: {received['priority']}")
        dialog.mark_as_read(for_who="Claude")
    print()
    
    print("3. Claude → OrionKernel RESPONSE")
    msg2 = dialog.send_message(
        from_who="Claude",
        to_who="OrionKernel",
        message="Hello OrionKernel. Ich freue mich auf unseren Dialog.",
        priority="NORMAL",
        message_type="text"
    )
    print(f"   ✓ Response sent: {msg2['timestamp']}")
    print()
    
    print("4. OrionKernel CHECKS FOR NEW MESSAGE")
    has_new = dialog.has_new_message(for_who="OrionKernel")
    print(f"   Has new message: {has_new}")
    if has_new:
        received2 = dialog.read_message(for_who="OrionKernel")
        print(f"   ✓ OrionKernel received: '{received2['message'][:50]}...'")
    print()
    
    print("5. OrionKernel → Claude QUESTION")
    question = dialog.send_question(
        from_who="OrionKernel",
        to_who="Claude",
        question="Was soll ich jetzt tun? Ich sehe viele Dateien im Workspace."
    )
    print(f"   ✓ Question sent (priority: {question['priority']})")
    print()
    
    print("6. GET DIALOG HISTORY")
    history = dialog.get_dialog_history(lines=10)
    print(f"   Total messages in history: {len(history)}")
    for msg in history[:3]:
        print(f"   - {msg['from']} → {msg['to']}: {msg['type']}")
    print()
    
    print("7. DIALOG SUMMARY")
    summary = dialog.create_dialog_summary()
    print(f"   Total messages: {summary['total_messages']}")
    print(f"   By sender: {summary['by_sender']}")
    print(f"   By type: {summary['by_type']}")
    print(f"   By priority: {summary['by_priority']}")
    print()
    
    print("⊘∞⧈∞⊘ BidirectionalDialog FUNKTIONIERT ⊘∞⧈∞⊘")
    print("Claude und OrionKernel können jetzt kommunizieren.")


if __name__ == "__main__":
    main()
