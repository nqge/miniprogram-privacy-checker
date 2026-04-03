#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私政策命名检查工具
基于：《网络安全标准实践指南》隐私政策命名规范
"""

import os
import re
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import argparse


class PrivacyNamingChecker:
    """小程序隐私政策命名检查器"""

    # 隐荐的隐私政策文件名
    RECOMMENDED_FILENAMES = [
        'privacy.md',
        'privacy.txt',
        '隐私政策.md',
        '隐私政策.txt',
        'Privacy Policy.md',
        'PRIVACY_POLICY.md',
    ]

    # 不应该使用的文件名
    NOT_RECOMMENDED_FILENAMES = [
        'privacy.txt',  # 太简单
        'policy.md',   # 太简单，容易与其他文件混淆
        'terms.md',    # 条款，不是隐私政策
        'agreement.md', # 协议，不是隐私政策
    ]

    # 常见的模糊或不规范的文件名
    VAGUE_NAMES = [
        'privacy', 'policies', 'policy', 'priv', 'privs',
        'agreement', 'terms',
    ]

    def __init__(self, miniprogram_path: str):
        """
        初始化隐私政策命名检查器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.privacy_policy_files = []
        self.issues = []

        # 查找隐私政策文件
        self._find_privacy_policy_files()

    def _find_privacy_policy_files(self):
        """查找隐私政策文件"""
        print(f"[*] 查找隐私政策文件...")

        # 查找根目录
        for filename in self.miniprogram_path.glob('*.md'):
            self.privacy_policy_files.append({
                'file': filename,
                'location': '根目录',
                'path': str(filename)
            })

        # 查找 pages 目录
        pages_dir = self.miniprogram_path / 'pages'
        if pages_dir.exists():
            for filename in pages_dir.glob('*.md'):
                self.privacy_policy_policy_files.append({
                    'file': filename,
                    'location': 'pages 目录',
                    'path': str(filename)
                })

        # 查找 utils 目录
        utils_dir = self.miniprogram_path / 'utils'
        if utils_dir.exists():
            for filename in utils_dir.glob('*.md'):
                self.privacy_policy_policy_files.append({
                    'file': filename,
                    'location': 'utils 目录',
                    'path': str(filename)
                })

        # 查找所有子目录
        for subdir in self.miniprogram_path.rglob('*/'):
            if subdir.is_dir():
                for filename in subdir.glob('*.md'):
                    self.privacy_policy_files.append({
                        'file': filename,
                        'location': f'{subdir.name}/',
                        'path': str(filename)
                    })

        print(f"[+] 发现 {len(self.privacy_policy_files)} 个可能的隐私政策文件")

    def check(self) -> Dict:
        """
        执行隐私政策命名检查

        Returns:
            检查查结果字典
        """
        print("[*] 开始隐私政策命名检查...")

        # 1. 检查是否找到隐私政策文件
        if not self.privacy_policy_files:
            self.issues.append({
                'type': 'critical',
                'message': '未找到隐私政策文件',
                'suggestion': '请在小程序根目录或 pages 目录下创建隐私政策文件（如 privacy.md）'
            })
            return self._generate_report()

        # 2. 检查文件命名
        print("\n[2/5] 检查文件命名...")
        self._check_file_naming()

        # 3. 检查文件内容
        print("\n[3/5] 检查文件内容...")
        self._check_file_contents()

        # 4. 检查文件可访问性
        print("\n[4/5] 检查文件可访问性...")
        self._check_file_accessibility()

        # 5. 生成检查报告
        print("\n[5/5] 生成检查报告...")
        return self._generate_report()

    def _check_file_naming(self):
        """检查文件命名合规性"""
        for file_info in self.privacy_policy_files:
            filename = file_info['file']
            file_path = file_info['path']

            # 检查是否使用推荐名称
            if filename not in self.RECOMMENDED_FILENAMES:
                self.issues.append({
                    'type': 'warning',
                    'category': '文件命名',
                    'file': str(file_info['path'].relative_to(self.miniprogram_path)),
                    'line': 1,
                    'message': f'隐私政策文件名不符合推荐规范',
                    'suggestion': f'建议使用推荐名称: privacy.md',
                    'code_snippet': filename
                })

            # 检查是否使用了不推荐的名称
            if filename in self.NOT_RECOMMENDED_FILENAMES:
                self.issues.append({
                    'type': 'warning',
                    'category': '文件命名',
                    'file': str(file_info['path'].relative_to(self.miniprogram_path)),
                    'line': 1,
                    'message': f'隐私政策文件名过于简单，容易与其他文件混淆',
                    'suggestion': f'建议使用更明确的文件名',
                    'code_snippet': filename
                })

            # 检查文件名是否包含模糊或不规范词汇
            base_name = filename.lower().replace('.md', '').replace('_', '').replace('-', '')
            for vague_term in self.VAGUE_NAMES:
                if vague_term in base_name and len(base_name) > 3:
                    self.issues.append({
                        'type': 'info',
                        'category': '文件命名',
                        'file': str(file_info['path'].relative_to(self.miniprogram_path)),
                        'line': 1,
                        'message': f'文件名包含模糊词汇: {vague_term}',
                        'suggestion': f'建议使用更明确的命名',
                        'code_snippet': filename
                    })
                    break

    def _check_file_contents(self):
        """检查隐私政策文件内容"""
        for file_info in self.privacy_policy_files:
            file_path = file_info['path']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检查文件是否包含必备条款
                has_required_clauses = False
                required_clauses_found = []

                # 基本必备条款
                basic_clauses = [
                    '收集目的',
                    '收集方式',
                    '收集范围',
                    '使用规则',
                    '存储期限',
                    '联系方式',
                ]

                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    for clause in basic_clauses:
                        if clause in line_lower:
                            has_required_clauses = True
                            required_clauses_found.append(clause)
                            break

                    # 检查文件是否包含法律依据
                    has_legal_references = False
                    legal_refs = [
                        '个人信息保护法',
                        '网络安全法',
                        '数据安全法',
                        'GDPR',
                        '民法典',
                    ]

                    for ref in legal_refs:
                        if ref in line:
                            has_legal_references = True
                            break

                # 检查文件长度
                if len(lines) < 50:
                    self.issues.append({
                        'type': 'warning',
                        'category': '内容完整性',
                        'file': str(file_path.relative_to(self.miniprogram_path)),
                        'line': 1,
                        'message': f'隐私政策文件内容过短（{len(lines)} 行）',
                        'suggestion': '建议补充更多详细内容，建议不少于 100 行',
                        'code_snippet': f'共 {len(lines)} 行'
                    })

                # 检查必备条款
                if not has_required_clauses:
                    missing_clauses = [c for c in basic_clauses if c not in required_clauses_found]
                    self.issues.append({
                        'type': 'critical',
                        'category': '必备条款',
                        'file': str(file_path.relative_to(self.miniprogram)),
                        'line': 1,
                        'message': f'隐私政策文件缺少必备条款: {", ".join(missing_clauses)}',
                        'suggestion': '请补充基本的隐私政策必备条款',
                        'code_snippet': lines[:10] if lines else ''
                    })

                # 检查法律依据
                if not has_legal_references:
                    self.issues.append({
                        'type': 'warning',
                        'category': '法律依据',
                        'file': str(file_path.relative_to(self.miniprogram_path)),
                        'line': 1,
                        'message': '隐私政策文件未引用法律依据',
                        'suggestion': '建议引用《个人信息保护法》《网络安全法》等法律依据增强政策权威性',
                        'code_snippet': lines[:10] if lines else ''
                    })

            except Exception as e:
                print(f"[-] 读取文件失败 {file_path}: {e}")

    def _check_file_accessibility(self):
        """检查隐私政策文件是否在小程序中可访问"""
        for file_info in self.privacy_policy_files:
            file_path = file_info['path']
            relative_path = str(file_path.relative_to(self.miniprogram_path))

            # 检查是否在 pages 目录下
            in_pages = file_info['location'] == 'pages 目录'

            # 检查 app.json 是否引用了隐私政策
            app_json = self.miniprogram_path / 'app.json'
            if app_json.exists():
                try:
                    with open(app_json, 'r', encoding='utf-8') as f:
                        app_config = json.load(f)

                    # 检查页面配置
                    if 'pages' in app_config:
                        for page_name, page_config in app_config['pages'].items():
                            if isinstance(page_config, dict):
                                if 'path' in page_config:
                                    page_path = page_config['path']
                                    if 'privacy' in page_path.lower():
                                        self.issues.append({
                                            'type': 'info',
                                            'category': '文件配置',
                                            'file': relative_path,
                                            'line': 1,
                                            'message': f'在 app.json 的 {page_name} 页面配置中引用了隐私政策',
                                            'suggestion': '配置正确，确保隐私政策可在用户主动触发时显示'
                                        })

                    # 检查 tabBar
                    if 'tabBar' in app_config:
                        tabbar = app_config['tabBar']
                        if 'page_path' in tabbar.get('list', []):
                            self.issues.append({
                                'type': 'info',
                                'category': '文件配置',
                                'file': relative_path,
                                'line': 1,
                                'message': f'在 tabBar.list 中配置了隐私政策入口',
                                'suggestion': '配置正确，确保隐私政策可被用户访问'
                            })

                except Exception as e:
                    print(f"[-] 读取 app.json 失败: {e}")

    def _generate_report(self) -> Dict:
        """生成检查报告"""
        # 统计问题类型
        issue_stats = defaultdict(int)
        for issue in self.issues:
            issue_stats[issue['type']] += 1

        # 计算评分
        critical_issues = issue_stats.get('critical', 0)
        warning_issues = issue_stats.get('warning', 0)
        info_issues = issue_stats.get('info', 0)

        if critical_issues == 0 and warning_issues == 0:
            score = 100
        elif critical_issues > 0:
            score = max(100 - (critical_issues * 30) - (warning_issues * 5), 0)
        else:
            score = max(100 - (critical_issues * 20) - (warning_issues * 10), 0)

        return {
            'score': score,
            'privacy_policy_files': [
                {
                    'file': str(f['file'].relative_to(self.miniprogram_path)),
                    'location': f['location']
                } for f in self.privacy_policy_files
            ],
            'issues': self.issues,
            'issue_stats': dict(issue_stats),
            'summary': {
                'total_policy_files': len(self.privacy_policy_files),
                'recommended_files_found': len([
                    f for f in self.privacy_policy_files
                    if f['file'].name in self.RECOMMENDED_FILENAMES
                ]),
                'vague_naming_files': len([
                    f for f in self.privacy_policy_policy_files
                    if f['file'].name in self.VAGUE_NAMES
                ]),
                'total_issues': len(self.issues),
                'critical_issues': critical_issues,
                'warning_issues': warning_issues,
                'info_issues': info_issues,
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序隐私政策命名检查报告")
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
    print("\n📋 检查摘要:")
    print(f"  - 隐私政策文件数: {summary['total_policy_files']}")
    print(f"  - 使用推荐命名: {summary['recommended_files_found']}")
    print(f"  - 模糊命名: {summary['vague_naming_files']}")
    print(f"  - 总问题数: {summary['total_issues']}")
    print(f"  - 严重问题: {summary['critical_issues']}")
    print(f"  - 警告问题: {summary['warning_issues']}")
    print(f"  - 提示信息: {summary['info_issues']}")

    # 隐私政策文件
    if report['privacy_policy_files']:
        print(f"\n📄 隐私政策文件 ({len(report['privacy_policy_files'])} 个):")
        for file_info in report['privacy_policy_files']:
            print(f"  • {file_info['file']}")
            print(f"    位置: {file_info['location']}")

    # 问题列表
    if report['issues']:
        print(f"\n🚨  问题列表 ({len(report['issues'])} 个):")
        for i, issue in enumerate(report['issues'][:10], 1):
            type_emoji = {
                'critical': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(issue['type'], '•')

            print(f"\n  {type_emoji} 问题 {i}: [{issue['type'].upper()}]")
            print(f"     类别: {issue.get('category', 'N/A')}")
            print(f"     文件: {issue.get('file', 'N/A')}")

            if 'line' in issue:
                print(f"     行号: {issue['line']}")
            print(f"     描述: {issue['message']}")
            print(f"     建议: {issue['suggestion']}")

            if 'code_snippet' in issue:
                code = issue['code_snippet']
                print(f"     代码: {code[:80]}...")
                if len(code) > 80:
                    print(f"     ... 还有 {len(code) - 80} 字节")

        if len(report['issues']) > 10:
            print(f"\n  ... 还有 {len(report['issues']) - 10} 个问题")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        import json
        with open(os.path.join(output_dir, 'privacy_naming_check.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/privacy_naming_check.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'privacy_naming_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序隐私政策命名检查报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"检查摘要:\n")
            f.write(f"  - 隐私政策文件数: {summary['total_policy_files']}\n")
            f.write(f"  - 使用推荐命名: {summary['recommended_files_found']}\n")
            f.write(f" - 模糊命名: {summary['vague_naming_files']}\n")
            f.write(f" - 总问题数: {summary['total_issues']}\n")
            f.write(f"  - 严重问题: {summary['critical_issues']}\n")
            f.write(f"  - 警告问题: {summary['warning_issues']}\n\n")

            if report['privacy_policy_files']:
                f.write("隐私政策文件:\n")
                for file_info in report['privacy_policy_files']:
                    f.write(f"  • {file_info['file']}\n")

            if report['issues']:
                f.write(f"\n问题列表:\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"{i}. [{issue['type'].upper()}] {issue.get('message')}\n")
                    if 'file' in issue:
                        f.write(f"   文件: {issue.get('file')}\n")
                    f.write(f"   建议: {issue.get('suggestion')}\n")

        print(f"\n[+] 文本报告已保存: {output_dir}/privacy_naming_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序隐私政策命名检查工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    checker = PrivacyNamingChecker(args.miniprogram_path)
    report = checker.check()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
