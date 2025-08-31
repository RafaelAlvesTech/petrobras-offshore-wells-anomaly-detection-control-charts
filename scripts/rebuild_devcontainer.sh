#!/bin/bash
set -e

echo "🔄 Rebuilding Petrobras Offshore Wells Anomaly Detection devcontainer..."

# Check if we're in the right directory
if [ ! -f ".devcontainer/devcontainer.json" ]; then
    echo "❌ Error: .devcontainer/devcontainer.json not found. Please run this script from the project root."
    exit 1
fi

# Stop and remove existing containers
echo "🛑 Stopping existing devcontainer..."
docker stop $(docker ps -q --filter "label=devcontainer.local_folder=/home/rafael/petrobras-offshore-wells-anomaly-detection-control-charts") 2>/dev/null || true

# Remove existing devcontainer images
echo "🗑️  Removing existing devcontainer images..."
docker rmi $(docker images -q --filter "label=devcontainer.local_folder=/home/rafael/petrobras-offshore-wells-anomaly-detection-control-charts") 2>/dev/null || true

# Clean up Docker system
echo "🧹 Cleaning up Docker system..."
docker system prune -f

# Rebuild devcontainer
echo "🔨 Rebuilding devcontainer..."
echo "This may take several minutes..."

# Use devcontainer CLI if available, otherwise provide instructions
if command -v devcontainer &> /dev/null; then
    devcontainer up --workspace-folder . --remove-existing-container
else
    echo "⚠️  devcontainer CLI not found. Please use VS Code/Cursor to rebuild the devcontainer:"
    echo "   1. Open Command Palette (Ctrl+Shift+P)"
    echo "   2. Run 'Dev Containers: Rebuild Container'"
    echo "   3. Or run 'Dev Containers: Rebuild and Reopen in Container'"
fi

echo "✅ Devcontainer rebuild complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Open the project in VS Code/Cursor"
echo "   2. Reopen in devcontainer if not already done"
echo "   3. Run the test script: bash .devcontainer/test_setup.sh"
echo "   4. Check the logs for any remaining issues"
echo ""
