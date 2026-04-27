# italy_intel manual sync 2026-04-27

- Sync date: `2026-04-27` (Asia/Shanghai)
- Upstream repo: `git@github.com:RickyShiJs/italy_intel.git`
- Latest upstream commit: `cadbf897f6895c498fc81845b943d0ea9083d45e`
- Commit date: `2026-04-27T16:51:42+08:00`
- Commit subject: `thread telegram into daily report pipeline`

## What changed upstream

- Telegram was upgraded from a standing coverage gap to a connected source in the Italy workflow.
- Telegram messages were explicitly threaded into the same lead filtering, 5A scoring, and `daily_themes` pipeline as Reddit and Twitter.
- The upstream schema guidance was tightened so fixed coverage gaps and runtime failures are no longer mixed together.

## What was imported locally

- Recorded the transferable method in `references/upstream-learning.md`.
- Updated local `SKILL.md` to preserve current honesty (`Telegram` still not connected here) while documenting the correct future integration pattern.
- Updated `references/output-schema.md` with the imported naming and channel-normalization rules.

## What was not imported

- No Italy-specific Telegram channel list was copied into AU / CA / FR.
- No false claim of Telegram support was added to the local multi-market workflow.
- No local Telegram scanner was implemented in this sync pass.
