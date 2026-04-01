#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序隐私合规检查技能 - 主包
"""

__version__ = "3.3.0"
__author__ = "小红🌸"
__description__ = "微信小程序个人信息保护合规性检查工具包（AI 增强版）"

from .checkers import (
    PermissionChecker,
    APIScanner,
    DataflowAnalyzer,
    DebugChecker,
    LogLeakChecker,
    PrivacyPolicyChecker,
    PrivacyNamingChecker,
    SDKDetector,
    HybridChecker
)

from .analyzers import (
    AIAgentEngine,
    CodeAnalyzer,
    RiskAnalyzer
)

from .generators import (
    ReportGenerator,
    SummaryGenerator,
    PermissionConfirmationGenerator,
    SelfAssessmentGenerator,
    DetailedPermissionReportGenerator,
    WordReportGenerator
)

from .fillers import (
    ExcelFiller,
    AIExcelFiller,
    WordFiller
)

from .utils import (
    Unpacker,
    PermissionDefinitions,
    Config,
    Logger
)

__all__ = [
    # Checkers
    'PermissionChecker',
    'APIScanner',
    'DataflowAnalyzer',
    'DebugChecker',
    'LogLeakChecker',
    'PrivacyPolicyChecker',
    'PrivacyNamingChecker',
    'SDKDetector',
    'HybridChecker',
    # Analyzers
    'AIAgentEngine',
    'CodeAnalyzer',
    'RiskAnalyzer',
    # Generators
    'ReportGenerator',
    'SummaryGenerator',
    'PermissionConfirmationGenerator',
    'SelfAssessmentGenerator',
    'DetailedPermissionReportGenerator',
    'WordReportGenerator',
    # Fillers
    'ExcelFiller',
    'AIExcelFiller',
    'WordFiller',
    # Utils
    'Unpacker',
    'PermissionDefinitions',
    'Config',
    'Logger',
]
