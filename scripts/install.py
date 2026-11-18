"""Install bochen-answer-style as a Skill, a Global Rule, or both."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "bochen-answer-style"

SKILL_TARGETS: dict[str, Path] = {
    "antigravity": Path.home() / ".gemini" / "config" / "skills",
    "codex": Path.home() / ".codex" / "skills",
    "claude": Path.home() / ".claude" / "skills",
    "agents": Path.cwd() / ".agents" / "skills",
}

RULE_TARGETS: dict[str, Path] = {
    "antigravity": Path.home() / ".gemini" / "GEMINI.md",
    "codex": Path.home() / ".codex" / "AGENTS.md",
    "claude": Path.home() / ".claude" / "CLAUDE.md",
    "agents": Path.cwd() / "AGENTS.md",
}

SKILL_ITEMS = ("SKILL.md", "README.md", "LICENSE", "agents", "examples")
RULE_MARKER = "# 全局回答风格规则（Bochen Answer Style）"


def install_skill(skill_root: Path, *, dry_run: bool = False) -> Path:
    dest = skill_root / SKILL_NAME
    if not dry_run:
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for item in SKILL_ITEMS:
            src = REPO_ROOT / item
            target = dest / item
            if src.is_dir():
                shutil.copytree(src, target)
            elif src.is_file():
                shutil.copy2(src, target)
    return dest


def install_rule(rule_file: Path, *, dry_run: bool = False) -> Path:
    rule_content = (REPO_ROOT / "rules" / "AGENTS.md").read_text(encoding="utf-8").strip() + "\n"
    if not dry_run:
        rule_file.parent.mkdir(parents=True, exist_ok=True)
        if rule_file.exists():
            existing = rule_file.read_text(encoding="utf-8")
            if RULE_MARKER not in existing:
                sep = "\n\n" if existing and not existing.endswith("\n\n") else ""
                rule_file.write_text(existing.rstrip() + sep + "\n\n" + rule_content, encoding="utf-8")
        else:
            rule_file.write_text(rule_content, encoding="utf-8")
    return rule_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install bochen-answer-style skill or rule.")
    parser.add_argument(
        "--client",
        choices=sorted(SKILL_TARGETS.keys()),
        default="antigravity",
        help="Client preset (default: antigravity).",
    )
    parser.add_argument(
        "--mode",
        choices=("skill", "rule", "both"),
        default="skill",
        help="Install as on-demand skill, always-on rule, or both (default: skill).",
    )
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=None,
        help="Override target skills parent directory.",
    )
    parser.add_argument(
        "--rule-file",
        type=Path,
        default=None,
        help="Override target rule Markdown file path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show target paths without modifying files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    prefix = "[dry-run] Would write" if args.dry_run else "Installed"

    if args.mode in ("skill", "both"):
        sdir = args.skill_dir if args.skill_dir is not None else SKILL_TARGETS[args.client]
        dest = install_skill(sdir, dry_run=args.dry_run)
        print(f"{prefix} skill -> {dest}")

    if args.mode in ("rule", "both"):
        rfile = args.rule_file if args.rule_file is not None else RULE_TARGETS[args.client]
        dest_rule = install_rule(rfile, dry_run=args.dry_run)
        print(f"{prefix} rule  -> {dest_rule}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
