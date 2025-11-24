"""
Test suite for Email Verifier API
"""
import pytest
import json
from app import app, validate_email_syntax, get_mx_records, verify_email


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestEmailSyntaxValidation:
    """Test email syntax validation"""
    
    def test_valid_email_syntax(self):
        """Test valid email formats"""
        assert validate_email_syntax('test@example.com') is True
        assert validate_email_syntax('user.name@domain.co.uk') is True
        assert validate_email_syntax('user+tag@example.com') is True
        assert validate_email_syntax('user123@test-domain.com') is True
    
    def test_invalid_email_syntax(self):
        """Test invalid email formats"""
        assert validate_email_syntax('invalid') is False
        assert validate_email_syntax('invalid@') is False
        assert validate_email_syntax('@example.com') is False
        assert validate_email_syntax('test@.com') is False
        assert validate_email_syntax('test @example.com') is False
        assert validate_email_syntax('') is False


class TestMXRecords:
    """Test MX record lookup"""
    
    def test_valid_domain_mx_records(self):
        """Test MX record lookup for a valid domain"""
        mx_records = get_mx_records('gmail.com')
        assert mx_records is not None
        assert len(mx_records) > 0
    
    def test_invalid_domain_mx_records(self):
        """Test MX record lookup for an invalid domain"""
        mx_records = get_mx_records('thisisnotavaliddomainfortesting12345.com')
        assert mx_records is None


class TestEmailVerification:
    """Test complete email verification"""
    
    def test_verify_valid_email(self):
        """Test verification of a valid email"""
        result = verify_email('test@gmail.com')
        assert result['syntax_valid'] is True
        assert result['domain_exists'] is True
        assert result['valid'] is True
        assert len(result['mx_records']) > 0
    
    def test_verify_invalid_syntax(self):
        """Test verification of email with invalid syntax"""
        result = verify_email('invalid-email')
        assert result['syntax_valid'] is False
        assert result['valid'] is False
    
    def test_verify_nonexistent_domain(self):
        """Test verification of email with non-existent domain"""
        result = verify_email('test@nonexistentdomain12345xyz.com')
        assert result['syntax_valid'] is True
        assert result['domain_exists'] is False
        assert result['valid'] is False


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_home_endpoint(self, client):
        """Test the home endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'service' in data
        assert data['service'] == 'Email Verifier API'
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_verify_endpoint_valid_email(self, client):
        """Test verify endpoint with a valid email"""
        response = client.post('/verify',
                              data=json.dumps({'email': 'test@gmail.com'}),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['syntax_valid'] is True
        assert data['email'] == 'test@gmail.com'
    
    def test_verify_endpoint_invalid_email(self, client):
        """Test verify endpoint with an invalid email"""
        response = client.post('/verify',
                              data=json.dumps({'email': 'invalid-email'}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['valid'] is False
    
    def test_verify_endpoint_missing_email(self, client):
        """Test verify endpoint without email field"""
        response = client.post('/verify',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_verify_endpoint_empty_email(self, client):
        """Test verify endpoint with empty email"""
        response = client.post('/verify',
                              data=json.dumps({'email': '   '}),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
