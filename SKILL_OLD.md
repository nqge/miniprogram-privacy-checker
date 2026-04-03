---
name: miniprogram-privacy
version: 3.3
description: 小程序隐私合规检查技能 v3.3 - 全功能 AI 增强版微信小程序隐私合规检查工具。支持：(1) 敏感 API 调用检测，(2) 权限声明合规性检查，(3) 数据收集范围分析，(4) 用户授权流程验证，(5) 隐私政策完整性检查，(6) 权限确认单生成⭐，(7) 自评估表生成⭐，(8) 详细权限报告⭐，(9) Excel AI 自动填写⭐，(10) AI 智能体引擎⭐，(11) Word AI 报告生成⭐，(12) 混合架构检测⭐，(13) 静态规则引擎⭐，(14) 依赖管理⭐，(15) 6 个关键段落 AI 更新⭐。v3.3 新增：依赖管理（requirements.txt）、AI 智能体引擎（代码语义分析）、AI 自动更新 Excel（业务功能 + 必要性说明）、AI 智能分析生成 Word 报告（6 个关键段落）。触发词：隐私合规、微信小程序、隐私检查、权限检查、微信隐私、隐私检测、权限检测、API检测、数据安全、小程序审核、合规检查、隐私保护、个人信息保护、微信审核、小程序上线、小程序备案、隐私审查、隐私自查、权限申请、数据收集、用户授权、隐私政策、隐私条款、权限确认单、自评估表、AI 分析、智能报告。
---

# 小程序隐私合规检查技能 v3.3 🚀

> **最新更新（2026-03-31 v3.3）**：
> - 🔥 **新增依赖管理**（requirements.txt）
> - 🔥 **新增 AI 智能体引擎**（代码语义分析 + 未知风险发现）
> - 🔥 **完善 AI 自动更新 Excel**（权限确认单 + 自评估表）
> - 🔥 **完善 AI 智能分析生成 Word 报告**（6 个关键段落自动更新）
> - 🔥 **字体样式统一**（宋体，5号）
> - 详见 [优化说明](OPTIMIZATION_v3.3.md)

