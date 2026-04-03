# Excel 自动填写指南

## 功能说明

自动填写两个 Excel 表格：
1. **权限确认单** - 38 项权限的详细确认
2. **自评估表** - 28 个评估点的自评估

## 准备工作

### 1. 安装依赖

```bash
pip install openpyxl pandas
```

### 2. 准备模板文件

在项目根目录放置：
```
/path/to/miniprogram/
├── 权限确认单.xlsx
├── 自评估表.xlsx
└── 小程序隐私合规检查报告模版.docx
```

### 3. 运行检查

```bash
./miniprogram-privacy-auto.sh /path/to/miniprogram
```

## 自动填写逻辑

### 权限确认单填写规则

| 检测结果 | 填写内容 |
|---------|---------|
| 检测到 API 调用 | ✅ 使用了该权限 |
| 未检测到调用 | ❌ 未使用该权限 |
| 调用频率高 | 🔶 需要说明使用场景 |

### 自评估表填写规则

| 评估点 | AI 分析结果 |
|--------|------------|
| 是否收集用户信息 | 根据代码检测结果填写 |
| 是否符合最小必要原则 | AI 评估数据收集范围 |
| 是否获得用户授权 | 检查授权流程代码 |
| 是否有隐私政策 | 检查隐私政策文件 |

## 手动调整

如果自动填写不准确，可以手动修改：

```python
# 编辑填写结果
python3 src/ai_excel_fill.py \
  --input privacy_report/permission_confirmation.json \
  --template templates/权限确认单.xlsx \
  --output 权限确认单_已填写.xlsx \
  --manual-adjust
```

## 验证结果

```bash
# 检查填写是否正确
python3 scripts/validate_excel.py \
  --input 权限确认单_已填写.xlsx \
  --expected 38  # 应该有 38 项权限
```

---

**参考**：
- [Excel 填写详细指南](AI_EXCEL_FILL_GUIDE.md)
- [权限映射表](permission_mapping.md)
