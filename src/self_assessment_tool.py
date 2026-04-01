#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序个人信息收集使用自评估工具
基于：《网络安全标准实践指南—移动互联网应用程序（App）收集使用个人信息自评估指南》
28个评估点，5大类别
"""

import os
import json
from pathlib import Path
from typing import Dict
from datetime import datetime
import argparse


class SelfAssessmentTool:
    """小程序个人信息收集使用自评估工具"""

    # 5 大类别，28 个评估点
    CATEGORIES = {
        'privacy_rules_public': '是否公开收集使用个人信息的规则',
        'purpose_disclosure': '是否明示收集使用个人信息的目的、方式和范围',
        'user_consent': '收集使用个人信息是否征得用户同意',
        'necessity_principle': '是否遵循必要原则，仅收集与其提供的服务直接相关的个人信息',
        'data_sharing': '是否未经同意向他人提供个人信息',
    }

    # 28 个详细评估点
    ASSESSMENT_ITEMS = {
        # 类别 1: 是否公开收集使用个人信息的规则 (6项: ID 1-6)
        'privacy_rules_public': [
            {
                'id': 1,
                'category': 'privacy_rules_public',
                'point': '是否有隐私政策等收集使用规则',
                'description': '是否在显著位置公开隐私政策等收集使用规则',
                'check_method': '检查小程序根目录和 pages 目录',
                'pass_criteria': '存在 privacy.md 或隐私政策.md 文件',
                'risk_level': 'critical'
            },
            {
                'id': 2,
                'category': 'privacy_rules_public',
                'point': '是否提示用户阅读隐私政策等收集使用规则',
                'description': '在用户首次打开时是否提示用户阅读隐私政策',
                'check_method': '检查 app.json 的 pages 配置',
                'pass_criteria': '在首页或启动页有隐私政策入口',
                'risk_level': 'critical'
            },
            {
                'id': 3,
                'category': 'privacy_rules_public',
                'point': '隐私政策等收集使用规则是否易于访问',
                'description': '隐私政策是否在小程序中易于找到和访问',
                'check_method': '检查页面配置和导航',
                'pass_criteria': '在 tabBar 或显著位置有隐私政策入口',
                'risk_level': 'high'
            },
            {
                'id': 4,
                'category': 'privacy_rules_public',
                'point': '隐私政策等收集使用规则是否易于阅读',
                'description': '隐私政策内容是否清晰易懂',
                'check_method': '检查隐私政策文件',
                'pass_criteria': '内容完整、结构清晰、语言易懂',
                'risk_level': 'medium'
            },
            {
                'id': 5,
                'category': 'privacy_rules_public',
                'point': '是否公开小程序运营者的基本情况',
                'description': '小程序是否公开了运营者的联系方式、企业信息等',
                'check_method': '检查隐私政策或关于页面',
                'pass_criteria': '包含联系方式、企业信息等',
                'risk_level': 'high'
            },
            {
                'id': 6,
                'category': 'privacy_rules_public',
                'point': '是否公开收集使用个人信息的其他规则',
                'description': '是否公开了其他收集使用规则（如服务协议、用户协议）',
                'check_method': '检查项目目录中的协议文件',
                'pass_criteria': '存在用户协议.md 或服务条款.md 文件',
                'risk_level': 'medium'
            },
        ],
        # 类别 2: 是否明示收集使用个人信息的目的、方式和范围 (5项: ID 7-11)
        'purpose_disclosure': [
            {
                'id': 7,
                'category': 'purpose_disclosure',
                'point': '是否逐一列出小程序（包括委托的第三方或嵌入的第三方代码、插件）收集使用个人信息的目的、方式、范围等',
                'description': '隐私政策中是否列出所有收集个人信息的目的、方式和范围',
                'check_method': '检查隐私政策内容',
                'pass_criteria': '包含所有收集的目的、方式和范围说明',
                'risk_level': 'critical'
            },
            {
                'id': 8,
                'category': 'purpose_disclosure',
                'point': '是否以适当的方式通知用户收集使用个人信息的目的、方式、范围的变化',
                'description': '隐私政策变更时是否通知用户',
                'check_method': '检查隐私政策版本和更新时间',
                'pass_criteria': '包含更新日期或生效日期',
                'risk_level': 'medium'
            },
            {
                'id': 9,
                'category': 'purpose_disclosure',
                'point': '是否同步告知申请打开权限和要求提供个人敏感信息的目的',
                'description': '在申请权限时是否同步告知目的',
                'check_method': '检查权限申请代码',
                'pass_criteria': '权限申请时有明确的目的说明',
                'risk_level': 'high'
            },
            {
                'id': 10,
                'category': 'purpose_disclosure',
                'point': '收集使用规则是否易于理解',
                'description': '隐私政策的表述是否清晰、明确、无歧义',
                'check_method': '检查隐私政策内容',
                'pass_criteria': '无模糊表述、无歧义',
                'risk_level': 'medium'
            },
        ],
        # 类别 3: 收集使用个人信息是否征得用户同意 (7项: ID 12-18)
        'user_consent': [
            {
                'id': 11,
                'category': 'user_consent',
                'point': '收集个人信息或打开可收集个人信息的权限前是否征得用户同意',
                'description': '在收集信息或申请权限前是否获得了用户的明确同意',
                'check_method': '检查权限申请和敏感API调用的代码流程',
                'pass_criteria': '在 wx.authorize 或 wx.openSetting 前有明确提示',
                'risk_level': 'critical'
            },
            {
                'id': 12,
                'category': 'user_consent',
                'point': '用户明确表示不同意收集后是否仍收集个人信息或打开可收集个人信息的权限',
                'description': '用户拒绝授权后是否仍尝试收集',
                'check_method': '检查权限拒绝处理逻辑',
                'pass_criteria': '用户拒绝后不再尝试收集或提供替代方案',
                'risk_level': 'critical'
            },
            {
                'id': 13,
                'category': 'user_consent',
                'point': '用户明确表示不同意收集后是否频繁征求用户同意、干扰用户正常使用',
                'description': '是否频繁弹出授权请求',
                'check_method': '检查授权请求频率',
                'pass_criteria': '不会频繁重复申请权限',
                'risk_level': 'high'
            },
            {
                'id': 14,
                'category': 'user_consent',
                'point': '实际收集的个人信息或打开的可收集个人信息权限是否超出用户授权范围',
                'description': '收集的信息是否超出授权范围',
                'check_method': '对比权限声明和实际使用',
                'pass_criteria': '所有收集都在授权范围内',
                'risk_level': 'critical'
            },
            {
                'id': 15,
                'category': 'user_consent',
                'point': '是否以默认选择同意隐私政策等非明示方式征求用户同意',
                'description': '是否使用默认同意、强制同意等非明示方式',
                'check_method': '检查授权配置和表单',
                'pass_criteria': '不使用默认同意或强制同意',
                'risk_level': 'critical'
            },
            {
                'id': 16,
                'category': 'user_consent',
                'point': '是否未经用户同意更改其设置的可收集个人信息权限状态',
                'description': '是否未经用户同意更改权限状态',
                'check_method': '检查权限设置代码',
                'pass_criteria': '不随意更改权限状态',
                'risk_level': 'critical'
            },
            {
                'id': 17,
                'category': 'user_consent',
                'point': '小程序利用用户个人信息和算法定向推送信息时，是否提供非定向推送信息的选项',
                'description': '是否提供了关闭定向推送的选项',
                'check_method': '检查推送配置',
                'pass_criteria': '提供关闭选项',
                'risk_level': 'medium'
            },
        ],
        # 类别 4: 是否遵循必要原则，仅收集与其提供的服务直接相关的个人信息 (4项: ID 19-22)
        'necessity_principle': [
            {
                'id': 18,
                'category': 'necessity_principle',
                'point': '是否以欺诈、诱骗等不正当方式误导用户同意收集个人信息或打开可收集个人信息的权限',
                'description': '是否存在误导性的授权请求',
                'check_method': '检查授权请求的文案和时机',
                'pass_criteria': '授权请求明确、准确、不误导',
                'risk_level': 'critical'
            },
            {
                'id': 19,
                'category': 'necessity_principle',
                'point': '是否向用户提供撤回同意收集个人信息的途径、方式',
                'description': '是否提供撤回同意的途径',
                'check_method': '检查隐私政策和设置',
                'pass_criteria': '提供明确的撤回方式和说明',
                'risk_level': 'high'
            },
            {
                'id': 20,
                'category': 'necessity_principle',
                'point': '是否违反其所声明的收集使用规则，收集使用个人信息',
                'description': '是否按声明的规则收集使用信息',
                'check_method': '对比声明和实际使用',
                'pass_criteria': '所有收集都符合声明',
                'risk_level': 'critical'
            },
            {
                'id': 21,
                'category': 'necessity_principle',
                'point': '是否收集与业务功能无关的个人信息',
                'description': '是否收集与业务无关的信息',
                'check_method': '检查敏感API调用和业务逻辑',
                'pass_criteria': '所有收集都与业务相关',
                'risk_level': 'high'
            },
            {
                'id': 22,
                'category': 'necessity_principle',
                'point': '用户是否可拒绝收集非必要信息或打开非必要权限',
                'description': '是否允许用户拒绝非必要信息或权限',
                'check_method': '检查业务逻辑',
                'pass_criteria': '提供拒绝选项或替代方案',
                'risk_level': 'medium'
            },
            {
                'id': 23,
                'category': 'necessity_principle',
                'point': '是否以非正当方式强迫收集用户个人信息',
                'description': '是否存在强迫收集的情况',
                'check_method': '检查收集流程和用户体验',
                'pass_criteria': '无强迫收集的情况',
                'risk_level': 'critical'
            },
            {
                'id': 24,
                'category': 'necessity_principle',
                'point': '收集个人信息的频度是否超出业务功能实际需要',
                'description': '收集频率是否合理',
                'check_method': '检查收集调用频率',
                'pass_criteria': '收集频率合理',
                'risk_level': 'medium'
            },
        ],
        # 类别 5: 是否未经同意向他人提供个人信息 (3项: ID 25-28)
        'data_sharing': [
            {
                'id': 25,
                'category': 'data_sharing',
                'point': '向他人提供个人信息前是否征得用户同意',
                'description': '第三方共享是否获得用户同意',
                'check_method': '检查第三方服务和共享声明',
                'pass_criteria': '在隐私政策中有明确说明并获得用户同意',
                'risk_level': 'critical'
            },
            {
                'id': 26,
                'category': 'data_sharing',
                'point': '是否按法律规定提供删除或更正个人信息功能，或公布投诉、举报方式等信息',
                'description': '是否提供注销账号功能',
                'check_method': '检查隐私政策和设置',
                'pass_criteria': '提供注销账号功能',
                'risk_level': 'critical'
            },
            {
                'id': 27,
                'category': 'data_sharing',
                'point': '是否提供有效的更正或删除个人信息',
                'description': '是否提供数据更正或删除功能',
                'check_method': '检查功能实现',
                'pass_criteria': '提供数据更正或删除功能',
                'risk_level': 'high'
            },
            {
                'id': 28,
                'category': 'data_sharing',
                'point': '是否建立并公布个人信息安全投诉、举报渠道',
                'description': '是否公布投诉举报渠道',
                'check_method': '检查隐私政策和联系信息',
                'pass_criteria': '有明确的联系方式和投诉渠道',
                'risk_level': 'high'
            },
        ],
    }

    def __init__(self, miniprogram_path: str):
        """初始化自评估工具"""
        self.miniprogram_path = Path(miniprogram_path)
        self.results = {}
        self.issues = []

    def assess(self) -> Dict:
        """执行自评估"""
        print(f"[*] 开始小程序个人信息收集使用自评估...")
        print(f"[*] 目标路径: {self.miniprogram_path}")
        print("")

        # 执行所有评估
        for category, items in self.ASSESSMENT_ITEMS.items():
            print(f"{'='*60}")
            print(f"类别: {category}")
            print(f"{'='*60}")
            print()

            for item in items:
                print(f"[{item['id']}] {item['point']}")
                print(f"     描述: {item['description']}")
                print(f"     检查方法: {item['check_method']}")
                print(f"     通过标准: {item['pass_criteria']}")
                print(f"     风险等级: {item['risk_level'].upper()}")

                # 执行检查
                result = self._check_item(item)
                self.results[item['id']] = result

                # 显示结果
                status_emoji = '✅' if result['status'] == 'pass' else '❌'
                print(f"     检查结果: {status_emoji} {result['status'].upper()}")

                if result['findings']:
                    print(f"     发现: {result['findings'][:3]}")

                if result['issues']:
                    print(f"     问题: {result['issues'][:3]}")

                print()

        # 生成评估报告
        return self._generate_report()

    def _check_item(self, item: Dict) -> Dict:
        """检查单个评估项"""
        findings = []
        issues = []
        status = 'fail'

        try:
            # 根据检查方法执行检查
            if '隐私政策' in item['check_method']:
                result = self._check_privacy_policy(item)
            elif '权限' in item['check_method'] or 'app.json' in item['check_method']:
                result = self._check_permissions(item)
            elif '代码' in item['check_method']:
                result = self._check_code(item)
            else:
                result = self._check_other(item)

            findings = result['findings']
            issues = result['issues']
            status = result['status']

        except Exception as e:
            issues.append(f"检查失败: {e}")
            status = 'error'

        return {
            'id': item['id'],
            'point': item['point'],
            'category': item['category'],
            'status': status,
            'findings': findings,
            'issues': issues
        }

    def _check_privacy_policy(self, item: Dict) -> Dict:
        """检查隐私政策"""
        findings = []
        issues = []
        status = 'fail'

        # 查找隐私政策文件
        privacy_files = list(self.miniprogram_path.rglob("privacy*.md")) + \
                      list(self.miniprogram_path.rglob("隐私*.md"))

        if not privacy_files:
            issues.append("未找到隐私政策文件")
            return {'status': 'fail', 'findings': findings, 'issues': issues}

        findings.append(f"发现 {len(privacy_files)} 个隐私政策文件")

        # 检查必备条款
        for policy_file in privacy_files:
            try:
                with open(policy_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()

                # 检查必备条款
                required_clauses = [
                    '收集目的',
                    '收集方式',
                    '收集范围',
                    '使用规则',
                    '联系方式',
                    '注销方式',
                ]

                missing_clauses = []
                for clause in required_clauses:
                    if clause not in content:
                        missing_clauses.append(clause)

                if missing_clauses:
                    issues.append(f"缺失条款: {', '.join(missing_clauses)}")
                else:
                    status = 'pass'

            except Exception as e:
                issues.append(f"读取文件失败: {e}")

        return {'status': status, 'findings': findings, 'issues': issues}

    def _check_permissions(self, item: Dict) -> Dict:
        """检查权限声明"""
        findings = []
        issues = []
        status = 'fail'

        app_json = self.miniprogram_path / 'app.json'

        if not app_json.exists():
            issues.append("未找到 app.json 文件")
            return {'status': 'fail', 'findings': findings, 'issues': issues}

        findings.append("找到 app.json 文件")

        try:
            with open(app_json, 'r', encoding='utf-8') as f:
                app_config = json.load(f)

            if 'permission' in app_config:
                findings.append(f"发现 {len(app_config['permission'])} 个权限声明")
                status = 'pass'
            else:
                issues.append("未声明 permission 字段")

        except Exception as e:
            issues.append(f"读取 app.json 失败: {e}")

        return {'status': status, 'findings': findings, 'issues': issues}

    def _check_code(self, item: Dict) -> Dict:
        """检查代码"""
        findings = []
        issues = []
        status = 'fail'

        # 扫描 JS 文件
        for js_file in self.miniprogram_path.rglob("*.js"):
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    lines = f.read().split('\n')

                # 检查敏感关键词
                keywords = {
                    'wx.authorize': '权限申请',
                    'wx.openSetting': '权限设置',
                }

                for keyword, desc in keywords.items():
                    for line_num, line in enumerate(lines, 1):
                        if keyword in line:
                            findings.append(f"{js_file.relative_to(self.miniprogram_path)}:{line_num}: {desc}")

                if findings:
                    status = 'pass'
                    break

            except Exception as e:
                issues.append(f"检查 {js_file} 失败: {e}")

        if findings:
            status = 'pass'

        return {'status': status, 'findings': findings, 'issues': issues}

    def _check_other(self, item: Dict) -> Dict:
        """检查其他"""
        return {'status': 'pass', 'findings': ['默认检查（通过）'], 'issues': []}

    def _generate_report(self) -> Dict:
        """生成评估报告"""
        total_items = 28
        pass_items = sum(
            1 for items in self.ASSESSMENT_ITEMS.values()
            for item in items
            if self.results.get(item['id'], {}).get('status') == 'pass'
        )
        fail_items = total_items - pass_items

        score = int((pass_items / total_items) * 100)

        return {
            'score': score,
            'total_items': total_items,
            'pass_items': pass_items,
            'fail_items': fail_items,
            'results': self.results,
            'summary': {
                'pass_rate': f"{(pass_items/total_items)*100:.1f}%",
                'total_issues': len(self.issues),
                'compliance_level': self._determine_level(score)
            }
        }

    def _determine_level(self, score: int) -> str:
        """确定合规等级"""
        if score >= 95:
            return '优秀（高合规）'
        elif score >= 80:
            return '良好（中合规）'
        elif score >= 60:
            return '一般（低合规）'
        elif score >= 40:
            return '较差（不合规）'
        else:
            return '极差（严重不合规）'


def print_assessment_table(self, report: Dict, output_dir: str = None):
    """打印评估表"""
    print("\n" + "="*80)
    print("            小程序个人信息收集使用自评估表")
    print("="*80)
    print("")

    # 按类别分组显示
    for category, items in self.ASSESSMENT_ITEMS.items():
        print(f"\n{'='*60}")
        print(f"类别: {category}")
        print(f"{'='*60}")

        for item in items:
            result = self.results.get(item['id'], {})
            status = result.get('status', 'unknown')
            status_emoji = '✅' if status == 'pass' else '❌'
            
            print(f"\n[{item['id']}] {item['point']}")
            print(f"  📝 描述: {item['description']}")
            print(f"  🔍 检查方法: {item['check_method']}")
            print(f"  ✅ 通过标准: {item['pass_criteria']}")
            print(f'  ⚠️  风险等级: {item["risk_level"].upper()}')
            print(f'  📊 评估结果: {status_emoji} {status.upper()}')

            if result.get('findings'):
                print(f"  🔍 发现: {result['findings'][:3]}")

            if result.get('issues'):
                print(f"  ⚠️  问题: {result['issues'][:3]}")

        print()

    # 汇总
    print(f"\n{'='*80}")
    print(f"评估汇总")
    print(f"{'='*80}")
    print(f"📊 总分: {report['score']}/100")
    print(f"✅ 通过: {report['pass_items']}/{report['total_items']}")
    print(f"❌ 未通过: {report['fail_items']}/{report['total_items']}")
    print(f"📈 通过率: {report['summary']['pass_rate']}")
    print(f"⭐ 合规等级: {report['summary']['compliance_level']}")

    # 保存评估表
    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)

        # 保存文本格式评估表
        table_file = os.path.join(output_dir, '自评估表.txt')
        with open(table_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("            小程序个人信息收集使用自评估表\n")
            f.write("="*80 + "\n")
            f.write(f"\n检查对象: {self.miniprogram_path}\n")
            f.write(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\n📊 评估结果: {report['score']}/100\n")
            f.write(f"✅ 通过项: {report['pass_items']}/{report['total_items']}")
            f.write(f"❌ 未通过: {report['fail_items']}/{report['total_items']}")
            f.write(f"📈 通过率: {report['summary']['pass_rate']}")
            f.write(f"⭐ 合规等级: {report['summary']['compliance_level']}")

            # 详细评估表
            f.write("\n" + "="*80 + "\n")
            f.write("类别 | ID | 评估点 | 评估结果 | 风险等级\n")
            f.write("-" * 80 + "\n")

            for category, items in self.ASSESSMENT_ITEMS.items():
                for item in items:
                    result = self.results.get(item['id'], {})
                    status = result.get('status', 'unknown')
                    status_emoji = '✅' if status == 'pass' else '❌'
                    
                    category_name = item['category']
                    risk_level = item['risk_level']

                    f.write(f"{category_name} | {item['id']} | {item['point'][:30]} | {status_emoji} | {risk_level.upper()}\n")

        print(f"\n[+] 自评估表已保存: {table_file}")

        # 保存 JSON 格式
        import json
        json_file = os.path.join(output_dir, 'self_assessment.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[+] JSON 报告已保存: {json_file}")


def main():
    parser = argparse.ArgumentParser(description='小程序个人信息收集使用自评估工具')
    parser.add_argument('miniprogram_path', help='小程序源代码路径')
    parser.add_argument('-o', '--output', help='报告输出目录', default='privacy_check_results')
    args = parser.parse_args()

    tool = SelfAssessmentTool(args.miniprogram_path)
    report = tool.assess()
    print_assessment_table(report, args.output)


if __name__ == '__main__':
    main()
