#!/bin/bash
# 小程序隐私合规检查自动化脚本
# 使用方法: ./miniprogram-privacy-auto.sh [小程序路径]
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
    echo "                        小程序隐私合规检查工具"
    echo "================================================================================"
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
        print_info "请输入小程序源代码路径:"
        read -r MINIPROGRAM_PATH
    else
        MINIPROGRAM_PATH="$1"
    fi

    # 移除路径末尾的斜杠
    MINIPROGRAM_PATH="${MINIPROGRAM_PATH%/}"

    # 检查路径是否存在
    if [ ! -d "$MINIPROGRAM_PATH" ]; then
        print_error "路径不存在: $MINIPROGRAM_PATH"
        exit 1
    fi

    # 检查是否包含 app.json
    if [ ! -f "$MINIPROGRAM_PATH/app.json" ]; then
        print_warning "未找到 app.json 文件"
        print_warning "请确保路径是小程序根目录"
        read -p "是否继续? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    print_success "小程序路径: $MINIPROGRAM_PATH"
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

# 阶段 1: 权限声明检查
check_permissions() {
    print_info ""
    print_info "========================================"
    print_info "阶段 1/5: 权限声明检查"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/permission_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR"

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
    print_info "阶段 2/5: 敏感 API 扫描"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/api_scanner.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR"

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
    print_info "阶段 3/5: 数据流分析"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/dataflow_analyzer.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR"

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
    print_info "阶段 4/7: 动态调试风险检测"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/debug_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR"

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
    print_info "阶段 5/7: 日志泄露风险检测"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/log_leak_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR"

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
    print_info "阶段 6/7: 隐私政策检查"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/privacy_policy_checker.py" "$MINIPROGRAM_PATH" -o "$OUTPUT_DIR"

    if [ $? -eq 0 ]; then
        print_success "隐私政策检查完成"
    else
        print_error "隐私政策检查失败"
        return 1
    fi
}

# 阶段 7: 生成综合报告
generate_report() {
    print_info ""
    print_info "========================================"
    print_info "阶段 7/7: 生成综合报告"
    print_info "========================================"
    echo ""

    python3 "$CORE_DIR/report_generator.py" -r "$OUTPUT_DIR" -o "$OUTPUT_DIR/privacy_compliance_report.md"

    if [ $? -eq 0 ]; then
        print_success "综合报告生成完成"
    else
        print_error "综合报告生成失败"
        return 1
    fi
}

# 显示报告位置
show_report_location() {
    print_info ""
    print_info "========================================"
    print_info "检查完成"
    print_info "========================================"
    echo ""

    print_success "综合报告: $OUTPUT_DIR/privacy_compliance_report.md"
    print_success "检查结果目录: $OUTPUT_DIR"

    echo ""
    print_info "生成的文件:"
    ls -lh "$OUTPUT_DIR" 2>/dev/null || true

    echo ""
    print_info "查看报告:"
    echo "  cat $OUTPUT_DIR/privacy_compliance_report.md"
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

    # 阶段 1: 权限声明检查
    check_permissions

    # 阶段 2: 敏感 API 扫描
    scan_apis

    # 阶段 3: 数据流分析
    analyze_dataflow

    # 阶段 4: 动态调试风险检测
    check_debug

    # 阶段 5: 日志泄露风险检测
    check_log_leaks

    # 阶段 6: 隐私政策检查
    check_privacy_policy

    # 阶段 7: 生成综合报告
    generate_report

    # 显示报告位置
    show_report_location
}

# 执行主函数
main "$@"
