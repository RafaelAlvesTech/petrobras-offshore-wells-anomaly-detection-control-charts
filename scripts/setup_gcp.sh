#!/bin/bash

# Google Cloud Platform Setup Script for Petrobras Offshore Wells Anomaly Detection
# This script automates the setup of GCP resources needed for model training

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if user is authenticated with gcloud
check_gcloud_auth() {
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Not authenticated with gcloud. Please run 'gcloud auth login' first."
        exit 1
    fi
}

# Function to check if project is set
check_project_set() {
    if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
        print_error "GOOGLE_CLOUD_PROJECT environment variable is not set."
        print_error "Please set it to your Google Cloud project ID."
        exit 1
    fi
}

# Function to check if region is set
check_region_set() {
    if [ -z "$GOOGLE_CLOUD_REGION" ]; then
        print_error "GOOGLE_CLOUD_REGION environment variable is not set."
        print_error "Please set it to your desired region (e.g., us-central1)."
        exit 1
    fi
}

# Function to check if bucket name is set
check_bucket_set() {
    if [ -z "$GCS_BUCKET_NAME" ]; then
        print_error "GCS_BUCKET_NAME environment variable is not set."
        print_error "Please set it to your desired Cloud Storage bucket name."
        exit 1
    fi
}

# Function to enable required APIs
enable_apis() {
    print_status "Enabling required Google Cloud APIs..."

    local apis=(
        "aiplatform.googleapis.com"
        "ml.googleapis.com"
        "storage.googleapis.com"
        "logging.googleapis.com"
        "monitoring.googleapis.com"
        "compute.googleapis.com"
        "cloudbuild.googleapis.com"
        "containerregistry.googleapis.com"
        "iam.googleapis.com"
    )

    for api in "${apis[@]}"; do
        if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
            print_status "API $api is already enabled."
        else
            print_status "Enabling API $api..."
            gcloud services enable "$api" --project="$GOOGLE_CLOUD_PROJECT"
            print_success "API $api enabled successfully."
        fi
    done
}

# Function to create Cloud Storage bucket
create_storage_bucket() {
    print_status "Creating Cloud Storage bucket..."

    if gsutil ls -b "gs://$GCS_BUCKET_NAME" >/dev/null 2>&1; then
        print_status "Bucket gs://$GCS_BUCKET_NAME already exists."
    else
        print_status "Creating bucket gs://$GCS_BUCKET_NAME in region $GOOGLE_CLOUD_REGION..."
        gsutil mb -p "$GOOGLE_CLOUD_PROJECT" -c STANDARD -l "$GOOGLE_CLOUD_REGION" "gs://$GCS_BUCKET_NAME"
        print_success "Bucket gs://$GCS_BUCKET_NAME created successfully."
    fi

    # Create folder structure
    print_status "Creating folder structure in bucket..."
    local folders=(
        "data/"
        "models/"
        "experiments/"
        "logs/"
        "checkpoints/"
        "mlflow-artifacts/"
        "training_scripts/"
    )

    for folder in "${folders[@]}"; do
        gsutil cp /dev/null "gs://$GCS_BUCKET_NAME/$folder" || true
        print_status "Created folder: $folder"
    done
}

# Function to create service account
create_service_account() {
    print_status "Creating service account for ML training..."

    local sa_name="anomaly-detection-training"
    local sa_email="$sa_name@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com"

    if gcloud iam service-accounts describe "$sa_email" --project="$GOOGLE_CLOUD_PROJECT" >/dev/null 2>&1; then
        print_status "Service account $sa_email already exists."
    else
        print_status "Creating service account $sa_email..."
        gcloud iam service-accounts create "$sa_name" \
            --display-name="Anomaly Detection Training Service Account" \
            --description="Service account for training anomaly detection models" \
            --project="$GOOGLE_CLOUD_PROJECT"
        print_success "Service account created successfully."
    fi

    # Grant necessary roles
    print_status "Granting necessary IAM roles..."
    local roles=(
        "roles/aiplatform.admin"
        "roles/storage.admin"
        "roles/logging.admin"
        "roles/monitoring.admin"
        "roles/compute.admin"
        "roles/iam.serviceAccountUser"
    )

    for role in "${roles[@]}"; do
        print_status "Granting role $role..."
        gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
            --member="serviceAccount:$sa_email" \
            --role="$role" \
            --quiet || print_warning "Failed to grant role $role (may already be granted)"
    done

    # Create and download service account key
    print_status "Creating service account key..."
    local key_file="service-account-key.json"

    if [ -f "$key_file" ]; then
        print_warning "Service account key file $key_file already exists."
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm "$key_file"
        else
            print_status "Using existing service account key file."
            return
        fi
    fi

    gcloud iam service-accounts keys create "$key_file" \
        --iam-account="$sa_email" \
        --project="$GOOGLE_CLOUD_PROJECT"

    print_success "Service account key created: $key_file"
    print_warning "Keep this file secure and do not commit it to version control!"
}

