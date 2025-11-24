# Email Verifier Backend

A robust email verification service built with Flask that validates email addresses through syntax checking, domain verification, and MX record lookup.

## Features

- ✅ Email syntax validation using regex patterns
- ✅ Domain existence verification
- ✅ MX record lookup for mail server validation
- ✅ RESTful API with JSON responses
- ✅ CORS enabled for cross-origin requests
- ✅ Health check endpoint for monitoring
- ✅ Docker support for containerized deployment
- ✅ Ready for Google Cloud Run deployment

## API Endpoints

### GET `/`
Returns API information and available endpoints.

**Response:**
```json
{
  "service": "Email Verifier API",
  "version": "1.0.0",
  "endpoints": {
    "/": "API information",
    "/verify": "Verify email address (POST)",
    "/health": "Health check"
  }
}
```

### GET `/health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

### POST `/verify`
Verifies an email address.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Success Response (200):**
```json
{
  "email": "user@example.com",
  "valid": true,
  "syntax_valid": true,
  "domain_exists": true,
  "mx_records": ["mx1.example.com.", "mx2.example.com."],
  "message": "Email appears to be valid"
}
```

**Error Response (400):**
```json
{
  "email": "invalid@nonexistent.com",
  "valid": false,
  "syntax_valid": true,
  "domain_exists": false,
  "mx_records": [],
  "message": "Domain does not exist or has no MX records"
}
```

## Local Development

### Prerequisites
- Python 3.11 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/alanherrera2015-beep/emailchecker.git
cd emailchecker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
```

The server will start on `http://localhost:8080`

### Testing

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest test_app.py -v
```

Run tests with coverage:
```bash
pytest test_app.py --cov=app --cov-report=html
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t email-verifier .
```

### Run Docker Container Locally

```bash
docker run -p 8080:8080 email-verifier
```

Test the container:
```bash
curl http://localhost:8080/health
```

## Google Cloud Run Deployment

### Prerequisites
- Google Cloud account
- `gcloud` CLI installed and configured

### Deployment Steps

1. **Set your project ID:**
```bash
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID
```

2. **Enable required APIs:**
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

3. **Build and deploy to Cloud Run:**
```bash
gcloud run deploy email-verifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

4. **Get the service URL:**
```bash
gcloud run services describe email-verifier \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

### Alternative: Using Docker with Cloud Run

1. **Build and push to Google Container Registry:**
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/email-verifier
```

2. **Deploy from Container Registry:**
```bash
gcloud run deploy email-verifier \
  --image gcr.io/$PROJECT_ID/email-verifier \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Usage Examples

### Using cURL

```bash
# Verify a valid email
curl -X POST http://localhost:8080/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "test@gmail.com"}'

# Check health
curl http://localhost:8080/health
```

### Using Python

```python
import requests

url = "http://localhost:8080/verify"
data = {"email": "test@example.com"}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (fetch)

```javascript
fetch('http://localhost:8080/verify', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ email: 'test@example.com' })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Project Structure

```
emailchecker/
├── app.py                 # Main Flask application
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── test_app.py           # Test suite
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore file
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Environment Variables

- `PORT`: Server port (default: 8080)

## Technology Stack

- **Framework**: Flask 3.0.0
- **DNS Resolution**: dnspython 2.4.2
- **CORS Support**: flask-cors 4.0.0
- **Production Server**: Gunicorn 21.2.0
- **Testing**: pytest 7.4.3

## Validation Logic

The email verifier performs three levels of validation:

1. **Syntax Check**: Validates email format using regex pattern
2. **Domain Verification**: Checks if the domain exists via DNS lookup
3. **MX Record Validation**: Verifies the domain has mail exchange servers configured

## Limitations

- Does not verify if the specific email address exists on the mail server
- Does not check for disposable email addresses
- Requires internet connectivity for DNS lookups
- MX record validation may fail for domains behind strict firewalls

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.