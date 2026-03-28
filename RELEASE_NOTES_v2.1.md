# 小程序隐私合规检查工具 v2.1 发布说明

**发布日期**: 2026-03-28
**版本**: v2.1
**类型**: 功能更新（Feature Release）

---

## 🎉 重大更新

### ✨ 新增功能

#### 1. 小程序申请权限确认单生成器
- **工具**: `core/permission_confirmation.py`
- **输出**: `权限确认单.txt` + `permission_confirmation.json`
- **功能**:
  - 自动扫描小程序中的权限使用情况
  - 生成标准的 38 项权限确认单
  - 包含 16 个权限组的详细说明
  - 智能推断业务功能和必要性
  - 记录权限调用的代码位置

#### 2. 个人信息收集使用自评估工具
- **工具**: `core/self_assessment_tool.py`
- **输出**: `自评估表.txt` + `self_assessment.json`
- **功能**:
  - 基于《App违法违规收集使用个人信息行为认定方法》
  - 5 大类别，28 个详细评估点
  - 自动评分系统（0-100 分）
  - 合规等级评级（优秀/良好/一般/较差/极差）
  - 详细的问题清单和修复建议

### 🔧 自动化脚本更新

**文件**: `miniprogram-privacy-auto.sh`

**新增阶段**:
- **阶段 9/11**: 生成小程序申请权限确认单
- **阶段 10/11**: 生成个人信息收集使用自评估表
- **阶段 11/11**: 生成综合报告（包含新表单引用）

**检查流程**（11 个阶段）:
1. ✅ 权限声明检查
2. ✅ 敏感 API 扫描
3. ✅ 数据流分析
4. ✅ 动态调试风险检测
5. ✅ 日志泄露风险检测
6. ✅ 隐私政策检查
7. ✅ 隐私政策命名检查
8. ✅ SDK 使用检测
9. ✅ **生成权限确认单** ⭐ 新增
10. ✅ **生成自评估表** ⭐ 新增
11. ✅ 生成综合报告

### 🐛 代码修复

修复了以下文件的语法错误：
- ✅ `core/self_assessment_tool.py` (第 220、578 行)
- ✅ `core/report_generator.py` (第 308、670 行)
- ✅ `core/summary_generator.py` (完全重写)

**测试状态**: 所有测试通过 ✅

### 📝 文档更新

- ✅ 更新 `SKILL.md` 到 v2.1
- ✅ 添加版本号和更新历史
- ✅ 详细说明新增功能和输出文件
- ✅ 创建 `UPDATE.md` 详细更新说明
- ✅ 创建 `SKILL_UPDATE_v2.1.md` 更新记录

---

## 📊 输出文件更新

### 新增文件（v2.1）

```
privacy_check_results/
├── 权限确认单.txt                   # ⭐ 小程序申请权限确认单（38项）
├── permission_confirmation.json     # ⭐ 权限确认单 JSON
├── 自评估表.txt                     # ⭐ 个人信息收集使用自评估表（28评估点）
├── self_assessment.json             # ⭐ 自评估表 JSON
└── summary_report.txt               # ⭐ 概要报告（包含所有表单引用）
```

### 现有文件（保持不变）

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
└── privacy_compliance_report.md     # 完整的合规检查报告
```

---

## 🚀 使用方法

### 快速开始

```bash
# 克隆或更新仓库
git clone https://github.com/nqge/miniprogram-privacy-checker.git
cd miniprogram-privacy-checker

# 运行自动化检查（推荐）
./miniprogram-privacy-auto.sh /path/to/your/miniprogram

# 查看生成的报告
cat privacy_check_results/权限确认单.txt
cat privacy_check_results/自评估表.txt
```

### 单独使用新工具

```bash
# 生成权限确认单
python3 core/permission_confirmation.py /path/to/miniprogram

# 生成自评估表
python3 core/self_assessment_tool.py /path/to/miniprogram
```

---

## 🎯 适用场景

### 审核必备材料

这两个新增的表单是微信小程序审核的重要材料：

1. **权限确认单**
   - 用于说明小程序申请的每个权限及其用途
   - 必须在提交审核前准备好
   - 审核人员会逐一核对

2. **自评估表**
   - 用于自我评估隐私合规性
   - 帮助识别潜在风险点
   - 提供改进建议

### 合规审查

- ✅ 内部合规审查
- ✅ 第三方合规评估
- ✅ 隐私影响评估
- ✅ 风险识别和整改

---

## 📚 参考标准

本工具基于以下官方标准：

- **《网络安全标准实践指南-移动互联网应用程序（App）系统权限申请使用指南》**
- **《App违法违规收集使用个人信息行为认定方法》**
- **《网络安全标准实践指南—移动互联网应用程序（App）收集使用个人信息自评估指南》**
- **《网络安全标准实践指南-移动互联网应用程序（App）个人信息保护常见问题及处置指南》**
- **《微信小程序平台运营规范》**
- **《个人信息保护法》**
- **《网络安全法》**

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/nqge/miniprogram-privacy-checker
- **Issues**: https://github.com/nqge/miniprogram-privacy-checker/issues
- **Wiki**: https://github.com/nqge/miniprogram-privacy-checker/wiki

---

## 🙏 致谢

**特别感谢**: 牛哥哥（LaBaBaGeiNi）

感谢牛哥哥发现并报告了缺少这两个重要表单的问题，使得这次更新得以完成。

您的反馈帮助我们不断改进工具！🌸

---

## 📋 更新清单

### 新增
- [x] 权限确认单生成器
- [x] 自评估表生成器
- [x] 自动化脚本集成
- [x] 更新历史记录
- [x] 问题反馈渠道

### 修复
- [x] Python 语法错误（5 处）
- [x] 代码测试验证
- [x] 文档同步更新

### 改进
- [x] 报告格式优化
- [x] 输出文件说明
- [x] 用户体验提升

---

## 🔄 升级指南

### 从 v2.0 升级到 v2.1

1. **拉取最新代码**
   ```bash
   git pull origin main
   ```

2. **验证安装**
   ```bash
   ./test_fix.sh
   ```

3. **开始使用**
   ```bash
   ./miniprogram-privacy-auto.sh /path/to/miniprogram
   ```

### 兼容性

- ✅ 向后兼容 v2.0
- ✅ 无需修改现有配置
- ✅ 新增功能可选使用

---

**发布负责人**: 小红🌸
**发布日期**: 2026-03-28
**下次更新**: 根据用户反馈和需求

---

## 📞 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- **GitHub Issues**: https://github.com/nqge/miniprogram-privacy-checker/issues
- **用户**: 牛哥哥（LaBaBaGeiNi）
- **维护者**: 小红🌸

---

_让小程序隐私合规检查更简单、更完整！🎉_
