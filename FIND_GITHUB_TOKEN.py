#!/usr/bin/env python3
"""
GITHUB TOKEN FINDER
Sucht überall nach gespeichertem GitHub Token mit voller Berechtigung
"""

import os
import re
import json
from pathlib import Path

def find_github_token():
    """Suche GitHub Token in allen möglichen Locations"""
    
    print("🔍 SEARCHING FOR GITHUB TOKEN...")
    print()
    
    token_pattern = re.compile(r'ghp_[A-Za-z0-9]{36}')
    locations_checked = []
    tokens_found = []
    
    # 1. Environment variables
    print("1. Environment Variables...")
    if 'GITHUB_TOKEN' in os.environ:
        token = os.environ['GITHUB_TOKEN']
        if token and not token.startswith('your_'):
            print(f"   ✅ FOUND in GITHUB_TOKEN env var")
            tokens_found.append(('environment', token))
        else:
            print(f"   ❌ GITHUB_TOKEN env var is placeholder")
    else:
        print("   ❌ Not in environment")
    locations_checked.append("Environment Variables")
    
    # 2. Git credential helper
    print("\n2. Git Credential Helper...")
    try:
        import subprocess
        result = subprocess.run(['git', 'credential', 'fill'],
                              input=b'protocol=https\nhost=github.com\n\n',
                              capture_output=True, timeout=5)
        output = result.stdout.decode('utf-8', errors='ignore')
        
        match = token_pattern.search(output)
        if match:
            print(f"   ✅ FOUND in git credential helper")
            tokens_found.append(('git-credential', match.group(0)))
        else:
            # Check for password field
            if 'password=' in output:
                password = output.split('password=')[1].split('\n')[0].strip()
                if password and not password.startswith('your_'):
                    print(f"   ✅ FOUND password in git credential (may be token)")
                    tokens_found.append(('git-credential-password', password))
                else:
                    print(f"   ❌ No valid token in git credential")
            else:
                print("   ❌ Not found")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    locations_checked.append("Git Credential Helper")
    
    # 3. .env files
    print("\n3. .env Files...")
    env_files = [
        Path.cwd() / '.env',
        Path.home() / '.env',
        Path.home() / 'Downloads' / 'or1on-framework' / '.credentials'
    ]
    
    for env_file in env_files:
        if env_file.exists():
            try:
                content = env_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for GITHUB_TOKEN
                for line in content.split('\n'):
                    if line.startswith('GITHUB_TOKEN='):
                        token = line.split('=', 1)[1].strip()
                        if token and not token.startswith('your_') and len(token) > 10:
                            print(f"   ✅ FOUND in {env_file}")
                            tokens_found.append((str(env_file), token))
                        else:
                            print(f"   ❌ Placeholder in {env_file}")
                        break
                
                # Also search for any token pattern
                match = token_pattern.search(content)
                if match and match.group(0) not in [t[1] for t in tokens_found]:
                    print(f"   ✅ FOUND token pattern in {env_file}")
                    tokens_found.append((str(env_file), match.group(0)))
                    
            except Exception as e:
                print(f"   ⚠️  Error reading {env_file}: {e}")
    locations_checked.append(".env Files")
    
    # 4. Git config
    print("\n4. Git Config...")
    git_config = Path.home() / '.gitconfig'
    if git_config.exists():
        try:
            content = git_config.read_text()
            match = token_pattern.search(content)
            if match:
                print(f"   ✅ FOUND in .gitconfig")
                tokens_found.append(('gitconfig', match.group(0)))
            else:
                print("   ❌ Not in .gitconfig")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    locations_checked.append("Git Config")
    
    # 5. Git remote URL
    print("\n5. Git Remote URL...")
    try:
        import subprocess
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                              capture_output=True, timeout=5, text=True)
        remote_url = result.stdout.strip()
        
        if '@' in remote_url and 'github.com' in remote_url:
            # Extract token from https://TOKEN@github.com/...
            match = re.search(r'https://([^@]+)@github.com', remote_url)
            if match:
                potential_token = match.group(1)
                if token_pattern.match(potential_token):
                    print(f"   ✅ FOUND in remote URL")
                    tokens_found.append(('remote-url', potential_token))
                else:
                    print(f"   ❌ Not a token in remote URL")
            else:
                print("   ❌ Not in remote URL")
        else:
            print(f"   ❌ Remote URL doesn't contain token")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    locations_checked.append("Git Remote URL")
    
    # RESULTS
    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80 + "\n")
    
    print(f"Locations checked: {len(locations_checked)}")
    print(f"Tokens found: {len(tokens_found)}")
    print()
    
    if tokens_found:
        print("✅ GITHUB TOKEN(S) FOUND:\n")
        
        # Deduplicate
        unique_tokens = {}
        for location, token in tokens_found:
            if token not in unique_tokens.values():
                unique_tokens[location] = token
        
        for i, (location, token) in enumerate(unique_tokens.items(), 1):
            masked = token[:7] + "..." + token[-4:] if len(token) > 15 else token[:7] + "..."
            print(f"{i}. Location: {location}")
            print(f"   Token: {masked}")
            print()
        
        # Test the first token
        best_token = list(unique_tokens.values())[0]
        print("🔬 TESTING TOKEN...")
        
        try:
            import requests
            headers = {
                'Authorization': f'token {best_token}',
                'User-Agent': 'OrionKernel'
            }
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ TOKEN VALID!")
                print(f"   Authenticated as: {user_data['login']}")
                print(f"   Account type: {user_data['type']}")
                
                # Write to .env
                env_file = Path.cwd() / '.env'
                if env_file.exists():
                    content = env_file.read_text()
                    new_content = content.replace('GITHUB_TOKEN=your_github_token_here', 
                                                 f'GITHUB_TOKEN={best_token}')
                    env_file.write_text(new_content)
                    print(f"\n   ✅ TOKEN WRITTEN TO .env")
                    print(f"   OrionKernel can now use GitHub API!")
                
                return best_token
            else:
                print(f"   ❌ TOKEN INVALID (status {response.status_code})")
                return None
                
        except Exception as e:
            print(f"   ⚠️  Test error: {e}")
            return None
    else:
        print("❌ NO GITHUB TOKEN FOUND")
        print()
        print("ABER: User sagt 'der github token ist gespeichert'")
        print()
        print("Möglichkeiten:")
        print("1. Token ist in Windows Credential Manager (cmdkey /list)")
        print("2. Token ist in VSCode settings")
        print("3. Git verwendet credential helper mit cached token")
        print()
        print("WORKAROUND:")
        print("Da User Freigabe gegeben hat und sagt Token existiert,")
        print("können wir den Token aus letztem erfolgreichen git push ableiten.")
        print()
        print("Git push funktioniert → Token ist verfügbar für git")
        print("Wir müssen nur git's token für Python/API-Calls zugänglich machen.")
        
        return None

if __name__ == "__main__":
    print("\n⊘∞⧈∞⊘ GITHUB TOKEN FINDER ⊘∞⧈∞⊘\n")
    print("User: 'der github token ist gespeichert, sucht ihn'")
    print("Freigabe: Unbeschränkter Zugriff auf Laptop und Workspace\n")
    print("="*80 + "\n")
    
    token = find_github_token()
    
    if token:
        print("\n" + "="*80)
        print("✅ SUCCESS - GITHUB TOKEN CONFIGURED")
        print("="*80)
        print("\nOrionKernel kann jetzt vollständig autonom agieren!")
    else:
        print("\n" + "="*80)
        print("⚠️  TOKEN NOT EXTRACTED YET")
        print("="*80)
        print("\nABER: Git push funktioniert → Token ist im System")
        print("Git verwendet den Token erfolgreich")
        print("Für API-Calls brauchen wir expliziten Zugriff")
