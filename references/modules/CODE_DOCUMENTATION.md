# 代码文档模块

## 触发场景

- 用户需要为实验代码写 README 或文档
- 用户需要生成代码注释规范
- 用户需要写实验复现说明（Reproduction Guide）
- 用户需要为论文补充代码附录
- 用户准备开源代码仓库

## 工作流程

### 1. 理解代码上下文

明确以下信息：
- **代码类型**：模型训练、数据分析、工具库、演示 Demo
- **目标用户**：审稿人（复现）、同行（二次开发）、自己（可维护性）
- **语言/框架**：Python/PyTorch/TensorFlow/JAX 等
- **仓库状态**：已有代码需补文档，还是从零规划

### 2. README 结构生成

```markdown
# [项目名]

[一句话描述]

## 安装

```bash
pip install -r requirements.txt
# 或
conda env create -f environment.yml
```

## 快速开始

```bash
# 最小可运行示例（5行以内）
python demo.py --input sample.jpg
```

## 项目结构

```
├── src/           # 核心源码
├── scripts/       # 运行脚本
├── configs/       # 配置文件
├── data/          # 数据（如适用）
├── checkpoints/   # 预训练模型
└── docs/          # 文档
```

## 使用方法

### 训练

```bash
python train.py --config configs/default.yaml
```

### 评估

```bash
python eval.py --checkpoint path/to/model.pt --dataset test
```

## 实验复现

要复现论文中的主要结果：

| 实验 | 配置 | 预期结果 | 耗时 |
|------|------|----------|------|
| Table 1 | configs/exp1.yaml | Acc 72.3±0.5 | ~2h on A100 |
| Table 2 | configs/exp2.yaml | F1 0.856 | ~4h on A100 |

## 引用

```bibtex
@article{your2026paper,
  ...
}
```

## 许可

[MIT / Apache 2.0 / CC BY 4.0]
```

### 3. 代码注释规范

#### Python docstring 模板（Google 风格）

```python
def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
    """一句话描述功能。

    Args:
        x: 输入张量，形状 (B, C, H, W)
        mask: 可选注意力掩码，形状 (B, H, W)

    Returns:
        输出张量，形状 (B, C_out, H, W)

    Raises:
        ValueError: 当输入通道数与模型不匹配时
    """
    ...
```

#### 模块级注释

```python
"""
模块名：语义分割解码器
功能：将多尺度编码特征融合并上采样到原图分辨率
输入：来自骨干网络的多层特征图 (P2, P3, P4, P5)
输出：逐像素类别概率图 (B, num_classes, H, W)
依赖：torch >= 2.0, mmcv >= 2.0
"""
```

### 4. 实验复现说明

这是论文代码文档最关键的部分，需要确保审稿人能独立复现。

```markdown
## 复现指南

### 环境

- Python 3.10+
- PyTorch 2.0.1 (CUDA 11.8)
- GPU: 推荐 24GB+ 显存 (A5000/A100)
- 磁盘: ~50GB (数据集 + 检查点)

### 数据准备

1. 下载 [数据集名] 从 [链接]
2. 解压到 `data/` 目录
3. 运行预处理：
   ```bash
   python scripts/preprocess.py --data_dir data/
   ```

### 训练

```bash
# 设置随机种子确保可复现
export SEED=42
python train.py \
  --config configs/reproduce.yaml \
  --seed $SEED \
  --output_dir logs/reproduce/
```

### 评估

```bash
# 下载预训练权重
wget https://xxx/checkpoint.pt -O checkpoints/model.pt

python eval.py \
  --checkpoint checkpoints/model.pt \
  --dataset test \
  --save_results results.json
```

### 预期结果

| 指标 | 论文报告值 | 复现值 | 允许误差 |
|------|-----------|--------|----------|
| Accuracy | 72.3 | 72.3±0.5 | ±0.5 |
| F1 Score | 0.856 | 0.856±0.01 | ±0.01 |
| Inference (ms) | 45.2 | 45.2±2.0 | ±5% |

### 常见问题

**Q: OOM 错误？**
A: 减小 batch_size 或使用 gradient_accumulation_steps

**Q: 复现结果与论文有偏差？**
A: 确保使用了相同的随机种子和 PyTorch 版本
```

### 5. 自查清单

- [ ] `README.md` 包含安装、快速开始、引用三要素
- [ ] `requirements.txt` 锁定所有依赖版本号
- [ ] 每个 `.py` 文件的公开函数有 docstring
- [ ] `configs/` 中有专门的复现配置文件
- [ ] 随机种子固定以确保可复现
- [ ] 预训练模型下载链接有效
- [ ] 提供了最小可运行 demo（< 10 行代码）

## 输出模板

根据用户需要输出以下一个或多个：

```
1. README.md          ← 仓库主页文档
2. REPRODUCTION.md    ← 实验复现详细说明
3. docstring 补全     ← 对现有代码逐函数补注释
4. 项目结构建议       ← 目录 + 配置文件组织建议
```

## 注意事项

- 文档的第一句话最重要——用户在 GitHub 搜索时只看到前 150 字符
- 最小可运行 demo 尽量简洁（5-10 行），让用户 30 秒内看到效果
- 复现指令中显式指定随机种子、版本号，任何模糊点都会被审稿人质疑
- 如果代码依赖预训练权重，确保链接长期有效（推荐 Zenodo 或 GitHub Releases）
- 实验耗时要标明 GPU 型号和显存要求

## 输出格式

默认 Markdown（直接生成 .md 文件）。也可生成 .rst（Sphinx 兼容）。
