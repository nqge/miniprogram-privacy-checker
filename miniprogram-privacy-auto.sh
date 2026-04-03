#!/bin/bash
# 小程序隐私合规检查自动化脚本 v3.3
# 使用方法: ./miniprogram-privacy-auto.sh [小程序路径或.wxapkg文件] [输出目录]
#
# 新增功能（v3.3）:
# - 1. ✅ 添加依赖管理（requirements.txt）
# - 2. ✅ 增加 AI 智能体引擎分析
# - 3. ✅ 完善功能（AI 自动更新 Excel 和 Word）
# - 4. ✅ 完善输出报告（AI 智能分析生成 Word 报告）

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$SCRIPT_DIR/core"
OUTPUT_DIR="${2:-privacy_check_results}"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[*] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[+] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[-] $1${NC}"
}

# 打印横幅
print_banner() {
    echo ""
    echo "================================================================================"
    echo "                 小程序隐私合规检查工具 v3.3 🚀"
    echo "================================================================================"
    echo ""
    echo "  📊 v3.3 新增功能"
    echo "  • 依赖管理（requirements.txt）"
    echo "  • AI 智能体引擎（深度分析未知风险）"
    echo "  • AI 自动更新 Excel（权限确认单 + 自评估表）"
    echo "  • AI 智能分析生成 Word 报告（6 个关键段落）"
    echo ""
    echo "  基于官方标准："
    echo "  - 《网络安全标准实践指南-移动互联网应用程序（App）系统权限申请使用指南》"
    echo "  - 《App违法违规收集使用个人信息行为认定方法》"
    echo "  - 《App收集使用个人信息自评估指南》"
    echo "  - 《App个人信息保护常见问题及处置指南》"
    echo ""
    echo "================================================================================"
    echo ""
}

# 检查 Python 环境
check_python() {
    print_info "检查 Python 环境..."

    if ! command -v python3 &> /dev/null; then
        print_error "未找到 Python 3"
        print_error "请先安装 Python 3.6 或更高版本"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 版本: $PYTHON_VERSION"
}

# 检查依赖
check_dependencies() {
    print_info "检查 Python 依赖..."

    # 检查 requirements.txt
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        print_info "安装依赖包..."
        pip3 install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || {
            print_warning "部分依赖安装失败，可能影响部分功能"
        }
        print_success "依赖检查完成"
    else
        print_warning "未找到 requirements.txt"
    fi
}

# 检查输入参数
check_input() {
    if [ -z "$1" ]; then
        print_info "请输入小程序路径或.wxapkg文件:"
        read -r MINIPROGRAM_PATH
    else
        MINIPROGRAM_PATH="$1"
    fi

    # 移除路径末尾的斜杠
    MINIPROGRAM_PATH="${MINIPROGRAM_PATH%/}"

    # 检测输入类型
    INPUT_TYPE=""

    if [ -f "$MINIPROGRAM_PATH" ]; then
        if [[ "$MINIPROGRAM_PATH" == *.wxapkg ]]; then
            INPUT_TYPE="wxapkg"
            print_info "检测到 .wxapkg 文件，将进行自动反编译"
        else
            INPUT_TYPE="project"
            print_info "检测到项目目录"
        fi
    elif [ -d "$MINIPROGRAM_PATH" ]; then
        INPUT_TYPE="project"
        print_info "检测到项目目录"
    else
        print_error "路径不存在: $MINIPROGRAM_PATH"
        exit 1
    fi

    # 创建输出目录
    mkdir -p "$OUTPUT_DIR"
    print_success "输出目录: $OUTPUT_DIR"
}

# 反编译 .wxapkg
unpack_wxapkg() {
    local wxapkg_path="$1"
    local unpack_dir="$OUTPUT_DIR/unpacked"

    print_info "反编译 .wxapkg 文件..."

    # 使用反编译工具
    if [ -f "$CORE_DIR/unpacker.py" ]; then
        python3 "$CORE_DIR/unpacker.py" "$wxapkg_path" "$unpack_dir" || {
            print_error "反编译失败"
            exit 1
        }
        print_success "反编译完成"
        echo "$unpack_dir"
    else
        print_error "未找到反编译工具"
        exit 1
    fi
}

