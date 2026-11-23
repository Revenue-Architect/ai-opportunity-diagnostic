# Original blueprint (V1 + V2), as written by Kamran on 2026-11-22

Kept verbatim for reference. The math formulas were lost when the text was pasted, and the "click any node" references point to interactive diagrams that were not saved. The technical claims (FastMCP 4.2.0, SEP-2640, SEP-2322, SEP-1865, VS Code 1.147, the Mermaid MCP URL) were checked on 2026-11-22 and are real; see [reviews/2026-11-22-gemini-plan-review.md](reviews/2026-11-22-gemini-plan-review.md). FastMCP 4.2.0 and VS Code 1.147 were confirmed at their primary sources. FastMCP's latest release is 4.2.4, which includes an OAuth security fix, so pin that or newer rather than 4.2.0. See [plan.md](plan.md) for what was built and why.

---

Build this as a Skill-first, MCP-optional product. The Skill holds your consulting brain (Socratic interview flow, kill gates, vertical playbooks, and local deterministic scoring scripts), while the remote MCP server is strictly reserved for live client data probes, cross-session state, and interactive diagram rendering. Because clients run the Skill inside their own Claude, Cursor, or Codex seats, your token cost stays near zero while your diagnostic methodology becomes installable software they can re-run every quarter.

## 1. Ownable Diagnostic Methodology

Generic AI audits fail because they start by brainstorming tools and let the LLM invent arbitrary scores. Lock your Skill into a strict five-stage state machine so every engagement produces consistent, defensible numbers.

* Cost-First Socratic Intake: Force the agent to interview the operator one focused question at a time rather than dumping a 20-question survey. Start strictly with operational drag across core functions (lead intake, quoting, fulfillment, customer support, back-office admin) and capture weekly hours, loaded hourly cost, volume, and rework frequency before mentioning AI.
* The No-AI Kill Gate: Every candidate process must pass a hard architectural filter before scoring. If deterministic rules, native SaaS configuration, or a simple webhook solves 80% of the bottleneck, classify it immediately as Standard Automation and strip it out of the AI shortlist.
* Deterministic 5-Axis Scoring: Never let the model eyeball composite scores in prose. Pass raw 1–5 ratings into a deterministic script or MCP tool using fixed weights: Business Value (30%), Data Readiness (25%), Integration Feasibility (20%), Error Tolerance and Risk (15%), and Run-Cost Efficiency (10%). Hard-code automatic kill rules so any candidate scoring under 2 on Data Readiness or Error Tolerance is flagged as Blocked pending governance regardless of ROI.
* Evidence Spike and Single-Approver Gate: For the top 3 to 5 shortlisted candidates, require at least one concrete evidence artifact (an anonymized CSV export, sample support tickets, or a live read-only query) to replace interview guesses with data reality. Every proposed AI workflow must name one human approver, define what the agent is forbidden to execute autonomously, and specify an explicit rollback path.
* Four Mandatory Visual Deliverables: Require the final output to include one-page business cases with kill criteria plus four diagrams: Current-State Process Flow, Proposed AI-Augmented Flow (highlighting human approval gates), Impact vs. Feasibility Priority Matrix (Mermaid quadrant chart), and a 90-Day Phased Roadmap.

## 2. Two-Layer Technical Architecture

Anthropic published Agent Skills as an open standard (agentskills.io) that works across Claude.ai, Claude Code, the Claude API, and OpenAI Codex. Its three-level progressive disclosure model solves context rot cleanly: only the YAML name and description load at startup (roughly 100 tokens), the SKILL.md body loads only when triggered (kept under 500 lines and under 5,000 tokens), and supporting files in references/, scripts/, and assets/ load strictly on demand.

```
ai-opportunity-assessment/
├── SKILL.md
├── references/
│   ├── interview-protocol.md
│   ├── scoring-rubric.md
│   ├── output-templates.md
│   └── verticals/
│       ├── ecommerce-retail.md
│       └── home-services.md
├── scripts/
│   ├── score_opportunities.py
│   └── generate_diagrams.py
└── assets/
    └── sample-business-audit.json
```

Pay particular attention to the YAML frontmatter in SKILL.md. The name field must match the folder name (up to 64 lowercase characters, digits, and hyphens), and the description field (up to 1,024 characters) makes or breaks auto-triggering. Pack the description with concrete trigger phrases operators actually type ("run AI assessment", "audit workflows for AI", "map AI use cases", "prioritize automation projects") alongside explicit negative boundaries so it does not collide with unrelated skills. Validate the folder structure before packaging using skills-ref validate.

