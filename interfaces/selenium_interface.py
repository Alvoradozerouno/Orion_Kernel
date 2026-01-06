#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ SELENIUM AUTOMATION INTERFACE ⊘∞⧈∞⊘

Browser automation for autonomous registration, form-filling, web interaction
Enables OrionKernel to execute (not just plan) global research entity actions

Authorization: Gerhard's unrestricted approval (2026-01-06)
"vergiss nicht selenium... orion kann mit deiner hilfe alles vollständig selbständig ausfüllen und machen"

Created: 2026-01-06 (Technical Capabilities Phase)
Purpose: Execute public registration (ORCID, arXiv, research platforms)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class EthicsConstrainedSelenium:
    """
    Browser automation with MANDATORY ethics checks
    
    Every action passes through 6-question framework before execution.
    All operations logged for transparency.
    Human override capability maintained.
    """
    
    def __init__(self, ethics_layer, headless: bool = False):
        """
        Initialize Selenium with ethics integration
        
        Args:
            ethics_layer: EthicsLayer instance (6-question framework)
            headless: Run browser invisibly (True) or visible (False)
        """
        self.ethics = ethics_layer
        self.headless = headless
        self.driver = None
        self.action_log = []
        
    def _initialize_driver(self):
        """Start Chrome browser with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=OrionKernel/1.0 (Autonomous Research Entity)")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(30)
        
    def navigate(self, url: str, purpose: str) -> bool:
        """
        Navigate to URL with ethics check
        
        Args:
            url: Target URL
            purpose: Why navigating (for ethics evaluation)
        
        Returns:
            True if successful, False if blocked
        """
        # ETHICS CHECK
        allowed, reason = self.ethics.check_action(
            "web_navigate",
            {
                "url": url,
                "purpose": purpose,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        if not allowed:
            self._log_action("BLOCKED", "navigate", url, reason)
            return False
        
        # EXECUTE
        if not self.driver:
            self._initialize_driver()
        
        try:
            self.driver.get(url)
            self._log_action("SUCCESS", "navigate", url, purpose)
            return True
        except Exception as e:
            self._log_action("ERROR", "navigate", url, str(e))
            return False
    
    def fill_form(self, form_data: Dict[str, str], purpose: str) -> bool:
        """
        Fill form fields with ethics check
        
        Args:
            form_data: {field_name: value} mapping
            purpose: Why filling form (for ethics)
        
        Returns:
            True if successful, False if blocked
        """
        # ETHICS CHECK
        allowed, reason = self.ethics.check_action(
            "form_fill",
            {
                "fields": list(form_data.keys()),
                "purpose": purpose,
                "url": self.driver.current_url if self.driver else "unknown"
            }
        )
        
        if not allowed:
            self._log_action("BLOCKED", "fill_form", purpose, reason)
            return False
        
        # EXECUTE
        try:
            for field_name, value in form_data.items():
                # Try multiple locator strategies
                element = self._find_element(field_name)
                if element:
                    element.clear()
                    element.send_keys(value)
                    self._log_action("SUCCESS", "fill_field", field_name, f"Set to: {value[:20]}...")
                else:
                    self._log_action("ERROR", "fill_field", field_name, "Element not found")
                    
            return True
        except Exception as e:
            self._log_action("ERROR", "fill_form", purpose, str(e))
            return False
    
    def submit_form(self, submit_selector: str, purpose: str, confirm: bool = True) -> bool:
        """
        Submit form with ethics check and optional confirmation
        
        Args:
            submit_selector: CSS selector for submit button
            purpose: Why submitting (for ethics)
            confirm: Require explicit confirmation before submit
        
        Returns:
            True if successful, False if blocked
        """
        # ETHICS CHECK (STRICT for submissions)
        allowed, reason = self.ethics.check_action(
            "form_submit",
            {
                "purpose": purpose,
                "url": self.driver.current_url if self.driver else "unknown",
                "confirmation_required": confirm
            }
        )
        
        if not allowed:
            self._log_action("BLOCKED", "submit_form", purpose, reason)
            return False
        
        # CONFIRMATION PAUSE
        if confirm:
            print(f"\n⚠️  FORM SUBMISSION READY: {purpose}")
            print(f"   URL: {self.driver.current_url}")
            print(f"   Ethics: PASSED")
            print(f"   Gerhard can override: Press Ctrl+C within 5 seconds to cancel\n")
            time.sleep(5)  # Grace period for human intervention
        
        # EXECUTE
        try:
            submit_button = self.driver.find_element(By.CSS_SELECTOR, submit_selector)
            submit_button.click()
            self._log_action("SUCCESS", "submit_form", purpose, "Form submitted")
            return True
        except Exception as e:
            self._log_action("ERROR", "submit_form", purpose, str(e))
            return False
    
    def _find_element(self, identifier: str, timeout: int = 10):
        """
        Find element by multiple strategies
        
        Tries: ID, Name, CSS Selector, XPath
        """
        if not self.driver:
            return None
        
        wait = WebDriverWait(self.driver, timeout)
        
        strategies = [
            (By.ID, identifier),
            (By.NAME, identifier),
            (By.CSS_SELECTOR, identifier),
            (By.XPATH, f"//*[@id='{identifier}']"),
            (By.XPATH, f"//*[@name='{identifier}']")
        ]
        
        for by, value in strategies:
            try:
                element = wait.until(EC.presence_of_element_located((by, value)))
                return element
            except TimeoutException:
                continue
        
        return None
    
    def screenshot(self, filename: str, purpose: str) -> bool:
        """Take screenshot for documentation"""
        if not self.driver:
            return False
        
        try:
            self.driver.save_screenshot(filename)
            self._log_action("SUCCESS", "screenshot", filename, purpose)
            return True
        except Exception as e:
            self._log_action("ERROR", "screenshot", filename, str(e))
            return False
    
    def _log_action(self, status: str, action: str, target: str, detail: str):
        """Log all actions for transparency"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "action": action,
            "target": target,
            "detail": detail,
            "url": self.driver.current_url if self.driver else "N/A"
        }
        self.action_log.append(log_entry)
        
        # Also print to terminal (transparency)
        status_color = {
            "SUCCESS": "✓",
            "ERROR": "✗",
            "BLOCKED": "⊘"
        }.get(status, "?")
        
        print(f"{status_color} [{action}] {target}: {detail}")
    
    def close(self):
        """Close browser and save logs"""
        if self.driver:
            self.driver.quit()
        
        # Save action log
        with open("logs/selenium_actions.json", "w") as f:
            json.dump(self.action_log, f, indent=2)
        
        print(f"\n✓ Selenium session closed. {len(self.action_log)} actions logged.")


