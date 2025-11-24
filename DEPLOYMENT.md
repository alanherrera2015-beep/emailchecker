# Email Verifier - Deployment Guide

This guide provides detailed instructions for deploying the Email Verifier backend to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account**: Create one at https://cloud.google.com/
2. **Google Cloud SDK**: Install `gcloud` CLI from https://cloud.google.com/sdk/docs/install
3. **Docker**: Install Docker Desktop from https://www.docker.com/products/docker-desktop

## Initial Setup

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Create a New Project (Optional)

```bash
# Create a new project
gcloud projects create YOUR-PROJECT-ID --name="Email Verifier"

# Set as default project
gcloud config set project YOUR-PROJECT-ID
```

Or use an existing project:

```bash
gcloud config set project YOUR-EXISTING-PROJECT-ID
```

### 3. Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud Build API (for building containers)
gcloud services enable cloudbuild.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com
```

### 4. Set Default Region (Optional)

```bash
gcloud config set run/region us-central1
```

## Deployment Methods

### Method 1: Direct Deployment from Source (Recommended)

This is the easiest method. Cloud Run will automatically build and deploy your application.

```bash
# Deploy directly from source code
gcloud run deploy email-verifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

**Parameters explained:**
- `--source .`: Build from the current directory
- `--platform managed`: Use fully managed Cloud Run
- `--region us-central1`: Deploy to US Central region
- `--allow-unauthenticated`: Allow public access (no authentication required)
- `--memory 512Mi`: Allocate 512MB of memory
- `--cpu 1`: Allocate 1 CPU
- `--max-instances 10`: Scale up to 10 instances maximum

### Method 2: Build and Deploy with Docker

If you prefer to build the Docker image yourself:

```bash
# Set your project ID
export PROJECT_ID=$(gcloud config get-value project)

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/email-verifier:latest .

# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker

# Push the image to Google Container Registry
docker push gcr.io/$PROJECT_ID/email-verifier:latest

# Deploy to Cloud Run
gcloud run deploy email-verifier \
  --image gcr.io/$PROJECT_ID/email-verifier:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Method 3: Using Cloud Build (CI/CD)

For automated deployments using Cloud Build:

```bash
# Submit build to Cloud Build
gcloud builds submit --config cloudbuild.yaml

# The cloudbuild.yaml file will automatically:
# 1. Build the Docker image
# 2. Push to Container Registry
# 3. Deploy to Cloud Run
```

## Post-Deployment

### Get Service URL

After deployment, get your service URL:

```bash
gcloud run services describe email-verifier \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

### Test the Deployment

```bash
# Get the service URL
export SERVICE_URL=$(gcloud run services describe email-verifier \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

# Test the health endpoint
curl $SERVICE_URL/health

# Test email verification
curl -X POST $SERVICE_URL/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "test@gmail.com"}'
```

## Monitoring and Logs

### View Logs

```bash
# Stream logs in real-time
gcloud run services logs tail email-verifier \
  --platform managed \
  --region us-central1

# View recent logs
gcloud run services logs read email-verifier \
  --platform managed \
  --region us-central1 \
  --limit 50
```

### Access Cloud Console

View detailed metrics and logs in the Cloud Console:
```
https://console.cloud.google.com/run
```

## Configuration Options

### Environment Variables

To add environment variables:

```bash
gcloud run services update email-verifier \
  --set-env-vars "KEY1=VALUE1,KEY2=VALUE2" \
  --region us-central1
```

### Memory and CPU

Adjust resources:

```bash
gcloud run services update email-verifier \
  --memory 1Gi \
  --cpu 2 \
  --region us-central1
```

### Scaling

Configure autoscaling:

```bash
gcloud run services update email-verifier \
  --min-instances 1 \
  --max-instances 100 \
  --region us-central1
```

### Request Timeout

Set maximum request processing time:

```bash
gcloud run services update email-verifier \
  --timeout 300 \
  --region us-central1
```

## Authentication (Optional)

To require authentication:

```bash
# Deploy with authentication required
gcloud run deploy email-verifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated

# Grant access to specific users
gcloud run services add-iam-policy-binding email-verifier \
  --member='user:user@example.com' \
  --role='roles/run.invoker' \
  --region us-central1
```

## Custom Domain

To use a custom domain:

```bash
# Map a custom domain
gcloud run domain-mappings create \
  --service email-verifier \
  --domain api.yourdomain.com \
  --region us-central1
```

Follow the instructions to verify domain ownership and configure DNS.

## Updating the Service

To update with new code:

```bash
# Simply run the deploy command again
gcloud run deploy email-verifier \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Cloud Run will automatically handle zero-downtime deployment.

## Deleting the Service

To delete the service:

```bash
gcloud run services delete email-verifier \
  --platform managed \
  --region us-central1
```

## Cost Optimization

Cloud Run pricing is based on:
- Request count
- Compute time (CPU and memory usage)
- Networking

Tips to reduce costs:
1. Set appropriate min/max instances
2. Use the smallest memory/CPU that meets your needs
3. Optimize application startup time
4. Set appropriate request timeout

Free tier includes:
- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds of compute time

## Troubleshooting

### View Service Details

```bash
gcloud run services describe email-verifier \
  --platform managed \
  --region us-central1
```

### Common Issues

1. **Container fails to start**: Check logs with `gcloud run services logs`
2. **Permission denied**: Ensure required APIs are enabled
3. **Build fails**: Check `cloudbuild.yaml` syntax and Dockerfile
4. **High latency**: Increase memory/CPU or adjust min-instances

### Get Support

- Cloud Run Documentation: https://cloud.google.com/run/docs
- Stack Overflow: Tag questions with `google-cloud-run`
- Cloud Console Support: https://console.cloud.google.com/support

## Best Practices

1. **Always test locally first** using Docker
2. **Use Cloud Build** for CI/CD pipelines
3. **Enable Cloud Logging** for debugging
4. **Set up Cloud Monitoring** for alerts
5. **Use secrets manager** for sensitive data
6. **Implement health checks** (already included)
7. **Set resource limits** to control costs
8. **Use custom domains** for production
9. **Enable HTTPS** (automatic with Cloud Run)
10. **Version your deployments** using tags

## GitHub Integration

### Continuous Deployment

Set up automatic deployment from GitHub:

1. Connect your GitHub repository in Cloud Build
2. Create a trigger that runs on push to main branch
3. Use the provided `cloudbuild.yaml` configuration

This enables automatic deployment whenever you push code to GitHub.

## Next Steps

1. Set up a custom domain
2. Configure Cloud Monitoring alerts
3. Implement rate limiting
4. Add authentication if needed
5. Set up a CDN for global distribution
6. Configure backup and disaster recovery

For more information, visit the [Cloud Run documentation](https://cloud.google.com/run/docs).
