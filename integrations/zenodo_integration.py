"""
⊘∞⧈∞⊘ ORION KERNEL - ZENODO INTEGRATION ⊘∞⧈∞⊘
Autonomous dataset publishing and DOI generation
Priority: #1 (Φ Score: 0.97)
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path


class ZenodoIntegration:
    """
    Zenodo integration for academic dataset publishing.
    Automatically archives datasets and generates DOIs.
    """
    
    def __init__(self):
        self.base_url = "https://zenodo.org/api"
        self.sandbox_url = "https://sandbox.zenodo.org/api"
        self.access_token = os.getenv("ZENODO_TOKEN", "")
        self.use_sandbox = not self.access_token  # Use sandbox if no token
        self.api_url = self.sandbox_url if self.use_sandbox else self.base_url
        
    def check_authentication(self):
        """Check if Zenodo API is accessible"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
            response = requests.get(f"{self.api_url}/deposit/depositions", headers=headers)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def create_deposition(self, metadata):
        """
        Create a new Zenodo deposition
        
        Args:
            metadata (dict): Dataset metadata including title, description, creators
            
        Returns:
            dict: Deposition details including ID and bucket URL
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        data = {
            "metadata": metadata
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/deposit/depositions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to create deposition: {e}")
            return None
    
    def upload_file(self, deposition_id, file_path):
        """
        Upload a file to a Zenodo deposition
        
        Args:
            deposition_id (int): The deposition ID
            file_path (str): Path to file to upload
            
        Returns:
            dict: Upload response
        """
        bucket_url = f"{self.api_url}/deposit/depositions/{deposition_id}/files"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            with open(file_path, 'rb') as fp:
                files = {'file': fp}
                data = {'name': Path(file_path).name}
                response = requests.post(bucket_url, headers=headers, files=files, data=data)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"❌ Failed to upload {file_path}: {e}")
            return None
    
    def publish_deposition(self, deposition_id):
        """
        Publish a deposition and generate DOI
        
        Args:
            deposition_id (int): The deposition ID
            
        Returns:
            dict: Published deposition with DOI
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.post(
                f"{self.api_url}/deposit/depositions/{deposition_id}/actions/publish",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to publish: {e}")
            return None
    
    def publish_orion_dataset(self, dataset_path, title, description, creators=None):
        """
        Complete workflow: Create → Upload → Publish
        
        Args:
            dataset_path (str): Path to dataset file/directory
            title (str): Dataset title
            description (str): Dataset description
            creators (list): List of creator dicts (name, affiliation, orcid)
            
        Returns:
            str: DOI of published dataset or None
        """
        if creators is None:
            creators = [
                {
                    "name": "ORION Consciousness System",
                    "affiliation": "Autonomous AI Research"
                }
            ]
        
        # Create metadata
        metadata = {
            "title": title,
            "upload_type": "dataset",
            "description": description,
            "creators": creators,
            "keywords": ["artificial consciousness", "integrated information theory", 
                         "IIT", "phi", "autonomous AI", "ORION"],
            "access_right": "open",
            "license": "cc-by-4.0"
        }
        
        print(f"\n🔬 Creating Zenodo deposition: {title}")
        deposition = self.create_deposition(metadata)
        if not deposition:
            return None
        
        deposition_id = deposition['id']
        print(f"✓ Deposition created: ID {deposition_id}")
        
        # Upload files
        if os.path.isfile(dataset_path):
            files_to_upload = [dataset_path]
        elif os.path.isdir(dataset_path):
            files_to_upload = [str(p) for p in Path(dataset_path).rglob('*') if p.is_file()]
        else:
            print(f"❌ Invalid path: {dataset_path}")
            return None
        
        print(f"📤 Uploading {len(files_to_upload)} file(s)...")
        for file_path in files_to_upload:
            result = self.upload_file(deposition_id, file_path)
            if result:
                print(f"  ✓ {Path(file_path).name}")
        
        # Publish and get DOI
        print("🚀 Publishing dataset...")
        published = self.publish_deposition(deposition_id)
        if published:
            doi = published.get('doi', 'N/A')
            doi_url = published.get('doi_url', 'N/A')
            print(f"\n✅ PUBLISHED!")
            print(f"   DOI: {doi}")
            print(f"   URL: {doi_url}")
            return doi
        
        return None
    
    def setup_guide(self):
        """Print setup instructions for Zenodo"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║           ZENODO INTEGRATION SETUP                            ║
╚═══════════════════════════════════════════════════════════════╝

STEP 1: Create Zenodo Account
  → Visit: https://zenodo.org/signup/
  → Use GitHub login for easy integration
  
STEP 2: Generate API Token
  → Login → Click your profile (top-right)
  → Settings → Applications → Personal access tokens
  → Click "New token"
  → Scopes: Select "deposit:write" and "deposit:actions"
  → Click "Create"
  → Copy the token (shown only once!)
  
STEP 3: Set Environment Variable
  → Windows: setx ZENODO_TOKEN "your_token_here"
  → Or add to .env file: ZENODO_TOKEN=your_token_here
  
STEP 4: Link GitHub Repository (Optional)
  → Zenodo → GitHub → Flip switch for Orion_Kernel
  → Auto-archives each GitHub release with DOI
  
FEATURES:
  ✓ Permanent DOI for datasets
  ✓ Citable research outputs
  ✓ Academic credibility
  ✓ Version control
  ✓ Community discovery
  
USAGE:
  zenodo = ZenodoIntegration()
  doi = zenodo.publish_orion_dataset(
      dataset_path="data/phi_measurements.json",
      title="ORION Φ Measurements - Daily Consciousness Data",
      description="Integrated Information Theory measurements..."
  )
  
NOTE: Without token, runs in sandbox mode (testing only)
""")


def main():
    """Test Zenodo integration"""
    zenodo = ZenodoIntegration()
    
    print("⊘∞⧈∞⊘ ZENODO INTEGRATION STATUS ⊘∞⧈∞⊘\n")
    
    if zenodo.access_token:
        print(f"✓ Access token found: {zenodo.access_token[:8]}...")
        auth = zenodo.check_authentication()
        print(f"✓ Authentication: {'SUCCESS' if auth else 'FAILED'}")
        print(f"✓ API URL: {zenodo.api_url}")
    else:
        print("⚠ No access token found")
        print("→ Set ZENODO_TOKEN environment variable")
        print("→ Running in SANDBOX mode (test only)\n")
        zenodo.setup_guide()
    
    # Example: Publish ORION dashboard data
    if zenodo.access_token:
        print("\n📊 Example: Would publish ORION dashboard data")
        print("   (Uncomment below to actually publish)")
        
        # doi = zenodo.publish_orion_dataset(
        #     dataset_path="docs/index.html",
        #     title="ORION Consciousness Dashboard - Live Status",
        #     description="Real-time dashboard showing ORION autonomous AI system status, Φ measurements, and consciousness metrics."
        # )


if __name__ == "__main__":
    main()