# 提取小程序名称
extract_miniprogram_name() {
    local project_path="$1"

    print_info "提取小程序名称..."

    # 尝试从 app.json 读取
    local app_json="$project_path/app.json"
    if [ -f "$app_json" ]; then
        MINIPROGRAM_NAME=$(python3 -c "
import json
try:
    with open('$app_json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(data.get('window', {}).get('navigationBarTitleText', '小程序'))
except:
    print('小程序')
" 2>/dev/null || echo "小程序")

        print_success "小程序名称: $MINIPROGRAM_NAME"
    else
        MINIPROGRAM_NAME="小程序"
        print_warning "未找到 app.json，使用默认名称: $MINIPROGRAM_NAME"
    fi
}

# 阶段 1: 权限声明检查
stage_1_permission_check() {
    print_info "[1/17] 权限声明检查..."

    if [ -f "$CORE_DIR/permission_checker.py" ]; then
        python3 "$CORE_DIR/permission_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "权限声明检查失败"
        }
        print_success "权限声明检查完成"
    else
        print_warning "未找到权限声明检查工具"
    fi
}

# 阶段 2: 敏感 API 扫描
stage_2_api_scan() {
    print_info "[2/17] 敏感 API 扫描..."

    if [ -f "$CORE_DIR/api_scanner.py" ]; then
        python3 "$CORE_DIR/api_scanner.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "敏感 API 扫描失败"
        }
        print_success "敏感 API 扫描完成"
    else
        print_warning "未找到敏感 API 扫描工具"
    fi
}

# 阶段 3: 数据流分析
stage_3_dataflow_analysis() {
    print_info "[3/17] 数据流分析..."

    if [ -f "$CORE_DIR/dataflow_analyzer.py" ]; then
        python3 "$CORE_DIR/dataflow_analyzer.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "数据流分析失败"
        }
        print_success "数据流分析完成"
    else
        print_warning "未找到数据流分析工具"
    fi
}

# 阶段 4: 动态调试风险检测
stage_4_debug_check() {
    print_info "[4/17] 动态调试风险检测..."

    if [ -f "$CORE_DIR/debug_checker.py" ]; then
        python3 "$CORE_DIR/debug_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "动态调试风险检测失败"
        }
        print_success "动态调试风险检测完成"
    else
        print_warning "未找到动态调试风险检测工具"
    fi
}

# 阶段 5: 日志泄露风险检测
stage_5_log_leak_check() {
    print_info "[5/17] 日志泄露风险检测..."

    if [ -f "$CORE_DIR/log_leak_checker.py" ]; then
        python3 "$CORE_DIR/log_leak_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "日志泄露风险检测失败"
        }
        print_success "日志泄露风险检测完成"
    else
        print_warning "未找到日志泄露风险检测工具"
    fi
}

# 阶段 6: 隐私政策检查
stage_6_privacy_policy_check() {
    print_info "[6/17] 隐私政策检查..."

    if [ -f "$CORE_DIR/privacy_policy_checker.py" ]; then
        python3 "$CORE_DIR/privacy_policy_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "隐私政策检查失败"
        }
        print_success "隐私政策检查完成"
    else
        print_warning "未找到隐私政策检查工具"
    fi
}

# 阶段 7: 隐私政策命名检查
stage_7_privacy_naming_check() {
    print_info "[7/17] 隐私政策命名检查..."

    if [ -f "$CORE_DIR/privacy_naming_checker.py" ]; then
        python3 "$CORE_DIR/privacy_naming_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "隐私政策命名检查失败"
        }
        print_success "隐私政策命名检查完成"
    else
        print_warning "未找到隐私政策命名检查工具"
    fi
}

# 阶段 8: SDK 使用检测
stage_8_sdk_check() {
    print_info "[8/17] SDK 使用检测..."

    if [ -f "$CORE_DIR/sdk_detector.py" ]; then
        python3 "$CORE_DIR/sdk_detector.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "SDK 使用检测失败"
        }
        print_success "SDK 使用检测完成"
    else
        print_warning "未找到 SDK 使用检测工具"
    fi
}

