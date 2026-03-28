#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私合规检查综合报告生成器（修复版）
生成简洁的概要视图报告，包含权限确认单和自评估表
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SummaryReportGenerator:
    """小程序隐私合规检查综合报告生成器"""

    def __init__(self):
        """初始化报告生成器"""

    def load_all_reports(self, results_dir: str) -> Dict:
        """加载所有检查报告"""
        reports = {}

        try:
            results_path = Path(results_dir)

            # 加载权限声明检查报告
            perm_report_path = results_path / 'permission_check.json'
            if perm_report_path.exists():
                with open(perm_report_path, 'r', encoding='utf-8') as f:
                    reports['permission'] = json.load(f)

            # 加载敏感 API 扫描报告
            api_report_path = results_path / 'api_scan.json'
            if api_report_path.exists():
                with open(api_report_path, 'r', encoding='utf-8') as f:
                    reports['api'] = json.load(f)

            # 加载数据流分析报告
            dataflow_report_path = results_path / 'dataflow_analysis.json'
            if dataflow_report_path.exists():
                with open(dataflow_report_path, 'r', encoding='utf-8') as f:
                    reports['dataflow'] = json.load(f)

            # 加载隐私政策检查报告
            privacy_policy_report_path = results_path / 'privacy_policy_check.json'
            if privacy_policy_report_path.exists():
                with open(privacy_policy_report_path, 'r', encoding='utf-8') as f:
                    reports['privacy_policy'] = json.load(f)

            # 加载动态调试风险检测报告
            debug_report_path = results_path / 'debug_check.json'
            if debug_report_path.exists():
                with open(debug_report_path, 'r', encoding='utf-8') as f:
                    reports['debug'] = json.load(f)

            # 加载日志泄露风险检测报告
            log_leak_report_path = results_path / 'log_leak_check.json'
            if log_leak_report_path.exists():
                with open(log_leak_report_path, 'r', encoding='utf-8') as f:
                    reports['log_leak'] = json.load(f)

            # 加载 SDK 检测报告
            sdk_report_path = results_path / 'sdk_check.json'
            if sdk_report_path.exists():
                with open(sdk_report_path, 'r', encoding='utf-8') as f:
                    reports['sdk'] = json.load(f)

            # 加载权限确认单
            perm_confirm_path = results_path / 'permission_confirmation.json'
            if perm_confirm_path.exists():
                with open(perm_confirm_path, 'r', encoding='utf-8') as f:
                    reports['permission_confirmation'] = json.load(f)

            # 加载自评估报告
            self_assess_path = results_path / 'self_assessment.json'
            if self_assess_path.exists():
                with open(self_assess_path, 'r', encoding='utf-8') as f:
                    reports['self_assessment'] = json.load(f)

        except Exception as e:
            print(f"[-] 加载报告失败: {e}")

        return reports

    def calculate_overall_score(self, reports: Dict) -> int:
        """计算总体评分"""
        scores = []

        if 'permission' in reports:
            scores.append(reports['permission'].get('score', 0))

        if 'api' in reports:
            scores.append(reports['api'].get('score', 0))

        if 'dataflow' in reports:
            scores.append(reports['dataflow'].get('score', 0))

        if 'privacy_policy' in reports:
            scores.append(reports['privacy_policy'].get('score', 0))

        if 'debug' in reports:
            scores.append(reports['debug'].get('score', 0))

        if 'log_leak' in reports:
            scores.append(reports['log_leak'].get('score', 0))

        if 'sdk' in reports:
            scores.append(reports['sdk'].get('score', 0))

        # 计算加权平均分
        weights = {
            'permission': 0.20,
            'api': 0.25,
            'dataflow': 0.15,
            'privacy_policy': 0.20,
            'debug': 0.10,
            'log_leak': 0.10,
            'sdk': 0.10,
        }

        weighted_sum = 0
        total_weight = 0

        for key, weight in weights.items():
            if key in reports:
                weighted_sum += reports[key].get('score', 0) * weight
                total_weight += weight

        if total_weight > 0:
            overall_score = int(weighted_sum / total_weight)
        else:
            overall_score = 100

        return overall_score

    def determine_risk_level(self, score: int) -> str:
        """确定风险等级"""
        if score >= 90:
            return '✅ 低风险'
        elif score >= 70:
            return '⚠️ 中风险'
        elif score >= 50:
            return '🟠 高风险'
        elif score >= 30:
            return '🔴 较高风险'
        else:
            return '⛔ 极高风险'

    def determine_review_probability(self, score: int) -> str:
        """确定审核通过概率"""
        if score >= 90:
            return '高（90%+）'
        elif score >= 70:
            return '较高（70%+）'
        elif score >= 50:
            return '中（50%+）'
        elif score >= 30:
            return '较低（30%+）'
        else:
            return '低（30%-）'

    def get_check_object_info(self, miniprogram_path: str) -> Dict:
        """获取小程序基本信息"""
        info = {
            'miniprogram_path': miniprogram_path,
            'check_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        # 读取 app.json 获取小程序信息
        app_json_path = Path(miniprogram_path) / 'app.json'
        if app_json_path.exists():
            try:
                with open(app_json_path, 'r', encoding='utf-8') as f:
                    app_config = json.load(f)

                info['appname'] = app_config.get('appName', '未命名')
                info['appid'] = app_config.get('appid', '未知')
                info['version'] = app_config.get('version', '未知')
                info['compileType'] = app_config.get('compileType', '未知')
                info['debug'] = app_config.get('debug', False)
            except Exception as e:
                info['error'] = f'读取 app.json 失败: {e}'

        return info

    def _get_status_emoji(self, score: int) -> str:
        """获取状态emoji"""
        if score >= 90:
            return '✅'
        elif score >= 70:
            return '⚠️'
        elif score >= 50:
            return '🟡'
        elif score >= 30:
            return '🟠'
        else:
            return '🔴'

    def generate_summary(self, reports: Dict, check_info: Dict, results_dir: str) -> str:
        """生成综合概要报告"""
        overall_score = self.calculate_overall_score(reports)
        risk_level = self.determine_risk_level(overall_score)
        review_prob = self.determine_review_probability(overall_score)

        # 收集所有问题
        all_issues = []
        for category, report in reports.items():
            if category in ['permission_confirmation', 'self_assessment']:
                continue
            if isinstance(report, dict) and 'issues' in report:
                for issue in report['issues']:
                    all_issues.append({
                        'category': category,
                        'severity': issue.get('type', 'info'),
                        'message': issue.get('message', ''),
                        'file': issue.get('file', ''),
                        'line': issue.get('line', ''),
                    })

        # 统计问题数量
        issue_stats = {
            'total': len(all_issues),
            'critical': len([i for i in all_issues if i['severity'] == 'critical']),
            'warning': len([i for i in all_issues if i['severity'] == 'warning']),
            'info': len([i for i in all_issues if i['severity'] == 'info']),
        }

        # 开始构建报告
        summary = f"""📊 小程序隐私合规检查报告

---

## 📋 检查概要

**检查对象**: {check_info.get('appid', '未知')} 小程序（{check_info.get('miniprogram_path', '未知')}）
**检查时间**: {check_info.get('check_timestamp', '未知')}
**小程序名称**: {check_info.get('appname', '未命名')}
**编译类型**: {check_info.get('compileType', '未知')}

---

## 📚 合规标准

基于以下官方标准进行检查：

1. **《个人信息保护法》** - 中国首部个人信息保护专门法律
2. **《网络安全法》** - 网络运营者安全义务
3. **《微信小程序平台运营规范》** - 微信平台运营规范

---

## 🎯 核心检查项

"""

        # 添加各项检查结果
        check_items = [
            ('permission', '权限声明检查'),
            ('api', '敏感 API 扫描'),
            ('dataflow', '数据流分析'),
            ('debug', '动态调试风险检测'),
            ('log_leak', '日志泄露风险检测'),
            ('privacy_policy', '隐私政策检查'),
            ('sdk', 'SDK 使用检测'),
        ]

        for key, name in check_items:
            if key in reports:
                score = reports[key].get('score', 0)
                status = self._get_status_emoji(score)
                summary += f"\n### {name}\n"
                summary += f"**评分**: {score}/100\n"
                summary += f"**状态**: {status}\n\n"

        # 添加权限确认单和自评估表
        summary += "---\n\n"
        summary += "## 📋 合规表单\n\n"

        perm_confirm_path = Path(results_dir) / 'permission_confirmation.json'
        if perm_confirm_path.exists():
            summary += "✅ **小程序申请权限确认单**: 已生成\n"
            summary += f"   文件: `权限确认单.txt`\n\n"
        else:
            summary += "❌ **小程序申请权限确认单**: 未生成\n\n"

        self_assess_path = Path(results_dir) / 'self_assessment.json'
        if self_assess_path.exists():
            with open(self_assess_path, 'r', encoding='utf-8') as f:
                assess_data = json.load(f)
            score = assess_data.get('score', 0)
            level = assess_data.get('summary', {}).get('compliance_level', '未知')
            summary += f"✅ **个人信息收集使用自评估表**: 已生成\n"
            summary += f"   评分: {score}/100\n"
            summary += f"   等级: {level}\n"
            summary += f"   文件: `自评估表.txt`\n\n"
        else:
            summary += "❌ **个人信息收集使用自评估表**: 未生成\n\n"

        summary += "---\n\n"
        summary += "## 🎯 综合评估\n\n"
        summary += f"### 总体评分\n"
        summary += f"**合规评分**: {overall_score}/100\n"
        summary += f"**风险等级**: {risk_level}\n"
        summary += f"**审核通过概率**: {review_prob}\n\n"

        summary += "### 评分构成\n"
        summary += "- 权限声明检查: 20%\n"
        summary += "- 敏感 API 扫描: 25%\n"
        summary += "- 数据流分析: 15%\n"
        summary += "- 隐私政策检查: 20%\n"
        summary += "- 动态调试风险: 10%\n"
        summary += "- 日志泄露风险: 10%\n"
        summary += "- SDK 使用检测: 10%\n\n"

        summary += "---\n\n"
        summary += "## 📊 问题统计\n\n"
        summary += f"**问题总计**\n"
        summary += f"- 总数: {issue_stats['total']}\n"
        summary += f"- 🔴 严重问题: {issue_stats['critical']} 个\n"
        summary += f"- ⚠️ 警告问题: {issue_stats['warning']} 个\n"
        summary += f"- ℹ️ 信息提示: {issue_stats['info']} 个\n\n"

        if issue_stats['critical'] > 0:
            summary += "---\n\n"
            summary += "## 🚨 高风险问题\n\n"
            critical_issues = [i for i in all_issues if i['severity'] == 'critical']
            for i, issue in enumerate(critical_issues[:10], 1):
                summary += f"{i}. **{issue['category']}** - {issue['message']}\n"
                if issue['file']:
                    summary += f"   位置: {issue['file']}:{issue['line']}\n"
                summary += "\n"

        summary += "---\n\n"
        summary += "## 📄 详细报告位置\n\n"
        summary += "完整检查报告请查看:\n"
        summary += "- 权限声明: `permission_check_report.txt`\n"
        summary += "- 敏感 API: `api_scan_report.txt`\n"
        summary += "- 数据流: `dataflow_report.txt`\n"
        summary += "- 动态调试: `debug_check_report.txt`\n"
        summary += "- 日志泄露: `log_leak_report.txt`\n"
        summary += "- 隐私政策: `privacy_policy_report.txt`\n"
        summary += "- SDK 检测: `sdk_check_report.txt`\n"
        summary += "- **权限确认单: `权限确认单.txt`** ⭐ 新增\n"
        summary += "- **自评估表: `自评估表.txt`** ⭐ 新增\n\n"
        summary += "JSON 格式报告:\n"
        summary += "- permission_check.json\n"
        summary += "- api_scan.json\n"
        summary += "- dataflow_analysis.json\n"
        summary += "- debug_check.json\n"
        summary += "- log_leak_check.json\n"
        summary += "- privacy_policy_check.json\n"
        summary += "- sdk_check.json\n"
        summary += "- **permission_confirmation.json** ⭐ 新增\n"
        summary += "- **self_assessment.json** ⭐ 新增\n\n"
        summary += "综合报告: `privacy_compliance_report.md`\n"
        summary += "概要报告: `summary_report.txt`\n\n"

        summary += "---\n\n"
        summary += f"_报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += "_生成工具: summary_generator.py v2.0 (修复版)\n"
        summary += "_基于官方标准: 个人信息保护法、网络安全法、微信小程序平台运营规范\n"

        return summary


def print_and_save_report(summary: str, output_file: str = None):
    """打印并保存报告"""
    print(summary)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\n[+] 报告已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='小程序隐私合规检查概要报告生成器（修复版）')
    parser.add_argument('results_dir', help='检查结果目录')
    parser.add_argument('-m', '--miniprogram', help='小程序路径（用于获取基本信息）', default='')
    parser.add_argument('-o', '--output', help='报告输出文件', default='summary_report.txt')
    args = parser.parse_args()

    generator = SummaryReportGenerator()

    # 检查小程序基本信息
    miniprogram_path = args.miniprogram if args.miniprogram else args.results_dir
    check_info = generator.get_check_object_info(miniprogram_path)

    # 加载所有报告
    reports = generator.load_all_reports(args.results_dir)

    # 生成概要报告
    summary = generator.generate_summary(reports, check_info, args.results_dir)

    # 打印并保存报告
    print_and_save_report(summary, args.output)


if __name__ == '__main__':
    main()
