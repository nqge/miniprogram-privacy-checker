#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成器模块
"""

from .report import ReportGenerator
from .summary import SummaryGenerator
from .permission_confirmation import PermissionConfirmationGenerator
from .self_assessment import SelfAssessmentGenerator
from .detailed_permission import DetailedPermissionReportGenerator
from .word_report import WordReportGenerator

__all__ = [
    'ReportGenerator',
    'SummaryGenerator',
    'PermissionConfirmationGenerator',
    'SelfAssessmentGenerator',
    'DetailedPermissionReportGenerator',
    'WordReportGenerator',
]
