"""
Email Verifier Backend API
A Flask-based service for verifying email addresses
"""
import re
import dns.resolver
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_email_syntax(email):
    """
    Validate email address syntax using regex
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_mx_records(domain):
    """
    Get MX records for a domain
    """
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return [str(r.exchange) for r in mx_records]
    except dns.resolver.NXDOMAIN:
        logger.warning(f"Domain does not exist: {domain}")
        return None
    except dns.resolver.NoAnswer:
        logger.warning(f"No MX records found for: {domain}")
        return None
    except dns.resolver.Timeout:
        logger.error(f"DNS query timeout for: {domain}")
        return None
    except Exception as e:
        logger.error(f"Error resolving MX records for {domain}: {str(e)}")
        return None


def verify_email(email):
    """
    Comprehensive email verification
    Returns a dictionary with verification results
    """
    result = {
        'email': email,
        'valid': False,
        'syntax_valid': False,
        'domain_exists': False,
        'mx_records': [],
        'message': ''
    }
    
    # Check syntax
    if not validate_email_syntax(email):
        result['message'] = 'Invalid email syntax'
        return result
    
    result['syntax_valid'] = True
    
    # Extract domain
    try:
        domain = email.split('@')[1]
    except IndexError:
        result['message'] = 'Invalid email format'
        return result
    
    # Check MX records
    mx_records = get_mx_records(domain)
    
    if mx_records is None:
        result['message'] = 'Domain does not exist or has no MX records'
        return result
    
    result['domain_exists'] = True
    result['mx_records'] = mx_records
    result['valid'] = True
    result['message'] = 'Email appears to be valid'
    
    return result


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API information
    """
    return jsonify({
        'service': 'Email Verifier API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'API information',
            '/verify': 'Verify email address (POST)',
            '/health': 'Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for monitoring
    """
    return jsonify({'status': 'healthy'}), 200


@app.route('/verify', methods=['POST'])
def verify():
    """
    Verify email address endpoint
    Expects JSON body with 'email' field
    """
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                'error': 'Missing email field in request body'
            }), 400
        
        email = data['email'].strip()
        
        if not email:
            return jsonify({
                'error': 'Email cannot be empty'
            }), 400
        
        # Verify the email
        result = verify_email(email)
        
        # Return appropriate status code
        status_code = 200 if result['valid'] else 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
