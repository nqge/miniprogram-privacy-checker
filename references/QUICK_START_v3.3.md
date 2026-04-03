# 小程序隐私合规检查工具 v3.3 - 快速开始指南

## 🚀 快速安装

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/miniprogram-privacy-checker

# 2. 安装依赖
pip install -r requirements.txt

# 3. 验证安装
python3 -c "import docx; import openpyxl; print('依赖安装成功')"
```

## 📋 使用方法

### 方法 1: 一键运行（推荐）

```bash
# 检查小程序项目
./miniprogram-privacy-auto.sh /path/to/miniprogram

# 检查 .wxapkg 文件（自动反编译）
./miniprogram-privacy-auto.sh /path/to/app.wxapkg

# 指定输出目录
./miniprogram-privacy-auto.sh /path/to/miniprogram /custom/output/dir
```

### 方法 2: 分步运行

```bash
# 1. 运行基础检查（阶段 1-12）
./miniprogram-privacy-auto.sh /path/to/miniprogram

# 2. AI 自动更新 Excel
python3 core/enhanced_ai_excel_fill.py \
    --result-dir privacy_check_results \
    --base-path . \
    --enable-ai

# 3. AI 智能分析生成 Word 报告
python3 core/enhanced_word_report_generator.py \
    --template "小程序个人信息保护合规检查报告模板.docx" \
    --result-dir privacy_check_results \
    --miniprogram-name "小程序名称" \
    --output "输出文件路径.docx" \
    --enable-ai
```

## 📊 输出文件

### 核心报告

1. **{小程序名称}小程序隐私合规检查报告.docx** ⭐
   - AI 智能分析生成
   - 6 个关键段落自动更新
   - 字体样式统一（宋体，5号）

2. **权限确认单.xlsx** ⭐
   - 38 项权限的业务功能说明（AI 生成）
   - 38 项权限的必要性说明（AI 生成）

3. **自评估表.xlsx** ⭐
   - 28 个评估点的评估结果（AI 生成）
   - 28 个评估点的评估说明（AI 生成）
   - 颜色标记（符合/不符合/部分符合）

### 辅助报告

4. **权限确认单.txt** - 38 项权限的文本确认单
5. **自评估表.txt** - 28 个评估点的文本自评估表
6. **privacy_compliance_report.md** - 综合合规报告
7. **summary_report.txt** - 概要报告

### 原始数据

8. **permission_check.json** - 权限检查结果
9. **api_scan.json** - API 扫描结果
10. **dataflow_analysis.json** - 数据流分析结果
11. **privacy_policy_check.json** - 隐私政策检查结果
12. **self_assessment.json** - 自评估结果
13. **permission_confirmation.json** - 权限确认结果
14. **sdk_detection.json** - SDK 检测结果
15. **hybrid_check.json** - 混合检测结果

## 🎯 检查阶段

### 基础检查（阶段 1-8）

1. ✅ 权限声明检查
2. ✅ 敏感 API 扫描
3. ✅ 数据流分析
4. ✅ 动态调试风险检测
5. ✅ 日志泄露风险检测
6. ✅ 隐私政策检查
7. ✅ 隐私政策命名检查
8. ✅ SDK 使用检测

### 高级检查（阶段 9-12）

9. ✅ 混合架构检测（静态规则 + AI 智能体）
10. ✅ 生成权限确认单（38 项权限）
11. ✅ 生成自评估表（28 个评估点）
12. ✅ 生成详细权限报告

### AI 增强（阶段 13-15）

13. ✅ Excel 自动填写（AI 生成业务功能和必要性说明）
14. ✅ Word 报告生成（AI 智能分析生成 6 个关键段落）
15. ✅ AI 智能体引擎深度分析

### 综合报告（阶段 16-17）

16. ✅ 生成综合报告（Markdown 格式）
17. ✅ 生成概要报告（文本格式）

## 🔧 配置选项

### AI 分析

```bash
# 启用 AI 分析（需要配置 LLM API）
python3 core/enhanced_word_report_generator.py \
    --template "模板.docx" \
    --result-dir privacy_check_results \
    --enable-ai

# 禁用 AI 分析（使用规则引擎）
python3 core/enhanced_word_report_generator.py \
    --template "模板.docx" \
    --result-dir privacy_check_results
```

### 输出目录

```bash
# 默认输出目录
./miniprogram-privacy-auto.sh /path/to/miniprogram
# 输出到: privacy_check_results/

# 自定义输出目录
./miniprogram-privacy-auto.sh /path/to/miniprogram /custom/output
# 输出到: /custom/output/
```

## 📝 注意事项

1. **依赖安装**
   - 必须安装 `python-docx` 和 `openpyxl`
   - 使用 `pip install -r requirements.txt`

2. **模板文件**
   - 确保 `小程序个人信息保护合规检查报告模板.docx` 存在
   - 模板文件必须包含 76 个段落

3. **Excel 文件**
   - 确保 `权限确认单.xlsx` 和 `自评估表.xlsx` 存在
   - 建议备份原始文件

4. **AI 分析**
   - 默认使用规则引擎（更稳定）
   - 启用 AI 需要配置 LLM API

## 🎯 下一步

1. 查看 Word 报告（主要输出）
2. 检查 Excel 文件（详细数据）
3. 阅读综合报告（总体评估）
4. 根据建议修复问题

---

**版本**: v3.3
**更新时间**: 2026-03-31
**维护者**: 小红🌸
