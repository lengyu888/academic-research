# 学术海报模块

## 触发场景

- 用户需要制作学术会议海报
- 用户需要设计实验室研究方向海报
- 用户需要做墙报展示

## 🌐 语言默认规则

**海报语言默认跟随用户输入内容语言。** 与 skill 全局语言保持原则一致：

| 用户输入内容 | 海报语言 | 字体策略 |
|-------------|---------|---------|
| 中文论文 / 中文描述 | **中文（默认）** | Noto Sans SC 优先 → Inter / Helvetica 回退 |
| 英文论文 / 英文描述 | 英文 | Inter / Helvetica 优先 → Noto Sans SC 回退 |
| 中英混合（中文 >70%）| 中文 | 同中文策略 |
| 未明确 | **中文** | 同中文策略 |

**判断方法**：分析用户提供的论文标题、摘要或研究内容。若中文字符占比 >50%，判定为中文内容；海报所有节标题、标签、图注生成中文版本。

**英文专有名词保留**：方法名（如"RadAlign""Faster R-CNN"）、指标名（如"BLEU-4""CIDEr-D"）、数据集名保留英文原文，不作翻译。

## 工作流程

### 1. 需求澄清

| 问题 | 选项 |
|------|------|
| 呈现风格 | HTML（现代/交互）或 LaTeX（传统/正式）或 PPT |
| 尺寸 | A0 竖版 / A0 横版 / 宽幅横版（4:1）/ 自定义 |
| 内容来源 | 已有论文/研究报告/口头描述 |
| 会议/场合 | 壁报展、实验室墙、答辩辅助 |
| 海报语言 | 中文（默认）/ 英文 / 中英双语 |

### 2. 内容结构（通用海报）

```
┌──────────────────────────────────────────────┐
│  TITLE                  Authors  ·  Affiliation  ·  Logo │
├────────────────────┬─────────────────────────┤
│  Introduction      │                         │
│  (2-3 bullets)     │      Main Figure        │
│                    │                         │
├────────────────────┤    (占海报面积的        │
│  Method            │     30-40%)             │
│  · Key idea        │                         │
│  · Architecture    │                         │
│  · Novelty         │                         │
├────────────────────┼─────────────────────────┤
│  Results           │  Conclusion             │
│  · Table/Chart 1   │  · Take-home message    │
│  · Table/Chart 2   │  · Future work          │
├────────────────────┴─────────────────────────┤
│  References (small font)  ·  Acknowledgments  ·  QR Code │
└──────────────────────────────────────────────┘
```

#### 每部分的字数预算（A0 竖版）

| 区域 | 字数 | 字号建议 | 重点 |
|------|------|----------|------|
| 标题 | 1-2行 | 72-96pt | 吸引眼球 |
| 导言 | 3-5 bullets, <200字 | 28-32pt | 只说核心问题 |
| 方法 | 3-5元素, <300字 | 24-28pt | 图文配合 |
| 结果 | 2-3图表, 少量标注 | 24-28pt | 图表为主 |
| 结论 | 3-4 bullets, <150字 | 28-36pt | 每点一句话 |

### 3. 输出格式

#### HTML 方式（推荐）

生成单文件 HTML，可打印为 PDF/A0。**默认生成中文海报**（节标题、标签为中文），英文专有名词保留原文。

