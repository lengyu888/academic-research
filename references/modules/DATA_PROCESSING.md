# 数据处理模块

## 触发场景

- 用户有实验数据需要分析
- 用户需要数据清洗、统计分析、可视化
- 用户需要假设检验或回归分析
- 用户对分析结果有疑问

## 工作流程

### 0. 环境准备（必须第一步执行）

**先检查依赖，缺失时再安装。不要盲目安装所有包。**

```python
# 在分析脚本顶部加入依赖检查
import subprocess, sys
REQUIRED = ['pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn']
missing = []
for pkg in REQUIRED:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q'] + missing)
```

**轻量模式**：如果用户只需快速查看数据概览（行数、列数、缺失值、基本统计），跳过重型依赖，用 Python 标准库：

```python
import csv, statistics
# csv.reader + statistics.mean/stdev 即可完成描述性统计
# 无需 pandas/numpy
```

### 1. 理解数据

明确以下信息：
- **数据来源**：文件路径、数据库、API
- **数据格式**：CSV、Excel、JSON
- **数据内容**：变量含义、数据类型、样本量
- **分析目标**：描述性统计、假设检验、回归分析、分类聚类

### 2. 数据质量检查

```python
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
print(f"维度: {df.shape}")
print(f"数据类型:\n{df.dtypes}")
print(f"缺失值:\n{df.isnull().sum()}")
print(f"描述性统计:\n{df.describe()}")

# 异常值检测（IQR）
for col in df.select_dtypes(include=[np.number]).columns:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
    if len(outliers) > 0:
        print(f"{col}: {len(outliers)} 个异常值")
```

### 3. 分析方法选择

| 分析目标 | 方法 | Python实现 |
|----------|------|-----------|
| 比较两组均值 | t检验 / Mann-Whitney U | `scipy.stats.ttest_ind` |
| 比较多组均值 | ANOVA / Kruskal-Wallis | `scipy.stats.f_oneway` |
| 分类变量关联 | 卡方检验 | `scipy.stats.chi2_contingency` |
| 变量相关性 | Pearson / Spearman | `scipy.stats.pearsonr` |
| 预测连续值 | 线性回归 | `statsmodels.api.OLS` |
| 降维可视化 | PCA / t-SNE | `sklearn.decomposition.PCA` |
| 聚类 | K-Means / DBSCAN | `sklearn.cluster.KMeans` |

### 4. 可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 分布图
sns.histplot(data=df, x='column', hue='group', kde=True)
# 箱线图
sns.boxplot(data=df, x='group', y='value')
# 相关性热力图
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
# 散点图
sns.scatterplot(data=df, x='x', y='y', hue='category')
```

**图表保存规则**：当需要将图表嵌入 PDF 报告时，必须先 `plt.savefig()` 再 `\includegraphics`：
```python
# 正确：先保存再引用
plt.savefig('figures/fig1.png', dpi=150, bbox_inches='tight')
# 在 .tex 中: \includegraphics[width=0.85\textwidth]{fig1.png}
```

### 5. 效应量（必须报告）

| 效应量 | 计算 | 小/中/大 |
|--------|------|----------|
| Cohen's d | 均值差/合并标准差 | 0.2 / 0.5 / 0.8 |
| η² | 组间SS/总SS | 0.01 / 0.06 / 0.14 |
| R² | 模型解释方差比例 | 0.01 / 0.09 / 0.25 |

**统计显著 ≠ 实际重要**，必须结合效应量判断。

### 6. 结果解读要点

- 均值 ± 标准差（M ± SD）
- 95% 置信区间
- p 值（精确值，如 p = 0.0032，而非仅 p < 0.05）
- 效应量及实际意义解读

## 输出模板

```markdown
## 数据分析报告

### 1. 数据概览
- 样本量：N = [数量]
- 变量数：[数量]（数值型 X 个，分类型 Y 个）
- 数据来源：[来源]

### 2. 数据质量
- 缺失值：[各变量缺失比例及处理方式]
- 异常值：[识别方法和处理方式]

### 3. 描述性统计
| 变量 | 均值 | 标准差 | 最小值 | 最大值 | 偏度 |

### 4. 分析结果
- 检验方法及选择理由
- 统计量、自由度、p值
- 效应量和置信区间
- 结果解读

### 5. 可视化
[图表及1-2句说明]

### 6. 结论
- 主要发现（数据支撑）
- 局限性
- 建议
```

## 注意事项

- 先检查依赖再安装，不要每次全量安装
- 简单数据概览可用 Python 标准库（csv + statistics）完成
- 复杂分析（ANOVA、回归、可视化）才需要 pandas/scipy/seaborn
- 代码必须可直接运行（包含 import）
- 解释每一步的目的
- p 值结合效应量和实际意义判断

## 输出格式

默认 Markdown。用户要求 DOCX 或 LaTeX 时，参考 `OUTPUT_DOCX.md` 或 `OUTPUT_LATEX.md`。

## 编码与平台兼容

- **Windows GBK**：分析脚本顶部加依赖检查块（见 0. 环境准备），输出文件统一 UTF-8
- **快速扫描**：用 `scripts/quick_stats.py data.csv` 获取数据概览（纯 stdlib，秒级完成）
- **自动报告**：用 `scripts/analysis_report.py data.csv --compile` 一键生成 .tex + PDF
- **依赖预检**：用 `scripts/dep_check.py pandas scipy` 只装缺失的包
- 设置 `PYTHONIOENCODING=utf-8:replace` 避免终端乱码

## 快速管道（推荐）

```bash
# 步骤 1：快速了解数据（stdlib，无需安装任何包）
python scripts/quick_stats.py data.csv

# 步骤 2：生成 LaTeX 报告（含图表）
python scripts/analysis_report.py data.csv --group-col model --figures --compile

# 纯文本报告（无图表）
python scripts/analysis_report.py data.csv --group-col model --compile
```

**`analysis_report.py` 参数说明**（v4.0）：

| 参数 | 说明 |
|------|------|
| `--figures` / `-f` | 自动生成 matplotlib 图表（箱线图、分组对比、相关热力图、交互热力图），保存到 `figures/` 目录 |
| `--compile` / `-c` | 编译 .tex 为 PDF |
| `--group-col VAR` | 按指定列分组对比 |
| `--fig-dir DIR` | 自定义图表输出目录（默认与 .tex 同目录下的 `figures/`） |
| `--output` / `-o` | 自定义 .tex 输出路径 |
| `--title TEXT` | 自定义报告标题 |

**图表自动嵌入**：使用 `--figures` 时，脚本会：
1. 在 `figures/` 目录生成 PNG 图表
2. 在 .tex 中通过 `\graphicspath{{figures/}}` + `\includegraphics` 自动嵌入
3. 图表包括：各变量箱线图、分组对比柱状图、相关系数热力图、分组×变量交互热力图
