# Advanced Claude Code Workshop

**Duration:** 10:30–16:00 (lunch 12:00–13:00)
**Audience:** Backend Python engineers familiar with Claude and LLM basics
**Focus:** Planning-first workflows, multi-agent systems, MCP integrations, verification loops

This codebase is intentionally incomplete. Use Claude Code to reason, plan, implement, test, and iterate.

---

## Stage 1: Orientation & Constraints
**Time:** 10:30–11:00 (30 min)

**Goal:** Understand the system boundaries, existing code structure, and Claude Code's planning capabilities.

**Tasks:**
- Clone the repo and explore the structure using Claude Code's exploration agents
- Ask Claude to identify what's implemented vs. what's missing
- Run the existing backend and frontend to confirm baseline functionality
- Review `pyproject.toml` and understand the MCP servers configured
- Have Claude explain the intended architecture: what should be local vs. delegated to MCP

**Success criteria:**
- Backend runs on `localhost:8000`
- Frontend connects and renders
- You can articulate what the MCP servers are supposed to provide
- You understand where the naive or incomplete implementations are

**Hints:**
- Use `/explore` or ask Claude to map the codebase before diving in
- Check `README.md` for assumptions about MCP server behavior

---

## Stage 2: Planning & Orchestration
**Time:** 11:00–12:00 (60 min)

**Goal:** Practice planning-first workflows and understand when to break tasks across multiple agents or phases.

**Tasks:**
- Implement a new endpoint: `POST /api/bookings` that accepts origin, destination, and date
- Before coding, ask Claude to enter plan mode and propose an implementation strategy
- The endpoint should validate inputs, call the MCP route provider, estimate pricing, and persist a booking
- Deliberately introduce a constraint: bookings must check for duplicate routes within the same day
- Ask Claude to reason about where validation belongs (API layer, service layer, database constraints)
- Use Claude to coordinate backend changes, test additions, and schema updates in sequence

**Success criteria:**
- `/api/bookings` endpoint exists and returns structured JSON
- Tests pass (or are written and pass)
- You rejected at least one naive implementation in favor of a better-planned approach
- You understand when Claude should pause to ask for your input vs. proceed autonomously

**Hints:**
- Use `EnterPlanMode` explicitly to see the planning workflow
- If Claude generates code before planning, stop it and ask for a plan first
- Consider: should duplicate detection be synchronous or async?

---

## Lunch Break
**Time:** 12:00–13:00

---

## Stage 3: External Systems via MCP
**Time:** 13:00–14:00 (60 min)

**Goal:** Integrate with MCP servers for routes, pricing, and emissions data. Handle failures gracefully.

**Tasks:**
- Extend the `/api/bookings` endpoint to call all three MCP providers: routes, pricing, emissions
- Simulate failure scenarios: one MCP server is slow, another returns errors intermittently
- Implement retry logic with exponential backoff for transient failures
- Add a `/api/bookings/{id}/status` endpoint that shows whether external data is still pending
- Use Claude to reason about when to fail fast vs. degrade gracefully
- Add observability: log MCP call durations and success rates

**Success criteria:**
- Booking flow calls all three MCP servers
- Retries happen automatically for transient errors
- Logs show MCP call outcomes
- You can explain the tradeoffs between sync, async, and eventual consistency approaches

**Hints:**
- MCP servers may be local scripts or stubs—check `mcp_servers/` directory
- Consider: should you block the booking if one provider is down?
- Use `TodoWrite` to break this into subtasks: integration, retry logic, observability

---

## Stage 4: Verification & Quality Gates
**Time:** 14:00–15:00 (60 min)

**Goal:** Build automated verification that catches regressions and enforces invariants.

**Tasks:**
- Add schema validation for all API responses using Pydantic models
- Write integration tests that assert booking invariants (e.g., price > 0, date in future)
- Introduce a failing test deliberately (e.g., negative pricing allowed) and ask Claude to fix the root cause
- Add a pre-commit hook or CI step that runs tests and type-checking
- Use Claude to identify edge cases: what happens if a route has no emissions data?
- Implement a `/health` endpoint that checks MCP connectivity and returns degraded status if providers are down

