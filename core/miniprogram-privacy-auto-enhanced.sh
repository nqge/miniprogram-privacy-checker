#!/bin/bash
# 小程序隐私合规检查自动化脚本（增强版）
# 使用方法: ./miniprogram-privacy-auto-enhanced.sh [小程序路径或.wxapkg文件]
#
# 基于标准:
# - 《网络安全标准实践指南-移动互联网应用程序（App）系统权限申请使用指南》
# - 《App违法违规收集使用个人信息行为认定方法》
# - 《网络安全标准实践指南—移动互联网应用程序（App）收集使用个人信息自评估指南》
# - 《网络安全标准实践指南-移动互联网应用程序（App）个人信息保护常见问题及处置指南》

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
    echo "                        小程序隐私合规检查工具 v3.2（增强版）"
    echo "================================================================================"
    echo ""
    echo "  🚀 增强功能"
    echo "  • 完整的 AI 智能分析填充"
    echo "  • 自动生成 Word 格式隐私合规报告"
    echo "  • 智能填充所有 {AI更新内容} 占位符"
    echo "  • 基于真实检查结果的智能分析"
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
    else
        print_error "路径不存在: $MINIPROGRAM_PATH"
        exit 1
    fi

    # 检查是否包含 app.json（项目目录）
    if [ "$INPUT_TYPE" = "project" ]; then
        if [ ! -f "$MINIPROGRAM_PATH/app.json" ]; then
            print_warning "未找到 app.json 文件"
            print_warning "请确保路径是小程序根目录"
            read -p "是否继续? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    fi

    print_success "检查类型: $INPUT_TYPE"
    print_success "输入路径: $MINIPROGRAM_PATH"
    print_success "输出目录: $OUTPUT_DIR"
}

# 清理旧的检查结果
clean_old_results() {
    print_info "清理旧的检查结果..."

    if [ -d "$OUTPUT_DIR" ]; then
        rm -rf "$OUTPUT_DIR"
        print_success "已清理旧的检查结果"
    fi

    mkdir -p "$OUTPUT_DIR"
    print_success "创建输出目录: $OUTPUT_DIR"
}

# 反编译 .wxapkg 文件（如果需要）
unpack_wxapkg() {
    if [ "$INPUT_TYPE" != "wxapkg" ]; then
        return 0
    fi

    print_info ""
    print_info "========================================"
    print_info "反编译阶段"
    print_info "========================================"
    echo ""

    TEMP_DIR=$(mktemp -d -t miniprogram_unpacked_XXXXXX)

    # 使用 unpacker 工具
    python3 "$CORE_DIR/unpacker.py" "$MINIPROGRAM_PATH" -o "$TEMP_DIR"

    if [ $? -ne 0 ]; then
        print_error "反编译失败"
        return 1
    fi

    # 验证反编译结果
    if [ ! -f "$TEMP_DIR/app.json" ]; then
        print_error "反编译结果验证失败，未找到 app.json"
        rm -rf "$TEMP_DIR"
        return 1
    fi

    # 更新输入路径为反编译后的目录
    MINIPROGRAM_PATH="$TEMP_DIR"
    INPUT_TYPE="project"

    print_success "反编译成功，项目路径: $MINIPROGRAM_PATH"

    # 保持临时目录，稍后清理
    TEMP_CLEANUP_DONE=false
    cleanup_temp_dir() {
        if [ "$TEMP_CLEANUP_DONE" = true ] || [ "$INPUT_TYPE" != "wxapkg" ]; then
            return 0
        fi

        print_info "清理临时目录..."
        rm -rf "$TEMP_DIR"
        TEMP_CLEANUP_DONE=true
        print_success "清理完成"
    }

    return 0
}

# 阶段 1: 权限声明检查
check_permissions() {
    print_info ""
    print_info "========================================"
    print_info "阶段 1/13: 权限声明检查"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/permission_checker.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "权限声明检查完成"
    else
        print_error "权限声明检查失败"
        return 1
    fi
}

# 阶段 2: 敏感 API 扫描
scan_apis() {
    print_info ""
    print_info "========================================"
    print_info "阶段 2/13: 敏感 API 扫描"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/api_scanner.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "敏感 API 扫描完成"
    else
        print_error "敏感 API 扫描失败"
        return 1
    fi
}

