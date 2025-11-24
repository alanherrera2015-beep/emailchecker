"""
Example usage of the Email Verifier API
Demonstrates how to interact with the email verification service
"""
import requests
import json


def verify_email(api_url, email):
    """
    Verify an email address using the API
    
    Args:
        api_url: Base URL of the email verifier API
        email: Email address to verify
    
    Returns:
        dict: Verification result
    """
    endpoint = f"{api_url}/verify"
    payload = {"email": email}
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        return {
            "status_code": response.status_code,
            "result": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }


def main():
    # Configure your API URL
    # For local testing: http://localhost:8080
    # For Cloud Run: https://your-service-url.run.app
    API_URL = "http://localhost:8080"
    
    # Test cases
    test_emails = [
        "valid@gmail.com",
        "test@example.com",
        "invalid-email",
        "user@nonexistentdomain12345.com",
        "admin@github.com"
    ]
    
    print("Email Verifier - Example Usage\n")
    print(f"API URL: {API_URL}\n")
    print("=" * 80)
    
    # Test each email
    for email in test_emails:
        print(f"\nVerifying: {email}")
        print("-" * 80)
        
        result = verify_email(API_URL, email)
        
        if "error" in result:
            print(f"ERROR: {result['error']}")
        else:
            print(f"Status Code: {result['status_code']}")
            print(f"Response:")
            print(json.dumps(result['result'], indent=2))
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
