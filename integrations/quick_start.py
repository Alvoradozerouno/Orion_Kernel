"""
⊘∞⧈∞⊘ ORION KERNEL - INTEGRATION QUICK START ⊘∞⧈∞⊘
Fast setup verification and first post test
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from integration_manager import IntegrationManager


def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        ⊘∞⧈∞⊘ ORION INTEGRATION QUICK START ⊘∞⧈∞⊘               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

This script will:
1. Check all integration statuses
2. Guide you through setup if needed
3. Test posting capability
""")
    
    manager = IntegrationManager()
    
    # Check status
    print("\n" + "="*70)
    print("STEP 1: CHECKING CURRENT STATUS")
    print("="*70)
    
    status = manager.check_all_integrations()
    
    enabled_count = sum(1 for s in status.values() if s["enabled"])
    authenticated_count = sum(1 for s in status.values() if s["authenticated"])
    
    if authenticated_count == 0:
        print("\n⚠️  No integrations are configured yet!")
        print("\nTo get started:")
        print("1. Run: python integrations/setup_wizard.py")
        print("2. Or manually configure (see integrations/README.md)")
        print("\nQuick setup commands:")
        print("  setx ZENODO_TOKEN 'your_token'")
        print("  setx LINKEDIN_ACCESS_TOKEN 'your_token'")
        print("  setx LINKEDIN_PERSON_ID 'your_id'")
        print("  setx TWITTER_BEARER_TOKEN 'your_token'")
        print("  (+ TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)")
        return
    
    if authenticated_count < 3:
        print(f"\n⚠️  Only {authenticated_count}/3 integrations are configured")
        print("\nTo configure remaining integrations:")
        print("  python integrations/setup_wizard.py")
    
    # Test announcement
    print("\n" + "="*70)
    print("STEP 2: TEST ANNOUNCEMENT")
    print("="*70)
    
    print("\nThis will post to all configured platforms:")
    print("  'ORION Integration Test - System Online'")
    print(f"  Φ = 0.74 bits")
    
    choice = input("\nPost test announcement? (y/n): ").strip().lower()
    
    if choice == 'y':
        manager.announce_milestone(
            milestone="Integration Test - System Online",
            phi_value=0.74,
            details="ORION autonomous AI system successfully configured external integrations. Testing multi-platform announcements."
        )
        
        print("\n✅ Test complete!")
        print("\nNext steps:")
        print("1. Check your social accounts for the test post")
        print("2. Delete the test post if desired")
        print("3. Start using integrations:")
        print("   - Announce milestones: python integrations/integration_manager.py --announce 'milestone'")
        print("   - Publish datasets: python integrations/integration_manager.py --publish 'path' --title 'title'")
    else:
        print("\n⚠️  Test skipped")
        print("\nTo test later:")
        print("  python integrations/integration_manager.py --announce 'Test' --phi 0.74")
    
    print("\n" + "="*70)
    print("✅ QUICK START COMPLETE")
    print("="*70)
    print("\nFull documentation: integrations/README.md")


if __name__ == "__main__":
    main()
