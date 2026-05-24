# academic-research

> 学术科研全流程智能助手 — Claude Code Skill v3.0

覆盖从选题开题、文献综述、实验设计、数据处理、公式推导、论文润色、投稿准备、代码文档、学术海报、答辩PPT到学位论文的**13个模块完整研究闭环**。

## 安装

```bash
# 方式一：Claude Code 内置安装
claude plugins install academic-research@your-github

# 方式二：手动安装
# 将本仓库克隆到 ~/.claude/skills/academic-research/
git clone https://github.com/your-user/academic-research.git \
  ~/.claude/skills/academic-research/
```

## 快速开始

触发词覆盖全流程学术场景，Claude Code 自动路由到对应模块：

| 你说... | 触发模块 |
|---------|----------|
| "帮我看看这个方向怎么选题" | `topic-proposal` |
| "梳理一下 XXX 领域的研究现状" | `literature-review` |
| "这个实验怎么设计" | `experiment-design` |
| "CSV 数据做个统计分析" | `data-processing` |
| "推导一下这个公式" | `formula-derivation` |
| "这段文字润色一下去掉AI味" | `paper-polish` |
| "帮我写个 Cover Letter" | `paper-submission` |
| "生成项目 README 和复现说明" | `code-documentation` |
| "做个会议海报" | `academic-poster` |
| "做个答辩 PPT" | `ppt-presentation` |
| "编译我的学位论文" | `latex-thesis` |

无需手动指定模块，skill 根据请求内容自动路由。多模块组合按数据流串行执行（如选题→文献综述→开题报告）。

## 项目结构

```
academic-research/
├── SKILL.md                      # 主入口：路由表 + 工作流 + 安全边界
├── README.md                     # 本文件
│
├── scripts/                      # 共享工具脚本
│   ├── dep_check.py              #   依赖预检 + 按需安装
│   ├── quick_stats.py            #   纯 stdlib 数据概览（秒级，无需 pip）
│   ├── analysis_report.py        #   CSV → .tex → PDF 一键管道
│   └── encoding_safe.py          #   Windows GBK 终端安全包装
│
├── references/
│   ├── modules/                  # 13 个模块参考文件
│   │   ├── TOPIC_PROPOSAL.md     #   选题开题：五维评估 + 创新点矩阵
│   │   ├── LITERATURE_REVIEW.md  #   文献综述：三种组织方式 + 批判性写作
│   │   ├── EXPERIMENT_DESIGN.md  #   实验设计：样本量估算 + 变量控制
│   │   ├── DATA_PROCESSING.md    #   数据处理：快速管道 + 完整统计检验
│   │   ├── FORMULA_DERIVATION.md #   公式推导：步骤验证 + 数值验证
│   │   ├── PAPER_POLISH.md       #   论文润色：8种AI味特征 + .docx/.tex 直编
│   │   ├── PAPER_SUBMISSION.md   #   论文投稿：Cover Letter + Rebuttal 策略
│   │   ├── CODE_DOCUMENTATION.md #   代码文档：README + 复现说明 + docstring
│   │   ├── ACADEMIC_POSTER.md    #   学术海报：HTML/LaTeX + 杂志风/瑞士风
│   │   ├── PPT_PRESENTATION.md   #   PPT制作：2种模板 × 9套主题色 × 32种布局
│   │   ├── RESEARCH_REPORT.md    #   科研报告：阶段性汇报模板
│   │   ├── COURSE_QA.md          #   课程答疑：由浅入深知识梳理
│   │   ├── LATEX_THESIS.md       #   学位论文：串行诊断 + 模板检测
│   │   ├── OUTPUT_DOCX.md        #   DOCX 输出格式参考
│   │   └── OUTPUT_LATEX.md       #   LaTeX 输出格式参考
│   │
│   ├── latex/                    # LaTeX 论文子系统
│   │   ├── SKILL.md              #   LaTeX 模块详细信息
│   │   ├── scripts/              #   17 个诊断/编译/检查脚本
│   │   │   ├── compile.py        #     XeLaTeX 编译引擎
│   │   │   ├── detect_template.py #   模板检测
│   │   │   ├── deai_check.py     #    去AI味批量检查
│   │   │   ├── check_format.py   #    格式合规检查
│   │   │   ├── verify_bib.py     #    参考文献验证
│   │   │   └── ...               #    13 个其他诊断脚本
│   │   ├── references/           #   LaTeX 专项参考（国标/学术规范/去AI味指南）
│   │   └── templates/            #   高校模板（北大/清华/燕山）
│   │
│   └── ppt/                      # PPT 子系统
│       ├── SKILL.md              #   PPT 模块详细信息
│       ├── assets/               #   模板文件 (magazine A / swiss B)
│       └── references/           #   主题色/布局/动效参考
```

