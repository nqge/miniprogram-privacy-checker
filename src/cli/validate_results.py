#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查结果验证器 - 命令行入口
"""

from .check_result_validator import CheckResultValidator

def main():
    """主函数"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='检查结果验证器')
    parser.add_argument('--result-dir', default='privacy_check_results', help='检查结果目录')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

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
    if summary['status_level'] == 'success':
        return 0
    elif summary['status_level'] == 'warning':
        return 0
    elif summary['status_level'] == 'partial':
        return 1
    else:
        return 2


if __name__ == '__main__':
    sys.exit(main())
