# Note templates (copy only the sections that apply; delete empty ones)

Frontmatter for every note:
```
---
project: Nova DAW
type: architecture | decision | bug | research | feature | ai | performance | learning | devlog | milestone | dashboard
status: IDEA | RESEARCH | PLANNED | IN-PROGRESS | IMPLEMENTED | VERIFIED | BLOCKED | DEPRECATED
priority: P0 | P1 | P2
updated: YYYY-MM-DD
tags: [nova, ...]
---
```

## Architecture: `<System Name>` (e.g. Audio Engine Architecture)
Purpose · Responsibilities · Components · Data Flow · Thread Ownership · Dependencies · Failure Modes · Performance Considerations · Current Limitations · Future Work · Related Code (paths) · Related

## Decision: `DECISION - <Name>`
Date · Problem · Options (A/B/C) · Decision · Why · Trade-offs · Risks · Future Revisit Condition · Related (link the architecture note and the `DECISIONS.md` id D-NNN)

## Bug: `<Symptom as a sentence>`
Problem · Reproduction · **Root Cause** · Investigation · Fix · Verification (command → result) · Regression Test (path) · Related Systems
Never store only the error message.

## Research: `RESEARCH - <Question>`
Question · What We Learned · Important Concepts · Useful Patterns · Risks · How Nova Can Apply It · What We Should NOT Copy · Sources · Related
Reverse-engineering research (REA, where lawful) instead: Research Goal · Target Behavior · Observations · Architecture Insight · Hypothesis · Verification · Application to Nova.
Insights only. No dumped pseudo-code, decompiled output or long article text.

## AI system: `<System Name>` (e.g. Mix Problem Detector)
Input · Analysis · Features · Output · Confidence · Project Actions · Undo Integration · Performance Cost · Known Limitations · False-Positive Risks · Testing

## Performance log (one table; milestones and regressions only)
| Date | Build | Scenario | Tracks | Plugins | Buffer | Sample rate | CPU | RAM | Dropouts | Render speed | UI FPS | Notes |

## Dev log: `YYYY-MM-DD - Development Log`
Completed · Fixed · Found · Next · Notes (important things only, no command history)

## Learning: in `17 - Learning`
Concept · Why It Matters · Example in Nova · Common Mistakes · What To Remember
Written so the owner can read and understand it without prior knowledge.

## Milestone: `MILESTONE - <Name>`
What We Built · What Works · What Doesn't · Architecture Changes · Performance · Important Bugs · Lessons Learned · Technical Debt · Next Milestone

## Dashboard: `Project Nova DAW - Dashboard` (the front page)
Current Status · Current Priority (P0/P1/P2) · Recent Work · Current Problems · Architecture · Roadmap · Research · Decisions · Performance · AI · Next Actions, all as `[[links]]` plus one-line summaries, mirroring `PROJECT_STATE.md`.

## Project Map: `Nova DAW - Project Map`
Core · Audio · Plugin · Rendering · AI · Quality · Research: link lists to the hub notes.

## Suggested folders (create only when non-empty)
00 Dashboard · 01 Project · 02 Architecture · 03 Audio Engine · 04 DSP · 05 Plugin System · 06 Sequencer · 07 Mixer · 08 AI · 09 UI UX · 10 Research · 11 Bugs · 12 Decisions · 13 Performance · 14 Testing · 15 Releases · 16 Ideas · 17 Learning · 99 Archive