##### 中文海报模板（默认）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  /* 中文字体优先 */
  body{width:841mm;height:1189mm;margin:0;padding:40px;
       font-family:'Noto Sans SC','Inter','Helvetica Neue',sans-serif;
       display:grid;grid-template-columns:1fr 1fr;gap:24px;
       background:white;color:#1a1a1a}
  .full-width{grid-column:1/-1}
  .title-block{text-align:center;padding:20px}
  h1{font-size:64px;font-weight:700;margin:0;line-height:1.15}
  h2{font-size:36px;font-weight:600;border-bottom:3px solid #002FA7;padding-bottom:4px}
  p,li{font-size:24px;line-height:1.6;font-weight:400}
  .authors{font-size:28px;color:#555}
  .figure{border:1px solid #ddd;padding:20px;text-align:center;
          font-size:28px;color:#999;min-height:300px}
  /* 中英文混排间距优化 */
  .cn-text{letter-spacing:0.02em}
  .en-term{font-family:'Inter',sans-serif;letter-spacing:0}
</style>
</head>
<body>
  <div class="title-block full-width">
    <h1>海报标题（中文）</h1>
    <p class="authors">作者1, 作者2 · 单位 · 联系方式</p>
  </div>
  <div>
    <h2>研究背景</h2>
    <ul><li>...</li></ul>
    <h2>方法</h2>
    <ul><li>...</li></ul>
  </div>
  <div>
    <div class="figure">[主要图表]</div>
    <h2>实验结果</h2>
    <div class="figure">[数据图表]</div>
  </div>
  <div class="full-width">
    <h2>结论</h2>
    <p>...</p>
  </div>
</body>
</html>
```

##### 中文海报节标题对照表

| 英文标题 | 中文标题（默认） |
|----------|-----------------|
| Introduction / Background / Motivation | 研究背景 |
| Method / Approach / Architecture | 方法 |
| Results / Experiments / Findings | 实验结果 |
| Conclusion / Takeaway | 结论 |
| References | 参考文献 |
| Acknowledgments | 致谢 |
| Future Work | 未来工作 |
| Contact | 联系方式 |

##### 英文海报模板（用户明确要求时使用）

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body{width:841mm;height:1189mm;margin:0;padding:40px;
       font-family:'Inter','Helvetica Neue','Noto Sans SC',sans-serif;
       display:grid;grid-template-columns:1fr 1fr;gap:24px;
       background:white;color:#1a1a1a}
  .full-width{grid-column:1/-1}
  .title-block{text-align:center;padding:20px}
  h1{font-size:64px;font-weight:300;margin:0}
  h2{font-size:36px;font-weight:400;border-bottom:3px solid #002FA7}
  p,li{font-size:24px;line-height:1.5;font-weight:300}
  .authors{font-size:28px;color:#555}
  .figure{border:1px solid #ddd;padding:20px;text-align:center;
          font-size:28px;color:#999;min-height:300px}
</style>
</head>
<body>
  <div class="title-block full-width">
    <h1>Poster Title Goes Here</h1>
    <p class="authors">Author1, Author2 · Affiliation · contact@email.com</p>
  </div>
  <div>
    <h2>Introduction</h2>
    <ul><li>...</li></ul>
    <h2>Method</h2>
    <ul><li>...</li></ul>
  </div>
  <div>
    <div class="figure">[Main Figure]</div>
    <h2>Results</h2>
    <div class="figure">[Chart]</div>
  </div>
  <div class="full-width">
    <h2>Conclusion</h2>
    <p>...</p>
  </div>
</body>
</html>
```

#### LaTeX 方式

```latex
\documentclass[final]{beamer}
\usepackage[orientation=portrait,size=a0]{beamerposter}
\usetheme{SimplePlus} % 或自定义

\begin{document}
\begin{frame}
  \begin{columns}
    \begin{column}{.45\textwidth}
      ... % Introduction + Method
    \end{column}
    \begin{column}{.45\textwidth}
      ... % Results + Conclusion
    \end{column}
  \end{columns}
\end{frame}
\end{document}
```

### 4. 海报设计原则

- **少即是多**：文字不超过总面积的 40%
- **视觉层级**：标题→主体图→分节标题→正文→细节
- **留白充足**：各区域间至少 5% 间距
- **统一配色**：2-3 种颜色，主色 + 强调色 + 中性灰度
- **图表优先**：能用图不用表，能用表不用文字
- **可读距离测试**：站在 1.5 米外应能看清标题和主体图

#### 中文海报专项规范

中文海报与英文海报在排版上有显著差异，需额外注意：

| 规范项 | 中文海报 | 英文海报 |
|--------|---------|---------|
| **正文字号** | ≥28pt（中文笔画密度高，字号需更大） | ≥24pt |
| **标题字重** | 700（Bold），中文细体远距不可读 | 300-400（Light/Regular） |
| **行距** | 1.6-1.8（中文无 x-height，需更宽松行距） | 1.4-1.5 |
| **字体优先级** | `'Noto Sans SC','思源黑体','Microsoft YaHei',sans-serif` | `'Inter','Helvetica Neue',sans-serif` |
| **中英混排** | 英文专有名词用 `<span style="font-family:'Inter'">` 包裹 | N/A |
| **标点** | 全角中文标点（，。；：） | 半角英文标点 |
| **列表符号** | 中文破折号 —— 或 · | 英文 dash — 或 bullet · |
| **数字/单位** | 数字与中文间加空格：`提升 23.7%` | `+23.7% improvement` |

**中文海报核心原则**：
- **标题加粗**：中文字体笔画复杂，远距离阅读必须使用 Bold（700）以上字重
- **段落短小**：中文信息密度高，每个 bullet 控制在 25 字以内
- **术语保留英文**：方法名（RadAlign、Faster R-CNN）和指标名（BLEU-4、CIDEr-D）保留英文，避免生硬翻译
- **双语标题可选**：国际会议海报可在中文标题下方用较小字号加英文副标题

## 输出模板

生成的 HTML 文件结构：

```
poster/
├── index.html      ← 主文件（浏览器打开 → 打印 PDF/A0）
└── images/         ← 如有矢量图
```

## 注意事项

- 海报不是论文的简单压缩，本质是 90 秒电梯演讲的视觉化
- 主图是海报的灵魂——占 30-40% 面积，体现最核心的实验对比或架构
- 标题要大、要有 hook（如 "RadAlign 在 MIMIC-CXR 上超越 SOTA 3.2 个百分点"）
- 打印前检查：A0 尺寸下中文字体不小于 28pt，图表标注清晰可读
- **默认中文输出**：除非用户明确要求英文，或输入内容全部为英文，否则海报节标题和正文使用中文

## 输出格式

默认 HTML（推荐打印为 PDF），可选 LaTeX（beamerposter）。用户要求 DOCX 时用 `docx-js` 生成。
