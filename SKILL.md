---
name: long-running-harness
description: Use when users request long-term, cross-session, persistent, planner-led, subagent-coordinated, or Anthropic-style long-running coding work.
---

# Long Running Harness

## Overview

This skill enables effective work across multiple context windows by implementing a planner-led harness. The main agent plans and coordinates; implementation and verification can be delegated to two focused subagents.

## When to Use

- Starting a complex project expected to require multiple sessions
- User requests project tracking or progress management
- Continuing work on an existing long-running project
- User mentions "long-term", "cross-session", or "persistent" development

## Core Components

| Component | Purpose |
|-----------|---------|
| `long_running/<feature-name>/plan.md` | Planner-owned scope, acceptance criteria, and selected implementation slice |
| `long_running/<feature-name>/feature_list.json` | JSON-formatted feature requirements, each with `passes: true/false` |
| `long_running/<feature-name>/progress.txt` | Session work log documenting what was done |
| `long_running/<feature-name>/init.sh` | Script to start development environment |
| `long_running/<feature-name>/state.json` | Current phase, selected feature, subagent ids, and blocker state |
| `long_running/<feature-name>/handoffs/` | Implementation and verification handoffs between agents |
| `long_running/<feature-name>/prompts/` | Reusable worker/evaluator prompt files |
| Git commits | Track changes with descriptive messages for history and rollback |

## Agent Roles

- **Main agent: planner/conductor.** Owns requirements, selected feature, acceptance criteria, state transitions, and final completion decision.
- **Implementation subagent: worker.** Implements exactly one selected feature and writes `handoffs/implementation.md`.
- **Verification subagent: evaluator.** Tests that feature end to end and writes `handoffs/verification.md`.

The worker does not accept its own work. The evaluator does not implement fixes unless the main agent explicitly changes the workflow.

## Mandatory Planning Conversation Gate

Before editing application code, configuration, tests, or deployment files, stop at the planning stage and communicate with the user.

The main agent MUST first provide:

- A concise restatement of the user goal and boundaries
- The proposed feature list or the feature list updates to be written
- The selected implementation slice
- Acceptance criteria
- Verification commands and manual checks
- Non-goals
- A recommendation on whether subagents should be used

Then ask the user to confirm the plan before implementation starts. If the user does not confirm, do not edit source files.

The planning message MUST also ask:

> Do you want this executed with subagents?

Offer exactly these execution modes:

- **Use subagents:** one implementation worker and one verification evaluator; the main agent plans, integrates, and updates completion state only after evaluator approval.
- **Main-agent only:** the main agent implements and verifies, while still writing `handoffs/implementation.md` and `handoffs/verification.md`.

Default recommendation: small single-surface changes usually do not need subagents; complex, risky, cross-module, or long-running work should use subagents.

## Execution Mode Rule

Subagents are recommended, not mandatory. The user must explicitly choose the execution mode during the planning conversation.

If the user chooses subagents:

- Spawn one implementation worker when tools and policy allow it.
- Spawn one verification evaluator after implementation.
- The main agent alone updates `feature_list.json` after evaluator pass.
- If tools or policy prevent subagent use, stop and ask whether to continue main-agent only.

If the user chooses main-agent only:

- The main agent may implement the selected feature.
- The main agent must write `handoffs/implementation.md`.
- The main agent must run verification and write `handoffs/verification.md`.
- The main agent must not mark `passes: true` without command output, browser evidence, or equivalent concrete verification.

## Phase 1: Initializer Workflow

Execute this phase only on the **first session** of a new project.

### Steps

1. **Analyze Requirements**
   - Parse user's initial prompt for feature requirements
   - Expand into comprehensive feature list (aim for granular, testable features)

2. **Create Harness Folder**
   - Choose a `feature-name` in kebab-case (e.g., `login-flow`, `ipc-refactor`)
   - Create `long_running/<feature-name>/` at the project root

3. **Create Feature List**
   - Generate `long_running/<feature-name>/feature_list.json` using template from `references/feature_list_template.json`
   - Each feature should have: category, description, verification steps, passes status
   - All features initially set to `"passes": false`

4. **Create Planner Files**
   - Generate `long_running/<feature-name>/plan.md`
   - Generate `long_running/<feature-name>/state.json`
   - Create `long_running/<feature-name>/handoffs/`
   - Create `long_running/<feature-name>/prompts/`

5. **Create Progress File**
   - Initialize `long_running/<feature-name>/progress.txt` with project metadata and initial state
   - Use template from `references/progress_template.txt`

6. **Create Init Script**
   - Generate `long_running/<feature-name>/init.sh` with commands to start development environment
   - Include dependency installation, server startup, environment setup
   - Use template from `references/init_sh_template.sh`

