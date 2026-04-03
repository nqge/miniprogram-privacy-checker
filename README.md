# 小程序隐私合规检查技能 v3.4

> 微信小程序个人信息保护合规性检查工具包

[![Version](https://img.shields.io/badge/version-3.4-brightgreen.svg)](https://github.com/nqge/miniprogram-privacy-checker)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-orange.svg)](https://openclaw.ai)

## ✨ 特性

- 🔍 **15 个检查阶段** - 全面覆盖隐私合规要求
- 🤖 **混合架构** - 静态规则 + AI 智能体双重检测
- 📊 **自动生成报告** - 权限确认单、自评估表、Word 报告
- 🚀 **一键运行** - 简单易用的自动化脚本
- 📝 **详细文档** - 完整的使用指南和参考资料

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/nqge/miniprogram-privacy-checker.git

# 安装依赖
pip install -r requirements.txt

# 运行检查
./miniprogram-privacy-auto.sh /path/to/miniprogram
```

## 📋 检查内容

1. 权限声明检查
2. 敏感 API 扫描（30+ 微信 API）
3. 数据流分析
4. 动态调试风险检测
5. 日志泄露风险检测
6. 隐私政策检查
7. 隐私政策命名检查
8. SDK 使用检测
9. 混合架构检测
10. 静态规则引擎
11. AI 智能体引擎
12. 权限确认单生成
13. 自评估表生成
14. 详细权限报告
15. Excel 自动填写

## 📊 输出文件

- `权限确认单.txt` - 38 项权限详细确认
- `自评估表.txt` - 28 个评估点自评估
- `详细权限报告.txt` - 类人工分析报告
- `{小程序名称}小程序隐私合规检查报告.docx` - Word 格式完整报告

## 📖 文档

- [快速开始](references/QUICK_START_v3.3.md)
- [权限映射表](references/permission_mapping.md)
- [AI 分析指南](references/ai_analysis_guide.md)
- [Excel 填写指南](references/excel_fill_guide.md)
- [更新日志](CHANGELOG.md)

## 🔧 技术架构

```
混合检测架构
├── 静态规则引擎（快速）
│   ├── 30+ 微信官方敏感 API
│   ├── 已知风险模式库
│   └── 规则匹配系统
└── AI 智能体引擎（深度）
    ├── 代码语义分析
    ├── 未知风险发现
    └── 智能评估系统
```

## 📦 目录结构

```
miniprogram-privacy-checker/
├── SKILL.md                 # 技能核心指令
├── miniprogram-privacy-auto.sh  # 主脚本
├── requirements.txt         # Python 依赖
├── src/                     # 源代码
│   ├── api_scanner.py
│   ├── permission_checker.py
│   ├── ai_agent_engine.py
│   └── ...
├── core/                    # 核心模块
├── scripts/                 # 辅助脚本
├── templates/               # Excel/Word 模板
├── references/              # 详细文档
│   ├── permission_mapping.md
│   ├── ai_analysis_guide.md
│   └── excel_fill_guide.md
└── tests/                   # 测试文件
```

## 🎯 v3.4 更新

### 重大优化

- **SKILL.md 压缩 89%** - 从 1169 行减少到 126 行
- **符合 AgentSkills 规范** - 遵循 skill-creator 最佳实践
- **优化上下文使用** - 核心指令始终加载，详细文档按需加载
- **改进可维护性** - 清晰的文件结构和模块化组织

### 新增文档

- `references/permission_mapping.md` - 权限映射表
- `references/ai_analysis_guide.md` - AI 分析指南
- `references/excel_fill_guide.md` - Excel 填写指南

详见 [CHANGELOG.md](CHANGELOG.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - AI Agent 平台
- [微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/) - 开发文档

---

**维护者**: 小红🌸  
**GitHub**: https://github.com/nqge/miniprogram-privacy-checker
