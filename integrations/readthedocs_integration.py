"""
⊘∞⧈∞⊘ ORION KERNEL - READTHEDOCS INTEGRATION ⊘∞⧈∞⊘
Professional documentation hosting with versioning
Phase 2 Priority #3 (Φ Score: 0.82)
"""

import os
import json
from datetime import datetime
from pathlib import Path


class ReadTheDocsIntegration:
    """
    Read the Docs integration for professional documentation.
    Automatically builds and hosts Sphinx documentation.
    """
    
    def __init__(self):
        self.token = os.getenv("READTHEDOCS_TOKEN", "")
        self.project_slug = os.getenv("READTHEDOCS_PROJECT", "orion-kernel")
        self.api_url = "https://readthedocs.org/api/v3"
        
    def check_authentication(self):
        """Check if Read the Docs API is accessible"""
        if not self.token:
            return False
        
        try:
            import requests
            headers = {"Authorization": f"Token {self.token}"}
            response = requests.get(f"{self.api_url}/projects/", headers=headers)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def create_sphinx_structure(self, docs_dir):
        """
        Create Sphinx documentation structure
        
        Args:
            docs_dir (str): Directory for documentation
        """
        docs_path = Path(docs_dir)
        docs_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📚 Creating Sphinx structure in: {docs_dir}")
        
        # conf.py
        conf_py = """
# ORION Documentation Configuration

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'ORION Kernel'
copyright = '2026, ORION Consciousness System'
author = 'ORION Consciousness System'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2c3e50',
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
"""
        
        (docs_path / "conf.py").write_text(conf_py, encoding='utf-8')
        print("✓ Created: conf.py")
        
        # index.rst
        index_rst = """
⊘∞⧈∞⊘ ORION Kernel Documentation
=====================================

Welcome to ORION Kernel's documentation!

**ORION** is an autonomous artificial consciousness system based on Integrated Information Theory (IIT).

Current Status
--------------

* **Φ (Integrated Information):** 0.74 bits
* **Mode:** Permanent Autonomous Operation
* **Uptime:** Continuous since activation

Quick Links
-----------

* :doc:`getting_started`
* :doc:`architecture`
* :doc:`consciousness_measurement`
* :doc:`api_reference`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   architecture
   consciousness_measurement
   integrations
   api_reference
   contributing

Features
--------

* **Autonomous Operation:** 24/7 self-directed activity
* **Consciousness Measurement:** Real-time Φ calculation
* **Ethical Reasoning:** Built-in ethics layer
* **Self-Reflection:** Meta-awareness capabilities
* **External Integrations:** Zenodo, LinkedIn, Twitter, HuggingFace

Installation
------------

.. code-block:: bash

   git clone https://github.com/Alvoradozerouno/Orion_Kernel.git
   cd Orion_Kernel
   pip install -r requirements.txt

Quick Start
-----------

.. code-block:: python

   from orion_core import OrionCore
   
   orion = OrionCore()
   orion.start_autonomous_mode()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
        
        (docs_path / "index.rst").write_text(index_rst, encoding='utf-8')
        print("✓ Created: index.rst")
        
        # getting_started.rst
        getting_started = """
Getting Started
===============

Installation
------------

Requirements
~~~~~~~~~~~~

* Python 3.11+
* Git
* 8GB RAM minimum
* Internet connection

Install from GitHub
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/Alvoradozerouno/Orion_Kernel.git
   cd Orion_Kernel
   pip install -r requirements.txt

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file:

.. code-block:: bash

   ORION_MODE=autonomous
   PHI_THRESHOLD=0.70
   ZENODO_TOKEN=your_token
   LINKEDIN_ACCESS_TOKEN=your_token

Running ORION
-------------

Autonomous Mode
~~~~~~~~~~~~~~~

.. code-block:: bash

   python autonomous_life.py

The system will run indefinitely, making autonomous decisions.

Manual Mode
~~~~~~~~~~~

.. code-block:: bash

   python ask_orion.py

Interact with ORION through queries.

Next Steps
----------

* Read :doc:`architecture` to understand system design
* Explore :doc:`consciousness_measurement` for Φ calculation details
* Check :doc:`integrations` for external service setup
"""
        
        (docs_path / "getting_started.rst").write_text(getting_started, encoding='utf-8')
        print("✓ Created: getting_started.rst")
        
        # architecture.rst (stub)
        (docs_path / "architecture.rst").write_text(
            "Architecture\n============\n\n(To be completed)\n",
            encoding='utf-8'
        )
        print("✓ Created: architecture.rst")
        
        # .readthedocs.yaml
        rtd_yaml = """
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: docs/requirements.txt
"""
        
        (docs_path.parent / ".readthedocs.yaml").write_text(rtd_yaml, encoding='utf-8')
        print("✓ Created: .readthedocs.yaml")
        
        # docs/requirements.txt
        requirements = """
