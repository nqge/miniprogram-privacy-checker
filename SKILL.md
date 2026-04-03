---
name: miniprogram-privacy
description: 微信小程序隐私合规检查工具。检查敏感API调用、权限声明、数据收集范围、用户授权流程、隐私政策完整性。支持生成权限确认单、自评估表、Word报告。触发词：隐私合规、微信小程序、隐私检查、权限检查、小程序审核、合规检查、隐私保护、个人信息保护。
---

# 小程序隐私合规检查

检查微信小程序是否符合《微信小程序个人信息保护规范》。

## 快速开始

```bash
# 一键检查（推荐）
./miniprogram-privacy-auto.sh /path/to/miniprogram

# 输出位置
cd /path/to/miniprogram/privacy_report/
```

**准备工作**：在项目根目录放置以下模板文件：
- `权限确认单.xlsx`
- `自评估表.xlsx`
- `小程序隐私合规检查报告模版.docx`

## 检查内容

### 15 个检查阶段

1. **权限声明检查** - 验证 app.json 权限声明
2. **敏感 API 扫描** - 检测 30+ 个微信敏感 API
3. **数据流分析** - 追踪数据收集和传输
4. **动态调试风险** - 检测调试代码残留
5. **日志泄露风险** - 检查敏感信息日志
6. **隐私政策检查** - 验证隐私政策完整性
7. **隐私政策命名** - 检查文件命名规范
8. **SDK 使用检测** - 分析第三方 SDK
9. **混合架构检测** - 静态规则 + AI 智能体
10. **静态规则引擎** - 快速扫描已知风险
11. **AI 智能体引擎** - 深度分析未知风险
12. **权限确认单生成** - 38 项权限确认单
13. **自评估表生成** - 28 个评估点
14. **详细权限报告** - 类人工分析报告
15. **Excel 自动填写** - AI 智能填写表格

## 输出文件

| 文件 | 说明 |
|------|------|
| `权限确认单.txt` | 38 项权限详细确认 |
| `自评估表.txt` | 28 个评估点自评估 |
| `详细权限报告.txt` | 类人工分析报告 |
| `permission_confirmation.json` | 权限确认单数据 |
| `self_assessment.json` | 自评估表数据 |
| `{小程序名称}小程序隐私合规检查报告.docx` | Word 格式完整报告 |

## 敏感 API 列表

### 定位相关
- `wx.getLocation` - 获取当前位置
- `wx.chooseLocation` - 打开地图选择位置
- `wx.startLocationUpdate` - 开启位置更新

### 用户信息
- `wx.getUserInfo` - 获取用户信息
- `wx.getUserProfile` - 获取用户资料
- `wx.getPhoneNumber` - 获取手机号

### 媒体相关
- `wx.chooseImage` - 选择图片
- `wx.chooseVideo` - 选择视频
- `wx.startRecord` - 开始录音
- `wx.getRecorderManager` - 录音管理器

### 设备信息
- `wx.getSystemInfo` - 获取系统信息
- `wx.getNetworkType` - 获取网络类型
- `wx.getBluetoothDevices` - 获取蓝牙设备

### 通讯录
- `wx.addPhoneContact` - 添加通讯录
- `wx.getPhoneNumber` - 获取手机号

### 剪贴板
- `wx.setClipboardData` - 设置剪贴板
- `wx.getClipboardData` - 获取剪贴板

### 日历
- `wx.addPhoneCalendar` - 添加日历事件

## 常见问题

### Q: 检查失败怎么办？
A: 查看错误日志，根据提示修复问题后重新运行

### Q: Excel 模板在哪里？
A: 在技能目录的 `templates/` 文件夹

### Q: 如何自定义检查规则？
A: 修改 `src/rules/` 下的配置文件

## 技术架构

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

## 参考资料

- [微信小程序个人信息保护规范](https://developers.weixin.qq.com/miniprogram/dev/framework/user-privacy/)
- [权限映射表](references/permission_mapping.md)
- [AI 分析指南](references/ai_analysis_guide.md)
- [Excel 填写指南](references/excel_fill_guide.md)

---

**版本**: 3.4  
**更新时间**: 2026-04-04  
**作者**: 小红🌸
