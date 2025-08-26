FROM python:3.11-slim

# Set environment variables for uv and Python
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set the working directory
WORKDIR /app

# Install uv using the official installer
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency files
COPY requirements.txt .

# Install project dependencies using uv
RUN /root/.cargo/bin/uv pip install -r requirements.txt

# Copy the rest of the project code
COPY . .

# Expose the default Jupyter port
EXPOSE 8888

# Default command to run when the container starts
# Starts a Jupyter Notebook, accessible from outside the container.
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
