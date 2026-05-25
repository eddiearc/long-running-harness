#!/usr/bin/env python3
"""
Initialize the long-running harness for a project.

Usage:
    python init_harness.py <project_path> <feature_name> <project_description>

This script creates:
    - long_running/<feature_name>/plan.md - Planner-owned scope and acceptance criteria
    - long_running/<feature_name>/feature_list.json - Feature tracking file
    - long_running/<feature_name>/progress.txt - Session progress log
    - long_running/<feature_name>/init.sh - Development environment startup script
    - long_running/<feature_name>/state.json - Harness state
    - long_running/<feature_name>/handoffs/ - Subagent handoff files
    - long_running/<feature_name>/prompts/ - Reusable subagent prompt files
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def create_feature_list(project_name: str, harness_dir: Path, description: str) -> None:
    """Create the initial feature_list.json file."""
    feature_list = {
        "project": {
            "name": project_name,
            "description": description,
            "created": datetime.now().isoformat(),
        },
        "features": [
            {
                "id": 1,
                "category": "setup",
                "description": "Project initialization and basic structure",
                "steps": [
                    "Create project directory structure",
                    "Initialize package management",
                    "Verify basic setup works"
                ],
                "priority": "high",
                "passes": False
            },
            {
                "id": 2,
                "category": "core",
                "description": "[TODO: Add core feature description]",
                "steps": [
                    "[TODO: Add verification step 1]",
                    "[TODO: Add verification step 2]"
                ],
                "priority": "high",
                "passes": False
            }
        ],
        "metadata": {
            "total_features": 2,
            "completed_features": 0,
            "last_updated": datetime.now().isoformat()
        }
    }

    output_path = harness_dir / "feature_list.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(feature_list, f, indent=2, ensure_ascii=False)

    print(f"✅ Created {output_path}")


def create_plan_file(harness_dir: Path, description: str) -> None:
    """Create the planner-owned plan.md file."""
    content = f"""# Planner Plan

## Problem Statement

{description}

## User-Facing Goal

## Selected Feature

No feature selected yet.

## Implementation Slice

## Acceptance Criteria

## Verification Commands

## Manual Checks

## Non-Goals

## Likely Files or Modules

## Notes for Subagents

"""

    output_path = harness_dir / "plan.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created {output_path}")


def create_progress_file(project_name: str, harness_dir: Path, description: str) -> None:
    """Create the initial progress.txt file."""
    content = f"""# Project Progress Log

## Project: {project_name}
**Description:** {description}
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Session: {datetime.now().strftime("%Y-%m-%d %H:%M")} (Initialization)

### What was done:
- Initialized project harness
- Created feature_list.json with initial feature requirements
- Created plan.md for planner-owned scope and acceptance criteria
- Created progress.txt for session tracking
- Created init.sh for environment setup
- Created state.json, handoffs/, and prompts/ for subagent coordination

### Current State:
- Project is ready for development
- Feature list needs to be expanded based on requirements
- Planner should select exactly one feature before delegating implementation

### Next Steps:
- Review and expand feature_list.json with all required features
- Fill plan.md with the selected feature, acceptance criteria, verification commands, and non-goals
- Implement the first feature from the list

---

## Notes for Future Sessions

When starting a new session:
1. Read this file to understand recent progress
2. Check git log for commit history
3. Review feature_list.json for next task
4. Run ./init.sh to start development environment
5. Pick ONE feature and update plan.md
6. Delegate implementation to a worker subagent when available
7. Delegate verification to an evaluator subagent
8. Update this file before ending session

"""

    output_path = harness_dir / "progress.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created {output_path}")


def create_state_file(project_name: str, feature_name: str, harness_dir: Path) -> None:
    """Create the initial state.json file."""
    now = datetime.now().isoformat()
    state = {
        "project": project_name,
        "feature_name": feature_name,
        "status": "planning",
        "selected_feature_id": None,
        "worker_agent": None,
        "evaluator_agent": None,
        "blocked_on": None,
        "updated_at": now,
    }

    output_path = harness_dir / "state.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✅ Created {output_path}")


def create_subagent_dirs(harness_dir: Path) -> None:
    """Create directories used for subagent coordination."""
    for dirname in ("handoffs", "prompts"):
        output_path = harness_dir / dirname
        output_path.mkdir(parents=True, exist_ok=True)
        keep_path = output_path / ".gitkeep"
        keep_path.write_text("", encoding="utf-8")
        print(f"✅ Created {output_path}")


def create_init_script(harness_dir: Path) -> None:
    """Create the init.sh startup script."""
    content = """#!/bin/bash
# Development Environment Initialization Script
# Run this at the start of each coding session

set -e

echo "🚀 Starting development environment..."

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Navigate to project root
cd "$PROJECT_ROOT"

# Check for common package managers and install dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
elif [ -f "requirements.txt" ]; then
    echo "🐍 Installing Python dependencies..."
    pip install -r requirements.txt
elif [ -f "Cargo.toml" ]; then
    echo "🦀 Building Rust project..."
    cargo build
elif [ -f "go.mod" ]; then
    echo "🐹 Installing Go dependencies..."
    go mod download
fi

# Start development server (customize based on your project)
# Uncomment and modify the appropriate line:

# Node.js
# npm run dev &

# Python Flask
# python app.py &

# Python Django
# python manage.py runserver &

# Go
# go run main.go &

echo "✅ Development environment ready!"
echo ""
echo "📋 Quick commands:"
echo "   - Planner plan:   cat $SCRIPT_DIR/plan.md"
echo "   - Check progress: cat $SCRIPT_DIR/progress.txt"
echo "   - View features:  cat $SCRIPT_DIR/feature_list.json"
echo "   - Harness state:  cat $SCRIPT_DIR/state.json"
echo "   - Git history:    git log --oneline -10"
"""

    output_path = harness_dir / "init.sh"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Make executable
    os.chmod(output_path, 0o755)

    print(f"✅ Created {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize long-running harness for a project"
    )
    parser.add_argument(
        "project_path",
        type=str,
        help="Path to the project directory"
    )
    parser.add_argument(
        "feature_name",
        type=str,
        help="Feature name for long_running/<feature_name> (use kebab-case)"
    )
    parser.add_argument(
        "description",
        type=str,
        help="Brief description of the project"
    )

    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    harness_dir = project_path / "long_running" / args.feature_name

    # Create project directory if it doesn't exist
    if not project_path.exists():
        project_path.mkdir(parents=True)
        print(f"📁 Created project directory: {project_path}")

    harness_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔧 Initializing harness for: {project_path.name}")
    print(f"   Description: {args.description}\n")

    # Create harness files
    create_plan_file(harness_dir, args.description)
    create_feature_list(project_path.name, harness_dir, args.description)
    create_progress_file(project_path.name, harness_dir, args.description)
    create_init_script(harness_dir)
    create_state_file(project_path.name, args.feature_name, harness_dir)
    create_subagent_dirs(harness_dir)

    print(f"\n✅ Harness initialization complete!")
    print(f"\nNext steps:")
    print(f"  1. cd {project_path}")
    print(f"  2. Edit long_running/{args.feature_name}/feature_list.json to add your features")
    print(f"  3. git init && git add . && git commit -m 'Initial setup'")
    print(f"  4. Start implementing features one at a time")


if __name__ == "__main__":
    main()