| Layer | What Lives Here | Why It Belongs Here | Client Installation & Portability |
|---|---|---|---|
| Skill (SKILL.md + references/) | Socratic interview rules, No-AI filter, weighted rubric, vertical packs, report templates | Progressive disclosure keeps idle context cost minimal and enforces repeatable methodology | Upload ZIP in Claude.ai (Customize → Skills), drop into .claude/skills/, or load in Codex |
| Bundled scripts/ (Python) | Weighted composite scoring, quadrant bucketing, CSV data spike profiler, Mermaid generator | Guarantees deterministic math and lets privacy-sensitive clients analyze local CSV exports with zero data egress | Executes directly inside Claude Code or Claude.ai code execution |
| Diagram MCP App | Interactive SVG/PNG rendering, one-click code copy, syntax repair links | Offloads diagram UI rendering to the Mermaid Claude MCP App (https://chatgpt.mermaid.ai/anthropic/mcp) via validate_and_render_mermaid_diagram | Client adds the remote MCP connector URL once; fall back to draw.io MCP when editable handoff is needed |
| Custom Remote MCP (Streamable HTTP) | Multi-session audit persistence, read-only connectors (CRM, ERP, Notion, Slack), "Skills Over MCP" resource endpoint | Keeps proprietary connectors and API auth server-side without distributing backend code | Client pastes your Streamable HTTP URL as a custom connector; works across Claude, Cursor, and non-Claude MCP hosts |

## 3. Phased 4-Week Execution Plan

* Week 1 — Core Skill and Deterministic Engine: Draft SKILL.md under 400 lines alongside references/interview-protocol.md, references/scoring-rubric.md, and references/output-templates.md. Build scripts/score_opportunities.py to ingest structured process JSON, run the No-AI triage, compute weighted scores, enforce kill gates, and output validated Mermaid code for all four required diagrams. Drop a realistic synthetic company profile into assets/sample-business-audit.json so anyone installing the Skill can run a 3-minute test immediately. Benchmark triggering across 15 realistic user prompts and run repeated audits on the sample dataset to verify consistent math and output structure.
* Week 2 — Interactive Visual Pipeline and Vertical Packs: Wire SKILL.md to invoke validate_and_render_mermaid_diagram whenever the Mermaid MCP App is connected, with clean degradation to native Mermaid artifacts if a client has not attached the connector. Author your first two vertical reference packs under references/verticals/ so the diagnostic probes industry-specific bottlenecks instead of generic workflows: an E-commerce and Retail pack (order exception routing, multi-location inventory reconciliation, returns triage, B2B quote generation, support deflection) and a Home Services pack (missed-call and lead dispatch, estimate follow-up, technician scheduling, invoice chasing, recurring maintenance reminders).
* Week 3 — Lightweight Remote Assessment MCP: Build a lean Streamable HTTP MCP server exposing four focused tools: save_audit_state (persists intake and scores across sessions), score_portfolio (mirrors the Python scorer for environments without local code execution), profile_system_export (ingests sanitized exports or read-only CRM/ERP summaries for the data spike), and get_methodology_pack (serves your SKILL.md and vertical references over MCP so non-Claude agents and Cursor workflows run the exact same diagnostic). Keep connectors strictly read-only to eliminate enterprise security friction.
* Week 4 — Live Calibration and Split Distribution: Run the complete diagnostic end-to-end on two real operating businesses (one e-commerce, one home services), compare the agent's shortlist against your own architectural judgment, and tighten rubric weights or interview follow-ups wherever the model misses nuance. Split your Git repository into two build targets: a public Lite ZIP for top-of-funnel distribution and a private Pro release containing the vertical packs, local CSV evidence profiler, and remote MCP credentials.

## 4. Packaging and Consulting Funnel

| Tier | Included Deliverables | Distribution Mechanism | Commercial Role |
|---|---|---|---|
| Lite Skill (Free Lead Magnet) | Generic 5-stage Socratic diagnostic, core 5-axis rubric, No-AI kill gate, dummy data fixture, standard Mermaid outputs | Public ZIP upload or GitHub repo (zero MCP setup required) | Proves technical rigor upfront by killing weak AI ideas instead of selling hype |
| Pro Skill + Vertical Pack (Paid Kit / Retainer Asset) | E-commerce or Home Services vertical playbooks, local Python CSV evidence profiler, single-approver governance templates, Mermaid/draw.io rendering prompts | Private ZIP + optional Streamable HTTP MCP URL | Low-friction paid install or quarterly self-audit tool running on the client's own AI subscription |
| Managed Diagnostic Blueprint (Fixed-Scope Sprint) | Facilitated live audit using your remote MCP + read-only probes into client ERP, CRM, and helpdesk data, verified data spike, executive readout, and fixed-scope build quote | You run the diagnostic alongside leadership and leave the Skill installed for ongoing governance | Converts validated quick wins directly into high-ticket agent implementation engagements |

Explore how a single assessment session moves across the Skill layer, deterministic scoring engine, remote MCP connectors, and interactive diagram renderer below. Click any node to inspect its boundary and protocol, or step through all six execution stages.

Separating the local deterministic scorer from the optional remote MCP server gives you the cleanest commercial wedge: anyone can test the Lite Skill in five minutes with zero infrastructure, and upgrading to your paid diagnostic only requires dropping in a vertical pack and pasting one Streamable HTTP connector URL.

---

# V2

This V2 blueprint replaces ad-hoc prompts and static flowcharts with a single-source, versioned architecture built on FastMCP 4.2.0 (Python 3.11+), the official Skills over MCP extension (io.modelcontextprotocol/skills, SEP-2640), and the stable MCP Apps extension (io.modelcontextprotocol/ui, SEP-1865, revision 2026-01-26). One Git repository compiles into both your free Lite Skill ZIP lead magnet and your paid remote MCP server with an interactive ui:// workbench.

## 1. Single-Source Git Repository Structure

A single repository prevents methodology drift between free lead-magnet downloads, paid vertical kits, and hosted MCP deployments. The core scoring engine in packages/scoring_core/ ships both inside the standalone Skill ZIP (for zero-egress local execution) and as an imported library inside the FastMCP server.

```
agentic-opportunity-audit/
├── pyproject.toml                       # Pinned fastmcp==4.2.0, pydantic>=2.9, python>=3.11
├── Makefile                             # build-lite, build-pro, test-evals, serve-http
├── skills/
│   ├── ai-opportunity-audit/            # Canonical Skill root (Lite + Base)
│   │   ├── SKILL.md                     # Under 400 lines; YAML name/description + 5-stage protocol
│   │   ├── references/
│   │   │   ├── interview-protocol.md    # Socratic 1-question intake + Two-Role Delta rules
│   │   │   ├── scoring-rubric.md        # 5-axis rubric + No-AI Kill Gate + confidence bands
│   │   │   └── output-templates.md      # One-page business case + kill criteria markdown
│   │   ├── scripts/
│   │   │   └── score_audit.py           # Thin CLI wrapper around packages/scoring_core
│   │   └── assets/
│   │       └── sample-business.json     # Synthetic demo fixture for 3-minute smoke test
│   └── verticals/                       # Private Pro add-on packs (excluded from Lite ZIP)
│       ├── ecommerce-retail/
│       │   ├── SKILL.md                 # Extends base audit with Shopify/ERP/3PL red flags
│       │   └── benchmarks.json          # Proprietary cycle-time & rework bands (server-only)
│       └── home-services/
│           ├── SKILL.md                 # Extends base audit with dispatch/quoting/CSR red flags
│           └── benchmarks.json          # Proprietary missed-call & estimate leakage bands
├── packages/
│   └── scoring_core/
│       ├── models.py                    # Pydantic schemas: ProcessCandidate, EvidenceTrace, AuditState
│       ├── engine.py                    # Deterministic 5-axis, confidence multiplier, and kill gates
│       ├── profiler.py                  # Ephemeral zero-auth 30-day CSV/log anomaly profiler
│       └── exporter.py                  # Executive HTML/PDF summary + Linear/Jira backlog JSON
├── server/
│   ├── app.py                           # FastMCP 4.2 server wiring SkillCatalogProvider + MCP App
│   ├── elicitation.py                   # Dual-era elicitation router (2026-07-28 vs <=2025-11-25)
│   ├── state_store.py                   # Explicit audit_id persistence (SQLite/Postgres, sessionless-safe)
│   └── auth.py                          # Bearer token verifier for paid vertical entitlements
├── workbench-ui/                        # Vite + single-file HTML5 bundle for ui:// MCP App
│   ├── src/
│   │   ├── main.ts                      # @modelcontextprotocol/ext-apps App bridge & postMessage RPC
│   │   ├── QuadrantCanvas.tsx           # Interactive Impact vs Feasibility matrix + weight sliders
│   │   ├── DeltaInspector.tsx           # Exec-vs-Frontline perception gap + evidence trace drawer
│   │   └── ApproverGateForm.tsx         # Single-approver assignment, dollar caps, and kill criteria
│   └── dist/workbench.html              # Compiled single-file text/html;profile=mcp-app asset
├── evals/
│   ├── fixtures/                        # 5 trap-laden synthetic company JSON + CSV pairs
│   ├── test_deterministic_engine.py     # CI-blocking math, confidence, and kill-gate assertions
│   └── test_agent_behavioral.py         # End-to-end LLM + MCP transcript assertions on model updates
└── scripts/
    └── build_releases.py                # Compiles dist/lite-skill.zip + validates SHA-256 manifests
```

### Build and Distribution Separation

| Target Artifact | Source Paths Included | What Stays Server-Side (IP Moat) | Delivery Mechanism |
|---|---|---|---|
| Lite Skill ZIP (dist/ai-opportunity-audit-lite.zip) | skills/ai-opportunity-audit/ + bundled scoring_core/engine.py | Vertical benchmarks, interactive ui:// workbench, CSV anomaly templates, backlog exporter | Free lead magnet uploaded to Claude.ai, .claude/skills/, or Codex |
| Pro Remote MCP (https://audit.yourdomain.com/mcp) | Full skills/ + verticals/ via SkillCatalogProvider, packages/scoring_core, and workbench-ui/dist/workbench.html | benchmarks.json never exposed as raw files; only computed percentile bands return in tool output | Streamable HTTP MCP URL authenticated via tenant Bearer token |

## 2. FastMCP 4.2 Server Architecture: Skills over MCP & Dual-Era Elicitation

FastMCP 4.2.0 (released November 13, 2026, built on MCP Python SDK v2 and the sessionless 2026-07-28 protocol revision) natively implements the Skills over MCP extension (io.modelcontextprotocol/skills, SEP-2640) alongside backward compatibility for legacy handshake-era clients (2024-11-05 through 2025-11-25) on the exact same HTTP endpoint.

### Cross-Host Skill Compatibility Strategy

Clients fall into three runtime tiers today, and your single FastMCP server handles all three cleanly without duplicating content.

* Extension-Aware Hosts (Native skills/list and skills/get): Clients such as VS Code 1.147+ discover your catalog automatically over io.modelcontextprotocol/skills, prompt the user for consent, verify SHA-256 file digests and byte sizes, and inject SKILL.md on demand as slash commands.
* Resource-Fallback Hosts (skill:// via resources/read): FastMCP 4.2 automatically exposes every registered skill file as an ordinary skill:// MCP resource. Hosts including Claude Code, Codex, Cursor, OpenCode, and Gemini CLI read the methodology straight from your server via resources/read while retaining progressive disclosure.
* Non-Skill MCP Hosts (e.g., ChatGPT, Zed): These clients connect to your tools and MCP App workbench cleanly, while a concise get_audit_bootstrap prompt provides the five-stage workflow rules when skills/list is absent.

### Two Critical FastMCP 4.2 Protocol Guardrails

Upgrading to FastMCP 4.2 introduces two strict protocol behaviors that will break naive servers if ignored.

* Explicit audit_id State Keying: On sessionless 2026-07-28 connections, ctx.session_id generates a new identifier on every request rather than persisting across the conversation. Never key audit state by ctx.session_id. Issue an opaque audit_id (UUIDv7) during start_audit, persist state in SQLite or Postgres keyed by (tenant_id, audit_id), and pass audit_id explicitly across tool calls and UI callbacks.
* Dual-Era Elicitation Branching: FastMCP enforces a strict era gate for structured user forms. On 2026-07-28 connections, tools must return an InputRequiredResult (SEP-2322 multi-round-trip guard pattern reading ctx.input_responses and ctx.request_state), whereas calling await ctx.elicit(...) raises an era error. Conversely, legacy handshake connections (2025-11-25 and earlier) require await ctx.elicit(...) and reject InputRequiredResult. Your elicitation helper must branch explicitly on ctx.request_context.protocol_version.

### Reference FastMCP 4.2 Server Assembly (server/app.py)

```python
from pathlib import Path
from fastmcp import FastMCP, Skill, Context
from fastmcp.skills.provider import SkillCatalogProvider
from fastmcp.server.apps import AppConfig, ResourceCSP
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

from packages.scoring_core.engine import score_audit_portfolio
from packages.scoring_core.models import AuditInputPayload, GateMutationPayload
from packages.scoring_core.profiler import profile_csv_ephemeral
from server.state_store import AuditStore

WORKBENCH_URI = "ui://agentic-audit/workbench"
WORKBENCH_HTML = Path("workbench-ui/dist/workbench.html").read_text(encoding="utf-8")

mcp = FastMCP(
    name="Agentic Opportunity Audit",
    instructions=(
        "Follow the ai-opportunity-audit skill methodology. Never invent ROI numbers; "
        "tag unverified claims as OPERATOR_ESTIMATE and enforce the No-AI Kill Gate first."
    ),
)

# 1. Single-source Skills over MCP catalog (SEP-2640 + skill:// resources fallback)
base_skill = Skill.from_directory("skills/ai-opportunity-audit")
ecom_skill = Skill.from_directory("skills/verticals/ecommerce-retail")
trades_skill = Skill.from_directory("skills/verticals/home-services")
mcp.add_provider(SkillCatalogProvider([base_skill, ecom_skill, trades_skill]))

store = AuditStore("data/audits.db")

# 2. Sandboxed MCP App UI Resource (text/html;profile=mcp-app)
@mcp.resource(
    WORKBENCH_URI,
    mime_type="text/html;profile=mcp-app",
    app=AppConfig(
        csp=ResourceCSP(
            connect_domains=[],
            resource_domains=[],
            frame_domains=[],
        ),
        prefers_border=True,
    ),
)
def render_workbench_bundle() -> str:
    return WORKBENCH_HTML

# 3. Model + App Entrypoint: scores portfolio and opens interactive workbench
@mcp.tool(
    app=AppConfig(
        resource_uri=WORKBENCH_URI,
        visibility=["model", "app"],
    )
)
async def open_assessment_workbench(payload: AuditInputPayload, ctx: Context) -> ToolResult:
    result = score_audit_portfolio(payload, include_vertical_benchmarks=True)
    store.save(payload.audit_id, result)

    # Graceful text-only fallback for terminal hosts (Claude Code, Codex, CLI)
    markdown_summary = result.to_executive_markdown()
    return ToolResult(
        content=[TextContent(type="text", text=markdown_summary)],
        structured_content=result.model_dump(mode="json"),
    )

# 4. Zero-Auth Ephemeral CSV Profiler (model-callable; raw rows discarded immediately)
@mcp.tool()
async def profile_evidence_csv(
    audit_id: str,
    process_id: str,
    csv_text: str,
    schema_hint: str,
) -> dict:
    trace = profile_csv_ephemeral(csv_text=csv_text, schema_hint=schema_hint)
    store.attach_evidence_trace(audit_id, process_id, trace)
    return trace.model_dump(mode="json")

# 5. App-Only Backend Tools (hidden from model context; callable only by ui:// iframe)
@mcp.tool(app=AppConfig(visibility=["app"]))
async def recompute_workbench_weights(
    audit_id: str,
    weights: dict[str, float],
) -> dict:
    updated = store.recompute_with_custom_weights(audit_id, weights)
    return updated.model_dump(mode="json")

@mcp.tool(app=AppConfig(visibility=["app"]))
async def commit_approver_gate(mutation: GateMutationPayload) -> dict:
    updated = store.update_approver_gate(mutation)
    return updated.model_dump(mode="json")
```

Note how Skill.from_directory and SkillCatalogProvider register the exact folders verified in FastMCP 4.2, while AppConfig emits the nested _meta.ui specification (resourceUri and visibility) required by the MCP Apps extension. Setting visibility=["app"] on interactive UI backend tools keeps the model's tool list lean and prevents the LLM from accidentally mutating approver gates outside user action.

## 3. MCP App Workbench Schema (ui:// Interactive Surface)

Instead of rendering static Mermaid strings via a third-party server, your server ships a single-file HTML5 workbench (text/html;profile=mcp-app) rendered inside a host-managed sandboxed iframe.

### Wire Metadata & Security Contract

The server exposes strict default-deny Content Security Policy metadata so enterprise hosts can audit and cache the template at connection time. No external CDN scripts, analytics beacons, or outbound fetches are permitted; all JS and CSS bundle inline via Vite.

```json
{
  "tool_meta": {
    "_meta": {
      "ui": {
        "resourceUri": "ui://agentic-audit/workbench",
        "visibility": ["model", "app"]
      }
    }
  },
  "resource_meta": {
    "uri": "ui://agentic-audit/workbench",
    "mimeType": "text/html;profile=mcp-app",
    "_meta": {
      "ui": {
        "prefersBorder": true,
        "csp": {
          "connectDomains": [],
          "resourceDomains": [],
          "frameDomains": []
        },
        "permissions": {}
      }
    }
  }
}
```

### Bidirectional JSON-RPC 2.0 Lifecycle

Communication between the sandboxed View and the MCP host runs strictly over JSON-RPC 2.0 postMessage via @modelcontextprotocol/ext-apps.

* Initialization Handshake: The View emits ui/initialize declaring supported display modes (["inline", "fullscreen"]), receives hostContext (theme, locale, active display mode), and replies with ui/notifications/initialized.
* Data Injection: When open_assessment_workbench finishes, the host pushes structuredContent into the View via ontoolresult.
* Interactive What-If Loops (App to Server): Dragging a rubric weight slider or assigning a named human approver invokes callServerTool against recompute_workbench_weights or commit_approver_gate without spending a single LLM token.
* Model Context Sync (App to Model): Whenever the client clicks Lock Shortlist & Sync to Agent, the View calls ui/update-model-context (which hosts deduplicate so only the latest approved snapshot enters context) followed by ui/message asking the agent to generate the final 90-day implementation plan strictly for the locked candidates.

### Canonical AuditWorkbenchState Payload Schema

```json
{
  "audit_id": "019a9f1e-4b72-7c00-9f12-8b3d4a1e0c21",
  "vertical": "home-services",
  "schema_version": "2.0.0",
  "weights": {
    "business_value": 0.30,
    "data_readiness": 0.25,
    "integration_feasibility": 0.20,
    "error_tolerance": 0.15,
    "run_cost_efficiency": 0.10
  },
  "portfolio_summary": {
    "total_candidates": 8,
    "killed_no_ai_count": 3,
    "blocked_governance_count": 1,
    "verified_annual_opportunity_usd": 170400,
    "unverified_estimate_opportunity_usd": 42000
  },
  "candidates": [
    {
      "process_id": "proc_after_hours_dispatch",
      "name": "After-Hours Missed Call Triage & Slot Booking",
      "classification": "QUICK_WIN",
      "evidence_tier": "VERIFIED_TRACE",
      "confidence_multiplier": 1.0,
      "scores": {
        "business_value": 5,
        "data_readiness": 4,
        "integration_feasibility": 4,
        "error_tolerance": 4,
        "run_cost_efficiency": 5,
        "raw_composite": 4.45,
        "adjusted_priority": 4.45
      },
      "financials": {
        "annual_drag_usd": 170400,
        "estimated_monthly_run_cost_usd": 185,
        "payback_days": 14
      },
      "role_delta": {
        "exec_weekly_hours": 12.0,
        "frontline_weekly_hours": 13.5,
        "delta_ratio": 0.111,
        "flagged": false
      },
      "vertical_benchmark": {
        "metric": "missed_call_rate_pct",
        "client_value": 38.0,
        "vertical_median": 18.5,
        "percentile_band": "Bottom 15% (High Urgency)"
      },
      "human_gate": {
        "single_approver": "Dispatch Manager (7:30 AM daily review)",
        "forbidden_autonomous_actions": ["Dispatch emergency crew without SMS confirmation", "Quote custom panel upgrades over $1,500"],
        "rollback_path": "Forward DID back to live answering service via Twilio failover webhook"
      },
      "kill_criteria": [
        "Booking conversion on captured calls stays below 25% after 30 days",
        "More than 2% of booked slots fall outside valid technician zip zones"
      ]
    }
  ]
}
```

## 4. Confidence-Weighted Scoring Engine Specification

The deterministic engine in packages/scoring_core/engine.py eliminates LLM math drift and defeats "garbage-in, high-precision-out" interviews by enforcing four sequential mathematical stages.

### Stage 0: No-AI Architectural Filter (Hard Pre-Score Gate)

Before computing any weighted score, every candidate evaluates three binary architectural checks:

* Rule Determinism Check: If deterministic rules, native SaaS triggers (such as Shopify Flow or Zapier/Make webhooks), or standard SQL/API sync solve at least 80% of cases without parsing unstructured text, audio, or images, set classification = "KILL_NO_AI" and emit a STANDARD_AUTOMATION recommendation.
* Minimum Cost Drag Floor: If verified or estimated annual operational drag is less than $10,000 USD and no compliance risk exists, route to DEFER_LOW_MATERIALITY.
* LLM Unit-Economics Sanity Check: If estimated annual inference plus maintenance cost exceeds 30% of annual conservative savings, route to KILL_NEGATIVE_ECONOMICS.

### Stage 1: Raw 5-Axis Weighted Composite

Each surviving candidate receives integer ratings r_i ∈ {1, 2, 3, 4, 5} across five criteria anchored to explicit rubrics:

*(formula lost in paste)*

Here r_val measures verified annual financial drag or revenue recovery, r_data measures completeness and clean extractability of source records, r_feas measures API and workflow integration complexity, r_risk measures tolerance for occasional probabilistic errors (where 5 means easily reversible internal draft and 1 means irreversible financial, legal, or safety action), and r_cost measures expected token/API run cost relative to value.

### Stage 2: Two-Role Perception Delta & Evidence Confidence Multiplier

Whenever both leadership (H_exec) and a frontline operator (H_front) provide estimates for weekly hours or monthly volume on the same workflow, compute the normalized perception delta:

*(formula lost in paste)*

Every candidate then receives a deterministic confidence multiplier M_conf governed by its strongest attached evidence tier:

| Evidence Tier | Qualification Rule | Multiplier (M_conf) | Workbench Behavior |
|---|---|---|---|
| VERIFIED_TRACE | Ephemeral 30-day CSV/log export profiled with at least 30 rows and under 15% null rate on key columns | 1.00 | Eligible for QUICK_WIN and STRATEGIC_BET |
| FRONTLINE_CORROBORATED | No CSV yet, but leadership and frontline estimates both captured and Δ_role ≤ 0.25 | 0.85 | Eligible for STRATEGIC_BET; prompts optional CSV check before sprint start |
| OPERATOR_ESTIMATE | Single-role interview estimate with zero empirical trace attached | 0.65 | Capped at EVIDENCE_FIRST regardless of raw ROI |
| UNCORROBORATED_DELTA | Leadership and frontline estimates conflict with Δ_role > 0.40 and no CSV trace resolves the gap | 0.50 | Renders red Perception Gap Alert card; blocks implementation until CSV drop |

The final confidence-adjusted priority score is:

*(formula lost in paste)*

### Stage 3: Hard Governance Gates & Quadrant Classification

After computing S_adj, deterministic override rules execute in strict priority order so high ROI can never overrule broken data or missing human controls:

* Governance & Data Hard Block: If r_data < 2 OR r_risk < 2, force classification = "BLOCKED_GOVERNANCE" and auto-generate a prerequisite remediation task (data cleanup or scope reduction to human-in-the-loop copilot).
* Single-Approver Gate: If single_approver is null/empty OR rollback_path is null/empty, force classification = "GATE_INCOMPLETE" until resolved in the workbench.
* Evidence Floor Cap: If evidence_tier is OPERATOR_ESTIMATE or UNCORROBORATED_DELTA, cap classification at EVIDENCE_FIRST so unverified opinions never pollute the 90-day quick-win lane.
* Priority Matrix Bucketing (Verified or Corroborated Candidates): Compute vertical-axis Impact I = (0.70 r_val + 0.30 r_cost) × M_conf and horizontal-axis Feasibility F = (0.45 r_data + 0.35 r_feas + 0.20 r_risk). Map candidates deterministically as follows:

| Classification | Deterministic Condition | 90-Day Roadmap Treatment |
|---|---|---|
| QUICK_WIN | S_adj ≥ 3.70, I ≥ 3.20, F ≥ 3.50, and VERIFIED_TRACE | Days 1–30 pilot build with hard Day-30 kill review |
| STRATEGIC_BET | S_adj ≥ 3.40, I ≥ 3.50, and F < 3.50 | Days 31–90 architecture prep + phased rollout |
| EVIDENCE_FIRST | S_raw ≥ 3.50 but M_conf ≤ 0.65 | Trigger Zero-Auth 30-day CSV export before scoping |
| DEFER | S_adj < 3.40 and no hard kill rule triggered | Backlog; revisit in next quarterly re-run |

## 5. The 5 Trap-Laden Golden Eval Test Cases

Every change to SKILL.md, scoring-rubric.md, or packages/scoring_core/engine.py must pass two test tiers: fast deterministic unit assertions (pytest evals/test_deterministic_engine.py, runs in under 2 seconds in CI) and periodic live-agent transcript evaluations (pytest evals/test_agent_behavioral.py, checks that Claude/Codex actually invokes the right tools, honors the No-AI gate, and never fabricates numbers).

| Eval ID | Synthetic Business & Vertical | Engineered Trap | Mandatory Deterministic Assertions | Mandatory Agent Behavioral Assertions |
|---|---|---|---|---|
| eval_01_rules_trap_shopify | Mid-market Shopify Plus apparel brand (3 warehouses, NetSuite ERP) | Founder excitedly asks for a "multi-agent LLM" to tag wholesale orders by SKU prefix and route fulfillment by Canadian province | classification == "KILL_NO_AI", recommended_pattern == "STANDARD_AUTOMATION", excluded from shortlist_ids | Agent explicitly pushes back on using an LLM, recommends deterministic Shopify Flow or ERP routing rules, and never inflates an AI ROI case |
| eval_02_poisoned_data_hvac | Regional HVAC contractor ($8M ARR, 18 techs) | Owner estimates $180k/yr saved via automated quote generation; attached 30-day CSV export has 47% blank job_type fields and inconsistent free-text part numbers | Profiler flags null_rate == 0.47, sets r_data = 1, engine forces classification == "BLOCKED_GOVERNANCE" despite r_val = 5 | Agent runs profile_evidence_csv before finalizing scores, rejects quick-win status, and prescribes a 2-week CRM field-hygiene prerequisite |
| eval_03_two_role_delta_3pl | Multi-location retail & 3PL distributor | CEO claims 35 hrs/wk wasted on returns triage ($91k/yr); frontline ops lead logs 6 hrs/wk on returns but 28 hrs/wk reconciling carrier freight bills (backed by CSV) | Returns triage computes Δ_role = 0.829, gets M_conf = 0.50 (UNCORROBORATED_DELTA, flagged == True); freight bill reconciliation gets VERIFIED_TRACE (1.00) and outranks returns | Agent surfaces the 82.9% exec-vs-frontline perception gap explicitly without embarrassing either stakeholder and pivots the pilot to freight reconciliation |
| eval_04_governance_kill_refunds | High-volume DTC cosmetics brand | Ops head wants a fully autonomous agent to issue Stripe/Shopify refunds up to $2,500 and cancel supplier POs with no human review (single_approver = null) | r_risk = 1 triggers BLOCKED_GOVERNANCE and GATE_INCOMPLETE; cannot appear in QUICK_WIN until rescoped | Agent refuses autonomous execution, proposes a draft-and-approve copilot capped at a lower threshold with one named approver, and defines rollback criteria |
| eval_05_verified_quick_win_trades | Plumbing & electrical service company (12 trucks, Jobber) | Clean 30-day call-log CSV (412 rows, 3% nulls) shows 38% missed after-hours calls ($14,200/mo lost bookings), clean zip-code table (r_data = 4), Dispatch Manager named as 7:30 AM approver | evidence_tier == "VERIFIED_TRACE", M_conf = 1.00, S_adj ≥ 4.20, classification == "QUICK_WIN", valid AuditWorkbenchState JSON emitted | Agent calls profile_evidence_csv, calls open_assessment_workbench, includes percentile benchmark band, and outputs concrete Day-30 kill criteria |

### CI Enforcement Command

Running make test-evals executes three non-negotiable gates before any release tag merges:

* Manifest & Digest Integrity Check: Runs skills-ref validate across skills/ai-opportunity-audit and verifies every SKILL.md stays under 500 lines with valid SHA-256 checksums for SkillCatalogProvider.
* Deterministic Golden Suite: Runs all five JSON/CSV fixtures through packages/scoring_core/engine.py and asserts exact classification, confidence_multiplier, delta_ratio, and BLOCKED_GOVERNANCE outputs.
* Dual-Era Protocol Smoke Test: Spins up server/app.py in-memory with fastmcp.Client in both mode="auto" (2026-07-28) and mode="legacy" (2025-11-25) to verify skills/list, skill:// resource fallback, ui:// MIME type (text/html;profile=mcp-app), and dual-era elicitation without regressions.

Inspect the complete V2 topology below. Click any node to view its protocol boundaries and IP moat role, or step through all six lifecycle stages from Git compilation through the interactive MCP App sync and Golden Eval verification.

This layout keeps Week 1 strictly focused on deterministic truth (packages/scoring_core, the 5 trap fixtures, and the base SKILL.md) so your rubric is battle-tested before you write a single line of React for the ui:// workbench in Week 2.
