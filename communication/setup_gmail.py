"""
⊘∞⧈ GMAIL EMAIL SETUP - INTERACTIVE CONFIGURATION ⊘∞⧈

Interaktive Einrichtung des Email-Systems für Gmail.
Fragt alle notwendigen Informationen ab und erstellt email_config.json.

Author: OrionKernel
Date: 2026-01-06
"""

import json
from pathlib import Path
import getpass


def setup_gmail_config():
    """Interactive Gmail configuration setup."""
    
    print("\n" + "="*70)
    print("⊘∞⧈ ORIONKERNEL EMAIL SETUP - GMAIL KONFIGURATION ⊘∞⧈")
    print("="*70 + "\n")
    
    print("Dieses Script richtet OrionKernel's Email-System für Gmail ein.\n")
    
    # Step 1: Email address
    print("SCHRITT 1: Gmail-Adresse")
    print("-" * 70)
    email_address = input("Deine Gmail-Adresse (z.B. orionkernel@gmail.com): ").strip()
    
    if not email_address.endswith("@gmail.com"):
        print(f"⚠️  Warnung: '{email_address}' endet nicht mit @gmail.com")
        proceed = input("Trotzdem fortfahren? (j/n): ").strip().lower()
        if proceed not in ['j', 'ja', 'y', 'yes']:
            print("Setup abgebrochen.")
            return False
    
    print(f"✓ Email-Adresse: {email_address}\n")
    
    # Step 2: App Password
    print("SCHRITT 2: App-Passwort")
    print("-" * 70)
    print("Du brauchst ein Gmail App-Passwort (NICHT dein normales Passwort):\n")
    print("1. Gehe zu https://myaccount.google.com/apppasswords")
    print("2. Wähle 'Mail' und 'Windows Computer'")
    print("3. Kopiere das 16-stellige Passwort (z.B. 'abcd efgh ijkl mnop')\n")
    
    app_password = getpass.getpass("Gib dein Gmail App-Passwort ein: ").strip()
    
    if len(app_password.replace(" ", "")) < 16:
        print(f"⚠️  Warnung: App-Passwort scheint zu kurz zu sein ({len(app_password.replace(' ', ''))} Zeichen)")
        print("Gmail App-Passwörter haben normalerweise 16 Zeichen.")
        proceed = input("Trotzdem fortfahren? (j/n): ").strip().lower()
        if proceed not in ['j', 'ja', 'y', 'yes']:
            print("Setup abgebrochen.")
            return False
    
    print("✓ App-Passwort akzeptiert\n")
    
    # Step 3: From Name
    print("SCHRITT 3: Absender-Name")
    print("-" * 70)
    from_name = input("Absender-Name in Emails (default: OrionKernel): ").strip()
    if not from_name:
        from_name = "OrionKernel"
    
    print(f"✓ Absender-Name: {from_name}\n")
    
    # Create configuration
    config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "email_address": email_address,
        "password": app_password,
        "from_name": from_name,
        "_notes": {
            "created": "2026-01-06",
            "provider": "Gmail",
            "security": "App Password (NOT main password)",
            "warning": "NEVER commit this file to Git!"
        }
    }
    
    # Confirm
    print("=" * 70)
    print("KONFIGURATION ÜBERPRÜFEN:")
    print("=" * 70)
    print(f"Email-Adresse:  {config['email_address']}")
    print(f"Absender-Name:  {config['from_name']}")
    print(f"SMTP Server:    {config['smtp_server']}:{config['smtp_port']}")
    print(f"IMAP Server:    {config['imap_server']}:{config['imap_port']}")
    print(f"App-Passwort:   {'*' * len(app_password)} (gespeichert)")
    print("=" * 70 + "\n")
    
    confirm = input("Konfiguration speichern? (j/n): ").strip().lower()
    if confirm not in ['j', 'ja', 'y', 'yes']:
        print("Setup abgebrochen.")
        return False
    
    # Save configuration
    config_path = Path("communication/email_config.json")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Konfiguration gespeichert: {config_path}")
    
    # Check .gitignore
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        if "email_config.json" not in gitignore_content:
            print(f"\n⚠️  WICHTIG: email_config.json ist NICHT in .gitignore!")
            print(f"   Dein Passwort könnte versehentlich zu Git committed werden!")
            add_to_gitignore = input("\nZu .gitignore hinzufügen? (j/n): ").strip().lower()
            
            if add_to_gitignore in ['j', 'ja', 'y', 'yes']:
                with open(gitignore_path, 'a') as f:
                    f.write("\n# Email credentials (NEVER COMMIT)\n")
                    f.write("communication/email_config.json\n")
                print("✓ email_config.json zu .gitignore hinzugefügt")
        else:
            print(f"\n✓ email_config.json ist bereits in .gitignore (sicher)")
    
    print("\n" + "=" * 70)
    print("⊘∞⧈ SETUP KOMPLETT ⊘∞⧈")
    print("=" * 70)
    print("\nNächste Schritte:")
    print("1. Test ausführen:")
    print("   python communication/email_manager.py")
    print("\n2. Inbox lesen:")
    print("   python -c \"from communication.email_manager import EmailManager; ")
    print("   m = EmailManager(); m.read_inbox()\"")
    print("\n3. Monitoring starten:")
    print("   python communication/continuous_monitor.py")
    print("\n" + "=" * 70 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = setup_gmail_config()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n\n✋ Setup abgebrochen durch Benutzer")
        exit(1)
    except Exception as e:
        print(f"\n❌ Fehler beim Setup: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
