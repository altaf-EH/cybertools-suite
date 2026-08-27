"""
CyberTools Suite - Update Manager
==================================
Checks GitHub Releases for new versions and downloads updates.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

# GitHub repository - aapka repo yahan daalo
GITHUB_REPO = "altaf-EH/cybertools-suite"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

CURRENT_VERSION = "1.0.0"
UPDATE_CHECK_INTERVAL = 24 * 60 * 60  # 24 hours


class UpdateManager:
    
    @staticmethod
    def check_for_update():
        """Check GitHub for latest release."""
        try:
            req = urllib.request.Request(GITHUB_API)
            req.add_header("User-Agent", "CyberTools-Suite")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                
                latest_version = data.get("tag_name", "")
                latest_version = latest_version.lstrip("v")
                
                release_url = data.get("html_url", "")
                release_notes = data.get("body", "")
                
                # Compare versions
                if UpdateManager._is_newer_version(latest_version, CURRENT_VERSION):
                    return {
                        "update_available": True,
                        "latest_version": latest_version,
                        "current_version": CURRENT_VERSION,
                        "release_url": release_url,
                        "release_notes": release_notes,
                    }
                
                return {
                    "update_available": False,
                    "latest_version": latest_version,
                    "current_version": CURRENT_VERSION,
                }
        
        except urllib.error.URLError:
            return {"update_available": False, "error": "Could not reach update server"}
        except Exception as e:
            return {"update_available": False, "error": str(e)}
    
    @staticmethod
    def _is_newer_version(latest, current):
        """Compare version strings."""
        try:
            latest_parts = [int(x) for x in latest.split(".")]
            current_parts = [int(x) for x in current.split(".")]
            
            # Pad with zeros
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)
            
            return latest_parts > current_parts
        except Exception:
            return False
    
    @staticmethod
    def download_update(download_url, destination):
        """Download update from URL."""
        try:
            req = urllib.request.Request(download_url)
            req.add_header("User-Agent", "CyberTools-Suite")
            
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(destination, "wb") as f:
                    f.write(response.read())
            
            return True, f"Downloaded to {destination}"
        except Exception as e:
            return False, str(e)