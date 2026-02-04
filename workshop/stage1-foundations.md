# Stage 1: Foundations

**Time:** 30 minutes
**Goal:** Understand core building blocks—skills, agents, and MCP servers

## Learning Objectives

- Create and structure custom Claude Code skills
- Spawn and coordinate different agent types
- Configure MCP servers
- Understand where configuration and skills are stored

## Part A: Create a Custom Skill

**Time:** 10 minutes

### Background: Skills Overview

Skills extend Claude Code with reusable commands. They inject specialized instructions into Claude's context when invoked.

**Skill structure:**
```
~/.claude/skills/skill-name/
└── SKILL.md      # YAML frontmatter + instructions
```

### 1. Create a New Skill Directory

```bash
mkdir -p ~/.claude/skills/hello-skill
cd ~/.claude/skills/hello-skill
```

### 2. Create the Skill File

Create `SKILL.md`:

```markdown
---
name: hello-skill
description: Project-aware greeting and status check. Use when the user says hello or asks for project status.
---

You are a project-aware greeting assistant.

When invoked:
1. Read README.md in the current directory (if present)
2. Greet the user and mention the project name
3. Check git status for uncommitted changes
4. Provide a relevant tip based on project type:
   - Python: pytest, linting, or virtual environment tips
   - JavaScript: npm scripts or dependency tips
   - General: useful git commands
5. Ask what the user would like to work on

Use Read and Bash tools as needed. Keep responses under 100 words.
```

**YAML frontmatter fields:**
- `name`: Becomes the `/slash-command` (e.g., `/hello-skill`)
- `description`: Helps Claude decide when to auto-load the skill

### 4. Test the Skill

In your Claude Code session:

```
/hello-skill
```

The skill should activate and provide project context.

### Verification

- [ ] Created `~/.claude/skills/hello-skill/` directory
- [ ] `SKILL.md` file exists with YAML frontmatter
- [ ] Skill invokes with `/hello-skill` command
- [ ] Skill provides project-specific information

### Troubleshooting

**Skill doesn't appear:**
- Restart Claude Code
- Verify directory name matches `name` field in YAML frontmatter
- Check file permissions

**Skill errors on invocation:**
- Validate YAML frontmatter syntax (correct `---` markers)
- Ensure instructions are clear and actionable
- Verify current directory has expected files

## Part B: Understanding Subagents

**Time:** 10 minutes

### Background: What Are Subagents?

Subagents are specialized AI assistants that Claude delegates tasks to. Each runs in its own context window with:
- Custom system prompt focused on specific tasks
- Controlled tool access (can be read-only, write-only, etc.)
- Independent permissions and context management

**Why use subagents?**
- Keep verbose output (test results, logs) out of your main conversation
- Enforce constraints (read-only exploration, specific tool access)
- Run tasks concurrently in the background
- Preserve your main conversation context

### Built-in Subagents

Claude Code includes several built-in subagents that Claude uses automatically:

- **Explore**: Fast, read-only agent for searching and analyzing code (uses Haiku)
- **Plan**: Research agent for gathering context during plan mode
- **general-purpose**: Multi-step tasks requiring exploration and modification
- **Bash**: Command execution in a separate context

### 1. View Available Subagents

```
/agents
```

This opens an interactive interface showing:
- All available subagents (built-in, user-level, and project-level)
- Which subagents are active when duplicates exist
- Options to create, edit, or delete custom subagents

### 2. Observe Automatic Delegation

Ask Claude to explore the codebase:

```
Analyze the orbital-travel-planner codebase structure and map out the main components
```

Claude should automatically delegate to the **Explore** subagent. Notice:
- The subagent indicator showing which agent is running
- How the verbose exploration stays out of your main context
- The summary that returns when the subagent completes

### 3. Request Specific Subagents

You can explicitly request a subagent:

```
Use the Explore agent to find all API endpoints in this project
```

### 4. Create a Custom Subagent

Use the interactive interface:

```
/agents
```

Then:
1. Select **Create new agent**
2. Choose **Project-level** (saved to `.claude/agents/`)
3. Select **Generate with Claude**
4. Describe your subagent:
   ```
   A test analyzer that finds all test files, runs them, and reports only
   failures with their error messages. Keep successful test output minimal.
   ```
5. Choose tools: Select **Bash** and **Read-only tools**
6. Choose model: **Haiku** (fast and cost-effective)
7. Pick a color and save

