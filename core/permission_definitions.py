#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序权限定义
基于：微信小程序权限申请规范和 Android/iOS 权限标准
"""

# 微信小程序权限定义
WECHAT_PERMISSIONS = {
    # ===== 位置权限 =====
    'scope.userLocation': {
        'group': '位置',
        'name': '访问精确位置',
        'category': '位置信息',
        'risk_level': 'high',
        'description': '获取用户的精确地理位置信息',
        'api': ['wx.getLocation', 'wx.chooseLocation', 'wx.openLocation'],
        'dynamic_request': True  # 需要运行时动态请求
    },
    'scope.userLocationBackground': {
        'group': '位置',
        'name': '支持后台访问位置',
        'category': '位置信息',
        'risk_level': 'high',
        'description': '在后台持续获取地理位置信息',
        'api': ['wx.startLocationUpdate', 'wx.onLocationChange'],
        'dynamic_request': True
    },

    # ===== 相机权限 =====
    'scope.camera': {
        'group': '相机',
        'name': '拍照',
        'category': '相机',
        'risk_level': 'high',
        'description': '使用相机拍摄照片或视频',
        'api': ['wx.chooseImage', 'wx.chooseMedia', 'wx.createCameraContext'],
        'dynamic_request': True,
        'note': '通过 wx.chooseImage 等 API 动态调用，系统自动处理权限请求'
    },

    # ===== 相册权限 =====
    'scope.writePhotosAlbum': {
        'group': '相册',
        'name': '相册',
        'category': '存储',
        'risk_level': 'medium',
        'description': '保存图片或视频到相册',
        'api': ['wx.saveImageToPhotosAlbum', 'wx.saveVideoToPhotosAlbum'],
        'dynamic_request': True
    },

    # ===== 麦克风权限 =====
    'scope.record': {
        'group': '麦克风',
        'name': '录音',
        'category': '麦克风',
        'risk_level': 'high',
        'description': '录制音频',
        'api': ['wx.startRecord', 'wx.getRecorderManager'],
        'dynamic_request': True,
        'note': '通过 wx.startRecord 等 API 动态调用，系统自动处理权限请求'
    },

    # ===== 通讯录权限 =====
    'scope.addContact': {
        'group': '通讯录',
        'name': '读取通讯录',
        'category': '通讯录',
        'risk_level': 'high',
        'description': '读取用户通讯录信息',
        'api': ['wx.chooseContact'],
        'dynamic_request': True
    },

    # ===== 蓝牙权限 =====
    'scope.bluetooth': {
        'group': '传感器',
        'name': '蓝牙',
        'category': '蓝牙',
        'risk_level': 'medium',
        'description': '搜索和连接蓝牙设备',
        'api': ['wx.openBluetoothAdapter', 'wx.startBluetoothDevicesDiscovery'],
        'dynamic_request': True
    },

    # ===== 剪贴板权限 =====
    'scope.clipboard': {
        'group': '存储',
        'name': '剪贴板',
        'category': '剪贴板',
        'risk_level': 'medium',
        'description': '读取系统剪贴板内容',
        'api': ['wx.getClipboardData'],
        'dynamic_request': True
    },

    # ===== NFC 权限 =====
    'scope.nfc': {
        'group': '传感器',
        'name': 'NFC',
        'category': 'NFC',
        'risk_level': 'medium',
        'description': '使用近场通信功能',
        'api': ['wx.startNFCDiscovery'],
        'dynamic_request': True
    },

    # ===== 微信运动权限 =====
    'scope.werun': {
        'group': '身体活动',
        'name': '识别身体活动',
        'category': '身体活动',
        'risk_level': 'medium',
        'description': '获取微信运动步数',
        'api': ['wx.getWeRunData'],
        'dynamic_request': True
    },

    # ===== 收货地址权限 =====
    'scope.address': {
        'group': '通讯录',
        'name': '收货地址',
        'category': '通讯录',
        'risk_level': 'medium',
        'description': '获取用户收货地址',
        'api': ['wx.chooseAddress'],
        'dynamic_request': True
    },

    # ===== 发票权限 =====
    'scope.invoiceTitle': {
        'group': '订购信息',
        'name': '发票抬头',
        'category': '订购信息',
        'risk_level': 'low',
        'description': '获取用户发票抬头',
        'api': ['wx.chooseInvoiceTitle'],
        'dynamic_request': True
    },
    'scope.invoice': {
        'group': '订购信息',
        'name': '发票',
        'category': '订购信息',
        'risk_level': 'low',
        'description': '选择用户发票',
        'api': ['wx.chooseInvoice'],
        'dynamic_request': True
    },
}

# Android 原生权限映射（小程序可能涉及）
ANDROID_PERMISSIONS = {
    # ===== 日历权限 =====
    'android.permission.READ_CALENDAR': {
        'group': '日历',
        'name': '读取日历',
        'category': '日历',
        'risk_level': 'medium',
        'description': '读取日历事件',
        'note': '小程序不支持原生日历权限'
    },
    'android.permission.WRITE_CALENDAR': {
        'group': '日历',
        'name': '编辑日历',
        'category': '日历',
        'risk_level': 'medium',
        'description': '编辑日历事件',
        'note': '小程序不支持原生日历权限'
    },

    # ===== 通话记录权限 =====
    'android.permission.READ_CALL_LOG': {
        'group': '通话记录',
        'name': '读取通话记录',
        'category': '电话',
        'risk_level': 'high',
        'description': '读取通话记录',
        'note': '小程序不支持原生通话记录权限'
    },
    'android.permission.WRITE_CALL_LOG': {
        'group': '通话记录',
        'name': '编辑通话记录',
        'category': '电话',
        'risk_level': 'high',
        'description': '编辑通话记录',
        'note': '小程序不支持原生通话记录权限'
    },
    'android.permission.PROCESS_OUTGOING_CALLS': {
        'group': '通话记录',
        'name': '监听呼出电话',
        'category': '电话',
        'risk_level': 'high',
        'description': '监听呼出电话',
        'note': '小程序不支持原生电话权限'
    },

    # ===== 电话权限 =====
    'android.permission.READ_PHONE_STATE': {
        'group': '电话',
        'name': '读取电话状态',
        'category': '电话',
        'risk_level': 'high',
        'description': '读取电话状态',
        'note': '小程序不支持原生电话权限'
    },
    'android.permission.READ_PHONE_NUMBERS': {
        'group': '电话',
        'name': '读取本机电话号码',
        'category': '电话',
        'risk_level': 'high',
        'description': '读取本机电话号码',
        'note': '小程序不支持原生电话权限，但可通过 getPhoneNumber 获取用户授权的手机号'
    },
    'android.permission.CALL_PHONE': {
        'group': '电话',
        'name': '拨打电话',
        'category': '电话',
        'risk_level': 'high',
        'description': '直接拨打电话',
        'note': '小程序不支持，可使用 wx.makeEntPhoneCall 拨号（需用户确认）'
    },
    'android.permission.READ_CALL_LOG': {
        'group': '电话',
        'name': '接听电话',
        'category': '电话',
        'risk_level': 'high',
        'description': '接听电话',
        'note': '小程序不支持'
    },
    'android.permission.ADD_VOICEMAIL': {
        'group': '电话',
        'name': '添加语音邮箱',
        'category': '电话',
        'risk_level': 'medium',
        'description': '添加语音邮箱',
        'note': '小程序不支持'
    },
    'android.permission.USE_SIP': {
        'group': '电话',
        'name': '使用网络电话',
        'category': '电话',
        'risk_level': 'medium',
        'description': '使用 SIP 电话',
        'note': '小程序不支持'
    },

    # ===== 传感器权限 =====
    'android.permission.BODY_SENSORS': {
        'group': '传感器',
        'name': '获取传感器信息',
        'category': '传感器',
        'risk_level': 'medium',
        'description': '访问身体传感器（如心率）',
        'note': '小程序通过 werun 接口访问运动数据'
    },

    # ===== 短信权限 =====
    'android.permission.SEND_SMS': {
        'group': '短信',
        'name': '发送短信',
        'category': '短信',
        'risk_level': 'high',
        'description': '发送短信',
        'note': '小程序不支持原生短信权限'
    },
    'android.permission.RECEIVE_SMS': {
        'group': '短信',
        'name': '接收短信',
        'category': '短信',
        'risk_level': 'high',
        'description': '接收短信',
        'note': '小程序不支持原生短信权限，验证码需用户手动输入'
    },
    'android.permission.READ_SMS': {
        'group': '短信',
        'name': '读取短信',
        'category': '短信',
        'risk_level': 'high',
        'description': '读取短信内容',
        'note': '小程序不支持原生短信权限，getPhoneNumber 使用微信授权而非读取短信'
    },
    'android.permission.RECEIVE_WAP_PUSH': {
        'group': '短信',
        'name': '接收 WAP 推送',
        'category': '短信',
        'risk_level': 'medium',
        'description': '接收 WAP 推送消息',
        'note': '小程序不支持'
    },
    'android.permission.RECEIVE_MMS': {
        'group': '短信',
        'name': '接收彩信',
        'category': '短信',
        'risk_level': 'medium',
        'description': '接收彩信',
        'note': '小程序不支持'
    },

    # ===== 存储权限 =====
    'android.permission.READ_EXTERNAL_STORAGE': {
        'group': '存储',
        'name': '读取 SD 卡',
        'category': '存储',
        'risk_level': 'medium',
        'description': '读取外部存储',
        'note': '小程序通过文件 API 访问，无需原生存储权限'
    },
    'android.permission.WRITE_EXTERNAL_STORAGE': {
        'group': '存储',
        'name': '写入 SD 卡',
        'category': '存储',
        'risk_level': 'medium',
        'description': '写入外部存储',
        'note': '小程序通过文件 API 访问，无需原生存储权限'
    },
    'android.permission.ACCESS_MEDIA_LOCATION': {
        'group': '存储',
        'name': '读取照片位置信息',
        'category': '存储',
        'risk_level': 'medium',
        'description': '读取照片中的地理位置信息',
        'note': '小程序有限支持'
    },

    # ===== 账户权限 =====
    'android.permission.GET_ACCOUNTS': {
        'group': '手机账户信息',
        'name': '获取小程序账号',
        'category': '账户',
        'risk_level': 'medium',
        'description': '获取设备上的账户列表',
        'note': '小程序通过 wx.login 获取登录凭证'
    },
    'android.permission.USE_CREDENTIALS': {
        'group': '手机账户信息',
        'name': '手机账户信息',
        'category': '账户',
        'risk_level': 'medium',
        'description': '使用账户凭证',
        'note': '小程序不支持'
    },

    # ===== 网络权限 =====
    'android.permission.INTERNET': {
        'group': '网络权限',
        'name': '网络权限',
        'category': '网络',
        'risk_level': 'low',
        'description': '访问网络',
        'note': '小程序默认支持，无需声明'
    },

    # ===== 系统权限 =====
    'android.permission.DISABLE_KEYGUARD': {
        'group': '系统',
        'name': '停用锁屏',
        'category': '系统',
        'risk_level': 'high',
        'description': '禁用键盘锁',
        'note': '小程序不支持'
    },
    'android.permission.INSTALL_SHORTCUT': {
        'group': '系统',
        'name': '修改图标',
        'category': '系统',
        'risk_level': 'medium',
        'description': '安装桌面快捷方式',
        'note': '小程序不支持'
    },
    'android.permission.RECEIVE_BOOT_COMPLETED': {
        'group': '系统',
        'name': '开机启动',
        'category': '系统',
        'risk_level': 'medium',
        'description': '开机自动启动',
        'note': '小程序不支持'
    },
    'android.permission.VIBRATE': {
        'group': '系统',
        'name': '振动',
        'category': '系统',
        'risk_level': 'low',
        'description': '控制振动',
        'note': '小程序通过 wx.vibrateShort 等支持'
    },
}

# 权限分组定义（按你提供的顺序）
PERMISSION_GROUPS = [
    '日历',
    '通话记录',
    '相机',
    '通讯录',
    '位置',
    '麦克风',
    '电话',
    '传感器',
    '短信',
    '存储',
    '身体活动',
    '订购信息',
    '手机账户信息',
    '网络权限',
    '系统',
]

# 完整权限列表（按你提供的顺序）
FULL_PERMISSION_LIST = [
    # 日历
    {'group': '日历', 'name': '读取日历', 'wechat_scope': None, 'android': 'android.permission.READ_CALENDAR'},
    {'group': '日历', 'name': '编辑日历', 'wechat_scope': None, 'android': 'android.permission.WRITE_CALENDAR'},

    # 通话记录
    {'group': '通话记录', 'name': '读取通话记录', 'wechat_scope': None, 'android': 'android.permission.READ_CALL_LOG'},
    {'group': '通话记录', 'name': '编辑通话记录', 'wechat_scope': None, 'android': 'android.permission.WRITE_CALL_LOG'},
    {'group': '通话记录', 'name': '监听呼出电话', 'wechat_scope': None, 'android': 'android.permission.PROCESS_OUTGOING_CALLS'},

    # 相机
    {'group': '相机', 'name': '拍照', 'wechat_scope': 'scope.camera', 'android': None, 'note': '通过 wx.chooseImage 动态调用'},

    # 相册
    {'group': '相册', 'name': '相册', 'wechat_scope': 'scope.writePhotosAlbum', 'android': None},

    # 通讯录
    {'group': '通讯录', 'name': '读取通讯录', 'wechat_scope': 'scope.addContact', 'android': None},
    {'group': '通讯录', 'name': '编辑通讯录', 'wechat_scope': None, 'android': 'android.permission.WRITE_CONTACTS'},
    {'group': '通讯录', 'name': '获取小程序账号', 'wechat_scope': None, 'android': 'android.permission.GET_ACCOUNTS', 'note': '通过 wx.login 实现'},

    # 位置
    {'group': '位置', 'name': '访问粗略位置', 'wechat_scope': None, 'android': 'android.permission.ACCESS_COARSE_LOCATION', 'note': '小程序通过 scope.userLocation 统一处理'},
    {'group': '位置', 'name': '访问精确位置', 'wechat_scope': 'scope.userLocation', 'android': 'android.permission.ACCESS_FINE_LOCATION'},
    {'group': '位置', 'name': '支持后台访问位置', 'wechat_scope': 'scope.userLocationBackground', 'android': 'android.permission.ACCESS_BACKGROUND_LOCATION'},

    # 麦克风
    {'group': '麦克风', 'name': '录音', 'wechat_scope': 'scope.record', 'android': 'android.permission.RECORD_AUDIO', 'note': '通过 wx.startRecord 动态调用'},

    # 电话
    {'group': '电话', 'name': '读取电话状态', 'wechat_scope': None, 'android': 'android.permission.READ_PHONE_STATE'},
    {'group': '电话', 'name': '读取本机电话号码', 'wechat_scope': None, 'android': 'android.permission.READ_PHONE_NUMBERS', 'note': '通过 getPhoneNumber 实现'},
    {'group': '电话', 'name': '拨打电话', 'wechat_scope': None, 'android': 'android.permission.CALL_PHONE', 'note': '通过 wx.makeEntPhoneCall 实现'},
    {'group': '电话', 'name': '接听电话', 'wechat_scope': None, 'android': None},
    {'group': '电话', 'name': '添加语音邮箱', 'wechat_scope': None, 'android': 'android.permission.ADD_VOICEMAIL'},
    {'group': '电话', 'name': '使用网络电话', 'wechat_scope': None, 'android': 'android.permission.USE_SIP'},
    {'group': '电话', 'name': '继续进行来自其他小程序的通话', 'wechat_scope': None, 'android': None, 'note': '小程序不支持'},

    # 传感器
    {'group': '传感器', 'name': '获取传感器信息', 'wechat_scope': None, 'android': 'android.permission.BODY_SENSORS'},

    # 短信
    {'group': '短信', 'name': '发送短信', 'wechat_scope': None, 'android': 'android.permission.SEND_SMS'},
    {'group': '短信', 'name': '接收短信', 'wechat_scope': None, 'android': 'android.permission.RECEIVE_SMS'},
    {'group': '短信', 'name': '读取短信', 'wechat_scope': None, 'android': 'android.permission.READ_SMS', 'note': '小程序不支持，验证码需手动输入'},
    {'group': '短信', 'name': '接收 WAP 推送', 'wechat_scope': None, 'android': 'android.permission.RECEIVE_WAP_PUSH'},
    {'group': '短信', 'name': '接收彩信', 'wechat_scope': None, 'android': 'android.permission.RECEIVE_MMS'},

    # 存储
    {'group': '存储', 'name': '读取 SD 卡', 'wechat_scope': None, 'android': 'android.permission.READ_EXTERNAL_STORAGE'},
    {'group': '存储', 'name': '写入 SD 卡', 'wechat_scope': None, 'android': 'android.permission.WRITE_EXTERNAL_STORAGE'},
    {'group': '存储', 'name': '读取照片位置信息', 'wechat_scope': None, 'android': 'android.permission.ACCESS_MEDIA_LOCATION'},

    # 身体活动
    {'group': '身体活动', 'name': '识别身体活动', 'wechat_scope': 'scope.werun', 'android': 'android.permission.ACTIVITY_RECOGNITION'},

    # 订购信息
    {'group': '订购信息', 'name': '订购信息', 'wechat_scope': None, 'android': None, 'note': '通过发票相关接口实现'},

    # 手机账户信息
    {'group': '手机账户信息', 'name': '手机账户信息', 'wechat_scope': None, 'android': 'android.permission.USE_CREDENTIALS'},

    # 网络权限
    {'group': '网络权限', 'name': '网络权限', 'wechat_scope': None, 'android': 'android.permission.INTERNET', 'note': '小程序默认支持'},

    # 系统
    {'group': '系统', 'name': '停用锁屏', 'wechat_scope': None, 'android': 'android.permission.DISABLE_KEYGUARD'},
    {'group': '系统', 'name': '修改图标', 'wechat_scope': None, 'android': 'android.permission.INSTALL_SHORTCUT'},
    {'group': '系统', 'name': '开机启动', 'wechat_scope': None, 'android': 'android.permission.RECEIVE_BOOT_COMPLETED'},
    {'group': '系统', 'name': '振动', 'wechat_scope': None, 'android': 'android.permission.VIBRATE', 'note': '通过 wx.vibrateShort 实现'},
]

# 误报说明文档
FALSE_POSITIVE_NOTES = """
## 误报原因说明

