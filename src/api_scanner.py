#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序敏感 API 扫描工具
基于：《App违法违规收集使用个人信息行为认定方法》
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import argparse


class APIScanner:
    """小程序敏感 API 扫描器"""

    # 详细的敏感 API 定义
    SENSITIVE_APIS = {
        # ===== 位置相关 =====
        'wx.getLocation': {
            'category': '位置信息',
            'risk_level': 'high',
            'required_permission': ['scope.userLocation'],
            'description': '获取当前的地理位置、速度',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.userLocation'
        },
        'wx.chooseLocation': {
            'category': '位置信息',
            'risk_level': 'high',
            'required_permission': ['scope.userLocation'],
            'description': '打开地图选择位置',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.userLocation'
        },
        'wx.openLocation': {
            'category': '位置信息',
            'risk_level': 'medium',
            'required_permission': [],
            'description': '在微信内置地图中查看位置',
            'compliance_tips': '建议声明 scope.userLocation'
        },

        # ===== 相册相关 =====
        'wx.chooseImage': {
            'category': '相册',
            'risk_level': 'high',
            'required_permission': ['scope.camera'],
            'description': '从本地相册选择图片或使用相机拍照',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.camera'
        },
        'wx.chooseMedia': {
            'category': '相册',
            'risk_level': 'high',
            'required_permission': ['scope.camera'],
            'description': '拍摄或从手机相册中选择图片或视频',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.camera'
        },
        'wx.chooseVideo': {
            'category': '相册',
            'risk_level': 'high',
            'required_permission': ['scope.camera'],
            'description': '拍摄视频或从手机相册中选择视频',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.camera'
        },
        'wx.saveImageToPhotosAlbum': {
            'category': '相册',
            'risk_level': 'medium',
            'required_permission': ['scope.writePhotosAlbum'],
            'description': '保存图片到系统相册',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.writePhotosAlbum'
        },
        'wx.saveVideoToPhotosAlbum': {
            'category': '相册',
            'risk_level': 'medium',
            'required_permission': ['scope.writePhotosAlbum'],
            'description': '保存视频到系统相册',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.writePhotosAlbum'
        },

        # ===== 录音相关 =====
        'wx.startRecord': {
            'category': '录音',
            'risk_level': 'high',
            'required_permission': ['scope.record'],
            'description': '开始录音',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.record'
        },
        'wx.stopRecord': {
            'category': '录音',
            'risk_level': 'medium',
            'required_permission': ['scope.record'],
            'description': '停止录音',
            'compliance_tips': '必须在获得用户授权后调用'
        },
        'wx.getRecorderManager': {
            'category': '录音',
            'risk_level': 'high',
            'required_permission': ['scope.record'],
            'description': '获取全局唯一的录音管理器',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.record'
        },

        # ===== 蓝牙相关 =====
        'wx.openBluetoothAdapter': {
            'category': '蓝牙',
            'risk_level': 'medium',
            'required_permission': ['scope.bluetooth'],
            'description': '初始化蓝牙适配器',
            'compliance_tips': '必须在获得用户授权后后调用，并在 app.json 中声明 scope.bluetooth'
        },
        'wx.closeBluetoothAdapter': {
            'category': '蓝牙',
            'risk_level': 'low',
            'required_permission': ['scope.bluetooth'],
            'description': '关闭蓝牙适配器',
            'compliance_tips': '建议在获得用户授权后调用'
        },

        # ===== 剪贴板相关 =====
        'wx.getClipboardData': {
            'category': '剪贴板',
            'risk_level': 'medium',
            'required_permission': ['scope.clipboard'],
            'description': '读取系统剪贴板内容',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.clipboard'
        },
        'wx.setClipboardData': {
            'category': '剪贴板',
            'risk_level': 'low',
            'required_permission': [],
            'description': '设置系统剪贴板内容',
            'compliance_tips': '无需权限，但不应滥用'
        },

        # ===== NFC 相关 =====
        'wx.startNFCDiscovery': {
            'category': 'NFC',
            'risk_level': 'medium',
            'required_permission': ['scope.nfc'],
            'description': '开始监听 NFC 设备',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.nfc'
        },
        'wx.stopNFCDiscovery': {
            'category': 'NFC',
            'risk_level': 'low',
            'required_permission': ['scope.nfc'],
            'description': '停止监听 NFC 设备',
            'compliance_tips': '建议在获得用户授权后调用'
        },

        # ===== 联系人相关 =====
        'wx.chooseContact': {
            'category': '联系人',
            'risk_level': 'high',
            'required_permission': ['scope.addContact'],
            'description': '选择联系人',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.addContact'
        },
        'wx.chooseMessageContact': {
            'category': '联系人',
            'risk_level': 'high',
            'required_permission': ['scope.addContact'],
            'description': '选择联系人（来自消息会话）',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.addContact'
        },

        # ===== 微信运动相关 =====
        'wx.getWeRunData': {
            'category': '健康数据',
            'risk_level': 'low',
            'required_permission': ['scope.werun'],
            'description': '获取用户过去三十天的微信运动步数',
            'compliance_tips': '必须在获得用户授权后调用，并在 app.json 中声明 scope.werun'
        },

        # ===== 设备信息相关 =====
        'wx.getSystemInfo': {
            'category': '设备信息',
            'risk_level': 'low',
            'required_permission': [],
            'description': '获取系统信息',
            'compliance_tips': '无需权限，但不应收集过多设备信息'
        },
        'wx.getSystemInfoSync': {
            'category': '设备信息',
            'risk_level': 'low',
            'required_permission': [],
            'description': '获取系统信息（同步）',
            'compliance_tips': '无需权限，但不应收集过多设备信息'
        },
        'wx.getDeviceInfo': {
            'category': '设备信息',
            'risk_level': 'low',
            'required_permission': [],
            'description': '获取设备基础信息',
            'compliance_tips': '无需权限，但不应收集过多设备信息'
        },

        # ===== 网络相关 =====
        'wx.request': {
            'category': '网络请求',
            'risk_level': 'medium',
            'required_permission': [],
            'description': '发起 HTTPS 网络请求',
            'compliance_tips': '必须使用 HTTPS，不得使用 HTTP 传输敏感信息'
        },
        'wx.uploadFile': {
            'category': '网络请求',
            'risk_level': 'medium',
            'required_permission': [],
            'description': '上传本地资源到开发者服务器',
            'compliance_tips': '必须使用 HTTPS，不得传输敏感信息'
        },
        'wx.downloadFile': {
            'category': '网络请求',
            'risk_level': 'low',
            'required_permission': [],
            'description': '下载文件资源到本地',
            'compliance_tips': '必须使用 HTTPS'
        },

        # ===== 存储相关 =====
        'wx.setStorage': {
            'category': '本地存储',
            'risk_level': 'low',
            'required_permission': [],
            'description': '将数据存储在本地缓存中指定的 key 中',
            'compliance_tips': '不得在本地存储敏感信息'
        },
        'wx.setStorageSync': {
            'category': '本地存储',
            'risk_level': 'low',
            'required_permission': [],
            'description': '将数据存储在本地缓存中指定的 key 中（同步）',
            'compliance_tips': '不得在本地存储敏感信息'
        },
        'wx.getStorage': {
            'category': '本地存储',
            'risk_level': 'low',
            'required_permission': [],
            'description': '从本地缓存中异步获取指定 key 对应的内容',
            'compliance_tips': '无'
        },
        'wx.getStorageSync': {
            'category': '本地存储',
            'risk_level': 'low',
            'required_permission': [],
            'description': '从本地缓存中同步获取指定 key 对应的内容',
            'compliance_tips': '无'
        },

        # ===== 用户信息相关 =====
        'wx.getUserInfo': {
            'category': '用户信息',
            'risk_level': 'high',
            'required_permission': [],
            'description': '获取用户信息（已废弃）',
            'compliance_tips': '该 API 已废弃，请使用 wx.getUserProfile 代替',
            'deprecated': '该 API 已废弃，不再建议使用'
        },
        'wx.getUserProfile': {
            'category': '用户信息',
            'risk_level': 'high',
            'required_permission': [],
            'description': '获取用户信息',
            'compliance_tips': '必须在获得用户授权后调用，并遵循最小必要原则'
        },

        # ===== 登录相关 =====
        'wx.login': {
            'category': '登录认证',
            'risk_level': 'medium',
            'required_permission': [],
            'description': '调用微信登录',
            'compliance_tips': '建议在用户主动触发时调用'
        },

        # ===== 支付相关 =====
        'wx.requestPayment': {
            'category': '支付',
            'risk_level': 'high',
            'required_permission': [],
            'description': '发起微信支付',
            'compliance_tips': '必须在用户明确支付意愿后调用'
        },

        # ===== 分享相关 =====
        'wx.shareAppMessage': {
            'category': '分享',
            'risk_level': 'low',
            'required_permission': [],
            'description': '分享小程序给微信好友',
            'compliance_tips': '无'
        },
        'wx.shareTimeline': {
            'category': '分享',
            'risk_level': 'low',
            'required_permission': [],
            'description': '分享小程序到朋友圈',
            'compliance_tips': '无'
        },
    }

    def __init__(self, miniprogram_path: str):
        """
        初始化 API 扫描器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.js_files = []
        self.api_calls = defaultdict(list)  # API 调用记录
        self.issues = []

        # 加载 JS 文件
        self._load_js_files()

    def _load_js_files(self):
        """加载所有 JS 文件"""
        print(f"[*] 扫描 JS 文件...")
        for js_file in self.miniprogram_path.rglob("*.js"):
            self.js_files.append(js_file)
        print(f"[+] 发现 {len(self.js_files)} 个 JS 文件")

    def scan(self) -> Dict:
        """
        执行 API 扫描

        Returns:
            扫描结果字典
        """
        print("[*] 开始扫描敏感 API...")

        # 1. 扫描所有 JS 文件中的 API 调用
        print("\n[1/3] 扫描所有 JS 文件...")
        self._scan_js_files()

        # 2. 分析 API 调用模式
        print("\n[2/3] 分析 API 调用模式...")
        self._analyze_api_patterns()

        # 3. 检查合规性
        print("\n[3/3] 检查合规性...")
        self._check_compliance()

        # 4. 生成扫描结果
        return self._generate_report()

    def _scan_js_files(self):
        """扫描所有 JS 文件中的 API 调用"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查每个敏感 API
                for api_name in self.SENSITIVE_APIS.keys():
                    # 增强的模式匹配
                    # 匹配多种调用形式：
                    # 1. wx.apiName(...)
                    # 2. e.apiName(...) (压缩后的代码)
                    # 3. t.apiName(...)
                    # 4. n.apiName(...)
                    patterns = [
                        re.compile(r'\bwx\.' + re.escape(api_name[3:]) + r'\s*\('),  # wx.apiName
                        re.compile(r'[etn]\.' + re.escape(api_name[3:]) + r'\s*\('),  # e/t/n.apiName (压缩代码)
                        re.compile(re.escape(api_name) + r'\s*\('),  # apiName(...)
                    ]

                    for line_num, line in enumerate(lines, 1):
                        # 检查所有模式
                        matched = False
                        for pattern in patterns:
                            if pattern.search(line):
                                matched = True
                                break

                        if matched:
                            # 提取调用上下文
                            context_start = max(0, line_num - 2)
                            context_end = min(len(lines), line_num + 3)
                            context = lines[context_start:context_end]

                            self.api_calls[api_name].append({
                                'api': api_name,  # 记录标准的 API 名称
                                'file': str(js_file.relative_to(self.miniprogram_path)),
                                'line': line_num,
                                'code': line.strip(),
                                'context': '\n'.join(context)
                            })

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 发现 {len(self.api_calls)} 个敏感 API 调用")
        for api, calls in self.api_calls.items():
            print(f"  - {api}: {len(calls)} 次调用")

    def _analyze_api_patterns(self):
        """分析 API 调用模式"""
        # 分析是否有在 onLoad/onShow 等生命周期函数中自动调用敏感 API
        auto_trigger_apis = {
            'wx.getLocation',
            'wx.chooseLocation',
            'wx.getRecorderManager',
            'wx.getClipboardData',
        }

        for api_name, calls in self.api_calls.items():
            if api_name not in auto_trigger_apis:
                continue

            for call in calls:
                code = call['code'].lower()
                context = call['context'].lower()

                # 检查是否在生命周期函数中自动触发
                if any(lifecycle in context for lifecycle in [
                    'onload', 'onshow', 'onready', 'onlaunch'
                ]):
                    # 检查是否有用户交互触发（如点击事件）
                    if not any(trigger in context for trigger in [
                        'onclick', 'ontap', 'bindtap', 'catchtap',
                        'onsubmit', 'onsubmitting', 'click', 'tap'
                    ]):
                        self.issues.append({
                            'type': 'warning',
                            'api': api_name,
                            'file': call['file'],
                            'line': call['line'],
                            'message': f'检测到 {api_name} 可能在生命周期函数中自动触发',
                            'suggestion': f'{api_name} 应该在用户主动触发（如点击按钮）后调用，而不是在页面加载时自动调用',
                            'code_snippet': call['code']
                        })

    def _check_compliance(self):
        """检查合规性"""
        # 检查已废弃的 API
        for api_name, calls in self.api_calls.items():
            api_info = self.SENSITIVE_APIS.get(api_name, {})

            # 检查废弃 API
            if api_info.get('deprecated'):
                for call in calls:
                    self.issues.append({
                        'type': 'critical',
                        'api': api_name,
                        'file': call['file'],
                        'line': call['line'],
                        'message': f'使用已废弃的 API: {api_name}',
                        'suggestion': api_info['deprecated'],
                        'code_snippet': call['code']
                    })

            # 检查高风险 API
            if api_info.get('risk_level') == 'high':
                api_info_text = api_info.get('description', '')
                for call in calls:
                    # 检查是否有授权检查
                    context = call['context'].lower()

                    # 检查是否有授权相关代码
                    has_auth_check = any(keyword in context for keyword in [
                        'authsetting', 'getsetting', 'authorize', 'scope',
                        '用户授权', '用户同意', '用户拒绝'
                    ])

                    if not has_auth_check:
                        self.issues.append({
                            'type': 'warning',
                            'api': api_name,
                            'file': call['file'],
                            'line': call['line'],
                            'message': f'高风险 API {api_name} 调用可能未进行授权检查',
                            'suggestion': f'建议在调用 {api_name} 前检查用户授权状态，使用 wx.getSetting() 检查授权',
                            'code_snippet': call['code']
                        })

        # 检查 wx.request 是否使用 HTTPS
        for api_name, calls in self.api_calls.items():
            if api_name == 'wx.request':
                for call in calls:
                    context = call['context']
                    # 检查是否有 http:// (不安全)
                    if 'http://' in context and 'https://' not in context:
                        self.issues.append({
                            'type': 'critical',
                            'api': api_name,
                            'file': call['file'],
                            'line': call['line'],
                            'message': '检测到使用 HTTP 协议发起网络请求',
                            'suggestion': '必须使用 HTTPS 协议，HTTP 协议存在中间人攻击风险，且不符合隐私合规要求',
                            'code_snippet': call['code']
                        })

    def _generate_report(self) -> Dict:
        """生成扫描报告"""
        # 统计各风险等级的 API 调用
        risk_stats = defaultdict(int)
        for api_name in self.api_calls.keys():
            api_info = self.SENSITIVE_APIS.get(api_name, {})
            risk_level = api_info.get('risk_level', 'low')
            risk_stats[risk_level] += 1

        # 统计问题类型
        issue_stats = defaultdict(int)
        for issue in self.issues:
            issue_stats[issue['type']] += 1

        # 计算评分
        total_calls = sum(len(calls) for calls in self.api_calls.values())
        critical_issues = issue_stats.get('critical', 0)
        warning_issues = issue_stats.get('warning', 0)

        if critical_issues == 0:
            score = max(100 - (warning_issues * 10), 0)
        else:
            score = max(100 - (critical_issues * 30) - (warning_issues * 10), 0)

        return {
            'score': score,
            'total_api_calls': total_calls,
            'api_calls': dict(self.api_calls),
            'issues': self.issues,
            'risk_stats': dict(risk_stats),
            'issue_stats': dict(issue_stats),
            'sensitive_apis_count': len(self.api_calls)
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序敏感 API 扫描报告")
    print("="*60)

    # 评分
    print(f"\n📊 合规评分: {report['score']}/100")
    if report['score'] >= 90:
        print("评级: ⭐⭐⭐⭐⭐ 优秀")
    elif report['score'] >= 70:
        print("评级: ⭐⭐⭐⭐ 良好")
    elif report['score'] >= 50:
        print("评级: ⭐⭐⭐ 一般")
    elif report['score'] >= 30:
        print("评级: ⭐⭐ 较差")
    else:
        print("评级: ⭐ 极差")

    # 摘要
    print("\n📋 扫描摘要:")
    print(f"  - 检测到的敏感 API 种类: {report['sensitive_apis_count']}")
    print(f"  - 敏感 API 调用总次数: {report['total_api_calls']}")
    print(f"  - 高风险 API: {report['risk_stats'].get('high', 0)} 种")
    print(f"  - 中风险 API: {report['risk_stats'].get('medium', 0)} 种")
    print(f"  - 低风险 API: {report['risk_stats'].get('low', 0)} 种")
    print(f"  - 严重问题: {report['issue_stats'].get('critical', 0)}")
    print(f"  - 警告问题: {report['issue_stats'].get('warning', 0)}")

    # 按 API 类别分组
    category_apis = {}
    for api_name, calls in report['api_calls'].items():
        api_info = APIScanner.SENSITIVE_APIS.get(api_name, {})
        category = api_info.get('category', '其他')
        if category not in category_apis:
            category_apis[category] = []
        category_apis[category].append((api_name, calls, api_info))

    print(f"\n🔍 敏感 API 调用详情（按类别）:")
    for category in sorted(category_apis.keys()):
        print(f"\n  【{category}】")
        for api_name, calls, api_info in sorted(category_apis[category]):
            risk_level = api_info.get('risk_level', 'low')
            risk_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk_level, '⚪')

            print(f"    {risk_emoji} {api_name}: {len(calls)} 次调用")
            print(f"       风险等级: {risk_level.upper()}")

            # 显示调用位置
            print(f"       调用位置:")
            for call in calls[:3]:  # 只显示前 3 个
                print(f"         - {call['file']}:{call['line']}")
            if len(calls) > 3:
                print(f"         ... 还有 {len(calls) - 3} 处调用")

            # 显示合规提示
            if api_info.get('compliance_tips'):
                print(f"       合规提示: {api_info['compliance_tips']}")

    # 问题列表
    if report['issues']:
        print(f"\n🚨 合规问题 ({len(report['issues'])} 个):")
        for i, issue in enumerate(report['issues'], 1):
            type_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(issue['type'], '•')

            print(f"\n  {type_emoji} 问题 {i}: [{issue['type'].upper()}]")
            print(f"     API: {issue.get('api', 'N/A')}")
            print(f"     文件: {issue['file']}:{issue.get('line', '?')}")
            print(f"     描述: {issue['message']}")
            print(f"     建议: {issue['suggestion']}")
            if issue.get('code_snippet'):
                print(f"     代码: {issue['code_snippet']}")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        with open(os.path.join(output_dir, 'api_scan.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/api_scan.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'api_scan_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序敏感 API 扫描报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"扫描摘要:\n")
            f.write(f"  - 检测到的敏感 API 种类: {report['sensitive_apis_count']}\n")
            f.write(f"  - 敏感 API 调用总次数: {report['total_api_calls']}\n\n")

            if report['issues']:
                f.write(f"合规问题 ({len(report['issues'])} 个):\n\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"{i}. [{issue['type'].upper()}] {issue['message']}\n")
                    f.write(f"   文件: {issue['file']}:{issue.get('line', '?')}\n")
                    f.write(f"   建议: {issue['suggestion']}\n\n")

        print(f"[+] 文本报告已保存: {output_dir}/api_scan_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序敏感 API 扫描工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    scanner = APIScanner(args.miniprogram_path)
    report = scanner.scan()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
