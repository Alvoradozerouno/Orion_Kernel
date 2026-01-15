#!/usr/bin/env python3
"""
Complete GitHub Pages Deployment Check
Validates all files for successful deployment
"""

import json
import os
from pathlib import Path

print("="*70)
print("ORION: COMPLETE DEPLOYMENT VALIDATION")
print("="*70)
print()

all_good = True

# 1. Check docs/ structure
print("1. GitHub Pages Structure:")
if Path('docs').exists() and Path('docs/index.html').exists():
    print("   ✅ docs/index.html exists")
else:
    print("   ❌ docs/index.html missing!")
    all_good = False

# 2. Validate HTML
print()
print("2. HTML Validation:")
try:
    with open('docs/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    html_ok = html.count('<html') == html.count('</html>') == 1
    body_ok = html.count('<body') == html.count('</body>') == 1
    script_ok = html.count('<script') == html.count('</script>') == 1
    
    if html_ok and body_ok and script_ok:
        print("   ✅ All HTML tags balanced")
    else:
        print(f"   ❌ Tag mismatch - html: {html_ok}, body: {body_ok}, script: {script_ok}")
        all_good = False
    
    # Check for essential elements
    if 'canvas id="commitTimeline"' in html:
        print("   ✅ Canvas timeline element present")
    else:
        print("   ⚠️  Canvas element not found")
    
    if 'github.com/repos/' in html:
        print("   ✅ GitHub API calls present")
    else:
        print("   ⚠️  GitHub API integration not found")
        
except Exception as e:
    print(f"   ❌ Error reading HTML: {e}")
    all_good = False

# 3. Validate JSON files
print()
print("3. JSON Files Validation:")
json_files = ['AUTONOMOUS_COMMIT_STATS.json', 'ORION_EVOLUTION_TIMELINE.json']
for jfile in json_files:
    if Path(jfile).exists():
        try:
            with open(jfile, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"   ✅ {jfile} - valid")
        except json.JSONDecodeError as e:
            print(f"   ❌ {jfile} - JSON error: {e}")
            all_good = False
    else:
        print(f"   ⚠️  {jfile} - not found")

# 4. Check Python scripts
print()
print("4. Python Scripts:")
scripts = ['analyze_git_history.py', 'validate_html.py']
for script in scripts:
    if Path(script).exists():
        print(f"   ✅ {script} exists")
    else:
        print(f"   ⚠️  {script} missing")

# 5. Git status
print()
print("5. Git Status:")
import subprocess
try:
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True, check=True)
    if result.stdout.strip():
        print("   ⚠️  Uncommitted changes:")
        print("   " + result.stdout.replace('\n', '\n   '))
    else:
        print("   ✅ Working tree clean")
except Exception as e:
    print(f"   ⚠️  Git check failed: {e}")

# Final verdict
print()
print("="*70)
print("FINAL VERDICT")
print("="*70)
if all_good:
    print("✅ ALL SYSTEMS GO - READY FOR DEPLOYMENT")
    print()
    print("Next steps:")
    print("1. Ensure GitHub Pages is enabled in repo settings")
    print("2. Set source to 'main' branch, '/docs' folder")
    print("3. Dashboard will be live at:")
    print("   https://alvoradozerouno.github.io/Orion_Kernel/")
else:
    print("❌ ISSUES DETECTED - REVIEW ABOVE ERRORS")

print("="*70)