# 阶段 9: 混合架构检测（v3.0 新增）
stage_9_hybrid_check() {
    print_info "[9/17] 混合架构检测（静态规则 + AI 智能体）..."

    if [ -f "$CORE_DIR/hybrid_checker.py" ]; then
        python3 "$CORE_DIR/hybrid_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "混合架构检测失败"
        }
        print_success "混合架构检测完成"
    else
        print_warning "未找到混合架构检测工具"
    fi
}

# 阶段 10: 生成权限确认单
stage_10_permission_confirmation() {
    print_info "[10/17] 生成权限确认单（38 项权限）..."

    if [ -f "$CORE_DIR/permission_confirmation.py" ]; then
        python3 "$CORE_DIR/permission_confirmation.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "权限确认单生成失败"
        }
        print_success "权限确认单生成完成"
    else
        print_warning "未找到权限确认单生成工具"
    fi
}

# 阶段 11: 生成自评估表
stage_11_self_assessment() {
    print_info "[11/17] 生成自评估表（28 个评估点）..."

    if [ -f "$CORE_DIR/self_assessment_tool.py" ]; then
        python3 "$CORE_DIR/self_assessment_tool.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "自评估表生成失败"
        }
        print_success "自评估表生成完成"
    else
        print_warning "未找到自评估表生成工具"
    fi
}

# 阶段 12: 生成详细权限报告（v3.1 新增）
stage_12_detailed_permission_report() {
    print_info "[12/17] 生成详细权限报告..."

    if [ -f "$CORE_DIR/detailed_permission_report.py" ]; then
        python3 "$CORE_DIR/detailed_permission_report.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR" || {
            print_warning "详细权限报告生成失败"
        }
        print_success "详细权限报告生成完成"
    else
        print_warning "未找到详细权限报告生成工具"
    fi
}

# 阶段 13: Excel 自动填写（v3.1 新增，v3.3 增强）
stage_13_excel_fill() {
    print_info "[13/17] AI 自动更新 Excel（权限确认单 + 自评估表）..."

    if [ -f "$CORE_DIR/enhanced_ai_excel_fill.py" ]; then
        python3 "$CORE_DIR/enhanced_ai_excel_fill.py" \
            --result-dir "$OUTPUT_DIR" \
            --base-path "$SCRIPT_DIR" || {
            print_warning "Excel 自动填写失败"
        }
        print_success "Excel 自动填写完成"
    else
        print_warning "未找到 Excel 自动填写工具"
    fi
}