7. **Ask for Plan Confirmation and Execution Mode**
   - Present the planning message required by the Mandatory Planning Conversation Gate
   - Ask the user to confirm the plan
   - Ask whether to use subagents or main-agent-only execution
   - Do not edit source files until the user confirms

8. **Initialize Git Repository**
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
   HARNESS_DIR="long_running/<feature-name>"
   cat "$HARNESS_DIR/progress.txt"
   git log --oneline -20
   ```
   Read recent progress and commit history.

3. **Review Features**
   Read `long_running/<feature-name>/feature_list.json` and identify the highest-priority incomplete feature.

4. **Start Environment**
   ```bash
   bash "$HARNESS_DIR/init.sh"
   ```
   Launch development server and verify basic functionality works.

5. **Verify Baseline**
   Run a quick sanity check to ensure the app is in a working state before making changes.

### Development Cycle

1. **Select ONE Feature**
   - Choose a single incomplete feature from `long_running/<feature-name>/feature_list.json`
   - Never attempt to implement multiple features at once
   - Update `plan.md` with the selected feature, scope, acceptance criteria, verification commands, manual checks, and non-goals
   - Ask the user to confirm the selected feature and choose the execution mode
   - Update `state.json` to `implementing` only after confirmation

2. **Implement According to Execution Mode**
   - If the user chose subagents, spawn one implementation subagent when tools and policy allow it
   - If using subagents, use `references/subagent_prompts.md` to create the worker prompt
   - If using subagents, give the worker a clear ownership scope and the selected feature
   - If using subagents, require the worker to write `handoffs/implementation.md`
   - If the user chose main-agent only, the main agent implements and writes `handoffs/implementation.md`
   - If subagents were requested but are unavailable, stop and ask whether to continue main-agent only

3. **Verify**
   - Update `state.json` to `verifying`
   - If the user chose subagents, spawn one evaluator subagent after the worker returns
   - If using subagents, use `references/subagent_prompts.md` to create the evaluator prompt
   - Run project tests: `npm test`, `pytest`, or equivalent
   - For web apps, use browser automation or realistic manual interaction when practical
   - If using subagents, require the evaluator to write `handoffs/verification.md`
   - If main-agent only, write `handoffs/verification.md` directly with command outputs and manual check results
   - Only mark as complete after actual verification

4. **Update Feature List**
   - Main agent changes `"passes": false` to `"passes": true` only for the verified selected feature
   - Never remove or edit feature descriptions

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Implement: [feature description]"
   ```

6. **Update Progress**
   Append to `long_running/<feature-name>/progress.txt`:
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
- [ ] long_running/<feature-name>/progress.txt updated with session summary
- [ ] No half-implemented features left undocumented

## Critical Rules

### Feature List Integrity
> It is unacceptable to remove or edit feature descriptions in long_running/<feature-name>/feature_list.json. Only the `passes` field may be modified.

### Incremental Progress
> Work on exactly ONE feature per development cycle. Attempting to implement multiple features simultaneously leads to context exhaustion and incomplete work.

### Clean State
> Every session must leave the codebase in a state suitable for merging to main: no major bugs, orderly code, and documented progress.

### Honest Verification
> Never mark a feature as `"passes": true` without actual verification. Premature completion marking is a primary failure mode.

### Subagent Availability
> Subagents are not mandatory. If the user chose subagents but built-in subagents are unavailable, the agent may offer `claude --print` as a fallback when practical, or ask whether to continue main-agent only. Document the final execution mode and reason in `progress.txt`.

### Subagent Separation
> The implementation subagent must not mark its own feature complete. The evaluator must not fix code while verifying. The main agent integrates both handoffs and owns the final decision.

## Resources

### scripts/init_harness.py

Run this script to initialize the harness for a new project:

```bash
python scripts/init_harness.py /path/to/project <feature-name> "Project description"
```

The script creates all required files with proper templates.

### references/

- `feature_list_template.json` - Template for feature list structure
- `progress_template.txt` - Template for progress file
- `init_sh_template.sh` - Template for init script
- `subagent_prompts.md` - Prompt templates for implementation and verification subagents

## Troubleshooting

### App in Broken State
If `init.sh` reveals the app doesn't work:
1. Check `git log` for recent changes
2. Consider `git revert` to restore working state
3. Document the issue in long_running/<feature-name>/progress.txt before fixing

### Context Running Low
If approaching context limit mid-feature:
1. Stop implementation immediately
2. Document current state in long_running/<feature-name>/progress.txt
3. Commit partial progress with clear description
4. Mark feature as still incomplete
