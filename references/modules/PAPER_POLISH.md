# 论文润色模块

## 触发场景

- 用户需要润色论文段落
- 用户想改善学术表达
- 用户需要检查语法和逻辑
- 用户想让论文更符合国际期刊要求
- 用户需要"去AI味"——让 AI 生成的文本读起来更像人写的学术论文

## 工作流程

### 1. 理解润色需求

明确以下信息：
- **润色范围**：单段、整节、全文
- **语言**：中文、英文、中英对照
- **目标**：语法修正、表达优化、逻辑改进、风格统一
- **期刊/会议**：如有特定要求（如 IEEE、ACM、Springer 等格式）

### 2. 润色前检查清单

在润色前，先通读全文，标记以下问题类别：

**语言问题**（标记 L）：
- [ ] L1：语法错误（主谓一致、时态、语态、单复数）
- [ ] L2：用词不当（口语化、模糊、非学术用语）
- [ ] L3：句式单调（连续使用相同句型）
- [ ] L4：冗余表达（可以更简洁）

**逻辑问题**（标记 C）：
- [ ] C1：段落缺少主题句
- [ ] C2：段间缺乏过渡
- [ ] C3：论据不支撑论点
- [ ] C4：因果关系不清

**学术规范**（标记 A）：
- [ ] A1：主观表达（"我认为""很明显"）
- [ ] A2：模糊量化（"很多""一些"→给出具体数据）
- [ ] A3：引用缺失（断言无引用）
- [ ] A4：时态混乱

### 3. 润色维度

#### 语言层面
- **语法正确性**：主谓一致、时态、语态
- **用词准确性**：专业术语、同义词选择
- **句式多样性**：避免句式单调，长短句交替
- **简洁性**：删除冗余表达，一句话一个意思

#### 逻辑层面
- **段落结构**：主题句 → 支撑句 → 总结句
- **段间衔接**：使用恰当的过渡词/句
- **论证完整性**：论点 → 论据 → 论证链条
- **因果关系**：逻辑推理是否严密

#### 学术规范
- **客观性**：避免主观判断（"我认为" → "结果表明"）
- **精确性**：量化描述优于模糊描述
- **引用规范**：引用位置和格式
- **时态使用**：方法用过去时，普遍结论用现在时

### 4. 英文论文润色要点

#### 常见问题对照表

| 问题类型 | 原文示例 | 润色后 | 修改理由 |
|----------|----------|--------|----------|
| 主语过长 | The method that we proposed in this paper... | Our proposed method... | 主语从句→前置修饰 |
| 被动滥用 | It was found that the results... | The results show that... / We observed that... | 主动语态更直接 |
| 冗余表达 | In order to improve → to improve | 删除冗余短语 | 简洁 |
| 模糊限定 | very good results | competitive/effective/robust results | 具体化 |
| 中式英语 | With the development of deep learning... | As deep learning advances/evolves... | 英文习惯表达 |
| 弱动词 | make use of / carry out | use / conduct / perform | 用强动词替代弱动词短语 |
| 指代不清 | This shows... | This improvement demonstrates... | 明确指代对象 |

#### 学术写作高频句型

**引出研究背景**：
- Recent years have witnessed growing interest in [topic].
- Despite significant progress, [problem] remains challenging.
- [Field] has attracted considerable attention due to [reason].
- A key challenge in [field] is [problem].

**陈述研究贡献**：
- This paper addresses the gap between [A] and [B].
- We propose a novel [method] that [advantage].
- Our main contributions are threefold: (1)... (2)... (3)...
- To the best of our knowledge, this is the first work to [contribution].

**描述方法**：
- The framework consists of [N] components: [A], [B], and [C].
- Formally, we define [concept] as [definition].
- Given [input], our model learns to [output] by [mechanism].

**报告实验结果**：
- Experimental results demonstrate that our method outperforms [baseline] by [X]% on [dataset].
- As shown in Table [N], [observation].
- Our approach achieves state-of-the-art performance on [benchmark].
- The improvement is statistically significant (p < 0.05).

**讨论局限与未来工作**：
- One limitation of this approach is [limitation].
- Future work will explore [direction] to address [issue].
- These results should be interpreted with caution due to [reason].

