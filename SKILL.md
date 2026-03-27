---
name: miniprogram-privacy
description: 小程序隐私合规检查技能 - 检测微信小程序是否符合《微信小程序个人信息保护规范》。用于：(1) 敏感 API 调用检测，(2) 权限声明合规性检查，(3) 数据收集范围分析，(4) 用户授权流程验证，(5) 隐私政策完整性检查。触发词：小程序、隐私合规、微信小程序、隐私检查、权限检查、微信隐私、隐私检测、权限检测、API检测、数据安全、小程序审核、合规检查、隐私保护、个人信息保护、微信审核、小程序上线、小程序备案、隐私审查、审核自查、隐私自查、权限申请、敏感信息、个人信息、数据收集、用户授权、隐私政策、隐私条款。
---

# 小程序隐私合规检查技能

微信小程序个人信息保护合规性检查工具包，**主要目的是检测小程序是否符合《微信小程序个人信息保护规范》**。

## 🎯 核心目标

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

### 🔥 核心工具：隐私合规检查

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
├── missing_permissions.json          # 缺失的权限声明
├── unused_permissions.json           # 未使用的权限声明
├── api_scan_report.txt              # 敏感 API 检测报告
├── sensitive_apis.json              # 发现的敏感 API 调用
├── unauthorized_apis.json           # 未授权的 API 调用
├── dataflow_report.txt              # 数据流分析报告
├── data_collection.json             # 数据收集点
├── data_transmission.json           # 数据传输点
├── privacy_policy_report.txt        # 隐私政策检查报告
├── missing_clauses.json            # 缺失的隐私条款
├── privacy_compliance_report.md     # 完整的合规检查报告
├── compliance_score.json            # 合规评分
└── recommendations.json            # 修复建议
```

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

_记住：隐私合规是小程序上线的基本要求，合规检查能避免审核不通过的风险。🌸_
