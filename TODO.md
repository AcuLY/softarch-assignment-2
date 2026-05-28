# TODO - 完整工作流程

## 当前状态：Phase 1 已完成 ✅
所有代码和提示词已就绪，等待 API key。

---

## Phase 2：拿到 API key 后执行

### 前置条件
- Python 3.9+ 已安装
- 已从助教处获取 API key

### 步骤 1：安装依赖
```bash
cd /Users/luca/dev/software-design
pip install -r requirements.txt
```

### 步骤 2：设置 API key
```bash
export GEMINI_API_KEY="你的key"
```

### 步骤 3：运行程序
```bash
cd /Users/luca/dev/software-design
python src/main.py
```

程序会自动完成：
- ✅ 4 轮 ADD 迭代对话
- ✅ 生成 `output/conversation_log.md`（交付物 2：对话日志）
- ✅ 生成 `output/report.md`（交付物 3：完整报告）
- ✅ 提取所有 Mermaid 视图到 `output/views/`

### 步骤 4：检查报告内容

`output/report.md` 包含以下三部分（全部自动生成）：

| 报告章节 | 内容 | 自动生成？ |
|---------|------|----------|
| **一、ADD 输出结果** | 4 轮迭代每轮的 Step 2-7 完整输出 | ✅ 自动从对话中提取 |
| **二、交互成本分析** | 方法/LLM/turns/tokens/时间 | ✅ 自动统计 |
| **三、个人反思** | 遇到的问题与解决方案 + 个人贡献 | ✅ 自动生成 |

### 步骤 5：唯一需要手动操作 — 填写姓名

编辑 `output/report.md` 中的个人贡献表格：
```
| [YOUR_NAME_1] | ... |
| [YOUR_NAME_2] | ... |
| [YOUR_NAME_3] | ... |
```
将 `[YOUR_NAME_1/2/3]` 替换为三位组员的真实姓名。

### 步骤 6：验证检查清单

- [ ] `output/conversation_log.md` 存在且包含 4 轮对话
- [ ] 每轮对话有时间戳
- [ ] 对话中包含 Mermaid 代码块
- [ ] `output/report.md` 三个章节完整
- [ ] 姓名已填写
- [ ] `output/views/` 目录有 .mmd 文件

---

## Phase 3：清理并提交

### 步骤 7：清理临时文件
```bash
rm TODO.md README.md
```

### 步骤 8：最终提交到 Moodle
提交以下内容：
1. **源代码**（15分）：整个 `src/` 目录
2. **对话日志**（15分）：`output/conversation_log.md`
3. **报告**（20分）：`output/report.md`

---

## 故障排除

### API key 报错
```
ERROR: GEMINI_API_KEY environment variable is not set.
```
解决：`export GEMINI_API_KEY="your-key"`

### 模型找不到
如果 `gemini-3.1-pro-preview` 不可用，修改 `src/config.py`：
```python
MODEL_NAME = "实际的模型名"
```

### 回复被截断
如果回复不完整，增大 `src/config.py` 中的 `max_output_tokens`：
```python
"max_output_tokens": 32768,  # 从 16384 加大
```

### 网络超时
如果 API 调用超时，重新运行程序即可（会从头开始新的对话）。
