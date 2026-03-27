#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私合规报告生成器
整合所有检查结果，生成综合合规报告
"""

import os
import json
from pathlib import Path
from typing import Dict
from datetime import datetime
import argparse


class ReportGenerator:
    """小程序隐私合规报告生成器"""

    def __init__(self, report_dir: str = 'privacy_check_results'):
        """
        初始化报告生成器

        Args:
            report_dir: 检查结果目录
        """
        self.report_dir = Path(report_dir)
        self.permission_report = None
        self.api_report = None
        self.dataflow_report = None
        self.privacy_policy_report = None

    def load_reports(self):
        """加载所有检查报告"""
        print("[*] 加载检查报告...")

        # 加载权限检查报告
        perm_report_path = self.report_dir / 'permission_check.json'
        if perm_report_path.exists():
            with open(perm_report_path, 'r', encoding='utf-8') as f:
                self.permission_report = json.load(f)
            print(f"[+] 加载权限检查报告")

        # 加载 API 扫描报告
        api_report_path = self.report_dir / 'api_scan.json'
        if api_report_path.exists():
            with open(api_report_path, 'r', encoding='utf-8') as f:
                self.api_report = json.load(f)
            print(f"[+] 加载 API 扫描报告")

        # 加载数据流分析报告
        dataflow_report_path = self.report_dir / 'dataflow_analysis.json'
        if dataflow_report_path.exists():
            with open(dataflow_report_path, 'r', encoding='utf-8') as f:
                self.dataflow_report = json.load(f)
            print(f"[+] 加载数据流分析报告")

        # 加载隐私政策检查报告
        policy_report_path = self.report_dir / 'privacy_policy_check.json'
        if policy_report_path.exists():
            with open(policy_report_path, 'r', encoding='utf-8') as f:
                self.privacy_policy_report = json.load(f)
            print(f"[+] 加载隐私政策检查报告")

    def generate(self) -> Dict:
        """生成综合合规报告"""
        print("[*] 生成综合合规报告...")

        # 计算总体评分
        overall_score = self._calculate_overall_score()

        # 收集所有问题
        all_issues = self._collect_all_issues()

        # 生成修复建议
        recommendations = self._generate_recommendations()

        # 生成报告
        report = {
            'overall_score': overall_score,
            'permission_score': self.permission_report['score'] if self.permission_report else 0,
            'api_score': self.api_report['score'] if self.api_report else 0,
            'dataflow_score': self.dataflow_report['score'] if self.dataflow_report else 0,
            'privacy_policy_score': self.privacy_policy_report['score'] if self.privacy_policy_report else 0,
            'all_issues': all_issues,
            'recommendations': recommendations,
            'summary': self._generate_summary(all_issues),
            'timestamp': datetime.now().isoformat()
        }

        return report

    def _calculate_overall_score(self) -> int:
        """计算总体评分"""
        scores = []

        if self.permission_report:
            scores.append(self.permission_report['score'])

        if self.api_report:
            scores.append(self.api_report['score'])

        if self.dataflow_report:
            scores.append(self.dataflow_report['score'])

        if self.privacy_policy_report:
            scores.append(self.privacy_policy_report['score'])

        if not scores:
            return 0

        # 加权平均
        weights = {
            'permission': 0.25,
            'api': 0.25,
            'dataflow': 0.25,
            'privacy_policy': 0.35
        }

        weighted_sum = 0
        total_weight = 0

        if self.permission_report:
            weighted_sum += self.permission_report['score'] * weights['permission']
            total_weight += weights['permission']

        if self.api_report:
            weighted_sum += self.api_report['score'] * weights['api']
            total_weight += weights['api']

        if self.dataflow_report:
            weighted_sum += self.dataflow_report['score'] * weights['dataflow']
            total_weight += weights['dataflow']

        if self.privacy_policy_report:
            weighted_sum += self.privacy_policy_report['score'] * weights['privacy_policy']
            total_weight += weights['privacy_policy']

        return int(weighted_sum / total_weight) if total_weight > 0 else 0

    def _collect_all_issues(self) -> list:
        """收集所有问题"""
        all_issues = []

        # 权限检查问题
        if self.permission_report and 'issues' in self.permission_report:
            for issue in self.permission_report['issues']:
                all_issues.append({
                    **issue,
                    'category': '权限声明',
                    'priority': 'high' if issue['type'] == 'critical' else 'medium'
                })

        # API 扫描问题
        if self.api_report and 'issues' in self.api_report:
            for issue in self.api_report['issues']:
                all_issues.append({
                    **issue,
                    'category': '敏感API',
                    'priority': 'high' if issue['type'] == 'critical' else 'medium'
                })

        # 数据流分析问题
        if self.dataflow_report and 'issues' in self.dataflow_report:
            for issue in self.dataflow_report['issues']:
                all_issues.append({
                    **issue,
                    'category': '数据流',
                    'priority': 'high' if issue['type'] == 'critical' else 'medium'
                })

        # 隐私政策问题
        if self.privacy_policy_report and 'issues' in self.privacy_policy_report:
            for issue in self.privacy_policy_report['issues']:
                all_issues.append({
                    **issue,
                    'category': '隐私政策',
                    'priority': 'high' if issue['type'] == 'critical' else 'medium'
                })

        # 按优先级和类型排序
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        type_order = {'critical': 0, 'warning': 1, 'info': 2}

        all_issues.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'low'), 2),
            type_order.get(x.get('type', 'info'), 2)
        ))

        return all_issues

    def _generate_recommendations(self) -> list:
        """生成修复建议"""
        recommendations = []

        # 检查缺失的权限声明
        if self.permission_report and 'missing_permissions' in self.permission_report:
            if self.permission_report['missing_permissions']:
                recommendations.append({
                    'priority': 'critical',
                    'title': '补充权限声明',
                    'description': '在 app.json 中添加缺失的权限声明',
                    'details': self.permission_report['missing_permissions'],
                    'action': '在 app.json 的 permission 字段中添加以下权限声明'
                })

        # 检查已废弃的 API
        if self.api_report and 'api_calls' in self.api_report:
            deprecated_apis = []
            for api_name in self.api_report['api_calls'].keys():
                from core.api_scanner import APIScanner
                api_info = APIScanner.SENSITIVE_APIS.get(api_name, {})
                if api_info.get('deprecated'):
                    deprecated_apis.append(api_name)

            if deprecated_apis:
                recommendations.append({
                    'priority': 'critical',
                    'title': '替换已废弃的 API',
                    'description': '使用已废弃的 API 会导致审核不通过',
                    'details': deprecated_apis,
                    'action': '将已废弃的 API 替换为新的 API'
                })

        # 检查 HTTP 传输
        if self.dataflow_report and 'data_transmission_points' in self.dataflow_report:
            http_transmissions = [
                t for t in self.dataflow_report['data_transmission_points']
                if t.get('uses_http')
            ]

            if http_transmissions:
                recommendations.append({
                    'priority': 'critical',
                    'title': '使用 HTTPS 替代 HTTP',
                    'description': 'HTTP 协议存在中间人攻击风险，不符合隐私合规要求',
                    'details': f'发现 {len(http_transmissions)} 处 HTTP 传输',
                    'action': '将所有 HTTP 请求改为 HTTPS'
                })

        # 检查隐私政策
        if self.privacy_policy_report:
            if not self.privacy_policy_report.get('privacy_policy_files'):
                recommendations.append({
                    'priority': 'critical',
                    'title': '创建隐私政策文件',
                    'description': '小程序必须提供隐私政策文档',
                    'details': [],
                    'action': '在根目录或 pages 目录下创建 privacy.md 或隐私政策.txt'
                })
            elif self.privacy_policy_report.get('missing_clauses'):
                recommendations.append({
                    'priority': 'high',
                    'title': '完善隐私政策内容',
                    'description': '隐私政策缺少必备条款',
                    'details': self.privacy_policy_report['missing_clauses'],
                    'action': '补充缺失的必备条款'
                })

        # 按优先级排序
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))

        return recommendations

    def _generate_summary(self, all_issues: list) -> dict:
        """生成摘要"""
        # 统计问题
        issue_stats = {
            'critical': len([i for i in all_issues if i.get('type') == 'critical']),
            'warning': len([i for i in all_issues if i.get('type') == 'warning']),
            'info': len([i for i in all_issues if i.get('type') == 'info'])
        }

        # 统计类别
        category_stats = {}
        for issue in all_issues:
            category = issue.get('category', '其他')
            category_stats[category] = category_stats.get(category, 0) + 1

        return {
            'total_issues': len(all_issues),
            'issue_stats': issue_stats,
            'category_stats': category_stats,
            'has_critical_issues': issue_stats['critical'] > 0,
            'has_warning_issues': issue_stats['warning'] > 0
        }

    def save_markdown_report(self, report: Dict, output_file: str = 'privacy_compliance_report.md'):
        """保存 Markdown 格式报告"""
        print(f"[*] 生成 Markdown 报告...")

        with open(output_file, 'w', encoding='utf-8') as f:
            # 标题
            f.write("# 小程序隐私合规检查报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # 总体评分
            score = report['overall_score']
            f.write("## 📊 总体评分\n\n")
            f.write(f"**合规评分**: {score}/100  \n\n")

            if score >= 90:
                grade = "⭐⭐⭐⭐⭐ 优秀"
                status = "✅ 合规性很高，审核通过概率大"
            elif score >= 70:
                grade = "⭐⭐⭐⭐ 良好"
                status = "⚠️ 整体合规，有少量需要改进"
            elif score >= 50:
                grade = "⭐⭐⭐ 一般"
                status = "⚠️ 存在一些风险，需要修复"
            elif score >= 30:
                grade = "⭐⭐ 较差"
                status = "🚨 存在较多问题，审核可能不通过"
            else:
                grade = "⭐ 极差"
                status = "🚨 严重违规，审核大概率不通过"

            f.write(f"**评级**: {grade}  \n")
            f.write(f"**状态**: {status}  \n\n")

            # 各项评分
            f.write("### 分项评分\n\n")
            f.write("| 检查项 | 评分 |\n")
            f.write("|--------|------|\n")

            if self.permission_report:
                perm_score = report['permission_score']
                perm_grade = "✅" if perm_score >= 80 else ("⚠️" if perm_score >= 60 else "🚨")
                f.write(f"| 权限声明检查 | {perm_score}/100 {perm_grade} |\n")

            if self.api_report:
                api_score = report['api_score']
                api_grade = "✅" if api_score >= 80 else ("⚠️" if api_score >= 60 else "🚨")
                f.write(f"| 敏感 API 扫描 | {api_score}/100 {api_grade} |\n")

            if self.dataflow_report:
                df_score = report['dataflow_score']
                df_grade = "✅" if df_score >= 80 else ("⚠️" if df_score >= 60 else "🚨")
                f.write(f"| 数据流分析 | {df_score}/100 {df_grade} |\n")

            if self.privacy_policy_report:
                pp_score = report['privacy_policy_score']
                pp_grade = "✅" if pp_score >= 80 else ("⚠️" if pp_score >= 60 else "🚨")
                f.write(f"| 隐私政策检查 | {pp_score}/100 {pp_grade} |\n")

            f.write("\n")

            # 检查摘要
            summary = report['summary']
            f.write("## 📋 检查摘要\n\n")
            f.write(f"- **总问题数**: {summary['total_issues']}  \n")
            f.write(f"- **严重问题**: {summary['issue_stats']['critical']}  \n")
            f.write(f"- **警告问题**: {summary['issue_stats']['warning']}  \n")
            f.write(f"- **提示信息**: {summary['issue_stats']['info']}  \n\n")

            if summary['category_stats']:
                f.write("### 问题分布\n\n")
                f.write("| 类别 | 问题数 |\n")
                f.write("|------|--------|\n")
                for category, count in sorted(summary['category_stats'].items(), key=lambda x: -x[1]):
                    f.write(f"| {category} | {count} |\n")
                f.write("\n")

            # 详细问题列表
            if report['all_issues']:
                f.write("## 🔍 详细问题列表\n\n")

                critical_issues = [i for i in report['all_issues'] if i.get('type') == 'critical']
                warning_issues = [i for i in report['all_issues'] if i.get('type') == 'warning']
                info_issues = [i for i in report['all_issues'] if i.get('type') == 'info']

                if critical_issues:
                    f.write("### 🚨 严重问题\n\n")
                    for i, issue in enumerate(critical_issues, 1):
                        f.fwrite(f"{i}. **{issue.get('category', '未知')}**  \n")
                        f.write(f"   - **描述**: {issue.get('message', '无描述')}  \n")
                        f.write(f"   - **建议**: {issue.get('suggestion', '无建议')}  \n")
                        if issue.get('file'):
                            f.write(f"   - **位置**: {issue['file']}:{issue.get('line', '?')}  \n")
                        f.write("\n")

                if warning_issues:
                    f.write("### ⚠️ 警告问题\n\n")
                    for i, issue in enumerate(warning_issues, 1):
                        f.write(f"{i}. **{issue.get('category', '未知')}**  \n")
                        f.write(f"   - **描述**: {issue.get('message', '无描述')}  \n")
                        f.write(f"   - **建议**: {issue.get('suggestion', '无建议')}  \n")
                        if issue.get('file'):
                            f.write(f"   - **位置**: {issue['file']}:{issue.get('line', '?')}  \n")
                        f.write("\n")

                if info_issues:
                    f.write("### ℹ️ 提示信息\n\n")
                    for i, issue in enumerate(info_issues, 1):
                        f.write(f"{i}. **{issue.get('category', '未知')}**  \n")
                        f.write(f"   - **描述**: {issue.get('message', '无描述')}  \n")
                        f.write(f"   - **建议**: {issue.get('suggestion', '无建议')}  \n")
                        if issue.get('file'):
                            f.write(f"   - **位置**: {issue['file']}:{issue.get('line', '?')}  \n")
                        f.write("\n")

            # 修复建议
            if report['recommendations']:
                f.write("## 💡 修复建议\n\n")

                # 按优先级分组
                critical_recs = [r for r in report['recommendations'] if r.get('priority') == 'critical']
                high_recs = [r for r in report['recommendations'] if r.get('priority') == 'high']
                medium_recs = [r for r in report['recommendations'] if r.get('priority') == 'medium']

                if critical_recs:
                    f.write("### 🚨 紧急修复（可能导致审核不通过）\n\n")
                    for i, rec in enumerate(critical_recs, 1):
                        f.write(f"{i}. **{rec['title']}**  \n")
                        f.write(f"   - **描述**: {rec['description']}  \n")
                        f.write(f"   - **操作**: {rec['action']}  \n")
                        if rec.get('details'):
                            f.write(f"   - **详情**: {rec['details']}  \n")
                        f.write("\n")

                if high_recs:
                    f.write("### ⚠️ 重要修复（建议尽快修复）\n\n")
                    for i, rec in enumerate(high_recs, 1):
                        f.write(f"{i}. **{rec['title']}**  \n")
                        f.write(f"   - **描述**: {rec['description']}  \n")
                        f.write(f"   - **操作**: {rec['action']}  \n")
                        if rec.get('details'):
                            f.write(f"   - **详情**: {rec['details']}  \n")
                        f.write("\n")

                if medium_recs:
                    f.write("### 💡 建议优化（可选）\n\n")
                    for i, rec in enumerate(medium_recs, 1):
                        f.write(f"{i}. **{rec['title']}**  \n")
                        f.write(f"   - **描述**: {rec['description']}  \n")
                        f.write(f"   - **操作**: {rec['action']}  \n")
                        if rec.get('details'):
                            f.write(f"   - **详情**: {rec['details']}  \n")
                        f.write("\n")

            # 免责声明
            f.write("---\n\n")
            f.write("## 📌 免责声明\n\n")
            f.write("本报告由小程序隐私合规检查工具自动生成，仅供参考。  \n")
            f.write("实际的合规性评估应以微信平台的审核结果为准。  \n")
            f.write("建议在提交审核前，仔细检查并修复所有严重问题。  \n\n")

        print(f"[+] Markdown 报告已保存: {output_file}")

    def print_summary(self, report: Dict):
        """打印报告摘要"""
        print("\n" + "="*70)
        print("小程序隐私合规检查 - 综合报告")
        print("="*70)

        score = report['overall_score']
        print(f"\n📊 总体评分: {score}/100")

        if score >= 90:
            print("评级: ⭐⭐⭐⭐⭐ 优秀")
            print("状态: ✅ 合规性很高，审核通过概率大")
        elif score >= 70:
            print("评级: ⭐⭐⭐⭐ 良好")
            print("状态: ⚠️ 整体合规，有少量需要改进")
        elif score >= 50:
            print("评级: ⭐⭐⭐ 一般")
            print("状态: ⚠️ 存在一些风险，需要修复")
        elif score >= 30:
            print("评级: ⭐⭐ 较差")
            print("状态: 🚨 存在较多问题，审核可能不通过")
        else:
            print("评级: ⭐ 极差")
            print("状态: 🚨 严重违规，审核大概率不通过")

        summary = report['summary']
        print(f"\n📋 问题汇总:")
        print(f"  - 总问题数: {summary['total_issues']}")
        print(f"  - 严重问题: {summary['issue_stats']['critical']}")
        print(f"  - 警告问题: {summary['issue_stats']['warning']}")
        print(f"  - 提示信息: {summary['issue_stats']['info']}")

        if report['recommendations']:
            print(f"\n💡 修复建议: {len(report['recommendations'])} 条")
            critical_count = len([r for r in report['recommendations'] if r.get('priority') == 'critical'])
            if critical_count > 0:
                print(f"  ⚠️  其中 {critical_count} 条为紧急修复项")


def main():
    parser = argparse.ArgumentParser(description='小程序隐私合规报告生成器')
    parser.add_argument('-r', '--report-dir', help='检查结果目录', default='privacy_check_results')
    parser.add_argument('-o', '--output', help='报告输出文件', default='privacy_compliance_report.md')
    args = parser.parse_args()

    generator = ReportGenerator(args.report_dir)
    generator.load_reports()
    report = generator.generate()
    generator.print_summary(report)
    generator.save_markdown_report(report(report, args.output))


if __name__ == '__main__':
    main()
