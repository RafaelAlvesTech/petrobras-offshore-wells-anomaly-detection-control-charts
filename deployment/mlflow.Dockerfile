# MLflow Server Dockerfile for Google Cloud Run
# This image provides a lightweight MLflow server for experiment tracking

FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install uv for package management
RUN pip install uv

# Create a non-root user
RUN useradd --create-home --shell /bin/bash mlflow_user

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv pip install --no-cache --system -r requirements.txt

# Copy MLflow server configuration
COPY mlflow_server.py .

# Create MLflow data directory and set permissions
RUN mkdir -p /mlflow && chown -R mlflow_user:mlflow_user /mlflow

# Switch to non-root user
USER mlflow_user

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start MLflow server
CMD ["python", "mlflow_server.py"]
