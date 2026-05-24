# 学术PPT制作模块

> 本模块基于 guizang-ppt-skill（作者：歸藏），生成横向翻页网页 PPT（单 HTML 文件）。

## 重要：读取完整 SKILL 文件

本文件只是路由入口。**生成 PPT 前必须先读取完整的 PPT SKILL 文件**：

```
references/ppt/SKILL.md
```

该文件包含完整的：
- 7 问需求澄清清单
- 模板拷贝和占位符替换步骤
- CSS 类名预检（Step 3.0）— **最关键，跳过会导致样式崩**
- 主题节奏规划（Step 3.0.5）
- 布局选择和版式多样性规则
- 图片比例规范（Step 3.2）
- 中文大标题字号分档（Step 3.2.1）
- 瑞士风最小字号与字重阶梯（Step 3.2.2）
- 风格 A/B 各自的完整自检清单
- 设计哲学和硬规则

## 快速路由

| 用户说... | 推荐风格 | 模板 | 主题色 | 布局 |
|-----------|----------|------|--------|------|
| 理工科/技术/数据/答辩 | B · 瑞士风 | `template-swiss.html` | `themes-swiss.md` | `layouts-swiss.md` (S01-S22) |
| 人文社科/故事/文化 | A · 杂志风 | `template.html` | `themes.md` | `layouts.md` (1-10) |
| 不确定 | 询问用户 | — | — | — |

## 资源文件路径

所有路径相对于 `references/ppt/`：

```
references/ppt/
├── SKILL.md                    ← 完整工作流和规则（必读）
├── assets/
│   ├── template.html           ← 风格A模板
│   ├── template-swiss.html     ← 风格B模板
│   ├── motion.min.js           ← 动效库
│   └── screenshot-backgrounds/ ← 截图背景
├── references/
│   ├── themes.md               ← 风格A 5套主题色
│   ├── themes-swiss.md         ← 风格B 4套主题色
│   ├── layouts.md              ← 风格A 10种布局
│   ├── layouts-swiss.md        ← 风格B S01-S22版式
│   ├── swiss-layout-lock.md    ← 风格B版式锁
│   ├── components.md           ← 组件手册
│   ├── checklist.md            ← 质量检查清单
│   ├── image-prompts.md        ← 配图提示词
│   ├── screenshot-framing.md   ← 截图适配
│   └── swiss-map-component.md  ← 地图组件
└── scripts/
    └── validate-swiss-deck.mjs ← 风格B校验脚本
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

### 学术会议（10-15页）
```
封面 → 研究动机 → 相关工作 → 方法 → 实验 → 结论 → Q&A
```

## 关键防错：必须保留模板结构

**绝对不要从零写 HTML 文件。** 必须先拷贝模板，再替换 `<!-- SLIDES_HERE -->`。

模板包含以下不可缺失的结构，翻页依赖它们：

```html
<body>
  <canvas id="bg-dark" class="bg"></canvas>    <!-- WebGL 深色背景 -->
  <canvas id="bg-light" class="bg"></canvas>   <!-- WebGL 浅色背景 -->
  <div id="hint">← → 翻页 · B 静态 · ESC 索引</div>

  <div id="deck">                               <!-- ⚠️ 翻页容器，缺失则无法翻页 -->
    <!-- 在此处插入 <section class="slide ..."> 页面 -->
    <!-- 替换 <!-- SLIDES_HERE --> 占位符 -->
  </div>

  <div id="nav"></div>                          <!-- 底部圆点导航 -->
  <script>/* WebGL + 翻页 + 动效 JS */</script>
</body>
```

**自检**：生成后运行 `grep -c 'id="deck"' index.html`，结果必须为 1。

## 动效系统规则（Motion One）

动画由 Motion One 驱动。**违反以下规则会导致页面不可见或动效失效**：

### 核心规则

1. **`data-anim` 只加在 `<section>` 内部的子元素上**（标题、卡片、列等），**绝不能加在 `<section>` 本身**
   - CSS 规则 `body.motion-ready [data-anim]{opacity:0}` 会隐藏所有带 `data-anim` 的元素
   - 如果 `data-anim` 在 `<section>` 上，整个页面会被隐藏！

2. **`<section>` 上选 recipe 的方式**：
   - 封面/尾页：加 `hero` class（如 `<section class="slide dark hero">`），自动触发 hero 动画
   - 引用页：`data-animate="quote"`，子元素用 `data-anim="line"`
   - 左右对比：`data-animate="directional"`，子元素用 `data-anim="left"` / `data-anim="right"`
   - 流水线：`data-animate="pipeline"`，子元素用 `data-anim="step"`
   - 其他页：不加任何属性，默认 cascade 动画

3. **每个需要动画的子元素加 `data-anim`**：
   ```html
   <!-- 正确 -->
   <section class="slide dark hero">
     <h1 data-anim>标题</h1>
     <p data-anim>内容</p>
   </section>

   <!-- 错误！整个页面会被隐藏 -->
   <section class="slide dark" data-anim="fade-up">
     <h1>标题</h1>
   </section>
   ```

### 自检命令

```bash
# 检查是否有 data-anim 错误地加在 section 上
grep -n 'class="slide.*data-anim' index.html
# 结果应该为空（无匹配）
```

## 注意事项

- 风格 A 和 B **不能混用**
- 一份 deck 只用一套主题色
- 不接受用户自定义 hex 值（从预设中选）
- 详细规则见 `references/ppt/SKILL.md`
