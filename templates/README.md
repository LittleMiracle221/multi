# Report Templates

This directory stores reusable Markdown templates for recurring outputs in this
repo.

Files:
- `daily_market_report.md`: single-market daily intel report for `CA`, `AU`, or `FR`
- `cross_market_digest.md`: daily cross-market summary across `CA`, `AU`, and `FR`
- `failure_alert.md`: daily failure and gap alert
- `weekly_recap.md`: weekly trend recap

Usage notes:
- Copy the structure and replace `{{PLACEHOLDER}}` tokens with real values.
- Keep daily files append-only: create a new dated file for each run instead of
  overwriting old ones.
- Keep field names aligned with `SKILL.md` and
  `references/output-schema.md`.
