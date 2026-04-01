#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序申请权限确认单生成工具
基于：微信小程序权限申请规范
"""

import os
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import argparse


class PermissionConfirmationTool:
    """小程序权限确认单生成工具"""

    # 微信小程序完整权限列表（38项）
    PERMISSION_GROUPS = {
        '日历': {
            'permissions': [
                {'id': 1, 'name': '读取日历', 'api': 'wx.getCalendar'},
                {'id': 2, 'name': '编辑日历', 'api': 'wx.addCalendar'},
            ],
            'description': '访问和修改用户日历数据'
        },
        '通话记录': {
            'permissions': [
                {'id': 3, 'name': '读取通话记录', 'api': 'read_call_log'},
                {'id': 4, 'name': '编辑通话记录', 'api': 'write_call_log'},
                {'id': 5, 'name': '监听呼出电话', 'api': 'process_outgoing_calls'},
            ],
            'description': '访问和修改用户通话记录'
        },
        '相机': {
            'permissions': [
                {'id': 6, 'name': '拍照', 'api': 'wx.createCamera'},
            ],
            'description': '访问摄像头拍照'
        },
        '通讯录': {
            'permissions': [
                {'id': 7, 'name': '读取通讯录', 'api': 'wx.chooseContact'},
                {'id': 8, 'name': '编辑通讯录', 'api': 'wx.addContact'},
                {'id': 9, 'name': '获取小程序账号', 'api': 'wx.getAccountInfoSync'},
            ],
            'description': '访问和修改用户通讯录'
        },
        '位置': {
            'permissions': [
                {'id': 10, 'name': '访问粗略位置', 'api': 'wx.getLocation(type=wgs84)'},
                {'id': 11, 'name': '访问精确位置', 'api': 'wx.getLocation(type=gcj02)'},
                {'id': 12, 'name': '支持后台访问位置', 'api': 'wx.onLocationChange'},
            ],
            'description': '获取用户地理位置信息'
        },
        '麦克风': {
            'permissions': [
                {'id': 13, 'name': '录音', 'api': 'wx.startRecord'},
            ],
            'description': '访问麦克风录音'
        },
        '电话': {
            'permissions': [
                {'id': 14, 'name': '读取电话状态', 'api': 'read_phone_state'},
                {'id': 15, 'name': '读取本机电话号码', 'api': 'get_phone_number'},
                {'id': 16, 'name': '拨打电话', 'api': 'wx.makePhoneCall'},
                {'id': 17, 'name': '接听电话', 'api': 'answer_phone_call'},
                {'id': 18, 'name': '添加语音邮箱', 'api': 'add_voicemail'},
                {'id': 19, 'name': '使用网络电话', 'api': 'use_sip'},
                {'id': 20, 'name': '继续进行来自其他小程序的通话', 'api': 'continue_phone_call'},
            ],
            'description': '访问电话功能'
        },
        '传感器': {
            'permissions': [
                {'id': 21, 'name': '获取传感器信息', 'api': 'wx.onAccelerometerChange'},
            ],
            'description': '访问设备传感器'
        },
        '短信': {
            'permissions': [
                {'id': 22, 'name': '发送短信', 'api': 'send_sms'},
                {'id': 23, 'name': '接收短信', 'api': 'receive_sms'},
                {'id': 24, 'name': '读取短信', 'api': 'read_sms'},
                {'id': 25, 'name': '接收WAP推送', 'api': 'receive_wap_push'},
                {'id': 26, 'name': '接收彩信', 'api': 'receive_mms'},
            ],
            'description': '发送和接收短信'
        },
        '存储': {
            'permissions': [
                {'id': 27, 'name': '读取SD卡', 'api': 'wx.getFileSystemManager.read'},
                {'id': 28, 'name': '写入SD卡', 'api': 'wx.getFileSystemManager.write'},
                {'id': 29, 'name': '读取照片位置信息', 'api': 'getImageInfo'},
            ],
            'description': '读写设备存储'
        },
        '身体活动': {
            'permissions': [
                {'id': 30, 'name': '识别身体活动', 'api': 'wx.onAccelerometerChange'},
            ],
            'description': '识别用户身体活动'
        },
        '照片': {
            'permissions': [
                {'id': 31, 'name': '读取照片', 'api': 'wx.chooseImage'},
            ],
            'description': '访问用户照片'
        },
        '订购信息': {
            'permissions': [
                {'id': 32, 'name': '订购信息', 'api': 'get_order_info'},
            ],
            'description': '获取用户订购信息'
        },
        '手机账户信息': {
            'permissions': [
                {'id': 33, 'name': '手机账户信息', 'api': 'get_account_info'},
            ],
            'description': '获取手机账户信息'
        },
        '网络权限': {
            'permissions': [
                {'id': 34, 'name': '网络权限', 'api': 'wx.request'},
            ],
            'description': '网络访问权限'
        },
        '系统设置': {
            'permissions': [
                {'id': 35, 'name': '停用锁屏', 'api': 'disable_keyguard'},
                {'id': 36, 'name': '修改图标', 'api': 'modify_icon'},
                {'id': 37, 'name': '开机启动', 'api': 'boot_startup'},
                {'id': 38, 'name': '振动', 'api': 'wx.vibrateShort'},
            ],
            'description': '修改系统设置'
        },
    }

    def __init__(self, miniprogram_path: str):
        """初始化权限确认单工具"""
        self.miniprogram_path = Path(miniprogram_path)
        self.permission_usage = {}
        self.app_config = {}

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
            except Exception as e:
                print(f"[-] 读取 app.json 失败: {e}")

        # 扫描代码中的权限调用
        print("\n[*] 扫描代码中的权限调用...")
        self._scan_permissions()

        # 生成确认单
        return self._generate_confirmation()

    def _scan_permissions(self):
        """扫描代码中的权限调用"""
        for js_file in self.miniprogram_path.rglob("*.js"):
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                for group_name, group_info in self.PERMISSION_GROUPS.items():
                    for perm in group_info['permissions']:
                        api = perm.get('api', '')
                        if api and api in content:
                            if perm['id'] not in self.permission_usage:
                                self.permission_usage[perm['id']] = {
                                    'group': group_name,
                                    'name': perm['name'],
                                    'api': api,
                                    'files': [],
                                    'usage_count': 0
                                }

                            # 记录使用位置
                            for line_num, line in enumerate(lines, 1):
                                if api in line:
                                    self.permission_usage[perm['id']]['files'].append({
                                        'file': str(js_file.relative_to(self.miniprogram_path)),
                                        'line': line_num,
                                        'code': line.strip()
                                    })
                                    self.permission_usage[perm['id']]['usage_count'] += 1

            except Exception as e:
                print(f"[-] 扫描文件失败 {js_file}: {e}")

    def _generate_confirmation(self) -> Dict:
        """生成权限确认单"""
        print("\n[*] 生成权限确认单...")

        # 读取小程序基本信息
        app_name = self.app_config.get('appName', '未设置')
        app_version = self.app_config.get('version', '1.0.0')

        # 从 project.config.json 读取更多信息
        project_config = self.miniprogram_path / 'project.config.json'
        if project_config.exists():
            try:
                with open(project_config, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                app_name = project_data.get('projectname', app_name)
            except Exception as e:
                print(f"[-] 读取 project.config.json 失败: {e}")

        # 生成确认单数据
        confirmation_data = {
            'basic_info': {
                'app_name': app_name,
                'app_version': app_version,
                'company': self.app_config.get('company', '待填写'),
                'contact': self.app_config.get('contact', '待填写'),
            },
            'permissions': [],
            'summary': {
                'total_permissions': 38,
                'used_permissions': len(self.permission_usage),
                'unused_permissions': 38 - len(self.permission_usage),
            }
        }

        # 按权限组生成详细信息
        for group_name, group_info in self.PERMISSION_GROUPS.items():
            for perm in group_info['permissions']:
                perm_id = perm['id']
                is_used = perm_id in self.permission_usage

                permission_info = {
                    'id': perm_id,
                    'group': group_name,
                    'name': perm['name'],
                    'is_applied': '是' if is_used else '否',
                    'business_function': self._get_business_function(perm_id),
                    'necessity': self._get_necessity_description(perm_id),
                    'api': perm.get('api', ''),
                    'usage_count': self.permission_usage.get(perm_id, {}).get('usage_count', 0),
                    'files': self.permission_usage.get(perm_id, {}).get('files', []),
                }

                confirmation_data['permissions'].append(permission_info)

        return confirmation_data

    def _get_business_function(self, perm_id: int) -> str:
        """获取对应的业务功能"""
        usage_info = self.permission_usage.get(perm_id, {})
        if not usage_info:
            return '未使用'

        # 根据权限类型推断业务功能
        group = usage_info['group']
        if '位置' in group:
            return '位置相关功能（导航、配送等）'
        elif '相机' in group or '照片' in group:
            return '图片相关功能（拍照、上传等）'
        elif '通讯录' in group:
            return '联系人相关功能（邀请、分享等）'
        elif '麦克风' in group:
            return '语音相关功能（录音、语音消息等）'
        elif '存储' in group:
            return '数据存储功能（缓存、文件管理等）'
        elif '网络' in group:
            return '网络通信功能（数据同步、API调用等）'
        else:
            return f'{group}相关功能'

    def _get_necessity_description(self, perm_id: int) -> str:
        """获取必要性说明"""
        usage_info = self.permission_usage.get(perm_id, {})
        if not usage_info:
            return '未使用，无需申请'

        group = usage_info['group']

        # 根据权限类型和具体使用情况生成必要性说明
        descriptions = {
            '位置': '为【{}】类小程序，【定位】功能需使用用户位置信息'.format(
                self.app_config.get('category', '本')
            ),
            '相机': '为【{}】类小程序，【拍照】功能需访问相机'.format(
                self.app_config.get('category', '本')
            ),
            '照片': '为【{}】类小程序，【图片上传】功能需读取用户照片'.format(
                self.app_config.get('category', '本')
            ),
            '通讯录': '为【{}】类小程序，【邀请好友】功能需访问通讯录'.format(
                self.app_config.get('category', '本')
            ),
            '麦克风': '为【{}】类小程序，【语音输入】功能需访问麦克风'.format(
                self.app_config.get('category', '本')
            ),
            '存储': '为【{}】类小程序，【数据缓存】功能需读写存储'.format(
                self.app_config.get('category', '本')
            ),
            '网络': '为【{}】类小程序，【数据同步】功能需使用网络权限'.format(
                self.app_config.get('category', '本')
            ),
        }

        return descriptions.get(group, f'为{self.app_config.get("category", "本")}类小程序，需要使用{group}权限')

    def generate_table(self, output_dir: str = None) -> str:
        """生成权限确认单表格"""
        confirmation_data = self._generate_confirmation()

        lines = []
        lines.append("=" * 120)
        lines.append("                        小程序申请权限确认单")
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
        lines.append(f"  • 已申请: {confirmation_data['summary']['used_permissions']}")
        lines.append(f"  • 未申请: {confirmation_data['summary']['unused_permissions']}")
        lines.append("")
        lines.append("=" * 120)
        lines.append("")
        lines.append("序号 | 权限组 | 敏感权限名称 | 小程序是否申请 | 对应业务功能 | 必要性说明")
        lines.append("-" * 120)

        for perm in confirmation_data['permissions']:
            is_applied = perm['is_applied']
            status_mark = "✅" if is_applied == "是" else "❌"

            lines.append(
                f"{perm['id']:3d} | "
                f"{perm['group']:8s} | "
                f"{perm['name']:16s} | "
                f"{status_mark} {is_applied:6s} | "
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
                for file_info in perm['files'][:5]:  # 只显示前5个调用位置
                    lines.append(f"  • {file_info['file']}:{file_info['line']}")
                if len(perm['files']) > 5:
                    lines.append(f"  ... 还有 {len(perm['files']) - 5} 处调用")

        lines.append("")
        lines.append("=" * 120)

        table_content = '\n'.join(lines)

        # 保存到文件
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            table_file = os.path.join(output_dir, '权限确认单.txt')
            with open(table_file, 'w', encoding='utf-8') as f:
                f.write(table_content)
            print(f"\n[+] 权限确认单已保存: {table_file}")

            # 保存 JSON 格式
            json_file = os.path.join(output_dir, 'permission_confirmation.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(confirmation_data, f, ensure_ascii=False, indent=2)
            print(f"[+] JSON 报告已保存: {json_file}")

        return table_content


def main():
    parser = argparse.ArgumentParser(description='小程序申请权限确认单生成工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    tool = PermissionConfirmationTool(args.miniprogram_path)
    tool.analyze()
    table = tool.generate_table(args.output)

    print("\n" + table)


if __name__ == '__main__':
    main()
