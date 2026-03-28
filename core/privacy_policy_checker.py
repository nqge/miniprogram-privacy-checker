#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私政策检查工具
基于：《网络安全标准实践指南-移动互联网应用程序（App）个人信息保护常见问题及处置指南》
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set
import argparse


class PrivacyPolicyChecker:
    """小程序隐私政策检查器"""

    # 必备条款（基于 TC260 指南）
    REQUIRED_CLAUSES = {
        'collect_purpose': {
            'name': '个人信息收集目的',
            'description': '说明收集个人信息的目的',
            'keywords': ['收集目的', '目的', '用于', '为了'],
            'required': True
        },
        'collect_method': {
            'name': '个人信息收集方式',
            'description': '说明收集个人信息的方式',
            'keywords': ['收集方式', '方式', '通过'],
            'required': True
        },
        'collect_scope': {
            'name': '个人信息收集范围',
            'description': '列出收集的个人信息类型',
            'keywords': ['收集范围', '范围', '信息类型', '包括'],
            'required': True
        },
        'storage_duration': {
            'name': '个人信息存储期限',
            'description': '说明信息存储多长时间',
            'keywords': ['存储期限', '保存期限', '期限', '保存'],
            'required': True
        },
        'use_rule': {
            'name': '个人信息使用规则',
            'description': '说明如何使用收集的信息',
            'keywords': ['使用规则', '使用', '规则', '处理'],
            'required': True
        },
        'third_party': {
            'name': '第三方服务说明',
            'description': '说明使用的第三方服务及其用途',
            'keywords': ['第三方', '第三方服务', '服务商', 'SDK'],
            'required': True
        },
        'user_rights': {
            'name': '用户权利说明',
            'description': '说明用户对个人信息的权利',
            'keywords': ['用户权利', '权利', '访问', '更正', '删除', '撤回同意'],
            'required': True
        },
        'delete_account': {
            'name': '信息注销方式',
            'description': '说明如何注销账户和删除信息',
            'keywords': ['注销', '删除账户', '删除信息', '注销账户'],
            'required': True
        },
        'contact_info': {
            'name': '联系方式',
            'description': '提供联系方式',
            'keywords': ['联系', '邮箱', '电话', '联系方式', '客服'],
            'required': True
        },
        'security_measures': {
            'name': '安全措施',
            'description': '说明采取的安全保护措施',
            'keywords': ['安全措施', '保护措施', '加密', '安全'],
            'required': False  # 推荐但非强制
        },
        'data_sharing': {
            'name': '信息共享规则',
            'description': '说明信息共享的规则和范围',
            'keywords': ['共享', '分享', '共享规则'],
            'required': False  # 推荐但非强制
        },
        'child_protection': {
            'name': '未成年人保护',
            'description': '说明对未成年人的保护措施',
            'keywords': ['未成年人', '儿童', '未满18周岁', '未成年'],
            'required': False  # 推荐但非强制
        },
    }

    # 常见的问题表述
    VAGUE_TERMS = [
        '为了更好的用户体验',
        '为了提供更好的服务',
        '为了优化',
        '可能包括',
        '等',
        '等数据',
        '等信息',
        '其他必要',
    ]

    # 常见的法律依据
    LEGAL_REFERENCES = [
        '个人信息保护法',
        '网络安全法',
        '数据安全法',
        '民法典',
        'GDPR',
    ]

    def __init__(self, miniprogram_path: str):
        """
        初始化隐私政策检查器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.privacy_policy_files = []
        self.privacy_policy_content = None
        self.missing_clauses = set()
        self.present_clauses = set()
        self.vague_statements = []
        self.issues = []

        # 查找隐私政策文件
        self._find_privacy_policy_files()

    def _find_privacy_policy_files(self):
        """查找隐私政策文件"""
        # 常见的隐私政策文件名
        policy_file_names = [
            'privacy.md',
            'privacy.txt',
            'privacy.html',
            '隐私政策.md',
            '隐私政策.txt',
            'privacy-policy.md',
            'privacy-policy.txt',
        ]

        # 查找根目录
        for file_name in policy_file_names:
            file_path = self.miniprogram_path / file_name
            if file_path.exists():
                self.privacy_policy_files.append(file_path)

        # 查找 pages 目录
        pages_dir = self.miniprogram_path / 'pages'
        if pages_dir.exists():
            for file_name in policy_file_names:
                file_path = pages_dir / file_name
                if file_path.exists():
                    self.privacy_policy_files.append(file_path)

        # 查找所有子目录
        for file_path in self.miniprogram_path.rglob("privacy*"):
            if file_path.is_file():
                self.privacy_policy_files.append(file_path)

        if self.privacy_policy_files:
            print(f"[+] 发现 {len(self.privacy_policy_files)} 个隐私政策文件:")
            for file in self.privacy_policy_files:
                print(f"  - {file}")
        else:
            print("[-] 未找到隐私政策文件")
            self.issues.append({
                'type': 'critical',
                'message': '未找到隐私政策文件',
                'suggestion': '请在小程序根目录或 pages 目录下创建隐私政策文件（如 privacy.md、隐私政策.txt）'
            })

    def check(self) -> Dict:
        """
        执行隐私政策检查

        Returns:
            检查结果字典
        """
        print("[*] 开始隐私政策检查...")

        if not self.privacy_policy_files:
            return self._generate_report()

        # 加载隐私政策内容
        print("\n[1/4] 加载隐私政策内容...")
        self._load_privacy_policy_content()

        if not self.privacy_policy_content:
            return self._generate_report()

        # 检查必备条款
        print("\n[2/4] 检查必备条款...")
        self._check_required_clauses()

        # 检查模糊表述
        print("\n[3/4] 检查模糊表述...")
        self._check_vague_statements()

        # 检查合规性
        print("\n[4/4] 检查合规性...")
        self._check_compliance()

        # 生成检查结果
        return self._generate_report()

    def _load_privacy_policy_content(self):
        """加载隐私政策内容"""
        # 加载第一个找到的隐私政策文件
        policy_file = self.privacy_policy_files[0]

        try:
            with open(policy_file, 'r', encoding='utf-8') as f:
                self.privacy_policy_content = f.read()
            print(f"[+] 成功加载隐私政策: {policy_file}")
            print(f"[+] 内容长度: {len(self.privacy_policy_content)} 字符")
        except Exception as e:
            print(f"[-] 读取隐私政策失败: {e}")
            self.issues.append({
                'type': 'critical',
                'message': f'无法读取隐私政策文件: {policy_file}',
                'suggestion': '请检查文件编码和权限'
            })

    def _check_required_clauses(self):
        """检查必备条款"""
        if not self.privacy_policy_content:
            return

        content = self.privacy_policy_content.lower()

        for clause_id, clause_info in self.REQUIRED_CLAUSES.items():
            # 检查是否包含该条款的关键词
            found = False
            matched_keywords = []

            for keyword in clause_info['keywords']:
                if keyword in content:
                    found = True
                    matched_keywords.append(keyword)

            if found:
                self.present_clauses.add(clause_id)
            elif clause_info['required']:
                self.missing_clauses.add(clause_id)
                self.issues.append({
                    'type': 'warning' if clause_id not in ['collect_purpose', 'collect_scope', 'contact_info'] else 'critical',
                    'message': f'缺少必备条款: {clause_info["name"]}',
                    'suggestion': f'请在隐私政策中补充"{clause_info["description"]}"的内容，建议包含关键词: {", ".join(clause_info["keywords"])}'
                })

        print(f"[+] 发现 {len(self.present_clauses)} 个条款")
        print(f"[-] 缺少 {len(self.missing_clauses)} 个必备条款")

    def _check_vague_statements(self):
        """检查模糊表述"""
        if not self.privacy_policy_content:
            return

        content = self.privacy_policy_content
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            for vague_term in self.VAGUE_TERMS:
                if vague_term in line_lower:
                    # 提取上下文
                    context_start = max(0, line_num - 1)
                    context_end = min(len(lines), line_num + 1)
                    context = '\n'.join(lines[context_start:context_end])

                    self.vague_statements.append({
                        'term': vague_term,
                        'line': line_num,
                        'context': context,
                        'full_line': line.strip()
                    })

                    # 如果模糊表述出现在关键条款中
                    if any(legal_ref in context.lower() for legal_ref in ['目的', '范围', '方式']):
                        self.issues.append({
                            'type': 'warning',
                            'message': f'发现模糊表述: "{vague_term}"',
                            'suggestion': '请使用更具体、明确的表述，避免使用模糊词汇',
                            'line': line_num,
                            'context': context
                        })
                    break  # 避免同一行重复记录

        if self.vague_statements:
            print(f"[+] 发现 {len(self.vague_statements)} 处模糊表述")
        else:
            print("[+] 未发现模糊表述")

    def _check_compliance(self):
        """检查合规性"""
        if not self.privacy_policy_content:
            return

        content = self.privacy_policy_content.lower()

        # 检查是否有法律依据
        has_legal_reference = any(ref in content for ref in self.LEGAL_REFERENCES)
        if not has_legal_reference:
            self.issues.append({
                'type': 'info',
                'message': '隐私政策中未引用法律依据',
                'suggestion': '建议引用《个人信息保护法》《网络安全法》等法律依据，增强政策权威性'
            })

        # 检查是否有更新日期
        has_update_date = any(keyword in content for keyword in ['更新日期', '生效日期', '最后更新', '生效时间'])
        if not has_update_date:
            self.issues.append({
                'type': 'warning',
                'message': '隐私政策中未标注更新日期或生效日期',
                'suggestion': '请在隐私政策中明确标注更新日期或生效日期，便于用户了解政策时效'
            })

        # 检查内容长度
        if len(self.privacy_policy_content) < 500:
            self.issues.append({
                'type': 'critical',
                'message': f'隐私政策内容过短（{len(self.privacy_policy_content)} 字符）',
                'suggestion': '隐私政策应详细、完整，建议不少于 500 字符'
            })
        elif len(self.privacy_policy_content) < 1000:
            self.issues.append({
                'type': 'warning',
                'message': f'隐私政策内容较短（{len(self.privacy_policy_content)} 字符）',
                'suggestion': '建议补充更多详细内容，使隐私政策更加完整'
            })

        # 检查是否有联系方式
        has_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', content)
        has_phone = re.search(r'1[3-9]\d{9}', content)

        if not has_email and not has_phone:
            self.issues.append({
                'type': 'critical',
                'message': '隐私政策中未提供有效的联系方式（邮箱或电话）',
                'suggestion': '请在隐私政策中提供有效的联系方式（邮箱或电话），便于用户咨询和反馈'
            })

    def _generate_report(self) -> Dict:
        """生成检查报告"""
        # 统计问题类型
        issue_stats = {}
        for issue in self.issues:
            issue_type = issue['type']
            issue_stats[issue_type] = issue_stats.get(issue_type, 0) + 1

        # 计算评分
        critical_issues = issue_stats.get('critical', 0)
        warning_issues = issue_stats.get('warning', 0)

        # 如果没有找到隐私政策文件，评分为 0
        if not self.privacy_policy_files:
            score = 0
        else:
            # 计算必备条款覆盖率
            required_clauses = [id for id, info in self.REQUIRED_CLAUSES.items() if info['required']]
            coverage = len(self.present_clauses & set(required_clauses)) / len(required_clauses)

            score = int(coverage * 60)  # 必备条款占 60 分
            score -= critical_issues * 20  # 严重问题扣 20 分
            score -= warning_issues * 10  # 警告问题问题扣 10 分
            score = max(score, 0)

        return {
            'score': score,
            'privacy_policy_files': [str(f) for f in self.privacy_policy_files],
            'present_clauses': list(self.present_clauses),
            'missing_clauses': list(self.missing_clauses),
            'vague_statements': self.vague_statements,
            'issues': self.issues,
            'issue_stats': issue_stats,
            'content_length': len(self.privacy_policy_content) if self.privacy_policy_content else 0,
            'summary': {
                'total_required_clauses': len([id for id, info in self.REQUIRED_CLAUSES.items() if info['required']]),
                'present_required_clauses': len(self.present_clauses),
                'missing_required_clauses': len(self.missing_clauses),
                'has_privacy_policy': len(self.privacy_policy_files) > 0,
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序隐私政策检查报告")
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
    print(f"  - 是否有隐私政策: {'是' if summary['has_privacy_policy'] else '否'}")
    if summary['has_privacy_policy']:
        print(f"  - 内容长度: {report['content_length']} 字符")
        print(f"  - 必备条款总数: {summary['total_required_clauses']}")
        print(f"  - 已包含条款: {summary['present_required_clauses']}")
        print(f"  - 缺失条款: {summary['missing_required_clauses']}")
        print(f"  - 严重问题: {report['issue_stats'].get('critical', 0)}")
        print(f"  - 警告问题: {report['issue_stats'].get('warning', 0)}")

    # 隐私政策文件
    if report['privacy_policy_files']:
        print(f"\n📄 隐私政策文件:")
        for file in report['privacy_policy_files']:
            print(f"  - {file}")

    # 缺失的条款
    if report['missing_clauses']:
        print(f"\n❌ 缺失的必备条款 ({len(report['missing_clauses'])} 个):")
        for clause_id in report['missing_clauses']:
            clause_info = PrivacyPolicyChecker.REQUIRED_CLAUSES.get(clause_id, {})
            print(f"  - {clause_info.get('name', clause_id)}")
            if 'description' in clause_info:
                print(f"    说明: {clause_info['description']}")
            if 'keywords' in clause_info:
                print(f"    建议关键词: {', '.join(clause_info['keywords'])}")

    # 已包含的条款
    if report['present_clauses']:
        print(f"\n✅ 已包含的条款 ({len(report['present_clauses'])} 个):")
        for clause_id in sorted(report['present_clauses']):
            clause_info = PrivacyPolicyChecker.REQUIRED_CLAUSES.get(clause_id, {})
            print(f"  - {clause_info.get('name', clause_id)}")

    # 模糊表述
    if report['vague_statements']:
        print(f"\n⚠️  模糊表述 ({len(report['vague_statements'])} 处):")
        for statement in report['vague_statements'][:5]:
            print(f"  • 行 {statement['line']}: {statement['term']}")
            print(f"    {statement['full_line'][:80]}...")
        if len(report['vague_statements']) > 5:
            print(f"  ... 还有 {len(report['vague_statements']) - 5} 处")

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
            print(f"     描述: {issue['message']}")
            print(f"     建议: {issue['suggestion']}")
            if 'line' in issue:
                print(f"     行号: {issue['line']}")

    # 保存报告
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        import json
        with open(os.path.join(output_dir, 'privacy_policy_check.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/privacy_policy_check.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'privacy_policy_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序隐私政策检查报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"检查摘要:\n")
            f.write(f"  - 是否有隐私政策: {'是' if summary['has_privacy_policy'] else '否'}\n")
            if summary['has_privacy_policy']:
                f.write(f"  - 内容长度: {report['content_length']} 字符\n")
                f.write(f"  - 必备条款总数: {summary['total_required_clauses']}\n")
                f.write(f"  - 已包含条款: {summary['present_required_clauses']}\n")
                f.write(f"  - 缺失条款: {summary['missing_required_clauses']}\n\n")

            if report['missing_clauses']:
                f.write("缺失的必备条款:\n")
                for clause_id in report['missing_clauses']:
                    clause_info = PrivacyPolicyChecker.REQUIRED_CLAUSES.get(clause_id, {})
                    f.write(f"  - {clause_info.get('name', clause_id)}\n")
                f.write("\n")

            if report['issues']:
                f.write(f"合规问题 ({len(report['issues'])} 个):\n\n")
                for i, issue in enumerate(report['issues'], 1):
                    f.write(f"{i}. [{issue['type'].upper()}] {issue['message']}\n")
                    f.write(f"   建议: {issue['suggestion']}\n\n")

        print(f"[+] 文本报告已保存: {output_dir}/privacy_policy_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序隐私政策检查工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    checker = PrivacyPolicyChecker(args.miniprogram_path)
    report = checker.check()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