## 模块详解

### 内容生产层

| 模块 | 输入 | 输出 | 关键特性 |
|------|------|------|----------|
| `literature-review` | 研究主题 | 综述框架 + 对比表 + 空白分析 | 避免流水账式综述 |
| `data-processing` | CSV/Excel/描述 | 统计报告 + 可视化 + 结论 | 效应量必报，4个工具脚本 |
| `formula-derivation` | 目标公式 | 推导全过程 + 验证 | 每步有依据，强制验证 |
| `paper-polish` | .docx/.tex/文本 | 润色对照 + AI味诊断 | 8种中文AI味特征检测 |

### 决策支持层

| 模块 | 核心能力 |
|------|----------|
| `topic-proposal` | 五维评估（创新性/可行性/重要性/可扩展性/匹配度）、创新点矩阵（问题×方法） |
| `experiment-design` | 6种实验类型、样本量估算（效应量+统计功效）、变量控制清单 |
| `course-qa` | 概念解释、由浅入深、举例说明 |

### 成果输出层

| 模块 | 核心能力 |
|------|----------|
| `paper-submission` | Cover Letter 模板、Rebuttal 逐条回复策略、期刊匹配、22项投稿检查 |
| `code-documentation` | README 模板、复现说明（Reproduction Guide）、docstring 规范 |
| `academic-poster` | HTML/LaTeX 双模式、A0 布局、杂志风/瑞士风双风格 |
| `ppt-presentation` | 单文件 HTML 横向翻页、WebGL 背景、Motion One 动效 |

### 专业输出层

| 模块 | 核心能力 |
|------|----------|
| `research-report` | 阶段性汇报：背景→内容→成果→计划 |
| `latex-thesis` | 17个诊断脚本、串行诊断、模板检测、国标检查 |

## 输出格式

所有内容模块支持三种输出：

| 格式 | 触发词 | 技术路径 |
|------|--------|----------|
| Markdown | 默认 | 直接输出 |
| DOCX | "生成 Word" | `docx-js` → `validate.py` |
| LaTeX/PDF | "导出 PDF" | `.tex` → `compile.py` (XeLaTeX) → `.pdf` |

## 平台兼容

- **Windows GBK**：所有中文输出脚本设置 `PYTHONIOENCODING=utf-8:replace`
- **LaTeX**：统一 XeLaTeX 引擎（`compile.py` 自动检测）
- **DOCX**：XML 中文使用实体编码，避免 GBK 解码错误
- **Python**：`scripts/dep_check.py` 预检依赖，只安装缺失包

## 安全边界

- 不编造学术数据、实验结果或研究结论
- 公式推导不跳步，必须包含至少一种验证方法
- 论文润色不改变作者学术观点
- PPT/Poster 不编造引用、基金声明或学术主张
- LaTeX 模块不直接修改 `\cite{}`、`\ref{}`、数学块、模板宏命令
- PPT 风格 A/B 不混用，主题色只用预设

## 版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.0 | 2026-05-24 | 新增5模块（topic-proposal/experiment-design/paper-submission/academic-poster/code-documentation）→ 13模块全流程闭环 |
| v2.0 | 2026-05-23 | 新增工具脚本层（dep_check/quick_stats/analysis_report/encoding_safe）、平台兼容 |
| v1.4 | 2026-05 | 初始版本：8模块 + docx/tex输出 |

## 许可

MIT License — 详见 [LICENSE](LICENSE)
