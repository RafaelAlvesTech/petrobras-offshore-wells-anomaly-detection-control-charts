# Use an official lightweight Python image.
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install uv, the package manager
RUN pip install uv

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
# Use --no-dev to avoid installing development-only packages
RUN uv sync --no-dev

# Copy the rest of the application source code
COPY . .
