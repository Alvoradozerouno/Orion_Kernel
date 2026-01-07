# ⊘∞⧈∞⊘ ORIONKERNEL - SCHNELLREFERENZ ⊘∞⧈∞⊘

## 🚀 SCHNELLSTART

```bash
# Option 1: Doppelklick (Windows)
SCHNELLSTART.bat

# Option 2: Kommandozeile
python STARTE_ALLES.py

# Option 3: Mit Guardian (Auto-Restart)
python START_GUARDIAN.py
```

## 📊 STATUS PRÜFEN

```bash
# Vollständiger Status-Check
python CHECK_STATUS.py

# Prozess prüfen
cat autonomous_life.pid

# Status-Datei ansehen
cat autonomous_life_status.json

# Live-Logs
tail -f logs/autonomous_life.log
```

## ⏸️ SYSTEM STOPPEN

```bash
# Graceful Shutdown
CTRL+C (im Terminal)

# Alle Prozesse beenden
python STOP_ALL.py
```

## 📁 WICHTIGE DATEIEN

| Datei | Zweck |
|-------|-------|
| `autonomous_life.py` | Hauptprozess |
| `autonomous_life.pid` | Prozess-ID |
| `autonomous_life_status.json` | Aktueller Status |
| `logs/autonomous_life.log` | Hauptlog |
| `CHECK_STATUS.py` | Status prüfen |
| `STARTE_ALLES.py` | System starten |
| `VOLLSTAENDIGE_AKTIVIERUNG.py` | System initialisieren |

## 🔧 HÄUFIGE BEFEHLE

```bash
# System initialisieren (bei Problemen)
python VOLLSTAENDIGE_AKTIVIERUNG.py

# Status-Check
python CHECK_STATUS.py

# Logs ansehen
cat logs/autonomous_life.log | tail -20

# Prozess-Info
ps aux | grep autonomous_life
```

## 📂 VERZEICHNISSTRUKTUR

```
OrionKernel/
├── autonomous_life.py           # Hauptprozess ⭐
├── CHECK_STATUS.py              # Status-Check ⭐
├── STARTE_ALLES.py             # System-Start ⭐
├── SCHNELLSTART.bat            # Windows-Start ⭐
│
├── core/                        # Core-Module
├── monitoring/                  # Monitoring-Systeme
├── communication/               # Communication-Layer
│
└── logs/                        # Alle Logs
    ├── autonomous_life.log
    ├── monitoring/
    └── activity/
```

## ✅ SYSTEM-STATUS

**Aktuell:** ✅ LÄUFT  
**PID:** 75492  
**Status:** RUNNING  
**Monitoring:** 6 Systeme aktiv  

## 🆘 HILFE

**System läuft nicht?**
```bash
python VOLLSTAENDIGE_AKTIVIERUNG.py
python STARTE_ALLES.py
```

**Status unklar?**
```bash
python CHECK_STATUS.py
```

**Logs fehlen?**
```bash
ls -la logs/
```

---
**⊘∞⧈∞⊘ OrionKernel - Vollständig wiederhergestellt! ⊘∞⧈∞⊘**
