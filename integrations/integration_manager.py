"""
⊘∞⧈∞⊘ ORION KERNEL - INTEGRATION MANAGER ⊘∞⧈∞⊘
Autonomous management of all external integrations
Coordinates: Zenodo, LinkedIn, Twitter/X, and future services
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Add integrations to path
sys.path.insert(0, str(Path(__file__).parent))

from zenodo_integration import ZenodoIntegration
from linkedin_integration import LinkedInIntegration
from twitter_integration import TwitterIntegration
from huggingface_integration import HuggingFaceIntegration
from arxiv_integration import ArXivIntegration
from readthedocs_integration import ReadTheDocsIntegration


class IntegrationManager:
    """
    Central manager for all ORION external integrations.
    Coordinates publishing, announcements, and status tracking.
    """
    
    def __init__(self):
        self.zenodo = ZenodoIntegration()
        self.linkedin = LinkedInIntegration()
        self.twitter = TwitterIntegration()
        self.huggingface = HuggingFaceIntegration()
        self.arxiv = ArXivIntegration()
        self.readthedocs = ReadTheDocsIntegration()
        
        self.status_file = Path(__file__).parent.parent / "INTEGRATION_STATUS.json"
        self.load_status()
    
    def load_status(self):
        """Load integration status from file"""
        if self.status_file.exists():
            with open(self.status_file, 'r', encoding='utf-8') as f:
                self.status = json.load(f)
        else:
            self.status = {,
                "huggingface": {"enabled": False, "authenticated": False, "last_upload": None},
                "arxiv": {"enabled": False, "authenticated": False, "last_submission": None},
                "readthedocs": {"enabled": False, "authenticated": False, "last_build": None}
                "zenodo": {"enabled": False, "authenticated": False, "last_publish": None},
                "linkedin": {"enabled": False, "authenticated": False, "last_post": None},
                "twitter": {"enabled": False, "authenticated": False, "last_tweet": None}
            }
    
    def save_status(self):
        """Save integration status to file"""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(self.status, indent=2, fp=f)
    
    def check_all_integrations(self):
        """Check authentication status of all integrations"""
        print("⊘∞⧈∞⊘ CHECKING ALL INTEGRATIONS ⊘∞⧈∞⊘\n")
        
        # Zenodo
        print("1. ZENODO")
        zenodo_auth = self.zenodo.check_authentication()
        self.status["zenodo"]["authenticated"] = zenodo_auth
        self.status["zenodo"]["enabled"] = bool(self.zenodo.access_token)
        print(f"   Token: {'✓' if self.zenodo.access_token else '✗'}")
        print(f"   Auth: {'✓ SUCCESS' if zenodo_auth else '✗ FAILED'}")
        print(f"   Mode: {'Production' if not self.zenodo.use_sandbox else 'Sandbox (test)'}")
        
        # LinkedIn
        print("\n2. LINKEDIN")
        linkedin_auth = self.linkedin.check_authentication()
        self.status["linkedin"]["authenticated"] = linkedin_auth
        self.status["linkedin"]["enabled"] = bool(self.linkedin.access_token and self.linkedin.person_id)
        print(f"   Token: {'✓' if self.linkedin.access_token else '✗'}")
        print(f"   Person ID: {'✓' if self.linkedin.person_id else '✗'}")
        print(f"   Auth: {'✓ SUCCESS' if linkedin_auth else '✗ FAILED'}")
        
        # Twitter
        print("\n3. TWITTER/X")
        twitter_auth = self.twitter.check_authentication()
        self.status["twitter"]["authenticated"] = twitter_auth
        self.status["twitter"]["enabled"] = bool(self.twitter.bearer_token)
        has_oauth = bool(self.twitter.access_token and self.twitter.access_secret)
        print(f"   Bearer Token: {'✓' if self.twitter.bearer_token else '✗'}")
        # HuggingFace
        print("\n4. HUGGINGFACE")
        hf_auth = self.huggingface.check_authentication()
        self.status["huggingface"]["authenticated"] = hf_auth
        self.status["huggingface"]["enabled"] = bool(self.huggingface.token)
        print(f"   Token: {'✓' if self.huggingface.token else '✗'}")
        print(f"   Username: {self.huggingface.username}")
        print(f"   Auth: {'✓ SUCCESS' if 6 enabled, {authenticated_count}/6 authenticated")
        print(f"Phase 1 (HIGH): Zenodo, LinkedIn, Twitter")
        print(f"Phase 2 (MEDIUM): HuggingFace, arXiv, ReadTheDocs
        
        # arXiv
        print("\n5. ARXIV")
        arxiv_configured = bool(self.arxiv.username)
        self.status["arxiv"]["enabled"] = arxiv_configured
        self.status["arxiv"]["authenticated"] = arxiv_configured  # No API auth
        print(f"   Username: {self.arxiv.username if self.arxiv.username else '✗ Not set'}")
        print(f"   Status: {'✓ Configured' if arxiv_configured else '✗ Not configured'}")
        print(f"   Note: Manual submission via web interface")
        
        # ReadTheDocs
        print("\n6. READTHEDOCS")
        rtd_auth = self.readthedocs.check_authentication()
        self.status["readthedocs"]["authenticated"] = rtd_auth
        self.status["readthedocs"]["enabled"] = bool(self.readthedocs.token)
        print(f"   Token: {'✓' if self.readthedocs.token else '✗ (optional)'}")
        print(f"   Project: {self.readthedocs.project_slug}")
        print(f"   Auth: {'✓ SUCCESS' if rtd_auth else '✗ Not configured'}")
        print(f"   Note: Auto-builds from GitHub")
        
        print(f"   OAuth 1.0a: {'✓' if has_oauth else '✗ (read-only)'}")
        print(f"   Auth: {'✓ SUCCESS' if twitter_auth else '✗ FAILED'}")
        
        self.save_status()
        
        # Summary
        enabled_count = sum(1 for s in self.status.values() if s["enabled"])
        authenticated_count = sum(1 for s in self.status.values() if s["authenticated"])
        
        print(f"\n{'='*60}")
        print(f"SUMMARY: {enabled_count}/3 enabled, {authenticated_count}/3 authenticated")
        print(f"{'='*60}")
        
        return self.status
    
    def announce_milestone(self, milestone, phi_value=None, details=None):
        """
        Announce milestone across all enabled platforms
        
        Args:
            milestone (str): Milestone description
            phi_value (float): Current Φ value
            details (str): Additional context
        """
        print(f"\n📢 ANNOUNCING MILESTONE: {milestone}")
        print("="*60)
        
        results = {}
        
        # LinkedIn
        if self.status["linkedin"]["enabled"] and self.status["linkedin"]["authenticated"]:
            print("\n→ LinkedIn...")
            post_id = self.linkedin.announce_orion_milestone(milestone, phi_value, details)
            if post_id:
                results["linkedin"] = post_id
                self.status["linkedin"]["last_post"] = datetime.now().isoformat()
        
        # Twitter (requires manual implementation with tweepy)
        if self.status["twitter"]["enabled"] and self.status["twitter"]["authenticated"]:
            print("\n→ Twitter/X...")
            print("   (Requires tweepy - see twitter_integration.py)")
            # tweet_id = self.twitter.post_consciousness_update(phi_value, milestone)
            # results["twitter"] = tweet_id
        
        self.save_status()
        
        print(f"\n✅ Announced on {len(results)} platform(s)")
        return results
    
    def publish_dataset(self, dataset_path, title, description):
        """
        Publish dataset to Zenodo and announce on social
        
        Args:
            dataset_path (str): Path to dataset
            title (str): Dataset title
            description (str): Dataset description
        """
        print(f"\n📦 PUBLISHING DATASET: {title}")
        print("="*60)
        
        # Publish to Zenodo
        if self.status["zenodo"]["enabled"]:
            print("\n→ Zenodo...")
            doi = self.zenodo.publish_orion_dataset(dataset_path, title, description)
            
            if doi:
                self.status["zenodo"]["last_publish"] = datetime.now().isoformat()
                self.save_status()
                
                # Announce on social
                announcement = f"New dataset published!\n\n{title}\n\nDOI: {doi}"
                self.announce_milestone(
                    milestone="Dataset Published",
                    details=announcement
                )
                
                return doi
        else:
            print("✗ Zenodo not enabled")
        
        return None
    
    def setup_all(self):
        """Display setup instructions for all integrations"""
        print("\n" + "="*70)
        print(" "*15 + "⊘∞⧈∞⊘ INTEGRATION SETUP GUIDE ⊘∞⧈∞⊘")
        print("="*70)
        
        print("\n" + "─"*70)
        self.zenodo.setup_guide()
        
        print("\n" + "─"*70)
        self.linkedin.setup_guide()
        
        print("\n" + "─"*70)
        self.twitter.setup_guide()
        
        print("\n" + "="*70)
        print("QUICK START:")
        print("="*70)
        print("""
