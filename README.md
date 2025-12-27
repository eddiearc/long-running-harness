# Long-Running Harness

A Claude Code skill for maintaining continuity across multiple context windows in long-running software projects.

Based on Anthropic's research: [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

## Problem

When AI agents work on complex projects spanning multiple sessions, each new session starts with no memory of what came before. This leads to:

- **One-shotting**: Attempting to build everything at once, exhausting context mid-implementation
- **Premature completion**: Declaring the project done when features are still incomplete
- **Lost progress**: Having to guess what happened in previous sessions

## Solution

This skill implements a two-phase development approach:

### Phase 1: Initializer

Sets up the project environment on the first run:

- `long_running/<feature-name>/feature_list.json` - Comprehensive feature requirements in JSON format
- `long_running/<feature-name>/progress.txt` - Session work log for tracking progress
- `long_running/<feature-name>/init.sh` - Development environment startup script
- Git repository with initial commit

### Phase 2: Coding Agent

Every subsequent session follows this workflow:

1. **Orient** - Read long_running/<feature-name>/progress.txt and git log
2. **Select** - Choose ONE incomplete feature from long_running/<feature-name>/feature_list.json
3. **Implement** - Make focused, incremental changes (execute concrete tasks via `claude --print` in bash)
4. **Verify** - Test the feature actually works
5. **Document** - Commit changes and update long_running/<feature-name>/progress.txt

## Installation

Copy the `long-running-harness` folder to your Claude Code skills directory:

```bash
cp -r long-running-harness ~/.claude/skills/
```

Or clone directly:

```bash
git clone https://github.com/eddiearc/long-running-harness.git ~/.claude/skills/long-running-harness
```

## Usage

### Initialize a New Project

```bash
python ~/.claude/skills/long-running-harness/scripts/init_harness.py /path/to/project <feature-name> "Project description"
```

Or let Claude handle it - the skill activates automatically when you:

- Start a complex project expected to require multiple sessions
- Mention "long-term project", "cross-session", or "continuous development"
- Request project tracking or progress management

### Continue Working

In subsequent sessions, Claude will automatically:

1. Read long_running/<feature-name>/progress.txt and git history
2. Review long_running/<feature-name>/feature_list.json for next task
3. Run long_running/<feature-name>/init.sh to start the development environment
4. Work on one feature at a time
5. Update tracking files before ending

## Files

```
long-running-harness/
├── SKILL.md                              # Main skill instructions
├── scripts/
│   └── init_harness.py                   # Project initialization script
└── references/
    ├── feature_list_template.json        # Feature list template
    ├── progress_template.txt             # Progress file template
    └── init_sh_template.sh               # Init script template
```

## Key Principles

1. **Incremental Progress** - Work on exactly ONE feature per cycle
2. **Clean State** - Leave codebase mergeable after each session
3. **Honest Verification** - Only mark features complete after actual testing
4. **Feature List Integrity** - Never remove or edit feature descriptions, only update `passes` status

## License

MIT
