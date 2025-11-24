# Email Verifier - Quick Start Guide

Get started with the Email Verifier API in under 5 minutes!

## 🚀 Quick Local Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

Server starts at `http://localhost:8080`

### 3. Test It!

```bash
# Check health
curl http://localhost:8080/health

# Verify an email
curl -X POST http://localhost:8080/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "test@gmail.com"}'
```

## 🐳 Quick Docker Setup

```bash
# Build
docker build -t email-verifier .

# Run
docker run -p 8080:8080 email-verifier

# Test
curl http://localhost:8080/health
```

## ☁️ Quick Cloud Run Deployment

```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR-PROJECT-ID

# Deploy
gcloud run deploy email-verifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📝 API Usage Examples

### Python
```python
import requests

response = requests.post(
    'http://localhost:8080/verify',
    json={'email': 'test@example.com'}
)
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:8080/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "user@domain.com"}'
```

### JavaScript
```javascript
fetch('http://localhost:8080/verify', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'test@example.com'})
})
.then(r => r.json())
.then(console.log);
```

## 🧪 Run Tests

```bash
pip install -r requirements-dev.txt
pytest test_app.py -v
```

## 📚 More Information

- **README.md** - Complete documentation
- **DEPLOYMENT.md** - Detailed deployment guide
- **example_usage.py** - Working Python examples

## 🆘 Troubleshooting

**Port already in use?**
```bash
export PORT=8081
python app.py
```

**DNS lookups failing?**
- Check internet connectivity
- Some corporate firewalls block DNS queries

**Docker build fails?**
- Ensure Docker is running
- Check internet connection for pip packages

## 📦 What's Included

- ✅ Email syntax validation
- ✅ Domain verification
- ✅ MX record checking
- ✅ RESTful API
- ✅ CORS support
- ✅ Health checks
- ✅ Docker ready
- ✅ Cloud Run ready
- ✅ Full test suite

## 🔗 Next Steps

1. Read the full **README.md** for detailed API documentation
2. Review **DEPLOYMENT.md** for production deployment options
3. Run **example_usage.py** to see the API in action
4. Customize the code for your specific needs

Happy email verifying! 🎉
