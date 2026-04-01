#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序日志泄露风险检测工具
专门检测日志输出中的敏感信息泄露
"""

import os
import re
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import argparse


class LogLeakChecker:
    """小程序日志泄露风险检测器"""

    # 敏感信息定义
    SENSITIVE_PATTERNS = {
        # ===== 认证凭证 =====
        'password': {
            'name': '密码',
            'description': '用户登录密码或支付密码',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*password[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*passwd[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*pwd[^),)]*\)',
                r'\.log\s*\([^)]*password[^)]*\)',
            ],
            'risk_level': 'critical',
            'category': '认证凭证'
        },
        'token': {
            'name': 'Token/SessionID',
            'description': '用户认证令牌或会话ID',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*token[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*openid[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*sessionid[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*session_key[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*access_token[^),)]*\)',
            ],
            'risk_level': 'critical',
            'category': '认证凭证'
        },
        'api_key': {
            'name': 'API Key/Secret Key',
            'description': 'API 密钥或 Secret 密钥',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*api[_-]?key[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*secret[_-]?key[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*appsecret[^),)]*\)',
            ],
            'risk_level': 'critical',
            'category': '认证凭证'
        },

        # ===== 个人信息 =====
        'phone': {
            'name': '手机号码',
            'description': '用户手机号码',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*phone[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*mobile[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*tel[^),)]*\)',
            ],
            'risk_level': 'high',
            'category': '个人信息'
        },
        'idcard': {
            'name': '身份证号',
            'description': '用户身份证号码',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*idcard[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*idCard[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*identity[^),)]*\)',
            ],
            'risk_level': 'high',
            'category': '个人信息'
        },
        'realname': {
            'name': '真实姓名',
            'description': '用户真实姓名',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*realname[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*realName[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*trueName[^),)]*\)',
            ],
            'risk_level': 'high',
            'category': '个人信息'
        },
        'email': {
            'name': '邮箱地址',
            'description': '用户邮箱地址',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*email[^),)]*\)',
            ],
            'risk_level': 'medium',
            'category': '个人信息'
        },
        'address': {
            'name': '地址信息',
            'description': '用户详细地址',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*address[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*province[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*city[^),)]*\)',
            ],
            'risk_level': 'medium',
            'category': '个人信息'
        },
        'bankcard': {
            'name': '银行卡号',
            'description': '用户银行卡号',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*bankcard[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*bankCard[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*cardNo[^),)]*\)',
            ],
            'risk_level': 'critical',
            'category': '个人信息'
        },

        # ===== 业务数据 =====
        'user_data': {
            'name': '用户数据',
            'description': '完整的用户信息对象',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*user[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*userInfo[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*user_info[^),)]*\)',
            ],
            'risk_level': 'medium',
            'category': '业务数据'
        },
        'request_data': {
            'name': '请求数据',
            'description': '接口请求数据（可能包含敏感信息）',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*data[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*params[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*body[^),)]*\)',
            ],
            'risk_level': 'medium',
            'category': '业务数据'
        },
        'response_data': {
            'name': '响应数据',
            'description': '接口响应数据（可能包含敏感信息）',
            'patterns': [
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*res[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*response[^),)]*\)',
                r'console\.(log|debug|info|warn|error)\s*\([^,)]*result[^),)]*\)',
            ],
            'risk_level': 'medium',
            'category': '业务数据'
        },
    }

    def __init__(self, miniprogram_path: str):
        """
        初始化日志泄露检测器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.js_files = []
        self.log_leaks = defaultdict(list)
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
        执行日志泄露检测

        Returns:
            检测结果字典
        """
        print("[*] 开始日志泄露检测...")

        # 1. 扫描 JS 文件中的日志输出
        print("\n[1/2] 扫描日志输出...")
        self._scan_console_logs()

        # 2. 分析泄露风险
        print("\n[2/2] 分析泄露风险...")
        self._analyze_leaks()

        # 3. 生成检测报告
        return self._generate_report()

    def _scan_console_logs(self):
        """扫描所有 JS 文件中的 console 调用"""
        console_patterns = [
            r'console\.log\s*\(',
            r'console\.debug\s*\(',
            r'console\.info\s*\(',
            r'console\.warn\s*\(',
            r'console\.error\s*\(',
            r'console\.trace\s*\(',
        ]

        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查所有 console 调用
                for line_num, line in enumerate(lines, 1):
                    for pattern in console_patterns:
                        if re.search(pattern, line):
                            # 检查是否包含敏感信息
                            self._check_sensitive_content(js_file, line_num, line)
                            break  # 避免重复检查

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 扫描完成，发现 {len(self.log_leaks)} 处潜在泄露")

    def _check_sensitive_content(self, js_file, line_num, line):
        """检查日志内容是否包含敏感信息"""
        line_lower = line.lower()

        for leak_type, leak_info in self.SENSITIVE_PATTERNS.items():
            for pattern in leak_info['patterns']:
                if re.search(pattern, line_lower):
                    # 提取上下文
                    try:
                        with open(js_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.split('\n')

                        context_start = max(0, line_num - 3)
                        context_end = min(len(lines), line_num + 4)
                        context = lines[context_start:context_end]

                        self.log_leaks[leak_type].append({
                            'file': str(js_file.relative_to(self.miniprogram_path)),
                            'line': line_num,
                            'code': line.strip(),
                            'context': '\n'.join(context),
                            'matched_pattern': pattern
                        })

                    except Exception as e:
                        print(f"[-] 提取上下文失败: {e}")

                    break  # 避免重复记录

    def _analyze_leaks(self):
        """分析泄露风险"""
        # 统计各类泄露的严重程度
        for leak_type, detections in self.log_leaks.items():
            leak_info = self.SENSITIVE_PATTERNS.get(leak_type, {})

            # 每个检测点生成一个问题
            for detection in detections[:5]:  # 最多显示 5 个
                self.issues.append({
                    'type': leak_info['risk_level'],
                    'category': leak_info['category'],
                    'leak_type': leak_info['name'],
                    'file': detection['file'],
                    'line': detection['line'],
                    'message': f'检测到 {leak_info["name"]} 的日志输出',
                    'suggestion': f'在生产环境中删除或注释掉 {leak_info["name"]} 的日志输出，避免信息泄露',
                    'code_snippet': detection['code'],
                    'description': leak_info['description']
                })

    def _generate_report(self) -> Dict:
        """生成检测报告"""
        # 统计类别
        category_stats = defaultdict(int)
        for leak_type in self.log_leaks.keys():
            leak_info = self.SENSITIVE_PATTERNS.get(leak_type, {})
            category = leak_info.get('category', '其他')
            category_stats[category] += 1

        # 统计风险等级
        risk_stats = defaultdict(int)
        for leak_type in self.log_leaks.keys():
            leak_info = self.SENSITIVE_PATTERNS.get(leak_type, {})
            risk_level = leak_info.get('risk_level', 'low')
            risk_stats[risk_level] += 1

        # 统计问题类型
        issue_stats = defaultdict(int)
        for issue in self.issues:
            issue_stats[issue['type']] += 1

        # 计算评分
        critical_leaks = len([
            t for t in self.log_leaks.keys()
            if self.SENSITIVE_PATTERNS.get(t, {}).get('risk_level') == 'critical'
        ])

        high_leaks = len([
            t for t in self.log_leaks.keys()
            if self.SENSITIVE_PATTERNS.get(t, {}).get('risk_level') == 'high'
        ])

        if critical_leaks > 0:
            score = max(100 - (critical_leleaks * 30) - (high_leaks * 15), 0)
        elif high_leaks > 0:
            score = max(100 - (high_leaks * 15) - (issue_stats.get('warning', 0) * 5), 0)
        else:
            score = max(100 - (issue_stats.get('warning', 0) * 10), 0)

        return {
            'score': score,
            'log_leaks': dict(self.log_leaks),
            'issues': self.issues,
            'category_stats': dict(category_stats),
            'risk_stats': dict(risk_stats),
            'issue_stats': dict(issue_stats),
            'summary': {
                'total_leak_types': len(self.log_leaks),
                'total_leak_points': sum(len(d) for d in self.log_leaks.values()),
                'critical_leak_types': critical_leaks,
                'high_leak_types': high_leaks,
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序日志泄露风险检测报告")
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
    print("\n📋 检测摘要:")
    print(f"  - 泄露类型: {summary['total_leak_types']}")
    print(f"  - 泄露点数: {summary['total_leak_points']}")
    print(f"  - 严重泄露: {summary['critical_leak_types']}")
    print(f"  - 高危泄露: {summary['high_leak_types']}")

    # 按类别显示泄露
    if report['category_stats']:
        print(f"\n📂 泄露分类:")
        for category, count in sorted(report['category_stats'].items(), key=lambda x: -x[1]):
            print(f"  - {category}: {count} 类")

    # 按风险等级显示
    if report['risk_stats']:
        print(f"\n🎭 风险等级分布:")
        for risk_level, count in report['risk_stats'].items():
            risk_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk_level, '⚪')
            print(f"  {risk_emoji} {risk_level.upper()}: {count} 类")

    # 详细泄露信息
    if report['log_leaks']:
        print(f"\n🔍 详细泄露信息:")

        for leak_type, detections in sorted(report['log_leaks'].items()):
            leak_info = LogLeakChecker.SENSITIVE_PATTERNS.get(leak_type, {})
            risk_level = leak_info.get('risk_level', 'low')
            risk_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk_level, '⚪')

            print(f"\n  {risk_emoji} {leak_info.get('name', leak_type)}")
            print(f"     风险: {risk_level.upper()}")
            print(f"     类别: {leak_info.get('category', 'N/A')}")
            print(f"     描述: {leak_info.get('description', 'N/A')}")
            print(f"     检测次数: {len(detections)}")

            # 显示检测位置
            print(f"     检测位置:")
            for detection in detections[:3]:
                print(f"       - {detection['file']}:{detection['line']}")
            if len(detections) > 3:
                print(f"       ... 还有 {len(detections) - 3} 处")

    # 问题列表
    if report['issues']:
        print(f"\n🚨 风险问题 ({len(report['issues'])} 个):")
        for i, issue in enumerate(report['issues'][:10], 1):
            type_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(issue['type'], '•')

            print(f"\n  {type_emoji} 问题 {i}: [{issue['type'].upper()}]")
            print(f"     类别: {issue['category']}")
            print(f"     泄露类型: {issue['leak_type']}")
            print(f"     位置: {issue['file']}:{issue['line']}")
            print(f"     描述: {issue['description']}")
            print(f"     建议: {issue['suggestion']}")

        if len(report['issues']) > 10:
            print(f"\n  ... 还有 {len(report['issues']) - 10} 个问题")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        import json
        with open(os.path.join(output_dir, 'log_leak_check.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/log_leak_check.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'log_leak_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序日志泄露风险检测报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"检测摘要:\n")
            f.write(f"  - 泄露类型: {summary['total_leak_types']}\n")
            f.write(f"  - 泄露点数: {summary['total_leak_points']}\n")
            f.write(f"  - 严重泄露: {summary['critical_leak_types']}\n\n")

            if report['log_leaks']:
                f.write(f"泄露详情:\n\n")
                for leak_type, detections in sorted(report['log_leaks'].items()):
                    leak_info = LogLeakChecker.SENSITIVE_PATTERNS.get(leak_type, {})
                    f.write(f"{leak_info.get('name', leak_type)}: {len(detections)} 处\n")
                    for detection in detections[:5]:
                        f.write(f"  - {detection['file']}:{detection['line']}\n")
                    f.write("\n")

            if report['issues']:
                f.write(f"风险问题 ({len(report['issues'])} 个):\n\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"{i}. [{issue['type'].upper()}] {issue['message']}\n")
                    f.write(f"   位置: {issue['file']}:{issue['line']}\n")
                    f.write(f"   建议: {issue['suggestion']}\n\n")

        print(f"[+] 文本报告已保存: {output_dir}/log_leak_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序日志泄露风险检测工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    checker = LogLeakChecker(args.miniprogram_path)
    report = checker.check()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
