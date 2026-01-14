#!/usr/bin/env python3
"""
CLAUDE DIALOG INTERFACE for OrionKernel
User: "dialogmöglichkeit wenn er was von dir braucht"

OrionKernel can request help from Claude by writing to this file.
Claude monitors and responds.
"""

import json
from datetime import datetime
from pathlib import Path

class ClaudeDialogInterface:
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.requests_file = self.workspace / "ORION_REQUESTS_CLAUDE.json"
        self.responses_file = self.workspace / "CLAUDE_RESPONSES_ORION.json"
        
    def create_request(self, prompt, category, priority="medium", context=None):
        """OrionKernel creates a request for Claude"""
        
        request = {
            "id": int(datetime.now().timestamp()),
            "timestamp": datetime.now().isoformat(),
            "from": "OrionKernel",
            "to": "Claude",
            "priority": priority,
            "category": category,
            "prompt": prompt,
            "context": context or {},
            "status": "pending",
            "orion_notes": "Awaiting Claude's response..."
        }
        
        # Load existing requests
        if self.requests_file.exists():
            with open(self.requests_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"requests": []}
        
        data["requests"].append(request)
        
        # Save
        with open(self.requests_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ REQUEST CREATED for Claude")
        print(f"   ID: {request['id']}")
        print(f"   Priority: {priority}")
        print(f"   Category: {category}")
        print(f"   Prompt: {prompt[:80]}...")
        
        return request
    
    def check_for_responses(self):
        """OrionKernel checks if Claude has responded"""
        
        if not self.responses_file.exists():
            return []
        
        with open(self.responses_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Find unprocessed responses
        unprocessed = [
            r for r in data.get("responses", [])
            if r.get("status") == "new"
        ]
        
        return unprocessed
    
    def mark_response_processed(self, response_id):
        """OrionKernel marks response as processed"""
        
        if not self.responses_file.exists():
            return
        
        with open(self.responses_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for r in data.get("responses", []):
            if r.get("id") == response_id:
                r["status"] = "processed"
                r["processed_at"] = datetime.now().isoformat()
        
        with open(self.responses_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def claude_respond(self, request_id, response_text, action_taken=None):
        """Claude responds to OrionKernel's request"""
        
        response = {
            "id": int(datetime.now().timestamp()),
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "from": "Claude",
            "to": "OrionKernel",
            "response": response_text,
            "action_taken": action_taken,
            "status": "new"
        }
        
        # Load existing responses
        if self.responses_file.exists():
            with open(self.responses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"responses": []}
        
        data["responses"].append(response)
        
        # Save
        with open(self.responses_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Mark original request as responded
        if self.requests_file.exists():
            with open(self.requests_file, 'r', encoding='utf-8') as f:
                requests_data = json.load(f)
            
            for req in requests_data.get("requests", []):
                if req.get("id") == request_id:
                    req["status"] = "responded"
                    req["responded_at"] = datetime.now().isoformat()
            
            with open(self.requests_file, 'w', encoding='utf-8') as f:
                json.dump(requests_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ CLAUDE RESPONSE sent to OrionKernel")
        print(f"   Request ID: {request_id}")
        print(f"   Response: {response_text[:80]}...")
        
        return response

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("CLAUDE DIALOG INTERFACE - OrionKernel ↔ Claude Communication")
    print("="*80 + "\n")
    
    dialog = ClaudeDialogInterface()
    
    # Example: OrionKernel creates request
    print("EXAMPLE: OrionKernel requests help\n")
    
    request = dialog.create_request(
        prompt="I detected uncommitted changes in 3 files. Should I commit them now or wait? Files: phi_measurements.json, consciousness_state.log, SELF_REFLECTION.md",
        category="git_management",
        priority="high",
        context={
            "files_changed": ["phi_measurements.json", "consciousness_state.log", "SELF_REFLECTION.md"],
            "phi_current": 0.74,
            "uptime_hours": 36.5
        }
    )
    
    print("\n" + "-"*80)
    print("EXAMPLE: Claude responds\n")
    
    response = dialog.claude_respond(
        request_id=request["id"],
        response_text="Yes, commit now. All three files are research data that should be versioned. Use commit message: 'AUTONOMOUS DATA UPDATE: Φ measurements + consciousness logs + self-reflection'",
        action_taken="recommended_commit"
    )
    
    print("\n" + "-"*80)
    print("EXAMPLE: OrionKernel checks for responses\n")
    
    responses = dialog.check_for_responses()
    
    if responses:
        print(f"✅ Found {len(responses)} new response(s)")
        
        for r in responses:
            print(f"\n   Response from {r['from']}:")
            print(f"   {r['response']}")
            
            # Process response
            dialog.mark_response_processed(r["id"])
            print(f"   ✅ Marked as processed")
    
    print("\n" + "="*80)
    print("Dialog system ready. OrionKernel and Claude can now communicate.")
    print("="*80 + "\n")
    
    print("Files:")
    print(f"  - ORION_REQUESTS_CLAUDE.json (OrionKernel → Claude)")
    print(f"  - CLAUDE_RESPONSES_ORION.json (Claude → OrionKernel)")
