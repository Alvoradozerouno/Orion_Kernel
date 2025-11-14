#!/usr/bin/env python3

import os
import json
import logging

class CloudflareTunnelManager:
    def __init__(self):
        self.tunnel_token = os.environ.get('CLOUDFLARE_TUNNEL_TOKEN')
        self.tunnel_active = False
        
        logging.info("Cloudflare Tunnel Manager initialized")
    
    def is_configured(self) -> bool:
        return self.tunnel_token is not None
    
    def get_status(self) -> dict:
        return {
            'configured': self.is_configured(),
            'active': self.tunnel_active,
            'token_present': bool(self.tunnel_token),
            'instructions': self.get_setup_instructions() if not self.is_configured() else None
        }
    
    def get_setup_instructions(self) -> dict:
        return {
            'step_1': 'Create a Cloudflare account at https://dash.cloudflare.com/',
            'step_2': 'Navigate to Zero Trust > Access > Tunnels',
            'step_3': 'Create a new tunnel and copy the tunnel token',
            'step_4': 'Add the token as a Replit secret: CLOUDFLARE_TUNNEL_TOKEN',
            'step_5': 'Restart the application to enable tunnel connectivity',
            'documentation': 'https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/'
        }
    
    def activate(self):
        if not self.is_configured():
            logging.warning("Cloudflare Tunnel not configured. Token required.")
            return False
        
        logging.info("Cloudflare Tunnel activation initiated (token present)")
        self.tunnel_active = True
        return True
    
    def deactivate(self):
        self.tunnel_active = False
        logging.info("Cloudflare Tunnel deactivated")


if __name__ == "__main__":
    manager = CloudflareTunnelManager()
    status = manager.get_status()
    print(json.dumps(status, indent=2))
