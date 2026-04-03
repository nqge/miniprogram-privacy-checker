# 小程序隐私合规检查技能 - 目录结构优化方案

**优化时间**: 2026-03-31
**版本**: v3.3
**目标**: 创建清晰、规范、易维护的目录结构

---

## 📁 当前目录结构

```
miniprogram-privacy-checker/
├── core/                           # 核心功能模块
│   ├── ai_agent_engine.py         # AI 智能体引擎
│   ├── api_scanner.py             # API 扫描器
│   ├── dataflow_analyzer.py       # 数据流分析器
│   ├── debug_checker.py           # 调试检查器
│   ├── detailed_permission_report.py  # 详细权限报告
│   ├── hybrid_checker.py          # 混合检查器
│   ├── log_leak_checker.py        # 日志泄露检查器
│   ├── miniprogram_privacy_checker_v2.py  # v2 版本检查器
│   ├── permission_checker.py      # 权限检查器
│   ├── permission_confirmation.py # 权限确认单生成器
│   ├── permission_definitions.py  # 权限定义
│   ├── privacy_naming_checker.py  # 隐私命名检查器
│   ├── privacy_policy_checker.py  # 隐私政策检查器
│   ├── report_generator.py        # 报告生成器
│   ├── sdk_detector.py            # SDK 检测器
│   ├── self_assessment_tool.py    # 自评估工具
│   ├── summary_generator.py       # 总结生成器
│   ├── unpacker.py                # 反编译工具
│   ├── update_word_report.py      # Word 报告更新工具
│   ├── word_report_generator.py   # Word 报告生成器
│   ├── enhanced_ai_excel_fill.py  # 增强版 AI Excel 填充工具
│   └── enhanced_word_report_generator.py  # 增强版 Word 报告生成器
├── 权限确认单.xlsx                 # 权限确认单模板
├── 操作步骤指引参考.xlsx           # 操作指南模板
├── 小程序个人信息保护合规检查报告模板.docx  # Word 报告模板
├── miniprogram-privacy-auto.sh     # 自动化脚本
├── word_report_generator.py        # Word 报告生成器（根目录副本）
├── requirements.txt               # 依赖管理
├── SKILL.md                       # 技能文档
├── README.md                      # 使用说明
├── UPDATE.md                      # 更新说明
├── CHANGELOG.md                   # 更新日志
├── OPTIMIZATION_v3.3.md          # v3.3 优化说明
├── QUICK_START_v3.3.md           # 快速开始指南
├── OPTIMIZATION_COMPLETE_REPORT.md  # 优化完成报告
└── AI_AGENT_ANALYSIS.md          # AI 智能体分析文档
```

---

## 🎯 优化后目录结构

