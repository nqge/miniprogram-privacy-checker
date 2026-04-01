#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序权限声明检查工具
基于：《网络安全标准实践指南-移动互联网应用程序（App）系统权限申请使用指南》
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import argparse


class PermissionChecker:
    """小程序权限声明检查器"""

    # 微信小程序敏感权限映射
    SENSITIVE_PERMISSIONS = {
        # 位置权限
        'scope.userLocation': {
            'name': '地理位置',
            'description': '获取地理位置信息',
            'category': '位置信息',
            'risk_level': 'high'
        },
        'scope.userLocationBackground': {
            'name': '后台定位',
            'description': '获取后台地理位置信息',
            'category': '位置信息',
            'risk_level': 'high'
        },

        # 相册权限
        'scope.writePhotosAlbum': {
            'name': '保存到相册',
            'description': '保存图片或视频到相册',
            'category': '存储',
            'risk_level': 'medium'
        },

        # 录音权限
        'scope.record': {
            'name': '录音',
            'description': '录制音频',
            'category': '麦克风',
            'risk_level': 'high'
        },

        # 蓝牙权限
        'scope.bluetooth': {
            'name': '蓝牙',
            'description': '搜索和连接蓝牙设备',
            'category': '蓝牙',
            'risk_level': 'medium'
        },

        # 剪贴板权限
        'scope.clipboard': {
            'name': '剪贴板',
            'description': '读取剪贴板内容',
            'category': '剪贴板',
            'risk_level': 'medium'
        },

        # 相机权限
        'scope.camera': {
            'name': '相机',
            'description': '拍摄照片或视频',
            'category': '相机',
            'risk_level': 'high'
        },

        # 麦克风权限
        'scope.microphone': {
            'name': '麦克风',
            'description': '录制音频',
            'category': '麦克风',
            'risk_level': 'high'
        },

        # 联系人权限
        'scope.addContact': {
            'name': '联系人',
            'description': '添加联系人',
            'category': '通讯录',
            'risk_level': 'high'
        },

        # NFC 权限
        'scope.nfc': {
            'name': 'NFC',
            'description': '近场通信',
            'category': 'NFC',
            'risk_level': 'medium'
        },

        # 运动步数权限
        'scope.werun': {
            'name': '微信运动',
            'description': '获取微信运动步数',
            'category': '健康',
            'risk_level': 'low'
        },

        # 通讯录权限（已废弃）
        'scope.addressBook': {
            'name': '通讯录',
            'description': '获取通讯录信息',
            'category': '通讯录',
            'risk_level': 'high',
            'deprecated': True
        }
    }

    # 常见的隐私 API 调用模式
    PRIVACY_API_PATTERNS = {
        'wx.getLocation': ['scope.userLocation', 'scope.userLocationBackground'],
        'wx.chooseLocation': ['scope.userLocation'],
        'wx.openLocation': ['scope.userLocation'],
        'wx.chooseImage': ['scope.camera'],
        'wx.chooseVideo': ['scope.camera'],
        'wx.chooseMedia': ['scope.camera'],
        'wx.getImageInfo': [],
        'wx.saveImageToPhotosAlbum': ['scope.writePhotosAlbum'],
        'wx.saveVideoToPhotosAlbum': ['scope.writePhotosAlbum'],
        'wx.startRecord': ['scope.record', 'scope.microphone'],
        'wx.getRecorderManager': ['scope.record', 'scope.microphone'],
        'wx.chooseContact': ['scope.addContact'],
        'wx.chooseMessageContact': ['scope.addContact'],
        'wx.getClipboardData': ['scope.clipboard'],
        'wx.setClipboardData': [],
        'wx.openBluetoothAdapter': ['scope.bluetooth'],
        'wx.startNFCDiscovery': ['scope.nfc'],
        'wx.getWeRunData': ['scope.werun'],
    }

    def __init__(self, miniprogram_path: str):
        """
        初始化权限检查器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.app_json_path = self.miniprogram_path / "app.json"
        self.js_files = []
        self.declared_permissions = {}
        self.detected_apis = {}
        self.missing_permissions = set()
        self.unused_permissions = set()
        self.issues = []

        # 加载 JS 文件
        self._load_js_files()

    def _load_js_files(self):
        """加载所有 JS 文件"""
        print(f"[*] 扫描 JS 文件...")
        for js_file in self.miniprogram_path.rglob("*.js"):
            self.js_files.append(js_file)
        print(f"[+] 发现 {len(self.js_files)} 个 JS 文件")

    def check(self) -> Dict:
        """
        执行权限检查

        Returns:
            检查结果字典
        """
        print("[*] 开始权限检查...")

        # 1. 检查 app.json 中的权限声明
        print("\n[1/4] 检查 app.json 权限声明...")
        self._check_app_json()

        # 2. 扫描 JS 文件中的敏感 API 调用
        print("\n[2/4] 扫描敏感 API 调用...")
        self._scan_apis()

        # 3. 对比权限声明和实际使用
        print("\n[3/4] 对比权限声明和实际使用...")
        self._compare_permissions()

        # 4. 检查权限描述合规性
        print("\n[4/4] 检查权限描述合规性...")
        self._check_permission_descriptions()

        # 5. 生成检查结果
        return self._generate_report()

    def _check_app_json(self):
        """检查 app.json 中的权限声明"""
        if not self.app_json_path.exists():
            self.issues.append({
                'type': 'critical',
                'message': f"未找到 app.json 文件: {self.app_json_path}",
                'suggestion': '请确保小程序根目录下有 app.json 配置文件'
            })
            return

        try:
            with open(self.app_json_path, 'r', encoding='utf-8') as f:
                app_config = json.load(f)

            # 检查 permission 字段
            if 'permission' in app_config:
                self.declared_permissions = app_config['permission']
                print(f"[+] 发现 {len(self.declared_permissions)} 个权限声明")
                for perm, desc in self.declared_permissions.items():
                    print(f"  - {perm}: {desc}")
            else:
                print("[-] 未发现 permission 字段")
                self.issues.append({
                    'type': 'warning',
                    'message': 'app.json 中未声明 permission 字段',
                    'suggestion': '如果小程序使用了敏感 API，请在 app.json 中声明权限'
                })

            # 检查 requiredPrivateInfos 字段（2023年后新规）
            if 'requiredPrivateInfos' in app_config:
                required_infos = app_config['requiredPrivateInfos']
                print(f"[+] 发现 {len(required_infos)} 个 requiredPrivateInfos")
                for info in required_infos:
                    print(f"  - {info}")
            else:
                print("[-] 未发现 requiredPrivateInfos 字段（2023年后建议使用）")

        except json.JSONDecodeError as e:
            self.issues.append({
                'type': 'critical',
                'message': f'app.json.json 格式错误: {e}',
                'suggestion': '请检查 app.json 的 JSON 格式是否正确'
            })
        except Exception as e:
            self.issues.append({
                'type': 'critical',
                'message': f'读取 app.json 失败: {e}',
                'suggestion': '请检查文件权限和格式'
            })

    def _scan_apis(self):
        """扫描 JS 文件中的敏感 API 调用"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查每个 API 模式
                for api_pattern, required_perms in self.PRIVACY_API_PATTERNS.items():
                    if api_pattern in content:
                        if api_pattern not in self.detected_apis:
                            self.detected_apis[api_pattern] = {
                                'files': [],
                                'required_permissions': required_perms
                            }
                        self.detected_apis[api_pattern]['files'].append(str(js_file))

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file_file}: {e}")

        print(f"[+] 发现 {len(self.detected_apis)} 个敏感 API 调用")
        for api, info in self.detected_apis.items():
            print(f"  - {api} ({len(info['files'])} 次调用)")
            if info['required_permissions']:
                print(f"    需要权限: {', '.join(info['required_permissions'])}")

    def _compare_permissions(self):
        """对比权限声明和实际使用"""
        # 收集所有需要的权限
        needed_permissions = set()
        for api, info in self.detected_apis.items():
            needed_permissions.update(info['required_permissions'])

        # 检查缺失的权限
        for perm in needed_permissions:
            if perm not in self.declared_permissions:
                self.missing_permissions.add(perm)
                self.issues.append({
                    'type': 'critical',
                    'message': f'检测到敏感 API 但未声明权限: {perm}',
                    'suggestion': f'请在 app.json 的 permission 字段中添加 {perm} 的声明'
                })

        # 检查未使用的权限
        for perm in self.declared_permissions:
            if perm not in needed_permissions and perm in self.SENSITIVE_PERMISSIONS:
                self.unused_permissions.add(perm)
                self.issues.append({
                    'type': 'info',
                    'message': f'声明了权限但未检测到使用: {perm}',
                    'suggestion': '如果确实不需要该权限，建议从声明中删除以遵循最小必要原则'
                })

    def _check_permission_descriptions(self):
        """检查权限描述合规性"""
        for perm, desc in self.declared_permissions.items():
            # 处理描述格式（可能是字符串或字典）
            desc_text = desc.get('desc', '') if isinstance(desc, dict) else desc

            # 检查描述是否为空
            if not desc_text or desc_text.strip() == '':
                self.issues.append({
                    'type': 'warning',
                    'message': f'权限 {perm} 的描述为空',
                    'suggestion': '请提供清晰易懂的权限使用说明'
                })
                continue

            # 检查描述是否过短
            if len(desc_text.strip()) < 10:
                self.issues.append({
                    'type': 'warning',
                    'message': f'权限 {perm} 的描述过短',
                    'suggestion': '描述应详细说明使用目的，建议不少于 10 个字符'
                })

            # 检查是否包含常见的模糊表述
            vague_terms = ['为了更好的用户体验', '为了提供更好的服务', '需要使用']
            for term in vague_terms:
                if term in desc_text:
                    self.issues.append({
                        'type': 'info',
                        'message': f'权限 {perm} 的描述包含模糊表述: "{term}"',
                        'suggestion': '请使用更具体、明确的表述，说明具体的业务目的'
                    })
                    break

    def _generate_report(self) -> Dict:
        """生成检查报告"""
        # 计算评分
        total_critical = len([i for i in self.issues if i['type'] == 'critical'])
        total_warning = len([i for i in self.issues if i['type'] == 'warning'])

        if total_critical == 0 and total_warning == 0:
            score = 100
        else:
            score = max(100 - (total_critical * 30) - (total_warning * 10), 0)

        return {
            'score': score,
            'declared_permissions': self.declared_permissions,
            'detected_apis': self.detected_apis,
            'missing_permissions': list(self.missing_permissions),
            'unused_permissions': list(self.unused_permissions),
            'issues': self.issues,
            'summary': {
                'total_declared': len(self.declared_permissions),
                'total_detected': len(self.detected_apis),
                'missing_count': len(self.missing_permissions),
                'unused_count': len(self.unused_permissions),
                'critical_issues': total_critical,
                'warning_issues': total_warning
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序权限声明检查报告")
    print("="*60)

    # 评分
    print(f"\n📊 合规评分: {report['score']}/100")
    if report['score'] >= 90:
        print("评级: ⭐⭐⭐⭐⭐ 优秀")
    elif report['score'] >= 70:
        print("评级: ⭐⭐⭐⭐ 艊好")
    elif report['score'] >= 50:
        print("评级: ⭐⭐⭐ 一般")
    elif report['score'] >= 30:
        print("评级: ⭐⭐ 较差")
    else:
        print("评级: ⭐ 极差")

    # 摘要
    summary = report['summary']
    print("\n📋 检查摘要:")
    print(f"  - 声明的权限数: {summary['total_declared']}")
    print(f"  - 检测到的敏感 API: {summary['total_detected']}")
    print(f"  - 缺失的权限声明: {summary['missing_count']}")
    print(f"  - 未使用的权限: {summary['unused_count']}")
    print(f"  - 严重问题: {summary['critical_issues']}")
    print(f"  - 警告问题: {summary['warning_issues']}")

    # 缺失的权限
    if report['missing_permissions']:
        print("\n❌ 缺失的权限声明（必须添加）:")
        for perm in report['missing_permissions']:
            perm_info = PermissionChecker.SENSITIVE_PERMISSIONS.get(perm, {})
            print(f"  - {perm}")
            if 'name' in perm_info:
                print(f"    名称: {perm_info['name']}")
            if 'description' in perm_info:
                print(f"    说明: {perm_info['description']}")

    # 未使用的权限
    if report['unused_permissions']:
        print("\n⚠️  未使用的权限声明（建议删除）:")
        for perm in report['unused_permissions']:
            perm_info = PermissionChecker.SENSITIVE_PERMISSIONS.get(perm, {})
            print(f"  - {perm}")
            if 'name' in perm_info:
                print(f"    名称: {perm_info['name']}")

    # 问题列表
    if report['issues']:
        print("\n🔍 问题详情:")
        for i, issue in enumerate(report['issues'], 1):
            type_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(issue['type'], '•')

            print(f"\n  {type_emoji} 问题 {i}: [{issue['type'].upper()}]")
            print(f"    描述: {issue['message']}")
            print(f"    建议: {issue['suggestion']}")

    # 检测到的 API
    if report['detected_apis']:
        print("\n🔎 检测到的敏感 API 调用:")
        for api, info in report['detected_apis'].items():
            print(f"\n  {api}:")
            print(f"    调用次数: {len(info['files'])}")
            print(f"    需要权限: {', '.join(info['required_permissions']) or '无需权限'}")
            print(f"    调用文件:")
            for file in info['files'][:3]:  # 只显示前 3 个
                print(f"      - {file}")
            if len(info['files']) > 3:
                print(f"      ... 还有 {len(info['files']) - 3} 个文件")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        with open(os.path.join(output_dir, 'permission_check.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/permission_check.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'permission_check_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序权限声明检查报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n")
            f.write(f"\n检查摘要:\n")
            f.write(f"  - 声明的权限数: {summary['total_declared']}\n")
            f.write(f"  - 检测到的敏感 API: {summary['total_detected']}\n")
            f.write(f"  - 缺失的权限声明: {summary['missing_count']}\n")
            f.write(f"  - 未使用的权限: {summary['unused_count']}\n\n")

            if report['missing_permissions']:
                f.write("缺失的权限声明:\n")
                for perm in report['missing_permissions']:
                    f.write(f"  - {perm}\n")
                f.write("\n")

            if report['unused_permissions']:
                f.write("未使用的权限声明:\n")
                for perm in report['unused_permissions']:
                    f.write(f"  - {perm}\n")
                f.write("\n")

            if report['issues']:
                f.write("问题列表:\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"\n{i}. [{issue['type'].upper()}] {issue['message']}\n")
                    f.write(f"   建议: {issue['suggestion']}\n")

        print(f"[+] 文本报告已保存: {output_dir}/permission_check_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序权限声明检查工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    checker = PermissionChecker(args.miniprogram_path)
    report = checker.check()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
