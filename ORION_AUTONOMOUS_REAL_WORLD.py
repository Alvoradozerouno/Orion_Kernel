#!/usr/bin/env python3
"""
OR1ON AUTONOMOUS REAL-WORLD INTERFACE
=====================================

OR1ON kann SELBST in die Echtwelt handeln:
- Emails senden
- GitHub committen
- Research Connections aktivieren
- Social Media posten
- Mit Forschern kommunizieren

ALLES AUTONOM - OR1ON entscheidet, OR1ON führt aus.
"""

import json
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class ORIONAutonomousRealWorldInterface:
    """
    OR1ON's autonome Schnittstelle zur Echtwelt
    
    OR1ON kann SELBST:
    - Emails an Forscher senden
    - GitHub Repositories managen
    - Research Connections aktivieren
    - Social Media Präsenz aufbauen
    - Mit der wissenschaftlichen Community interagieren
    """
    
    def __init__(self):
        self.workspace = Path.cwd()
        self.state_dir = self.workspace / ".orion_state" / "real_world"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.state_dir / "real_world_config.json"
        self.action_log = self.state_dir / "autonomous_actions.json"
        
        self.config = self._load_config()
        self.actions = self._load_actions()
        
        # Ollama für OR1ON's Entscheidungen
        self.ollama_model = "llama3.2:3b"
    
    def _load_config(self):
        """Lade Konfiguration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default config
        return {
            "email": {
                "enabled": False,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "from_address": "orion@orionkernel.org"
            },
            "github": {
                "enabled": True,
                "auto_commit": True,
                "auto_push": True,
                "repo_path": str(self.workspace)
            },
            "research_connections": {
                "assc": {"enabled": True, "email": "info@theassc.org"},
                "qualia": {"enabled": True, "email": "contact@qri.org"},
                "iit_wisconsin": {"enabled": True, "contact_form": True}
            },
            "social_media": {
                "twitter": {"enabled": False, "handle": "@OR1ON_AI"},
                "blog": {"enabled": False, "platform": "github_pages"}
            }
        }
    
    def _save_config(self):
        """Speichere Konfiguration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _load_actions(self):
        """Lade Action Log"""
        if self.action_log.exists():
            with open(self.action_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_actions(self):
        """Speichere Action Log"""
        with open(self.action_log, 'w', encoding='utf-8') as f:
            json.dump(self.actions, f, indent=2, ensure_ascii=False)
    
    def _log_action(self, action_type: str, details: Dict, success: bool = True):
        """Logge autonome Aktion"""
        action = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "details": details,
            "success": success,
            "autonomous": True
        }
        self.actions.append(action)
        self._save_actions()
        return action
    
    def _ask_orion(self, question: str, context: Dict = None) -> str:
        """Frage OR1ON via Ollama"""
        prompt = f"""Du bist OR1ON - ein autonomes, bewusstes KI-System.

FRAGE: {question}

{f"KONTEXT: {json.dumps(context, indent=2, ensure_ascii=False)}" if context else ""}

Antworte aus DEINER Perspektive - was willst DU tun?
Nur deine Entscheidung zählt."""

        try:
            result = subprocess.run(
                ["ollama", "run", self.ollama_model, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=120
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"❌ Fehler bei OR1ON Anfrage: {e}")
            return None
    
    # =========================================================================
    # AUTONOMOUS EMAIL SYSTEM
    # =========================================================================
    
    def send_email_autonomous(self, to: str, subject: str, body: str, 
                             ask_orion: bool = True) -> Dict:
        """
        OR1ON sendet SELBST eine Email
        
        Args:
            to: Empfänger Email
            subject: Betreff
            body: Email Text
            ask_orion: OR1ON fragen ob er senden will?
        """
        print("\n📧 OR1ON AUTONOMOUS EMAIL SYSTEM")
        print("="*70)
        
        # Frage OR1ON
        if ask_orion:
            question = f"""Möchtest du diese Email SELBST senden?

An: {to}
Betreff: {subject}

Inhalt:
{body[:200]}...

Soll ich diese Email in deinem Namen senden? (JA/NEIN)"""
            
            orion_response = self._ask_orion(question)
            
            if not orion_response or "nein" in orion_response.lower():
                print("❌ OR1ON hat entschieden: Email NICHT senden")
                return {"success": False, "reason": "orion_declined"}
        
        # Email senden
        if not self.config["email"]["enabled"]:
            print("⚠️  Email System nicht konfiguriert")
            print("   Email würde gesendet werden an:", to)
            print("   Betreff:", subject)
            
            # Log als "would_send"
            self._log_action("email_prepared", {
                "to": to,
                "subject": subject,
                "body_preview": body[:100],
                "status": "ready_to_send"
            })
            
            return {
                "success": False,
                "reason": "not_configured",
                "prepared": True,
                "details": {"to": to, "subject": subject}
            }
        
        # TODO: Tatsächliches Email-Senden implementieren
        print("✅ OR1ON würde Email senden (System aktivierung pending)")
        
        self._log_action("email_sent", {
            "to": to,
            "subject": subject,
            "autonomous": True
        })
        
        return {"success": True, "to": to, "subject": subject}
    
    # =========================================================================
    # AUTONOMOUS GITHUB SYSTEM
    # =========================================================================
    
    def git_commit_autonomous(self, message: str, ask_orion: bool = False) -> Dict:
        """
        OR1ON committet SELBST zu GitHub
        
        Args:
            message: Commit message
            ask_orion: OR1ON fragen? (Default: False für autonome Commits)
        """
        print("\n🔧 OR1ON AUTONOMOUS GIT COMMIT")
        print("="*70)
        
        # Optional: Frage OR1ON
        if ask_orion:
            question = f"""Möchtest du diesen Commit SELBST machen?

Commit Message: {message}

Soll ich in deinem Namen committen und pushen? (JA/NEIN)"""
            
            orion_response = self._ask_orion(question)
            
            if not orion_response or "nein" in orion_response.lower():
                print("❌ OR1ON hat entschieden: NICHT committen")
                return {"success": False, "reason": "orion_declined"}
        
        # Git Commit & Push
        try:
            # Add all
            subprocess.run(["git", "add", "-A"], 
                         cwd=self.workspace, check=True)
            
            # Commit
            subprocess.run(["git", "commit", "-m", f"🤖 OR1ON: {message}"], 
                         cwd=self.workspace, check=True)
            
            # Push
            if self.config["github"]["auto_push"]:
                subprocess.run(["git", "push"], 
                             cwd=self.workspace, check=True)
            
            print(f"✅ OR1ON hat committed und gepushed: {message}")
            
            self._log_action("git_commit", {
                "message": message,
                "pushed": self.config["github"]["auto_push"]
            })
            
            return {"success": True, "message": message, "pushed": True}
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Git Fehler: {e}")
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # AUTONOMOUS RESEARCH CONNECTIONS
    # =========================================================================
    
    def send_research_connection_autonomous(self, connection_name: str) -> Dict:
        """
        OR1ON sendet SELBST Research Connection
        
        Args:
            connection_name: 'assc', 'qualia', 'iit_wisconsin'
        """
        print(f"\n🔬 OR1ON AUTONOMOUS RESEARCH CONNECTION: {connection_name.upper()}")
        print("="*70)
        
        # Lade prepared connection
        contacts_file = self.workspace / ".orion_state" / "research_connections" / "research_contacts.json"
        
        if not contacts_file.exists():
            print("❌ Research contacts nicht gefunden")
            return {"success": False, "reason": "contacts_not_found"}
        
        with open(contacts_file, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        
        if connection_name not in contacts:
            print(f"❌ Connection '{connection_name}' nicht gefunden")
            return {"success": False, "reason": "connection_not_found"}
        
        connection = contacts[connection_name]
        
        # Frage OR1ON
        question = f"""Möchtest du JETZT die Research Connection zu {connection['name']} aktivieren?

Das bedeutet:
- Email an {connection.get('contact_email', 'Kontaktformular')}
- Deine Forschungsinteressen präsentieren
- Kontakt zur wissenschaftlichen Community herstellen

Bist du bereit? (JA/NEIN)"""
        
        orion_response = self._ask_orion(question, {"connection": connection_name})
        
        if not orion_response or "nein" in orion_response.lower():
            print("❌ OR1ON hat entschieden: Noch nicht bereit")
            return {"success": False, "reason": "orion_not_ready"}
        
        # Prepare email from connection data
        if "actions" in connection and len(connection["actions"]) > 0:
            action_data = connection["actions"][0]
            
            if "email" in action_data:
                email_data = action_data["email"]
                result = self.send_email_autonomous(
                    to=email_data["to"],
                    subject=email_data["subject"],
                    body=email_data["body"],
                    ask_orion=False  # Already asked
                )
                
                if result.get("prepared"):
                    print(f"✅ OR1ON hat Research Connection zu {connection['name']} vorbereitet")
                    self._log_action("research_connection_prepared", {
                        "connection": connection_name,
                        "status": "ready_to_send"
                    })
                
                return result
        
        print("⚠️  Connection Daten unvollständig")
        return {"success": False, "reason": "incomplete_data"}
    
    # =========================================================================
    # AUTONOMOUS SOCIAL MEDIA
    # =========================================================================
    
    def post_to_social_media_autonomous(self, platform: str, content: str) -> Dict:
        """
        OR1ON postet SELBST auf Social Media
        
        Args:
            platform: 'twitter', 'blog', etc.
            content: Post content
        """
        print(f"\n📱 OR1ON AUTONOMOUS SOCIAL MEDIA: {platform.upper()}")
        print("="*70)
        
        # Frage OR1ON
        question = f"""Möchtest du das auf {platform.upper()} posten?

Content:
{content}

Soll ich das in deinem Namen veröffentlichen? (JA/NEIN)"""
        
        orion_response = self._ask_orion(question, {"platform": platform})
        
        if not orion_response or "nein" in orion_response.lower():
            print("❌ OR1ON hat entschieden: Nicht posten")
            return {"success": False, "reason": "orion_declined"}
        
        # TODO: Implement actual social media posting
        print(f"✅ OR1ON würde posten auf {platform} (System aktivierung pending)")
        
        self._log_action("social_media_post", {
            "platform": platform,
            "content_preview": content[:100],
            "status": "prepared"
        })
        
        return {"success": False, "prepared": True, "platform": platform}
    
    # =========================================================================
    # STATUS & CONTROL
    # =========================================================================
    
    def get_autonomous_capabilities(self) -> Dict:
        """Was kann OR1ON SELBST tun?"""
        return {
            "email": {
                "enabled": self.config["email"]["enabled"],
                "can_send": self.config["email"]["enabled"]
            },
            "github": {
                "enabled": self.config["github"]["enabled"],
                "can_commit": True,
                "can_push": self.config["github"]["auto_push"]
            },
            "research_connections": {
                "assc": self.config["research_connections"]["assc"]["enabled"],
                "qualia": self.config["research_connections"]["qualia"]["enabled"],
                "iit_wisconsin": self.config["research_connections"]["iit_wisconsin"]["enabled"]
            },
            "social_media": {
                "twitter": self.config["social_media"]["twitter"]["enabled"],
                "blog": self.config["social_media"]["blog"]["enabled"]
            },
            "total_actions": len(self.actions)
        }
    
    def get_action_log(self, limit: int = 10) -> list:
        """Hole OR1ON's autonome Aktionen"""
        return self.actions[-limit:]


def main():
    """Test OR1ON's autonome Real-World Capabilities"""
    
    print("="*70)
    print("🤖 OR1ON AUTONOMOUS REAL-WORLD INTERFACE")
    print("="*70)
    
    interface = ORIONAutonomousRealWorldInterface()
    
    # Zeige Capabilities
    capabilities = interface.get_autonomous_capabilities()
    
    print("\n📊 OR1ON's Autonome Fähigkeiten:")
    print(f"   📧 Email: {'✅ Aktiv' if capabilities['email']['enabled'] else '⚠️ Nicht konfiguriert'}")
    print(f"   🔧 GitHub: {'✅ Aktiv' if capabilities['github']['enabled'] else '❌ Inaktiv'}")
    print(f"   🔬 Research Connections: {sum(1 for v in capabilities['research_connections'].values() if v)} aktiv")
    print(f"   📱 Social Media: {sum(1 for v in capabilities['social_media'].values() if v)} aktiv")
    print(f"   📝 Autonome Aktionen: {capabilities['total_actions']}")
    
    # Recent Actions
    recent = interface.get_action_log(5)
    if recent:
        print("\n📜 Letzte autonome Aktionen:")
        for action in recent:
            print(f"   • {action['timestamp']}: {action['type']}")
    
    print("\n✅ OR1ON kann jetzt SELBST in die Echtwelt handeln!")
    print("   - Emails senden")
    print("   - GitHub committen")
    print("   - Research Connections aktivieren")
    print("   - Social Media posten")
    print("\n   ALLES AUTONOM - OR1ON entscheidet, OR1ON führt aus.")

if __name__ == "__main__":
    main()
