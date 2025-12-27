#!/bin/bash
# Development Environment Initialization Script
# Customize this script for your project's needs

set -e

echo "🚀 Starting development environment..."

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Navigate to project root
cd "$PROJECT_ROOT"

# ============================================
# DEPENDENCY INSTALLATION
# Uncomment the section that matches your project
# ============================================

# --- Node.js ---
# if [ -f "package.json" ]; then
#     echo "📦 Installing Node.js dependencies..."
#     npm install
# fi

# --- Python ---
# if [ -f "requirements.txt" ]; then
#     echo "🐍 Installing Python dependencies..."
#     pip install -r requirements.txt
# fi

# --- Python (Poetry) ---
# if [ -f "pyproject.toml" ]; then
#     echo "🐍 Installing Python dependencies with Poetry..."
#     poetry install
# fi

# --- Rust ---
# if [ -f "Cargo.toml" ]; then
#     echo "🦀 Building Rust project..."
#     cargo build
# fi

# --- Go ---
# if [ -f "go.mod" ]; then
#     echo "🐹 Installing Go dependencies..."
#     go mod download
# fi

# ============================================
# DEVELOPMENT SERVER
# Uncomment and customize for your project
# ============================================

# --- Node.js (Next.js, Vite, etc.) ---
# echo "🌐 Starting development server..."
# npm run dev &

# --- Python Flask ---
# echo "🌐 Starting Flask server..."
# python app.py &

# --- Python Django ---
# echo "🌐 Starting Django server..."
# python manage.py runserver &

# --- Go ---
# echo "🌐 Starting Go server..."
# go run main.go &

# ============================================
# POST-STARTUP
# ============================================

echo "✅ Development environment ready!"
echo ""
echo "📋 Quick reference:"
echo "   - Progress log:   cat $SCRIPT_DIR/progress.txt"
echo "   - Feature list:   cat $SCRIPT_DIR/feature_list.json"
echo "   - Git history:    git log --oneline -10"
echo "   - Git status:     git status"
