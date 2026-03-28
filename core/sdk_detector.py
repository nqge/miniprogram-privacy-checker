#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序第三方 SDK 检测工具
检测项目中的第三方 SDK 使用，分析隐私合规风险
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict
import argparse


class SDKDetector:
    """小程序 SDK 检测器"""

    # 常见的第三方 SDK 列表（按隐私风险分类）
    KNOWN_SDKS = {
        # ===== 高风险 SDK =====
        'umeng': {
            'name': '友盟',
            'risk_level': 'high',
            'description': '友盟 SDK',
            'common_patterns': [
                r'https?://(\w+)?\.umeng\.cn/',
                r'w?\.umeng\.com/',
                r'from.*umeng',
            ],
            'sensitive_apis': ['getPhoneNumber', 'getInstallReferrer', 'getSystemInfo', 'getAdvertisingId'],
            'privacy_risks': [
                '收集设备信息',
                '获取安装渠道',
                '获取广告ID'
            ]
        },
        'wechat_open': {
            'name': '微信开放平台',
            'risk_level': 'high',
            'description': '微信开放平台 SDK',
            'common_patterns': [
                r'https?://(\w+)?\.wechat\.open\.com/',
                r'w?\.weixin\.open\.com/',
                r'from.*wechat.*open',
            ],
            'sensitive_apis': ['getPhoneNumber', 'getUserProfile', 'getLaunchArgs'],
            'privacy_risks': [
                '获取用户手机号',
                '获取用户信息',
                '获取启动参数'
            ]
        },

        # ===== 中等风险 SDK =====
        'alipay': {
            'name': '支付宝 SDK',
            'risk_level': 'medium',
            'description': '支付宝支付',
            'common_patterns': [
                r'https?://(\w+)?\.alipay\.com/',
                r'w?\.alipaysdk\.com/',
                r'.*alipay.*sdk',
            ],
            'sensitive_apis': ['tradePay', 'authTrade'],
            'privacy_risks': [
                '发起支付',
                '认证交易'
            ]
        },
        'tencent_map': {
            'name': '腾讯地图 SDK',
            'risk_level': 'medium',
            'description': '腾讯地图',
            'common_patterns': [
                r'https?://(\w+)?\.map\.qq\.com/',
                r'w?\.map\.qq\.com/',
                r'.*qq\.map.*sdk',
                r'apis\.map\.qq\.com',
            ],
            'sensitive_apis': ['geocoder', 'getuserlocation', 'reverseGeocoder'],
            'privacy_risks': [
                '获取用户位置',
                '逆地址解析'
            ]
        },

        # ===== 低风险 SDK =====
        'share_trace': {
            'name': 'ShareTrace 微博',
            'risk_level': 'low',
            'description': 'ShareTrace 微博 SDK',
            'common_patterns': [
                r'https?://(\w+)?(\w+)?\.cn\.sharetrace\.com/',
                r'cn\.sharetrace\.com/',
                r'w?\.cn\.sharetrace\.com/',
                r'from.*sharetrace',
            ],
            'sensitive_apis': ['shareContent', 'shareImage'],
            'privacy_risks': [
                '分享内容',
                '分享图片'
            ]
        },
        'crash_cn': {
            'name': 'CNZZDash 创',
            'risk_level': 'low',
            'description': 'CNZZDash',
            'common_patterns': [
                r'https?://(\w+)?\.dash\.cn\.zabbix\.com/',
                r'w?\.zabbix\.com/',
                r'from.*zabbix',
            ],
            'sensitive_apis': [],
            'privacy_risks': []
        },
    }

    # 代理/CDN 相关
    PROXY_PATTERNS = [
        r'(https?:)?//.*\.(?:cn|com|net|org|io)',
        r'(http?:)?//.*\.(?:cn|com|net|org|io)',
    ]

    def __init__(self, miniprogram_path: str):
        """
        初始化 SDK 检测器

        Args:
            miniprogram_path: 小程序源代码路径
        """
        self.miniprogram_path = Path(miniprogram_path)
        self.js_files = []
        self.json_files = []
        self.detected_sdks = defaultdict(list)
        self.sdk_dependencies = []
        self.cdn_requests = []
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
        执行 SDK 检测

        Returns:
            检测结果字典
        """
        print("[*] 开始 SDK 检测...")

        # 1. 扫描 package.json 和 app.json 中的依赖
        print("\n[1/5] 扫描依赖配置文件...")
        self._scan_package_configs()

        # 2. 扫描 JS 文件中的 SDK 引用
        print("\n[2/5] 扫描 SDK 引用...")
        self._scan_sdk_usage()

        # 3. 扫描 CDN/代理请求
        print("\n[3/5] 扫描网络请求...")
        self._scan_network_cdn_requests()

        # 4. 检测第三方域访问
        print("\n[[4/5] 检测第三方域访问...")
        self._check_third_party_domains()

        # 5. 生成检查报告
        print("\n[5/5] 生成检查报告...")
        return self._generate_report()

    def _scan_package_configs(self):
        """扫描 package.json 和 app.json 中的依赖"""
        # 扫描 package.json
        package_json = self.miniprogram_path / 'package.json'
        if package_json.exists():
            self._scan_package_config(package_json)

        # 扫描 app.json
        app_json = self.miniprogram_path / 'app.json'
        if app_json.exists():
            self._scan_app_config(app_json)

    def _scan_package_config(self, config_file: Path):
        """扫描 package.json 文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 检查 dependencies
            if 'dependencies' in config:
                for dep in config['dependencies']:
                    self._check_dependency(dep, str(config_file.relative_to(self.miniprogram_path)))
                    if 'version' in dep:
                        self.sdk_dependencies.append({
                            'source': str(config_file.relative_to(self.miniprogram_path)),
                            'name': dep['name'],
                            'version': dep.get('version', 'latest'),
                            'url': dep.get('url', '')
                        })

        except Exception as e:
            print(f"[-] 读取文件失败 {config_file}: {e}")

    def _scan_app_config(self, config_file: path):
        """扫描 app.json 文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 检查 plugins（小程序云开发插件）
            if 'plugins' in config:
                for plugin in config['plugins']:
'].values():
                    self._check_dependency(plugin, str(config_file.relative_to(self.miniprogram_path)))

            # 检查 cloudcontainer（云开发云函数）
            if 'cloudcontainer' in config:
                cloudcontainer = config['cloudcontainer']
                if 'plugins' in cloudcontainer:
                    for plugin in cloudcontainer['plugins'].values():
                        self._check_dependency(plugin, str(config_file.relative_to(self.miniprogram_path)))

        except Exception as e:
            print(f"[-] 读取文件失败 {config_file}: {e}")

    def _check_dependency(self, dep_info: str, source_file: str):
        """检查依赖信息"""
        dep_name = dep_info

        # 检查是否为已知高风险 SDK
        for sdk_key, sdk_info in self.KNOWN_SDKS.items():
            if sdk_key in dep_info.lower():
                self.detected_sdks[sdk_key].append({
                    'file': source_file,
                    'pattern': dep_info,
                    'risk_level': sdk_info['risk_level']
                })
                
                # 根据风险等级记录问题
                risk_level = sdk_info['risk_level']
                if risk_level in ['high', 'critical']:
                    self.issues.append({
                        'type': risk_level,
                        'category': '第三方SDK',
                        'sdk_name': sdk_info['name'],
                        'file': source_file,
                        'message': f'检测到高风险 SDK: {sdk_info["name"]}',
                        'suggestion': f'请评估 {sdk_info["name"]} 的必要性，如非必需建议移除，并检查其隐私政策'
                    })
                elif risk_level == 'medium':
                    self.issues.append({
                        'type': 'warning',
                        'category': '第三方SDK',
                        'sdk_name': sdk_info['name'],
                        'file': source_file,
                        'message': f'检测到 SDK: {sdk_info["name"]}',
                        'suggestion': f'请检查 {sdk_info["name"]} 的隐私政策，确保符合隐私合规要求'
                    })

    def _scan_sdk_usage(self):
        """扫描 JS 文件中的 SDK 引用"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', 'encoding='utf-8') as f:
                    content = f.read()
                    lines = content