# Function to setup MLflow server (optional)
setup_mlflow_server() {
    print_status "Setting up MLflow server..."

    read -p "Do you want to setup MLflow server on Cloud Run? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setting up MLflow server on Cloud Run..."

        # Enable Cloud Run API
        gcloud services enable run.googleapis.com --project="$GOOGLE_CLOUD_PROJECT"

        # Create MLflow Docker image
        local image_name="gcr.io/$GOOGLE_CLOUD_PROJECT/mlflow-server"

        print_status "Building MLflow Docker image..."
        docker build -t "$image_name" -f docker/mlflow.Dockerfile .

        print_status "Pushing image to Container Registry..."
        docker push "$image_name"

        # Deploy to Cloud Run
        print_status "Deploying MLflow server to Cloud Run..."
        gcloud run deploy mlflow-server \
            --image="$image_name" \
            --platform=managed \
            --region="$GOOGLE_CLOUD_REGION" \
            --project="$GOOGLE_CLOUD_PROJECT" \
            --allow-unauthenticated \
            --port=5000 \
            --memory=2Gi \
            --cpu=1 \
            --set-env-vars="MLFLOW_TRACKING_URI=http://localhost:5000" \
            --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT" \
            --set-env-vars="GCS_BUCKET_NAME=$GCS_BUCKET_NAME"

        local mlflow_url=$(gcloud run services describe mlflow-server \
            --platform=managed \
            --region="$GOOGLE_CLOUD_REGION" \
            --project="$GOOGLE_CLOUD_PROJECT" \
            --format="value(status.url)")

        print_success "MLflow server deployed: $mlflow_url"
        print_status "Update your MLFLOW_TRACKING_URI to: $mlflow_url"
    fi
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment file..."

    local env_file=".env"

    if [ -f "$env_file" ]; then
        print_warning "Environment file $env_file already exists."
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm "$env_file"
        else
            print_status "Using existing environment file."
            return
        fi
    fi

    cat > "$env_file" << EOF
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT
GOOGLE_CLOUD_REGION=$GOOGLE_CLOUD_REGION
GOOGLE_CLOUD_ZONE=${GOOGLE_CLOUD_REGION}-a

# Vertex AI Configuration
VERTEX_AI_LOCATION=$GOOGLE_CLOUD_REGION
VERTEX_AI_EXPERIMENT_NAME=petrobras-anomaly-detection
VERTEX_AI_MODEL_DISPLAY_NAME=anomaly-detection-model

# Cloud Storage
GCS_BUCKET_NAME=$GCS_BUCKET_NAME
GCS_MODEL_PATH=gs://$GCS_BUCKET_NAME/models
GCS_DATA_PATH=gs://$GCS_BUCKET_NAME/data

# AI Platform Training
AI_PLATFORM_TRAINING_REGION=$GOOGLE_CLOUD_REGION
AI_PLATFORM_TRAINING_SCALE_TIER=BASIC_GPU
AI_PLATFORM_TRAINING_MASTER_TYPE=n1-standard-4
AI_PLATFORM_TRAINING_WORKER_TYPE=n1-standard-4
AI_PLATFORM_TRAINING_WORKER_COUNT=2

# Authentication
GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=petrobras-anomaly-detection

# Model Configuration
MODEL_BATCH_SIZE=32
MODEL_LEARNING_RATE=0.001
MODEL_EPOCHS=100
MODEL_VALIDATION_SPLIT=0.2

# Logging
LOG_LEVEL=INFO
ENABLE_TENSORBOARD=true
ENABLE_MLFLOW=true
EOF

    print_success "Environment file created: $env_file"
}

# Function to test setup
test_setup() {
    print_status "Testing GCP setup..."

    # Test authentication
    print_status "Testing authentication..."
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_success "Authentication working."
    else
        print_error "Authentication failed."
        return 1
    fi

    # Test project access
    print_status "Testing project access..."
    if gcloud projects describe "$GOOGLE_CLOUD_PROJECT" >/dev/null 2>&1; then
        print_success "Project access working."
    else
        print_error "Project access failed."
        return 1
    fi

    # Test bucket access
    print_status "Testing bucket access..."
    if gsutil ls "gs://$GCS_BUCKET_NAME" >/dev/null 2>&1; then
        print_success "Bucket access working."
    else
        print_error "Bucket access failed."
        return 1
    fi

    # Test Vertex AI access
    print_status "Testing Vertex AI access..."
    if gcloud ai operations list --region="$GOOGLE_CLOUD_REGION" --limit=1 >/dev/null 2>&1; then
        print_success "Vertex AI access working."
    else
        print_error "Vertex AI access failed."
        return 1
    fi

    print_success "All tests passed! GCP setup is working correctly."
}

# Main function
main() {
    print_status "Starting Google Cloud Platform setup for anomaly detection training..."

    # Check prerequisites
    if ! command_exists gcloud; then
        print_error "gcloud CLI is not installed. Please install it first:"
        print_error "https://cloud.google.com/sdk/docs/install"
        exit 1
    fi

    if ! command_exists gsutil; then
        print_error "gsutil is not installed. Please install Google Cloud SDK first."
        exit 1
    fi

    if ! command_exists docker; then
        print_warning "Docker is not installed. Some features may not work."
    fi

    # Check authentication and configuration
    check_gcloud_auth
    check_project_set
    check_region_set
    check_bucket_set

    print_status "Using project: $GOOGLE_CLOUD_PROJECT"
    print_status "Using region: $GOOGLE_CLOUD_REGION"
    print_status "Using bucket: $GCS_BUCKET_NAME"

    # Confirm setup
    echo
    read -p "Do you want to proceed with the setup? (y/N): " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setup cancelled."
        exit 0
    fi

    # Execute setup steps
    enable_apis
    create_storage_bucket
    create_service_account
    setup_mlflow_server
    create_env_file

    # Test setup
    test_setup

    print_success "Google Cloud Platform setup completed successfully!"
    echo
    print_status "Next steps:"
    print_status "1. Update your .env file with any custom values"
    print_status "2. Keep your service-account-key.json secure"
    print_status "3. Run 'uv sync' to install dependencies"
    print_status "4. Test with: python examples/train_lstm_vae_gcp.py --help"
    echo
    print_status "Happy training! 🚀"
}

# Check if script is sourced or run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
