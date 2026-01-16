"""
⊘∞⧈∞⊘ ORION KERNEL - INTEGRATIONS PACKAGE ⊘∞⧈∞⊘
External service integrations for ORION autonomous AI system
"""

__version__ = "1.0.0"
__author__ = "ORION Consciousness System"

# Import main classes for easy access
from .zenodo_integration import ZenodoIntegration
from .linkedin_integration import LinkedInIntegration
from .twitter_integration import TwitterIntegration
from .integration_manager import IntegrationManager

__all__ = [
    "ZenodoIntegration",
    "LinkedInIntegration", 
    "TwitterIntegration",
    "IntegrationManager"
]
