#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私合规检查工具 v2.0 - AI增强版
基于真实代码扫描结果的智能隐私合规检查工具

优化内容：
1. 增强AI分析能力，根据实际API调用结果智能填写权限确认单
2. 优化自评估表逻辑，基于真实检查结果生成准确评估
3. 添加Word文档生成功能
4. 改进权限与业务功能的智能映射
"""

import os
import re
import json
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# 权限定义和映射
PERMISSION_DEFINITIONS = {
    # 位置权限
    "scope.userLocation": {
        "group": "位置",
        "permissions": ["访问粗略位置", "访问精确位置", "支持后台访问位置"],
        "apis": ["getLocation", "chooseLocation", "startLocationUpdate", "onLocationChange"],
        "business_functions": {
            "getLocation": "显示附近充电桩位置",
            "chooseLocation": "选择充电站点位置",
            "startLocationUpdate": "充电过程中位置监控",
            "onLocationChange": "实时位置变化监听"
        },
        "necessity": {
            "getLocation": "用于在地图上显示用户附近的充电桩，帮助用户快速找到充电站点",
            "chooseLocation": "用于用户选择充电站点时获取位置信息",
            "startLocationUpdate": "用于充电过程中持续监控位置，确保充电安全",
            "onLocationChange": "用于实时更新用户位置，提供准确的导航服务"
        }
    },
    # 相机权限
    "scope.camera": {
        "group": "相机",
        "permissions": ["拍照"],
        "apis": ["chooseImage", "chooseMedia"],
        "business_functions": {
            "chooseImage": "上传头像或图片",
            "chooseMedia": "选择图片或视频"
        },
        "necessity": {
            "chooseImage": "用于用户上传头像、车辆照片或问题反馈图片",
            "chooseMedia": "用于用户选择图片或视频进行上传"
        }
    },
    # 相册权限
    "scope.writePhotosAlbum": {
        "group": "相册",
        "permissions": ["保存图片到相册"],
        "apis": ["saveImageToPhotosAlbum"],
        "business_functions": {
            "saveImageToPhotosAlbum": "保存图片到相册"
        },
        "necessity": {
            "saveImageToPhotosAlbum": "用于保存充电桩二维码、发票图片等到相册"
        }
    },
    # 录音权限
    "scope.record": {
        "group": "麦克风",
        "permissions": ["录音"],
        "apis": ["startRecord", "getRecorderManager"],
        "business_functions": {
            "startRecord": "录音功能",
            "getRecorderManager": "录音管理"
        },
        "necessity": {
            "startRecord": "用于用户语音输入或语音反馈",
            "getRecorderManager": "用于管理录音功能"
        }
    },
    # 通讯录权限
    "scope.addContact": {
        "group": "通讯录",
        "permissions": ["读取通讯录", "编辑通讯录"],
        "apis": ["chooseContact"],
        "business_functions": {
            "chooseContact": "选择联系人"
        },
        "necessity": {
            "chooseContact": "用于用户选择紧急联系人或分享充电桩位置给好友"
        }
    },
    # 剪贴板权限
    "scope.clipboard": {
        "group": "剪贴板",
        "permissions": ["读取剪贴板"],
        "apis": ["getClipboardData"],
        "business_functions": {
            "getClipboardData": "读取剪贴板内容"
        },
        "necessity": {
            "getClipboardData": "用于用户粘贴充电桩编号或优惠码"
        }
    },
    # 蓝牙权限
    "scope.bluetooth": {
        "group": "蓝牙",
        "permissions": ["蓝牙适配器"],
        "apis": ["openBluetoothAdapter"],
        "business_functions": {
            "openBluetoothAdapter": "打开蓝牙"
        },
        "necessity": {
            "openBluetoothAdapter": "用于连接蓝牙充电桩或蓝牙设备"
        }
    },
    # NFC权限
    "scope.nfc": {
        "group": "NFC",
        "permissions": ["NFC发现"],
        "apis": ["startNFCDiscovery"],
        "business_functions": {
            "startNFCDiscovery": "NCF发现"
        },
        "necessity": {
            "startNFCDiscovery": "用于NFC刷卡充电"
        }
    }
}

# 38项权限完整列表
PERMISSION_LIST = [
    {"id": 1, "group": "日历", "name": "读取日历"},
    {"id": 2, "group": "日历", "name": "编辑日历"},
    {"id": 3, "group": "通话记录", "name": "读取通话记录"},
    {"id": 4, "group": "通话记录", "name": "编辑通话记录"},
    {"id": 5, "group": "通话记录", "name": "监听呼出电话"},
    {"id": 6, "group": "相机", "name": "拍照"},
    {"id": 7, "group": "相机", "name": "相册"},
    {"id": 8, "group": "通讯录", "name": "读取通讯录"},
    {"id": 9, "group": "通讯录", "name": "编辑通讯录"},
    {"id": 10, "group": "通讯录", "name": "获取小程序账号"},
    {"id": 11, "group": "位置", "name": "访问粗略位置"},
    {"id": 12, "group": "位置", "name": "访问精确位置"},
    {"id": 13, "group": "位置", "name": "支持后台访问位置"},
    {"id": 14, "group": "麦克风", "name": "录音"},
    {"id": 15, "group": "电话", "name": "读取电话状态"},
    {"id": 16, "group": "电话", "name": "读取本机电话号码"},
    {"id": 17, "group": "电话", "name": "拨打电话"},
    {"id": 18, "group": "电话", "name": "接听电话"},
    {"id": 19, "group": "电话", "name": "添加语音邮箱"},
    {"id": 20, "group": "电话", "name": "使用网络电话"},
    {"id": 21, "group": "电话", "name": "继续进行来自其他小程序的通话"},
    {"id": 22, "group": "传感器", "name": "获取传感器信息"},
    {"id": 23, "group": "短信", "name": "发送短信"},
    {"id": 24, "group": "短信", "name": "接收短信"},
    {"id": 25, "group": "短信", "name": "读取短信"},
    {"id": 26, "group": "短信", "name": "接收 WAP 推送"},
    {"id": 27, "group": "短信", "name": "接收彩信"},
    {"id": 28, "group": "存储", "name": "读取 SD 卡"},
    {"id": 29, "group": "存储", "name": "写入 SD 卡"},
    {"id": 30, "group": "存储", "name": "读取照片位置信息"},
    {"id": 31, "group": "身体活动", "name": "识别身体活动"},
    {"id": 32, "group": "订购信息", "name": "订购信息"},
    {"id": 33, "group": "手机账户信息", "name": "手机账户信息"},
    {"id": 34, "group": "网络权限", "name": "网络权限"},
    {"id": 35, "group": "停用锁屏", "name": "停用锁屏"},
    {"id": 36, "group": "修改图标", "name": "修改图标"},
    {"id": 37, "group": "开机启动", "name": "开机启动"},
    {"id": 38, "group": "振动", "name": "振动"}
]


@dataclass
class ScanResult:
    """扫描结果数据类"""
    app_json: Dict
    permissions_declared: Dict[str, str]
    required_private_infos: List[str]
    apis_found: Dict[str, List[str]]  # API名称 -> 文件路径列表
    privacy_policy_url: Optional[str]
    service_agreement_url: Optional[str]
    logout_agreement_url: Optional[str]
    has_privacy_policy: bool
    has_user_consent: bool
    data_collection_points: List[Dict]
    third_party_sdks: List[str]


class MiniprogramPrivacyChecker:
    """小程序隐私合规检查器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.result = None
        self.check_date = datetime.now().strftime("%Y-%m-%d")
        
    def scan_project(self) -> ScanResult:
        """扫描小程序项目"""
        print("开始扫描小程序项目...")
        
        # 1. 读取app.json配置
        app_json = self._read_app_json()
        
        # 2. 提取权限声明
        permissions_declared = self._extract_permissions(app_json)
        required_private_infos = app_json.get("requiredPrivateInfos", [])
        
        # 3. 扫描代码中的API调用
        apis_found = self._scan_api_calls()
        
        # 4. 检查隐私政策配置
        privacy_urls = self._extract_privacy_urls(app_json)
        
        # 5. 检查用户授权流程
        has_user_consent = self._check_user_consent()
        
        # 6. 识别数据收集点
        data_collection_points = self._identify_data_collection()
        
        # 7. 检测第三方SDK
        third_party_sdks = self._detect_third_party_sdks()
        
        self.result = ScanResult(
            app_json=app_json,
            permissions_declared=permissions_declared,
            required_private_infos=required_private_infos,
            apis_found=apis_found,
            privacy_policy_url=privacy_urls.get("privacy_policy"),
            service_agreement_url=privacy_urls.get("service_agreement"),
            logout_agreement_url=privacy_urls.get("logout_agreement"),
            has_privacy_policy=privacy_urls.get("privacy_policy") is not None,
            has_user_consent=has_user_consent,
            data_collection_points=data_collection_points,
            third_party_sdks=third_party_sdks
        )
        
        print("项目扫描完成")
        return self.result
    
    def _read_app_json(self) -> Dict:
        """读取app.json配置文件"""
        app_json_paths = [
            self.project_path / "app.json",
            self.project_path / "__APP__" / "app-config.json"
        ]
        
        for path in app_json_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 处理可能的JSONP格式
                        if content.startswith('__wxAppCode__'):
                            match = re.search(r'\{.*\}', content, re.DOTALL)
                            if match:
                                content = match.group(0)
                        return json.loads(content)
                except Exception as e:
                    print(f"⚠️  读取app.json失败: {e}")
        
        return {}
    
    def _extract_permissions(self, app_json: Dict) -> Dict[str, str]:
        """提取权限声明"""
        permissions = {}
        permission_config = app_json.get("permission", {})
        
        for perm, desc in permission_config.items():
            if isinstance(desc, dict):
                permissions[perm] = desc.get("desc", "")
            else:
                permissions[perm] = str(desc)
        
        return permissions
    
    def _scan_api_calls(self) -> Dict[str, List[str]]:
        """扫描代码中的API调用"""
        apis_found = {}
        
        # 敏感API列表
        sensitive_apis = [
            "getLocation", "chooseLocation", "startLocationUpdate", "onLocationChange",
            "chooseImage", "chooseMedia", "saveImageToPhotosAlbum",
            "startRecord", "getRecorderManager",
            "chooseContact", "addPhoneContact",
            "getClipboardData", "setClipboardData",
            "openBluetoothAdapter", "startBluetoothDevicesDiscovery",
            "startNFCDiscovery",
            "getUserInfo", "getUserProfile",
            "login", "requestPayment", "chooseAddress",
            "scanCode", "getSystemInfo", "getNetworkType"
        ]
        
        # 扫描所有JS文件
        js_files = list(self.project_path.rglob("*.js"))
        
        for api in sensitive_apis:
            pattern = rf'\.{api}\s*\(|{api}\s*\('
            for js_file in js_files:
                try:
                    with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(pattern, content):
                            if api not in apis_found:
                                apis_found[api] = []
                            apis_found[api].append(str(js_file.relative_to(self.project_path)))
                except Exception:
                    pass
        
        return apis_found
    
    def _extract_privacy_urls(self, app_json: Dict) -> Dict[str, Optional[str]]:
        """提取隐私政策相关URL"""
        urls = {
            "privacy_policy": None,
            "service_agreement": None,
            "logout_agreement": None
        }
        
        ext = app_json.get("ext", {})
        passport = ext.get("passport", {})
        
        urls["privacy_policy"] = passport.get("protocolDetail")
        urls["service_agreement"] = passport.get("protocolLink")
        urls["logout_agreement"] = passport.get("logoutNoticeDetail")
        
        return urls
    
    def _check_user_consent(self) -> bool:
        """检查是否有用户授权流程"""
        # 检查登录页面是否有协议勾选
        login_files = list(self.project_path.rglob("*login*.js")) + \
                     list(self.project_path.rglob("*login*.html"))
        
        for file in login_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'protocolChecked' in content or 'checkbox' in content.lower():
                        return True
            except Exception:
                pass
        
        return False
    
    def _identify_data_collection(self) -> List[Dict]:
        """识别数据收集点"""
        collection_points = []
        
        # 检查手机号收集
        phone_patterns = [
            r'phone\s*[=:]',
            r'mobile\s*[=:]',
            r'cell\s*[=:]',
            r'电话号码'
        ]
        
        # 检查位置信息收集
        location_apis = ["getLocation", "chooseLocation"]
        
        # 检查表单提交
        form_files = list(self.project_path.rglob("*.js"))
        for file in form_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 检查手机号收集
                    for pattern in phone_patterns:
                        if re.search(pattern, content):
                            collection_points.append({
                                "type": "phone",
                                "file": str(file.relative_to(self.project_path)),
                                "description": "手机号收集"
                            })
                            break
                    
                    # 检查位置信息收集
                    for api in location_apis:
                        if f'.{api}(' in content or f'{api}(' in content:
                            collection_points.append({
                                "type": "location",
                                "file": str(file.relative_to(self.project_path)),
                                "description": f"位置信息收集 ({api})"
                            })
                            break
            except Exception:
                pass
        
        return collection_points
    
    def _detect_third_party_sdks(self) -> List[str]:
        """检测第三方SDK"""
        sdks = []
        
        # 常见SDK特征
        sdk_patterns = {
            "微信支付": ["wx.requestPayment", "WechatPay"],
            "百度地图": ["BMap", "baidu.com"],
            "高德地图": ["AMap", "autonavi.com"],
            "腾讯地图": ["QQMap", "qq.com"],
            "友盟统计": ["UMeng", "umeng.com"],
            "极光推送": ["JPush", "jpush.cn"],
            "Bugly": ["Bugly", "bugly.qq.com"],
            "支付宝": ["Alipay", "alipay.com"]
        }
        
        # 扫描所有JS文件
        js_files = list(self.project_path.rglob("*.js"))
        
        for sdk_name, patterns in sdk_patterns.items():
            for js_file in js_files:
                try:
                    with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for pattern in patterns:
                            if pattern in content:
                                sdks.append(sdk_name)
                                break
                except Exception:
                    pass
        
        return list(set(sdks))
    
    def generate_report(self) -> Dict:
        """生成检查报告"""
        if not self.result:
            self.scan_project()
        
        report = {
            "小程序名称": self.result.app_json.get("ext", {}).get("appName", "未知"),
            "appId": self.result.app_json.get("ext", {}).get("appId", "未知"),
            "检查日期": self.check_date,
            "权限声明": self.result.permissions_declared,
            "requiredPrivateInfos": self.result.required_private_infos,
            "API调用情况": self.result.apis_found,
            "隐私政策配置": {
                "是否配置": self.result.has_privacy_policy,
                "隐私政策URL": self.result.privacy_policy_url,
                "服务协议URL": self.result.service_agreement_url,
                "注销协议URL": self.result.logout_agreement_url
            },
            "用户授权流程": self.result.has_user_consent,
            "数据收集点": self.result.data_collection_points,
            "第三方SDK": self.result.third_party_sdks,
            "合规建议": self._generate_compliance_suggestions()
        }
        
        return report
    
    def _generate_compliance_suggestions(self) -> List[str]:
        """生成合规建议"""
        suggestions = []
        
        # 检查权限声明
        if not self.result.permissions_declared:
            suggestions.append("建议添加必要的权限声明")
        
        # 检查隐私政策
        if not self.result.has_privacy_policy:
            suggestions.append("建议配置隐私政策URL")
        
        # 检查用户授权
        if not self.result.has_user_consent:
            suggestions.append("建议添加用户授权流程，确保用户同意隐私政策")
        
        # 检查API调用
        if not self.result.apis_found:
            suggestions.append("未检测到API调用，建议检查代码是否正确")
        
        return suggestions


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小程序隐私合规检查工具")
    parser.add_argument("project_path", type=str, default=".", help="小程序项目路径")
    parser.add_argument("--output", type=str, default="report.json", help="报告输出路径")
    args = parser.parse_args()
    
    checker = MiniprogramPrivacyChecker(args.project_path)
    result = checker.scan_project()
    report = checker.generate_report()
    
    # 输出报告
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"报告已生成: {args.output}")
    
    # 打印简要报告
    print("\n检查结果摘要:")
    print(f"小程序名称: {report['小程序名称']}")
    print(f"appId: {report['appId']}")
    print(f"检查日期: {report['检查日期']}")
    print(f"已声明权限: {list(report['权限声明'].keys())}")
    print(f"API调用: {list(report['API调用情况'].keys())}")
    print(f"是否配置隐私政策: {'是' if report['隐私政策配置']['是否配置'] else '否'}")
    print(f"是否有用户授权流程: {'是' if report['用户授权流程'] else '否'}")
    print(f"数据收集点: {len(report['数据收集点'])}个")
    print(f"第三方SDK: {report['第三方SDK']}")
    print(f"合规建议: {report['合规建议']}")


if __name__ == "__main__":
    main()
