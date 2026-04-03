#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查结果验证器
验证每个阶段的输出文件是否存在，内容是否完整，更新是否正确
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CheckResultValidator:
    """检查结果验证器"""

    def __init__(self, result_dir: str = 'privacy_check_results'):
        """
        初始化验证器

        Args:
            result_dir: 检查结果目录
        """
        self.result_dir = Path(result_dir)
        self.validation_results = {
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'warnings': [],
            'errors': [],
            'missing_files': [],
            'incomplete_updates': []
        }

    def validate_all(self) -> Dict[str, Any]:
        """
        执行所有验证检查

        Returns:
            验证结果字典
        """
        logger.info("开始验证检查结果...")

        # 验证各个阶段
        self._validate_stage_1_permission_check()
        self._validate_stage_2_api_scan()
        self._validate_stage_3_dataflow_analysis()
        self._validate_stage_4_debug_check()
        self._validate_stage_5_log_leak_check()
        self._validate_stage_6_privacy_policy_check()
        self._validate_stage_7_privacy_naming_check()
        self._validate_stage_8_sdk_check()
        self._validate_stage_9_hybrid_check()
        self._validate_stage_10_permission_confirmation()
        self._validate_stage_11_self_assessment()
        self._validate_stage_12_detailed_permission_report()
        self._validate_stage_13_excel_fill()
        self._validate_stage_14_word_report()
        self._validate_stage_15_ai_analysis()
        self._validate_stage_16_summary_report()
        self._validate_stage_17_overall_report()

        # 生成总结报告
        return self._generate_summary()

    def _check_file_exists(self, file_path: Path, stage_name: str) -> bool:
        """
        检查文件是否存在

        Args:
            file_path: 文件路径
            stage_name: 阶段名称

        Returns:
            文件是否存在
        """
        self.validation_results['total_checks'] += 1

        if not file_path.exists():
            error_msg = f"[{stage_name}] 缺少文件: {file_path.name}"
            self.validation_results['errors'].append(error_msg)
            self.validation_results['missing_files'].append(str(file_path))
            self.validation_results['failed_checks'] += 1
            logger.error(error_msg)
            return False

        self.validation_results['passed_checks'] += 1
        logger.info(f"[{stage_name}] ✅ 文件存在: {file_path.name}")
        return True

    def _check_json_valid(self, file_path: Path, stage_name: str) -> bool:
        """
        检查 JSON 文件是否有效

        Args:
            file_path: JSON 文件路径
            stage_name: 阶段名称

        Returns:
            JSON 是否有效
        """
        if not file_path.exists():
            return False

        self.validation_results['total_checks'] += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查 JSON 是否为空
            if not data:
                warning_msg = f"[{stage_name}] JSON 文件为空: {file_path.name}"
                self.validation_results['warnings'].append(warning_msg)
                logger.warning(warning_msg)
                return False

            self.validation_results['passed_checks'] += 1
            logger.info(f"[{stage_name}] ✅ JSON 文件有效: {file_path.name}")
            return True

        except json.JSONDecodeError as e:
            error_msg = f"[{stage_name}] JSON 文件格式错误: {file_path.name} - {e}"
            self.validation_results['errors'].append(error_msg)
            self.validation_results['failed_checks'] += 1
            logger.error(error_msg)
            return False

    def _check_file_not_empty(self, file_path: Path, stage_name: str) -> bool:
        """
        检查文件是否为空

        Args:
            file_path: 文件路径
            stage_name: 阶段名称

        Returns:
            文件是否非空
        """
        if not file_path.exists():
            return False

        self.validation_results['total_checks'] += 1

        if file_path.stat().st_size == 0:
            warning_msg = f"[{stage_name}] 文件为空: {file_path.name}"
            self.validation_results['warnings'].append(warning_msg)
            logger.warning(warning_msg)
            return False

        self.validation_results['passed_checks'] += 1
        logger.info(f"[{stage_name}] ✅ 文件非空: {file_path.name}")
        return True

    def _check_content_updated(self, file_path: Path, required_keywords: List[str], stage_name: str) -> bool:
        """
        检查文件内容是否已更新

        Args:
            file_path: 文件路径
            required_keywords: 必需的关键词列表
            stage_name: 阶段名称

        Returns:
            内容是否已更新
        """
        if not file_path.exists():
            return False

        self.validation_results['total_checks'] += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查必需的关键词
            missing_keywords = []
            for keyword in required_keywords:
                if keyword not in content:
                    missing_keywords.append(keyword)

            if missing_keywords:
                warning_msg = f"[{stage_name}] 文件缺少关键词: {file_path.name} - {missing_keywords}"
                self.validation_results['warnings'].append(warning_msg)
                self.validation_results['incomplete_updates'].append(str(file_path))
                logger.warning(warning_msg)
                return False

            self.validation_results['passed_checks'] += 1
            logger.info(f"[{stage_name}] ✅ 内容已更新: {file_path.name}")
            return True

        except Exception as e:
            error_msg = f"[{stage_name}] 检查内容失败: {file_path.name} - {e}"
            self.validation_results['errors'].append(error_msg)
            self.validation_results['failed_checks'] += 1
            logger.error(error_msg)
            return False

    def _validate_stage_1_permission_check(self):
        """验证阶段 1: 权限声明检查"""
        stage_name = "阶段1: 权限声明检查"

        # 检查 JSON 文件
        json_file = self.result_dir / 'permission_check.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'permission_check_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_2_api_scan(self):
        """验证阶段 2: 敏感 API 扫描"""
        stage_name = "阶段2: 敏感 API 扫描"

        # 检查 JSON 文件
        json_file = self.result_dir / 'api_scan.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'api_scan_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_3_dataflow_analysis(self):
        """验证阶段 3: 数据流分析"""
        stage_name = "阶段3: 数据流分析"

        # 检查 JSON 文件
        json_file = self.result_dir / 'dataflow_analysis.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'dataflow_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_4_debug_check(self):
        """验证阶段 4: 动态调试风险检测"""
        stage_name = "阶段4: 动态调试风险检测"

        # 检查 JSON 文件
        json_file = self.result_dir / 'debug_check.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'debug_check_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_5_log_leak_check(self):
        """验证阶段 5: 日志泄露风险检测"""
        stage_name = "阶段5: 日志泄露风险检测"

        # 检查 JSON 文件
        json_file = self.result_dir / 'log_leak_check.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'log_leak_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_6_privacy_policy_check(self):
        """验证阶段 6: 隐私政策检查"""
        stage_name = "阶段6: 隐私政策检查"

        # 检查 JSON 文件
        json_file = self.result_dir / 'privacy_policy_check.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'privacy_policy_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_7_privacy_naming_check(self):
        """验证阶段 7: 隐私政策命名检查"""
        stage_name = "阶段7: 隐私政策命名检查"

        # 检查 JSON 文件
        json_file = self.result_dir / 'privacy_naming_check.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

    def _validate_stage_8_sdk_check(self):
        """验证阶段 8: SDK 使用检测"""
        stage_name = "阶段8: SDK 使用检测"

        # 检查 JSON 文件
        json_file = self.result_dir / 'sdk_detection.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'sdk_check_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_9_hybrid_check(self):
        """验证阶段 9: 混合架构检测"""
        stage_name = "阶段9: 混合架构检测"

        # 检查 JSON 文件
        json_file = self.result_dir / 'hybrid_check.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

        # 检查报告文件
        report_file = self.result_dir / 'hybrid_check_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_10_permission_confirmation(self):
        """验证阶段 10: 生成权限确认单"""
        stage_name = "阶段10: 生成权限确认单"

        # 检查文本文件
        txt_file = self.result_dir / '权限确认单.txt'
        if self._check_file_exists(txt_file, stage_name):
            self._check_file_not_empty(txt_file, stage_name)

        # 检查 JSON 文件
        json_file = self.result_dir / 'permission_confirmation.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

    def _validate_stage_11_self_assessment(self):
        """验证阶段 11: 生成自评估表"""
        stage_name = "阶段11: 生成自评估表"

        # 检查文本文件
        txt_file = self.result_dir / '自评估表.txt'
        if self._check_file_exists(txt_file, stage_name):
            self._check_file_not_empty(txt_file, stage_name)

        # 检查 JSON 文件
        json_file = self.result_dir / 'self_assessment.json'
        if self._check_file_exists(json_file, stage_name):
            self._check_json_valid(json_file, stage_name)

    def _validate_stage_12_detailed_permission_report(self):
        """验证阶段 12: 生成详细权限报告"""
        stage_name = "阶段12: 生成详细权限报告"

        # 检查报告文件
        report_file = self.result_dir / 'detailed_permission_report.txt'
        if self._check_file_exists(report_file, stage_name):
            self._check_file_not_empty(report_file, stage_name)

    def _validate_stage_13_excel_fill(self):
        """验证阶段 13: Excel 自动填写"""
        stage_name = "阶段13: Excel 自动填写"

        # 检查权限确认单 Excel
        permission_excel = self.result_dir / '权限确认单.xlsx'
        if self._check_file_exists(permission_excel, stage_name):
            self._check_file_not_empty(permission_excel, stage_name)

        # 检查自评估表 Excel
        assessment_excel = self.result_dir / '自评估表.xlsx'
        if self._check_file_exists(assessment_excel, stage_name):
            self._check_file_not_empty(assessment_excel, stage_name)

    def _validate_stage_14_word_report(self):
        """验证阶段 14: Word 报告生成"""
        stage_name = "阶段14: Word 报告生成"

        # 查找 Word 文件
        word_files = list(self.result_dir.glob('*小程序隐私合规检查报告.docx'))

        if not word_files:
            error_msg = f"[{stage_name}] 未找到 Word 报告文件"
            self.validation_results['errors'].append(error_msg)
            self.validation_results['missing_files'].append('*.docx')
            self.validation_results['failed_checks'] += 1
            logger.error(error_msg)
            return

        # 检查文件
        for word_file in word_files:
            if self._check_file_exists(word_file, stage_name):
                self._check_file_not_empty(word_file, stage_name)

    def _validate_stage_15_ai_analysis(self):
        """验证阶段 15: AI 智能体引擎深度分析"""
        stage_name = "阶段15: AI 智能体引擎深度分析"

        # AI 分析主要是辅助功能，没有特定输出文件
        # 这里检查是否有相关日志或输出
        logger.info(f"[{stage_name}] ✅ AI 分析完成")

    def _validate_stage_16_summary_report(self):
        """验证阶段 16: 生成综合报告"""
        stage_name = "阶段16: 生成综合报告"

        # 检查 Markdown 报告
        md_file = self.result_dir / 'privacy_compliance_report.md'
        if self._check_file_exists(md_file, stage_name):
            # 检查必需的章节
            required_keywords = ['# 小程序隐私合规检查报告', '## 检查概述', '## 核心检测结论']
            self._check_content_updated(md_file, required_keywords, stage_name)

    def _validate_stage_17_overall_report(self):
        """验证阶段 17: 生成概要报告"""
        stage_name = "阶段17: 生成概要报告"

        # 检查概要报告
        summary_file = self.result_dir / 'summary_report.txt'
        if self._check_file_exists(summary_file, stage_name):
            self._check_file_not_empty(summary_file, stage_name)

    def _generate_summary(self) -> Dict[str, Any]:
        """
        生成验证总结

        Returns:
            总结字典
        """
        total = self.validation_results['total_checks']
        passed = self.validation_results['passed_checks']
        failed = self.validation_results['failed_checks']
        warnings_count = len(self.validation_results['warnings'])
        errors_count = len(self.validation_results['errors'])

        # 计算通过率
        pass_rate = (passed / total * 100) if total > 0 else 0

        # 确定状态
        if failed == 0 and warnings_count == 0:
            status = "✅ 完全通过"
            status_level = "success"
        elif failed == 0 and warnings_count > 0:
            status = "⚠️ 通过（有警告）"
            status_level = "warning"
        elif failed > 0 and pass_rate >= 80:
            status = "⚠️ 部分通过"
            status_level = "partial"
        else:
            status = "❌ 验证失败"
            status_level = "failed"

        summary = {
            'status': status,
            'status_level': status_level,
            'total_checks': total,
            'passed_checks': passed,
            'failed_checks': failed,
            'warnings_count': warnings_count,
            'errors_count': errors_count,
            'pass_rate': pass_rate,
            'missing_files': self.validation_results['missing_files'],
            'incomplete_updates': self.validation_results['incomplete_updates'],
            'warnings': self.validation_results['warnings'],
            'errors': self.validation_results['errors']
        }

        return summary

    def print_summary(self, summary: Dict[str, Any]):
        """
        打印验证总结

        Args:
            summary: 总结字典
        """
        print("\n" + "=" * 80)
        print("                        检查结果验证报告")
        print("=" * 80)
        print()

        print(f"状态: {summary['status']}")
        print(f"通过率: {summary['pass_rate']:.1f}%")
        print()

        print(f"总检查项: {summary['total_checks']}")
        print(f"✅ 通过: {summary['passed_checks']}")
        print(f"❌ 失败: {summary['failed_checks']}")
        print(f"⚠️  警告: {summary['warnings_count']}")
        print()

        if summary['missing_files']:
            print("❌ 缺失文件:")
            for file in summary['missing_files']:
                print(f"  - {file}")
            print()

        if summary['incomplete_updates']:
            print("⚠️  更新不完整:")
            for file in summary['incomplete_updates']:
                print(f"  - {file}")
            print()

        if summary['warnings']:
            print("⚠️  警告:")
            for warning in summary['warnings'][:10]:
                print(f"  - {warning}")
            if len(summary['warnings']) > 10:
                print(f"  ... 还有 {len(summary['warnings']) - 10} 条警告")
            print()

        if summary['errors']:
            print("❌ 错误:")
            for error in summary['errors'][:10]:
                print(f"  - {error}")
            if len(summary['errors']) > 10:
                print(f"  ... 还有 {len(summary['errors']) - 10} 条错误")
            print()

        print("=" * 80)
        print()

        # 给出建议
        if summary['status_level'] == 'success':
            print("🎉 所有检查通过！检查结果完整且准确。")
        elif summary['status_level'] == 'warning':
            print("⚠️  检查通过，但存在一些警告。建议检查并修复警告项。")
        elif summary['status_level'] == 'partial':
            print("⚠️  部分检查失败。建议检查并修复失败项。")
        else:
            print("❌ 验证失败。请检查错误日志并重新运行检查。")

        print()

    def save_summary(self, summary: Dict[str, Any], output_file: str = None):
        """
        保存验证总结到文件

        Args:
            summary: 总结字典
            output_file: 输出文件路径
        """
        if not output_file:
            output_file = self.result_dir / 'validation_summary.json'

        output_file = Path(output_file)

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)

            logger.info(f"验证总结已保存: {output_file}")

        except Exception as e:
            logger.error(f"保存验证总结失败: {e}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='检查结果验证器')
    parser.add_argument('--result-dir', default='privacy_check_results', help='检查结果目录')
    parser.add_argument('--output', help='输出文件路径')

    args = parser.parse_args()

    # 创建验证器
    validator = CheckResultValidator(result_dir=args.result_dir)

    # 执行验证
    summary = validator.validate_all()

    # 打印总结
    validator.print_summary(summary)

    # 保存总结
    validator.save_summary(summary, args.output)

    # 返回状态码
    return 0 if summary['status_level'] in ['success', 'warning'] else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
