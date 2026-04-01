#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 增强型隐私检测引擎（混合架构）
结合静态规则和 AI 智能体，实现全面的隐私风险检测
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class StaticRuleEngine:
    """静态规则引擎 - 快速扫描已知问题"""

    # 微信官方敏感 API
    WECHAT_SENSITIVE_APIS = {
        # 用户信息
        'wx.getUserInfo': '用户信息',
        'wx.getUserProfile': '用户资料',
        'wx.getPhoneNumber': '手机号码',
        'wx.chooseContact': '联系人',

        # 位置信息
        'wx.getLocation': '地理位置',
        'wx.chooseLocation': '地理位置',
        'wx.startLocationUpdate': '地理位置',
        'wx.onLocationChange': '地理位置',

        # 设备信息
        'wx.getSystemInfo': '系统信息',
        'wx.getSystemInfoSync': '系统信息',
        'wx.getNetworkType': '网络类型',

        # 媒体信息
        'wx.chooseImage': '图片',
        'wx.chooseMedia': '媒体文件',
        'wx.chooseMessageFile': '文件',
        'wx.chooseVideo': '视频',

        # 录音
        'wx.startRecord': '录音',
        'wx.getRecorderManager': '录音管理器',
        'wx.getBackgroundAudioManager': '背景音频',

        # 剪贴板
        'wx.getClipboardData': '剪贴板数据',
        'wx.setClipboardData': '剪贴板数据',

        # 蓝牙
        'wx.openBluetoothAdapter': '蓝牙适配器',
        'wx.getBluetoothDevices': '蓝牙设备',

        # 其他
        'wx.scanCode': '扫码',
        'wx.navigateTo': '页面跳转',
    }

    # 数据收集关键词
    DATA_COLLECTION_KEYWORDS = [
        'collect', 'gather', 'track', 'monitor',
        'record', 'log', 'capture', 'harvest',
        '收集', '采集', '追踪', '监控'
    ]

    # 隐私相关词汇
    PRIVACY_KEYWORDS = [
        'privacy', 'personal', 'user', 'profile',
        '隐私', '个人', '用户', '资料'
    ]

    def __init__(self):
        """初始化静态规则引擎"""
        self.findings = []

    def scan(self, code: str, file_path: str = None) -> List[Dict]:
        """
        快速扫描代码中的已知隐私风险

        Args:
            code: 代码内容
            file_path: 文件路径

        Returns:
            检测到的问题列表
        """
        self.findings = []

        # 扫描微信敏感 API
        self._scan_wechat_apis(code, file_path)

        # 扫描数据收集模式
        self._scan_data_collection_patterns(code, file_path)

        # 扫描硬编码敏感数据
        self._scan_hardcoded_secrets(code, file_path)

        return self.findings

    def _scan_wechat_apis(self, code: str, file_path: str):
        """扫描微信敏感 API 调用"""
        for api, description in self.WECHAT_SENSITIVE_APIS.items():
            # 正则匹配 API 调用
            pattern = rf'{re.escape(api)}\s*\('
            matches = re.finditer(pattern, code)

            for match in matches:
                line_num = code[:match.start()].count('\n') + 1

                self.findings.append({
                    'type': 'known_api_call',
                    'severity': 'medium',
                    'api': api,
                    'description': f'检测到敏感 API 调用: {api} ({description})',
                    'file': file_path,
                    'line': line_num,
                    'confidence': 'high',
                    'source': 'static_rule'
                })

    def _scan_data_collection_patterns(self, code: str, file_path: str):
        """扫描数据收集模式"""
        for keyword in self.DATA_COLLECTION_KEYWORDS:
            # 匹配函数名或变量名包含关键词
            pattern = rf'\b\w*{re.escape(keyword)}\w*\s*\('
            matches = re.finditer(pattern, code, re.IGNORECASE)

            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                func_call = match.group(0)

                # 检查是否与隐私相关
                has_privacy_context = any(
                    kw in code[max(0, match.start()-200):match.end()+200]
                    for kw in self.PRIVACY_KEYWORDS
                )

                if has_privacy_context:
                    self.findings.append({
                        'type': 'data_collection_pattern',
                        'severity': 'low',
                        'pattern': func_call,
                        'description': f'检测到疑似数据收集: {func_call}',
                        'file': file_path,
                        'line': line_num,
                        'confidence': 'medium',
                        'source': 'static_rule'
                    })

    def _scan_hardcoded_secrets(self, code: str, file_path: str):
        """扫描硬编码的敏感数据"""
        # 检测 API Key
        apikey_patterns = [
            r'api[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'secret["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'token["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
        ]

        for pattern in apikey_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1

                self.findings.append({
                    'type': 'hardcoded_secret',
                    'severity': 'critical',
                    'description': f'检测到硬编码的敏感数据: {match.group(0)[:50]}...',
                    'file': file_path,
                    'line': line_num,
                    'confidence': 'high',
                    'source': 'static_rule'
                })


class AIAgentEngine:
    """AI 智能体引擎 - 深度分析未知风险"""

    def __init__(self):
        """初始化 AI 引擎"""
        self.findings = []
        self.llm_available = self._check_llm_available()

    def _check_llm_available(self) -> bool:
        """检查 LLM 是否可用"""
        # 暂时返回 False，使用启发式分析
        return False

    def analyze(self, code: str, file_path: str = None, context: Dict = None) -> List[Dict]:
        """
        使用 AI 深度分析代码中的隐私风险

        Args:
            code: 代码内容
            file_path: 文件路径
            context: 上下文信息（如其他文件的分析结果）

        Returns:
            检测到的问题列表
        """
        self.findings = []

        # 如果 LLM 不可用，使用启发式分析
        if not self.llm_available:
            return self._heuristic_analysis(code, file_path, context)

        # 使用 LLM 进行深度分析
        return self._llm_analysis(code, file_path, context)

    def _heuristic_analysis(self, code: str, file_path: str, context: Dict) -> List[Dict]:
        """启发式分析（当 LLM 不可用时）"""

        # 1. 语义分析 - 理解代码意图
        self._semantic_analysis(code, file_path)

        # 2. 数据流追踪 - 追踪敏感数据
        self._dataflow_tracing(code, file_path)

        # 3. 模式识别 - 识别可疑模式
        self._pattern_recognition(code, file_path)

        # 4. 动态调用检测 - 检测动态构建的 API 调用
        self._dynamic_call_detection(code, file_path)

        # 5. 第三方库分析 - 检测第三方 SDK
        self._third_party_analysis(code, file_path)

        return self.findings

    def _semantic_analysis(self, code: str, file_path: str):
        """语义分析 - 理解代码意图"""
        lines = code.split('\n')

        for line_num, line in enumerate(lines, 1):
            # 识别数据收集意图
            if any(word in line for word in ['收集', '采集', 'collect', 'gather']):
                # 检查是否说明用途
                if 'for' in line or '用于' in line or 'purpose' in line:
                    # 有说明用途，风险较低
                    continue

                # 无说明用途，标记为潜在风险
                self.findings.append({
                    'type': 'unclear_data_collection',
                    'severity': 'medium',
                    'description': f'检测到数据收集但未说明用途: {line.strip()[:80]}',
                    'file': file_path,
                    'line': line_num,
                    'confidence': 'medium',
                    'source': 'ai_heuristic'
                })

        # 新增：检测数据发送但未加密
        send_pattern = r'(wx\.request|http\.post|fetch)\s*\([^)]*url[^)]*\)'
        for match in re.finditer(send_pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            code_snippet = code[max(0, match.start()-100):match.end()+100]

            # 检查是否使用 HTTPS
            if 'https' not in code_snippet.lower():
                self.findings.append({
                    'type': 'insecure_data_transmission',
                    'severity': 'high',
                    'description': '检测到数据发送但未使用 HTTPS（可能存在中间人攻击风险）',
                    'file': file_path,
                    'line': line_num,
                    'confidence': 'medium',
                    'source': 'ai_heuristic'
                })

    def _dataflow_tracing(self, code: str, file_path: str):
        """数据流追踪 - 追踪敏感数据的使用"""
        # 简化版数据流追踪
        # 追踪变量从定义到使用的路径

        # 1. 找到敏感数据收集点
        sensitive_vars = set()
        for match in re.finditer(r'(const|let|var)\s+(\w+)\s*=.*?(getUserInfo|getLocation|chooseContact)', code):
            var_name = match.group(2)
            sensitive_vars.add(var_name)

        # 2. 追踪这些变量的使用
        for var_name in sensitive_vars:
            # 查找变量的所有使用
            pattern = rf'\b{re.escape(var_name)}\b'
            matches = list(re.finditer(pattern, code))

            if len(matches) > 2:  # 除了定义，还有其他使用
                # 数据被传递或使用，需要检查
                for match in matches[1:]:  # 跳过定义
                    line_num = code[:match.start()].count('\n') + 1
                    line = code.split('\n')[line_num - 1]

                    # 检查是否安全传输
                    if 'https' in line.lower() or 'encrypt' in line.lower():
                        # 安全传输
                        continue

                    # 可能的风险
                    self.findings.append({
                        'type': 'sensitive_data_usage',
                        'severity': 'medium',
                        'description': f'敏感数据 {var_name} 被使用，需确认是否安全处理',
                        'file': file_path,
                        'line': line_num,
                        'confidence': 'medium',
                        'source': 'ai_heuristic'
                    })

    def _pattern_recognition(self, code: str, file_path: str):
        """模式识别 - 识别可疑模式"""

        # 1. 间接调用模式
        indirect_call_pattern = r'\w+\[\s*["\'].*?(?:user|location|contact|info)["\'].*?\]\s*\('
        for match in re.finditer(indirect_call_pattern, code, re.IGNORECASE):
            line_num = code[:match.start()].count('\n') + 1

            self.findings.append({
                'type': 'indirect_api_call',
                'severity': 'high',
                'description': f'检测到间接 API 调用，可能是动态调用: {match.group(0)[:60]}',
                'file': file_path,
                'line': line_num,
                'confidence': 'medium',
                'source': 'ai_heuristic'
            })

        # 2. 第三方库隐私风险
        third_party_pattern = r'(require|import)\s*\(\s*["\'].*?(?:analytics|tracking|monitoring|ads)["\']'
        for match in re.finditer(third_party_pattern, code, re.IGNORECASE):
            line_num = code[:match.start()].count('\n') + 1
            lib_name = match.group(0)

            self.findings.append({
                'type': 'third_party_privacy_risk',
                'severity': 'high',
                'description': f'检测到第三方库可能涉及隐私收集: {lib_name}',
                'file': file_path,
                'line': line_num,
                'confidence': 'medium',
                'source': 'ai_heuristic'
            })

    def _dynamic_call_detection(self, code: str, file_path: str):
        """动态调用检测 - 检测动态构建的 API 调用"""

        # 检测模式 1: 字符串拼接
        concat_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*["\'][\w]+["\']\s*\+\s*["\'][\w]+["\']'
        for match in re.finditer(concat_pattern, code):
            var_name = match.group(1)
            # 查找这个变量是否被用作 API 调用
            usage_pattern = rf'wx\[\s*{re.escape(var_name)}\s*\]'
            if re.search(usage_pattern, code):
                line_num = code[:match.start()].count('\n') + 1

                self.findings.append({
                    'type': 'dynamic_api_call',
                    'severity': 'high',
                    'description': f'检测到动态构建的 API 调用: {var_name}（可能绕过静态检测）',
                    'file': file_path,
                    'line': line_num,
                    'confidence': 'high',
                    'source': 'ai_heuristic'
                })

        # 检测模式 2: 数组/对象属性访问（放宽匹配）
        bracket_pattern = r'wx\[[^\]]+\]'
        for match in re.finditer(bracket_pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            call_content = match.group(0)

            # 排除简单的字符串字面量
            if re.match(r'wx\[\s*["\'][\w]+["\']\s*\]', call_content):
                # 这是简单的属性访问，可能是合法的
                # 但仍然需要标记，因为它可能包含敏感 API
                if any(keyword in call_content for keyword in ['user', 'location', 'info', 'contact']):
                    self.findings.append({
                        'type': 'bracket_notation_call',
                        'severity': 'medium',
                        'description': f'使用括号表示法调用 API（可能隐藏真实意图）: {call_content}',
                        'file': file_path,
                        'line': line_num,
                        'confidence': 'low',
                        'source': 'ai_heuristic'
                    })
            else:
                # 复杂的表达式，高风险
                self.findings.append({
                    'type': 'complex_dynamic_call',
                    'severity': 'high',
                    'description': f'检测到复杂的动态 API 调用（可能绕过静态检测）: {call_content}',
                    'file': file_path,
                    'line': line_num,
                    'confidence': 'high',
                    'source': 'ai_heuristic'
                })

    def _third_party_analysis(self, code: str, file_path: str):
        """第三方库分析 - 深度分析第三方 SDK"""

        # 已知隐私相关的第三方库
        privacy_libraries = {
            'analytics': '数据分析',
            'tracking': '用户追踪',
            'monitoring': '行为监控',
            'advertising': '广告投放',
            'ads': '广告',
            'statistics': '统计分析',
            'behavior': '行为分析',
        }

        # 扩展的导入检测
        import_patterns = [
            r'(?:require|import)\s*\(\s*["\'].*?({})["\']'.format('|'.join(privacy_libraries.keys())),
            r'(?:from)\s+["\'].*?({})["\']'.format('|'.join(privacy_libraries.keys())),
        ]

        for pattern in import_patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                line_num = code[:match.start()].count('\n') + 1
                lib_info = match.group(0)

                # 识别是哪种类型的库
                lib_type = 'unknown'
                for keyword, desc in privacy_libraries.items():
                    if keyword in lib_info.lower():
                        lib_type = desc
                        break

                self.findings.append({
                    'type': 'third_party_sdk',
                    'severity': 'high',
                    'description': f'检测到第三方库: {lib_info}（{lib_type}）',
                    'file': file_path,
                    'line': line_num,
                    'risk_detail': f'该库可能收集用户数据，需查看隐私政策',
                    'confidence': 'high',
                    'source': 'ai_heuristic'
                })

    def _llm_analysis(self, code: str, file_path: str, context: Dict) -> List[Dict]:
        """使用 LLM 进行深度分析"""

        # TODO: 实际的 LLM 调用
        # 这里是示例代码，需要根据实际使用的 LLM API 进行调整

        # 示例 prompt
        prompt = f"""
分析以下小程序代码的隐私风险：

文件: {file_path}
代码:
{code[:2000]}

请检查：
1. 是否收集用户数据？
2. 收集了哪些数据？
3. 是否有用户授权？
4. 数据如何使用和传输？
5. 是否存在隐私风险？

以 JSON 格式返回检测结果。
"""

        # 调用 LLM（示例）
        # response = llm.complete(prompt)
        # findings = parse_llm_response(response)

        # 暂时返回空，等待实际 LLM 集成
        return []


class HybridPrivacyChecker:
    """混合架构隐私检测器"""

    def __init__(self):
        """初始化混合检测器"""
        self.static_engine = StaticRuleEngine()
        self.ai_engine = AIAgentEngine()
        self.all_findings = []

    def check(self, code: str, file_path: str = None, context: Dict = None) -> Dict:
        """
        使用混合架构检测隐私风险

        Args:
            code: 代码内容
            file_path: 文件路径
            context: 上下文信息

        Returns:
            检测结果
        """
        print(f"[*] 混合架构检测: {file_path or '未知文件'}")

        # 阶段 1: 静态规则快速扫描
        print("  [-] 阶段 1/2: 静态规则扫描...")
        static_findings = self.static_engine.scan(code, file_path)
        print(f"  [+] 发现 {len(static_findings)} 个已知问题")

        # 阶段 2: AI 深度分析
        print("  [-] 阶段 2/2: AI 深度分析...")
        ai_findings = self.ai_engine.analyze(code, file_path, context)
        print(f"  [+] 发现 {len(ai_findings)} 个潜在风险")

        # 合并结果
        self.all_findings = static_findings + ai_findings

        # 去重和分析
        result = {
            'total_findings': len(self.all_findings),
            'static_findings': len(static_findings),
            'ai_findings': len(ai_findings),
            'findings': self._merge_findings(self.all_findings),
            'summary': self._generate_summary()
        }

        return result

    def _merge_findings(self, findings: List[Dict]) -> List[Dict]:
        """合并和去重检测结果"""
        # 按文件和行号去重
        unique = {}
        for finding in findings:
            key = (finding.get('file'), finding.get('line'), finding.get('type'))
            if key not in unique:
                unique[key] = finding
            else:
                # 如果已存在，保留置信度更高的
                if finding.get('confidence') == 'high':
                    unique[key] = finding

        # 按严重程度排序
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_findings = sorted(
            unique.values(),
            key=lambda x: severity_order.get(x.get('severity', 'low'), 4)
        )

        return sorted_findings

    def _generate_summary(self) -> Dict:
        """生成检测摘要"""
        summary = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'by_source': {
                'static_rule': 0,
                'ai_heuristic': 0,
                'ai_llm': 0
            }
        }

        for finding in self.all_findings:
            severity = finding.get('severity', 'low')
            summary[severity] = summary.get(severity, 0) + 1

            source = finding.get('source', 'unknown')
            summary['by_source'][source] = summary['by_source'].get(source, 0) + 1

        return summary


def main():
    """测试混合检测器"""
    # 示例代码
    test_code = """
    // 测试代码
    const userInfo = wx.getUserInfo()  // 已知 API
    const location = wx.getLocation()  // 已知 API

    // 动态调用
    const apiName = 'get' + 'User' + 'Profile'
    const data = wx[apiName]()

    // 第三方库
    const analytics = require('analytics-sdk')
    analytics.init({ collect: true })

    // 硬编码密钥
    const apiKey = 'sk-1234567890abcdefghijklmnopqrstuvwxyz'
    """

    # 创建检测器
    checker = HybridPrivacyChecker()

    # 执行检测
    result = checker.check(test_code, 'test.js')

    # 输出结果
    print("\n" + "="*70)
    print("检测结果")
    print("="*70)
    print(f"\n总发现: {result['total_findings']}")
    print(f"  - 静态规则: {result['static_findings']}")
    print(f"  - AI 分析: {result['ai_findings']}")
    print(f"\n严重程度分布:")
    print(f"  - 严重: {result['summary']['critical']}")
    print(f"  - 高: {result['summary']['high']}")
    print(f"  - 中: {result['summary']['medium']}")
    print(f"  - 低: {result['summary']['low']}")
    print(f"\n来源分布:")
    print(f"  - 静态规则: {result['summary']['by_source']['static_rule']}")
    print(f"  - AI 启发式: {result['summary']['by_source']['ai_heuristic']}")

    print(f"\n详细发现:")
    for i, finding in enumerate(result['findings'], 1):
        print(f"\n{i}. {finding['description']}")
        print(f"   类型: {finding['type']}")
        print(f"   严重程度: {finding['severity']}")
        print(f"   置信度: {finding['confidence']}")
        print(f"   来源: {finding['source']}")
        print(f"   位置: {finding['file']}:{finding['line']}")


if __name__ == '__main__':
    main()