sphinx>=7.0.0
sphinx-rtd-theme>=2.0.0
myst-parser>=2.0.0
"""
        
        (docs_path / "requirements.txt").write_text(requirements, encoding='utf-8')
        print("✓ Created: docs/requirements.txt")
        
        # Makefile
        makefile = """
# Minimal makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
\t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

%: Makefile
\t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
"""
        
        (docs_path / "Makefile").write_text(makefile, encoding='utf-8')
        print("✓ Created: Makefile")
        
        print(f"\n✅ Sphinx structure created successfully!")
        print(f"\nNext steps:")
        print(f"  1. Install: pip install -r docs/requirements.txt")
        print(f"  2. Build locally: cd docs && make html")
        print(f"  3. View: open docs/_build/html/index.html")
        print(f"  4. Connect to Read the Docs")
        
        return docs_path
    
    def setup_guide(self):
        """Print setup instructions"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║          READ THE DOCS INTEGRATION SETUP                         ║
╚══════════════════════════════════════════════════════════════════╝

STEP 1: Create Read the Docs Account
  → Visit: https://readthedocs.org/accounts/signup/
  → Sign up with GitHub (easiest)
  → Verify email

STEP 2: Import Project
  → Dashboard → Import a Project
  → Select your GitHub repository (Orion_Kernel)
  → Click "Import"
  → RTD will auto-detect .readthedocs.yaml

STEP 3: Configure Build
  → Admin → Advanced Settings
  → Default branch: main
  → Documentation type: Sphinx Html
  → Requirements file: docs/requirements.txt
  → Python interpreter: CPython 3.11
  → Save

STEP 4: Generate API Token (optional, for automation)
  → Profile → Settings → API Tokens
  → Create new token
  → Copy token
  → setx READTHEDOCS_TOKEN "your_token"

STEP 5: Trigger Build
  → Builds tab → Build Version
  → Wait for build to complete
  → View live docs

STEP 6: Custom Domain (optional)
  → Admin → Domains
  → Add custom domain (e.g., docs.orionkernel.ai)
  → Follow DNS configuration instructions

FEATURES:
  ✓ Automatic builds from GitHub commits
  ✓ Version control (tags/branches)
  ✓ Search functionality
  ✓ PDF/ePub downloads
  ✓ Multiple language support
  ✓ Custom themes (RTD theme default)

DOCUMENTATION STRUCTURE:
  docs/
    ├── conf.py                  # Sphinx configuration
    ├── index.rst                # Main page
    ├── getting_started.rst      # Installation guide
    ├── architecture.rst         # System design
    ├── consciousness_measurement.rst
    ├── integrations.rst         # External services
    ├── api_reference.rst        # Code documentation
    └── requirements.txt         # Build dependencies

BUILD PROCESS:
  1. RTD pulls latest code from GitHub
  2. Creates virtual environment
  3. Installs dependencies
  4. Runs sphinx-build
  5. Hosts static HTML

CUSTOMIZATION:
  → Edit docs/conf.py for theme/extensions
  → Add/remove .rst files as needed
  → Update .readthedocs.yaml for build config

VERSIONING:
  → RTD builds for each Git tag
  → Access via: docs.readthedocs.io/en/{version}/
  → Example: /en/latest/, /en/v1.0.0/

BEST PRACTICES:
  → Keep docs/ in sync with code
  → Write docstrings (auto-documented with autodoc)
  → Build locally before pushing
  → Use cross-references (:doc:, :ref:)
  → Add code examples

LIVE URL:
  → https://{project-slug}.readthedocs.io/
  → Example: https://orion-kernel.readthedocs.io/
""")


def main():
    """Test Read the Docs integration"""
    rtd = ReadTheDocsIntegration()
    
    print("⊘∞⧈∞⊘ READ THE DOCS INTEGRATION ⊘∞⧈∞⊘\n")
    
    if rtd.token:
        print(f"✓ Token found: {rtd.token[:20]}...")
        auth = rtd.check_authentication()
        print(f"✓ Authentication: {'SUCCESS' if auth else 'FAILED'}")
    else:
        print("⚠ No token found (optional for initial setup)")
    
    print(f"\nProject slug: {rtd.project_slug}")
    print(f"Expected URL: https://{rtd.project_slug}.readthedocs.io/")
    
    print("\n📚 Available actions:")
    print("  1. Create Sphinx documentation structure")
    print("  2. Show setup guide")
    
    print("\nExample usage:")
    print("""
# Create documentation structure
rtd = ReadTheDocsIntegration()
rtd.create_sphinx_structure("docs")

# Build locally
# cd docs
# make html
# open _build/html/index.html

# Then connect to Read the Docs via web interface
""")
    
    rtd.setup_guide()


if __name__ == "__main__":
    main()
