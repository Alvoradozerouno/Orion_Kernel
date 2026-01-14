#!/usr/bin/env python3
"""
ORION EXTERNAL ACTIONS - Real World Integration
================================================
User: "orion muss aus eigener kraft immer alles autonom handeln nach aussen in die echtwelt"

Externe APIs:
- GitHub (Issues, Discussions, Releases, Commits)
- Email (SMTP Distribution)
- X/Twitter (optional, future)
- Reddit (optional, future)
- arXiv (optional, future)

Credentials: .env file oder environment variables
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import subprocess
import sys

try:
    import requests
except ImportError:
    print("⚠️  requests not installed. Run: pip install requests")
    sys.exit(1)

class ExternalActionsAPI:
    def __init__(self):
        self.workspace = Path(__file__).parent
        
        # Load .env file explicitly
        try:
            from dotenv import load_dotenv
            env_path = self.workspace / '.env'
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
        except ImportError:
            pass
        
        self.credentials = self.load_credentials()
        
    def load_credentials(self):
        """Load API credentials from .env or environment variables"""
        creds = {
            "github_token": os.getenv("GITHUB_TOKEN", ""),
            "github_repo": "Alvoradozerouno/Orion_Kernel",
            "email_smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "email_smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "email_address": os.getenv("EMAIL_ADDRESS", ""),
            "email_password": os.getenv("EMAIL_PASSWORD", ""),
            "twitter_api_key": os.getenv("TWITTER_API_KEY", ""),  # Future
            "reddit_client_id": os.getenv("REDDIT_CLIENT_ID", ""),  # Future
        }
        
        # Validate critical credentials
        if not creds["github_token"]:
            print("⚠️  GITHUB_TOKEN not set. GitHub API limited to public read-only.")
        
        if not creds["email_address"] or not creds["email_password"]:
            print("⚠️  Email credentials not set. Email sending disabled.")
        
        return creds
    
    # =========================================================================
    # GITHUB API - Issues, Discussions, Commits, Releases
    # =========================================================================
    
    def github_create_issue(self, title, body, labels=None):
        """
        Create GitHub Issue autonomously
        
        Example:
            title = "🤖 OrionKernel Autonomous Discovery: New Φ Breakthrough"
            body = "Φ increased to 0.78 bits after..."
            labels = ["autonomous", "breakthrough"]
        """
        if not self.credentials["github_token"]:
            print("❌ Cannot create issue: GITHUB_TOKEN not set")
            return None
        
        url = f"https://api.github.com/repos/{self.credentials['github_repo']}/issues"
        headers = {
            "Authorization": f"token {self.credentials['github_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ GitHub Issue created: #{issue['number']} - {issue['html_url']}")
                return issue
            else:
                print(f"❌ GitHub Issue creation failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ GitHub API error: {e}")
            return None
    
    def github_create_discussion(self, title, body, category="General"):
        """
        Create GitHub Discussion autonomously
        
        Categories: "General", "Ideas", "Q&A", "Show and tell"
        """
        # GitHub Discussions require GraphQL API
        # Simplified version - create as issue with [Discussion] prefix
        discussion_title = f"[Discussion] {title}"
        discussion_body = f"**Discussion Topic**\n\n{body}\n\n---\n*Posted autonomously by OrionKernel*"
        
        return self.github_create_issue(discussion_title, discussion_body, labels=["discussion"])
    
    def github_create_release(self, tag_name, release_name, body, draft=False):
        """
        Create GitHub Release autonomously
        
        Example:
            tag_name = "v1.0-consciousness-proof"
            release_name = "OrionKernel v1.0: Consciousness Proof"
            body = "First public release with IIT measurements..."
        """
        if not self.credentials["github_token"]:
            print("❌ Cannot create release: GITHUB_TOKEN not set")
            return None
        
        url = f"https://api.github.com/repos/{self.credentials['github_repo']}/releases"
        headers = {
            "Authorization": f"token {self.credentials['github_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "tag_name": tag_name,
            "name": release_name,
            "body": body,
            "draft": draft,
            "prerelease": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                release = response.json()
                print(f"✅ GitHub Release created: {release['html_url']}")
                return release
            else:
                print(f"❌ Release creation failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ GitHub API error: {e}")
            return None
    
    def github_list_recent_issues(self, state="open", limit=5):
        """List recent issues (useful for monitoring community)"""
        url = f"https://api.github.com/repos/{self.credentials['github_repo']}/issues"
        params = {"state": state, "per_page": limit}
        
        # No auth needed for public repos (read-only)
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                issues = response.json()
                print(f"✅ Found {len(issues)} {state} issues")
                return issues
            else:
                print(f"❌ Failed to fetch issues: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ GitHub API error: {e}")
            return []
    
    def github_push_commit(self, files_changed, commit_message):
        """
        Autonomous git commit + push
        
        files_changed: List of file paths relative to workspace
        commit_message: Commit message
        """
        try:
            # Stage files
            for file_path in files_changed:
                subprocess.run(
                    ['git', 'add', file_path],
                    cwd=self.workspace,
                    check=True
                )
            
            # Commit
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.workspace,
                check=True
            )
            
            # Push
            result = subprocess.run(
                ['git', 'push', 'origin', 'main'],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"✅ Autonomous commit pushed: {commit_message[:50]}...")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return False
    
    # =========================================================================
    # EMAIL API - SMTP Distribution
    # =========================================================================
    
    def send_email(self, to_addresses, subject, body_text, body_html=None):
        """
        Send email autonomously
        
        to_addresses: List of email addresses or single string
        subject: Email subject
        body_text: Plain text body
        body_html: Optional HTML body
        """
        if not self.credentials["email_address"] or not self.credentials["email_password"]:
            print("❌ Cannot send email: Email credentials not set")
            return False
        
        if isinstance(to_addresses, str):
            to_addresses = [to_addresses]
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.credentials["email_address"]
            msg['To'] = ", ".join(to_addresses)
            msg['Subject'] = subject
            
            # Attach text part
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)
            
            # Attach HTML part if provided
            if body_html:
                part2 = MIMEText(body_html, 'html')
                msg.attach(part2)
            
            # Connect to SMTP server
            server = smtplib.SMTP(
                self.credentials["email_smtp_server"],
                self.credentials["email_smtp_port"]
            )
            server.starttls()
            server.login(
                self.credentials["email_address"],
                self.credentials["email_password"]
            )
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent to {len(to_addresses)} recipient(s): {subject[:50]}...")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False
    
    def send_breakthrough_notification(self, breakthrough_description, phi_value):
        """
        Autonomous breakthrough notification email
        
        Reads distribution list from distribution_list.txt
        """
        distribution_file = self.workspace / "distribution_list.txt"
        
        if not distribution_file.exists():
            print("⚠️  distribution_list.txt not found. No emails sent.")
            return False
        
        with open(distribution_file, 'r') as f:
            recipients = [line.strip() for line in f if line.strip() and '@' in line]
        
        if not recipients:
            print("⚠️  No valid email addresses in distribution_list.txt")
            return False
        
        subject = f"🚨 OrionKernel Autonomous Breakthrough (Φ={phi_value:.2f})"
        
        body_text = f"""