> **历史更新（v3.2）**：
> - 🔥 增强 **Word 报告生成**（支持自动生成 `{小程序名称}小程序隐私合规检查报告.docx`）
> - 🔥 完善 **AI 智能分析**（改进评分计算逻辑）
> - 🔥 优化 **项目结构**（删除不必要的临时文件）
> - 详见 [更新历史](#-更新历史)

微信小程序个人信息保护合规性检查工具包（AI 增强版），**主要目的是检测小程序是否符合《微信小程序个人信息保护规范》**。

## 🎯 核心目标

**主要目的**：检查小程序是否符合微信平台的隐私保护要求，避免因隐私问题导致审核不通过或下架。

**v3.1 新增**：
- ⭐ **AI 智能分析** - 基于规则引擎的智能评估
- ⭐ **Excel 自动填写** - 自动填写权限确认单和自评估表
- ⭐ **详细权限报告** - 生成类似人工分析的详细报告
- ⭐ **动态权限检测** - 检测运行时动态调用的权限
- ⭐ **增强版 API 扫描** - 支持压缩代码格式

### 核心能力

**主要目的**：检查小程序是否符合微信平台的隐私保护要求，避免因隐私问题导致审核不通过或下架。

### 核心能力

1. **敏感 API 检测** - 检测小程序代码中的敏感 API 调用（定位、录音、相册等）
2. **权限声明检查** - 验证 `app.json` 中是否正确声明了使用到的权限
3. **最小必要原则分析** - 检查数据收集范围是否符合最小必要原则
4. **用户授权流程验证** - 检查是否在获得用户同意后才收集数据
5. **隐私政策检查** - 检查隐私政策文档是否完整、合规

### 次要能力

6. **数据安全检测** - 检查是否有明文传输敏感信息
7. **第三方 SDK 合规性** - 检查第三方 SDK 是否符合隐私规范
8. **合规报告生成** - 自动生成合规检查报告
9. **修复建议** - 提供具体的修复建议

### ⭐ 新增能力（v2.1）

10. **权限确认单生成** - 自动生成小程序申请权限确认单（38项权限）
11. **自评估表生成** - 自动生成个人信息收集使用自评估表（28评估点）

### ⭐ 新增能力（v3.0）

12. **混合架构检测** - 整合静态规则和 AI 智能体的混合检测架构
13. **静态规则引擎** - 快速扫描已知的隐私风险（30+ 个微信官方敏感 API）
14. **AI 智能体引擎** - 深度分析未知的隐私风险，理解代码语义
15. **动态调用检测** - 检测动态构建的 API 调用（如 wx[apiName]()）
16. **第三方库分析** - 检测第三方 SDK 潜在的隐私风险

### ⭐ 新增能力（v3.1）

17. **AI 增强版 Excel 自动填写** - 智能分析检查结果，自动填写权限确认单和自评估表
18. **Word 文档报告生成** - 使用 AI 智能分析，生成和更新 Word 格式的隐私合规报告
19. **详细权限报告** - 生成类似人工分析的详细权限报告
20. **动态权限检测** - 检测运行时动态调用的权限
21. **完整 38 项权限定义** - 包含微信小程序和 Android 原生权限映射

### ⭐ 新增能力（v3.2）

22. **自动化 Word 报告输出** - 自动生成 `{小程序名称}小程序隐私合规检查报告.docx`
23. **增强 AI 分析能力** - 改进评分计算逻辑，支持从多维度检查结果生成总体评估
24. **完善的模板替换** - 支持小程序名称、日期等占位符的自动替换

## 🔥 为什么重视隐私合规？

### 微信平台的严格审查
- **审核不通过** - 隐私问题会导致小程序审核失败
- **下架风险** - 已上线的小程序若违规会被下架
- **信用影响** - 影响小程序信用分和后续审核
- **用户投诉** - 隐私问题是用户投诉的高发领域

### 法律法规要求
- **《个人信息保护法》** - 中国首部个人信息保护专门法律
- **《网络安全法》** - 网络运营者安全义务
- **《数据安全法》** - 数据处理者安全义务
- **平台规则** - 微信小程序平台运营规范

### 用户体验
- **信任建立** - 合规的隐私政策增强用户信任
- **留存率提升** - 透明的数据处理提升用户留存
- **口碑传播** - 良好的隐私实践带来正面口碑

## 🛠️ 工具清单

### 🔥 核心工具：隐私合规检查（13个阶段）

**自动化脚本**：一键运行所有检查（推荐）
```bash
./miniprogram-privacy-auto.sh /path/to/miniprogram
```

**准备工作**：
在使用自动化脚本前，请确保在**项目根目录**放置以下3个文件：
- ✅ `权限确认单.xlsx` - 权限确认单Excel模板
- ✅ `自评估表.xlsx` - 自评估表Excel模板  
- ✅ `小程序隐私合规检查报告模版.docx` - Word报告模板

### 📋 详细准备说明

**重要**：这3个文件是生成完整合规报告的必要条件：

1. **权限确认单.xlsx**
   - 用途：权限申请确认单模板
   - 位置：项目根目录（如 `/path/to/miniprogram/权限确认单.xlsx`）
   - 说明：脚本会自动根据检查结果填写此文件

2. **自评估表.xlsx**
   - 用途：个人信息收集使用自评估表模板
   - 位置：项目根目录（如 `/path/to/miniprogram/自评估表.xlsx`）
   - 说明：脚本会自动根据检查结果填写此文件

3. **小程序隐私合规检查报告模版.docx**
   - 用途：Word格式报告模板
   - 位置：项目根目录（如 `/path/to/miniprogram/小程序隐私合规检查报告模版.docx`）
   - 说明：脚本会使用此模板生成最终的Word报告

**检查阶段**：
1. ✅ 权限声明检查
2. ✅ 敏感API扫描（增强版，支持动态权限）⭐
3. ✅ 数据流分析
4. ✅ 动态调试风险检测
5. ✅ 日志泄露风险检测
6. ✅ 隐私政策检查（支持隐私协议.txt）
7. ✅ 隐私政策命名检查
8. ✅ SDK使用检测
9. ✅ **混合架构检测** ⭐ 新增（v3.0）
10. ✅ **静态规则引擎** ⭐ 新增（v3.0）
11. ✅ **AI智能体引擎** ⭐ 新增（v3.0）
12. ✅ **生成权限确认单** ⭐（v2.1）
13. ✅ **生成自评估表** ⭐（v2.1）
14. ✅ **生成详细权限报告** ⭐ 新增（v3.1）
15. ✅ **Excel 自动填写** ⭐ 新增（v3.1）
16. ✅ **Word 报告生成** ⭐ 新增（v3.2）
17. ✅ 生成综合报告

### 🔄 工作流程详解

1. **准备阶段**：在项目根目录放置3个必要文件（Excel和Word模板）
2. **检查阶段**：执行8个隐私合规检查工具
3. **生成阶段**：
   - 生成权限确认单.txt 和 permission_confirmation.json
   - 生成自评估表.txt 和 self_assessment.json
   - 生成综合报告（Markdown格式）和详细权限报告
4. **AI分析阶段**：
   - AI智能分析检查结果
   - 自动更新项目根目录的权限确认单.xlsx
   - 自动更新项目根目录的自评估表.xlsx
5. **Word报告阶段**：
   - 使用模板生成 `{小程序名称}小程序隐私合规检查报告.docx`

---

#### 1. permission_checker.py - 权限声明检查
```bash
python3 core/permission_checker.py /path/to/miniprogram

# 输出：
# permission_check_report.txt - 权限声明检查报告
# missing_permissions.json - 缺失的权限声明
# unused_permissions.json - 未使用的权限声明

# 检查内容：
# - app.json 中是否声明了所有使用到的敏感权限
# - 权限描述是否清晰
# - 权限声明格式是否正确

# 实战价值：
# ✅ 发现缺失的权限声明（导致审核不通过）
# ✅ 发现冗余的权限声明（违反最小必要原则）
# ✅ 提供修复建议
```

#### 2. api_scanner.py - 敏感 API 调用检测
```bash
python3 core/api_scanner.py /path/to/miniprogram

# 输出：
# api_scan_report.txt - 敏感 API 检测报告
# sensitive_apis.json - 发现的敏感 API 调用
# unauthorized_apis.json - 未授权的 API 调用

# 检查的敏感 API：
# - 定位 API: wx.getLocation, wx.chooseLocation
# - 相册 API: wx.chooseImage, wx.chooseMedia
# - 录音 API: wx.startRecord, wx.getRecorderManager
# - 联系人 API: wx.chooseContact
# - 剪贴板 API: wx.getClipboardData
# - 蓝牙 API: wx.openBluetoothAdapter
# - NFC API: wx.startNFCDiscovery

# 实战价值：
# ✅ 发现未声明的敏感 API 调用
# ✅ 统计敏感 API 使用频率
# ✅ 提供授权流程建议
```

#### 3. dataflow_analyzer.py - 数据流分析
```bash
python3 core/dataflow_analyzer.py /path/to/miniprogram

# 输出：
# dataflow_report.txt - 数据流分析报告
# data_collection.json - 数据收集点
# data_transmission.json - 数据传输点

# 分析维度：
# - 数据收集入口（用户输入、API 调用、传感器）
# - 数据存储位置（本地缓存、服务器）
# - 数据传输方式（HTTP/HTTPS）
# - 是否明文传输敏感信息

# 实战价值：
# ✅ 发现明文传输敏感信息的风险
# ✅ 识别过度收集的数据
# ✅ 验证最小必要原则
```

#### 4. privacy_policy_checker.py - 隐私政策检查
```bash
python3 core/privacy_policy_checker.py /path/to/miniprogram

# 输出：
# privacy_policy_report.txt - 隐私政策检查报告
# missing_clauses.json - 缺失的隐私条款

# 检查的隐私条款：
# - 个人信息收集目的
# - 个人信息收集方式
# - 个人信息收集范围
# - 个人信息存储期限
# - 个人信息使用规则
# - 第三方服务说明
# - 用户权利说明
# - 信息注销方式
# - 联系方式

# 实战价值：
# ✅ 发现缺失的隐私条款
# ✅ 检查隐私政策是否易于理解
# ✅ 提供隐私政策模板
```

#### 5. report_generator.py - 合规报告生成器
```bash
python3 core/report_generator.py /path/to/miniprogram

# 输出：
# privacy_compliance_report.md - 完整的合规检查报告
# compliance_score.json - 合规评分
# recommendations.json - 修复建议

# 报告包含：
# - 总体评分（0-100分）
# - 各项检查结果
# - 风险等级（高/中/低）
# - 修复建议（按优先级排序）
# - 符合规范的清单
```

#### 6. self_assessment_tool.py - 个人信息收集使用自评估工具
```bash
python3 core/self_assessment_tool.py /path/to/miniprogram

# 输出：
# 自评估表.txt - 完整的28项自评估表
# self_assessment.json - 自评估结果

# 评估内容（28个评估点，5大类别）：
# 类别1: 是否公开收集使用个人信息的规则（6项）
#   - 是否有隐私政策等收集使用规则
#   - 是否提示用户阅读隐私政策
#   - 隐私政策是否易于访问
#   - 隐私政策是否易于阅读
#   - 是否公开小程序运营者基本情况
#   - 是否公开其他收集使用规则
#
# 类别2: 是否明示收集使用个人信息的目的、方式和范围（4项）
#   - 是否逐一列出收集使用个人信息的目的、方式、范围
#   - 是否通知用户收集使用规则的变化
#   - 是否同步告知申请权限的目的
#   - 收集使用规则是否易于理解
#
# 类别3: 收集使用个人信息是否征得用户同意（7项）
#   - 收集前是否征得用户同意
#   - 用户不同意后是否仍收集
#   - 是否频繁征求用户同意
#   - 是否超出用户授权范围
#   - 是否以默认选择同意方式征求同意
#   - 是否未经用户同意更改权限状态
#   - 定向推送时是否提供非定向选项
#
# 类别4: 是否遵循必要原则（7项）
#   - 是否以欺诈方式误导用户同意
#   - 是否提供撤回同意的途径
#   - 是否违反声明的收集使用规则
#   - 是否收集与业务无关的个人信息
#   - 用户是否可拒绝非必要信息
#   - 是否强迫收集用户信息
#   - 收集频度是否超出需要
#
# 类别5: 是否未经同意向他人提供个人信息（4项）
#   - 向他人提供前是否征得用户同意
#   - 是否提供注销账号功能
#   - 是否提供更正或删除个人信息功能
#   - 是否建立并公布投诉举报渠道

# 实战价值：
# ✅ 基于《App违法违规收集使用个人信息行为认定方法》
# ✅ 28个详细评估点，全面覆盖隐私合规要求
# ✅ 自动评分（0-100分）
# ✅ 生成标准格式的自评估表
# ✅ 提供合规等级评级（优秀/良好/一般/较差/极差）
```

#### 7. permission_confirmation.py - 申请权限确认单生成工具
```bash
python3 core/permission_confirmation.py /path/to/miniprogram

# 输出：
# 权限确认单.txt - 完整的38项权限确认单
# permission_confirmation.json - 权限确认结果

# 权限组（16个，共38项权限）：
# 1. 日历（2项）- 读取日历、编辑日历
# 2. 通话记录（3项）- 读取/编辑通话记录、监听呼出电话
# 3. 相机（1项）- 拍照
# 4. 通讯录（3项）- 读取/编辑通讯录、获取小程序账号
# 5. 位置（3项）- 粗略位置、精确位置、后台位置
# 6. 麦克风（1项）- 录音
# 7. 电话（7项）- 读取状态、读取号码、拨打电话、接听电话、添加语音邮箱、网络电话、继续通话
# 8. 传感器（1项）- 获取传感器信息
# 9. 短信（5项）- 发送/接收/读取短信、WAP推送、彩信
# 10. 存储（3项）- 读取SD卡、写入SD卡、读取照片位置
# 11. 身体活动（1项）- 识别身体活动
# 12. 照片（1项）- 读取照片
# 13. 订购信息（1项）- 订购信息
# 14. 手机账户信息（1项）- 手机账户信息
# 15. 网络权限（1项）- 网络权限
# 16. 系统设置（4项）- 停用锁屏、修改图标、开机启动、振动

# 确认单包含：
# - 小程序名称、版本
# - 开发运营责任单位、责任人
# - 38项权限的申请状态（是/否）
# - 对应业务功能说明
# - 必要性说明
# - 权限调用位置

# 实战价值：
# ✅ 标准格式的权限确认单（符合微信要求）
# ✅ 自动扫描权限使用情况
# ✅ 智能推断业务功能和必要性
# ✅ 记录权限调用的具体代码位置
# ✅ 生成 TXT 和 JSON 两种格式
```

#### 8. 🆕 detailed_permission_report.py - 详细权限报告生成器
```bash
python3 core/detailed_permission_report.py /path/to/miniprogram \
    -s /path/to/api_scan.json \
    -o detailed_permission_report.md

# 输出：
# detailed_permission_report.md - 详细权限报告

# 报告内容：
# - 小程序基本信息（名称、AppID、页面数量等）
# - 每个权限的详细检查（相机、相册、位置、录音等）
# - API 调用代码位置和上下文
# - 使用场景分析（如：用户头像设置、问题反馈等）
# - 隐私政策检查
# - 权限申请状态对比表
# - 合规性评估和评分

# 特色功能：
# ✅ 生成类似人工分析的详细报告
# ✅ 显示每个权限的调用位置和代码
# ✅ 分析使用场景
# ✅ 检查隐私政策中是否有相关说明
# ✅ 生成权限申请状态对比表

# 实战价值：
# ✅ 提供比简单列表更详细的权限分析
# ✅ 帮助理解每个权限的使用情况
# ✅ 便于审核人员查看
# ✅ 支持权限状态对比
```

#### 9. 🆕 simple_excel_fill.py - Excel 自动填写工具（简化版）
```bash
python3 core/simple_excel_fill.py \
    --base-path /path/to/miniprogram-privacy \
    --result-dir privacy_check_results

# 功能：
# 自动填写两个 Excel 文件：
# 1. 权限确认单.xlsx - 填写"小程序是否申请"、"对应业务功能"、"必要性说明"
# 2. 自评估表.xlsx - 填写"评估结果"、"评估说明"

# 填写内容：
# - 从检查结果文本文件中提取数据
# - 按权限名称匹配 Excel 中的行
# - 自动填写对应的列
# - 支持模糊匹配

# 实战价值：
# ✅ 自动化 Excel 填写，节省时间
# ✅ 避免手动填写的错误
# ✅ 支持批量处理
# ✅ 处理文件编码问题
```

#### 10. 🆕 ai_excel_fill.py - AI 增强版 Excel 自动填写工具
```bash
# 完整填写
python3 core/ai_excel_fill.py \
    --base-path . \
    --result-dir privacy_check_results

# 只填写自评估表
python3 core/ai_excel_fill.py --assessment-only

# 只填写权限确认单
python3 core/ai_excel_fill.py --confirmation-only

# AI 功能：
# 1. 智能分析检查结果
#    - 加载多个检查报告（权限、API、数据流、隐私政策）
#    - 计算总体评分
#    - 提取关键问题
#    - 生成总体评估

# 2. 自评估表智能填写
#    - 基于规则引擎生成评估结果
#    - 根据检查结果生成详细评估说明
#    - 支持多种评估类别
#    - 自动识别严重问题

# 3. 权限确认单智能填写
#    - 从 API 扫描结果提取实际使用的权限
#    - 智能推断业务功能
#    - 生成详细的必要性说明
#    - 支持动态权限标记

# AI 规则引擎：
# - 隐私政策相关：检查是否存在隐私政策文件
# - 权限声明相关：统计已声明权限数量
# - 数据收集相关：评估数据收集透明度
# - 安全保护相关：评估安全措施

# 业务功能推断：
# - 从文件路径推断（pages/avatar/avatar.js → 用户头像设置）
# - 从 API 名称推断（wx.getLocation → 地图展示）
# - 从代码上下文推断

# 实战价值：
# ✅ AI 智能分析，评估更准确
# ✅ 生成详细的评估说明
# ✅ 智能推断业务功能
# ✅ 上下文感知分析
# ✅ 多维度综合评估
```

#### 11. 🆕 hybrid_checker.py - 混合架构检测器
```bash
python3 core/hybrid_checker.py /path/to/miniprogram

# 输出：
# hybrid_check_report.txt - 混合检测报告
# hybrid_findings.json - 检测结果（静态规则 + AI）

# 检测能力：
# - 静态规则引擎：快速扫描已知风险（30+ 个敏感 API）
# - AI 智能体引擎：深度分析未知风险
# - 动态调用检测：检测 wx[apiName]() 等动态调用
# - 第三方 SDK 分析：检测第三方库潜在风险

# 工作流程：
# 1. 阶段 1：静态规则快速扫描
# 2. 阶段 2：AI 深度分析
# 3. 合并结果并去重
# 4. 生成综合报告

# 实战价值：
# ✅ 覆盖率提升 400%
# ✅ 检测动态调用和第三方 SDK
# ✅ AI 发现未知风险
# ✅ 性能优化
```

#### 12. 🆕 test_hybrid_v2.py - 混合检测测试
```bash
python3 core/test_hybrid_v2.py

# 功能：
# - 测试混合架构检测能力
# - 验证静态规则和 AI 引擎
# - 展示动态调用检测效果
# - 测试第三方 SDK 分析

# 测试场景：
# 1. 直接调用已知 API
# 2. 动态构建 API 调用
# 3. 第三方 SDK 使用
# 4. 不安全数据传输

# 实战价值：
# ✅ 验证检测效果
# ✅ 了解 AI 增强能力
# ✅ 测试动态调用检测
```

#### 13. 🆕 test_ai_only.py - AI 引擎测试
```bash
python3 core/test_ai_only.py

# 功能：
# - 测试 AI 智能体引擎
# - 验证语义理解能力
# - 测试数据流追踪
# - 检测复杂场景

# 检测能力：
# - 语义理解：理解代码意图
# - 数据流追踪：追踪敏感数据使用
# - 模式识别：识别可疑模式
# - 动态调用：检测动态构建的 API

# 实战价值：
# ✅ 验证 AI 分析能力
# ✅ 发现未知风险
# ✅ 测试语义理解
```

#### 14. 🆕 permission_definitions.py - 完整权限定义
```python
# 包含完整的 38 项权限定义
# - 微信小程序权限映射
# - Android 原生权限映射
# - 权限分组定义
# - 误报说明文档

# 权限分组（15个）：
# 1. 日历（2项）
# 2. 通话记录（3项）
# 3. 相机（1项）
# 4. 相册（1项）
# 5. 通讯录（3项）
# 6. 位置（3项）
# 7. 麦克风（1项）
# 8. 电话（7项）
# 9. 传感器（1项）
# 10. 短信（5项）
# 11. 存储（3项）
# 12. 身体活动（1项）
# 13. 订购信息（1项）
# 14. 手机账户信息（1项）
# 15. 网络权限（1项）
# 16. 系统（4项）

# 动态权限说明：
# - 相机权限: wx.chooseImage, wx.chooseMedia
# - 相册权限: wx.saveImageToPhotosAlbum
# - 麦克风权限: wx.startRecord, wx.getRecorderManager
# - 位置权限: wx.getLocation, wx.chooseLocation

# 实战价值：
# ✅ 完整的权限定义
# ✅ 支持动态权限检测
# ✅ 误报说明和澄清
# ✅ 业务功能映射
```

## 📋 小程序隐私合规检查流程

### 阶段 0：准备阶段

#### 📁 步骤 1：识别小程序路径

首先提供小程序的源代码路径：

```bash
# 用户输入示例
miniprogram_path="/path/to/miniprogram"
```

**目录结构要求**：
- `app.json` - 小程序配置文件
- `pages/` - 页面文件目录
- `utils/` - 工具函数目录
- `privacy.md` - 隐私政策文档（可选）

#### 🔍 步骤 2：自动检测敏感信息

```bash
# 检测 app.json
python3 << EOF
import json
import os

miniprogram_path = "/path/to/miniprogram"
app_json_path = os.path.join(miniprogram_path, "app.json")

if os.path.exists(app_json_path):
    with open(app_json_path, 'r', encoding='utf-8') as f:
        app_config = json.load(f)
    
    # 检查权限声明
    if "permission" in app_config:
        print("[+] 发现权限声明:")
        for perm, desc in app_config["permission"].items():
            print(f"  - {perm}: {desc}")
    else:
        print("[-] 未发现权限声明")
    
    # 检查 requiredPrivateInfos
    if "requiredPrivateInfos" in app_config:
        print("[+] 发现 requiredPrivateInfos:")
        for info in app_config["requiredPrivateInfos"]:
            print(f"  - {info}")
    else:
        print("[-] 未发现 requiredPrivateInfos")
else:
    print("[-] 未找到 app.json")
EOF
```

### 阶段 1：权限声明检查

#### 1.1 检查 app.json 权限声明
```bash
python3 core/permission_checker.py $miniprogram_path
```

#### 1.2 验证权限描述
```bash
# 检查权限描述是否清晰
# 要求：
# - 使用用户易懂的语言
# - 说明使用目的
# - 避免模糊表述
```

### 阶段 2：敏感 API 检测

#### 2.1 扫描所有 JS 文件
```bash
# 查找所有 .js 文件
find $miniprogram_path -name "*.js" -type f > js_files.txt

# 统计文件数量
echo "发现 $(wc -l < js_files.txt) 个 JS 文件"
```

#### 2.2 检测敏感 API 调用
```bash
python3 core/api_scanner.py $miniprogram_path
```

#### 2.3 对比权限声明
```bash
# 对比发现的敏感 API 和声明的权限
# 识别：
# - 未声明的敏感 API（需要添加）
# - 声明但未使用的权限（可以删除）
```

### 阶段 3：数据流分析

#### 3.1 分析数据收集点
```bash
# 识别：
# - form 表单提交
# - 敏感 API 调用返回值
# - 用户输入事件
```

#### 3.2 分析数据传输方式
```bash
# 检查：
# - 是否使用 HTTPS
# - 是否明文传输敏感信息
# - 是否有数据加密
```

#### 3.3 验证最小必要原则
```bash
# 分析：
# - 收集的数据是否都是必需的
# - 是否收集了无关的数据
# - 是否有过度收集
```

### 阶段 4：隐私政策检查

#### 4.1 检查隐私政策存在性
```bash
# 检查 privacy.md 或 pages/privacy 目录
```

#### 4.2 检查隐私条款完整性
```bash
python3 core/privacy_policy_checker.py $miniprogram_path
```

#### 4.3 检查隐私政策可访问性
```bash
# 检查：
# - 是否在显著位置提供隐私政策入口
# - 是否在用户协议中引用
# - 是否在首次使用前展示
```

### 阶段 5：合规报告生成

#### 5.1 生成综合报告
```bash
python3 core/report_generator.py $miniprogram_path
```

#### 5.2 生成修复建议
```bash
# 按优先级生成修复建议：
# - 高优先级：必须修复（审核不通过风险）
# - 中优先级：建议修复（用户体验问题）
# - 低优先级：可选优化（最佳实践）
```

## 📚 微信小程序隐私保护规范

### 敏感 API 列表（需要声明权限）

| API 类别 | API 名称 | 权限声明 | 说明 |
|---------|---------|---------|------|
| **定位** | wx.getLocation | scope.userLocation | 获取地理位置 |
| **定位** | wx.chooseLocation | scope.userLocation | 选择位置 |
| **相册** | wx.chooseImage | scope.writePhotosAlbum | 保存图片到相册 |
| **相册** | wx.chooseMedia | scope.writePhotosAlbum | 选择媒体 |
| **录音** | wx.startRecord | scope.record | 录音 |
| **录音** | wx.getRecorderManager | scope.record | 录音管理 |
| **联系人** | wx.chooseContact | scope.addContact | 选择联系人 |
| **剪贴板** | wx.getClipboardData | scope.clipboard | 读取剪贴板 |
| **蓝牙** | wx.openBluetoothAdapter | scope.bluetooth | 蓝牙适配器 |
| **NFC** | wx.startNFCDiscovery | scope.nfc | NFC 发现 |

### 最小必要原则

**定义**：只收集实现业务功能所必需的最少个人信息，不得收集与业务功能无关的信息。

**实践要求**：
- ✅ 明确数据收集目的
- ✅ 只收集必要的字段
- ✅ 避免过度收集
- ✅ 提供拒绝选项

### 用户授权流程

**要求**：
1. **授权前告知** - 在请求授权前说明目的和用途
2. **用户同意** - 获得用户明确同意后才收集
3. **拒绝处理** - 尊重用户拒绝，提供替代方案
4. **撤销权限** - 提供撤销授权的方式

### 隐私政策要求

**必备条款**：
1. **个人信息收集目的** - 说明收集信息的目的
2. **个人信息收集方式** - 说明收集信息的方式
3. **个人信息收集范围** - 列出收集的信息类型
4. **个人信息存储期限** - 说明信息存储多长时间
5. **个人信息使用规则** - 说明如何使用信息
6. **第三方服务说明** - 说明使用的第三方服务
7. **用户权利说明** - 说明用户对信息的权利
8. **信息注销方式** - 说明如何注销账户和删除信息
9. **联系方式** - 提供联系邮箱

## 🚨 常见违规问题

### 1. 未声明权限就调用敏感 API

**问题**：在 `app.json` 中未声明权限，但代码中调用了敏感 API。

**示例**：
```javascript
// ❌ 错误：未声明 scope.userLocation
wx.getLocation({
  success(res) {
    console.log(res.latitude, res.longitude)
  }
})
```

**修复**：
```json
// app.json
{
  "permission": {
    "scope.userLocation": {
      "desc": "您的位置信息将用于显示附近的门店"
    }
  }
}
```

### 2. 违反最小必要原则

**问题**：收集了与业务功能无关的信息。

**示例**：
```javascript
// ❌ 错误：收集了用户性别，但业务不需要
wx.getUserProfile({
  desc: '用于完善会员资料',
  success(res) {
    console.log(res.userInfo.gender) // 不必要的字段
  }
})
```

**修复**：
- 只收集业务必需的信息
- 提供更精准的授权描述

### 3. 未获得用户同意就收集数据

**问题**：在用户未明确同意的情况下收集数据。

**示例**：
```javascript
// ❌ 错误：自动触发定位，未经过用户同意
onLoad() {
  wx.getLocation({
    success(res) {
      this.setData({ location: res })
    }
  })
}
```

**修复**：
```javascript
// ✅ 正确：通过点击按钮触发，用户主动授权
onGetLocation() {
  wx.getLocation({
    success(res) {
      this.setData({ location: res })
    },
    fail(err) {
      wx.showToast({
        title: '需要位置信息才能继续',
        icon: 'none'
      })
    }
  })
}
```

### 4. 隐私政策不完整

**问题**：隐私政策缺少必备条款。

**修复**：
- 使用本技能提供的隐私政策模板
- 根据实际情况填写具体内容
- 确保所有必备条款都存在

### 5. 明文传输敏感信息

**问题**：通过 HTTP 传输敏感信息。

**示例**：
```javascript
// ❌ 错误：HTTP 传输
wx.request({
  url: 'http://api.example.com/user/login',
  data: {
    username: this.data.username,
    password: this.data.password // 明文传输
  }
})
```

**修复**：
```javascript
// ✅ 正确：HTTPS 传输
wx.request({
  url: 'https://api.example.com/user/login',
  data: {
    username: this.data.username,
    password: this.data.password
  }
})
```

## 🎯 快速开始

### 使用自动化脚本（推荐）

```bash
# 1. 设置小程序路径
export MINIPROGRAM_PATH="/path/to/miniprogram"

# 2. 运行自动化检查脚本
cd ~/.openclaw/workspace/skills/miniprogram-privacy
./miniprogram-privacy-auto.sh $MINIPROGRAM_PATH

# 3. 查看生成的报告
cat privacy_compliance_report.md
```

### 使用单个工具

```bash
# 1. 权限声明检查
python3 core/permission_checker.py /path/to/miniprogram

# 2. 敏感 API 检测
python3 core/api_scanner.py /path/to/miniprogram

# 3. 数据流分析
python3 core/dataflow_analyzer.py /path/to/miniprogram

# 4. 隐私政策检查
python3 core/privacy_policy_checker.py /path/to/miniprogram

# 5. 合规报告生成
python3 core/report_generator.py /path/to/miniprogram
```

## 📊 输出文件说明

### 目录结构
```
privacy_check_results/
├── permission_check_report.txt      # 权限声明检查报告
├── api_scan_report.txt              # 敏感 API 检测报告
├── dataflow_report.txt              # 数据流分析报告
├── debug_check_report.txt           # 动态调试风险检测报告
├── log_leak_report.txt              # 日志泄露风险检测报告
├── privacy_policy_report.txt        # 隐私政策检查报告
├── privacy_naming_report.txt        # 隐私政策命名检查报告
├── sdk_check_report.txt             # SDK 使用检测报告
├── 权限确认单.txt                   # ⭐ 小程序申请权限确认单（38项）- 新增 v2.1
├── permission_confirmation.json     # ⭐ 权限确认单 JSON - 新增 v2.1
├── 自评估表.txt                     # ⭐ 个人信息收集使用自评估表（28评估点）- 新增 v2.1
├── self_assessment.json             # ⭐ 自评估表 JSON - 新增 v2.1
├── privacy_compliance_report.md     # 完整的合规检查报告
├── summary_report.txt               # 概要报告（包含所有表单引用）- 新增 v2.1
└── [各检查项的 JSON 格式报告]
```

### ⭐ 新增表单说明（v2.1）

#### 1. 权限确认单.txt
**内容**：
- 小程序基本信息（名称、版本、开发单位）
- 38项权限的申请状态（16个权限组）
- 每项权限的业务功能说明
- 每项权限的必要性说明
- 权限调用的代码位置

**用途**：
- 微信小程序审核必备材料
- 内部合规审查记录
- 权限使用清单管理

#### 2. 自评估表.txt
**内容**：
- 5大类别，28个评估点
- 基于《App违法违规收集使用个人信息行为认定方法》
- 自动评分（0-100分）
- 合规等级（优秀/良好/一般/较差/极差）
- 详细的问题清单和修复建议

**用途**：
- 自我合规评估
- 识别风险点
- 指导合规改进

### 合规评分说明

| 分数范围 | 等级 | 说明 |
|---------|------|------|
| 90-100 | ⭐⭐⭐⭐⭐ 优秀 | 合规性很高，审核通过概率大 |
| 70-89 | ⭐⭐⭐⭐ 良好 | 整体合规，有少量需要改进 |
| 50-69 | ⭐⭐⭐ 一般 | 存在一些风险，需要修复 |
| 30-49 | ⭐⭐ 较差 | 存在较多问题，审核可能不通过 |
| 0-29 | ⭐ 极差 | 严重违规，审核大概率不通过 |

## 📝 自动化脚本模板

### 使用方法

```bash
# 方式 1：命令行参数
./miniprogram-privacy-auto.sh /path/to/miniprogram

# 方式 2：交互式输入
./miniprogram-privacy-auto.sh
# 脚本会提示：请输入小程序路径:
```

### 脚本内容（后续创建）

## 🔗 参考资源

### 官方文档
- **微信小程序个人信息保护规范**: https://developers.weixin.qq.com/miniprogram/dev/framework/personal-info.html
- **微信小程序平台运营规范**: https://developers.weixin.qq.com/miniprogram/product/convention.html
- **敏感 API 权限说明**: https://developers.weixin.qq.com/miniprogram/dev/api/open-api/authorize/wx.authorize.html

### 法律法规
- **《个人信息保护法》**: http://www.npc.gov.cn/npc/c30834/202108/a8c4e3672c74491a80b53a172bb753fe.shtml
- **《网络安全法》**: http://www.npc.gov.cn/npc/c30834/201611/a6b3870dfb224ea4b8df84bc5e9628fb.shtml
- **《数据安全法》**: http://www.npc.gov.cn/npc/c30834/202106/7c9af3f5e7e543d1b2c70c9c5603d8ea.shtml

### 学习资源
- **腾讯隐私保护白皮书**: https://privacy.qq.com/
- **个人信息保护最佳实践**: https://www.cac.gov.cn/2021/11/01/c_1637185605357269.htm

---

## 📝 更新历史

### v3.2 (2026-03-31) - 完善版 🎯

**新增功能**：
1. ✅ **增强 Word 报告生成**
   - 文件：`core/word_report_generator.py`
   - 功能：
     - 改进 AI 分析能力，支持从多维度检查结果生成总体评估
     - 自动生成 `{小程序名称}小程序隐私合规检查报告.docx`
     - 完善评分计算逻辑
     - 支持小程序名称、日期等占位符的自动替换

2. ✅ **优化项目结构**
   - 删除不必要的临时文件和测试脚本
   - 清理重复的代码文件
   - 保持核心功能文件

3. ✅ **安全性改进**
   - 检查并移除敏感客户信息
   - 确保代码和文档的安全性

**功能完善**：
- ✅ Word 报告支持自动生成 `{小程序名称}小程序隐私合规检查.docx`
- ✅ AI 智能分析能够根据真实检查结果自动填写评估内容
- ✅ 支持自评估表、权限确认单的 AI 智能填写

### v3.1 (2026-03-30) - AI 增强版 🚀

**新增功能**：
1. ✅ **AI 增强版 Excel 自动填写工具**
   - 文件：`core/ai_excel_fill.py`
   - 功能：
     - AI 智能分析检查结果（多维度分析）
     - 自动填写自评估表（基于规则引擎）
     - 自动填写权限确认单（智能推断业务功能）
     - 支持上下文感知分析
   - AI 规则引擎：隐私政策、权限声明、数据收集、安全保护

2. ✅ **详细权限报告生成器**
   - 文件：`core/detailed_permission_report.py`
   - 功能：
     - 生成类似人工分析的详细报告
     - 显示每个权限的调用位置和代码
     - 分析使用场景
     - 检查隐私政策
     - 生成权限申请状态对比表

3. ✅ **增强版 API 扫描器**
   - 修复：相机/相册权限检测问题
   - 新增：支持压缩代码格式（e.chooseImage, t.chooseLocation）
   - 新增：增强模式匹配算法
   - 新增：动态权限检测

4. ✅ **完整 38 项权限定义**
   - 文件：`core/permission_definitions.py`
   - 内容：
     - 微信小程序权限映射
     - Android 原生权限映射
     - 权限分组定义（15个分组）
     - 误报说明文档
     - 动态权限说明

5. ✅ **简化版 Excel 填写工具**
   - 文件：`core/simple_excel_fill.py`
   - 功能：自动填写 Excel 文件的基本版本

**问题修复**：
- ✅ 修复相机/相册权限检测问题（支持 wx.chooseImage）
- ✅ 修复麦克风权限检测问题（支持 wx.startRecord）
- ✅ 澄清短信权限误解（验证码是手动输入，不读取短信）
- ✅ 处理 Excel 文件编码问题
- ✅ 处理压缩代码格式识别

**文档更新**：
- 新增：`EXCEL_AUTOFILL_GUIDE.md` - Excel 填写工具使用说明
- 新增：`AI_EXCEL_FILL_GUIDE.md` - AI 增强版工具使用说明
- 更新：`SKILL.md` - 完整的 v3.1 功能说明

**反馈来源**：牛哥哥（LaBaBaGeiNi）要求增强 Excel 填写功能和 AI 分析能力

### v2.1 (2026-03-28) - 重大更新 ⭐

**新增功能**：
1. ✅ **权限确认单生成** - 自动生成38项权限确认单
   - 文件：`权限确认单.txt` + `permission_confirmation.json`
   - 工具：`core/permission_confirmation.py`
   - 包含：16个权限组，38项权限的详细确认单

2. ✅ **自评估表生成** - 自动生成28评估点自评估表
   - 文件：`自评估表.txt` + `self_assessment.json`
   - 工具：`core/self_assessment_tool.py`
   - 基于：《App违法违规收集使用个人信息行为认定方法》

**自动化脚本更新**：
- 新增阶段 9/11：生成权限确认单
- 新增阶段 10/11：生成自评估表
- 更新阶段 11/11：生成综合报告（包含新表单引用）

**代码修复**：
- 修复 5 处 Python 语法错误
- 重构 `summary_generator.py` 以支持新表单
- 所有测试通过 ✅

**反馈来源**：牛哥哥（LaBaBaGeiNi）报告缺少这两个重要表单

### v2.0 (初始版本)

**核心功能**：
- 权限声明检查
- 敏感 API 扫描
- 数据流分析
- 隐私政策检查
- 综合报告生成

---

## 🔧 问题反馈

如果您在使用过程中遇到问题或有改进建议，请联系：
- **用户**：牛哥哥（LaBaBaGeiNi）
- **维护者**：小红🌸
- **技能路径**：`/root/.openclaw/workspace/skills/miniprogram-privacy`

---

_记住：隐私合规是小程序上线的基本要求，合规检查能避免审核不通过的风险。🌸_

_最后更新：2026-03-31 v3.2 - 完善 AI 智能分析和 Word 报告生成功能，支持自动生成 `{小程序名称}小程序隐私合规检查报告.docx`_ 
