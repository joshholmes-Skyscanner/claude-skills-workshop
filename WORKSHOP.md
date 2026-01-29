# Workshop Guide (Facilitator + Participants)

This repo is deliberately **not complete**. The point is to use Claude Code to:
1) plan improvements
2) implement
3) verify with tests + invariants
4) iterate via failures

## Target outcomes by end of day
- A planner that builds routes via provider data (MCP) and ranks by cost/time/emissions/risk
- A deterministic test harness and a chaos harness (timeouts/partial data)
- CI-ready checks (schema + invariants)

## Exercises (high level)
1) Replace naive route generation with graph-based search (k-shortest paths)
2) Add pricing modifiers (peak/off-peak, carrier, “space weather”)
3) Enforce invariants (no negative price, valid time windows, bounded layovers)
4) Add chaos mode handling: retries + graceful degradation
5) Extend scoring modes: `cheapest`, `fastest`, `greenest`, `balanced`
