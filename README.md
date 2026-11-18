# bochen-answer-style-skill

[![CI](https://github.com/bochensu0-web/bochen-answer-style-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/bochensu0-web/bochen-answer-style-skill/actions/workflows/ci.yml)

为苏博晨定制的中文全局回答风格 Skill 与常驻规则包（兼容 **Antigravity**、**Codex**、**Claude Code** 及支持 Agent Skills 规范的客户端）。

核心目标：**结论前置、篇幅随问题大小伸缩、机制与最小例子优先、少套话低 AI 腔、事实与推断边界清晰**。

## 仓库结构

```text
bochen-answer-style-skill/
├── SKILL.md                        # 标准 Agent Skill 主文件（可直接克隆即用）
├── agents/openai.yaml              # 客户端 UI 元数据
├── rules/AGENTS.md                 # 常驻全局规则版（适配 GEMINI.md / AGENTS.md / CLAUDE.md）
├── examples/before-after.md        # 5 类高频场景“AI 腔 vs 博晨风格”改写对照
├── evals/bochen-answer-style.json  # 6 组正向触发与格式例外评测用例
├── scripts/install.py              # 支持 Skill / Rule 双模式安装脚本
├── tests/test_skill.py             # 结构、编码、链接与幂等安装测试
└── LICENSE
```

## 两种使用方式

### 1. 作为按需 Skill 安装（标准 Agent Skills 目录）

可直接克隆到客户端 `skills/` 目录：

```bash
# Antigravity
git clone https://github.com/bochensu0-web/bochen-answer-style-skill.git ~/.gemini/config/skills/bochen-answer-style

# Codex
git clone https://github.com/bochensu0-web/bochen-answer-style-skill.git ~/.codex/skills/bochen-answer-style
```

或使用内置安装脚本：

```bash
python scripts/install.py --client antigravity --mode skill
python scripts/install.py --client codex --mode skill
```

### 2. 作为常驻全局规则写入（免手动触发，推荐）

回答风格属于跨任务的全局表达层，写入客户端全局规则文件后无需每轮手动指定 `$bochen-answer-style`（脚本会自动幂等追加，不覆盖你原有的其他规则）：

```bash
# 写入 ~/.gemini/GEMINI.md（Antigravity 全局常驻）
python scripts/install.py --client antigravity --mode rule

# 同时安装 Skill 与常驻规则
python scripts/install.py --client antigravity --mode both
```

## 风格要点速览

- **前 1–3 句给结论或推荐**，再讲最关键的 2–3 个机制，不复述题目、不寒暄。
- **小问题短答，大问题深讲**：一句话能说清的不写长教程；首次出现术语配一句白话定义和数字/代码小例子。
- **删掉无信息套话**：不用“作为 AI”“值得注意的是”“总而言之”“希望对你有帮助”，不用机械的“首先、其次、最后”。
- **尊重任务格式例外**：公文通知、英文论文、固定模板或逐字翻译优先服从任务格式。
- **可信度优先**：区分事实、推断与建议；涉及当前产品规格、价格、政策或模型表现时先核实最新来源。

具体改写对比见 [`examples/before-after.md`](examples/before-after.md)，配套专项学习/算法/论文套件见 [`bochen-ai-skills`](https://github.com/bochensu0-web/bochen-ai-skills)。

## 本地测试

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## License

MIT — 见 [`LICENSE`](LICENSE)。
