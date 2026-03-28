#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试 AI 启发式分析
"""

from hybrid_checker import AIAgentEngine

# 简单测试代码
test_code = """
const apiName = 'get' + 'Location'
wx[apiName]()

const analytics = require('analytics-sdk')
"""

ai_engine = AIAgentEngine()
result = ai_engine.analyze(test_code, 'test.js')

print(f"AI 分析结果: {len(result)} 个发现")
for i, finding in enumerate(result, 1):
    print(f"\n{i}. {finding['description']}")
    print(f"   类型: {finding['type']}")
    print(f"   严重程度: {finding['severity']}")
