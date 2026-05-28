# 软件体系结构 Assignment 2 — 自动化工具说明

> ⚠️ 此文件为临时说明文档，最终提交前会删除。

## 项目是什么

一个 Python 脚本，自动调用 Gemini API 完成酒店定价系统的 ADD 3.0 架构设计（4 轮迭代），并自动生成所有交付物。

---

## 文件结构一览

```
src/
├── main.py              ← 主程序入口，运行即完成所有工作
├── config.py            ← 配置文件（API key、模型名、路径）
├── utils.py             ← 工具函数（日志记录、报告生成、Mermaid提取）
└── prompts/
    ├── system_prompt.txt    ← 【核心】System Prompt
    ├── iteration1.txt       ← 迭代1的用户提示词
    ├── iteration2.txt       ← 迭代2的用户提示词
    ├── iteration3.txt       ← 迭代3的用户提示词
    └── iteration4.txt       ← 迭代4的用户提示词
```

---

## 提示词设计说明

### System Prompt（`system_prompt.txt`）

这是 Gemini 的"系统指令"，程序启动时一次性传入，后续每轮对话都隐含这个上下文。

包含内容：
| 部分 | 说明 |
|------|------|
| 角色设定 | "你是一位资深软件架构师" — 引导模型以专业身份思考 |
| ADD 3.0 方法论 | 完整的 7 步流程描述（直接从作业 PDF 提取翻译） |
| 案例知识 | Hotel Pricing System 全部信息：6个用例、9个质量属性、5个关注点、6个约束 |
| 输出格式要求 | 必须用 Mermaid 画图、必须用英文回复 |

**为什么用中文写？** 方便我们理解内容。加了"必须用英文回复"指令，Gemini 会输出英文。

### 迭代提示词（`iteration1-4.txt`）

每轮迭代发送一条消息，告诉 Gemini 本轮要做什么：

| 文件 | 迭代目标 | 重点驱动因素 |
|------|---------|------------|
| `iteration1.txt` | 建立整体系统结构 | CRN-1, CRN-2, QA-4, QA-7, 全部约束 |
| `iteration2.txt` | 支撑主要功能的结构 | HPS-1~6, QA-5, QA-6 |
| `iteration3.txt` | 可靠性和可用性 | QA-1, QA-2, QA-3, QA-8 |
| `iteration4.txt` | 开发与运维 | QA-7, QA-9, CRN-3~5 |

每个 prompt 明确列出了 Step 2-7 各步要做什么、要画什么图。

---

## 程序运行流程

```
main.py 启动
  │
  ├─ 读取 system_prompt.txt → 作为 Gemini 的 system_instruction
  ├─ 创建 ChatSession（自动维护对话历史）
  │
  ├─ 循环 4 次：
  │   ├─ 读取 iterationN.txt
  │   ├─ 发送给 Gemini
  │   ├─ 接收回复 + 记录时间戳 + 统计 token
  │   └─ 提取 Mermaid 代码块 → 保存为 .mmd 文件
  │
  └─ 生成输出：
      ├─ output/conversation_log.md  ← 交付物2
      └─ output/report.md           ← 交付物3
```

---

## 自动生成的报告包含什么

| 报告章节 | 内容来源 |
|---------|---------|
| 一、ADD 输出结果 | 从 Gemini 4 轮对话回复中提取，每轮 Step 2-7 |
| 二、交互成本分析 | 程序自动统计：方法、LLM、turns数、token量、耗时 |
| 三、个人反思 | 预写了5个问题+解决方案，以及3人贡献分工 |

**唯一需要手动改的**：报告末尾贡献表中的 `[YOUR_NAME_1/2/3]` 换成真实姓名。

---

## 如何运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API key（从助教处获取）
export GEMINI_API_KEY="你的key"

# 3. 运行
cd /path/to/software-design
python src/main.py

# 4. 查看结果
ls output/
```

---

## 注意事项

- 运行一次大约消耗 5-10 分钟（取决于模型响应速度）
- 如果某轮报错程序会继续下一轮，不会中断
- 如需修改模型名称，改 `src/config.py` 的 `MODEL_NAME`
- output/ 目录在 .gitignore 中，不会被推送到 GitHub