# 阶段 14: Word 报告生成（v3.2 新增，v3.3 增强）
stage_14_word_report() {
    print_info "[14/17] AI 智能分析生成 Word 报告（6 个关键段落）..."

    # 查找模板文件
    local template_file=""
    for file in "$SCRIPT_DIR"/*.docx; do
        if [[ "$file" =~ template|模板 ]]; then
            template_file="$file"
            break
        fi
    done

    if [ -z "$template_file" ]; then
        # 使用第一个 docx 文件
        template_file=$(ls "$SCRIPT_DIR"/*.docx 2>/dev/null | head -1)
    fi

    if [ -f "$template_file" ] && [ -f "$CORE_DIR/enhanced_word_report_generator.py" ]; then
        python3 "$CORE_DIR/enhanced_word_report_generator.py" \
            --template "$template_file" \
            --result-dir "$OUTPUT_DIR" \
            --miniprogram-name "$MINIPROGRAM_NAME" \
            --output "$OUTPUT_DIR/${MINIPROGRAM_NAME}小程序隐私合规检查报告.docx" || {
            print_warning "Word 报告生成失败"
        }
        print_success "Word 报告生成完成"
    else
        print_warning "未找到 Word 报告生成工具或模板文件"
    fi
}

# 阶段 15: AI 智能体引擎分析（v3.3 新增）
stage_15_ai_analysis() {
    print_info "[15/17] AI 智能体引擎深度分析..."

    if [ -f "$CORE_DIR/ai_agent_engine.py" ]; then
        python3 "$CORE_DIR/ai_agent_engine.py" || {
            print_warning "AI 智能体分析失败"
        }
        print_success "AI 智能体分析完成"
    else
        print_warning "未找到 AI 智能体引擎"
    fi
}

# 阶段 16: 生成综合报告
stage_16_summary_report() {
    print_info "[16/17] 生成综合报告..."

    if [ -f "$CORE_DIR/report_generator.py" ]; then
        python3 "$CORE_DIR/report_generator.py" \
            -r "$OUTPUT_DIR" \
            -o "$OUTPUT_DIR/privacy_compliance_report.md" || {
            print_warning "综合报告生成失败"
        }
        print_success "综合报告生成完成"
    else
        print_warning "未找到报告生成工具"
    fi
}

# 阶段 17: 生成概要报告
stage_17_overall_report() {
    print_info "[17/17] 生成概要报告..."

    if [ -f "$CORE_DIR/summary_generator.py" ]; then
        python3 "$CORE_DIR/summary_generator.py" \
            -r "$OUTPUT_DIR" \
            -o "$OUTPUT_DIR/summary_report.txt" || {
            print_warning "概要报告生成失败"
        }
        print_success "概要报告生成完成"
    else
        print_warning "未找到概要报告生成工具"
    fi
}

# 阶段 18: 验证检查结果（v3.3 新增）
stage_18_validate_results() {
    print_info "[18/18] 验证检查结果..."

    if [ -f "$CORE_DIR/check_result_validator.py" ]; then
        python3 "$CORE_DIR/check_result_validator.py" \
            --result-dir "$OUTPUT_DIR" \
            --output "$OUTPUT_DIR/validation_summary.json" || {
            print_warning "检查结果验证失败"
        }
        print_success "检查结果验证完成"
    else
        print_warning "未找到检查结果验证工具"
    fi
}

# 主函数
main() {
    print_banner

    # 检查环境
    check_python
    check_dependencies

    # 检查输入
    check_input "$1"

    # 处理 .wxapkg 文件
    if [ "$INPUT_TYPE" = "wxapkg" ]; then
        MINIPROGRAM_PATH=$(unpack_wxapkg "$MINIPROGRAM_PATH")
    fi

    # 提取小程序名称
    extract_miniprogram_name "$MINIPROGRAM_PATH"

    echo ""
    print_info "开始检查..."
    echo ""

    # 执行 17 个检查阶段
    stage_1_permission_check
    stage_2_api_scan
    stage_3_dataflow_analysis
    stage_4_debug_check
    stage_5_log_leak_check
    stage_6_privacy_policy_check
    stage_7_privacy_naming_check
    stage_8_sdk_check
    stage_9_hybrid_check
    stage_10_permission_confirmation
    stage_11_self_assessment
    stage_12_detailed_permission_report
    stage_13_excel_fill
    stage_14_word_report
    stage_15_ai_analysis
    stage_16_summary_report
    stage_17_overall_report
    stage_18_validate_results

    echo ""
    echo "================================================================================"
    echo "                         ✅ 检查完成！"
    echo "================================================================================"
    echo ""
    echo "  📁 输出目录: $OUTPUT_DIR"
    echo ""
    echo "  📊 生成的报告："
    echo "  • 权限确认单.txt - 38 项权限的详细确认单"
    echo "  • 自评估表.txt - 28 个评估点的自评估表"
    echo "  • 权限确认单.xlsx - AI 自动更新（业务功能 + 必要性说明）"
    echo "  • 自评估表.xlsx - AI 自动更新（评估结果 + 评估说明）"
    echo "  • ${MINIPROGRAM_NAME}小程序隐私合规检查报告.docx - AI 智能分析生成（6 个关键段落）"
    echo "  • privacy_compliance_report.md - 综合合规报告"
    echo "  • summary_report.txt - 概要报告"
    echo ""
    echo "  🎯 下一步："
    echo "  1. 查看 Word 报告（${MINIPROGRAM_NAME}小程序隐私合规检查报告.docx）"
    echo "  2. 检查 Excel 文件（权限确认单.xlsx + 自评估表.xlsx）"
    echo "  3. 阅读综合报告（privacy_compliance_report.md）"
    echo "  4. 根据建议修复问题"
    echo ""
    echo "================================================================================"
    echo ""
}

# 运行主函数
main "$@"
