# Advanced Claude Code Workshop: Meta-Programming & Skill Development

**Duration:** 10:30–16:00 (lunch 12:00–13:00)
**Audience:** Backend Python engineers familiar with Claude and LLM basics
**Focus:** Custom skills, agent orchestration, self-validation loops, MCP tooling, meta-programming

**Philosophy:** The orbital-travel-planner is a vehicle. The goal is to build reusable skills, validation harnesses, and agent coordination patterns you'll use daily after this workshop.

---

## Stage 1: Meta-Programming Foundation
**Time:** 10:30–11:15 (45 min)

**Goal:** Understand how Claude Code's skill system works and create your first custom skill that orchestrates multiple agents.

**Tasks:**
- Explore the Claude Code skill architecture: where skills live, how they're invoked, how they compose
- Create a custom skill `/validate-api` that:
  - Spawns an Explore agent to find all API endpoints in the codebase
  - Spawns a Plan agent to design a validation strategy
  - Generates test cases for each endpoint
  - Creates an MCP server that validates responses against OpenAPI schemas
- Make the skill reusable: it should work on any FastAPI project, not just this one
- Have the skill write its findings to a structured report that can be consumed by other agents

**Success criteria:**
- You can invoke `/validate-api` and it autonomously discovers, plans, and validates endpoints
- The skill demonstrates agent-to-agent handoff (Explore → Plan → Execute)
- You understand the skill manifest format and can explain how skills compose
- You have a working MCP server that validates API responses

**Hints:**
- Skills are just structured prompts + tool permissions—study existing skills first
- The skill should use `Task` tool to spawn specialized agents, not do everything inline
- Consider: how does the Explore agent communicate findings to the Plan agent?
- Look at MCP server examples for request/response validation patterns

---

## Stage 2: Self-Validating Systems
**Time:** 11:15–12:00 (45 min)

**Goal:** Build verification loops where Claude validates its own work using external tools and MCP servers.

**Tasks:**
- Create an MCP server that wraps Postman/Newman or similar API testing tool
- The MCP server should:
  - Accept endpoint definitions and expected responses
  - Execute actual HTTP requests against running services
  - Return structured pass/fail results with diffs
- Create a skill `/implement-verified` that:
  - Takes a feature description (e.g., "add pagination to bookings endpoint")
  - Enters plan mode and proposes implementation
  - Implements the feature
  - Uses the validation MCP server to test the endpoint
  - If validation fails, spawns a debugging agent to fix issues
  - Loops until validation passes or max iterations reached
- The skill should maintain a validation report showing iteration history

**Success criteria:**
- You have a working MCP server that validates HTTP endpoints
- The `/implement-verified` skill demonstrates autonomous fix loops
- Claude fixes at least one failing test without human intervention
- You can explain the tradeoffs: when to loop vs. when to ask for help

**Hints:**
- The MCP server can shell out to `curl` or `httpx` for actual validation
- Consider using contract testing (Pact/Dredd) patterns for validation
- The skill needs to parse validation failures and form hypotheses about root causes
- Think about guardrails: max iterations, degradation paths, when to escalate

---

## Lunch Break
**Time:** 12:00–13:00

---

## Stage 3: Advanced Agent Orchestration
**Time:** 13:00–14:00 (60 min)

**Goal:** Create skills that coordinate multiple specialized agents in parallel and handle complex dependency graphs.

**Tasks:**
- Create a skill `/chaos-test` that orchestrates multiple agents in parallel:
  - Agent 1: Injects random failures into MCP servers (latency, errors, malformed data)
  - Agent 2: Runs the booking flow repeatedly and logs failures
  - Agent 3: Monitors logs and identifies failure patterns
  - Agent 4: Proposes fixes based on failure analysis
- The skill should:
  - Use background agents (`run_in_background: true`) for long-running tasks
  - Aggregate results from multiple agents using structured data (JSON)
  - Create a dependency graph: Agent 4 waits for Agent 3's analysis
  - Generate a final report with root cause analysis and proposed fixes
- Implement at least one fix from the chaos testing and verify it resolves the issue

**Success criteria:**
- Four agents run concurrently (two in parallel, two with dependencies)
- The skill aggregates findings from multiple agents into coherent recommendations
- You identified and fixed a real concurrency or failure-handling bug
- You can diagram the agent coordination flow and explain when to use parallel vs. sequential

**Hints:**
- Use `TaskOutput` to retrieve results from background agents
- Agents should write to structured files that other agents can read (JSON, not prose)
- Consider using a "coordinator" agent that doesn't do work but orchestrates others
- Think about how to make this skill generic—should work for any API project

---

## Stage 4: Daily Workflow Skills
**Time:** 14:00–15:00 (60 min)

**Goal:** Create practical, reusable skills for common engineering tasks beyond just coding.

