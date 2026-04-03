# AI 智能分析指南

## 混合检测架构

### 静态规则引擎（快速扫描）

**优点**：
- 速度快（秒级）
- 准确率高（已知风险）
- 无需外部依赖

**适用场景**：
- 快速初筛
- 已知 API 检测
- 标准风险模式

**检测内容**：
```python
# 30+ 微信官方敏感 API
wx.getLocation()
wx.chooseLocation()
wx.getUserInfo()
wx.getUserProfile()
wx.getPhoneNumber()
wx.chooseImage()
wx.chooseVideo()
wx.startRecord()
# ... 更多
```

### AI 智能体引擎（深度分析）

**优点**：
- 理解代码语义
- 发现未知风险
- 适应性强

**适用场景**：
- 动态 API 调用
- 混淆代码分析
- 复杂数据流

**检测能力**：
```javascript
// 检测动态调用
const apiName = getUserInput();
wx[apiName](); // AI 可以识别这种动态调用

// 检测混淆代码
const _0x1234 = 'getLocation';
wx[_0x1234](); // AI 可以追踪变量
```

## AI 分析流程

### 1. 代码预处理
```bash
# 解析 JavaScript 代码
# 提取 AST（抽象语法树）
# 识别关键节点
```

### 2. 语义分析
```python
# 理解代码意图
# 追踪数据流
# 识别敏感操作
```

### 3. 风险评估
```python
# 计算风险分数
# 生成修复建议
# 输出分析报告
```

## 配置选项

```bash
# 启用 AI 分析
./miniprogram-privacy-auto.sh /path/to/miniprogram --enable-ai

# 禁用 AI 分析（仅静态规则）
./miniprogram-privacy-auto.sh /path/to/miniprogram --disable-ai

# 设置 AI 分析深度
export AI_ANALYSIS_DEPTH=deep  # deep | normal | quick
```

---

**参考**：
- [AI Agent 分析报告](AI_AGENT_ANALYSIS.md)
- [混合架构设计](DIRECTORY_STRUCTURE_OPTIMIZATION.md)
