#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序数据流分析工具
基于：《App违法违规收集使用个人信息行为认定方法》
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import argparse


class DataflowAnalyzer:
    """小程序数据流分析器"""

    # 敏感数据类型定义
    SENSITIVE_DATA_TYPES = {
        '用户位置': {
            'patterns': ['latitude', 'longitude', 'address', 'city', 'province', 'getLocation'],
            'risk_level': 'high',
            'description': '用户地理位置信息'
        },
        '手机号': {
            'patterns': ['phoneNumber', 'phone', 'mobile', 'tel'],
            'risk_level': 'high',
            'description': '用户手机号码'
        },
        '身份证': {
            'patterns': ['idCard', 'idcard', 'idCardNo', 'identity', '身份证'],
            'risk_level': 'high',
            'description': '用户身份证号'
        },
        '银行卡': {
            'patterns': ['bankCard', 'cardNo', 'accountNo', 'bankAccount'],
            'risk_level': 'high',
            'description': '用户银行卡号'
        },
        '真实姓名': {
            'patterns': ['realName', 'realname', 'trueName', 'truename', 'userName'],
            'risk_level': 'high',
            'description': '用户真实姓名'
        },
        '用户头像': {
            'patterns': ['avatarUrl', 'avatar', 'headImg', 'avatarurl'],
            'risk_level': 'medium',
            'description': '用户头像图片'
        },
        '用户昵称': {
            'patterns': ['nickName', 'nickname', 'nick'],
            'risk_level': 'low',
            'description': '用户昵称'
        },
        '密码': {
            'patterns': ['password', 'passwd', 'pwd', 'pass'],
            'risk_level': 'critical',
            'description': '用户密码'
        },
        'token': {
            'patterns': ['token', 'access_token', 'openid', 'sessionid', 'session_key'],
            'risk_level': 'critical',
            'description': '用户认证凭证'
        },
        '设备信息': {
            'patterns': ['deviceId', 'deviceInfo', 'model', 'system', 'platform'],
            'risk_level': 'medium',
            'description': '设备信息'
        },
    }

    # 数据收集方式
    COLLECTION_METHODS = {
        '用户输入': ['input', 'textarea', 'bindinput', 'bind:input'],
        'API调用': ['wx.getLocation', 'wx.getUserProfile', 'wx.chooseContact', 'wx.getWeRunData'],
        '表单提交': ['form', 'bindsubmit', 'bind:submit'],
        '传感器': ['startAccelerometer', 'startCompass', 'startGyroscope'],
    }

    # 数据存储方式
    STORAGE_METHODS = {
        '本地存储': ['wx.setStorage', 'wx.setStorageSync'],
        '缓存': ['cache'],
    }

    # 数据传输方式
    TRANSMISSION_METHODS = {
        'wx.request': '网络请求',
        'wx.uploadFile': '文件上传',
        'wx.downloadFile': '文件下载',
    }

    def __init__(self, miniprogram_path: str):
        """
        初始化数据流分析器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.js_files = []
        self.wxml_files = []
        self.data_collection_points = []
        self.data_storage_points = []
        self.data_transmission_points = []
        self.sensitive_data_usage = []
        self.issues = []

        # 加载文件
        self._load_files()

    def _load_files(self):
        """加载所有源文件"""
        print(f"[*] 扫描源文件...")
        for js_file in self.miniprogram_path.rglob("*.js"):
            self.js_files.append(js_file)
        for wxml_file in self.miniprogram_path.rglob("*.wxml"):
            self.wxml_files.append(wxml_file)
        print(f"[+] 发现 {len(self.js_files)} 个 JS 文件，{len(self.wxml_files)} 个 WXML 文件")

    def analyze(self) -> Dict:
        """
        执行数据流分析

        Returns:
            分析结果字典
        """
        print("[*] 开始数据流分析...")

        # 1. 分析数据收集点
        print("\n[1/5] 分析数据收集点...")
        self._analyze_collection_points()

        # 2. 分析数据存储点
        print("\n[2/5] 分析数据存储点...")
        self._analyze_storage_points()

        # 3. 分析数据传输点
        print("\n[3/5] 分析数据传输点...")
        self._analyze_transmission_points()

        # 4. 分析敏感数据使用
        print("\n[4/5] 分析敏感数据使用...")
        self._analyze_sensitive_data()

        # 5. 检查合规性
        print("\n[5/5] 检查合规性...")
        self._check_compliance()

        # 6. 生成分析报告
        return self._generate_report()

    def _analyze_collection_points(self):
        """分析数据收集点"""
        # 分析 WXML 文件中的用户输入
        for wxml_file in self.wxml_files:
            try:
                with open(wxml_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查 input 标签
                input_pattern = re.compile(r'<input[^>]*bindinput=["\']([^"\']+)["\'][^>]*name=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
                for match in input_pattern.finditer(content):
                    event_handler = match.group(1)
                    field_name = match.group(2)
                    self.data_collection_points.append({
                        'type': '用户输入',
                        'file': str(wxml_file.relative_to(self.miniprogram_path)),
                        'handler': event_handler,
                        'field': field_name,
                        'description': f'用户输入字段: {field_name}'
                    })

                # 检查 form 标签
                form_pattern = re.compile(r'<form[^>]*bindsubmit=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
                for match in form_pattern.finditer(content):
                    event_handler = match.group(1)
                    self.data_collection_points.append({
                        'type': '表单提交',
                        'file': str(wxml_file.relative_to(self.miniprogram_path)),
                        'handler': event_handler,
                        'description': f'表单提交事件: {event_handler}'
                    })

            except Exception as e:
                print(f"[-] 读取文件失败 {wxml_file}: {e}")

        # 分析 JS 文件中的敏感 API 调用
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查敏感 API 调用
                for method, apis in self.COLLECTION_METHODS.items():
                    for api in apis:
                        if api in content:
                            for line_num, line in enumerate(lines, 1):
                                if api in line:
                                    self.data_collection_points.append({
                                        'type': method,
                                        'file': str(js_file.relative_to(self.miniprogram_path)),
                                        'line': line_num,
                                        'api': api,
                                        'code': line.strip(),
                                        'description': f'敏感 API 调用: {api}'
                                    })

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 发现 {len(self.data_collection_points)} 个数据收集点")

    def _analyze_storage_points(self):
        """分析数据存储点"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查本地存储 API
                for method, apis in self.STORAGE_METHODS.items():
                    for api in apis:
                        if api in content:
                            for line_num, line in enumerate(lines, 1):
                                if api in line:
                                    # 检查存储的数据类型
                                    stored_data = []
                                    for data_type, info in self.SENSITIVE_DATA_TYPES.items():
                                        for pattern in info['patterns']:
                                            if pattern in line:
                                                stored_data.append(data_type)
                                                break

                                    self.data_storage_points.append({
                                        'type': method,
                                        'file': str(js_file.relative_to(self.miniprogram_path)),
                                        'line': line_num,
                                        'api': api,
                                        'code': line.strip(),
                                        'stored_data': stored_data,
                                        'description': f'{method}: {api}'
                                    })

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 发现 {len(self.data_storage_points)} 个数据存储点")

    def _analyze_transmission_points(self):
        """分析数据传输点"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查数据传输 API
                for api, desc in self.TRANSMISSION_METHODS.items():
                    if api in content:
                        for line_num, line in enumerate(lines, 1):
                            if api in line:
                                # 检查是否使用 HTTPS
                                uses_https = 'https://' in line
                                uses_http = 'http://' in line and 'https://' not in line

                                # 检查传输的数据类型
                                transmitted_data = []
                                for data_type, info in self.SENSITIVE_DATA_TYPES.items():
                                    for pattern in info['patterns']:
                                        if pattern in line:
                                            transmitted_data.append(data_type)
                                            break

                                self.data_transmission_points.append({
                                    'type': desc,
                                    'file': str(js_file.relative_to(self.miniprogram_path)),
                                    'line': line_num,
                                    'api': api,
                                    'code': line.strip(),
                                    'uses_https': uses_https,
                                    'uses_http': uses_http,
                                    'transmitted_data': transmitted_data,
                                    'description': f'{desc}: {api}'
                                })

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 发现 {len(self.data_transmission_points)} 个数据传输点")

    def _analyze_sensitive_data(self):
        """分析敏感数据使用"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查敏感数据类型
                for data_type, info in self.SENSITIVE_DATA_TYPES.items():
                    for pattern in info['patterns']:
                        if pattern in content:
                            for line_num, line in enumerate(lines, 1):
                                if pattern in line:
                                    self.sensitive_data_usage.append({
                                        'data_type': data_type,
                                        'risk_level': info['risk_level'],
                                        'file': str(js_file.relative_to(self.miniprogram_path)),
                                        'line': line_num,
                                        'pattern': pattern,
                                        'code': line.strip(),
                                        'description': info['description']
                                    })
                                    break  # 避免重复记录

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 发现 {len(self.sensitive_data_usage)} 处敏感数据使用")

    def _check_compliance(self):
        """检查合规性"""
        # 检查本地存储敏感数据
        for storage in self.data_storage_points:
            if storage['stored_data']:
                critical_data = [d for d in storage['stored_data']
                                if self.SENSITIVE_DATA_TYPES[d]['risk_level'] in ['critical', 'high']]
                if critical_data:
                    self.issues.append({
                        'type': 'warning',
                        'category': '数据存储',
                        'file': storage['file'],
                        'line': storage['line'],
                        'message': f'本地存储了敏感数据: {", ".join(critical_data)}',
                        'suggestion': '敏感数据不应在本地存储，如确需存储，请使用加密方式',
                        'code_snippet': storage['code']
                    })

        # 检查 HTTP 传输
        for transmission in self.data_transmission_points:
            if transmission['uses_http']:
                self.issues.append({
                    'type': 'critical',
                    'category': '数据传输',
                    'file': transmission['file'],
                    'line': transmission['line'],
                    'message': '使用 HTTP 协议传输数据',
                    'suggestion': '必须使用 HTTPS 协议，HTTP 协议存在中间人攻击风险',
                    'code_snippet': transmission['code']
                })

        # 检查敏感数据明文传输
        for transmission in self.data_transmission_points:
            transmitted_data = transmission['transmitted_data']
            critical_data = [d for d in transmitted_data
                            if self.SENSITIVE_DATA_TYPES[d]['risk_level'] in ['critical', 'high']]
            if critical_data and not transmission['uses_https']:
                self.issues.append({
                    'type': 'critical',
                    'category': '数据传输',
                    'file': transmission['file'],
                    'line': transmission['line'],
                    'message': f'可能通过非 HTTPS 传输敏感数据: {", ".join(critical_data)}',
                    'suggestion': '敏感数据必须通过 HTTPS 加密传输',
                    'code_snippet': transmission['code']
                })

    def _generate_report(self) -> Dict:
        """生成分析报告"""
        # 统计风险等级
        risk_stats = defaultdict(int)
        for usage in self.sensitive_data_usage:
            risk_level = usage['risk_level']
            risk_stats[risk_level] += 1

        # 统计问题类型
        issue_stats = defaultdict(int)
        for issue in self.issues:
            issue_stats[issue['type']] += 1

        # 计算评分
        critical_issues = issue_stats.get('critical', 0)
        warning_issues = issue_stats.get('warning', 0)

        if critical_issues == 0:
            score = max(100 - (warning_issues * 15), 0)
        else:
            score = max(100 - (critical_issues * 30) - (warning_issues * 10), 0)

        return {
            'score': score,
            'data_collection_points': self.data_collection_points,
            'data_storage_points': self.data_storage_points,
            'data_transmission_points': self.data_transmission_points,
            'sensitive_data_usage': self.sensitive_data_usage,
            'issues': self.issues,
            'risk_stats': dict(risk_stats),
            'issue_stats': dict(issue_stats),
            'summary': {
                'total_collection_points': len(self.data_collection_points),
                'total_storage_points': len(self.data_storage_points),
                'total_transmission_points': len(self.data_transmission_points),
                'total_sensitive_data_usage': len(self.sensitive_data_usage),
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序数据流分析报告")
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
    summary = report['summary']
    print("\n📋 分析摘要:")
    print(f"  - 数据收集点: {summary['total_collection_points']}")
    print(f"  - 数据存储点: {summary['total_storage_points']}")
    print(f"  - 数据传输点: {summary['total_transmission_points']}")
    print(f"  - 敏感数据使用: {summary['total_sensitive_data_usage']}")
    print(f"  - 严重问题: {report['issue_stats'].get('critical', 0)}")
    print(f"  - 警告问题: {report['issue_stats'].get('warning', 0)}")

    # 数据收集点
    if report['data_collection_points']:
        print(f"\n🔍 数据收集点 ({len(report['data_collection_points'])} 个):")
        for point in report['data_collection_points'][:10]:
            print(f"  • [{point['type']}] {point['description']}")
            print(f"    位置: {point['file']}")
            if 'line' in point:
                print(f"    行号: {point['line']}")
        if len(report['data_collection_points']) > 10:
            print(f"  ... 还有 {len(report['data_collection_points']) - 10} 个")

    # 数据存储点
    if report['data_storage_points']:
        print(f"\n💾 数据存储点 ({len(report['data_storage_points'])} 个):")
        for point in report['data_storage_points'][:10]:
            print(f"  • [{point['type']}] {point['description']}")
            if point['stored_data']:
                print(f"    存储数据: {', '.join(point['stored_data'])}")
            print(f"    位置: {point['file']}:{point['line']}")
        if len(report['data_storage_points']) > 10:
            print(f"  ... 还有 {len(report['data_storage_points']) - 10} 个")

    # 数据传输点
    if report['data_transmission_points']:
        print(f"\n🌐 数据传输点 ({len(report['data_transmission_points'])} 个):")
        for point in report['data_transmission_points'][:10]:
            protocol = "HTTPS ✓" if point['uses_https'] else ("HTTP ✗" if point['uses_http'] else "未知")
            print(f"  • [{point['type']}] {point['description']} ({protocol})")
            if point['transmitted_data']:
                print(f"    传输数据: {', '.join(point['transmitted_data'])}")
            print(f"    位置: {point['file']}:{point['line']}")
        if len(report['data_transmission_points']) > 10:
            print(f"  ... 还有 {len(report['data_transmission_points']) - 10} 个")

    # 敏感数据使用
    if report['sensitive_data_usage']:
        print(f"\n🔒 敏感数据使用 ({len(report['sensitive_data_usage'])} 处):")
        risk_levels = {usage['data_type']: usage['risk_level'] for usage in report['sensitive_data_usage']}
        for data_type, risk_level in sorted(risk_levels.items()):
            risk_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk_level, '⚪')
            print(f"  {risk_emoji} {data_type} ({risk_level.upper()})")

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
            print(f"     类别: {issue['category']}")
            print(f"     位置: {issue['file']}:{issue['line']}")
            print(f"     描述: {issue['message']}")
            print(f"     建议: {issue['suggestion']}")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        with open(os.path.join(output_dir, 'dataflow_analysis.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/dataflow_analysis.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'dataflow_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序数据流分析报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"分析摘要:\n")
            f.write(f"  - 数据收集点: {summary['total_collection_points']}\n")
            f.write(f"  - 数据存储点: {summary['total_storage_points']}\n")
            f.write(f"  - 数据传输点: {summary['total_transmission_points']}\n")
            f.write(f"  - 敏感数据使用: {summary['total_sensitive_data_usage']}\n\n")

            if report['issues']:
                f.write(f"合规问题 ({len(report['issues'])} 个):\n\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"{i}. [{issue['type'].upper()}] {issue['message']}\n")
                    f.write(f"   位置: {issue['file']}:{issue['line']}\n")
                    f.write(f"   建议: {issue['suggestion']}\n\n")

        print(f"[+] 文本报告已保存: {output_dir}/dataflow_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序数据流分析工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    analyzer = DataflowAnalyzer(args.miniprogram_path)
    report = analyzer.analyze()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
