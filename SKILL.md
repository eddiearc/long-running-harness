---
name: long-running-harness
description: This skill provides a framework for maintaining continuity across multiple context windows in long-running software projects. Activates when working on complex projects that span multiple sessions, when users mention "long-term project", "cross-session", "continuous development", or when setting up project tracking mechanisms. Based on Anthropic's research on effective harnesses for long-running agents.
---

# Long Running Harness

## Overview

This skill enables effective work across multiple context windows by implementing a two-phase development approach: an **Initializer Phase** that sets up the project environment, and a **Coding Phase** that ensures incremental progress with clear artifacts for subsequent sessions.

## When to Use

- Starting a complex project expected to require multiple sessions
- User requests project tracking or progress management
- Continuing work on an existing long-running project
- User mentions "long-term", "cross-session", or "persistent" development

## Core Components

| Component | Purpose |
|-----------|---------|
| `feature_list.json` | JSON-formatted feature requirements, each with `passes: true/false` |
| `progress.txt` | Session work log documenting what was done |
| `init.sh` | Script to start development environment |
| Git commits | Track changes with descriptive messages for history and rollback |

## Phase 1: Initializer Workflow

Execute this phase only on the **first session** of a new project.

### Steps

1. **Analyze Requirements**
   - Parse user's initial prompt for feature requirements
   - Expand into comprehensive feature list (aim for granular, testable features)

2. **Create Feature List**
   - Generate `feature_list.json` using template from `references/feature_list_template.json`
   - Each feature should have: category, description, verification steps, passes status
   - All features initially set to `"passes": false`

3. **Create Progress File**
   - Initialize `progress.txt` with project metadata and initial state
   - Use template from `references/progress_template.txt`

4. **Create Init Script**
   - Generate `init.sh` with commands to start development environment
   - Include dependency installation, server startup, environment setup
   - Use template from `references/init_sh_template.sh`

5. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial project setup with harness files"
   ```

## Phase 2: Coding Workflow

Execute this phase on **every subsequent session**.

### Session Start Sequence

1. **Orient**
   ```bash
   pwd
   ```
   Confirm working directory.

2. **Get Up to Speed**
   ```bash
   cat progress.txt
   git log --oneline -20
   ```
   Read recent progress and commit history.

3. **Review Features**
   Read `feature_list.json` and identify the highest-priority incomplete feature.

4. **Start Environment**
   ```bash
   ./init.sh
   ```
   Launch development server and verify basic functionality works.

5. **Verify Baseline**
   Run a quick sanity check to ensure the app is in a working state before making changes.

### Development Cycle

1. **Select ONE Feature**
   - Choose a single incomplete feature from `feature_list.json`
   - Never attempt to implement multiple features at once

2. **Implement**
   - Write code for the selected feature
   - Keep changes focused and minimal

3. **Verify**
   - Run project tests: `npm test`, `pytest`, or equivalent
   - Manually verify the feature works as expected
   - Only mark as complete after actual verification

4. **Update Feature List**
   - Change `"passes": false` to `"passes": true` only for verified features
   - Never remove or edit feature descriptions

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Implement: [feature description]"
   ```

6. **Update Progress**
   Append to `progress.txt`:
   ```
   ## Session: [date/time]
   - Implemented: [feature description]
   - Status: [working/issues]
   - Next: [suggested next feature]
   ```

### Session End Checklist

Before ending a session, ensure:
- [ ] Code compiles/runs without errors
- [ ] All tests pass
- [ ] Git commit made with descriptive message
- [ ] progress.txt updated with session summary
- [ ] No half-implemented features left undocumented

## Critical Rules

### Feature List Integrity
> It is unacceptable to remove or edit feature descriptions in feature_list.json. Only the `passes` field may be modified.

### Incremental Progress
> Work on exactly ONE feature per development cycle. Attempting to implement multiple features simultaneously leads to context exhaustion and incomplete work.

### Clean State
> Every session must leave the codebase in a state suitable for merging to main: no major bugs, orderly code, and documented progress.

### Honest Verification
> Never mark a feature as `"passes": true` without actual verification. Premature completion marking is a primary failure mode.

## Resources

### scripts/init_harness.py

Run this script to initialize the harness for a new project:

```bash
python scripts/init_harness.py /path/to/project "Project description"
```

The script creates all required files with proper templates.

### references/

- `feature_list_template.json` - Template for feature list structure
- `progress_template.txt` - Template for progress file
- `init_sh_template.sh` - Template for init script

## Troubleshooting

### App in Broken State
If `init.sh` reveals the app doesn't work:
1. Check `git log` for recent changes
2. Consider `git revert` to restore working state
3. Document the issue in progress.txt before fixing

### Context Running Low
If approaching context limit mid-feature:
1. Stop implementation immediately
2. Document current state in progress.txt
3. Commit partial progress with clear description
4. Mark feature as still incomplete