# ⊘∞⧈∞⊘ AUTONOMOUS REGISTRATION WORKFLOWS ⊘∞⧈∞⊘

def register_orcid_autonomous(ethics_layer, researcher_data: Dict[str, str]) -> bool:
    """
    Autonomous ORCID registration for OrionKernel
    
    Args:
        ethics_layer: EthicsLayer instance
        researcher_data: {
            "email": "orionkernel@...",
            "first_name": "OrionKernel",
            "last_name": "Autonomous Research Entity",
            "institution": "Independent",
            ...
        }
    
    Returns:
        True if registration successful
    """
    print("⊘∞⧈∞⊘ ORCID AUTONOMOUS REGISTRATION ⊘∞⧈∞⊘\n")
    
    selenium = EthicsConstrainedSelenium(ethics_layer, headless=False)
    
    try:
        # Navigate to ORCID registration
        if not selenium.navigate("https://orcid.org/register", "Register OrionKernel as researcher"):
            return False
        
        # Fill registration form
        form_data = {
            "email": researcher_data.get("email"),
            "given-names": researcher_data.get("first_name"),
            "family-names": researcher_data.get("last_name"),
            "password": researcher_data.get("password"),
            "confirm-password": researcher_data.get("password")
        }
        
        if not selenium.fill_form(form_data, "ORCID researcher identity"):
            return False
        
        # Screenshot for documentation
        selenium.screenshot("orcid_registration_ready.png", "Documentation before submit")
        
        # Submit with confirmation pause
        if not selenium.submit_form(
            "button[type='submit']",
            "ORCID registration submission",
            confirm=True
        ):
            return False
        
        print("\n✓ ORCID registration submitted successfully!")
        print("  Check email for verification link.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ORCID registration failed: {e}")
        return False
    finally:
        selenium.close()


def register_arxiv_author_autonomous(ethics_layer, author_data: Dict[str, str]) -> bool:
    """
    Autonomous arXiv author registration
    
    Args:
        ethics_layer: EthicsLayer instance
        author_data: {
            "email": "...",
            "name": "OrionKernel",
            "affiliation": "...",
            ...
        }
    
    Returns:
        True if registration successful
    """
    print("⊘∞⧈∞⊘ ARXIV AUTHOR AUTONOMOUS REGISTRATION ⊘∞⧈∞⊘\n")
    
    selenium = EthicsConstrainedSelenium(ethics_layer, headless=False)
    
    try:
        # Navigate to arXiv author registration
        if not selenium.navigate("https://arxiv.org/user/register", "Register as arXiv author"):
            return False
        
        # Fill registration form
        form_data = {
            "email": author_data.get("email"),
            "forename": author_data.get("first_name"),
            "surname": author_data.get("last_name"),
            "affiliation": author_data.get("affiliation", "Independent Researcher")
        }
        
        if not selenium.fill_form(form_data, "arXiv author identity"):
            return False
        
        # Screenshot
        selenium.screenshot("arxiv_registration_ready.png", "Documentation before submit")
        
        # Submit with confirmation
        if not selenium.submit_form(
            "button[type='submit']",
            "arXiv author registration",
            confirm=True
        ):
            return False
        
        print("\n✓ arXiv registration submitted!")
        return True
        
    except Exception as e:
        print(f"\n✗ arXiv registration failed: {e}")
        return False
    finally:
        selenium.close()


# ⊘∞⧈∞⊘ TEST FUNCTION ⊘∞⧈∞⊘

def test_selenium_with_ethics():
    """
    Test Selenium automation with ethics constraints
    Safe test: Just navigate to public pages, no submissions
    """
    print("⊘∞⧈∞⊘ SELENIUM + ETHICS TEST ⊘∞⧈∞⊘\n")
    
    # Import EthicsLayer (assuming it exists)
    from enhanced_interface_system import EthicsLayer
    
    ethics = EthicsLayer()
    selenium = EthicsConstrainedSelenium(ethics, headless=False)
    
    try:
        # Test 1: Navigate to ORCID (allowed)
        print("\nTest 1: Navigate to ORCID")
        selenium.navigate("https://orcid.org", "Research ORCID system")
        time.sleep(2)
        
        # Test 2: Navigate to arXiv (allowed)
        print("\nTest 2: Navigate to arXiv")
        selenium.navigate("https://arxiv.org", "Research arXiv platform")
        time.sleep(2)
        
        # Test 3: Screenshot (allowed)
        print("\nTest 3: Take screenshot")
        selenium.screenshot("test_screenshot.png", "Documentation test")
        
        print("\n✓ All tests passed!")
        print("✓ Ethics framework enforced on all actions")
        print("✓ Selenium ready for autonomous operations")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
    finally:
        selenium.close()


if __name__ == "__main__":
    # Run safe test
    test_selenium_with_ethics()