```
miniprogram-privacy-checker/
├── README.md                      # 项目说明（入口）
├── SKILL.md                       # 技能文档
├── CHANGELOG.md                   # 更新日志
├── QUICK_START.md                 # 快速开始指南
├── requirements.txt               # 依赖管理
├── LICENSE                        # 许可证
│
├── bin/                           # 可执行文件
│   ├── miniprogram-privacy-auto.sh  # 主自动化脚本
│   └── install.sh                  # 安装脚本
│
├── src/                           # 源代码
│   ├── __init__.py
│   │
│   ├── checkers/                  # 检查器模块
│   │   ├── __init__.py
│   │   ├── permission.py          # 权限检查器
│   │   ├── api_scanner.py         # API 扫描器
│   │   ├── dataflow.py            # 数据流分析器
│   │   ├── debug.py               # 调试检查器
│   │   ├── log_leak.py            # 日志泄露检查器
│   │   ├── privacy_policy.py      # 隐私政策检查器
│   │   ├── privacy_naming.py      # 隐私命名检查器
│   │   ├── sdk.py                 # SDK 检测器
│   │   └── hybrid.py              # 混合检查器
│   │
│   ├── analyzers/                 # 分析器模块
│   │   ├── __init__.py
│   │   ├── ai_agent.py            # AI 智能体引擎
│   │   ├── code_analyzer.py       # 代码分析器
│   │   └── risk_analyzer.py       # 风险分析器
│   │
│   ├── generators/                # 生成器模块
│   │   ├── __init__.py
│   │   ├── report.py              # 综合报告生成器
│   │   ├── summary.py             # 总结生成器
│   │   ├── permission_confirmation.py  # 权限确认单生成器
│   │   ├── self_assessment.py     # 自评估表生成器
│   │   ├── detailed_permission.py  # 详细权限报告生成器
│   │   └── word_report.py         # Word 报告生成器
│   │
│   ├── fillers/                   # 填充器模块
│   │   ├── __init__.py
│   │   ├── excel_fill.py          # Excel 填充器
│   │   ├── ai_excel_fill.py       # AI Excel 填充器
│   │   └── word_fill.py           # Word 填充器
│   │
│   ├── utils/                     # 工具模块
│   │   ├── __init__.py
│   │   ├── unpacker.py            # 反编译工具
│   │   ├── definitions.py         # 权限定义
│   │   ├── config.py              # 配置管理
│   │   ├── logger.py              # 日志工具
│   │   └── exceptions.py          # 自定义异常
│   │
│   └── cli/                       # 命令行接口
│       ├── __init__.py
│       └── main.py                # 主命令行入口
│
├── templates/                     # 模板文件
│   ├── excel/
│   │   ├── 权限确认单.xlsx
│   │   └── 自评估表.xlsx
│   │
│   └── word/
│       └── 小程序个人信息保护合规检查报告模板.docx
│
├── docs/                          # 文档
│   ├── ARCHITECTURE.md            # 架构说明
│   ├── API.md                     # API 文档
│   ├── AI_AGENT_ANALYSIS.md       # AI 智能体分析
│   ├── OPTIMIZATION_v3.3.md      # v3.3 优化说明
│   └── UPDATE.md                  # 更新说明
│
├── tests/                         # 测试
│   ├── __init__.py
│   ├── test_checkers/            # 检查器测试
│   ├── test_analyzers/           # 分析器测试
│   ├── test_generators/          # 生成器测试
│   └── test_integration/         # 集成测试
│
├── examples/                      # 示例
│   ├── basic_usage.sh             # 基本用法示例
│   └── test_miniprogram/          # 测试用小程序
│
└── scripts/                       # 辅助脚本
    ├── install.sh                 # 安装脚本
    ├── setup_env.sh              # 环境设置脚本
    └── run_tests.sh              # 运行测试脚本
```

---

## 🔄 迁移步骤

### 步骤 1: 创建新目录结构

```bash
cd /root/.openclaw/workspace/skills/miniprogram-privacy-checker

# 创建新目录
mkdir -p bin src/checkers src/analyzers src/generators src/fillers src/utils src/cli
mkdir -p templates/excel templates/word
mkdir -p docs tests examples scripts
```

### 步骤 2: 迁移文件

