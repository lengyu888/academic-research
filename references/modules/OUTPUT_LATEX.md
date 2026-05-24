# LaTeX 输出参考

当用户要求"生成 tex""导出 LaTeX""编译 PDF"时，读取本文件，生成 .tex 后可选编译。

## 中文文档模板

生成 `.tex` 文件时使用以下模板结构（ctexart + XeLaTeX）：

```latex
\documentclass[12pt,a4paper]{ctexart}

% ===== 宏包 =====
\usepackage[top=2.5cm, bottom=2.5cm, left=3cm, right=2.5cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{titlesec}

% ===== 页面样式 =====
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\small\textcolor{gray}{学术文档}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% ===== 超链接 =====
\hypersetup{
  colorlinks=true,
  linkcolor=blue!60!black,
  urlcolor=blue!70!black,
  citecolor=green!50!black
}

% ===== 标题格式 =====
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection}{1em}{}

\title{[标题]}
\author{[作者]}
\date{\today}

\begin{document}
\maketitle

% === 在此处替换为各模块内容 ===

\end{document}
```

## 模块内容映射

### 文献综述 → LaTeX

```latex
\section{引言}
[研究意义和综述范围]

\section{研究现状}

\subsection{[主题/方向1]}
[综合分析该方向的研究进展]

\subsection{[主题/方向2]}
[综合分析]

\section{研究方法对比}
\begin{table}[htbp]
  \centering
  \caption{研究方法对比}
  \begin{tabular}{lllll}
    \toprule
    方法类别 & 代表工作 & 优势 & 局限性 & 适用场景 \\
    \midrule
    ... & ... & ... & ... & ... \\
    \bottomrule
  \end{tabular}
\end{table}

\section{当前研究的局限性}
\begin{itemize}[leftmargin=2em]
  \item 局限1
  \item 局限2
\end{itemize}

\section{未来研究方向}
\begin{itemize}[leftmargin=2em]
  \item 方向1
  \item 方向2
\end{itemize}

\section{本研究的定位}
[说明本研究如何填补上述空白]
```

### 数据处理 → LaTeX

```latex
\section{数据概览}
\begin{table}[htbp]
  \centering
  \caption{数据基本信息}
  \begin{tabular}{ll}
    \toprule
    项目 & 值 \\
    \midrule
    样本量 & $N = ...$ \\
    变量数 & ... \\
    \bottomrule
  \end{tabular}
\end{table}

\section{数据质量}
缺失值：... \\
异常值：... \\
数据预处理：...

\section{描述性统计}
\begin{table}[htbp]
  \centering
  \caption{描述性统计}
  \begin{tabular}{lccccc}
    \toprule
    变量 & 均值 & 标准差 & 最小值 & 最大值 & 中位数 \\
    \midrule
    ... & ... & ... & ... & ... & ... \\
    \bottomrule
  \end{tabular}
\end{table}

\section{分析结果}
[统计检验结果]

\section{结论}
\begin{itemize}[leftmargin=2em]
  \item 主要发现：...
  \item 局限性：...
  \item 建议：...
\end{itemize}
```

### 公式推导 → LaTeX

```latex
\section{问题描述}
[说明要推导什么，为什么重要]

\section{已知条件}
\begin{itemize}[leftmargin=2em]
  \item 前提假设：...
  \item 已知公式：...
\end{itemize}

\section{推导过程}

\textbf{Step 1:} [步骤名称]
\begin{align}
  [公式]
\end{align}
[解释这一步做了什么]

\textbf{Step 2:} [步骤名称]
\begin{align}
  [公式]
\end{align}
[解释]

\textbf{最终结果：}
\begin{equation}
  [最终公式]
\end{equation}

\section{结果解读}
\begin{itemize}[leftmargin=2em]
  \item 物理/实际意义：...
  \item 特殊情况：...
  \item 直觉理解：...
\end{itemize}

\section{应用举例}
[该公式的典型应用场景]
```

### 论文润色 → LaTeX

```latex
\section{润色范围}
\begin{table}[htbp]
  \centering
  \begin{tabular}{ll}
    \toprule
    项目 & 内容 \\
    \midrule
    文本长度 & ... \\
    润色语言 & ... \\
    润色重点 & ... \\
    \bottomrule
  \end{tabular}
\end{table}

\section{润色结果}

\subsection{第1段}
\textbf{原文：}
\begin{quote}
  [原文内容]
\end{quote}

\textbf{润色后：}
\begin{quote}
  [润色后内容]
\end{quote}

\textbf{修改说明：}
\begin{table}[htbp]
  \centering
  \begin{tabular}{llll}
    \toprule
    修改点 & 原文 & 修改后 & 修改原因 \\
    \midrule
    ... & ... & ... & ... \\
    \bottomrule
  \end{tabular}
\end{table}

\section{整体建议}
\begin{enumerate}[leftmargin=2em]
  \item 建议1
  \item 建议2
\end{enumerate}

\section{常见问题汇总}
\begin{table}[htbp]
  \centering
  \begin{tabular}{lc}
    \toprule
    问题类型 & 出现次数 \\
    \midrule
    ... & X 次 \\
    \bottomrule
  \end{tabular}
\end{table}
```

## 编译流程

生成 `.tex` 文件后，可选编译为 PDF：

```bash
# 方式一：用 latex-thesis 模块的 compile.py（推荐）
uv run python "C:/Users/28482/.claude/skills/academic-research/references/latex/scripts/compile.py" output.tex

# 方式二：直接用 latexmk（需已安装 TeX Live）
latexmk -xelatex -interaction=nonstopmode output.tex
```

编译要求：
- TeX Live 或 MiKTeX 已安装
- XeLaTeX 引擎（中文文档必须）
- ctex 宏包已安装

## 注意事项

- 中文文档必须用 `ctexart` 文档类 + XeLaTeX 引擎
- 表格用 `booktabs`（`\toprule`/`\midrule`/`\bottomrule`），比 `\hline` 更专业
- 公式环境：行内用 `$...$`，独立公式用 `equation`，多行对齐用 `align`
- 图片用 `graphicx` 的 `\includegraphics`，需指定路径
- 生成后先让用户检查 .tex 内容，再决定是否编译
- 如果用户已有论文项目，应将内容写入对应章节文件而非新建独立文档