**Tasks:**
- Each participant picks one skill to build (or propose your own):
  - **`/retro-prep`**: Analyzes git commits since last sprint, generates retro talking points, identifies patterns (what went well, what didn't)
  - **`/pr-impact`**: Given a PR number, analyzes blast radius—what services/endpoints are affected, what tests need to run, what could break
  - **`/onboard-service`**: Given a new service repo, generates architecture diagram, identifies dependencies, finds the "entry points", creates a dev setup checklist
  - **`/incident-debrief`**: Given logs or error messages, generates a structured incident report with timeline, root cause, and prevention steps
  - **`/debt-audit`**: Scans codebase for technical debt markers (TODO, FIXME, hardcoded values, missing tests), prioritizes by risk
- The skill must:
  - Work on any repo, not just this one
  - Coordinate multiple agents or tools
  - Produce structured output (markdown report, JSON, or diagram)
  - Be parameterizable (e.g., `/retro-prep --since="2 weeks ago"`)

**Success criteria:**
- Your skill is fully functional and tested on this repo
- You've tested it on at least one other repo (can be from your work, with sanitized data)
- The skill saves you >10 minutes vs. doing the task manually
- You can explain how you'd install this skill in your daily Claude Code setup

**Hints:**
- Skills can call other skills—compose primitives
- Use the Explore agent for broad codebase analysis, Grep/Glob for targeted searches
- Consider using `AskUserQuestion` to make skills interactive when needed
- Think about output format: can other tools consume your skill's output?

---

## Stage 5: MCP Server Development
**Time:** 15:00–15:45 (45 min)

**Goal:** Build a custom MCP server that extends Claude's capabilities for your domain.

**Tasks:**
- Create an MCP server that provides domain-specific tools for API development:
  - `validate_endpoint`: Given OpenAPI spec, validates actual endpoint behavior
  - `generate_test_data`: Creates realistic test data for schemas
  - `compare_versions`: Diffs two API versions and identifies breaking changes
  - `check_security`: Scans endpoints for common vulnerabilities (missing auth, CORS issues, etc.)
- Integrate the MCP server into Claude Code's configuration
- Create a skill that uses your MCP server to perform end-to-end API auditing
- Test the skill on the orbital-travel-planner API

**Success criteria:**
- Your MCP server implements at least 3 tools and responds correctly to MCP protocol messages
- Claude Code can discover and invoke your MCP server's tools
- A skill successfully uses your MCP server to audit the API
- You can explain the MCP protocol: tool discovery, invocation, error handling

**Hints:**
- Study the MCP specification: server lifecycle, tool definition format, JSON-RPC transport
- MCP servers can be written in Python—use `mcp` package or build from scratch
- Consider: should tools be synchronous or async? What about long-running operations?
- Think about error handling: how do you communicate failures to Claude?

---

## Stage 6: Integration & Reflection
**Time:** 15:45–16:00 (15 min)

**Goal:** Integrate your skills into a cohesive workflow and plan post-workshop usage.

**Tasks:**
- Create a meta-skill `/full-audit` that composes the skills you've built:
  - Runs API validation
  - Executes chaos testing
  - Performs security checks
  - Generates a comprehensive report
- Install your custom skills in your local Claude Code setup
- Document each skill: purpose, parameters, example usage, known limitations
- As a group, share the most useful skill created and demonstrate it

**Success criteria:**
- You have 2-3 working custom skills installed locally
- You can invoke them on different repos
- You've documented how to share skills with your team
- You can articulate when to build a skill vs. use an ad-hoc prompt

**Hints:**
- Skills can live in a shared repo—consider team distribution strategy
- Use `git log --oneline` to see what you built today
- Think about which skills need MCP servers vs. which work with existing tools

---

## Meta-Patterns to Internalize

### Agent Coordination
- **Parallel agents**: Independent tasks (multiple file searches, concurrent tests)
- **Sequential agents**: Output of one feeds another (Explore → Plan → Implement)
- **Background agents**: Long-running tasks that don't block (chaos testing, log monitoring)
- **Coordinator agents**: No work, just orchestration and aggregation

### Self-Validation Loops
- **External validation**: MCP servers that run real tests (API calls, type checks, security scans)
- **Fix-verify cycles**: Claude attempts fix → validates → fixes again if needed
- **Guardrails**: Max iterations, confidence thresholds, escalation paths
- **Structured feedback**: Parse failures into actionable hypotheses

### Skill Design
- **Composability**: Skills call other skills, tools, and agents
- **Reusability**: Parameterize for different repos, contexts, and use cases
- **Observability**: Log agent handoffs, decision points, and failures
- **Graceful degradation**: Partial success is better than all-or-nothing

### MCP Server Patterns
- **Tool granularity**: One focused thing vs. Swiss army knife
- **Stateless preferred**: Each call is independent
- **Rich errors**: Return structured diagnostics, not just "failed"
- **Composable tools**: Tools that can be chained in sequences

---

## Post-Workshop: Taking Skills Home

**Installation:**
- Copy skills to `~/.claude/skills/` (or your team's shared skills repo)
- Update Claude Code config to reference your MCP servers
- Test skills on a different project to verify portability

**Sharing with team:**
- Document each skill's purpose, parameters, and example usage
- Consider a team "skills registry" with contribution guidelines
- Run internal demos to show patterns (not just "here's a tool")

**Evolution:**
- Start with narrow, high-value skills (e.g., `/retro-prep`)
- Iterate based on usage: What's actually saving time?
- Build MCP servers when skills need capabilities Claude doesn't have natively
- Share learnings: When did agent orchestration help? When did it over-complicate?

---

## Resources

**Claude Code internals:**
- Skill manifest format: `~/.claude/skills/*/skill.json`
- Agent types and capabilities: Plan, Explore, Bash, general-purpose
- Task tool parameters: `subagent_type`, `run_in_background`, `resume`

**MCP development:**
- Specification: <https://modelcontextprotocol.io/>
- Python SDK: `pip install mcp`
- Example servers: <https://github.com/modelcontextprotocol/servers>

**Validation & testing:**
- OpenAPI validation: `openapi-spec-validator`, `schemathesis`
- Contract testing: Pact, Dredd
- API testing: Postman/Newman, `httpx`, `requests`

**Agent patterns:**
- Background tasks: `run_in_background=true`, poll with `TaskOutput`
- Structured output: Write JSON to files, agents read and process
- Error recovery: Parse failures, form hypotheses, attempt fixes
