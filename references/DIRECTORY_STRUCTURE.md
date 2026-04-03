# 小程序隐私合规检查技能 - 目录结构 v3.3

**优化时间**: 2026-03-31
**版本**: v3.3

---

## 📁 目录结构

```
miniprogram-privacy-checker/
├── README.md                      # 项目说明（入口）
├── SKILL.md                       # 技能文档
├── CHANGELOG.md                   # 更新日志
├── QUICK_START.md                 # 快速开始指南
├── requirements.txt               # 依赖管理
│
├── bin/                           # 可执行文件
│   └── miniprogram-privacy-auto.sh  # 主自动化脚本
│
├── src/                           # 源代码
│   ├── __init__.py
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
│   │   └── ai_agent_engine.py     # AI 智能体引擎
│   │
│   ├── generators/                # 生成器模块
│   │   ├── __init__.py
│   │   ├── report_generator.py    # 报告生成器
│   │   ├── summary_generator.py   # 总结生成器
│   │   ├── permission_confirmation.py  # 权限确认单生成器
│   │   ├── self_assessment_tool.py    # 自评估表生成器
│   │   ├── detailed_permission_report.py  # 详细权限报告生成器
│   │   ├── word_report_generator.py     # Word 报告生成器
│   │   └── enhanced_word_report_generator.py  # 增强版 Word 报告生成器
│   │
│   ├── fillers/                   # 填充器模块
│   │   ├── __init__.py
│   │   ├── ai_excel_fill.py       # AI Excel 填充器
│   │   └── enhanced_ai_excel_fill.py  # 增强版 AI Excel 填充器
│   │
│   └── utils/                     # 工具模块
│       ├── __init__.py
│       ├── unpacker.py            # 反编译工具
│       └── permission_definitions.py  # 权限定义
│
├── templates/                     # 模板文件
│   ├── excel/
│   │   ├── 权限确认单.xlsx
│   │   └── 操作步骤指引参考.xlsx
│   │
│   └── word/
│       └── 小程序个人信息保护合规检查报告模板.docx
│
├── docs/                          # 文档
│   ├── AI_AGENT_ANALYSIS.md       # AI 智能体分析
│   ├── OPTIMIZATION_v3.3.md      # v3.3 优化说明
│   ├── OPTIMIZATION_COMPLETE_REPORT.md  # 优化完成报告
│   └── UPDATE.md                  # 更新说明
│
└── tests/                         # 测试
    └── __init__.py
```

---

## 🎯 模块说明

### bin/ - 可执行文件
- `miniprogram-privacy-auto.sh`: 主自动化脚本，一键运行所有检查

### src/ - 源代码
- `checkers/`: 各种检查器（权限、API、数据流等）
- `analyzers/`: 分析器（AI 智能体）
- `generators/`: 生成器（报告、总结、Excel、Word）
- `fillers/`: 填充器（Excel、Word 自动填写）
- `utils/`: 工具（反编译、配置、日志）

### templates/ - 模板文件
- `excel/`: Excel 模板（权限确认单、自评估表）
- `word/`: Word 模板（合规检查报告）

### docs/ - 文档
- AI 智能体分析文档
- 优化说明文档
- 更新说明文档

### tests/ - 测试
- 单元测试
- 集成测试

---

## 🚀 使用方法

### 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行检查
bin/miniprogram-privacy-auto.sh /path/to/miniprogram
```

### 作为模块使用

```python
# 导入检查器
from src.checkers import PermissionChecker, APIScanner

# 导入分析器
from src.analyzers import AIAgentEngine

# 导入生成器
from src.generators import ReportGenerator, WordReportGenerator

# 导入填充器
from src.fillers import AIExcelFiller
```

---

## 📊 优化效果

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

**版本**: v3.3
**更新时间**: 2026-03-31
**维护者**: 小红🌸
