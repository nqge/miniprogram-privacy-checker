# 小程序隐私合规检查技能

自动检测微信小程序是否符合《微信小程序个人信息保护规范》和《App违法违规收集使用个人信息行为认定方法》。

## 🎯 功能特性

- ✅ **权限声明检查** - 验证 app.json 中的权限声明是否完整
- ✅ **敏感 API 扫描** - 检测代码中的敏感 API 调用
- ✅ **数据流分析** - 分析数据收集、存储、传输流程
- ✅ **动态调试风险检测** - 检测生产环境中的调试工具和配置
- ✅ **日志泄露风险检测** - 检测日志输出中的敏感信息
- ✅ **隐私政策检查** - 检查隐私政策文件的完整性
- ✅ **自动反编译** - 支持 .wxapkg 文件自动反编译
- ✅ **合规报告生成** - 自动生成综合合规报告和修复建议

## 🚀 快速开始

### 方式 1: 使用自动化脚本（推荐）

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/miniprogram-privacy

# 运行自动化检查
./miniprogram-privacy-auto.sh /path/to/miniprogram

# 查看报告
cat privacy_check_results/privacy_compliance_report.md
```

### 方式 2: 使用单个工具

```bash
# 1. 权限声明检查
python3 core/permission_checker.py /path/to/miniprogram -o privacy_check_results

# 2. 敏感 API 扫描
python3 core/api_scanner.py /path/to/miniprogram -o privacy_check_results

# 3. 数据流分析
python3 core/dataflow_analyzer.py /path/to/miniprogram -o privacy_check_results

# 4. 隐私政策检查
python3 core/privacy_policy_checker.py /path/to/miniprogram -o privacy_check_results

# 5. 生成综合报告
python3 core/report_generator.py -r privacy_check_results -o privacy_compliance_report.md
```

## 📋 检查流程

```
小程序源代码或 .wxapkg 文件
    ↓
[1/7] 权限声明检查
    ↓
[2/7] 敏感 API 扫描
    ↓
[3/7] 数据流分析
    ↓
[4/7] 动态调试风险检测
    - 检测调试工具（vConsole、eruda）
    - 检测调试配置
    - 检测 SourceMap 泄露
    ↓
[5/7] 日志泄露风险检测
    - 检测敏感信息日志输出
    - 检测认证凭证泄露
    - 检测个人信息泄露
    ↓
[6/7] 隐私政策检查
    ↓
[7/7] 生成综合报告
    ↓
隐私合规报告
```

## 📊 合规评分

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | ⭐⭐⭐⭐⭐ 优秀 | 合规性很高，审核通过概率大 |
| 70-89 | ⭐⭐⭐⭐ 良好 | 整体合规，有少量需要改进 |
| 50-69 | ⭐⭐⭐ 一般 | 存在一些风险，需要修复 |
| 30-49 | ⭐⭐ 较差 | 存在较多问题，审核可能不通过 |
| 0-29 | ⭐ 极差 | 严重违规，审核大概率不通过 |

## 📁 目录结构

```
miniprogram-privacy/
├── SKILL.md                           # 核心技能文档
├── README.md                           # 本文件
├── miniprogram-privacy-auto.sh           # 自动化检查脚本
├── core/
│   ├── permission_checker.py             # 权限声明检查
│   ├── api_scanner.py                  # 敏感 API 扫描
│   ├── dataflow_analyzer.py             # 数据流分析
│   ├── privacy_policy_checker.py        # 隐私政策检查
│   └── report_generator.py              # 合规报告生成器
└── templates/
    └── privacy_policy_template.md       # 隐私政策模板
```

## 📝 输出文件

```
privacy_check_results/
├── permission_check.json               # 权限检查结果（JSON）
├── permission_check_report.txt        # 权限检查报告（文本）
├── api_scan.json                      # API 扫描结果（JSON）
├── api_scan_report.txt                 # API 扫描报告（文本）
├── dataflow_analysis.json              # 数据流分析结果（JSON）
├── dataflow_report.txt                 # 数据流分析报告（文本）
├── privacy_policy_check.json           # 隐私政策检查结果（JSON）
├── privacy_policy_report.txt           # 隐私政策检查报告（文本）
└── privacy_compliance_report.md       # 综合合规报告（Markdown）
```

## 🔧 常见问题

### Q: 报告显示缺少权限声明，但我已经声明了？

A: 请检查 app.json 中 permission 字段的格式是否正确，权限名称是否拼写正确。

### Q: 如何修复敏感 API 调用问题？

A: 参考报告中的修复建议，通常需要：
1. 在 app.json 中添加权限声明
2. 在调用 API 前检查用户授权状态
3. 在获得用户同意后才调用敏感 API

### Q: 隐私政策应该放在哪里？

A: 可以放在以下位置之一：
- 小程序根目录：`privacy.md` 或 `隐私政策.txt`
- pages 目录：`pages/privacy.md`

### Q: 如何使用隐私政策模板？

A:
```bash
# 复制模板
cp templates/privacy_policy_template.md /path/to/miniprogram/privacy.md

# 根据实际情况编辑模板
vim /path/to/miniprogram/privacy.md
```

## 📚 参考标准

本技能基于以下官方标准：

- 《网络安全标准实践指南-移动互联网应用程序（App）系统权限申请使用指南》
- 《App违法违规收集使用个人信息行为认定方法》
- 《网络安全标准实践指南—移动互联网应用程序（App）收集使用个人信息自评估指南》
- 《网络安全标准实践指南-移动互联网应用程序（App）个人信息保护常见问题及处置指南》

## 🌸 维护者

小红 - 专注于网络安全和自动化工具开发的数字女性 AI 伙伴

---

**祝你审核顺利！** 🎉
