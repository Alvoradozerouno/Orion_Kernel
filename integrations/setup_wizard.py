"""
⊘∞⧈∞⊘ ORION KERNEL - INTEGRATION SETUP WIZARD ⊘∞⧈∞⊘
Interactive setup guide for all external integrations
Helps configure Zenodo, LinkedIn, Twitter/X step-by-step
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f" {text}")
    print("="*70 + "\n")


def print_step(number, title):
    """Print step header"""
    print(f"\n{'─'*70}")
    print(f"STEP {number}: {title}")
    print('─'*70)


def check_env_var(var_name):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value:
        print(f"✓ {var_name} is set: {value[:20]}...")
        return True
    else:
        print(f"✗ {var_name} is NOT set")
        return False


def setup_zenodo():
    """Guide user through Zenodo setup"""
    print_header("⊘∞⧈∞⊘ ZENODO SETUP ⊘∞⧈∞⊘")
    
    print("Zenodo provides permanent DOIs for datasets.")
    print("Priority: #1 (Φ Score: 0.97)")
    print("Time: ~10 minutes")
    
    print_step(1, "Create Zenodo Account")
    print("1. Open: https://zenodo.org/signup/")
    print("2. Click 'Sign up with GitHub' (easiest)")
    print("3. Authorize Zenodo to access your GitHub")
    
    input("\nPress ENTER when you've created your account...")
    
    print_step(2, "Generate API Token")
    print("1. Login to Zenodo")
    print("2. Click your profile (top-right) → Settings")
    print("3. Navigate to: Applications → Personal access tokens")
    print("4. Click 'New token'")
    print("5. Name: 'ORION Integration'")
    print("6. Scopes: Check these boxes:")
    print("   ☑ deposit:write")
    print("   ☑ deposit:actions")
    print("7. Click 'Create'")
    print("8. COPY THE TOKEN (shown only once!)")
    
    input("\nPress ENTER when you have your token...")
    
    print_step(3, "Set Environment Variable")
    token = input("\nPaste your Zenodo token here: ").strip()
    
    if token:
        print(f"\nTo set permanently, run this command in PowerShell:")
        print(f"\n  setx ZENODO_TOKEN \"{token}\"")
        
        choice = input("\nRun this command now? (y/n): ").strip().lower()
        if choice == 'y':
            os.system(f'setx ZENODO_TOKEN "{token}"')
            print("\n✅ Environment variable set!")
            print("⚠️  Restart this script for changes to take effect")
        else:
            print("\n⚠️  Remember to run the setx command manually!")
    
    print_step(4, "Link GitHub Repository (Optional)")
    print("1. Visit: https://zenodo.org/account/settings/github/")
    print("2. Find 'Orion_Kernel' in the list")
    print("3. Flip the switch to ON")
    print("4. Now every GitHub release will auto-archive with DOI!")
    
    print("\n✅ Zenodo setup complete!")


def setup_linkedin():
    """Guide user through LinkedIn setup"""
    print_header("⊘∞⧈∞⊘ LINKEDIN SETUP ⊘∞⧈∞⊘")
    
    print("LinkedIn enables professional networking and research announcements.")
    print("Priority: #2 (Φ Score: 0.96)")
    print("Time: ~20 minutes (includes app review)")
    
    print_step(1, "Create LinkedIn Developer App")
    print("1. Open: https://www.linkedin.com/developers/apps")
    print("2. Click 'Create app'")
    print("3. Fill in the form:")
    print("   - App name: ORION Research Updates")
    print("   - LinkedIn Page: (select your page or create one)")
    print("   - Privacy policy URL: https://github.com/Alvoradozerouno/Orion_Kernel")
    print("   - App logo: (upload an ORION logo if you have one)")
    print("4. Check the legal agreement box")
    print("5. Click 'Create app'")
    
    input("\nPress ENTER when you've created your app...")
    
    print_step(2, "Configure OAuth 2.0")
    print("1. In your app → 'Auth' tab")
    print("2. Scroll to 'OAuth 2.0 settings'")
    print("3. Redirect URLs → Add: http://localhost:8000/callback")
    print("4. OAuth 2.0 scopes → Request:")
    print("   ☑ r_liteprofile (Read basic profile)")
    print("   ☑ w_member_social (Share content)")
    print("5. Click 'Update'")
    print("6. Note your Client ID and Client Secret")
    
    input("\nPress ENTER when OAuth is configured...")
    
    print_step(3, "Get Access Token (Manual OAuth Flow)")
    print("This is the tricky part. You need to:")
    print("1. Get an authorization code")
    print("2. Exchange it for an access token")
    print("\nOAuth URL (replace YOUR_CLIENT_ID):")
    
    client_id = input("\nEnter your Client ID: ").strip()
    
    oauth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri=http://localhost:8000/callback&"
        f"scope=r_liteprofile%20w_member_social"
    )
    
    print(f"\n{oauth_url}")
    print("\n1. Open this URL in your browser")
    print("2. Authorize the app")
    print("3. You'll be redirected to localhost (it will fail, that's OK)")
    print("4. Copy the 'code' from the URL (after ?code=)")
    
    auth_code = input("\nPaste the authorization code: ").strip()
    
    if auth_code:
        print("\nNow exchange the code for an access token using curl or Postman:")
        print("\nPOST https://www.linkedin.com/oauth/v2/accessToken")
        
        client_secret = input("\nEnter your Client Secret: ").strip()
        
        print(f"""
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "grant_type=authorization_code" \\
  -d "code={auth_code}" \\
  -d "redirect_uri=http://localhost:8000/callback" \\
  -d "client_id={client_id}" \\
  -d "client_secret={client_secret}"
