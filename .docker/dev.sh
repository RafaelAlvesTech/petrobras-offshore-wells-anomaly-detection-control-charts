#!/bin/bash

# Petrobras Offshore Wells Anomaly Detection - Development Helper Script
# This script provides convenient commands for managing the devcontainer

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

# Function to show help
show_help() {
    echo "🛢️  Petrobras Offshore Wells Anomaly Detection - Dev Helper"
    echo "=========================================================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     - Build the Docker container"
    echo "  up        - Start the development environment"
    echo "  down      - Stop the development environment"
    echo "  restart   - Restart the development environment"
    echo "  logs      - Show container logs"
    echo "  shell     - Open a shell in the running container"
    echo "  jupyter   - Start Jupyter Lab"
    echo "  mlflow    - Start MLflow server"
    echo "  api       - Start API server"
    echo "  clean     - Clean up containers and images"
    echo "  status    - Show container status"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 up        # Start the environment"
    echo "  $0 jupyter   # Start Jupyter Lab"
    echo "  $0 shell     # Open shell in container"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose is not installed or not in PATH"
        exit 1
    fi
}

# Function to check if we're in the right directory
check_directory() {
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found. Please run this script from the .docker directory"
        exit 1
    fi
}

# Main script logic
main() {
    # Change to script directory
    cd "$(dirname "$0")"

    check_docker_compose
    check_directory

    case "${1:-help}" in
        build)
            print_status "Building Docker container..."
            docker-compose build --no-cache
            print_success "Container built successfully!"
            ;;
        up)
            print_status "Starting development environment..."
            docker-compose up -d
            print_success "Development environment started!"
            print_status "Services available at:"
            echo "  - API: http://localhost:8000"
            echo "  - Jupyter: http://localhost:8888"
            echo "  - MLflow: http://localhost:5000"
            ;;
        down)
            print_status "Stopping development environment..."
            docker-compose down
            print_success "Development environment stopped!"
            ;;
        restart)
            print_status "Restarting development environment..."
            docker-compose restart
            print_success "Development environment restarted!"
            ;;
        logs)
            print_status "Showing container logs..."
            docker-compose logs -f app
            ;;
        shell)
            print_status "Opening shell in container..."
            docker-compose exec app /bin/zsh
            ;;
        jupyter)
            print_status "Starting Jupyter Lab..."
            docker-compose exec app start_service jupyter
            ;;
        mlflow)
            print_status "Starting MLflow server..."
            docker-compose exec app start_service mlflow
            ;;
        api)
            print_status "Starting API server..."
            docker-compose exec app start_service api
            ;;
        clean)
            print_warning "This will remove all containers and images. Continue? (y/N)"
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                print_status "Cleaning up containers and images..."
                docker-compose down --rmi all --volumes --remove-orphans
                print_success "Cleanup completed!"
            else
                print_status "Cleanup cancelled."
            fi
            ;;
        status)
            print_status "Container status:"
            docker-compose ps
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
