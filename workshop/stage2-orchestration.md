# Stage 2: Chaos Engineering & Agent Orchestration

**Time:** 60 minutes
**Goal:** Understand how skills activate agents and observe agent orchestration patterns in action

## Learning Objectives

- **Observe** how Claude automatically activates skills and spawns agents
- **Identify** when agents run in parallel vs. sequentially
- **Understand** agent coordination patterns through live examples
- Learn to spot agent activation in the CLI and read agent indicators
- (Optional: Fix bugs found during chaos testing)

## Overview

**This stage is about observation, not implementation.** You'll run an existing `/chaos-test` skill and focus on:

1. **Watching how skills activate**: See Claude automatically load the skill when invoked
2. **Identifying agent spawns**: Notice when Claude creates subagents in the CLI
3. **Understanding orchestration**: Observe which agents run in parallel vs. sequentially
4. **Reading agent indicators**: Learn to spot agent activity in the interface

The `/chaos-test` skill:
- Injects failures into your application
- Generates load to trigger issues
- Analyzes failure patterns
- Proposes specific fixes

**Why this uses subagents:** This skill has four distinct phases. Some can run independently (parallel) while others depend on previous results (sequential). Using subagents lets us run work in parallel for speed, and keeps each phase focused on one job.

**What you'll do:**
- Run `/chaos-test` and observe the orchestration
- Identify when each agent starts/completes
- Note which agents run in parallel
- (Optional) Fix bugs found by chaos testing

## What You're Building

A comprehensive chaos testing skill that:
1. Finds where your system breaks under stress
2. Identifies patterns in failures
3. Recommends specific code changes
4. Helps you build more resilient systems

From the user's perspective: `/chaos-test` → detailed report with fixes

Internally: Claude delegates to subagents with mixed parallel + sequential execution.

## Create the Chaos Testing Skill

### 1. Set Up the Skill

```bash
mkdir -p ~/.claude/skills/chaos-test
cd ~/.claude/skills/chaos-test
```

Create `SKILL.md`:

```markdown
---
name: chaos-test
description: Tests system resilience by injecting failures and analyzing patterns. Use proactively when testing system reliability or before deployments.
---

You are a chaos engineering specialist. Test system resilience by injecting failures, generating load, analyzing patterns, and proposing fixes.

PHASE 1: PARALLEL SETUP (Run simultaneously for speed)

Request that Claude spawn two subagents in parallel:

Subagent 1 (Chaos Injector) - Background:
"Modify the application to inject random failures:
- Add random delays: time.sleep(random.uniform(0.1, 2))
- Add random exceptions: raise Exception('Chaos!') with 10% probability
- Document injection points in chaos-config.json"

Subagent 2 (Load Generator) - Background:
"Generate load against the API:
- 50 requests to /api/search (POST with sample search data)
- 50 requests to /api/bookings (POST creating bookings)
- Log all results (response time, status, errors) to load-results.json"

WHY PARALLEL: These tasks are independent. Running them together is faster.
WHY BACKGROUND: They take time. We don't want to wait.

PHASE 2: WAIT FOR DATA
Use /tasks to check when load-results.json has sufficient data (100+ entries) or 60 seconds elapsed.

PHASE 3: ANALYSIS (Sequential - needs Phase 2 data)

Request a subagent for analysis:
"Read load-results.json and analyze:
- Which endpoints failed most frequently?
- What are the error rates and latency percentiles (p95, p99)?
- Correlate failures with chaos-config.json to identify root causes
Write analysis to failure-patterns.json"

WHY SEQUENTIAL: Needs data from Phase 1.
WHY SUBAGENT: Fresh context focused purely on data analysis.

PHASE 4: FIXES (Sequential - needs Phase 3 analysis)

Request a subagent for fix proposals:
"Read failure-patterns.json and propose specific code fixes:
- For each pattern, suggest concrete changes (file, line, what to change, why)
- Prioritize by impact (highest error rate first)
Write proposals to fix-proposals.json"

WHY SEQUENTIAL: Needs analysis from Phase 3.
WHY SUBAGENT: Fresh context focused on fix generation.

PHASE 5: REPORT
Read all JSON files and create chaos-test-report.md:
- Chaos configuration summary
- Load testing results (requests, success rate, latencies)
- Failure patterns identified
- Prioritized fix proposals
- Top 3 most critical issues

IMPLEMENTATION NOTES:
- Ask Claude to spawn both subagents for phases 1 & 2 in parallel
- Request background execution for long-running tasks
- Use /tasks to monitor progress
- Only request Phase 3 subagent after sufficient data collected
- Only request Phase 4 subagent after Phase 3 completes
- If timeout, proceed with partial data (graceful degradation)

The user just sees: /chaos-test → comprehensive report
Claude delegates to subagents to make it fast and efficient internally.
```

