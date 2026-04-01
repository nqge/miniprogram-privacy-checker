#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序动态调试风险检测工具
检测生产环境中是否启用了动态调试功能
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import argparse


class DebugChecker:
    """小程序动态调试风险检测器"""

    # 动态调试工具和配置
    DEBUG_PATTERNS = {
        'vconsole': {
            'name': 'vConsole 调试工具',
            'description': 'vConsole 是一个轻量、可拓展、针对手机网页的前端开发者调试面板',
            'risk_level': 'high',
            'patterns': [
                r'vconsole',
                r'VConsole',
                r'initVConsole',
                r'new\s+VConsole',
            ],
            'detection_files': ['.js', '.json']
        },
        'eruda': {
            'name': 'eruda 调试工具',
            'description': 'eruda 是一个专为手机网页前端设计的调试面板',
            'risk_level': 'high',
            'patterns': [
                r'eruda',
                r'Eruda',
                r'initEruda',
                r'erudaLoad',
                r'eruda\.init',
            ],
            'detection_files': ['.js', '.json']
        },
        'debug_mode': {
            'name': 'Debug 调试模式',
            'description': '启用调试模式会暴露更多调试信息',
            'risk_level': 'medium',
            'patterns': [
                r'debug\s*[=:]\s*true',
                r'VEBRSION\s*=\s*"\s*\d+\.\d+\.\d+\s+-\s*dev',
                r'"debug"\s*:\s*true',
            ],
            'detection_files': ['.js', '.json']
        },
        'devtool': {
            'name': 'DevTools 开发者工具',
            'description': '开发者工具可能在生产环境中暴露',
            'risk_level': 'high',
            'patterns': [
                r'openDevTools',
                r'showDevTools',
                r'enableDevTools',
                r'__wxConfig__.*debug',
            ],
            'detection_files': ['.js']
        },
        'sourcemap': {
            'name': 'SourceMap 源码映射',
            'description': 'SourceMap 可能在生产环境中暴露源码',
            'risk_level': 'medium',
            'patterns': [
                r'sourceMappingURL',
                r'sourcemaps',
                r'\.map"',
                r'data:application/json;base64',
            ],
            'detection_files': ['.js']
        },
        'console_debug': {
            'name': 'Console 调试输出',
            'description': '生产环境中保留大量 console 调试信息',
            'risk_level': 'low',
            'patterns': [
                r'console\.(log|debug|info|warn|error|trace)\s*\(',
                r'console\.log\s*',
            ],
            'detection_files': ['.js']
        },
    }

    # 敏感信息的日志输出
    SENSITIVE_LOG_PATTERNS = {
        'password': {
            'name': '密码信息',
            'patterns': [
                r'console\.\w+\s*\([^)]*password[^)]*\)',
                r'console\.\w\+\s*\([^)]*passwd[^)]*\)',
                r'console\.\w+\s*\([^)]*pwd[^)]*\)',
            ],
            'risk_level': 'critical'
        },
        'token': {
            'name': 'Token/认证信息',
            'patterns': [
                r'console\.\w+\s*\([^)]*token[^)]*\)',
                r'console\.\w+\s*\([^)]*openid[^)]*\)',
                r'console\.\w+\s*\([^)]*sessionid[^)]*\)',
                r'console\.\w+\s*\([^)]*session_key[^)]*\)',
            ],
            'risk_level': 'critical'
        },
        'user_info': {
            'name': '用户个人信息',
            'patterns': [
                r'console\.\w+\s*\([^)]*phone[^)]*\)',
                r'console\.\w+\s*\([^)]*mobile[^)]*\)',
                r'console\.\w+\s*\([^)]*idcard[^)]*\)',
                r'console\.\w+\s*\([^)]*idCard[^)]*\)',
                r'console\.\w+\s*\([^)]*realname[^)]*\)',
            ],
            'risk_level': 'high'
        },
        'request_data': {
            'name': '接口请求数据',
            'patterns': [
                r'console\.\w+\s*\([^)]*data[^)]*\)',
                r'console\.\w+\s*\([^)]*params[^)]*\)',
                r'console\.\w+\s*\([^)]*body[^)]*\)',
            ],
            'risk_level': 'medium'
        },
    }

    def __init__(self, miniprogram_path: str):
        """
        初始化调试风险检测器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.js_files = []
        self.json_files = []
        self.debug_detections = defaultdict(list)
        self.sensitive_log_detections = defaultdict(list)
        self.issues = []

        # 加载文件
        self._load_files()

    def _load_files(self):
        """加载所有源文件"""
        print(f"[*] 扫描源文件...")
        for js_file in self.miniprogram_path.rglob("*.js"):
            self.js_files.append(js_file)
        for json_file in self.miniprogram_path.rglob("*.json"):
            self.json_files.append(json_file)
        print(f"[+] 发现 {len(self.js_files)} 个 JS 文件，{len(self.json_files)} 个 JSON 文件")

    def check(self) -> Dict:
        """
        执行调试风险检查

        Returns:
            检查结果字典
        """
        print("[*] 开始动态调试风险检查...")

        # 1. 检测动态调试工具
        print("\n[1/3] 检测动态调试工具...")
        self._detect_debug_tools()

        # 2. 检测敏感信息日志输出
        print("\n[2/3] 检测敏感信息日志输出...")
        self._detect_sensitive_logs()

        # 3. 检查配置文件
        print("\n[3/3] 检查配置文件...")
        self._check_config_files()

        # 4. 生成检查报告
        return self._generate_report()

    def _detect_debug_tools(self):
        """检测动态调试工具"""
        for debug_type, debug_info in self.DEBUG_PATTERNS.items():
            # 确定要扫描的文件类型
            files_to_scan = []
            if '.js' in debug_info['detection_files']:
                files_to_scan.extend(self.js_files)
            if '.json' in debug_info['detection_files']:
                files_to_scan.extend(self.json_files)

            # 扫描文件
            for file_path in files_to_scan:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')

                    # 检查每个模式
                    for pattern in debug_info['patterns']:
                        regex = re.compile(pattern, re.IGNORECASE)
                        for line_num, line in enumerate(lines, 1):
                            if regex.search(line):
                                # 提取上下文
                                context_start = max(0, line_num - 2)
                                context_end = min(len(lines), line_num + 3)
                                context = lines[context_start:context_end]

                                self.debug_detections[debug_type].append({
                                    'file': str(file_path.relative_to(self.miniprogram_path)),
                                    'line': line_num,
                                    'pattern': pattern,
                                    'code': line.strip(),
                                    'context': '\n'.join(context)
                                })

                                # 记录问题
                                self.issues.append({
                                    'type': 'critical' if debug_info['risk_level'] == 'high' else 'warning',
                                    'category': '动态调试',
                                    'tool': debug_info['name'],
                                    'file': str(file_path.relative_to(self.miniprogram_path)),
                                    'line': line_num,
                                    'message': f'检测到 {debug_info["name"]} 使用',
                                    'suggestion': f'在生产环境中禁用 {debug_info["name"]}，{debug_info["description"]}',
                                    'code_snippet': line.strip()
                                })
                                break  # 避免同一行重复记录

                except Exception as e:
                    print(f"[-] 读取文件失败 {file_path}: {e}")

        print(f"[+] 发现 {len(self.debug_detections)} 种调试工具")

    def _detect_sensitive_logs(self):
        """检测敏感信息日志输出"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查每个敏感类型
                for log_type, log_info in self.SENSITIVE_LOG_PATTERNS.items():
                    for pattern in log_info['patterns']:
                        regex = re.compile(pattern, re.IGNORECASE)
                        for line_num, line in enumerate(lines, 1):
                            if regex.search(line):
                                # 提取上下文
                                context_start = max(0, line_num - 2)
                                context_end = min(len(lines), line_num + 3)
                                context = lines[context_start:context_end]

                                self.sensitive_log_detections[log_type].append({
                                    'file': str(js_file.relative_to(self.miniprogram_path)),
                                    'line': line_num,
                                    'pattern': pattern,
                                    'code': line.strip(),
                                    'context': '\n'.join(context)
                                })

                                # 记录问题
                                self.issues.append({
                                    'type': log_info['risk_level'],
                                    'category': '日志泄露',
                                    'log_type': log_info['name'],
                                    'file': str(js_file.relative_to(self.miniprogram_path)),
                                    'line': line_num,
                                    'message': f'检测到 {log_info["name"]} 的日志输出',
                                    'suggestion': '在生产环境中删除或注释掉敏感信息的日志输出',
                                    'code_snippet': line.strip()
                                })
                                break  # 避免同一行重复记录

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        print(f"[+] 发现 {len(self.sensitive_log_detections)} 种敏感日志输出")

    def _check_config_files(self):
        """检查配置文件"""
        # 检查 app.json
        app_json = self.miniprogram_path / 'app.json'
        if app_json.exists():
            try:
                with open(app_json, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 检查 debug 配置
                if config.get('debug') == True:
                    self.issues.append({
                        'type': 'critical',
                        'category': '配置安全',
                        'file': 'app.json',
                        'message': 'app.json 中启用了 debug 模式',
                        'suggestion': '在生产环境中将 debug 设置为 false',
                        'code_snippet': '"debug": true'
                    })

                    # 添加到调试检测结果
                    self.debug_detections['debug_mode'].append({
                        'file': 'app.json',
                        'line': 1,
                        'pattern': 'debug',
                        'code': '"debug": true',
                        'context': 'app.json 配置'
                    })

                # 检查版本号是否为 dev
                version = config.get('version', '')
                if 'dev' in version.lower() or version.endswith('.0.0'):
                    self.issues.append({
                        'type': 'warning',
                        'category': '配置安全',
                        'file': 'app.json',
                        'message': f'版本号可能为开发版本: {version}',
                        'suggestion': '生产环境中使用正式版本号',
                        'code_snippet': f'"version": "{version}"'
                    })

            except Exception as e:
                print(f"[-] 读取 app.json 失败: {e}")

    def _generate_report(self) -> Dict:
        """生成检查报告"""
        # 统计调试工具风险等级
        debug_risk_stats = defaultdict(int)
        for debug_type in self.debug_detections.keys():
            debug_info = self.DEBUG_PATTERNS.get(debug_type, {})
            risk_level = debug_info.get('risk_level', 'low')
            debug_risk_stats[risk_level] += 1

        # 统计敏感日志风险等级
        log_risk_stats = defaultdict(int)
        for log_type in self.sensitive_log_detections.keys():
            log_info = self.SENSITIVE_LOG_PATTERNS.get(log_type, {})
            risk_level = log_info.get('risk_level', 'low')
            log_risk_stats[risk_level] += 1

        # 统计问题类型
        issue_stats = defaultdict(int)
        for issue in self.issues:
            issue_stats[issue['type']] += 1

        # 计算评分
        critical_issues = issue_stats.get('critical', 0)
        warning_issues = issue_stats.get('warning', 0)

        # 如果有严重的调试工具（vconsole, eruda, devtool），扣分更重
        high_risk_tools = len([
            t for t in self.debug_detections.keys()
            if self.DEBUG_PATTERNS.get(t, {}).get('risk_level') == 'high'
        ])

        if critical_issues == 0 and high_risk_tools == 0:
            score = max(100 - (warning_issues * 10), 0)
        else:
            score = max(100 - (critical_issues * 25) - (high_risk_tools * 20) - (warning_issues * 5), 0)

        return {
            'score': score,
            'debug_detections': dict(self.debug_detections),
            'sensitive_log_detections': dict(self.sensitive_log_detections),
            'issues': self.issues,
            'debug_risk_stats': dict(debug_risk_stats),
            'log_risk_stats': dict(log_risk_stats),
            'issue_stats': dict(issue_stats),
            'summary': {
                'total_debug_tools': len(self.debug_detections),
                'total_sensitive_logs': len(self.sensitive_log_detections),
                'high_risk_debug_tools': high_risk_tools,
                'critical_issues': critical_issues,
                'warning_issues': warning_issues,
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序动态调试风险检测报告")
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
    print(f"  - 动态调试工具种类: {summary['total_debug_tools']}")
    print(f"  - 高风险调试工具: {summary['high_risk_debug_tools']}")
    print(f"  - 敏感日志类型: {summary['total_sensitive_logs']}")
    print(f"  - 严重问题: {summary['critical_issues']}")
    print(f"  - 警告问题: {summary['warning_issues']}")

    # 动态调试工具检测结果
    if report['debug_detections']:
        print(f"\n🔍 动态调试工具检测结果:")
        for debug_type, detections in sorted(report['debug_detections'].items()):
            debug_info = DebugChecker.DEBUG_PATTERNS.get(debug_type, {})
            risk_level = debug_info.get('risk_level', 'low')
            risk_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk_level, '⚪')

            print(f"\n  {risk_emoji} {debug_info.get('name', debug_type)} (风险: {risk_level.upper()})")
            print(f"     检测次数: {len(detections)}")
            print(f"     描述: {debug_info.get('description', 'N/A')}")

            # 显示检测位置
            print(f"     检测位置:")
            for detection in detections[:3]:
                print(f"       - {detection['file']}:{detection['line']}")
            if len(detections) > 3:
                print(f"       ... 还有 {len(detections) - 3} 处")

    # 敏感日志检测结果
    if report['sensitive_log_detections']:
        print(f"\n🔒 敏感日志检测结果:")
        for log_type, detections in sorted(report['sensitive_log_detections'].items()):
            log_info = DebugChecker.SENSITIVE_LOG_PATTERNS.get(log_type, {})
            risk_level = log_info.get('risk_level', 'low')
            risk_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(risk_level, '⚪')

            print(f"\n  {risk_emoji} {log_info.get('name', log_type)} (风险: {risk_level.upper()})")
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
        for i, issue in enumerate(report['issues'], 1):
            type_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(issue['type'], '•')

            print(f"\n  {type_emoji} 问题 {i}: [{issue['type'].upper()}]")
            print(f"     类别: {issue['category']}")
            if 'tool' in issue:
                print(f"     工具: {issue['tool']}")
            if 'log_type' in issue:
                print(f"     日志类型: {issue['log_type']}")
            print(f"     位置: {issue['file']}:{issue['line']}")
            print(f"     描述: {issue['message']}")
            print(f"     建议: {issue['suggestion']}")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        import json as json_module
        with open(os.path.join(output_dir, 'debug_check.json'), 'w', encoding='utf-8') as f:
            json_module.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/debug_check.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'debug_check_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序动态调试风险检测报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"检测摘要:\n")
            f.write(f"  - 动态调试工具种类: {summary['total_debug_tools']}\n")
            f.write(f"  - 敏感日志类型: {summary['total_sensitive_logs']}\n\n")

            if report['issues']:
                f.write(f"风险问题 ({len(report['issues'])} 个):\n\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"{i}. [{issue['type'].upper()}] {issue['message']}\n")
                    f.write(f"   位置: {issue['file']}:{issue['line']}\n")
                    f.write(f"   建议: {issue['suggestion']}\n\n")

        print(f"[+] 文本报告已保存: {output_dir}/debug_check_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序动态调试风险检测工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    checker = DebugChecker(args.miniprogram_path)
    report = checker.check()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
