# LaTeX学位论文模块（完整版）

> 本模块整合自 latex-thesis-zh，处理中文 LaTeX 学位论文项目。

## 概述

使用此模块处理已有中文 LaTeX 学位论文项目中的定向问题。保持低摩擦：先判断最小匹配模块，再运行对应脚本，最后以论文审阅友好的格式返回问题和建议。

## 能力

- 编译并诊断 XeLaTeX / LuaLaTeX / latexmk 构建问题
- 检查论文格式、GB/T 7714 相关要求、章节结构、模板类型和术语一致性
- 审阅逻辑连贯性、文献综述质量、标题后导语完整性、实验章节写法、标题表达与 AI 痕迹
- 针对文献综述提供"共识 -> 分歧 -> 局限 -> 空白 -> 本文切入点"的重写蓝图
- 在不破坏引用、标签和数学环境的前提下给出可落地的中文论文修改建议

## 触发场景

- 编译失败或工具链不确定
- 学位论文格式、国标或学校模板检查
- 章节结构梳理或模板识别
- 术语、缩略语、命名一致性检查
- 逻辑连贯性、文献综述质量、标题后导语完整性检查
- 文献综述重写、比较分析不足、研究空白推导薄弱
- 标题优化、学术表达或去 AI 化检查
- 实验章节语言与结构审阅

## 不适用场景

- 英文会议或期刊论文
- Typst 项目
- 仅有 DOCX/PDF、没有 LaTeX 源文件的场景
- 从零写一篇学位论文

## 模块路由

| 模块 | 使用场景 | 命令 | 参考文件 |
|------|----------|------|----------|
| `compile` | 编译失败 | `uv run python scripts/compile.py main.tex` | `references/latex/references/modules/COMPILE.md` |
| `format` | 格式检查 | `uv run python scripts/check_format.py main.tex` | `references/latex/references/modules/FORMAT.md` |
| `structure` | 结构梳理 | `uv run python scripts/map_structure.py main.tex` | `references/latex/references/STRUCTURE_GUIDE.md` |
| `consistency` | 术语一致性 | `uv run python scripts/check_consistency.py main.tex --terms` | `references/latex/references/modules/CONSISTENCY.md` |
| `template` | 模板识别 | `uv run python scripts/detect_template.py main.tex` | `references/latex/references/modules/TEMPLATE.md` |
| `bibliography` | 参考文献 | `uv run python scripts/verify_bib.py references.bib --standard gb7714` | `references/latex/references/modules/BIBLIOGRAPHY.md` |
| `title` | 标题优化 | `uv run python scripts/optimize_title.py main.tex --check` | `references/latex/references/modules/TITLE.md` |
| `deai` | 去AI化 | `uv run python scripts/deai_check.py main.tex --section introduction` | `references/latex/references/modules/DEAI.md` |
| `logic` | 逻辑审阅 | `uv run python scripts/analyze_logic.py main.tex --section related` | `references/latex/references/modules/LOGIC.md` |
| `literature` | 文献综述 | `uv run python scripts/analyze_literature.py main.tex --section related` | `references/latex/references/modules/LITERATURE.md` |
| `experiment` | 实验章节 | `uv run python scripts/analyze_experiment.py main.tex --section experiments` | `references/latex/references/modules/EXPERIMENT.md` |
| `tables` | 表格校验 | `uv run python scripts/check_tables.py main.tex` | `references/latex/references/modules/TABLES.md` |
| `abstract` | 摘要诊断 | `uv run python scripts/analyze_abstract.py main.tex --lang zh` | `references/latex/references/modules/ABSTRACT.md` |

## 路由规则

- 先根据用户问题自动推断模块，不把"你想用哪个模块"当成默认追问
- 如果一个请求同时包含 2-3 个兼容目标，按固定顺序串行执行：`template` -> `compile` -> `format` -> `structure` / `consistency` -> `bibliography` -> `logic` / `literature` -> `experiment` / `title` / `deai` / `tables` / `abstract`
- 涉及模板不明、编译失败、学校规范不清时，优先 `template`
- 某个脚本失败时，先返回精确命令、退出码和关键报错

## 输入要求

- 论文入口文件，例如 `main.tex`
- 可选 `--section SECTION`，当用户只关注某一章或某一节
- 可选 bibliography 路径
- 可选学校/模板上下文（thuthesis、pkuthss 等）

## 输出规范

- 使用 LaTeX 友好的审阅格式返回问题：`% MODULE (L##) [Severity] [Priority]: ...`
- 明确给出执行的命令；若脚本失败，必须报告退出码和关键 stderr
- 将"检查结果"和"建议改写"分开陈述
- 默认保留 `\cite{}`、`\ref{}`、`\label{}`、数学环境、参考文献键和模板宏命令

## 工作流

1. 解析用户请求，锁定入口文件，推断模块；若缺参数，只追问缺失项
2. 若请求覆盖多个兼容模块，按路由规则顺序串行执行
3. 读取对应模块的参考文件
4. 运行对应脚本
5. 以审阅格式返回结果

## 安全边界

- 不编造引用、资助声明、致谢或学术主张
- 不修改 `\cite{}`、`\ref{}`、`\label{}`、数学块、参考文献键和模板宏命令（除非用户明确要求）
- 标题建议、去AI化修改、逻辑评论作为建议返回，不直接修改源文件

## 资源文件

```
references/latex/
├── SKILL.md                ← 完整的latex-thesis-zh原文
├── references/
│   ├── COMPILATION.md      ← 编译策略
│   ├── GB_STANDARD.md      ← GB/T 7714
│   ├── STRUCTURE_GUIDE.md  ← 章节结构
│   ├── LOGIC_COHERENCE.md  ← 逻辑连贯性
│   ├── TITLE_OPTIMIZATION.md
│   ├── DEAI_GUIDE.md
│   ├── modules/            ← 各模块详细参考
│   └── UNIVERSITIES/       ← 学校索引
├── templates/
│   ├── generic.md
│   ├── thuthesis.md
│   └── pkuthss.md
└── scripts/
    ├── compile.py
    ├── check_format.py
    ├── map_structure.py
    ├── detect_template.py
    └── ...
```

## 示例请求

- "帮我定位这个中文学位论文 main.tex 为什么 XeLaTeX 一直编译失败"
- "请梳理这篇硕士论文的章节结构，并检查术语是否前后统一"
- "按 GB/T 7714 帮我检查参考文献"
- "检查 related work 的逻辑链条和研究空白推导"
- "把文献综述从作者年份罗列改成按主题对话式写法"
- "帮我检查每一章、每一节、四级标题后有没有先写导语"

详细规则见 `references/latex/SKILL.md`