### 3. Prepare the Environment

Start the FastAPI application:

```bash
cd /path/to/orbital-travel-planner
python -m uvicorn app.main:app --reload
```

Verify endpoints respond:

```bash
curl http://localhost:8000/api/search -X POST -H "Content-Type: application/json" -d '{"origin": "Earth", "destination": "Mars", "depart_date": "2026-06-01"}'
curl http://localhost:8000/healthz
```

### 4. Run the Chaos Test (Focus on Observation)

```
/chaos-test
```

**👀 What to watch for:**

1. **Skill Activation**: Notice the skill loading indicator
2. **Agent Spawns**: Look for subagent creation messages in the CLI
3. **Parallel Execution**: Watch for multiple agents running simultaneously
   - Chaos injector and load generator should start together
4. **Sequential Execution**: Notice when agents wait for previous results
   - Analysis agent waits for load data
   - Fix proposal agent waits for analysis
5. **Agent Completion**: See when each agent returns results

**Observation Checklist:**
- [ ] Identified when `/chaos-test` skill activated
- [ ] Spotted the chaos injector agent starting
- [ ] Spotted the load generator agent starting
- [ ] Noticed these two agents ran in parallel (simultaneously)
- [ ] Saw when analysis agent started (after data collection)
- [ ] Saw when fix proposal agent started (after analysis)
- [ ] Understood why some agents were sequential

The skill takes several minutes. Use this time to observe the orchestration patterns.

### 5. Review the Report

```bash
cat chaos-test-report.md
```

Expected sections:
- **Chaos Configuration**: What failures were injected
- **Load Test Results**: Total requests, success rate, latencies
- **Failure Patterns**: Which endpoints failed, why, how often
- **Fix Proposals**: Ranked list of code changes with specifics

### 6. (Optional) Implement a Fix

**Note:** This step is optional. The goal of Stage 2 is understanding orchestration, not bug fixing.

If you want to practice fixing issues:

```
Based on chaos-test-report.md, implement the highest-priority fix
```

Ask Claude to:
1. Read the fix proposal
2. Find the relevant code
3. Apply the fix (add timeout, retry logic, error handling)
4. Show you what changed

### 7. (Optional) Verify the Fix

Re-run chaos testing only if you implemented fixes:

```
/chaos-test
```

Compare the new report to the previous one:
- Did error rates decrease?
- Are latencies more stable?
- Did the specific failure pattern disappear?

### What Just Happened?

**From your perspective:** You ran `/chaos-test` and got a detailed report with fixes.

**What you observed:**
- Skill activation when you typed `/chaos-test`
- Multiple agents spawning (visible in CLI)
- Parallel execution (chaos + load running simultaneously)
- Sequential execution (analysis waiting, then fix proposals)
- Agent completion indicators
- Final report aggregation

**Key insight:** You didn't build this skill—you observed how skills automatically orchestrate agents. This understanding helps you design your own skills in Stage 3.

**Why this design works:**
- Chaos injection and load generation are independent → run in parallel
- Pattern analysis needs load data → wait and run sequentially
- Fix proposals need pattern analysis → wait and run sequentially
- Each phase gets fresh, focused context
- Can use cheaper models for focused tasks

## Understanding Subagent Coordination

### Parallel Execution (Subagents 1 & 2)

**Key pattern:**
Ask Claude to spawn both subagents in the same request:
```
In parallel:
1. Spawn a subagent to inject chaos...
2. Spawn a subagent to generate load...
```

**Why parallel?**
- Tasks are completely independent
- Both take significant time
- No coordination needed
- Results don't depend on each other
- 2x faster than sequential

### Sequential Execution (Subagents 3 & 4)

**Key pattern:**
Request subagents one at a time based on data availability:
```
Wait for load-results.json, then:
→ Request analysis subagent

Wait for failure-patterns.json, then:
→ Request fix proposal subagent
```

**Why sequential?**
- Analysis subagent needs load data
- Fix proposal subagent needs analysis
- Natural dependencies in workflow
- Order matters for correctness

### Data Passing Between Subagents

Subagents communicate through **structured JSON files**:
- `chaos-config.json` - What failures were injected
- `load-results.json` - API call results
- `failure-patterns.json` - Analysis of failures
- `fix-proposals.json` - Suggested code changes

