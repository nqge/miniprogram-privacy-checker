#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序权限调用详细报告生成器

生成类似人工分析的详细权限调用报告，包含：
1. 每个权限的详细调用情况
2. 代码位置和上下文
3. 调用链路分析
4. 合规性评估
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict


class DetailedPermissionReportGenerator:
    """详细权限报告生成器"""

    # 权限调用详情模板
    PERMISSION_DETAILS = {
        'scope.camera': {
            'name': '相机',
            'apis': ['wx.chooseImage', 'wx.chooseMedia', 'wx.chooseVideo'],
            'description': '拍照或从相册选择图片/视频',
            'typical_usage': ['用户头像设置', '问题反馈提供图片', '扫码付款'],
            'necessity': '必须'
        },
        'scope.writePhotosAlbum': {
            'name': '相册',
            'apis': ['wx.saveImageToPhotosAlbum', 'wx.saveVideoToPhotosAlbum'],
            'description': '保存图片/视频到系统相册',
            'typical_usage': ['保存图片', '保存视频'],
            'necessity': '必须'
        },
        'scope.userLocation': {
            'name': '地理位置',
            'apis': ['wx.getLocation', 'wx.chooseLocation', 'wx.openLocation'],
            'description': '获取用户地理位置信息',
            'typical_usage': ['地图展示', '附近门店', '导航服务'],
            'necessity': '必须'
        },
        'scope.record': {
            'name': '录音',
            'apis': ['wx.startRecord', 'wx.getRecorderManager'],
            'description': '录制音频',
            'typical_usage': ['语音输入', '语音消息', '语音识别'],
            'necessity': '必须'
        },
        'scope.bluetooth': {
            'name': '蓝牙',
            'apis': ['wx.openBluetoothAdapter'],
            'description': '蓝牙适配器',
            'typical_usage': ['蓝牙设备连接', '数据传输'],
            'necessity': '必须'
        },
        'scope.clipboard': {
            'name': '剪贴板',
            'apis': ['wx.getClipboardData'],
            'description': '读取系统剪贴板',
            'typical_usage': ['复制粘贴', '内容分享'],
            'necessity': '必须'
        },
        'scope.nfc': {
            'name': 'NFC',
            'apis': ['wx.startNFCDiscovery'],
            'description': 'NFC 设备',
            'typical_usage': ['NFC 刷卡', '近场通信'],
            'necessity': '必须'
        },
        'scope.werun': {
            'name': '微信运动',
            'apis': ['wx.getWeRunData'],
            'description': '获取微信运动步数',
            'typical_usage': ['健康数据', '运动统计'],
            'necessity': '必须'
        },
        'scope.addContact': {
            'name': '通讯录',
            'apis': ['wx.chooseContact'],
            'description': '获取通讯录',
            'typical_usage': ['添加联系人', '邀请好友'],
            'necessity': '必须'
        },
        'scope.address': {
            'name': '收货地址',
            'apis': ['wx.chooseAddress'],
            'description': '获取收货地址',
            'typical_usage': ['电商下单', '配送服务'],
            'necessity': '必须'
        },
        'scope.invoiceTitle': {
            'name': '发票抬头',
            'apis': ['wx.chooseInvoiceTitle'],
            'description': '获取发票抬头',
            'typical_usage': ['开具发票', '报销凭证'],
            'necessity': '必须'
        },
        'scope.invoice': {
            'name': '发票',
            'apis': ['wx.chooseInvoice'],
            'description': '选择发票',
            'typical_usage': ['发票管理', '报销'],
            'necessity': '必须'
        }
    }

    def __init__(self, miniprogram_path: str, scan_results: Dict):
        """
        初始化详细报告生成器

        Args:
            miniprogram_path: 小程序路径
            scan_results: API 扫描结果
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.scan_results = scan_results

        # 加载小程序基本信息
        self.miniprogram_info = self._load_miniprogram_info()

    def _load_miniprogram_info(self) -> Dict:
        """加载小程序基本信息"""
        info = {
            'name': '未知',
            'appid': '未知',
            'check_time': datetime.now().strftime('%Y年%m月%d日')
        }

        # 从 app.json 读取
        app_json = self.miniprogram_path / 'app.json'
        if app_json.exists():
            try:
                with open(app_json, 'r', encoding='utf-8') as f:
                    app_config = json.load(f)
                info['page_count'] = len(app_config.get('pages', []))
            except:
                pass

        # 从 project.config.json 读取
        project_config = self.miniprogram_path / 'project.config.json'
        if project_config.exists():
            try:
                with open(project_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                info['name'] = config.get('projectname', '未知')
                info['appid'] = config.get('appid', '未知')
            except:
                pass

        return info

    def _analyze_permission_usage(self, permission_scope: str) -> Dict:
        """
        分析特定权限的使用情况

        Args:
            permission_scope: 权限 scope，如 'scope.camera'

        Returns:
            权限使用情况详情
        """
        permission_info = self.PERMISSION_DETAILS.get(permission_scope, {})
        if not permission_info:
            return None

        related_apis = permission_info.get('apis', [])
        api_calls = self.scan_results.get('api_calls', {})

        # 查找所有相关的 API 调用
        found_calls = []
        for api in related_apis:
            if api in api_calls:
                found_calls.extend(api_calls[api])

        if not found_calls:
            return None

        # 分析调用详情
        details = {
            'permission_name': permission_info.get('name'),
            'permission_scope': permission_scope,
            'is_used': True,
            'apis_found': list(set([call['api'] for call in found_calls if 'api' in call])),
            'call_count': len(found_calls),
            'call_details': found_calls,
            'description': permission_info.get('description'),
            'typical_usage': permission_info.get('typical_usage', []),
            'necessity': permission_info.get('necessity', '必须')
        }

        # 分析调用上下文，识别使用场景
        details['usage_scenarios'] = self._analyze_usage_scenarios(found_calls)

        return details

    def _analyze_usage_scenarios(self, calls: List[Dict]) -> List[str]:
        """
        分析 API 调用的使用场景

        Args:
            calls: API 调用列表

        Returns:
            使用场景列表
        """
        scenarios = []

        for call in calls:
            context = call.get('context', '').lower()
            code = call.get('code', '').lower()

            # 分析函数名和上下文
            if 'avatar' in code or 'head' in code or '头像' in context:
                if '用户头像' not in scenarios:
                    scenarios.append('用户头像设置')
            elif 'feedback' in code or '反馈' in context:
                if '问题反馈' not in scenarios:
                    scenarios.append('问题反馈')
            elif 'scan' in code or '扫码' in context:
                if '扫码' not in scenarios:
                    scenarios.append('扫码功能')
            elif 'upload' in code or '上传' in context:
                if '上传图片' not in scenarios:
                    scenarios.append('上传图片')

        return scenarios if scenarios else ['通用功能']

    def _check_privacy_policy(self, permission_scope: str) -> Dict:
        """
        检查隐私政策中是否有该权限的说明

        Args:
            permission_scope: 权限 scope

        Returns:
            隐私政策检查结果
        """
        # 查找隐私政策文件
        privacy_files = list(self.miniprogram_path.rglob('privacy.md'))
        privacy_files.extend(list(self.miniprogram_path.rglob('隐私政策.txt')))
        privacy_files.extend(list(self.miniprogram_path.rglob('privacy.txt')))

        if not privacy_files:
            return {'found': False, 'message': '未找到隐私政策文件'}

        permission_info = self.PERMISSION_DETAILS.get(permission_scope, {})
        permission_name = permission_info.get('name', '')

        for privacy_file in privacy_files:
            try:
                with open(privacy_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查是否提到该权限
                if permission_name in content or permission_scope in content:
                    # 提取相关行
                    lines = content.split('\n')
                    relevant_lines = []
                    for i, line in enumerate(lines):
                        if permission_name in line or permission_scope in line:
                            start = max(0, i - 2)
                            end = min(len(lines), i + 3)
                            relevant_lines.extend(lines[start:end])
                            break

                    return {
                        'found': True,
                        'file': str(privacy_file.relative_to(self.miniprogram_path)),
                        'content': '\n'.join(relevant_lines[:10])  # 限制行数
                    }
            except:
                continue

        return {'found': False, 'message': f'隐私政策中未找到{permission_name}相关说明'}

    def generate_report(self, output_file: str = None) -> str:
        """
        生成详细的权限调用报告

        Args:
            output_file: 输出文件路径

        Returns:
            报告内容
        """
        lines = []

        # 报告头部
        lines.append(f"**检查时间**: {self.miniprogram_info['check_time']}")
        lines.append(f"**项目名称**: {self.miniprogram_info['name']}")
        lines.append(f"**小程序AppID**: {self.miniprogram_info['appid']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 分析每个权限
        section_num = 1
        permission_status = []  # 记录权限状态

        for permission_scope, permission_info in self.PERMISSION_DETAILS.items():
            # 分析权限使用情况
            usage = self._analyze_permission_usage(permission_scope)

            if not usage:
                # 未使用的权限，跳过
                continue

            # 检查隐私政策
            privacy_check = self._check_privacy_policy(permission_scope)

            # 生成该权限的详细报告
            lines.append(f"## {self._to_chinese_num(section_num)}、{permission_info['name']}权限调用检查")
            lines.append("")

            # 使用状态
            if usage['is_used']:
                lines.append(f"### ✅ 确认：检测到{permission_info['name']}权限调用")
                permission_status.append({
                    'permission': permission_info['name'],
                    'scope': permission_scope,
                    'status': '已使用',
                    'declared': permission_scope in self.scan_results.get('declared_permissions', {})
                })
            else:
                lines.append(f"### ⬜ 未检测到{permission_info['name']}权限调用")
                permission_status.append({
                    'permission': permission_info['name'],
                    'scope': permission_scope,
                    'status': '未使用',
                    'declared': False
                })

            lines.append("")

            # API 调用详情
            if usage['apis_found']:
                lines.append("#### 1. 检测到的 API 调用")
                lines.append("")
                for api in usage['apis_found']:
                    lines.append(f"- `{api}`")
                lines.append("")

            # 代码位置
            if usage['call_details']:
                lines.append("#### 2. 代码位置")
                lines.append("")

                for i, call in enumerate(usage['call_details'][:3], 1):  # 最多显示3个
                    lines.append(f"**调用 {i}**")
                    lines.append(f"  - **文件**: `{call.get('file', 'unknown')}`")
                    lines.append(f"  - **行号**: 第 {call.get('line', '?')} 行")
                    lines.append(f"  - **代码**: ```javascript")
                    lines.append(f"    {call.get('code', '')}")
                    lines.append(f"    ```")
                    lines.append("")

            # 使用场景
            if usage.get('usage_scenarios'):
                lines.append("#### 3. 使用场景")
                lines.append("")
                for scenario in usage['usage_scenarios']:
                    lines.append(f"- {scenario}")
                lines.append("")

            # 隐私政策检查
            lines.append("#### 4. 隐私政策检查")
            lines.append("")
            if privacy_check.get('found'):
                lines.append("✅ **已在隐私政策中说明**：")
                lines.append("")
                lines.append(f"```\n{privacy_check.get('content', '')}\n```")
            else:
                lines.append("❌ **未在隐私政策中找到相关说明**")
                lines.append("")
                lines.append(f"**建议**: 请在隐私政策中补充{permission_info['name']}权限的使用说明")

            lines.append("")
            lines.append("---")
            lines.append("")

            section_num += 1

        # 生成权限状态对比表
        lines.append("## 权限申请状态对比")
        lines.append("")
        lines.append("| 权限类别 | 权限名称 | 实际使用情况 | 确认单状态 | 是否正确 |")
        lines.append("|---------|---------|-------------|-----------|---------|")

        declared_permissions = self.scan_results.get('declared_permissions', {})

        for status in permission_status:
            actual_status = "✅ 已使用" if status['status'] == '已使用' else "❌ 未使用"
            declared_status = "✅ 已申请" if status['declared'] else "⬜ 未申请"
            is_correct = "✅ 正确" if (status['status'] == '已使用') == status['declared'] else "❌ 错误"

            lines.append(f"| {status['permission']} | {status['scope']} | {actual_status} | {declared_status} | {is_correct} |")

        lines.append("")

        # 合规性评估
        lines.append("## 合规性评估")
        lines.append("")

        # 统计
        total_used = len([s for s in permission_status if s['status'] == '已使用'])
        total_declared = len([s for s in permission_status if s['declared']])
        correct_count = len([s for s in permission_status if (s['status'] == '已使用') == s['declared']])

        lines.append(f"- **检测到的权限使用**: {total_used} 项")
        lines.append(f"- **已声明的权限**: {total_declared} 项")
        lines.append(f"- **状态正确率**: {correct_count}/{len(permission_status)} ({correct_count*100//len(permission_status) if permission_status else 0}%)")
        lines.append("")

        # 评分
        if correct_count == len(permission_status):
            lines.append("**总体评价**: ⭐⭐⭐⭐⭐ 优秀")
            lines.append("")
            lines.append("**评分**: 95/100")
        elif correct_count >= len(permission_status) * 0.8:
            lines.append("**总体评价**: ⭐⭐⭐⭐ 良好")
            lines.append("")
            lines.append("**评分**: 80/100")
        else:
            lines.append("**总体评价**: ⭐⭐⭐ 一般")
            lines.append("")
            lines.append("**评分**: 60/100")

        lines.append("")

        # 保存报告
        report_content = '\n'.join(lines)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"[+] 详细权限报告已保存: {output_file}")

        return report_content

    def _to_chinese_num(self, num: int) -> str:
        """数字转中文"""
        chinese_nums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        return chinese_nums[num - 1] if num <= 10 else str(num)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='生成详细权限调用报告')
    parser.add_argument('miniprogram_path', help='小程序路径')
    parser.add_argument('-s', '--scan-results', help='API 扫描结果 JSON 文件')
    parser.add_argument('-o', '--output', help='输出文件路径', default='detailed_permission_report.md')

    args = parser.parse_args()

    # 加载扫描结果
    if args.scan_results:
        with open(args.scan_results, 'r', encoding='utf-8') as f:
            scan_results = json.load(f)
    else:
        # 如果没有提供扫描结果，尝试从默认位置加载
        default_scan = Path(args.miniprogram_path) / 'privacy_check_results' / 'api_scan.json'
        if default_scan.exists():
            with open(default_scan, 'r', encoding='utf-8') as f:
                scan_results = json.load(f)
        else:
            print("[-] 错误：未找到扫描结果文件")
            return

    # 生成报告
    generator = DetailedPermissionReportGenerator(args.miniprogram_path, scan_results)
    generator.generate_report(args.output)


if __name__ == '__main__':
    main()
