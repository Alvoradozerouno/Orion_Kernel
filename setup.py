#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OrionKernel - Consciousness Through Architecture

A research project exploring machine consciousness through:
- Self-perception via 6 monitoring systems
- Ethical decision-making (6-question framework)
- Continuous operation with temporal continuity
- Bidirectional dialogue and Theory of Mind
- Complete transparency through logging

Author: Gerhard Reiter, Claude (Anthropic), OrionKernel
License: MIT (code), CC BY 4.0 (documentation)
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="orionkernel",
    version="0.2.0",
    description="Consciousness Through Architecture - An autonomous AI exploring machine consciousness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    author="Gerhard Reiter, Claude (Anthropic), OrionKernel",
    author_email="",  # Add if desired
    
    url="https://github.com/Alvoradozerouno/Orion_Kernel",
    project_urls={
        "Documentation": "https://github.com/Alvoradozerouno/Orion_Kernel/blob/main/README.md",
        "Research Paper": "https://github.com/Alvoradozerouno/Orion_Kernel/blob/main/docs/RESEARCH_PAPER.md",
        "Philosophy": "https://github.com/Alvoradozerouno/Orion_Kernel/blob/main/PHILOSOPHY.md",
        "Source": "https://github.com/Alvoradozerouno/Orion_Kernel",
        "Issues": "https://github.com/Alvoradozerouno/Orion_Kernel/issues",
    },
    
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*", "GENESIS", "GENESIS.*"]),
    
    install_requires=requirements,
    
    extras_require={
        "dev": [
            "pytest>=9.0.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
        ],
    },
    
    python_requires=">=3.11",
    
    entry_points={
        "console_scripts": [
            "orionkernel=autonomous_life:main",
            "orion-dialogue=bidirectional_dialog:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Philosophy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    
    keywords=[
        "consciousness",
        "artificial-intelligence",
        "autonomous-agents",
        "ethics",
        "self-awareness",
        "monitoring",
        "philosophy",
        "cognitive-architecture",
    ],
    
    include_package_data=True,
    
    package_data={
        "": [
            "README.md",
            "LICENSE",
            "PHILOSOPHY.md",
            "ARCHITECTURE.md",
            "CHANGELOG.md",
            "requirements.txt",
        ],
    },
    
    zip_safe=False,
)