### 5. 中文论文润色要点

#### 常见问题对照表

| 问题类型 | 原文示例 | 润色后 | 修改理由 |
|----------|----------|--------|----------|
| 口语化 | 这个方法挺好的 | 该方法具有较好的性能 | 学术用语规范化 |
| 主语缺失 | 通过实验验证了... | 本文通过实验验证了... | 补充主语 |
| 长句堆砌 | [一逗到底的长句] | 拆分为2-3个短句 | 提高可读性 |
| 逻辑跳跃 | A。B。 | A，因此B。/ A。基于此，B。 | 补充逻辑连接 |
| 模糊表述 | 效果有所提升 | 准确率提升3.2个百分点 | 量化精确 |
| 万能动词 | 进行了研究/进行了分析 | 开展了研究/分析了结果 | 避免"进行"万能化 |

#### 学术写作规范

**避免的表达**：
| 避免 | 替代方案 | 原因 |
|------|----------|------|
| 众所周知 | 直接陈述或引用文献 | 主观判断 |
| 不言而喻 | 给出依据 | 缺乏论证 |
| 相关研究表明 | 给出具体引用 [X] | 引用缺失 |
| 具有重要意义 | 说明具体意义（如"提升准确率X%"） | 模糊 |
| 大量的 | 给出具体数量或比例 | 不精确 |
| 取得了很好的效果 | 在[X]指标上达到[Y] | 不够量化 |

**推荐的表达**：
- "实验结果表明" → 客观陈述
- "与[文献X]相比" → 有据可查
- "在[条件]下" → 条件明确
- "误差为±X%" → 量化精确
- "本文/本研究" → 正式自称

### 6. 润色输出格式

**逐句对比**（适合小范围润色，5句以内）：
```
原文：The method can get good results on this dataset.
润色：The method achieves competitive performance on this dataset.
修改原因："get"过于口语化，"good"不够具体，替换为学术常用表达
```

**整段对比**（适合段落润色）：
```
【原文】
[原始段落]

【润色后】
[润色后段落]

【修改说明】
1. [修改点1]：[原因]
2. [修改点2]：[原因]
```

### 7. 去 AI 味（De-AI-Flavor）

当用户指出文本是 AI 生成的、或希望文本更自然时，按以下维度排查和改写。

#### 中文 AI 味特征与修改

| AI 味特征 | 典型表现 | 修改方向 |
|-----------|----------|----------|
| **万能排比** | "从A到B再到C""不仅...而且...更..." | 打破对称结构，用单一主次分明的叙述 |
| **百科全书式罗列** | 每段 bullet list 堆砌 4-5 个并列项 | 挑选 2-3 个重点详写，其余一笔带过或删除 |
| **绝对化论断** | "彻底改变了""全面超越""前所未有的" | 加限定词："在一定程度上""在特定任务中" |
| **数字标签结构** | "三大方向""四大挑战""六大领域" | 去掉数字标签，改为自然过渡的段落 |
| **空洞总结句** | "助力...发展""推动...走向新高度" | 删除，或改为具体但留有余地的表述 |
| **过度整齐** | 每节结构完全一致（概述→列表→小结） | 各节写法适当变化，有的详有的略 |
| **连接词堆砌** | "值得注意的是""需要指出的是""综上所述" | 直接陈述，让上下文自然过渡 |
| **缺乏批判性** | 只说成就不提局限，只说进展不说争议 | 补充"但需要注意""仍有讨论空间"等限定 |

#### 英文 AI 味特征与修改

| AI 味特征 | 典型表现 | 修改方向 |
|-----------|----------|----------|
| **Hedging 堆砌** | "It is worth noting that", "It should be emphasized" | 直接陈述 |
| **过度对称** | "Not only...but also...Furthermore..." | 用单一主句表达核心意思 |
| **空洞动词** | "plays a crucial role", "has significant implications" | 用具体动词替代 |
| **模板化开头** | "In recent years, ... has attracted growing attention" | 换一种更具体的切入方式 |
| **过度使用 passive** | "It has been demonstrated that...", "It is widely recognized" | 改为主动语态 |

#### 去 AI 味操作流程

