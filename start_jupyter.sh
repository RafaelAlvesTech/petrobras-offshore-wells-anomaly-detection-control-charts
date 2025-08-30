#!/bin/bash
echo "🚀 Starting Jupyter Notebook for Petrobras project..."
cd "$(dirname "$0")/notebooks"
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
