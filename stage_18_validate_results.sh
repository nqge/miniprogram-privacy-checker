#!/bin/bash
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