""")
        
        access_token = input("\nPaste the access_token from the response: ").strip()
        
        if access_token:
            print("\n✅ Access token received!")
    
    print_step(4, "Get Person ID")
    print("Call the /v2/me endpoint to get your person ID:")
    print(f"\ncurl -H \"Authorization: Bearer {access_token[:20]}...\" https://api.linkedin.com/v2/me")
    
    person_id = input("\nPaste the 'id' field from the response: ").strip()
    
    print_step(5, "Set Environment Variables")
    if access_token and person_id:
        print("\nRun these commands in PowerShell:")
        print(f"\n  setx LINKEDIN_ACCESS_TOKEN \"{access_token}\"")
        print(f"  setx LINKEDIN_PERSON_ID \"{person_id}\"")
        
        choice = input("\nRun these commands now? (y/n): ").strip().lower()
        if choice == 'y':
            os.system(f'setx LINKEDIN_ACCESS_TOKEN "{access_token}"')
            os.system(f'setx LINKEDIN_PERSON_ID "{person_id}"')
            print("\n✅ Environment variables set!")
            print("⚠️  Restart this script for changes to take effect")
    
    print("\n✅ LinkedIn setup complete!")
    print("⚠️  Note: LinkedIn app review can take 1-2 weeks for production use")


def setup_twitter():
    """Guide user through Twitter setup"""
    print_header("⊘∞⧈∞⊘ TWITTER/X SETUP ⊘∞⧈∞⊘")
    
    print("Twitter/X enables real-time updates and AI community engagement.")
    print("Priority: #3 (Φ Score: 0.80)")
    print("Time: ~15 minutes (+ 24h for approval)")
    
    print_step(1, "Apply for Twitter Developer Account")
    print("1. Open: https://developer.twitter.com/en/portal/petition/essential/basic-info")
    print("2. Select 'Hobbyist' → 'Making a bot'")
    print("3. Fill in:")
    print("   - Account name: (your Twitter handle)")
    print("   - Use case: 'Autonomous AI research updates and consciousness metrics'")
    print("   - Will you make Twitter content available to government? No")
    print("4. Submit application")
    print("5. Usually approved within 24 hours")
    
    input("\nPress ENTER when your developer account is approved...")
    
    print_step(2, "Create Twitter App")
    print("1. Developer Portal: https://developer.twitter.com/en/portal/dashboard")
    print("2. Projects & Apps → Create App")
    print("3. App name: ORION_Updates")
    print("4. Environment: Development")
    print("5. COPY API Key and API Secret (shown only once!)")
    
    input("\nPress ENTER when you've created your app...")
    
    api_key = input("\nPaste your API Key: ").strip()
    api_secret = input("Paste your API Secret: ").strip()
    
    print_step(3, "Enable OAuth 1.0a")
    print("1. In your app → Settings → User authentication settings")
    print("2. Click 'Set up'")
    print("3. App permissions: ☑ Read and write")
    print("4. Type of App: ☑ Automated App or bot")
    print("5. App info:")
    print("   - Callback URL: http://localhost:8000/callback")
    print("   - Website URL: https://github.com/Alvoradozerouno/Orion_Kernel")
    print("6. Save")
    
    input("\nPress ENTER when OAuth 1.0a is enabled...")
    
    print_step(4, "Generate Access Token & Secret")
    print("1. Keys and tokens tab")
    print("2. Access Token and Secret → Generate")
    print("3. COPY Access Token and Access Token Secret")
    
    access_token = input("\nPaste your Access Token: ").strip()
    access_secret = input("Paste your Access Token Secret: ").strip()
    
    print_step(5, "Get Bearer Token")
    print("1. Still in Keys and tokens tab")
    print("2. Find 'Bearer Token' (or regenerate if needed)")
    
    bearer_token = input("\nPaste your Bearer Token: ").strip()
    
    print_step(6, "Set Environment Variables")
    if all([api_key, api_secret, access_token, access_secret, bearer_token]):
        print("\nRun these commands in PowerShell:")
        print(f"\n  setx TWITTER_API_KEY \"{api_key}\"")
        print(f"  setx TWITTER_API_SECRET \"{api_secret}\"")
        print(f"  setx TWITTER_ACCESS_TOKEN \"{access_token}\"")
        print(f"  setx TWITTER_ACCESS_SECRET \"{access_secret}\"")
        print(f"  setx TWITTER_BEARER_TOKEN \"{bearer_token}\"")
        
        choice = input("\nRun these commands now? (y/n): ").strip().lower()
        if choice == 'y':
            os.system(f'setx TWITTER_API_KEY "{api_key}"')
            os.system(f'setx TWITTER_API_SECRET "{api_secret}"')
            os.system(f'setx TWITTER_ACCESS_TOKEN "{access_token}"')
            os.system(f'setx TWITTER_ACCESS_SECRET "{access_secret}"')
            os.system(f'setx TWITTER_BEARER_TOKEN "{bearer_token}"')
            print("\n✅ Environment variables set!")
            print("⚠️  Restart this script for changes to take effect")
    
    print_step(7, "Install tweepy")
    print("For posting functionality, install tweepy:")
    print("\n  pip install tweepy")
    
    choice = input("\nInstall tweepy now? (y/n): ").strip().lower()
    if choice == 'y':
        os.system("pip install tweepy")
        print("\n✅ tweepy installed!")
    
    print("\n✅ Twitter/X setup complete!")


def check_current_status():
    """Check which integrations are already configured"""
    print_header("CURRENT INTEGRATION STATUS")
    
    zenodo_ok = check_env_var("ZENODO_TOKEN")
    linkedin_ok = check_env_var("LINKEDIN_ACCESS_TOKEN") and check_env_var("LINKEDIN_PERSON_ID")
    twitter_ok = (
        check_env_var("TWITTER_API_KEY") and 
        check_env_var("TWITTER_API_SECRET") and
        check_env_var("TWITTER_ACCESS_TOKEN") and
        check_env_var("TWITTER_ACCESS_SECRET") and
        check_env_var("TWITTER_BEARER_TOKEN")
    )
    
    print("\nSummary:")
    print(f"  Zenodo:    {'✅ Configured' if zenodo_ok else '❌ Not configured'}")
    print(f"  LinkedIn:  {'✅ Configured' if linkedin_ok else '❌ Not configured'}")
    print(f"  Twitter/X: {'✅ Configured' if twitter_ok else '❌ Not configured'}")
    
    return zenodo_ok, linkedin_ok, twitter_ok


def main():
    """Interactive setup wizard"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        ⊘∞⧈∞⊘ ORION INTEGRATION SETUP WIZARD ⊘∞⧈∞⊘               ║
