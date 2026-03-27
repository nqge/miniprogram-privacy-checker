#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私合规检查 - 增强版
基于用户要求的特定检查条件
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict
import json


class EnhancedPrivacyChecker:
    """小程序隐私合规检查器 - 增强版"""

    # 用户要求的检查条件
    REQUIRED_PATTERNS = {
        'permission': {
            'name': '权限声明检查',
            'pattern': r'(permission|requiredPrivateInfos|privacyPolicy|隐私|用户协议|服务条款)',
            'description': '检查权限声明和隐私政策配置',
            'risk_level': 'critical'
        },
        'ad_component': {
            'name': '广告组件检查',
            'pattern': r'(ad|广告|tt-ad|bs-ad|wx-open-launch-weapp|official-account)',
            'description': '检查第三方广告组件',
            'risk_level': 'high'
        },
        'storage_api': {
            'name': '存储 API 检查',
            'pattern': r'(setStorageSync|getStorageSync|setStorage|getStorage|removeStorage|clearStorage)',
            'description': '检查本地存储使用',
            'risk_level': 'medium'
        },
        'network_api': {
            'name': '网络 API 检查',
            'pattern': r'(request|uploadFile|downloadFile|connectSocket|sendSocketMessage)',
            'description': '检查网络请求和数据传输',
            'risk_level': 'medium'
        },
        'third_party_sdk': {
            'name': '第三方 SDK 检查',
            'pattern': r'(wx-open-launch-weapp|official-account|ad-component|ad|广告)',
            'description': '检查第三方 SDK 和广告组件',
            'risk_level': 'high'
        },
        'platform_sdk': {
            'name': '平台 SDK 检查',
            'pattern': r'(tt-official-account|tt-ad|bs-ad|tt-wx-open-launch-weapp)',
            'description': '检查抖音/百度等平台 SDK',
            'risk_level': 'high'
        },
        'encryption': {
            'name': '加密检测',
            'pattern': r'(encryptedRequest|AES|RSA|encrypt|decrypt|crypto)',
            'description': '检查加密算法使用',
            'risk_level': 'medium'
        },
        'user_data': {
            'name': '用户数据收集检测',
            'pattern': r'(userID|userName|userPhone|telNo|phone|mobile|realName|idCard|carNumber|plateNumber)',
            'description': '分析用户数据收集和使用情况',
            'risk_level': 'high'
        }
    }

    def __init__(self, miniprogram_path: str):
        """初始化检查器"""
        self.miniprogram_path = Path(miniprogram_path)
        self.findings = defaultdict(list)
        self.issues = []

    def check_all(self) -> Dict:
        """执行所有检查"""
        print(f"[*] 开始增强版隐私合规检查...")
        print(f"[*] 目标路径: {self.miniprogram_path}")
        print("")

        results = {}

        for check_key, check_info in self.REQUIRED_PATTERNS.items():
            print(f"[{check_info['name']}]")
            print(f"  模式: {check_info['pattern']}")
            print(f"  描述: {check_info['description']}")
            print(f"  风险等级: {check_info['risk_level'].upper()}")
            print(f"  状态: 检测中...")

            findings = self._scan_pattern(check_info['pattern'])
            self.findings[check_key] = findings

            if findings:
                print(f"  发现: {len(findings)} 处")
                for finding in findings[:3]:
                    print(f"    • {finding['file']}:{finding['line']}")
                if len(findings) > 3:
                    print(f"    ... 还有 {len(findings) - 3} 处")

                # 根据风险等级记录问题
                if check_info['risk_level'] == 'critical' and len(findings) > 0:
                    self.issues.append({
                        'type': 'critical',
                        'category': check_info['name'],
                        'message': f'检测到 {check_info['name']}，发现 {len(findings)} 处',
                        'suggestion': f'请检查 {check_info['description']}',
                        'findings': findings[:3]
                    })
                elif check_info['risk_level'] == 'high' and len(findings) > 5:
                    self.issues.append({
                        'type': 'warning',
                        'category': check_info['name'],
                        'message': f'发现大量 {check_info['name']} ({len(findings)} 处)',
                        'suggestion': f'建议评估 {check_info['description']} 的必要性',
                        'findings': findings[:3]
                    })
            else:
                print(f"  未发现")

            print()

        # 生成检查报告
        return self._generate_report(results)

    def _scan_pattern(self, pattern: str) -> List:
        """扫描文件中的模式"""
        results = []
        regex = re.compile(pattern, re.IGNORECASE)

        for js_file in self.miniprogram_path.rglob("*.js"):
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                for line_num, line in enumerate(lines, 1):
                    if regex.search(line):
                        results.append({
                            'file': str(js_file.relative_to(self.miniprogram_path)),
                            'line': line_num,
                            'code': line.strip(),
                            'pattern': pattern
                        })

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

        return results

    def _generate_report(self, results: Dict) -> Dict:
        """生成检查报告"""
        # 计算评分
        total_findings = sum(len(f) for f in results.values())
        critical_issues = len([i for i in self.issues if i['type'] == 'critical'])
        warning_issues = len([i for i in self.issues if i['type'] == 'warning'])

        if total_findings == 0:
            score = 100
        elif critical_issues > 0:
            score = max(100 - (critical_issues * 30), 0)
        elif warning_issues > 0:
            score = max(100 - (warning_issues * 15), 0)
        else:
            score = max(100 - (total_findings * 2), 0)

        return {
            'score': score,
            'findings': results,
            'issues': self.issues,
            'summary': {
                'total_findings': total_findings,
                'critical_issues': critical_issues,
                'warning_issues': warning_issues
            }
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='小程序隐私合规检查 - 增强版')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    args = parser.parse_args()

    checker = EnhancedPrivacyChecker(args.miniprogram_path)
    report = checker.check_all()

    print("\n" + "="*60)
    print("检查完成")
    print("="*60)
    print(f"\n📊 评分: {report['score']}/100")
    print(f"🔍 发现: {report['summary']['total_findings']} 处")
    print(f"🚨 严重问题: {report['summary']['critical_issues']}")
    print(f"⚠️  警告问题: {report['summary']['warning_issues']}")


if __name__ == '__main__':
    main()
