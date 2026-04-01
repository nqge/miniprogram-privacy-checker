#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word报告生成器
基于模板生成小程序隐私合规检查报告
"""

import os
import json
from docx import Document
from datetime import datetime


def generate_word_report(report_data, template_path, output_path):
    """
    基于模板生成Word报告
    
    Args:
        report_data: 报告数据字典
        template_path: 模板文件路径
        output_path: 输出文件路径
    """
    try:
        # 加载模板
        doc = Document(template_path)
        
        # 获取报告数据
        app_name = report_data.get("小程序名称", "未知")
        app_id = report_data.get("appId", "未知")
        check_date = report_data.get("检查日期", datetime.now().strftime("%Y-%m-%d"))
        permissions_declared = report_data.get("权限声明", {})
        required_private_infos = report_data.get("requiredPrivateInfos", [])
        apis_found = report_data.get("API调用情况", {})
        privacy_policy = report_data.get("隐私政策配置", {})
        has_user_consent = report_data.get("用户授权流程", False)
        data_collection_points = report_data.get("数据收集点", [])
        third_party_sdks = report_data.get("第三方SDK", [])
        compliance_suggestions = report_data.get("合规建议", [])
        
        # 替换文档中的占位符
        for paragraph in doc.paragraphs:
            if "{小程序名称}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{小程序名称}", app_name)
            if "{appId}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{appId}", app_id)
            if "{检查日期}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{检查日期}", check_date)
            if "{已声明权限}" in paragraph.text:
                permissions_text = ", ".join(list(permissions_declared.keys())) if permissions_declared else "无"
                paragraph.text = paragraph.text.replace("{已声明权限}", permissions_text)
            if "{requiredPrivateInfos}" in paragraph.text:
                required_text = ", ".join(required_private_infos) if required_private_infos else "无"
                paragraph.text = paragraph.text.replace("{requiredPrivateInfos}", required_text)
            if "{API调用情况}" in paragraph.text:
                api_text = ", ".join(list(apis_found.keys())) if apis_found else "无"
                paragraph.text = paragraph.text.replace("{API调用情况}", api_text)
            if "{是否配置隐私政策}" in paragraph.text:
                privacy_text = "是" if privacy_policy.get("是否配置", False) else "否"
                paragraph.text = paragraph.text.replace("{是否配置隐私政策}", privacy_text)
            if "{是否有用户授权流程}" in paragraph.text:
                consent_text = "是" if has_user_consent else "否"
                paragraph.text = paragraph.text.replace("{是否有用户授权流程}", consent_text)
            if "{数据收集点数量}" in paragraph.text:
                points_count = str(len(data_collection_points))
                paragraph.text = paragraph.text.replace("{数据收集点数量}", points_count)
            if "{第三方SDK}" in paragraph.text:
                sdk_text = ", ".join(third_party_sdks) if third_party_sdks else "无"
                paragraph.text = paragraph.text.replace("{第三方SDK}", sdk_text)
            if "{合规建议}" in paragraph.text:
                suggestions_text = "；".join(compliance_suggestions) if compliance_suggestions else "无"
                paragraph.text = paragraph.text.replace("{合规建议}", suggestions_text)
        
        # 保存生成的报告
        doc.save(output_path)
        print(f"Word报告已生成: {output_path}")
        return True
    except Exception as e:
        print(f"生成Word报告失败: {e}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Word报告生成器")
    parser.add_argument("report_json", type=str, default="report.json", help="报告JSON文件路径")
    parser.add_argument("--template", type=str, default="D:\\AI\\skills\\miniprogram-privacy-checker-main\\小程序隐私合规检查报告模版.docx", help="模板文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    args = parser.parse_args()
    
    # 加载报告数据
    try:
        with open(args.report_json, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
    except Exception as e:
        print(f"加载报告数据失败: {e}")
        return
    
    # 确定输出文件路径
    if args.output:
        output_path = args.output
    else:
        app_name = report_data.get("小程序名称", "未知")
        output_path = f"{app_name}小程序隐私合规检查报告.docx"
    
    # 生成报告
    generate_word_report(report_data, args.template, output_path)


if __name__ == "__main__":
    main()
