#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试混合检测器的增强功能
"""

import sys
sys.path.append('/root/.openclaw/workspace/skills/miniprogram-privacy/core')

from hybrid_checker import HybridPrivacyChecker

# 更全面的测试代码
test_code_v2 = """
// 页面配置
Page({
    data: {
        userInfo: null,
        location: null
    },

    onLoad() {
        // 场景 1: 直接调用已知 API
        wx.getUserInfo({
            success: (res) => {
                this.setData({ userInfo: res.userInfo })
            }
        })

        // 场景 2: 动态调用（绕过静态检测）
        const apiName = 'get' + 'Location'
        wx[apiName]({
            success: (res) => {
                this.setData({ location: res })
            }
        })

        // 场景 3: 第三方库
        const analytics = require('analytics-sdk')
        analytics.init({
            appId: 'xxx',
            collectUserBehavior: true,  // 收集用户行为
            autoTrack: true
        })

        // 场景 4: 数据收集但不说明用途
        function collectUserData() {
            const data = {
                age: this.data.age,
                gender: this.data.gender
            }
            // 没有说明用途，直接发送
            wx.request({
                url: 'https://api.example.com/collect',
                data: data
            })
        }

        // 场景 5: 硬编码密钥
        const API_KEY = 'sk-1234567890abcdefghijklmnopqrstuv'

        // 场景 6: 敏感数据传递
        const sensitiveData = wx.getStorageSync('sensitive_info')
        someThirdPartyLib.send(sensitiveData)
    }
})
"""

# 创建检测器
checker = HybridPrivacyChecker()

# 执行检测
result = checker.check(test_code_v2, 'page.js')

# 输出结果
print("\n" + "="*70)
print("混合架构检测结果 v2.0")
print("="*70)
print(f"\n总发现: {result['total_findings']}")
print(f"  - 静态规则: {result['static_findings']}")
print(f"  - AI 分析: {result['ai_findings']}")
print(f"\n严重程度分布:")
print(f"  - 严重 (Critical): {result['summary']['critical']}")
print(f"  - 高 (High): {result['summary']['high']}")
print(f"  - 中 (Medium): {result['summary']['medium']}")
print(f"  - 低 (Low): {result['summary']['low']}")
print(f"\n来源分布:")
print(f"  - 静态规则: {result['summary']['by_source']['static_rule']}")
print(f"  - AI 启发式: {result['summary']['by_source']['ai_heuristic']}")

print(f"\n{'='*70}")
print("详细发现")
print("="*70)

for i, finding in enumerate(result['findings'], 1):
    severity_icon = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }.get(finding['severity'], '⚪')

    source_icon = {
        'static_rule': '📜',
        'ai_heuristic': '🤖',
        'ai_llm': '🧠'
    }.get(finding['source'], '❓')

    print(f"\n{i}. {severity_icon} {finding['description']}")
    print(f"   类型: {finding['type']}")
    print(f"   严重程度: {finding['severity']}")
    print(f"   置信度: {finding['confidence']}")
    print(f"   来源: {source_icon} {finding['source']}")
    print(f"   位置: {finding['file']}:{finding['line']}")

# 对比分析
print("\n" + "="*70)
print("对比分析")
print("="*70)

static_only = [f for f in result['findings'] if f['source'] == 'static_rule']
ai_only = [f for f in result['findings'] if f['source'] == 'ai_heuristic']

print(f"\n只有静态规则发现的: {len(static_only)} 个")
print(f"只有 AI 发现的: {len(ai_only)} 个")

if ai_only:
    print(f"\n✨ AI 额外发现的风险（静态规则无法检测）:")
    for i, finding in enumerate(ai_only, 1):
        print(f"\n  {i}. {finding['description']}")
        print(f"     类型: {finding['type']}")
        print(f"     严重程度: {finding['severity']}")