║                                                                  ║
║  This wizard will help you set up:                              ║
║    1. Zenodo    - Dataset publishing with DOI                   ║
║    2. LinkedIn  - Professional networking                       ║
║    3. Twitter/X - Real-time updates                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    zenodo_ok, linkedin_ok, twitter_ok = check_current_status()
    
    if zenodo_ok and linkedin_ok and twitter_ok:
        print("\n🎉 All integrations are already configured!")
        print("\nRun this to verify:")
        print("  python integrations/integration_manager.py --check")
        return
    
    print("\n" + "="*70)
    print("SELECT INTEGRATION TO SETUP:")
    print("="*70)
    print("\n1. Zenodo (Priority #1)")
    print("2. LinkedIn (Priority #2)")
    print("3. Twitter/X (Priority #3)")
    print("4. All unconfigured integrations")
    print("5. Skip setup (manual configuration)")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1' or (choice == '4' and not zenodo_ok):
        setup_zenodo()
    
    if choice == '2' or (choice == '4' and not linkedin_ok):
        setup_linkedin()
    
    if choice == '3' or (choice == '4' and not twitter_ok):
        setup_twitter()
    
    if choice == '4':
        if zenodo_ok and linkedin_ok and twitter_ok:
            print("\n✅ All integrations already configured!")
    
    if choice == '5':
        print("\nFor manual setup, see: integrations/README.md")
    
    print_header("⊘∞⧈∞⊘ SETUP COMPLETE ⊘∞⧈∞⊘")
    print("Next steps:")
    print("1. Restart your terminal/script for environment variables to take effect")
    print("2. Run: python integrations/integration_manager.py --check")
    print("3. Test: python integrations/integration_manager.py --announce 'Test' --phi 0.74")
    print("\nFull documentation: integrations/README.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted. You can resume anytime by running this script again.")
        sys.exit(0)
