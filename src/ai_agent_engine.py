#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 智能体引擎 - 深度分析未知的隐私风险
使用 LLM 进行代码语义分析和风险评估
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AIAgentEngine:
    """AI 智能体引擎"""

    def __init__(self, model: str = "glm-4-flash", enable_ai: bool = True):
        """
        初始化 AI 智能体引擎

        Args:
            model: LLM 模型名称
            enable_ai: 是否启用 AI 分析（False 时使用规则引擎）
        """
        self.model = model
        self.enable_ai = enable_ai
        self.prompt_templates = {
            'code_analysis': """
分析以下小程序代码，识别隐私风险：

{code}

请检查：
1. 是否收集用户数据？
2. 收集了哪些数据？
3. 是否有授权？
4. 数据如何使用？

返回 JSON 格式：
{{
    "risks": [
        {{
            "type": "数据收集",
            "severity": "高",
            "description": "描述",
            "evidence": ["代码片段1", "代码片段2"],
            "suggestion": "修复建议"
        }}
    ],
    "confidence": 0.8,
    "summary": "总体评估"
}}
""",
            'permission_analysis': """
分析以下权限检查结果，生成权限确认总结：

{check_results}

请生成：
1. 权限使用情况总结
2. 必要性分析
3. 风险评估

返回 JSON 格式：
{{
    "summary": "权限使用总结",
    "necessary_permissions": [...],
    "unnecessary_permissions": [...],
    "risk_assessment": "风险评估"
}}
""",
            'assessment_analysis': """
分析以下自评估检查结果，生成个人信息保护总结：

{check_results}

请生成：
1. 个人信息收集情况
2. 保护措施评估
3. 合规性总结

返回 JSON 格式：
{{
    "collection_summary": "收集情况总结",
    "protection_measures": [...],
    "compliance_summary": "合规性总结"
}}
"""
        }

    def analyze_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        分析代码语义

        Args:
            code: 代码内容
            context: 上下文信息

        Returns:
            分析结果字典
        """
        if not self.enable_ai:
            return self._rule_based_analysis(code, context)

        logger.info("使用 AI 智能体分析代码...")

        # 构建提示词
        prompt = self.prompt_templates['code_analysis'].format(code=code[:5000])  # 限制长度

        try:
            # 调用 LLM（这里需要根据实际情况实现）
            # result = self._call_llm(prompt)
            # return json.loads(result)

            # 临时返回模拟结果
            return {
                "risks": [],
                "confidence": 0.0,
                "summary": "AI 分析未启用"
            }
        except Exception as e:
            logger.error(f"AI 分析失败: {e}")
            return self._rule_based_analysis(code, context)

    def _rule_based_analysis(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        基于规则的分析（后备方案）

        Args:
            code: 代码内容
            context: 上下文信息

        Returns:
            分析结果字典
        """
        logger.info("使用规则引擎分析代码...")

        risks = []
        confidence = 0.5

        # 检测敏感 API
        sensitive_patterns = {
            r'wx\.getLocation': {
                'type': '位置信息收集',
                'severity': '中',
                'description': '检测到获取用户位置的 API 调用',
                'suggestion': '需要在 app.json 中声明权限，并在调用前获得用户授权'
            },
            r'wx\.chooseImage|wx\.chooseMedia': {
                'type': '相册访问',
                'severity': '中',
                'description': '检测到访问相册的 API 调用',
                'suggestion': '需要在调用前获得用户授权'
            },
            r'wx\.getUserInfo|getUserProfile': {
                'type': '用户信息收集',
                'severity': '高',
                'description': '检测到获取用户信息的 API 调用',
                'suggestion': '必须在用户主动触发后调用，并获得明确授权'
            },
            r'wx\.getPhoneNumber|getBindPhoneNumber': {
                'type': '手机号收集',
                'severity': '高',
                'description': '检测到获取手机号的 API 调用',
                'suggestion': '需要用户主动触发，且不能在进入小程序时直接弹窗'
            },
            r'wx\.startRecord|RecorderManager': {
                'type': '录音功能',
                'severity': '中',
                'description': '检测到录音功能的 API 调用',
                'suggestion': '需要在调用前获得用户授权'
            },
        }

        for pattern, risk_info in sensitive_patterns.items():
            matches = re.findall(pattern, code)
            if matches:
                risks.append({
                    **risk_info,
                    'evidence': [f"发现 {len(matches)} 次调用"],
                    'count': len(matches)
                })
                confidence += 0.1

        return {
            "risks": risks,
            "confidence": min(confidence, 1.0),
            "summary": f"通过规则引擎发现 {len(risks)} 个潜在风险"
        }

    def discover_unknown_patterns(self, code: str) -> List[Dict[str, Any]]:
        """
        发现未知的隐私风险模式

        Args:
            code: 代码内容

        Returns:
            未知风险模式列表
        """
        logger.info("发现未知隐私风险模式...")

        unknown_patterns = []

        # 检测动态 API 调用
        dynamic_api_calls = re.findall(r'wx\[[^\]]+\]', code)
        if dynamic_api_calls:
            unknown_patterns.append({
                'type': '动态 API 调用',
                'severity': '中',
                'description': '检测到动态构建的 API 调用',
                'evidence': dynamic_api_calls[:5],
                'suggestion': '建议使用静态 API 调用，便于审查和维护'
            })

        # 检测数据聚合
        if re.search(r'collectAge|collectGender|collectLocation', code):
            unknown_patterns.append({
                'type': '数据聚合',
                'severity': '高',
                'description': '可能在进行用户画像数据聚合',
                'evidence': ['检测到多个数据收集调用'],
                'suggestion': '确保数据收集符合最小必要原则，避免过度收集'
            })

        # 检测第三方库
        third_party_libs = re.findall(r'require\(["\']([^"\']+)["\']\)', code)
        privacy_related_libs = [lib for lib in third_party_libs if any(keyword in lib.lower() for keyword in ['analytics', 'tracking', 'ad', 'stat'])]

        if privacy_related_libs:
            unknown_patterns.append({
                'type': '第三方隐私库',
                'severity': '中',
                'description': '检测到可能涉及隐私的第三方库',
                'evidence': privacy_related_libs,
                'suggestion': '请检查第三方库的隐私政策，确保符合规范'
            })

        return unknown_patterns

    def analyze_permission_summary(self, permission_check_file: Path) -> Dict[str, Any]:
        """
        分析权限检查结果，生成权限确认总结

        Args:
            permission_check_file: 权限检查结果文件

        Returns:
            权限总结字典
        """
        logger.info("分析权限检查结果...")

        try:
            with open(permission_check_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"加载权限检查结果失败: {e}")
            return {
                "summary": "无法加载权限检查结果",
                "necessary_permissions": [],
                "unnecessary_permissions": [],
                "risk_assessment": "未知"
            }

        # 提取已声明和使用的权限
        declared_permissions = data.get('declared_permissions', {})
        used_permissions = data.get('used_permissions', {})

        # 分析必要性
        necessary = []
        unnecessary = []

        for perm_name, perm_info in used_permissions.items():
            if perm_name in declared_permissions:
                necessary.append({
                    'name': perm_name,
                    'purpose': perm_info.get('purpose', '未说明'),
                    'usage': perm_info.get('count', 0)
                })
            else:
                unnecessary.append({
                    'name': perm_name,
                    'purpose': perm_info.get('purpose', '未说明'),
                    'usage': perm_info.get('count', 0),
                    'suggestion': f'需要在 app.json 中声明 {perm_name} 权限'
                })

        # 风险评估
        total_risks = len(unnecessary)
        if total_risks == 0:
            risk_assessment = "低风险 - 所有权限均已正确声明"
        elif total_risks <= 2:
            risk_assessment = "中风险 - 部分权限未声明，建议补充"
        else:
            risk_assessment = "高风险 - 多个权限未声明，存在合规风险"

        return {
            "summary": f"共使用 {len(used_permissions)} 项权限，其中 {len(necessary)} 项已声明，{len(unnecessary)} 项未声明",
            "necessary_permissions": necessary,
            "unnecessary_permissions": unnecessary,
            "risk_assessment": risk_assessment
        }

    def analyze_assessment_summary(self, assessment_file: Path) -> Dict[str, Any]:
        """
        分析自评估检查结果，生成个人信息保护总结

        Args:
            assessment_file: 自评估检查结果文件

        Returns:
            自评估总结字典
        """
        logger.info("分析自评估检查结果...")

        try:
            with open(assessment_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"加载自评估结果失败: {e}")
            return {
                "collection_summary": "无法加载自评估结果",
                "protection_measures": [],
                "compliance_summary": "未知"
            }

        # 提取评估结果
        assessments = data.get('assessments', [])

        # 分类统计
        passed = sum(1 for a in assessments if a.get('result') == '符合')
        failed = sum(1 for a in assessments if a.get('result') == '不符合')
        partial = sum(1 for a in assessments if a.get('result') == '部分符合')

        # 提取保护措施
        protection_measures = []
        for a in assessments:
            if a.get('result') in ['符合', '部分符合']:
                measure = a.get('measure', a.get('description', ''))
                if measure:
                    protection_measures.append(measure)

        # 合规性总结
        total = len(assessments)
        if total == 0:
            compliance_summary = "无法评估"
        elif passed == total:
            compliance_summary = "完全合规 - 所有评估点均符合要求"
        elif passed / total >= 0.8:
            compliance_summary = "基本合规 - 大部分评估点符合要求，有少量改进空间"
        elif passed / total >= 0.6:
            compliance_summary = "部分合规 - 半数以上评估点符合要求，需要重点改进"
        else:
            compliance_summary = "合规性较低 - 多数评估点不符合要求，存在较大合规风险"

        # 收集情况总结
        collection_items = []
        for a in assessments:
            if '收集' in a.get('description', '') or '采集' in a.get('description', ''):
                collection_items.append(a.get('description', ''))

        collection_summary = f"共评估 {total} 个检查点，其中 {passed} 项符合，{partial} 项部分符合，{failed} 项不符合"
        if collection_items:
            collection_summary += f"。涉及个人信息收集的评估点 {len(collection_items)} 项"

        return {
            "collection_summary": collection_summary,
            "protection_measures": protection_measures[:10],  # 限制数量
            "compliance_summary": compliance_summary
        }

    def generate_report_section(self, section_type: str, check_results_dir: Path) -> str:
        """
        生成报告的特定章节内容

        Args:
            section_type: 章节类型（permission, assessment, privacy_policy, security）
            check_results_dir: 检查结果目录

        Returns:
            章节内容文本
        """
        logger.info(f"生成 {section_type} 章节内容...")

        if section_type == 'permission':
            # 权限申请章节
            perm_file = check_results_dir / 'permission_check.json'
            if perm_file.exists():
                summary = self.analyze_permission_summary(perm_file)
                return f"""
### 权限申请情况

{summary['summary']}

**已正确声明的权限**:
{chr(10).join([f"- {p['name']}: {p['purpose']}（使用 {p.get('usage', 0)} 次）" for p in summary['necessary_permissions']])}

**未声明的权限**:
{chr(10).join([f"- {p['name']}: {p['suggestion']}" for p in summary['unnecessary_permissions']]) if summary['unnecessary_permissions'] else '无'}

**风险评估**: {summary['risk_assessment']}
"""

        elif section_type == 'assessment':
            # 个人信息自评估章节
            assess_file = check_results_dir / 'self_assessment.json'
            if assess_file.exists():
                summary = self.analyze_assessment_summary(assess_file)
                return f"""
### 个人信息保护情况

{summary['collection_summary']}

**保护措施**:
{chr(10).join([f"- {m}" for m in summary['protection_measures']]) if summary['protection_measures'] else '无'}

**合规性总结**: {summary['compliance_summary']}
"""

        elif section_type == 'privacy_policy':
            # 隐私政策章节
            policy_file = check_results_dir / 'privacy_policy_check.json'
            if policy_file.exists():
                with open(policy_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                completeness = data.get('completeness', 0)
                missing_items = data.get('missing_items', [])

                return f"""
### 隐私政策完整性

**完整度**: {completeness}%

**缺失内容**:
{chr(10).join([f"- {item}" for item in missing_items]) if missing_items else '无'}

**建议**: 请根据《个人信息保护法》和平台要求，完善隐私政策内容
"""

        elif section_type == 'security':
            # 安全与第三方章节
            sdk_file = check_results_dir / 'sdk_detection.json'
            if sdk_file.exists():
                with open(sdk_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                sdks = data.get('sdks', [])
                return f"""
### 第三方 SDK 使用情况

**检测到的 SDK**: {len(sdks)}

{chr(10).join([f"- **{sdk['name']}**: {sdk.get('purpose', '用途未知')}" for sdk in sdks]) if sdks else '未检测到第三方 SDK'}

**建议**: 请检查第三方 SDK 的隐私政策，确保其数据处理行为符合规范
"""

        return "# 该章节内容生成失败"


if __name__ == '__main__':
    # 测试代码
    engine = AIAgentEngine(enable_ai=False)

    # 测试规则分析
    test_code = """
    wx.getLocation({
        type: 'wgs84',
        success: (res) => {
            console.log(res.latitude, res.longitude)
        }
    })

    wx.getUserInfo({
        success: (res) => {
            console.log(res.userInfo)
        }
    })
    """

    result = engine.analyze_code(test_code)
    print(json.dumps(result, ensure_ascii=False, indent=2))