.split('\n')

                # 检查每个 SDK 的模式
                for sdk_key, sdk_info in self.KNOWN_SDKS.items():
                    for pattern in sdk_info['common_patterns']:
                        regex = re.compile(pattern, re.IGNORECASE)
                        for line_num, line in enumerate(lines, 1):
                            if regex.search(line):
                                self.detected_sdks[sdk_key].append({
                                    'file': str(js_file.relative_to(self.miniprogram_path)),
                                    'pattern': pattern,
                                    'line': line_num,
                                    'code': line.strip()
                                })

                                # 记录敏感 API 调用
                                self._check_sensitive_api_usage(
                                    js_file,
                                    line_num,
                                    line,
                                    sdk_info['name'],
                                    sdk_info['sensitive_apis']
                                )
            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

    def _check_sensitive_api_usage(self, js_file, line_num, line, sdk_name, sensitive_apis):
        """检查 SDK 的敏感 API 调用"""
        for api in sensitive_apis:
            if f'{api}(' in line or f'"{api}"' in line:
                self.issues.append({
                    'type': 'warning',
                    'category': '敏感API调用',
                    'sdk_name': sdk_name,
                    'file': str(js_file.relative_to(self.miniprogram_path)),
                    'line': line_num,
                    'message': f'检测到 {sdk_name} 的敏感 API 调用: {api}()',
                    'suggestion': f'请评估 {api}() 调用的必要性，并确保符合隐私政策'
                })

    def _scan_network_cdn_requests(self):
        """扫描网络请求（CDN/代理）"""
        for js_file in self.js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # 检测代理/CDN 模式
                for line_num, line in enumerate(lines, 1):
                    # 检测代理设置
                    if re.search(r'proxy\s*[:=]\s*["\']', line):
                        # 提取代理地址
                        proxy_match = re.search(r'["\']([^"\']+)["\']', line)
                        if cProxy_match:
                            proxy = proxy_match.group(1)
                            self._check_proxy_address(proxy, js_file, line_num)

                    # 检测 CDN 域式
                    if re.search(r'https?://\s*(cdn|cloud|obj)(?:-storage|\.cloudfront|\.cos)', line):
                        self.cdn_requests.append({
                            'file': str(js_file.relative_to(self.miniprogram_path)),
                            'line': line_num,
                            'code': line.strip(),
                            'type': 'cdn'
                        })

            except Exception as e:
                print(f"[-] 读取文件失败 {js_file}: {e}")

    def _check_proxy_address(self, proxy, js_file, line_num):
        """检查代理地址"""
        # 检测是否为第三方代理
        third_party_domains = [
            'aliyun', 'qiniucdn', 'upyun', 'bce', 'tencentyyun', 'fastgit',
            'qiniu', 'qnyun', 'dnspod', 'xiniu', 'cdn', 'yun', 'aliyun'
        ]

        for domain in third_party_domains:
            if domain in proxy.lower():
                self.issues.append({
                    'type': 'warning',
                    'category': '网络配置',
                    'file': str(js_file.relative_to(self.miniprogram_path)),
                    'line': line_num,
                    'message': f'检测到第三方代理: {domain}',
                    'suggestion': '第三方代理可能存在数据泄露风险，建议使用自建 CDN 或可信的 CDN 服务'
                })
                break

    def _check_third_party_domains(self):
        """检查第三方域访问"""
        # 统计访问的第三方域
        third_party_domains = defaultdict(int)
        for req in self.cdn_requests:
            for domain in third_party_domains:
                if domain in req['code'].lower():
                    third_party_domains[domain] += 1

        # 检测访问频率
        for domain, count in third_party.items():
            if count >= 3:
                self. issues.append({
                    'type': 'warning',
                    'category': '第三方域访问',
                    'message': f'频繁访问第三方域名: {domain} ({count} 次)',
                    'suggestion': '建议评估第三方域的必要性，减少不必要的第三方依赖'
                })

    def _generate_report(self) -> Dict:
        """生成检查报告"""
        # 统计问题
        issue_stats = defaultdict(int)
        for issue in self.issues:
            issue_stats[issue['type']] += 1

        # 统计 SDK 飀测
        sdk_count = len(self) 1 for sdk in self.detected_sdks.keys()))

        # 计算评分
        critical_issues = issue_stats.get('critical', 0)
        high_risk_sdks = len([k for k, v in self.detected_sdks.items()
                                    if self.KNOWN_SDKS.get(k, {}).get('risk_level') == 'high'])

        if critical_issues > 0 or high_risk_sdks > 3:
            score = max(100 - (critical_issues * 30) - (high_risk_sdks * 15), 0)
        elif issue_stats.get('warning', 0) > 10:
            score = max(100 - issue_stats['warning'] * 8), 0)
        elif issue_stats.get('info', 0) > 20:
            score = max(100 - issue_stats['info'] * 3), 0)
        else:
            score = 100

        return {
            'score': score,
            'detected_sdks': dict([(k, len(v)) for k, v in self.detected_sdks.items()]),
            'sdk_dependencies': self.sdk_dependencies,
            'cdn_requests': len(self.cdn_requests),
            'third_party_domains': dict(third_party_domains),
            'issues': self.issues,
            'issue_stats': dict(issue_stats),
            'summary': {
                'total_detected_sdks': sdk_count,
                'high_risk_sdks': high_risk_sdks,
                'critical_issues': critical_issues,
                'warning_issues': issue_stats.get('warning', 0),
                'info_issues': issue_stats.get('info', 0),
            }
        }


