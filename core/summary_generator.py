#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私合规检查综合报告生成器
生成简洁的概要视图报告
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
            # 加载权限声明检查报告
            perm_report_path = Path(results_dir) / 'permission_check.json'
            if perm_report_path.exists():
                with open(perm_report_path, 'r', encoding='utf-8') as f:
                    reports['permission'] = json.load(f)

            # 加载敏感 API 扫描报告
            api_report_path = Path(results_dir) / 'api_scan.json'
            if api_report_path.exists():
                with open(api_report_path, 'r', encoding='utf-8') as f:
                    reports['api'] = json.load(f)

            # 加载数据流分析报告
            dataflow_report_path = Path(results_dir) / 'dataflow_analysis.json'
            if dataflow_report_path.exists():
                with open(dataflow_report_path, 'r', encoding='utf-8') as f:
                    reports['dataflow'] = json.load(f)

            # 加载隐私政策检查报告
            privacy_policy_report_path = Path(results_dir) / 'privacy_policy_check.json'
            if privacy_policy_report_path.exists():
                with open(privacy_policy_report_path, 'r', encoding='utf-8') as f:
                    reports['privacy_policy'] = json.load(f)

            # 加载动态调试风险检测报告
            debug_report_path = Path(results_dir) / 'debug_check.json'
            if debug_report_path.exists():
                with open(debug_report_path, 'r', encoding='utf-8') + (os.access(debug_report_path, os.R_OK)):
                    reports['debug'] = json.load(f)

            # 加载日志泄露风险检测报告
            log_leak_report_path = Path(results_dir) / 'log_leak_check.json'
            if log_leak_report_path.exists():
                with open(log_leak_report_path, 'r', encoding='utf-8') + (os.access(log_leak_report_path, os.R_OK)):
                    reports['log_leak'] = json.load(f)

            # 加加载 SDK 检测报告
            sdk_report_path = Path(results_dir) / 'sdk_check.json'
            if sdk_report_path.exists():
                with open(sdk_report_path, 'r', encoding='utf-8') as f:
                    reports['sdk'] = json.load(f)

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
            'permission': 0.20,  # 权限声明最重要
            'api': 0.25,           # 敏感 API 重要
            'dataflow': 0.15,        # 数据流分析
            'privacy_policy': 0.20,   # 隐私政策重要
            'debug': 0.10,          # 动态调试风险
            'log_leak': 0.10,        # 日志泄露风险
            'sdk': 0.10,           # SDK 使用
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
            return '⛤ 极高风险'

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
            'check_timestamp': datetime.now().isoformat('%Y-%m-%d %H:%M:%S'),
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

    def generate_summary(self, reports: Dict, check_info: Dict) -> str:
        """生成综合概要报告"""
        # 计算总体评分
        overall_score = self.calculate_overall_score(reports)
        risk_level = self.determine_risk_level(overall_score)
        review_prob = self.determine_review_probability(overall_score)

        # 收集所有问题
        all_issues = []

        # 权限相关
        if 'permission' in reports:
            perm_issues = reports['permission'].get('issues', [])
            for issue in perm_issues:
                all_issues.append({
                    'category': '权限声明',
                    'severity': issue.get('type', 'info'),
                    'message': issue.get('message', ''),
                    'file': issue.get('file', ''),
                    'line': issue.get('line', ''),
                })

        # 敏感 API 相关
        if 'api' in reports:
            api_issues = reports['api'].get('issues', [])
            for issue in api_issues:
                all_issues.append({
                    'category': '敏感API',
                    'severity': issue.get('type', 'info'),
                    'message': issue.get('message', ''),
                    'file': issue.get('file', ''),
                    'line': issue.get('line', ''),
                })

        # 数据流相关
        if 'dataflow' in reports:
            df_issues = reports['dataflow'].get('issues', [])
            for issue in df_issues:
                all_issues.append({
                    'category': '数据流',
                    'severity': issue.get('type', 'info'),
                    'message': issue.get('message', ''),
                    'file': issue.get('file', ''),
                    'line': issue.get('line', ''),
                })

        # 隐私政策相关
        if 'privacy_policy' in reports:
            pp_issues = reports['privacy_policy'].get('issues', [])
            for issue in pp_issues:
                all_issues.append({
                    'category': '隐私政策',
                    'severity': issue.get('type', 'info'),
                    'message': issue.get('message', ''),
                    'file': issue.get('file', ''),
                    'line': issue.get('line', ''),
                })

        # 动态调试风险
        if 'debug' in reports:
            debug_issues = reports['debug'].get('issues', [])
            for issue in debug_issues:
                all_issues.append({
                    'category': '动态调试',
                    'severity': issue.get('type', 'info'),
                    'message': issue.get('message', ''),
                    'file': issue.get('file', ''),
                    'line': issue.get('line', ''),
                })

        # 日志泄露风险
        if 'log_leak' in reports:
            log_issues = reports['log_leak'].get('issues', [])
            for issue in log_issues:
                all_issues.append({
                    'category': '日志泄露',
                    'severity': issue.get('type', 'info'),
                    'message': issue.get('message', ''),
                    'file': issue.get('file', ''),
                    'line': issue.get('line', ''),
                })

        # SDK 使用
        if 'sdk' in reports:
            sdk_issues = reports['sdk'].get('issues', [])
            for issue in sdk_issues:
                all_issues.append({
                    'category': '第三方SDK',
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

        # 生成概要
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

### 1. 权限声明检查
**评分**: {reports['permission'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('permission', {}).get('score', 0))}
"""

        if 'permission' in reports:
            perm_report = reports['permission']
            perm_summary = perm_report.get('summary', {})
            
            # 检测到的敏感 API
            detected_apis = perm_report.get('detected_apis', {})
            total_apis = len(detected_apis)
            
            # 缺失的权限
            missing = perm_report.get('missing_permissions', [])
            unused = perm_report.get('unused_permissions', [])
            
            print(f"- 检测到的敏感 API: {total_apis} 种")
            if total_apis > 0:
                # 按风险等级分组
                high_risk = len([k for k in detected_apis.keys() if 'high' in k.lower()])
                medium_risk = len([k for k in detected_apis.keys() if 'medium' in k.lower()])
                low_risk = len([k for k in detected_apis.keys() if 'low' in k.lower()])
                
                if high_risk > 0:
                    print(f"  - 🔴 高风险: {high_risk} 种")
                if medium_risk > 0:
                    print(f"  - 🟡 中风险: {medium_risk} 种")
                if low_risk > 0:
                    print(f"  - 🟢 低风险: {low_risk} 种")
            
            if missing:
                print(f"- 缺失的权限声明: {len(missing)} 个")
                if len(missing) <= 5:
                    for perm in missing:
                        print(f"  • {perm}")
                else:
                    print(f"  • 详见详细报告")
            
            if unused:
                print(f"- 未使用的权限声明: {len(unused)} 个")

### 2. 敏感 API 扫描
**评分**: {reports['api'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('api', {}).get('score', 0))}
"""

        if 'api' in reports:
            api_report = reports['api']
            detected_apis = api_report.get('detected_apis', {})
            total_calls = sum(len(calls) for calls in detected_apis.values())
            
            print(f"- 检测到的敏感 API 调用: {total_calls} 次")
            print(f"- 检测到的 API 种类: {len(detected_apis)} 种")
            
            # 按类别统计
            categories = {}
            for api_name, calls in detected_apis.items():
                for call in calls:
                    category = call.get('category', '未知')
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += 1
            
            print(f"- 按类别统计:")
            for category, count in sorted(categories.items(), key=lambda x: -x[1]):
                print(f"  - {category}: {count} 次")

### 3. 数据流分析
**评分**: {reports['dataflow'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('dataflow', {}).get('score', 0))}
"""

        if 'dataflow' in reports:
            df_report = reports['dataflow']
            summary = df_report.get('summary', {})
            
            print(f"- 数据收集点: {summary.get('total_collection_points', 0)} 个")
            print(f"- 数据存储点: {summary.get('total_storage_points', 0)} 个")
            print(f"- 数据传输点: {summary.get('total_transmission_points', 0)} 个")
            
            # 敏感数据使用
            sensitive_usage = summary.get('total_sensitive_data_usage', 0)
            if sensitive_usage > 0:
                print(f"- 敏感数据使用: {sensitive_usage} 处")
            
            # 风查明文传输
            http_trans = df_report.get('data_transmission_points', [])
            http_count = len([t for t in http_trans if t.get('uses_http')])
            if http_count > 0:
                print(f"⚠️  HTTP 传输: {http_count} 处（明文传输风险）")

### 4. 动态调试风险检测
**评分**: {reports['debug'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('debug', {}).get('score', 0))}
"""

        if 'debug' in reports:
            debug_report = reports['debug']
            debug_detections = debug_report.get('debug_detections', {})
            total_detections = sum(len(detections) for detections in debug_detections.values())
            
            print(f"- 检测到的调试工具: {total_detections} 处")
            
            # 高风险调试工具
            high_risk_tools = [
                'vConsole', 'eruda', 'Debugger'
            ]
            high_risk_count = 0
            
            for tool_name in high_risk_tools:
                if tool_name.lower() in str(debug_detections).lower():
                    count = len(debug_detections.get(tool_name, []))
                    high_risk_count += count
            
            if high_risk_count > 0:
                print(f"⚠️  高风险调试工具: {high_risk_count} 个")

### 5. 日志泄露风险检测
**评分**: {reports['log_leak'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('log_leak', {}).get('score', 0))}
"""

        if 'log_leak' in reports:
            log_report = reports['log_leak']
            sensitive_log = log_report.get('sensitive_data_usage', {})
            
            print(f"- 检测到的敏感日志泄露: {len(sensitive_log)} 处")
            
            # 按类型统计
            leak_types = {}
            for leak_type, detections in sensitive_log.items():
                leak_count = len(detections)
                if leak_count > 0:
                    leak_types[leak_type] = leak_count
            
            print(f"- 泄漏类型统计:")
            for leak_type, count in sorted(leak_types.items(), key=lambda x: -x[1]):
                risk_level = {
                    'password': '🔴',
                    'token': '🔴',
                    'user_info': '🔴',
                    'personal_data': '🔴',
                }.get(leak_type.lower(), '⚠️')
                print(f"  - {leak_type}: {count} 处")

### 6. 隐私政策检查
**评分**: {reports['privacy_policy'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('privacy_policy', {}).get('score', 0))}
"""

        if 'privacy_policy' in reports:
            pp_report = reports['privacy_policy']
            summary = pp_report.get('summary', {})
            
            has_policy = summary.get('has_privacy_policy', False)
            
            print(f"- 隐私政策文件: {'有' if has_policy else '无'}")
            
            if has_policy:
                present = summary.get('present_required_clauses', 0)
                total = summary.get('total_required_clauses', 9)
                print(f"- 必备条款: {present}/{total}")
                
                if present < total:
                    missing = total - present
                    print(f"  ⚠️  缺失必备条款: {missing} 个")

### 7. SDK 使用检测
**评分**: {reports['sdk'].get('score', 0)}/100
**状态**: {self._get_status_emoji(reports.get('sdk', {}).get('score', 0))}
"""

        if 'sdk' in reports:
            sdk_report = reports['sdk']
            summary = sdk_report.get('summary', {})
            
            total_detected = summary.get('total_detected_sdks', 0)
            high_risk = summary.get('high_risk_sdks', 0)
            
            print(f"- 检测到的 SDK: {total_detected} 种")
            if high_risk > 0:
                print(f"  - 🔴 高风险 SDK: {high_risk} 种")
            
            # 检测到的 SDK 列表
            detected_sdks = list(sdk_report.get('detected_sdks', {}).keys())
            if detected_sdks:
                print(f"- 检测到: {', '.join(sorted(detected_sdks))}")

---

## 🎯 综合评估

### 总体评分
**合规评分**: {overall_score}/100
**风险等级**: {risk_level}
**审核通过概率**: {review_prob}

### 评分构成
- 权限声明检查: 20%
- 敏感 API 扫描: 25%
- 数据流分析: 15%
- 隐私政策检查: 20%
- 动态调试风险: 10%
- 日志泄露风险: 10%
- SDK 使用检测: 10%

---

## 📊 问题统计

### 问题总计
- 总数: {issue_stats['total']}
- 🔴 严重问题: {issue_stats['critical']} 个
- ⚠️  警告问题: {issue_stats['warning']} 个
- ℹ️ 信息提示: {issue_stats['info']} 个

### 问题分布
- 权限声明: {len([i for i in all_issues if i['category'] == '权限声明'])} 个
- 敏感API: {len([i for i in all_issues if i['category'] == '敏感API'])} 个
- 数据流: {len([i for i in all_issues if i['category'] == '数据流'])} 个
- 隐私政策: {len([i for i in all_issues if i['category'] == '隐私政策'])} 个
- 动态调试: {len([i for i in all_issues if i['category'] == '动态调试'])} 个
- 日志泄露: {len([i for i in all_issues if i['category'] == '日志泄露'])} 个
- 第三方SDK: {len([i for i in all_issues if i['category'] == '第三方SDK'])} 个

---

## 📋 高风险问题
"""

if issue_stats['critical'] > 0:
    print("🚨 以下问题必须修复（审核不通过风险）:")
    for i, issue in enumerate(sorted(all_issues, key=lambda x: (x['severity'] == 'critical', x['severity'] == 'warning'), x.get('line')):
        if issue['severity'] == 'critical':
            print(f"  • [{i+1}] {issue['category']} - {issue['message']}")
            if issue['file']:
                print(f"      文件: {issue['file']}:{issue['line']}")
            if issue['suggestion']:
                print(f"      建议: {issue['suggestion']}")
else:
    print("✅ 无严重问题")

---

## 📋 修复建议

"""

if overall_score >= 90:
    print("✅ 合规性良好，建议定期检查")
elif overall_score >= 70:
    print("⚠️ 整体合规，有少量需要改进")
elif overall_score >= 50:
    print("🟠️ 存在一些风险，建议及时修复的问题")
elif overall_score >= 30:
    print("🟠 存在较多问题，审核可能不通过")
else:
    print("🔴 严重违规，审核大概率不通过")

---

## 📄 详细报告位置

完整检查报告请查看:
- 权限声明: permission_check_report.txt
- 敏感 API: api_scan_report.txt
- 数据流: dataflow_report.txt
- 动态调试: debug_check_report.txt
- 日志泄露: log_leak_report.txt
- 隐私政策: privacy_policy_report.txt
- SDK 检测: sdk_check_report.txt

JSON 格式报告:
- permission_check.json
- api_scan.json
- dataflow_analysis.json
- debug_check.json
- log_leak_check.json
- privacy_policy_check.json
- sdk_check.json

综合报告: privacy_compliance_report.md
概要报告: summary_report.txt

---

_报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
_生成工具: summary_generator.py v1.0
_基于官方标准: 个人信息保护法、网络安全法、微信小程序平台运营规范
"""

    def _get_status_emoji(self, report: Dict) -> str:
        """获取状态emoji"""
        score = report.get('score', 0)
        if score >= 90:
            return '✅'
        elif score >= 70:
            return '⚠️'
        elif score >= 50:
            return '🟡'
        elif score >= 30:
            return '🟠'
        else:
            return '⚠️'


def print_report(summary: str, output_file: str = None):
    """打印报告"""
    print(summary)

    if output_file:
        # 保存文本格式
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\n[+] 报告已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='小程序隐私合规检查概要报告生成器')
    parser.add_argument('results_dir', help='检查结果目录', default='privacy_check_results')
    parser.add_argument('-o', '--output', help='报告输出文件', default='summary_report.txt')
    args = parser.parse_args()

    generator = SummaryReportGenerator()
    
    # 检查小程序基本信息
    check_info = generator.get_check_object_info(args.results_dir)
    
    # 加载所有报告
    reports = generator.load_all_reports(args.results_dir)
    
    # 生成概要报告
    summary = generator.generate_summary(reports, check_info)
    
    # 打印报告
    print_report(summary, args.output)


if __name__ == '__main__':
    main()