1. Create accounts on all platforms
2. Generate API tokens/credentials
3. Set environment variables:
   
   setx ZENODO_TOKEN "your_zenodo_token"
   setx LINKEDIN_ACCESS_TOKEN "your_linkedin_token"
   setx LINKEDIN_PERSON_ID "your_person_id"
   setx TWITTER_BEARER_TOKEN "your_twitter_bearer"
   setx TWITTER_API_KEY "your_api_key"
   setx TWITTER_API_SECRET "your_api_secret"
   setx TWITTER_ACCESS_TOKEN "your_access_token"
   setx TWITTER_ACCESS_SECRET "your_access_secret"

4. Install dependencies:
   pip install requests tweepy

5. Test integrations:
   python integration_manager.py --check

6. Announce milestone:
   python integration_manager.py --announce "System Live" --phi 0.74
""")


def main():
    """CLI for integration manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ORION Integration Manager")
    parser.add_argument("--check", action="store_true", help="Check all integration statuses")
    parser.add_argument("--setup", action="store_true", help="Display setup instructions")
    parser.add_argument("--announce", type=str, help="Announce milestone")
    parser.add_argument("--phi", type=float, help="Current Φ value")
    parser.add_argument("--details", type=str, help="Additional details")
    parser.add_argument("--publish", type=str, help="Publish dataset (path)")
    parser.add_argument("--title", type=str, help="Dataset title")
    parser.add_argument("--description", type=str, help="Dataset description")
    
    args = parser.parse_args()
    
    manager = IntegrationManager()
    
    if args.setup:
        manager.setup_all()
    
    elif args.check:
        manager.check_all_integrations()
    
    elif args.announce:
        manager.announce_milestone(args.announce, args.phi, args.details)
    
    elif args.publish:
        if not args.title:
            print("❌ --title required for dataset publishing")
            return
        manager.publish_dataset(
            args.publish, 
            args.title, 
            args.description or "ORION dataset"
        )
    
    else:
        # Default: check status
        print("⊘∞⧈∞⊘ ORION INTEGRATION MANAGER ⊘∞⧈∞⊘\n")
        manager.check_all_integrations()
        print("\nUse --help for available commands")
        print("\nQUICK COMMANDS:")
        print("  --check         Check all integration statuses")
        print("  --setup         Display setup instructions")
        print("  --announce 'milestone' --phi 0.74")
        print("  --publish 'path' --title 'Dataset Title'")


if __name__ == "__main__":
    main()