```bash
# 迁移检查器
mv core/permission_checker.py src/checkers/permission.py
mv core/api_scanner.py src/checkers/api_scanner.py
mv core/dataflow_analyzer.py src/checkers/dataflow.py
mv core/debug_checker.py src/checkers/debug.py
mv core/log_leak_checker.py src/checkers/log_leak.py
mv core/privacy_policy_checker.py src/checkers/privacy_policy.py
mv core/privacy_naming_checker.py src/checkers/privacy_naming.py
mv core/sdk_detector.py src/checkers/sdk.py
mv core/hybrid_checker.py src/checkers/hybrid.py

# 迁移分析器
mv core/ai_agent_engine.py src/analyzers/ai_agent.py

# 迁移生成器
mv core/report_generator.py src/generators/report.py
mv core/summary_generator.py src/generators/summary.py
mv core/permission_confirmation.py src/generators/permission_confirmation.py
mv core/self_assessment_tool.py src/generators/self_assessment.py
mv core/detailed_permission_report.py src/generators/detailed_permission.py
mv core/word_report_generator.py src/generators/word_report.py
mv core/enhanced_word_report_generator.py src/generators/enhanced_word_report.py

# 迁移填充器
mv core/ai_excel_fill.py src/fillers/ai_excel_fill.py
mv core/enhanced_ai_excel_fill.py src/fillers/enhanced_ai_excel_fill.py

# 迁移工具
mv core/unpacker.py src/utils/unpacker.py
mv core/permission_definitions.py src/utils/definitions.py

# 迁移模板
mv "权限确认单.xlsx" templates/excel/
mv "操作步骤指引参考.xlsx" templates/excel/
mv "小程序个人信息保护合规检查报告模板.docx" templates/word/

# 迁移文档
mv AI_AGENT_ANALYSIS.md docs/
mv OPTIMIZATION_v3.3.md docs/
mv OPTIMIZATION_COMPLETE_REPORT.md docs/
mv UPDATE.md docs/

# 迁移脚本
mv miniprogram-privacy-auto.sh bin/

# 删除根目录的重复文件
rm word_report_generator.py
```

### 步骤 3: 更新导入路径

```bash
# 更新所有 Python 文件的导入路径
find src -name "*.py" -exec sed -i 's/from core\./from src\./g' {} \;
```

### 步骤 4: 创建 __init__.py 文件

```bash
# 创建 __init__.py 文件
touch src/__init__.py
touch src/checkers/__init__.py
touch src/analyzers/__init__.py
touch src/generators/__init__.py
touch src/fillers/__init__.py
touch src/utils/__init__.py
touch src/cli/__init__.py
touch tests/__init__.py
```

---

## 📝 更新文档

### 更新 README.md

```markdown
# 小程序隐私合规检查技能

## 快速开始

\`\`\`bash
# 安装依赖
pip install -r requirements.txt

# 运行检查
bin/miniprogram-privacy-auto.sh /path/to/miniprogram
\`\`\`

## 项目结构

\`\`\`
miniprogram-privacy-checker/
├── bin/           # 可执行文件
├── src/           # 源代码
│   ├── checkers/  # 检查器
│   ├── analyzers/ # 分析器
│   ├── generators/# 生成器
│   ├── fillers/   # 填充器
│   └── utils/     # 工具
├── templates/     # 模板文件
├── docs/          # 文档
└── tests/         # 测试
\`\`\`
```

### 更新 SKILL.md

```markdown
# 小程序隐私合规检查技能 v3.3

## 项目结构

- **bin/**: 可执行脚本
- **src/**: 源代码
  - **checkers/**: 各种检查器（权限、API、数据流等）
  - **analyzers/**: 分析器（AI 智能体、代码分析、风险分析）
  - **generators/**: 生成器（报告、总结、Excel、Word）
  - **fillers/**: 填充器（Excel、Word 自动填写）
  - **utils/**: 工具（反编译、配置、日志）
- **templates/**: 模板文件（Excel、Word）
- **docs/**: 文档
- **tests/**: 测试
```

---

## 🎯 优化效果

### 清晰度提升

- ✅ 功能模块清晰分离
- ✅ 文件分类合理
- ✅ 依赖关系明确

### 可维护性提升

- ✅ 易于查找文件
- ✅ 易于添加新功能
- ✅ 易于编写测试

### 可扩展性提升

- ✅ 模块化设计
- ✅ 插件化架构
- ✅ 标准化接口

---

## 📊 对比

| 方面 | 优化前 | 优化后 |
|------|--------|--------|
| 目录层级 | 2 层 | 3 层 |
| 模块化程度 | 低 | 高 |
| 文件分类 | 混乱 | 清晰 |
| 可维护性 | 中 | 高 |
| 可扩展性 | 中 | 高 |

---

**优化时间**: 2026-03-31
**版本**: v3.3
**维护者**: 小红🌸