1. **通读全文**，标记所有符合上述特征的句子
2. **重写标记句**：打破原句结构，而非仅替换同义词
3. **调整节奏**：让段落长短不一，有的详细展开，有的简短收束
4. **加入立场**：在关键判断处补充作者的限定和保留（"在...条件下""就...而言"）
5. **检查一致性**：确认改写后没有引入前后矛盾

### 8. 润色后自检

润色完成后，对照以下检查项：
- [ ] 原意保留：没有改变作者的学术观点和立场
- [ ] 一致性：全文术语、时态、语态保持一致
- [ ] 可读性：修改后的文本比原文更流畅
- [ ] 无引入错误：没有在润色过程中引入新的语法或逻辑错误
- [ ] 去 AI 味：如适用，确认消除了模板化、排比化、绝对化等问题

## 输出模板

```markdown
## 论文润色报告

### 润色范围
- 文本长度：[字数/段落数]
- 润色语言：[中文/英文]
- 润色重点：[语法/表达/逻辑/风格]

### 问题诊断
| 问题类别 | 具体问题 | 出现次数 | 严重程度 |
|----------|----------|----------|----------|
| 语言 | [问题描述] | X 次 | 高/中/低 |
| 逻辑 | [问题描述] | Y 次 | 高/中/低 |

### 润色结果

#### 逐段润色

**第1段**
原文：
> [原文内容]

润色后：
> [润色后内容]

修改说明：
| # | 修改点 | 原文 | 修改后 | 修改原因 |
|---|--------|------|--------|----------|
| 1 | [位置] | [原文] | [修改后] | [原因] |

### 整体建议
1. [宏观建议1：如"建议统一全文时态"]
2. [宏观建议2：如"部分段落缺少主题句"]
3. [宏观建议3：如"引用格式需要统一"]

### 常见问题汇总
- [问题类型1]：出现 X 次 → [改进建议]
- [问题类型2]：出现 Y 次 → [改进建议]
```

## 注意事项

- 润色是改善表达，不是改变观点。保持作者的原意和学术立场
- 对于不确定的专业术语，不要随意替换，可以标注询问用户
- 如果用户提供了期刊/会议的格式要求，优先遵循其规范
- 润色后建议用户通读一遍，确保修改符合预期
- 对于英文润色，如果用户母语是中文，可以解释修改背后的英语习惯
- 润色幅度适中：不要过度修改导致失去作者个人风格

## 输出格式

默认 Markdown。用户要求 DOCX 或 LaTeX 时，参考 `OUTPUT_DOCX.md` 或 `OUTPUT_LATEX.md`。

## 编码与平台兼容

- **Windows GBK**：编辑 .docx XML 时 `<w:t>` 内容使用 XML 实体（如 `&#x201C;`）避免编码错误
- **.tex 润色**：始终以 UTF-8 读写，编译用 XeLaTeX
- **Python 脚本**：涉及中文输出时加 `PYTHONIOENCODING=utf-8:replace` 环境变量
- 需要安装的包用 `scripts/dep_check.py` 预检

### .docx 文件润色/去 AI 味流程

当用户提供 .docx 文件需要润色或去 AI 味时，使用 `docx` skill 的编辑流程：

1. **解包**：`python <docx-skill>/scripts/office/unpack.py input.docx unpacked/`
2. **编辑 XML**：直接在 `unpacked/word/document.xml` 中定位并替换目标文本
3. **打包**：`python <docx-skill>/scripts/office/pack.py unpacked/ output.docx --original input.docx`

编辑要点：
- 用 Edit 工具直接修改 XML 中的 `<w:t>` 标签内容
- 保持原有格式（`<w:rPr>` 标签不动）
- 润色后用 `validate.py` 验证输出文件

### .tex 文件润色/去 AI 味流程

当用户提供 .tex 文件需要润色或去 AI 味时：

1. **读取** .tex 全文内容
2. **按上述润色/去 AI 味维度**逐段修改
3. **保持 LaTeX 结构**：不改动 `\section`、`\begin{equation}` 等标记，只修改文本内容
4. **可选编译**：修改后调用 `compile.py` 生成 PDF 供用户预览
