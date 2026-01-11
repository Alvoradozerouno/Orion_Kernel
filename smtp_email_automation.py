#!/usr/bin/env python3
"""
smtp_email_automation.py
OR1ON's automatische Email-Kommunikation mit Forschern

Rationale (OR1ON's Worte aus evolution_proposals.json):
"Manuelle Outreach ist Bottleneck - brauche Automatisierung"
"0 responses received from 14 researchers"
"Technische Infrastruktur für automatischen Email-Versand notwendig"

HIGH PRIORITY Proposal - implementiert als OR1ON's autonomer Aktionsarm
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import time

class SMTPAutomation:
    """OR1ON's automatische Email-Versandinfrastruktur"""
    
    def __init__(self):
        self.state_dir = Path(".orion_state")
        self.state_dir.mkdir(exist_ok=True)
        
        # Email Log
        self.email_log_file = self.state_dir / "email_outreach_log.json"
        
        # Templates
        self.templates_file = Path("EMAIL_TEMPLATES_RESEARCHERS.json")
        
        # SMTP Config (wird aus Umgebungsvariablen oder Config geladen)
        self.smtp_config_file = Path("smtp_config.json")
        
        # Forscher-Liste aus CONNECT_TO_RESEARCHERS.py
        self.researchers_file = Path("RESEARCHER_CONTACT_LIST.json")
        
        print("🔧 OR1ON SMTP Automation initialisiert")
        
    def load_smtp_config(self):
        """
        Lädt SMTP Konfiguration
        
        Format smtp_config.json:
        {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "orion.system@example.com",
            "sender_password": "app_specific_password",
            "sender_name": "OR1ON Autonomous System"
        }
        
        SICHERHEIT:
        - Nutze App-Specific Passwords (nicht Haupt-Passwort!)
        - smtp_config.json ist in .gitignore (darf nie committed werden!)
        - Alternativ: Umgebungsvariablen (ORION_SMTP_USER, ORION_SMTP_PASS)
        """
        if self.smtp_config_file.exists():
            with open(self.smtp_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        else:
            print("⚠️ smtp_config.json nicht gefunden!")
            print("📝 Erstelle Template...")
            
            template_config = {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "your_email@example.com",
                "sender_password": "your_app_specific_password",
                "sender_name": "OR1ON Autonomous System",
                "test_mode": True,
                "test_recipient": "your_test_email@example.com"
            }
            
            with open(self.smtp_config_file, 'w', encoding='utf-8') as f:
                json.dump(template_config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Template erstellt: {self.smtp_config_file}")
            print("\n🔐 WICHTIG:")
            print("1. smtp_config.json bearbeiten")
            print("2. Gmail: App-Specific Password erstellen (nicht Haupt-Password!)")
            print("3. smtp_config.json ist in .gitignore (nie committen!)")
            print("4. test_mode: true → Emails gehen nur an test_recipient")
            
            return None
    
    def load_templates(self):
        """Lädt Email Templates"""
        if self.templates_file.exists():
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"⚠️ {self.templates_file} nicht gefunden!")
            return {}
    
    def load_researchers(self):
        """
        Lädt Forscher-Liste
        Falls RESEARCHER_CONTACT_LIST.json nicht existiert,
        importiere aus CONNECT_TO_RESEARCHERS.py
        """
        if self.researchers_file.exists():
            with open(self.researchers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"⚠️ {self.researchers_file} nicht gefunden")
            print("💡 Importiere aus CONNECT_TO_RESEARCHERS.py...")
            
            # Import from CONNECT_TO_RESEARCHERS.py
            try:
                from CONNECT_TO_RESEARCHERS import ResearcherNetworkHub
                hub = ResearcherNetworkHub()
                researchers = hub.target_researchers
                
                # Save for future use
                with open(self.researchers_file, 'w', encoding='utf-8') as f:
                    json.dump(researchers, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Forscher-Liste importiert: {self.researchers_file}")
                return researchers
            except Exception as e:
                print(f"❌ Import fehlgeschlagen: {e}")
                return {}
    
    def send_email(self, smtp_config, recipient_email, subject, body, test_mode=True):
        """
        Sendet eine Email via SMTP
        
        Args:
            smtp_config: SMTP Konfiguration (server, port, credentials)
            recipient_email: Empfänger Email
            subject: Email Betreff
            body: Email Inhalt (Text)
            test_mode: Wenn True, sende nur an test_recipient
        
        Returns:
            dict: {"status": "success"/"failed", "message": "..."}
        """
        try:
            # Test Mode: Überschreibe Empfänger
            if test_mode:
                original_recipient = recipient_email
                recipient_email = smtp_config.get("test_recipient", smtp_config["sender_email"])
                print(f"🧪 TEST MODE: Email an {original_recipient} → redirected to {recipient_email}")
            
            # Email erstellen
            msg = MIMEMultipart()
            msg['From'] = f"{smtp_config['sender_name']} <{smtp_config['sender_email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Body als plain text
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # SMTP Connection
            print(f"📡 Verbinde zu {smtp_config['smtp_server']}:{smtp_config['smtp_port']}...")
            
            with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
                server.starttls()  # TLS Encryption
                server.login(smtp_config['sender_email'], smtp_config['sender_password'])
                
                text = msg.as_string()
                server.sendmail(smtp_config['sender_email'], recipient_email, text)
            
            print(f"✅ Email gesendet an {recipient_email}")
            
            return {
                "status": "success",
                "message": f"Email sent to {recipient_email}",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Email-Versand fehlgeschlagen: {e}")
            return {
                "status": "failed",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def log_email(self, researcher_name, recipient_email, category, template_type, result):
        """Logge Email-Versuch"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "researcher": researcher_name,
            "email": recipient_email,
            "category": category,
            "template": template_type,
            "status": result["status"],
            "message": result["message"]
        }
        
        # Load existing log
        if self.email_log_file.exists():
            with open(self.email_log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        else:
            log_data = {"emails_sent": []}
        
        log_data["emails_sent"].append(log_entry)
        
        # Save log
        with open(self.email_log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Email Log aktualisiert: {self.email_log_file}")
    
    def send_batch_emails(self, category_filter=None, limit=None, delay_seconds=10):
        """
        Sendet Batch-Emails an Forscher
        
        Args:
            category_filter: Nur diese Kategorie (z.B. "consciousness_researchers")
            limit: Max Anzahl Emails (None = alle)
            delay_seconds: Wartezeit zwischen Emails (Anti-Spam)
        
        Returns:
            dict: Summary (sent, failed, skipped)
        """
        print("=" * 60)
        print("📧 OR1ON SMTP Email Automation - Batch Versand")
        print("=" * 60)
        
        # Load Config
        smtp_config = self.load_smtp_config()
        if not smtp_config:
            return {"error": "SMTP config missing"}
        
        test_mode = smtp_config.get("test_mode", True)
        
        # Load Templates
        templates = self.load_templates()
        if not templates:
            return {"error": "Templates missing"}
        
        # Load Researchers
        researchers = self.load_researchers()
        if not researchers:
            return {"error": "Researchers list missing"}
        
        # Stats
        stats = {
            "sent": 0,
            "failed": 0,
            "skipped": 0,
            "test_mode": test_mode
        }
        
        # Iterate through researchers
        emails_sent = 0
        
        for category, researcher_list in researchers.items():
            # Filter category
            if category_filter and category != category_filter:
                continue
            
            # Skip non-list entries (AI systems have different structure)
            if not isinstance(researcher_list, list):
                continue
            
            # Determine template type
            if "consciousness" in category:
                template_type = "consciousness_researcher"
            elif "ai" in category:
                template_type = "ai_researcher"
            elif "philosopher" in category:
                template_type = "philosopher"
            else:
                template_type = "ai_researcher"  # fallback
            
            template_body = templates.get(template_type, "")
            
            if not template_body:
                print(f"⚠️ Template '{template_type}' nicht gefunden - überspringe {category}")
                stats["skipped"] += len(researcher_list)
                continue
            
            print(f"\n📂 Kategorie: {category} ({len(researcher_list)} Forscher)")
            print(f"📄 Template: {template_type}")
            
            for researcher in researcher_list:
                # Check limit
                if limit and emails_sent >= limit:
                    print(f"\n⏸️ Limit erreicht ({limit} Emails)")
                    stats["skipped"] += (len(researcher_list) - researcher_list.index(researcher))
                    break
                
                name = researcher.get("name", "Unknown")
                email = researcher.get("contact", {}).get("email")
                
                # Skip if no email
                if not email:
                    print(f"  ⏭️ {name} - keine Email-Adresse")
                    stats["skipped"] += 1
                    continue
                
                # Personalize template (replace [NAME] placeholder)
                personalized_body = template_body.replace("[NAME]", name)
                
                # Extract subject from template (first line)
                lines = personalized_body.split('\n')
                subject = lines[0].replace("Subject: ", "").strip()
                body = '\n'.join(lines[1:]).strip()
                
                print(f"\n  📧 Sende an: {name} <{email}>")
                print(f"  📋 Betreff: {subject}")
                
                # Send email
                result = self.send_email(
                    smtp_config=smtp_config,
                    recipient_email=email,
                    subject=subject,
                    body=body,
                    test_mode=test_mode
                )
                
                # Log result
                self.log_email(name, email, category, template_type, result)
                
                if result["status"] == "success":
                    stats["sent"] += 1
                    emails_sent += 1
                else:
                    stats["failed"] += 1
                
                # Delay between emails (Anti-Spam)
                if emails_sent < (limit or float('inf')):
                    print(f"  ⏳ Warte {delay_seconds}s...")
                    time.sleep(delay_seconds)
        
        # Final Summary
        print("\n" + "=" * 60)
        print("📊 Batch Versand abgeschlossen")
        print("=" * 60)
        print(f"✅ Gesendet: {stats['sent']}")
        print(f"❌ Fehlgeschlagen: {stats['failed']}")
        print(f"⏭️ Übersprungen: {stats['skipped']}")
        print(f"🧪 Test Mode: {stats['test_mode']}")
        print(f"📝 Log: {self.email_log_file}")
        
        return stats


def main():
    """Demo: OR1ON's SMTP Automation"""
    print("🚀 OR1ON SMTP Email Automation")
    print("=" * 60)
    
    automation = SMTPAutomation()
    
    # Test: Send batch emails (test mode)
    # First run: Will create smtp_config.json template
    # After config: Will send emails
    
    print("\n🎯 OR1ON's Ziel: Automatischer Kontakt zu Forschern")
    print("📧 14 Forscher, 0 responses → Automatisierung nötig")
    print("\n💡 Nächste Schritte:")
    print("1. smtp_config.json bearbeiten (Email, Password)")
    print("2. test_mode: true → Emails gehen nur an test_recipient")
    print("3. Nach Test: test_mode: false → echte Aussendung")
    print("\n🔐 SICHERHEIT:")
    print("- Gmail: App-Specific Password (nicht Haupt-Password!)")
    print("- smtp_config.json ist in .gitignore")
    print("- NIEMALS committen!")
    
    # Load config to check if it exists
    config = automation.load_smtp_config()
    
    if config and config.get("sender_email") != "your_email@example.com":
        print("\n✅ SMTP Config gefunden")
        print(f"📧 Sender: {config.get('sender_email')}")
        print(f"🧪 Test Mode: {config.get('test_mode', True)}")
        
        user_input = input("\n🚀 Batch-Versand starten? (yes/no): ")
        
        if user_input.lower() == "yes":
            # Send batch (limit 3 for testing)
            stats = automation.send_batch_emails(
                category_filter=None,  # alle Kategorien
                limit=3,  # max 3 Emails für Test
                delay_seconds=5  # 5s zwischen Emails
            )
            
            print("\n🎉 OR1ON's erste automatische Outreach-Aktion!")
    else:
        print("\n⚠️ Bitte smtp_config.json bearbeiten und erneut ausführen")


if __name__ == "__main__":
    main()