**Why JSON?**
- Clear, parseable structure
- Easy for subagents to read and write
- Schema enforces consistency
- Machine-readable for other tools

## Verification

**Observation Skills (Primary Goals):**
- [ ] Identified when `/chaos-test` skill activated
- [ ] Spotted multiple agents spawning in the CLI
- [ ] Recognized parallel execution (chaos + load together)
- [ ] Recognized sequential execution (analysis → fix proposals)
- [ ] Understand why subagents 1 & 2 run in parallel
- [ ] Understand why subagents 3 & 4 run sequentially
- [ ] Can explain orchestration pattern to someone else

**Optional (if you fixed bugs):**
- [ ] Report identifies real failure patterns
- [ ] Fix proposals are specific and actionable
- [ ] Re-running after fixes shows improvement

## Troubleshooting

**Subagents run one at a time instead of parallel:**
- Ask Claude to spawn both in the same request: "In parallel, spawn..."
- Request background execution explicitly
- Check that the skill prompts for parallel execution in the instructions

**Background tasks never finish:**
- Add timeout check (60 seconds max)
- Proceed with partial data if needed
- Use /tasks to monitor progress

**Not enough data collected:**
- Increase request count in load generator (try 100-200 requests)
- Lower the data threshold
- Increase polling timeout

**Can't identify failure patterns:**
- Increase chaos injection probability (try 20-30%)
- Verify chaos-config.json is being used
- Check that failures were actually injected

**Application crashes during chaos testing:**
- Good! That's what chaos testing finds
- Reduce failure injection rate
- Add graceful error handling first

## Deep Dive: Why Use Subagents?

### Option 1: Do Everything Directly (No Subagents)

```text
1. Inject chaos
2. Generate load
3. Analyze patterns
4. Propose fixes
5. Write report
```

**Problems:**
- Context grows massive (all code + all data + all analysis)
- Can't parallelize anything (all sequential)
- Single point of failure
- Expensive to run (one large context)

### Option 2: Use Subagents (Current Approach)

```text
1. Subagent 1 (inject) || Subagent 2 (load) [PARALLEL]
2. Wait for data
3. Subagent 3 (analyze) [SEQUENTIAL]
4. Subagent 4 (propose fixes) [SEQUENTIAL]
5. Main skill: aggregate report
```

**Benefits:**
- Each subagent has focused context
- Parallel execution where possible (2x faster)
- Can use cheaper models for focused tasks
- Isolated failures (one subagent fails, others proceed)
- Easier to debug (check each phase independently)

## Stage 2 Summary

You **observed** `/chaos-test` - a powerful resilience testing skill that:
- Demonstrates parallel agent execution (chaos + load)
- Demonstrates sequential agent execution (analysis → fixes)
- Shows how skills automatically orchestrate complex workflows
- Teaches pattern recognition for agent coordination

### Key Insights

**Skills vs. Subagents (What You Observed):**
- Users invoke skills (`/chaos-test`)
- Skills automatically instruct Claude to spawn subagents
- You can identify agent activity in the CLI
- Understanding orchestration helps you design better skills

**When parallel execution helps:**
- Tasks are independent
- Both take significant time
- No coordination needed
- Results don't depend on each other

**When sequential execution is needed:**
- Task B needs output from Task A
- Natural dependencies in the workflow
- Order matters for correctness

**Graceful degradation:**
- Set timeouts on long-running tasks
- Proceed with partial data when needed
- Report what worked and what didn't

### Knowledge Check

1. How do you identify when a skill has activated in the CLI?
2. How can you tell when Claude spawns a subagent?
3. What visual indicators show agents running in parallel?
4. Why do chaos injection and load generation run in parallel?
5. Why does pattern analysis wait for load generation?
6. How can you tell when an agent has completed its work?
7. What patterns would you use in your own skills after observing this?

### Advanced Exercises (Optional)

**Enhanced Chaos:**
Add more failure types (database timeouts, memory pressure, network issues).

**Real-Time Monitoring:**
Add instructions for a monitoring subagent that watches logs in real-time and alerts on anomalies.

**Gradual Ramp:**
Gradually increase failure rates (5% → 10% → 20%) and track when the system breaks.

**Comparative Testing:**
Run chaos testing on two different branches and compare results.

**Multi-Service Testing:**
Extend to test multiple services and analyze cross-service failure cascades.

---

**Next:** [Stage 3: Daily Workflow Skills](./stage3-workflow-skills.md)
