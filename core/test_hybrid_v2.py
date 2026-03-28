#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试混合检测器的完整功能
"""

import sys
sys.path.append('/root/.openclaw/workspace/skills/miniprogram-privacy/core')

from hybrid_checker import HybridPrivacyChecker

# 测试代码
test_cases = {
    'dynamic_call.js': """
// 测试动态调用
const apiName = 'get' + 'Location'
wx[apiName]()
""",

    'third_party.js': """
// 测试第三方库
const analytics = require('analytics-sdk')
analytics.init({ collect: true })
""",

    'complex.js': """
// 综合测试
Page({
    onLoad() {
        // 直接调用
        wx.getUserInfo()

        // 动态调用
        const method = 'getLocation'
        wx[method]()

        // 第三方库
        const tracking = require('user-tracking')
        tracking.start()
    }
})
"""
}

# 创建检测器
checker = HybridPrivacyChecker()

# 测试所有场景
all_results = {}

for file_name, code in test_cases.items():
    print(f"\n{'='*70}")
    print(f"测试文件: {file_name}")
    print('='*70)

    result = checker.check(code, file_name)
    all_results[file_name] = result

    print(f"\n总发现: {result['total_findings']}")
    print(f"  - 静态规则: {result['static_findings']}")
    print(f"  - AI 分析: {result['ai_findings']}")

    if result['findings']:
        print(f"\n详细发现:")
        for i, finding in enumerate(result['findings'], 1):
            print(f"\n  {i}. {finding['description']}")
            print(f"     类型: {finding['type']}")
            print(f"     严重程度: {finding['severity']}")
            print(f"     来源: {finding['source']}")

# 汇总统计
print(f"\n{'='*70}")
print("汇总统计")
print('='*70)

total_static = 0
total_ai = 0

for file_name, result in all_results.items():
    total_static += result['static_findings']
    total_ai += result['ai_findings']

print(f"\n总计发现:")
print(f"  - 静态规则: {total_static} 个")
print(f"  - AI 分析: {total_ai} 个")
print(f"  - 总计: {total_static + total_ai} 个")

if total_ai > 0:
    print(f"\n✨ AI 额外发现了 {total_ai} 个静态规则无法检测的风险！")