# 阶段 3: 数据流分析
analyze_dataflow() {
    print_info ""
    print_info "========================================"
    print_info "阶段 3/13: 数据流分析"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/dataflow_analyzer.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "数据流分析完成"
    else
        print_error "数据流分析失败"
        return 1
    fi
}

# 阶段 4: 动态调试风险检测
check_debug() {
    print_info ""
    print_info "========================================"
    print_info "阶段 4/13: 动态调试风险检测"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/debug_checker.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "动态调试风险检测完成"
    else
        print_error "动态调试风险检测失败"
        return 1
    fi
}

# 阶段 5: 日志泄露风险检测
check_log_leaks() {
    print_info ""
    print_info "========================================"
    print_info "阶段 5/13: 日志泄露风险检测"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/log_leak_checker.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "日志泄露风险检测完成"
    else
        print_error "日志泄露风险检测失败"
        return 1
    fi
}

# 阶段 6: 隐私政策检查
check_privacy_policy() {
    print_info ""
    print_info "========================================"
    print_info "阶段 6/13: 隐私政策检查"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/privacy_policy_checker.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "隐私政策检查完成"
    else
        print_error "隐私政策检查失败"
        return 1
    fi
}

# 阶段 7: 隐私政策命名检查
check_privacy_naming() {
    print_info ""
    print_info "========================================"
    print_info "阶段 7/13: 隐私政策命名检查"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/privacy_naming_checker.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "隐私政策命名检查完成"
    else
        print_error "隐私政策命名检查失败"
        return 1
    fi
}

# 阶段 8: SDK 检测
check_sdk_usage() {
    print_info ""
    print_info "========================================"
    print_info "阶段 8/13: SDK 检测"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/sdk_detector.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "SDK 使用检测完成"
    else
        print_error "SDK 使用检测失败"
        return 1
    fi
}

# 阶段 9: 生成小程序申请权限确认单
generate_permission_confirmation() {
    print_info ""
    print_info "========================================"
    print_info "阶段 9/13: 生成小程序申请权限确认单"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/permission_confirmation.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "权限确认单生成完成"
    else
        print_warning "权限确认单生成失败（非关键）"
    fi
}

# 阶段 10: 生成小程序收集使用个人信息自评估表
generate_self_assessment() {
    print_info ""
    print_info "========================================"
    print_info "阶段 10/13: 生成个人信息收集使用自评估表"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/self_assessment_tool.py" "$MINIPROGRAM_PATH" -o "$1"

    if [ $? -eq 0 ]; then
        print_success "自评估表生成完成"
    else
        print_warning "自评估表生成失败（非关键）"
    fi
}

# 阶段 11: 生成综合报告
generate_report() {
    print_info ""
    print_info "========================================"
    print_info "阶段 11/13: 生成综合报告"
    print_info "========================================"
    echo ""

    # 生成 Markdown 格式报告（传递小程序路径）
    python3 "$CORE_DIR/report_generator.py" -r "$1" -o "$1/privacy_compliance_report.md" -m "$MINIPROGRAM_PATH"

    if [ $? -eq 0 ]; then
        print_success "Markdown 综合报告生成完成"
    else
        print_warning "Markdown 报告生成失败（非关键）"
    fi

    # 生成概要报告（包含权限确认单和自评估表的引用）
    python3 "$CORE_DIR/summary_generator.py" "$1" -m "$MINIPROGRAM_PATH" -o "$1/summary_report.txt"

    if [ $? -eq 0 ]; then
        print_success "概要报告生成完成"
    else
        print_warning "概要报告生成失败（非关键）"
    fi

    # 生成详细权限调用报告
    print_info ""
    print_info "生成详细权限调用报告..."
    python3 "$CORE_DIR/detailed_permission_report.py" "$MINIPROGRAM_PATH" \
        -s "$1/api_scan.json" \
        -o "$1/detailed_permission_report.md"

    if [ $? -eq 0 ]; then
        print_success "详细权限报告生成完成"
    else
        print_warning "详细权限报告生成失败（非关键）"
    fi
}

