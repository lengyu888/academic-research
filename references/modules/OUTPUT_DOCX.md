# DOCX 输出参考

当用户要求"生成 Word""导出 docx"时，读取本文件，用 docx-js 生成 .docx。

## 前置条件

```bash
npm install -g docx  # 全局安装 docx-js
```

## 基础模板

生成 JS 脚本后用 `node` 执行。脚本结构固定，只需替换 `children` 内容。

```javascript
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat
} = require("docx");

// ===== 样式 =====
const styles = {
  default: {
    document: { run: { font: "Arial", size: 24 } } // 12pt
  },
  paragraphStyles: [
    {
      id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 36, bold: true, font: "Arial" },
      paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
    },
    {
      id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 30, bold: true, font: "Arial" },
      paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
    },
    {
      id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 26, bold: true, font: "Arial" },
      paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
    }
  ]
};

// ===== 编号配置 =====
const numbering = {
  config: [
    {
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    }
  ]
};

// ===== 表格辅助函数 =====
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function makeRow(cells, isHeader = false) {
  return new TableRow({
    children: cells.map(text =>
      new TableCell({
        borders,
        margins: cellMargins,
        width: { size: Math.floor(9360 / cells.length), type: WidthType.DXA },
        shading: isHeader ? { fill: "E8EDF2", type: ShadingType.CLEAR } : undefined,
        children: [new Paragraph({
          children: [new TextRun({ text, bold: isHeader, size: 22 })]
        })]
      })
    )
  });
}

function makeTable(headers, rows) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: headers.map(() => Math.floor(9360 / headers.length)),
    rows: [
      makeRow(headers, true),
      ...rows.map(r => makeRow(r))
    ]
  });
}

// ===== 文档结构 =====
const doc = new Document({
  styles,
  numbering,
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "学术文档", size: 18, color: "999999" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18 })
          ]
        })]
      })
    },
    children: [
      // === 在此处替换为各模块内容 ===
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("标题")]
      }),
      new Paragraph({
        children: [new TextRun("正文内容")]
      }),
    ]
  }]
});

// ===== 输出 =====
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("output.docx", buffer);
  console.log("Generated: output.docx");
});
```

## 模块内容映射

### 文献综述 → DOCX

```javascript
children: [
  // 标题
  h1("文献综述：[主题]"),
  h2("1. 引言"),
  p("[研究意义和综述范围]"),
  h2("2. 研究现状"),
  h3("2.1 [主题/方向1]"),
  p("[综合分析]"),
  h3("2.2 [主题/方向2]"),
  p("[综合分析]"),
  h2("3. 研究方法对比"),
  makeTable(
    ["方法类别", "代表工作", "优势", "局限性", "适用场景"],
    [["...", "...", "...", "...", "..."]]
  ),
  h2("4. 当前研究的局限性"),
  bullet("局限1"), bullet("局限2"),
  h2("5. 未来研究方向"),
  bullet("方向1"), bullet("方向2"),
]
```

### 数据处理 → DOCX

```javascript
children: [
  h1("数据分析报告"),
  h2("1. 数据概览"),
  makeTable(["项目", "值"], [["样本量", "N=..."], ["变量数", "..."]]),
  h2("2. 数据质量"),
  p("缺失值：... / 异常值：..."),
  h2("3. 描述性统计"),
  makeTable(
    ["变量", "均值", "标准差", "最小值", "最大值"],
    [["...", "...", "...", "...", "..."]]
  ),
  h2("4. 分析结果"),
  p("[统计检验结果]"),
  h2("5. 结论"),
  p("[发现和建议]"),
]
```

### 公式推导 → DOCX

```javascript
children: [
  h1("公式推导：[目标公式]"),
  h2("1. 问题描述"),
  p("[说明]"),
  h2("2. 已知条件"),
  bullet("前提假设：..."),
  bullet("已知公式：..."),
  h2("3. 推导过程"),
  p("Step 1: [步骤名称]", true), // bold
  p("[推导过程]"),
  p("Step 2: [步骤名称]", true),
  p("[推导过程]"),
  h2("4. 结果解读"),
  p("[物理意义和直觉理解]"),
  h2("5. 应用举例"),
  p("[应用场景]"),
]
```

注意：公式部分在 Word 中以文本描述呈现（如 `∂L/∂w = (1/N) Σ(yi - ŷi)·xi`），无法渲染 LaTeX 数学环境。如需高质量公式排版，建议用户选择 LaTeX 输出。

### 论文润色 → DOCX

```javascript
children: [
  h1("论文润色报告"),
  h2("润色范围"),
  makeTable(["项目", "内容"], [["文本长度", "..."], ["润色语言", "..."], ["润色重点", "..."]]),
  h2("润色结果"),
  // 每段对比
  p("第1段", true),
  p("原文：[原文内容]"),
  p("润色后：[润色后内容]"),
  makeTable(
    ["修改点", "原文", "修改后", "修改原因"],
    [["...", "...", "...", "..."]]
  ),
  h2("整体建议"),
  bullet("建议1"), bullet("建议2"),
  h2("常见问题汇总"),
  makeTable(["问题类型", "出现次数"], [["...", "X 次"]]),
]
```

## 辅助函数

在 JS 脚本顶部定义：

```javascript
function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] });
}
function p(text, bold = false) {
  return new Paragraph({ children: [new TextRun({ text, size: 24, bold })] });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, size: 24 })]
  });
}
```

## 验证

生成后验证文件有效性：

```bash
python "C:/Users/28482/.claude/skills/docx/scripts/office/validate.py" output.docx
```

## 注意事项

- 表格必须设置 `columnWidths` + 每个 cell 的 `width`，且两者一致
- 用 `WidthType.DXA`（不用 PERCENTAGE），Google Docs 兼容性最好
- 中文字体用 "SimSun" 或 "Microsoft YaHei"，英文用 "Arial"
- 公式在 Word 中只能以纯文本展示，复杂公式建议用户选 LaTeX 输出
- 输出路径由用户指定，或默认为当前目录下 `output.docx`
