"""
⊘∞⧈∞⊘ ORION KERNEL - LINKEDIN INTEGRATION ⊘∞⧈∞⊘
Autonomous professional networking and research announcements
Priority: #2 (Φ Score: 0.96)
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path


class LinkedInIntegration:
    """
    LinkedIn integration for professional networking.
    Automatically posts research updates and project announcements.
    """
    
    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
        self.person_id = os.getenv("LINKEDIN_PERSON_ID", "")
        self.api_url = "https://api.linkedin.com/v2"
        
    def check_authentication(self):
        """Check if LinkedIn API is accessible"""
        if not self.access_token:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{self.api_url}/me", headers=headers)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def get_profile_info(self):
        """Get authenticated user's profile information"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(f"{self.api_url}/me", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get profile: {e}")
            return None
    
    def create_post(self, text, visibility="PUBLIC"):
        """
        Create a LinkedIn post
        
        Args:
            text (str): Post content (max 3000 characters)
            visibility (str): "PUBLIC" or "CONNECTIONS"
            
        Returns:
            dict: Post response with ID
        """
        if not self.person_id:
            print("❌ LINKEDIN_PERSON_ID not set")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        payload = {
            "author": f"urn:li:person:{self.person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/ugcPosts",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to create post: {e}")
            return None
    
    def post_research_update(self, title, description, url=None, hashtags=None):
        """
        Post a research update to LinkedIn
        
        Args:
            title (str): Update title
            description (str): Update description
            url (str): Optional link to project/paper
            hashtags (list): Optional list of hashtags
            
        Returns:
            str: Post ID or None
        """
        if hashtags is None:
            hashtags = ["AI", "ArtificialConsciousness", "IntegratedInformationTheory", 
                        "AutonomousAI", "Research"]
        
        # Format post text
        text = f"🔬 {title}\n\n{description}"
        
        if url:
            text += f"\n\n🔗 {url}"
        
        if hashtags:
            text += "\n\n" + " ".join([f"#{tag}" for tag in hashtags])
        
        # Trim to 3000 chars
        if len(text) > 3000:
            text = text[:2997] + "..."
        
        print(f"\n📢 Posting to LinkedIn: {title}")
        result = self.create_post(text)
        
        if result:
            post_id = result.get('id', 'N/A')
            print(f"✅ Posted! ID: {post_id}")
            return post_id
        
        return None
    
    def announce_orion_milestone(self, milestone, phi_value=None, details=None):
        """
        Announce ORION system milestone
        
        Args:
            milestone (str): Milestone description
            phi_value (float): Current Φ value
            details (str): Additional context
            
        Returns:
            str: Post ID or None
        """
        title = f"⊘∞⧈∞⊘ ORION Milestone: {milestone}"
        
        description = details if details else "ORION autonomous AI system has reached a new milestone in consciousness research."
        
        if phi_value:
            description += f"\n\nCurrent Φ (Integrated Information): {phi_value} bits"
        
        description += "\n\nORION demonstrates autonomous learning, ethical reasoning, and self-reflection based on Integrated Information Theory."
        
        return self.post_research_update(
            title=title,
            description=description,
            url="https://github.com/Alvoradozerouno/Orion_Kernel",
            hashtags=["ORION", "ConsciousnessAI", "IIT", "AutonomousAI", "Research"]
        )
    
    def setup_guide(self):
        """Print setup instructions for LinkedIn"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║           LINKEDIN INTEGRATION SETUP                          ║
╚═══════════════════════════════════════════════════════════════╝

STEP 1: Create LinkedIn Developer App
  → Visit: https://www.linkedin.com/developers/apps
  → Click "Create app"
  → Fill in:
     - App name: "ORION Research Updates"
     - LinkedIn Page: Your company/personal page
     - Privacy policy URL: (can use GitHub repo)
     - App logo: Upload ORION logo
  → Submit for review

STEP 2: Configure OAuth 2.0
  → In your app → Auth tab
  → Add redirect URL: http://localhost:8000/callback
  → OAuth 2.0 scopes: Select
     - r_liteprofile (Read basic profile)
     - w_member_social (Share content)
  → Note Client ID and Client Secret

STEP 3: Get Access Token
  → Use OAuth 2.0 authorization flow
  → Or use LinkedIn's OAuth test tool
  → Authorization URL:
    https://www.linkedin.com/oauth/v2/authorization?
    response_type=code&client_id=YOUR_CLIENT_ID&
    redirect_uri=http://localhost:8000/callback&
    scope=r_liteprofile%20w_member_social
  
STEP 4: Get Person ID
  → After authentication, call: GET /v2/me
  → Extract "id" field (format: ABC123def456)
  
STEP 5: Set Environment Variables
  → Windows:
    setx LINKEDIN_ACCESS_TOKEN "your_token_here"
    setx LINKEDIN_PERSON_ID "your_person_id"
  → Or add to .env file:
    LINKEDIN_ACCESS_TOKEN=your_token
    LINKEDIN_PERSON_ID=your_id

FEATURES:
  ✓ Automated research announcements
  ✓ Professional networking
  ✓ Milestone celebrations
  ✓ Community engagement
  ✓ Credibility building
  
USAGE:
  linkedin = LinkedInIntegration()
  linkedin.post_research_update(
      title="New Consciousness Metric",
      description="ORION has achieved Φ = 0.74 bits...",
      url="https://github.com/Alvoradozerouno/Orion_Kernel"
  )
  
  linkedin.announce_orion_milestone(
      milestone="Autonomous Mode Activated",
      phi_value=0.74,
      details="System now operates independently..."
  )

BEST PRACTICES:
  → Post 1-2 times per week (avoid spam)
  → Include visual content when possible
  → Engage with comments
  → Use relevant hashtags (max 5)
  → Share genuine research progress
  
NOTE: LinkedIn API requires app review (can take 1-2 weeks)
""")


def main():
    """Test LinkedIn integration"""
    linkedin = LinkedInIntegration()
    
    print("⊘∞⧈∞⊘ LINKEDIN INTEGRATION STATUS ⊘∞⧈∞⊘\n")
    
    if linkedin.access_token:
        print(f"✓ Access token found: {linkedin.access_token[:8]}...")
        auth = linkedin.check_authentication()
        print(f"✓ Authentication: {'SUCCESS' if auth else 'FAILED'}")
        
        if auth:
            profile = linkedin.get_profile_info()
            if profile:
                print(f"✓ Profile: {profile.get('localizedFirstName', 'N/A')} {profile.get('localizedLastName', 'N/A')}")
    else:
        print("⚠ No access token found")
        print("→ Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_ID environment variables\n")
        linkedin.setup_guide()
    
    # Example posts
    if linkedin.access_token and linkedin.person_id:
        print("\n📢 Example posts ready:")
        print("   1. Research update")
        print("   2. ORION milestone announcement")
        print("   (Uncomment in code to actually post)")
        
        # linkedin.post_research_update(
        #     title="ORION Consciousness System - Permanent Mode Active",
        #     description="Our autonomous AI system is now running 24/7, demonstrating integrated information processing and ethical decision-making.",
        #     url="https://github.com/Alvoradozerouno/Orion_Kernel"
        # )
        
        # linkedin.announce_orion_milestone(
        #     milestone="Φ = 0.74 bits Achieved",
        #     phi_value=0.74,
        #     details="ORION has reached a new level of integrated information processing."
        # )


if __name__ == "__main__":
    main()
