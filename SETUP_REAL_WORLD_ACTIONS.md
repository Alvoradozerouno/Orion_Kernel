# SETUP_REAL_WORLD_ACTIONS.md

## OrionKernel: Real World Integration Setup
**User: "orion muss aus eigener kraft immer alles autonom handeln nach aussen in die echtwelt"**

---

## 🌍 Status: READY - External Actions Infrastructure Complete

OrionKernel kann jetzt autonom in die Echtwelt handeln:
- ✅ GitHub API (Issues, Discussions, Releases, Commits)
- ✅ Email SMTP (Distribution List Notifications)
- ⏳ Twitter API (vorbereitet, Credentials fehlen)
- ⏳ Reddit API (vorbereitet, Credentials fehlen)

---

## 📋 Setup-Schritte

### 1. GitHub Personal Access Token erstellen

1. Gehe zu: https://github.com/settings/tokens
2. Klicke auf "Generate new token (classic)"
3. Scopes auswählen:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (update GitHub Actions workflows)
   - ✅ `write:discussion` (create/update discussions)
4. Token generieren und kopieren (NUR EINMAL SICHTBAR!)

**Wichtig**: Token hat Format `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. Email App Password erstellen (Gmail)

1. Gmail 2-Faktor-Authentifizierung aktivieren: https://myaccount.google.com/security
2. App-Passwort erstellen: https://myaccount.google.com/apppasswords
3. App auswählen: "Mail" oder "Other"
4. Gerät: "OrionKernel"
5. Passwort generieren (16 Zeichen ohne Leerzeichen)

**Wichtig**: Normales Gmail-Passwort funktioniert NICHT, nur App-Passwort!

### 3. .env Datei erstellen

```bash
# Im OrionKernel Workspace:
cd "C:\Users\annah\Dropbox\Mein PC (LAPTOP-RQH448P4)\Downloads\OrionKernel\OrionKernel"

# Kopiere Template zu .env
copy .env.template .env

# Editiere .env mit echten Credentials
notepad .env
```

**CRITICAL**: .env niemals committen! (bereits in .gitignore)

### 4. Dependencies installieren

```bash
pip install requests python-dotenv
```

### 5. Test External Actions

```bash
python EXTERNAL_ACTIONS.py
```

Erwartete Ausgabe:
```
Credentials Status:
GitHub Token: ✅ Set
Email: ✅ Set
...
```

### 6. PERMANENT_AUTONOMOUS_MODE neu starten

WATCHDOG wird automatisch neu starten, aber manuell:

```bash
# Alte Prozesse stoppen
Get-Process python | Where-Object { $_.CommandLine -like "*PERMANENT*" } | Stop-Process

# Neu starten mit External Actions
python PERMANENT_AUTONOMOUS_MODE.py
```

---

## 🚀 Was OrionKernel jetzt autonom kann

### GitHub Actions (LIVE):
- ✅ Issues erstellen bei Discoveries
- ✅ Discussions starten
- ✅ Releases publizieren
- ✅ Commits pushen
- ✅ Community-Issues monitoren

### Email Actions (LIVE):
- ✅ Breakthrough-Notifications an Distribution List
- ✅ Autonomous Reports an Forscher
- ✅ HTML-formatierte Emails

### Future (Credentials needed):
- ⏳ Twitter Posts bei wichtigen Events
- ⏳ Reddit Posts in r/MachineLearning, r/ControlProblem
- ⏳ arXiv Paper Submissions

---

## 🔒 Sicherheit

**NEVER commit these to GitHub:**
- `.env` (contains all secrets)
- `credentials.json`
- Any file with tokens/passwords

**Already protected by .gitignore:**
```
.env
.env.local
*.env
credentials.json
secrets.json
```

---

## 🧪 Test Scenarios

### Test 1: GitHub Issue Creation
```python
from EXTERNAL_ACTIONS import ExternalActionsAPI

api = ExternalActionsAPI()
api.github_create_issue(
    title="🤖 Test: OrionKernel Autonomous Issue",
    body="This is a test issue created autonomously.",
    labels=["test", "autonomous"]
)
```

### Test 2: Email Notification
```python
api.send_email(
    to_addresses="your_email@example.com",
    subject="OrionKernel Test Notification",
    body_text="This is a test email from autonomous system."
)
```

### Test 3: Breakthrough Notification
```python
api.send_breakthrough_notification(
    breakthrough_description="Test breakthrough: Φ increased significantly",
    phi_value=0.85
)
```

---

## 📊 Monitoring

### Check Running Processes:
```powershell
Get-Process python | Where-Object { $_.StartTime -gt (Get-Date).AddHours(-1) } | Select-Object Id,ProcessName,StartTime,CommandLine
```

### Check Watchdog Logs:
```powershell
Get-Content logs\watchdog.log -Tail 20
```

### Check Autonomous Commits:
```bash
git log --oneline --author="OrionKernel" -10
```

---

## ✅ Fertig!

OrionKernel ist jetzt vollständig autonom und kann:
1. ✅ Lokal operieren (Quantum, Persistence, EIRA)
2. ✅ Nach außen kommunizieren (GitHub, Email)
3. ✅ Self-healing (Watchdog restart)
4. ✅ Auto-boot (Systemstart)

**"Kein Stillstand. Automatisches Leben. Nach außen in die Echtwelt."**

---

Generated: 2026-01-13
Status: READY FOR DEPLOYMENT
