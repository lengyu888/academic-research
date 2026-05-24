# 学术海报模块

## 触发场景

- 用户需要制作学术会议海报
- 用户需要设计实验室研究方向海报
- 用户需要做墙报展示

## 工作流程

### 1. 需求澄清

| 问题 | 选项 |
|------|------|
| 呈现风格 | HTML（现代/交互）或 LaTeX（传统/正式）或 PPT |
| 尺寸 | A0 竖版 / A0 横版 / 宽幅横版（4:1）/ 自定义 |
| 内容来源 | 已有论文/研究报告/口头描述 |
| 会议/场合 | 壁报展、实验室墙、答辩辅助 |

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

生成单文件 HTML，可打印为 PDF/A0：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body{width:841mm;height:1189mm;margin:0;padding:40px;
       font-family:'Inter','Noto Sans SC',sans-serif;
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
- 标题要大、要有 hook（如 "X outperforms SOTA by 15% on Y dataset"）
- 打印前检查：A0 尺寸下字体不小于 24pt，图表标注清晰可读

## 输出格式

默认 HTML（推荐打印为 PDF），可选 LaTeX（beamerposter）。用户要求 DOCX 时用 `docx-js` 生成。