**Success criteria:**
- All API responses validate against Pydantic schemas
- Tests cover happy path and at least three failure modes
- You fixed a deliberately broken test by changing code, not the test
- Health endpoint accurately reflects system state

**Hints:**
- Use `pytest` with fixtures to mock MCP responses
- Ask Claude to generate property-based tests for invariants (e.g., pricing consistency)
- Consider: should schema validation happen at serialization time or earlier?

---

## Stage 5: Creative Extension Sprint
**Time:** 15:00–15:45 (45 min)

**Goal:** Apply advanced patterns to a self-directed feature. Demonstrate multi-step reasoning and verification loops.

**Tasks:**
- Choose one extension (or propose your own):
  - **Multi-leg journeys:** Allow bookings with layovers, optimize for cost or emissions
  - **Dynamic pricing:** Adjust prices based on demand, time-of-day, or inventory
  - **Recommendation engine:** Suggest alternative routes if the requested one is unavailable
  - **Admin dashboard:** Add endpoints to view all bookings, filter by status, export to CSV
- Before implementing, ask Claude to:
  - Propose multiple approaches and rank them by complexity, extensibility, and risk
  - Identify which existing code will need refactoring
  - Estimate how many files will change (no time estimates, just scope)
- Implement the feature using Claude Code
- Write tests and verify the feature works end-to-end

**Success criteria:**
- Feature is functional and tested
- You chose an approach after weighing tradeoffs (not just the first idea)
- Claude proposed a plan, you approved it, then implementation followed
- You can explain one thing you would do differently with more time

**Hints:**
- Use `AskUserQuestion` to clarify ambiguous requirements before Claude commits to an approach
- If the feature requires external data, extend the MCP servers or mock them
- Timebox ruthlessly—partially complete is fine if the architecture is sound

---

## Stage 6: Wrap-up & Reflection
**Time:** 15:45–16:00 (15 min)

**Goal:** Consolidate learnings and identify patterns for advanced Claude Code usage.

**Tasks:**
- Review the git diff for the day—how much code changed?
- Ask Claude to summarize what it implemented and identify areas of technical debt
- Discuss as a group:
  - When did planning-first save time vs. slow you down?
  - What kinds of tasks are best delegated to autonomous agents?
  - How did MCP integrations compare to hardcoded logic?
  - What verification gates caught real bugs vs. busywork?

**Success criteria:**
- You can articulate 2–3 patterns for effective Claude Code usage
- You identified at least one failure mode (yours or Claude's) and how to avoid it next time

**Hints:**
- Use `git log --oneline` to see the commit history
- Ask Claude: "What would you refactor if you had another hour?"

---

## General Guidelines

**Planning-first workflow:**
- Prefer `EnterPlanMode` for any task touching >2 files or introducing new abstractions
- Use `TodoWrite` to break complex tasks into trackable subtasks
- When Claude proposes a solution, ask "what are the alternatives?" before proceeding

**Multi-agent coordination:**
- Use specialized agents (Explore, Plan, Test) rather than doing everything in the main loop
- Run independent tasks in parallel when possible (e.g., multiple file searches)

**Verification loops:**
- Write tests before implementation when the requirements are clear
- Use failing tests to drive fixes, not the other way around
- Automate as much verification as possible (schemas, type-checking, integration tests)

**MCP integration patterns:**
- Treat external systems as unreliable by default
- Design for graceful degradation when providers are unavailable
- Log, observe, and surface errors to users appropriately

**Common pitfalls:**
- Jumping into code without planning
- Accepting the first solution without exploring tradeoffs
- Writing tests that only validate happy paths
- Hardcoding logic that should be configurable or delegated to MCP

---

## Resources

- Claude Code docs: <https://github.com/anthropics/claude-code>
- MCP specification: <https://modelcontextprotocol.io/>
- This repo's README for baseline setup and MCP server behavior