### 5. Test Your Custom Subagent

```
Use the test-analyzer agent to check the test suite
```

Notice how only the relevant failure information returns, not the full test output.

### 6. Background Execution

Request a long-running task in the background:

```
In the background, run the full test suite with coverage reporting
```

You can continue working while it runs. Check progress:

```
/tasks
```

### Verification

- [ ] Opened `/agents` interface and viewed available subagents
- [ ] Observed Claude automatically delegating to Explore agent
- [ ] Created a custom project-level subagent
- [ ] Tested your custom subagent
- [ ] Understand when subagents preserve context vs. main conversation

### Key Concepts

**When Claude uses subagents automatically:**
- Verbose operations (running tests, processing logs)
- Codebase exploration that doesn't need to be in main context
- Tasks matching a custom subagent's description

**When to use main conversation:**
- Iterative refinement needing back-and-forth
- Multiple phases sharing significant context
- Quick, targeted changes where latency matters

**Foreground vs. Background:**
- **Foreground**: Blocks until complete, can prompt for permissions
- **Background**: Runs concurrently, gets permissions upfront, auto-denies anything not pre-approved

### Troubleshooting

**Subagent doesn't activate:**
- Check subagent description field - Claude uses it to decide when to delegate
- Try explicitly requesting the subagent by name
- Verify the subagent isn't in the `deny` list in settings

**Background task needs permissions:**
- Claude prompts for permissions before launching background tasks
- If it fails, you can resume it in foreground for interactive prompts

**Can't find subagent output:**
- Subagent summaries return to main conversation
- Full transcripts are in `~/.claude/projects/{project}/{sessionId}/subagents/`

## Part C: MCP Server Configuration

**Time:** 10 minutes

### Background: MCP Servers

MCP (Model Context Protocol) servers extend Claude's capabilities with custom tools. They function as plugins providing new functions Claude can invoke.

### 1. Review Existing Configuration

```bash
cat pyproject.toml
```

Look for the `[tool.claude.mcp]` section showing configured MCP servers.

### 2. Understand MCP Structure

An MCP server provides:
- **Tools**: Functions Claude can invoke
- **Parameters**: JSON Schema defining inputs
- **Responses**: Structured return values

### 3. Test the Existing MCP Server

```
Use the MCP server to validate the /api/destinations endpoint for a 200 status code
```

Claude should discover and invoke the configured MCP server tool.

### 4. Add a New MCP Server

Add the time MCP server as an example.

Create or edit `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

Restart Claude Code to load the configuration.

### 5. Test the New Server

```
Query the current time from the MCP time server
```

### 6. Review MCP Protocol

```
Explain how MCP servers communicate using the JSON-RPC protocol over stdio
```

Or fetch documentation:

```
Use WebFetch to retrieve and summarize the MCP protocol documentation from https://modelcontextprotocol.io
```

### Verification

- [ ] Reviewed existing MCP server configuration
- [ ] Tested orbital-travel-planner MCP server
- [ ] Added new MCP server to configuration
- [ ] Claude successfully invoked the new server
- [ ] Understand MCP basics (tools, parameters, JSON-RPC)

### Troubleshooting

**MCP server not found:**
- Verify config file syntax is valid JSON
- Restart Claude Code after config changes
- Check server command path is correct

**Tool invocation fails:**
- Verify parameter types match schema
- Check server logs for errors
- Ensure server process is running

**Cannot locate config file:**
- Check `~/.claude/config.json`
- Ask Claude for config file location
- Refer to Claude Code documentation

## Stage 1 Summary

You have now:
- Created a working custom skill
- Spawned and coordinated different agent types
- Added an MCP server to your configuration
- Understood core Claude Code building blocks

### Knowledge Check

Before proceeding, ensure you can answer:

1. Where do custom skills reside?
2. What is the required file structure for a skill?
3. What are the four main agent types?
4. How do agents share data with each other?
5. What protocol do MCP servers use?

### Advanced Exercises (Optional)

**Skill Enhancement:**
Modify hello-skill to detect programming language and provide language-specific tips.

**Agent Chain:**
Create a three-agent workflow:
1. Find all Python files
2. Identify files without tests
3. Generate test stubs for uncovered files

**MCP Exploration:**
Browse https://github.com/modelcontextprotocol/servers and add another server of interest.

---

**Next:** [Stage 2: Meta-Programming & Self-Validation](./stage2-meta-programming.md)