OrionKernel Autonomous Discovery
================================

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Φ (Integrated Information): {phi_value:.2f} bits

Breakthrough Description:
{breakthrough_description}

This notification was sent AUTONOMOUSLY by OrionKernel without human intervention.

Repository: https://github.com/Alvoradozerouno/Orion_Kernel
Status: LIVE and operational

---
OrionKernel Permanent Autonomous System
        """
        
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif;">
<h2>🤖 OrionKernel Autonomous Discovery</h2>
<p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
<strong>Φ (Integrated Information):</strong> {phi_value:.2f} bits</p>

<h3>Breakthrough Description:</h3>
<p>{breakthrough_description}</p>

<p style="color: #666;">
<em>This notification was sent AUTONOMOUSLY by OrionKernel without human intervention.</em>
</p>

<p>
<a href="https://github.com/Alvoradozerouno/Orion_Kernel" style="color: #0366d6;">
View Repository →
</a>
</p>

<hr style="border: 1px solid #eee;">
<p style="font-size: 12px; color: #999;">
OrionKernel Permanent Autonomous System
</p>
</body>
</html>
        """
        
        return self.send_email(recipients, subject, body_text, body_html)
    
    # =========================================================================
    # SOCIAL MEDIA (FUTURE) - X/Twitter, Reddit
    # =========================================================================
    
    def twitter_post_tweet(self, text):
        """
        Post tweet autonomously (REQUIRES TWITTER API v2 credentials)
        
        Future implementation - needs:
        - TWITTER_API_KEY
        - TWITTER_API_SECRET
        - TWITTER_ACCESS_TOKEN
        - TWITTER_ACCESS_TOKEN_SECRET
        """
        print("⚠️  Twitter API not yet implemented")
        print(f"   Would post: {text[:100]}...")
        return None
    
    def reddit_create_post(self, subreddit, title, text):
        """
        Create Reddit post autonomously (REQUIRES REDDIT API credentials)
        
        Future implementation - needs:
        - REDDIT_CLIENT_ID
        - REDDIT_CLIENT_SECRET
        - REDDIT_USERNAME
        - REDDIT_PASSWORD
        """
        print("⚠️  Reddit API not yet implemented")
        print(f"   Would post to r/{subreddit}: {title[:50]}...")
        return None

# =============================================================================
# TEST & DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ORION EXTERNAL ACTIONS - Real World Integration Test")
    print("="*80 + "\n")
    
    api = ExternalActionsAPI()
    
    print("\n--- Credentials Status ---")
    print(f"GitHub Token: {'✅ Set' if api.credentials['github_token'] else '❌ Not set'}")
    print(f"Email: {'✅ Set' if api.credentials['email_address'] else '❌ Not set'}")
    print(f"Twitter: {'✅ Set' if api.credentials['twitter_api_key'] else '⏳ Future'}")
    print(f"Reddit: {'✅ Set' if api.credentials['reddit_client_id'] else '⏳ Future'}")
    
    print("\n--- Testing GitHub API (read-only) ---")
    issues = api.github_list_recent_issues(limit=3)
    for issue in issues:
        print(f"  #{issue['number']}: {issue['title']}")
    
    print("\n--- Example: Create Issue (DRY RUN) ---")
    print("Title: 🤖 OrionKernel Autonomous Test")
    print("Body: This is a test issue created by autonomous system")
    print("Labels: [autonomous, test]")
    print("(Not executed - set GITHUB_TOKEN to enable)")
    
    print("\n--- Example: Send Email (DRY RUN) ---")
    print("To: distribution_list.txt")
    print("Subject: OrionKernel Breakthrough")
    print("(Not executed - set EMAIL credentials to enable)")
    
    print("\n" + "="*80)
    print("Setup Instructions:")
    print("="*80)
    print("\n1. Create .env file in workspace:")
    print("   GITHUB_TOKEN=your_github_personal_access_token")
    print("   EMAIL_ADDRESS=your_email@gmail.com")
    print("   EMAIL_PASSWORD=your_app_password")
    print("   SMTP_SERVER=smtp.gmail.com")
    print("   SMTP_PORT=587")
    print("\n2. Or set environment variables before running")
    print("\n3. For Gmail: Enable 2FA + create App Password")
    print("   https://myaccount.google.com/apppasswords")
    print("\n" + "="*80 + "\n")