### 1. 相机和相册权限误报
**根本原因**: 微信小程序的相机和相册权限通过 wx.chooseImage() API 动态调用

**技术细节**:
- wx.chooseImage() 是微信提供的媒体选择 API
- 调用时会自动弹出系统选择框，用户可选择"拍照"或"从相册选择"
- 系统会自动处理权限请求，无需在 app.json 中声明
- 权限请求是运行时动态触发的，而不是静态配置

**检查工具的局限性**:
- 检查工具主要扫描 app.json 中的静态权限声明
- 无法完全识别运行时动态调用的 API
- 需要通过代码扫描来发现这些动态权限调用

### 2. 麦克风权限误报
**根本原因**: 麦克风权限通过 wx.startRecord() API 动态调用

**技术细节**:
- wx.startRecord() 是微信提供的录音 API
- 调用时会自动弹出系统权限请求框
- 无需在 app.json 中声明
- 权限请求是运行时动态触发的

**检查工具的局限性**:
- 同样无法识别运行时动态调用的录音 API
- 需要通过代码扫描来发现

### 3. 短信权限的误解
**误解**: 认为手机验证码登录需要"读取短信"权限

**实际情况**:
- 小程序使用微信官方的 getPhoneNumber 接口
- 用户点击"手机号一键登录"按钮后，微信弹出授权框
- 用户同意后，小程序通过加密方式获取手机号信息
- 验证码是用户手动输入的，不是自动读取
- 不需要任何短信相关权限
"""