def print_report(report: Dict, output_dir: str = None):
    """打印并保存报告"""

    print("\n" + "="*60)
    print("小程序第三方 SDK 检测报告")
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
    print(f"  - 检测到的 SDK: {summary['total_detected_sdks']} 种")
    print(f"  - 高风险 SDK: {summary['high_risk_sdks']} 种")
    print(f"  - 严重问题: {summary['critical_issues']}")
    print(f"  - 警告问题: {summary['warning_issues']}")
    print(f"  - 信息提示: {summary['info_issues']}")

    # 检测到的 SDK 列表
    if report['detected_sdks']:
        print(f"\n🔍 检测到的 SDK 列表:")
        for sdk_key, detections in sorted(report['detected_sdks'].items()):
            sdk_info = SDKDetector.KNOWN_SDKS.get(sdk_key, {})
            risk_level = sdk_info.get('risk_level', 'unknown')
            risk_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢',
                'unknown': '⚪'
            }.get(risk_level, '⚪')

            print(f"  {risk_emoji} {sdk_info['name']} ({risk_level.upper()}) - {len(detections)} 处处引用")

            # 显示部分引用位置
            for detection in detections[:3]:
                print(f"     - {detection['file']}:{detection['line']}")
            if len(detections) > 3:
                print(f"     ... 还有 {len(detections) - 3} 处处引用")

    # 依赖列表
    if report['sdk_dependencies']:
        print(f"\n📦 声测到的依赖:")
        for dep in report['sdk_dependencies'][:10]:
            print(f"  - {dep['name']}: {dep.get('version', 'latest')}")

    # CDN 请求
    if report['cdn_requests']:
        print(f"\n🌐 CDN/代理请求: {report['cdn_requests']} 处")

    # 第三方域访问统计
    if report['third_party_domains']:
        print(f"\n🌐 第三方域访问统计:")
        for domain, count in sorted(report['third_party_domains'].items(), key=lambda x: -x[1], reverse=True):
            print(f"  - {domain}: {count} 次")

    # 问题列表
    if report['issues']:
        print(f"\n⚠️ 风险问题 ({len(report['issues'])} 个):")
        for i, issue in enumerate(report['issues'][:20], 1):
            type_emoji = {
                'critical': '🚨',
                'warning': '⚠️️',
                'info': 'ℹ️'
            }.get(issue['type'], '•')

            print(f"\n  {type_emoji} 问题 {i}: [{issue['type'].upper()}]")
            print(f"     类别: {issue.get('category', 'N/A')}")
            if 'sdk_name' in issue:
                print(f"     SDK: {issue['sdk_name']}")
            if 'file' in issue:
                print(f"     文件: {issue['file']}")
            if 'line' in issue:
                print(f"     行号: {issue['line']}")
            print(f"     描述: {issue['message']}")
            print(f"     建议: {issue['suggestion']}")

        if len(report['issues']) > 20:
            print(f"\n  ... 还有 {len(report['issues']) - 20} 个问题")

    # 保存报告
    if output_dir:
        import json
        os.makedirs(output_dir, exist_ok=True)

        # 保存 JSON 格式
        with open(os.path.join(output_dir, 'sdk_check.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n[+] JSON 报告已保存: {output_dir}/sdk_check.json")

        # 保存文本格式
        with open(os.path.join(output_dir, 'sdk_check_report.txt'), 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("小程序第三方 SDK 检测报告\n")
            f.write("="*60 + "\n\n")
            f.write(f"合规评分: {report['score']}/100\n\n")
            f.write(f"检测摘要:\n")
            f.write(f"  - 检测到的 SDK: {summary['total_detected_sdks']} 种\n")
            f.write(f" - 高风险 SDK: {summary['high_risk_sdks']} 种\n")
            f.write(f" - 严重问题: {summary['critical_issues']}\n")
            f.write(f" - 警告问题: {summary['warning_issues']}\n\n")

            if report['detected_sdks']:
                f.write("\n检测到的 SDK 列表:\n")
                for sdk_key, detections in sorted(report['detected_sdks'].items()):
                    sdk_info = SDKDetector.KNOWN_SDKS.get(sdk_key, {})
                    f.write(f"{sdk_info['name']} ({sdk_info['risk_level']}): {len(detections)} 处\n")

            if report['sdk_dependencies']:
                f.write("\n检测到的依赖:\n")
                for dep in report['sdk_dependencies'][:5]:
                    f.write(f"  - {dep['name']}: {dep.get('version', 'latest')}\n")

            if report['third_party_domains']:
                f.write("\n第三方域访问:\n")
                for domain, count in sorted(report['third_party_domains'].items()):
                    f.write(f"  - {domain}: {count} 次\n")

            if report['issues']:
                f.write("\n风险问题:\n")
                for issue in report['issues'][:10]:
                    f.write(f"[{issue['type']}] {issue['message']}\n")

        print(f"\n[+] 文本报告已保存: {output_dir}/sdk_check_report.txt")


def main():
    parser = argparse.ArgumentParser(description='小程序第三方 SDK 检测工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    checker = SDKDetector(args.miniprogram_path)
    report = checker.check()
    print_report(report, args.output)


if __name__ == '__main__':
    main()