# 阶段 12: Excel 自动填写
auto_fill_excel() {
    print_info ""
    print_info "========================================"
    print_info "阶段 12/13: Excel 自动填写"
    print_info "========================================"
    echo ""

    # 使用 AI 增强版 Excel 自动填写工具
    print_info "使用 AI 增强版 Excel 自动填写工具..."
    python3 "$CORE_DIR/ai_excel_fill.py" \
        --base-path "$SCRIPT_DIR" \
        --result-dir "$1"

    if [ $? -eq 0 ]; then
        print_success "Excel 自动填写完成"
    else
        print_warning "Excel 自动填写失败（非关键）"
    fi
}

# 阶段 13: Word 报告生成（增强版）
generate_word_report() {
    print_info ""
    print_info "========================================"
    print_info "阶段 13/13: Word 报告生成（增强版）"
    print_info "========================================"
    echo ""

    # 提取小程序名称
    MINIPROGRAM_NAME="小程序"
    if [ -f "$MINIPROGRAM_PATH/app.json" ]; then
        MINIPROGRAM_NAME=$(grep -o '"name":"[^"]*"' "$MINIPROGRAM_PATH/app.json" | cut -d'"' -f4 || echo "小程序")
    fi

    # 使用增强版 Word 文档生成器
    print_info "使用增强版 Word 文档生成器（支持完整 AI 智能分析填充）..."
    python3 "$SCRIPT_DIR/enhanced_word_report_generator.py" \
        --template "$SCRIPT_DIR/小程序隐私合规检查报告模版.docx" \
        --result-dir "$1" \
        --output "$1/${MINIPROGRAM_NAME}小程序隐私合规检查报告.docx" \
        --name "$MINIPROGRAM_NAME"

    if [ $? -eq 0 ]; then
        print_success "Word 报告生成完成（已智能填充所有 {AI更新内容}）"
    else
        print_warning "Word 报告生成失败（非关键）"
    fi
}

# 显示报告位置
show_report_location() {
    print_info ""
    print_info "========================================"
    print_info "检查完成"
    print_info "========================================"
    echo ""

    print_success "综合报告: $1/privacy_compliance_report.md"
    print_success "详细权限报告: $1/detailed_permission_report.md"
    print_success "检查结果目录: $1"
    
    # 查找生成的 Word 报告
    WORD_REPORT=$(ls "$1/*小程序隐私合规检查报告.docx" 2>/dev/null | head -1)
    if [ -f "$WORD_REPORT" ]; then
        print_success "Word 报告: $WORD_REPORT"
        print_info "Word 报告已智能填充所有 {AI更新内容} 占位符"
    fi

    echo ""
    print_info "生成的文件:"
    ls -lh "$1" 2>/dev/null || true

    echo ""
    print_info "查看报告:"
    echo "  cat $1/privacy_compliance_report.md"
    echo ""
    print_info "Excel 文件已自动填写:"
    echo "  - 权限确认单.xlsx"
    echo "  - 自评估表.xlsx"
    echo ""
    print_info "Word 报告已智能填充所有 AI 分析内容"
    echo ""
}

# 主函数
main() {
    print_banner

    # 检查 Python 环境
    check_python

    # 检查输入参数
    check_input "$1"

    # 清理旧的检查结果
    clean_old_results

    # 反编译 .wxapkg 文件（如果需要）
    unpack_wxapkg
    RESULT=$?

    if [ $RESULT -ne 0 ]; then
        print_error "反编译失败，退出"
        exit 1
    fi

    # 执行所有检查阶段
    check_permissions "$OUTPUT_DIR"
    scan_apis "$OUTPUT_DIR"
    analyze_dataflow "$OUTPUT_DIR"
    check_debug "$OUTPUT_DIR"
    check_log_leaks "$OUTPUT_DIR"
    check_privacy_policy "$OUTPUT_DIR"
    check_privacy_naming "$OUTPUT_DIR"
    check_sdk_usage "$OUTPUT_DIR"
    generate_permission_confirmation "$OUTPUT_DIR"
    generate_self_assessment "$OUTPUT_DIR"
    generate_report "$OUTPUT_DIR"
    auto_fill_excel "$OUTPUT_DIR"
    generate_word_report "$OUTPUT_DIR"

    # 清理临时目录
    cleanup_temp_dir

    # 显示报告位置
    show_report_location "$OUTPUT_DIR"
}

# 执行主函数
main "$@"