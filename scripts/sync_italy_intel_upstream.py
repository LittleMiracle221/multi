#!/usr/bin/env python3
"""
同步上游 italy_intel GitHub 仓库的变更，并把 diff 元数据落到本地。

设计目标：
- 只负责“发现更新 + 记录变更”
- 不在脚本里硬编码 AI 总结逻辑
- 让后续人工或自动化代理基于产物更新 AU / CA / FR 的研究 playbook
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/RickyShiJs/italy_intel.git"
REPO_URL = os.environ.get("ITALY_INTEL_REPO_URL", DEFAULT_REPO_URL).strip() or DEFAULT_REPO_URL
ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_DIR = ROOT / ".cache" / "upstreams" / "italy_intel"
STATE_FILE = ROOT / "state" / "italy_intel_sync.json"
RUNS_DIR = ROOT / "upstream_sync" / "runs"
PATCHES_DIR = ROOT / "upstream_sync" / "patches"


@dataclass
class CommandResult:
    stdout: str


def run_git(*args: str, cwd: Path | None = None) -> CommandResult:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed with code {proc.returncode}: "
            f"{proc.stderr.strip() or proc.stdout.strip()}"
        )
    return CommandResult(stdout=proc.stdout.strip())


def ensure_dirs() -> None:
    for path in (UPSTREAM_DIR.parent, STATE_FILE.parent, RUNS_DIR, PATCHES_DIR):
        path.mkdir(parents=True, exist_ok=True)


def clone_or_fetch() -> None:
    if not UPSTREAM_DIR.exists():
        run_git("clone", "--quiet", REPO_URL, str(UPSTREAM_DIR))
        return
    run_git("-C", str(UPSTREAM_DIR), "fetch", "--quiet", "origin")


def get_head_commit() -> str:
    return run_git("-C", str(UPSTREAM_DIR), "rev-parse", "origin/HEAD").stdout


def ensure_origin_head_symbolic_ref() -> None:
    try:
        run_git("-C", str(UPSTREAM_DIR), "remote", "set-head", "origin", "--auto")
    except RuntimeError:
        # 某些仓库/网络状态下 set-head 可能失败，后面会尝试直接解析默认分支
        pass


def get_default_branch() -> str:
    ref = run_git(
        "-C", str(UPSTREAM_DIR), "symbolic-ref", "refs/remotes/origin/HEAD"
    ).stdout
    return ref.rsplit("/", 1)[-1]


def resolve_head_commit() -> tuple[str, str]:
    ensure_origin_head_symbolic_ref()
    branch = get_default_branch()
    commit = run_git("-C", str(UPSTREAM_DIR), "rev-parse", f"origin/{branch}").stdout
    return branch, commit


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def get_commit_subject(commit: str) -> str:
    return run_git(
        "-C", str(UPSTREAM_DIR),
        "log",
        "-1",
        "--format=%s",
        commit,
    ).stdout


def get_commit_date(commit: str) -> str:
    return run_git(
        "-C", str(UPSTREAM_DIR),
        "log",
        "-1",
        "--format=%cI",
        commit,
    ).stdout


def get_commit_range_log(old_commit: str, new_commit: str) -> str:
    return run_git(
        "-C", str(UPSTREAM_DIR),
        "log",
        "--reverse",
        "--format=%H%x09%cI%x09%s",
        f"{old_commit}..{new_commit}",
    ).stdout


def get_changed_files(old_commit: str, new_commit: str) -> list[str]:
    out = run_git(
        "-C", str(UPSTREAM_DIR),
        "diff",
        "--name-only",
        old_commit,
        new_commit,
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def write_patch(old_commit: str, new_commit: str, stamp: str) -> Path:
    patch = run_git(
        "-C", str(UPSTREAM_DIR),
        "diff",
        "--binary",
        old_commit,
        new_commit,
    ).stdout
    patch_path = PATCHES_DIR / f"{stamp}_{old_commit[:7]}_{new_commit[:7]}.patch"
    patch_path.write_text(patch, encoding="utf-8")
    return patch_path


def write_run_summary(
    *,
    stamp: str,
    branch: str,
    old_commit: str,
    new_commit: str,
    changed_files: list[str],
    patch_path: Path,
) -> Path:
    log_text = get_commit_range_log(old_commit, new_commit)
    subject = get_commit_subject(new_commit)
    commit_date = get_commit_date(new_commit)
    summary_path = RUNS_DIR / f"{stamp}_italy_intel_update.md"

    lines = [
        f"# italy_intel update {stamp}",
        "",
        f"- Source repo: `{REPO_URL}`",
        f"- Default branch: `{branch}`",
        f"- Previous commit: `{old_commit}`",
        f"- New commit: `{new_commit}`",
        f"- New commit date: `{commit_date}`",
        f"- New commit subject: {subject}",
        f"- Patch archive: `{patch_path.relative_to(ROOT)}`",
        "",
        "## Changed files",
        "",
    ]

    if changed_files:
        lines.extend([f"- `{path}`" for path in changed_files])
    else:
        lines.append("- None reported by git diff")

    lines.extend(
        [
            "",
            "## Commit log",
            "",
        ]
    )

    if log_text:
        for row in log_text.splitlines():
            commit, committed_at, message = row.split("\t", 2)
            lines.append(f"- `{commit[:7]}` | `{committed_at}` | {message}")
    else:
        lines.append("- No intermediate commits listed")

    lines.extend(
        [
            "",
            "## Next review checklist",
            "",
            "- 看这次变化是不是新增了可复用的渠道、关键词、提示词、打分规则或输出 schema。",
            "- 把纯意大利本地法规细节和可迁移的方法拆开。",
            "- 只把对 AU / CA / FR 真有帮助的部分写入 `references/upstream-learning.md`。",
            "- 如有必要，再更新 `references/markets/*.md` 或执行脚本。",
        ]
    )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary_path


def bootstrap_state(branch: str, commit: str) -> None:
    save_state(
        {
            "repo_url": REPO_URL,
            "default_branch": branch,
            "last_seen_commit": commit,
            "last_seen_subject": get_commit_subject(commit),
            "last_seen_commit_date": get_commit_date(commit),
            "last_checked_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )


def main() -> int:
    ensure_dirs()
    clone_or_fetch()

    branch, head_commit = resolve_head_commit()
    state = load_state()
    previous_commit = state.get("last_seen_commit")

    if not previous_commit:
        bootstrap_state(branch, head_commit)
        print(f"BOOTSTRAPPED::{head_commit}")
        return 0

    if previous_commit == head_commit:
        state.update(
            {
                "default_branch": branch,
                "last_checked_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        )
        save_state(state)
        print(f"NO_CHANGE::{head_commit}")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    changed_files = get_changed_files(previous_commit, head_commit)
    patch_path = write_patch(previous_commit, head_commit, stamp)
    summary_path = write_run_summary(
        stamp=stamp,
        branch=branch,
        old_commit=previous_commit,
        new_commit=head_commit,
        changed_files=changed_files,
        patch_path=patch_path,
    )

    state.update(
        {
            "repo_url": REPO_URL,
            "default_branch": branch,
            "last_seen_commit": head_commit,
            "last_seen_subject": get_commit_subject(head_commit),
            "last_seen_commit_date": get_commit_date(head_commit),
            "last_checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "last_summary_path": str(summary_path.relative_to(ROOT)),
            "last_patch_path": str(patch_path.relative_to(ROOT)),
        }
    )
    save_state(state)

    print(f"UPDATED::{summary_path}::{patch_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        raise SystemExit(130)
