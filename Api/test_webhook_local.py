#!/usr/bin/env python3
"""
Test script to test the webhook endpoint locally
"""

import requests
import json
import hmac
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Configuration
WEBHOOK_URL = "http://localhost:8000/webhooks/github"
SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "test_secret")

# Sample GitHub webhook payload (based on your actual webhook)
sample_payload = {
    "action": "opened",
    "number": 999,
    "pull_request": {
        "id": 2786741146,
        "number": 999,
        "title": "Test PR for Local Testing",
        "body": "This is a test PR to verify webhook functionality",
        "state": "open",
        "draft": False,
        "user": {
            "login": "Manoj645"
        },
        "html_url": "https://github.com/Manoj645/AI_Agents_Repo/pull/999",
        "created_at": "2025-08-30T11:55:07Z",
        "updated_at": "2025-08-30T11:55:07Z",
        "closed_at": None,
        "merged_at": None,
        "additions": 10,
        "deletions": 2,
        "changed_files": 1,
        "commits": 1,
        "mergeable": None,
        "rebaseable": None,
        "mergeable_state": "unknown",
        "head": {
            "ref": "test-branch",
            "sha": "test123456789"
        },
        "base": {
            "ref": "main",
            "sha": "main123456789"
        }
    },
    "repository": {
        "full_name": "Manoj645/AI_Agents_Repo"
    }
}

def generate_signature(payload: str, secret: str) -> str:
    """Generate GitHub webhook signature"""
    return f"sha256={hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()}"

def test_webhook():
    """Test the webhook endpoint"""
    print(f"Testing webhook at: {WEBHOOK_URL}")
    print(f"Using secret: {SECRET[:10]}..." if len(SECRET) > 10 else f"Using secret: {SECRET}")
    
    # Convert payload to JSON string
    payload_str = json.dumps(sample_payload)
    
    # Generate signature
    signature = generate_signature(payload_str, SECRET)
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature
    }
    
    try:
        # Send request
        response = requests.post(
            WEBHOOK_URL,
            data=payload_str,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print("❌ Webhook test failed!")
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_webhook()
