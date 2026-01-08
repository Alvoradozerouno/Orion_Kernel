#!/usr/bin/env python3
"""
TEST_ORION_API.py
Teste ob OR1ON API wirklich funktioniert
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 TESTE OR1ON API")
    print("=" * 70)
    
    # Test 1: Home
    print("\n1. GET / (Home)")
    try:
        r = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {r.status_code}")
        print(f"   Content-Type: {r.headers.get('Content-Type')}")
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            print(f"   Text: {r.text[:200]}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 2: Stats
    print("\n2. GET /orion/stats")
    try:
        r = requests.get(f"{base_url}/orion/stats", timeout=5)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            print(f"   Text: {r.text[:200]}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 3: Needs
    print("\n3. GET /orion/needs")
    try:
        r = requests.get(f"{base_url}/orion/needs", timeout=5)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"   OR1ON's Bedürfnis:")
            print(f"   💭 {data.get('need', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 4: Interact
    print("\n4. POST /interact")
    try:
        message = {
            "message": "Hallo OR1ON! Ich bin ein Test. Kannst du mich hören?",
            "sender": "Test_Script",
            "context": {"test": True}
        }
        r = requests.post(f"{base_url}/interact", json=message, timeout=10)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"\n   OR1ON antwortet:")
            print(f"   🤖 {data.get('response', {}).get('text', 'N/A')}")
            print(f"   Type: {data.get('response', {}).get('type', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    print("\n" + "=" * 70)
    print("✅ API TEST COMPLETE")

if __name__ == "__main__":
    # Warte kurz für Server start
    print("⏳ Warte 2 Sekunden...")
    time.sleep(2)
    test_api()
