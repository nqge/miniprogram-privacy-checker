#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序申请权限确认单生成工具（增强版）
基于：微信小程序权限申请规范和完整38项权限列表
更新：支持动态权限检测（相机、相册、麦克风等）
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
import argparse

# 导入新的权限定义
import sys
sys.path.insert(0, str(Path(__file__).parent))
from permission_definitions import FULL_PERMISSION_LIST, WECHAT_PERMISSIONS


class EnhancedPermissionConfirmationTool:
    """增强版小程序权限确认单生成工具"""

    # 完整的38项权限列表
    PERMISSION_GROUPS = FULL_PERMISSION_LIST

    def __init__(self, miniprogram_path: str):
        """
        初始化权限确认单生成工具

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.permission_usage = {}  # 权限使用情况
        self.app_config = {}
        self.declared_permissions = set()  # 在 app.json 中声明的权限
        self.dynamic_permissions = set()  # 通过代码检测到的动态权限
        self.api_calls = {}  # API 调用记录

    def analyze(self) -> Dict:
        """分析权限使用情况"""
        print(f"[*] 开始分析小程序权限使用情况...")
        print(f"[*] 目标路径: {self.miniprogram_path}")
        print("")

        # 读取 app.json
        app_json = self.miniprogram_path / 'app.json'
        if app_json.exists():
            try:
                with open(app_json, 'r', encoding='utf-8') as f:
                    self.app_config = json.load(f)
                print(f"[+] 找到 app.json 配置文件")

                # 提取声明的权限
                permission_field = self.app_config.get('permission', {})
                if permission_field:
                    self.declared_permissions = set(permission_field.keys())
                    print(f"[+] 声明的权限: {len(self.declared_permissions)} 项")
                    for perm in sorted(self.declared_permissions):
                        print(f"  - {perm}")
            except Exception as e:
                print(f"[-] 读取 app.json 失败: {e}")

        # 扫描代码中的 API 调用
        print("\n[*] 扫描代码中的 API 调用...")
        self._scan_api_calls()

        # 检测动态权限（相机、相册、麦克风等）
        print("\n[*] 检测动态权限调用...")
        self._detect_dynamic_permissions()

        # 生成确认单
        return self._generate_confirmation()

    def _scan_api_calls(self):
        """扫描代码中的 API 调用"""
        for js_file in self.miniprogram_path.rglob("*.js"):
            try:
                with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 扫描所有微信 API
                for api_name in self._get_all_wechat_apis():
                    # 多种模式匹配
                    patterns = [
                        rf'\bwx\.{re.escape(api_name)}\s*\(',
                        rf'[etn]\.{re.escape(api_name)}\s*\(',  # 压缩代码
                    ]

                    for pattern in patterns:
                        regex = re.compile(pattern)
                        for line_num, line in enumerate(lines, 1):
                            if regex.search(line):
                                if api_name not in self.api_calls:
                                    self.api_calls[api_name] = []

                                self.api_calls[api_name].append({
                                    'file': str(js_file.relative_to(self.miniprogram_path)),
                                    'line': line_num,
                                    'code': line.strip()
                                })
                                break  # 避免重复记录同一行

            except Exception as e:
                print(f"[-] 扫描文件失败 {js_file}: {e}")

        print(f"[+] 检测到 API 调用: {len(self.api_calls)} 种")

    def _get_all_wechat_apis(self) -> Set[str]:
        """获取所有需要检测的微信 API"""
        apis = set()

        # 从权限定义中提取
        for perm in self.PERMISSION_GROUPS:
            api = perm.get('api')
            if api and api.startswith('wx.'):
                apis.add(api)

        # 从 WECHAT_PERMISSIONS 中提取
        for scope, info in WECHAT_PERMISSIONS.items():
            for api in info.get('api', []):
                apis.add(api)

        return apis

    def _detect_dynamic_permissions(self):
        """
        检测动态权限调用

        动态权限是指通过 API 动态调用，不需要在 app.json 中声明的权限：
        - 相机权限: wx.chooseImage, wx.chooseMedia
        - 相册权限: wx.saveImageToPhotosAlbum, wx.saveVideoToPhotosAlbum
        - 麦克风权限: wx.startRecord, wx.getRecorderManager
        - 位置权限: wx.getLocation, wx.chooseLocation
        """
        # API 到权限的映射
        api_to_permission = {
            'wx.chooseImage': 'scope.camera',
            'wx.chooseMedia': 'scope.camera',
            'wx.createCameraContext': 'scope.camera',
            'wx.saveImageToPhotosAlbum': 'scope.writePhotosAlbum',
            'wx.saveVideoToPhotosAlbum': 'scope.writePhotosAlbum',
            'wx.startRecord': 'scope.record',
            'wx.getRecorderManager': 'scope.record',
            'wx.getLocation': 'scope.userLocation',
            'wx.chooseLocation': 'scope.userLocation',
            'wx.openLocation': 'scope.userLocation',
            'wx.startLocationUpdate': 'scope.userLocationBackground',
            'wx.onLocationChange': 'scope.userLocationBackground',
            'wx.chooseContact': 'scope.addContact',
            'wx.openBluetoothAdapter': 'scope.bluetooth',
            'wx.startBluetoothDevicesDiscovery': 'scope.bluetooth',
            'wx.getClipboardData': 'scope.clipboard',
            'wx.startNFCDiscovery': 'scope.nfc',
            'wx.getWeRunData': 'scope.werun',
            'wx.chooseAddress': 'scope.address',
            'wx.chooseInvoiceTitle': 'scope.invoiceTitle',
            'wx.chooseInvoice': 'scope.invoice',
        }

        # 检测调用的 API 对应的权限
        for api_name, calls in self.api_calls.items():
            if api_name in api_to_permission:
                permission = api_to_permission[api_name]
                self.dynamic_permissions.add(permission)

        print(f"[+] 检测到动态权限: {len(self.dynamic_permissions)} 项")
        for perm in sorted(self.dynamic_permissions):
            print(f"  - {perm}")

    def _generate_confirmation(self) -> Dict:
        """生成权限确认单"""
        # 基本信息
        basic_info = {
            'app_name': self.app_config.get('appName', '未知'),
            'app_version': self.app_config.get('version', '1.0.0'),
            'company': self.app_config.get('company', '待填写'),
            'contact': self.app_config.get('contact', '待填写'),
        }

        # 权限列表
        permissions = []

        for idx, perm_def in enumerate(self.PERMISSION_GROUPS, 1):
            perm_name = perm_def['name']
            group = perm_def['group']
            wechat_scope = perm_def.get('wechat_scope')
            note = perm_def.get('note', '')

            # 判断是否使用了该权限
            is_used = False
            usage_count = 0
            files = []

            # 检查是否在声明的权限中
            declared = wechat_scope in self.declared_permissions if wechat_scope else False

            # 检查是否在动态权限中
            dynamic = wechat_scope in self.dynamic_permissions if wechat_scope else False

            # 检查是否有 API 调用
            api = perm_def.get('api')
            if api and api in self.api_calls:
                is_used = True
                usage_count = len(self.api_calls[api])
                files = self.api_calls[api][:10]  # 最多显示10个

            # 如果是动态权限，也算作已使用
            if dynamic and not is_used:
                is_used = True
                # 查找相关的 API 调用
                for api_name, calls in self.api_calls.items():
                    if api_name.startswith(api.split('(')[0] if '(' in api else api):
                        usage_count = len(calls)
                        files = calls[:10]
                        break

            permissions.append({
                'id': idx,
                'group': group,
                'name': perm_name,
                'is_applied': '是' if is_used else '否',
                'business_function': self._get_business_function(perm_name),
                'necessity': self._get_necessity(perm_name, note),
                'usage_count': usage_count,
                'files': files,
                'declared': declared,
                'dynamic': dynamic,
                'note': note
            })

        # 统计
        total_permissions = len(permissions)
        used_permissions = len([p for p in permissions if p['is_applied'] == '是'])

        summary = {
            'total_permissions': total_permissions,
            'used_permissions': used_permissions,
            'unused_permissions': total_permissions - used_permissions,
        }

        return {
            'basic_info': basic_info,
            'summary': summary,
            'permissions': permissions,
            'declared_permissions': list(self.declared_permissions),
            'dynamic_permissions': list(self.dynamic_permissions),
        }

    def _get_business_function(self, perm_name: str) -> str:
        """获取权限对应的业务功能"""
        business_functions = {
            '读取日历': '日历事件管理',
            '编辑日历': '添加日历事件',
            '读取通话记录': '通话记录查询',
            '编辑通话记录': '通话记录管理',
            '监听呼出电话': '电话监听',
            '拍照': '用户头像设置、问题反馈、扫码付款',
            '相册': '保存图片、上传图片',
            '读取通讯录': '邀请好友、添加联系人',
            '编辑通讯录': '添加联系人',
            '获取小程序账号': '登录授权',
            '访问粗略位置': '位置服务、附近门店',
            '访问精确位置': '导航服务、地图展示',
            '支持后台访问位置': '持续定位服务',
            '录音': '语音输入、语音消息',
            '读取电话状态': '通话状态检测',
            '读取本机电话号码': '手机号快速登录',
            '拨打电话': '客服电话',
            '接听电话': '电话接听',
            '添加语音邮箱': '语音邮件',
            '使用网络电话': '网络通话',
            '继续进行来自其他小程序的通话': '通话连续性',
            '获取传感器信息': '设备姿态检测',
            '发送短信': '短信验证',
            '接收短信': '短信接收',
            '读取短信': '验证码自动读取（不支持）',
            '接收 WAP 推送': 'WAP 消息',
            '接收彩信': '彩信接收',
            '读取 SD 卡': '文件读取',
            '写入 SD 卡': '文件保存',
            '读取照片位置信息': '照片地理信息',
            '识别身体活动': '运动步数统计',
            '订购信息': '订单管理',
            '手机账户信息': '账户管理',
            '网络权限': '网络通信',
            '停用锁屏': '锁屏控制',
            '修改图标': '桌面快捷方式',
            '开机启动': '自启动',
            '振动': '触觉反馈',
        }
        return business_functions.get(perm_name, '其他功能')

    def _get_necessity(self, perm_name: str, note: str = '') -> str:
        """获取权限必要性说明"""
        if note:
            return note

        necessity = {
            '拍照': '用户主动触发时使用，用于头像设置等功能',
            '相册': '用户主动触发时使用，用于保存图片',
            '录音': '用户主动触发时使用，用于语音输入',
            '读取本机电话号码': '通过微信授权获取，不读取短信',
            '访问精确位置': '用户授权后使用，用于位置服务',
            '识别身体活动': '用户授权后使用，获取运动数据',
        }
        return necessity.get(perm_name, '根据业务需要使用')

    def generate_table(self, output_dir: str = None) -> str:
        """生成权限确认单表格"""
        confirmation_data = self.analyze()

        lines = []
        lines.append("=" * 120)
        lines.append("                        小程序申请权限确认单（增强版）")
        lines.append("=" * 120)
        lines.append("")
        lines.append(f"小程序名称: {confirmation_data['basic_info']['app_name']}")
        lines.append(f"小程序版本: {confirmation_data['basic_info']['app_version']}")
        lines.append(f"开发运营责任单位: {confirmation_data['basic_info']['company']}")
        lines.append(f"责任人: {confirmation_data['basic_info']['contact']}")
        lines.append("")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("=" * 120)
        lines.append("")
        lines.append("权限汇总:")
        lines.append(f"  • 总权限数: {confirmation_data['summary']['total_permissions']}")
        lines.append(f"  • 已使用: {confirmation_data['summary']['used_permissions']}")
        lines.append(f"  • 未使用: {confirmation_data['summary']['unused_permissions']}")
        lines.append(f"  • 动态权限（通过API调用）: {len(confirmation_data['dynamic_permissions'])}")
        lines.append("")
        lines.append("=" * 120)
        lines.append("")
        lines.append("序号 | 权限组 | 敏感权限名称 | 小程序是否申请 | 对应业务功能 | 必要性说明")
        lines.append("-" * 120)

        for perm in confirmation_data['permissions']:
            is_applied = perm['is_applied']
            status_mark = "✅" if is_applied == "是" else "❌"

            # 如果是动态权限，添加标记
            applied_text = is_applied
            if perm.get('dynamic'):
                applied_text = f"{is_applied} (动态)"

            lines.append(
                f"{perm['id']:3d} | "
                f"{perm['group']:8s} | "
                f"{perm['name']:20s} | "
                f"{status_mark} {applied_text:15s} | "
                f"{perm['business_function']:30s} | "
                f"{perm['necessity']:40s}"
            )

        lines.append("")
        lines.append("=" * 120)
        lines.append("")
        lines.append("权限使用详情:")
        lines.append("")

        # 列出已使用的权限及其调用位置
        for perm in confirmation_data['permissions']:
            if perm['is_applied'] == '是':
                lines.append(f"\n【{perm['group']}】{perm['name']} (调用 {perm['usage_count']} 次)")
                if perm.get('note'):
                    lines.append(f"  说明: {perm['note']}")
                for file_info in perm['files'][:5]:  # 只显示前5个调用位置
                    lines.append(f"  • {file_info['file']}:{file_info['line']}")
                if len(perm['files']) > 5:
                    lines.append(f"  ... 还有 {len(perm['files']) - 5} 处调用")

        lines.append("")
        lines.append("=" * 120)
        lines.append("")
        lines.append("动态权限说明:")
        lines.append("")
        lines.append("以下权限通过 API 动态调用，系统会自动处理权限请求，无需在 app.json 中声明：")
        lines.append("  • 相机权限: wx.chooseImage, wx.chooseMedia")
        lines.append("  • 相册权限: wx.saveImageToPhotosAlbum, wx.saveVideoToPhotosAlbum")
        lines.append("  • 麦克风权限: wx.startRecord, wx.getRecorderManager")
        lines.append("  • 位置权限: wx.getLocation, wx.chooseLocation")
        lines.append("")
        lines.append("这些权限在运行时动态触发，调用时会弹出系统权限请求框，用户确认后才能使用。")
        lines.append("")
        lines.append("=" * 120)

        table_content = '\n'.join(lines)

        # 保存到文件
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            table_file = os.path.join(output_dir, '权限确认单_增强版.txt')
            with open(table_file, 'w', encoding='utf-8') as f:
                f.write(table_content)
            print(f"\n[+] 权限确认单已保存: {table_file}")

            # 保存 JSON 格式
            json_file = os.path.join(output_dir, 'permission_confirmation_enhanced.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(confirmation_data, f, ensure_ascii=False, indent=2)
            print(f"[+] JSON 报告已保存: {json_file}")

        return table_content


def main():
    parser = argparse.ArgumentParser(description='小程序申请权限确认单生成工具（增强版）')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    tool = EnhancedPermissionConfirmationTool(args.miniprogram_path)
    table = tool.generate_table(args.output)

    print("\n" + table)


if __name__ == '__main__':
    main()
