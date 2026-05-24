# 学术PPT制作模块（完整版）

> 本模块整合自 guizang-ppt-skill（作者：歸藏），生成横向翻页网页 PPT（单 HTML 文件）。

## 概述

生成一份**单文件 HTML**的横向翻页 PPT，提供两种视觉基调：

### 风格 A · 电子杂志 × 电子墨水（默认）
- **WebGL 流体 / 等高线 / 色散背景**（hero 页可见）
- **衬线标题（Noto Serif SC + Playfair Display）+ 非衬线正文 + 等宽元数据**
- 适合：人文社科、行业观察、故事性分享
- 美学锚点：像 *Monocle* 杂志贴上了代码

### 风格 B · 瑞士国际主义（Swiss Style）
- **WebGL 极细网格 + 点阵背景**（信息驱动设计）
- **全程无衬线（Inter + Helvetica + Noto Sans SC）+ 极致字号对比**
- **高反差功能色**：克莱因蓝 IKB / 柠檬黄 / 柠檬绿 / 安全橙（四选一）
- 适合：理工科、数据汇报、技术分享、工程领域
- 美学锚点：像 Massimo Vignelli + Helvetica Forever

**两种风格共享**：横向翻页（键盘 ← →、滚轮、触屏、ESC 索引）、Lucide 图标、Motion One 入场动效。

## 学术场景风格选择

| 用户说... | 推荐风格 |
|-----------|----------|
| 理工科 / 技术 / 工程 / 数据 | **B · 瑞士风** |
| 人文社科 / 故事 / 文化 | **A · 杂志风** |
| 毕业答辩 / 学位论文 | B 更合适 |
| 组会汇报 / 课题分享 | 根据内容选择 |
| 不确定 | 询问用户偏好 |

## 工作流

### Step 1 · 需求澄清

**7 问澄清清单**：

| # | 问题 | 为什么要问 |
|---|------|-----------|
| 1 | **风格 A 还是 B?** | 决定用哪个 template + layouts + themes |
| 2 | **受众是谁?分享场景?** | 决定语言风格和深度 |
| 3 | **分享时长?** | 15分钟≈10页, 30分钟≈20页, 45分钟≈25-30页 |
| 4 | **有没有原始素材?** | 有素材就基于素材 |
| 5 | **有没有图片或截图?** | 决定图文版式 |
| 6 | **想要哪套主题色?** | 杂志风5套 / 瑞士风4套 |
| 7 | **有没有硬约束?** | 避免返工 |

### Step 2 · 拷贝模板

```bash
mkdir -p "项目/XXX/ppt/images"

# 风格 A · 电子杂志风
cp "$SKILL_ROOT/references/ppt/assets/template.html" "项目/XXX/ppt/index.html"

# 或 风格 B · 瑞士国际主义风
cp "$SKILL_ROOT/references/ppt/assets/template-swiss.html" "项目/XXX/ppt/index.html"
```

**必改占位符**：`<title>` 标签中的 `[必填] 替换为 PPT 标题`

### Step 3 · 选定主题色

**风格 A · 5 套预设**（只能选不能自定义）：

| # | 主题 | 适合 |
|---|------|------|
| 1 | 墨水经典 | 通用 / 商业发布 |
| 2 | 靛蓝瓷 | 科技 / 研究 / 数据 |
| 3 | 森林墨 | 自然 / 可持续 / 文化 |
| 4 | 牛皮纸 | 怀旧 / 人文 / 文学 |
| 5 | 沙丘 | 艺术 / 设计 / 创意 |

操作：读 `references/ppt/references/themes.md`，找到对应主题的 `:root` 块，整体替换模板开头的 `:root{` 块。

**风格 B · 4 套预设**：
- IKB 克莱因蓝 / 柠檬黄 / 柠檬绿 / 安全橙

操作：读 `references/ppt/references/themes-swiss.md`。

### Step 4 · 填充内容

**类名预检**（最重要）：
- 风格 A 模板里有 `h-hero`(衬线)、`stat-card`、`grid-2-7-5` 等
- 风格 B 模板里有 `h-hero`(无衬线)、`kpi-hero`、`accent-block`、`span-N` 等
- 同名 class 在两个模板里**视觉表现完全不同**

**挑布局**：
- 风格 A → `references/ppt/references/layouts.md`（10种布局）
- 风格 B → `references/ppt/references/layouts-swiss.md`（S01-S22共22种版式）

**风格 B 版式多样性硬规则**：
- 7-8页至少使用6个不同S编号版式
- 不允许连续3页使用同一种主体结构

### Step 5 · 自检

生成后打开 `references/ppt/references/checklist.md` 逐项对照。

**风格 A 必查**：
1. 大标题必须是衬线字体
2. 图片网格只用 `height:Nvh`，不用 `aspect-ratio`
3. 用 Lucide，不用 emoji

**风格 B 必查**：
1. 全程无衬线
2. 只有一个 accent 色
3. 不允许渐变/阴影/圆角
4. 大字字重 200

### Step 6 · 本地预览

```bash
open "项目/XXX/ppt/index.html"
```

## 学术PPT典型结构

### 毕业答辩（15-20页）
```
封面 → 目录 → 研究背景(2-3页) → 研究方法(3-4页) → 实验结果(3-4页) → 讨论(1-2页) → 总结 → 致谢
```

### 组会汇报（8-12页）
```
封面 → 本周工作(3-4页) → 实验结果(2-3页) → 下周计划(1-2页) → 讨论
```

## 资源文件

```
references/ppt/
├── SKILL.md              ← 完整的guizang-ppt-skill原文
├── assets/
│   ├── template.html     ← 风格A模板
│   ├── template-swiss.html ← 风格B模板
│   ├── motion.min.js     ← 动效库
│   └── screenshot-backgrounds/
├── references/
│   ├── components.md     ← 组件手册
│   ├── layouts.md        ← 风格A布局
│   ├── layouts-swiss.md  ← 风格B布局
│   ├── themes.md         ← 风格A主题色
│   ├── themes-swiss.md   ← 风格B主题色
│   ├── checklist.md      ← 质量检查清单
│   └── ...
└── scripts/
    └── validate-swiss-deck.mjs
```

## 注意事项

- 风格 A 和 B **不能混用**
- 一份 deck 只用一套主题色
- 不接受用户自定义 hex 值
- 详细规则见 `references/ppt/SKILL.md`
