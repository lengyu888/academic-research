# 论文投稿模块

## 触发场景

- 用户准备投稿论文
- 用户需要写 Cover Letter
- 用户收到审稿意见需要写 Rebuttal / Response
- 用户不知道改投哪个期刊
- 用户需要检查投稿格式合规性

## 工作流程

### 1. 理解投稿需求

明确以下信息：
- **论文类型**：期刊、会议、预印本
- **目标期刊/会议**：如已知
- **论文内容**：用户提供论文文件或核心内容摘要
- **当前阶段**：初投、修改后重投、改投

### 2. 期刊匹配推荐

| 匹配维度 | 考虑因素 |
|----------|----------|
| 研究领域 | 目标期刊征稿范围是否符合 |
| 论文水平 | IF/CCF 分区与论文创新性匹配 |
| 审稿周期 | 快报/Letter 还是 长文/Regular |
| 版面费 | OA 费用、超页费 |
| 概率估计 | 过高→浪费时间，过低→亏待工作 |

推荐输出格式：
```
| 期刊 | 分区 | 审稿周期 | 匹配度 | 理由 |
|------|------|----------|--------|------|
| TPAMI | CCF-A | 8-12周 | 中等 | 投稿竞争激烈，创新点需突出 |
| TIP | CCF-A | 6-10周 | 较高 | 近期发表相关主题较多 |
```

### 3. Cover Letter 生成

结构模板：

```
[日期]

Dear Editor,

[第1段：说明投稿意图]
We are pleased to submit our manuscript entitled "[标题]" for 
consideration for publication in [期刊名].

[第2段：研究背景与核心贡献（3-4句）]
[领域重要性（1句）→ 当前空白（1句）→ 本工作解决什么（1-2句）]

[第3段：创新点与重要性]
The key contributions of this work are:
1. [贡献1]
2. [贡献2]
3. [贡献3]

[第4段：声明（无利益冲突、无重复投稿等）]
We confirm that this manuscript has not been published elsewhere
and is not under consideration by any other journal. All authors
have read and approved the final version.

Sincerely,
[通讯作者]
```

### 4. Response to Reviewers 撰写

#### 基本原则

- 开头感谢审稿人时间和建设性意见
- 逐一回复每个问题，不改原文结构
- 引用修改后的具体位置（第X页第Y行，红色标记）
- 态度谦逊但守住学术立场
- 如果无法满足某个要求，解释原因

#### 结构模板

```
Dear Editor and Reviewers,

We sincerely thank the reviewers for their time and constructive
comments, which have significantly improved this manuscript.

Below we provide a point-by-point response to each comment.
Revisions are highlighted in RED in the revised manuscript.

============================================================
Reviewer 1
============================================================

Comment 1: [审稿人原话]
Response: [你的回复]
Action: On page X, line Y, we have [修改了什么].

Comment 2: [审稿人原话]
Response: [你的回复]
Action: [修改内容]

============================================================
Reviewer 2
============================================================
...

We hope these revisions address all concerns satisfactorily.
```

#### 常见的审稿意见类别和回复策略

| 审稿意见类型 | 回复策略 |
|-------------|----------|
| 要求补充实验 | 能做就做，不能做要解释原因（资源/时间/合理性） |
| 质疑方法有效性 | 引用文献支持 + 补充控制实验/消融实验 |
| 建议引用某篇论文 | 评估是否相关，相关就加，不相关礼貌说明 |
| 指出写作问题 | 感谢纠正，逐一修改 |
| 认为贡献不够 | 重新梳理贡献与现有工作的本质差异 |
| 质疑实验设置 | 补充实验细节 + 说明设置的合理性（文献支持） |

### 5. 投稿前自检清单

格式检查：
- [ ] 页数/字数在限制内
- [ ] 模板符合期刊/会议要求（如 IEEE 双栏、Springer LNCS）
- [ ] 图片清晰度≥300dpi
- [ ] 参考文献格式正确（检查 DOI 链接有效性）
- [ ] 匿名化已执行（如双盲审稿，去除作者信息和致谢中的基金号）

内容检查：
- [ ] 所有引用在正文中都有出现
- [ ] 图表引用序号正确（Fig.1 → Fig.2 等）
- [ ] 补充材料链接有效
- [ ] 作者列表及单位无误
- [ ] 通讯作者邮箱正确

## 输出模板

```markdown
## 投稿准备报告

### 1. 投稿信息
- 目标期刊：[名称]
- 论文题目：[标题]
- 投稿类型：[Regular/Letters/Review]

### 2. Cover Letter
[生成的 Cover Letter]

### 3. 格式检查结果
| 检查项 | 状态 | 备注 |
|--------|------|------|
| [项目] | ✓/✗ | [说明] |

### 4. Response to Reviewers（如适用）
[分审稿人的逐条回复]
```

## 注意事项

- Cover Letter 不要重复摘要，要强调研究动机和与目标期刊的契合度
- Rebuttal 是论文与发表之间最后的机会，态度决定命运
- 被拒后冷静分析原因再改投，不要无修改直接转投
- 预印本（arXiv）与正式投稿不冲突，但注意目标期刊的预印本政策

## 输出格式

默认 Markdown。用户要求 DOCX 或 LaTeX 时，参考 `OUTPUT_DOCX.md` 或 `OUTPUT_LATEX.md`。
