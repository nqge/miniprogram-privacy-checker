# 更新日志

## v3.4 (2026-04-04)

### 🎉 重大优化

#### SKILL.md 重构
- **精简内容**：从 1169 行压缩到 ~120 行（减少 90%）
- **结构优化**：按照 skill-creator 最佳实践重组
- **渐进式加载**：核心指令在 SKILL.md，详细文档在 references/

#### 文件组织
- **移除冗余**：删除 README、CHANGELOG、UPDATE 等辅助文档
- **分类归档**：将技术文档移到 references/ 目录
- **保持简洁**：只保留核心脚本和必要配置

#### 文档优化
- **新增 references/permission_mapping.md** - 权限映射表
- **新增 references/ai_analysis_guide.md** - AI 智能分析指南
- **新增 references/excel_fill_guide.md** - Excel 自动填写指南

### 📊 优化对比

| 项目 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| SKILL.md 行数 | 1169 | ~120 | -90% |
| 文件数量 | 20+ | 15 | -25% |
| 上下文占用 | 高 | 低 | 显著降低 |
| 加载速度 | 慢 | 快 | 显著提升 |

### 🔧 技术改进

1. **符合 AgentSkills 规范**
   - 遵循 skill-creator 指导原则
   - 保持 SKILL.md 简洁（<500 行）
   - 使用渐进式加载

2. **优化上下文使用**
   - 核心指令始终加载
   - 详细文档按需加载
   - 减少不必要的 token 消耗

3. **改进可维护性**
   - 清晰的文件结构
   - 模块化文档组织
   - 易于更新和扩展

### 📝 文件变更

**新增文件**：
- `references/permission_mapping.md`
- `references/ai_analysis_guide.md`
- `references/excel_fill_guide.md`

**移动文件**：
- 所有技术文档 → `references/`
- 历史文档 → `references/`

**保留文件**：
- `SKILL.md` - 核心指令（重写）
- `miniprogram-privacy-auto.sh` - 主脚本
- `src/` - 源代码
- `scripts/` - 辅助脚本
- `templates/` - 模板文件
- `requirements.txt` - 依赖

---

## v3.3 (2026-03-31)

### 新增功能
- 依赖管理（requirements.txt）
- AI 智能体引擎（代码语义分析）
- AI 自动更新 Excel
- AI 智能分析生成 Word 报告

---

## v3.2

### 新增功能
- 自动化 Word 报告输出
- 增强 AI 分析能力

---

## v3.1

### 新增功能
- AI 增强版 Excel 自动填写
- Word 文档报告生成
- 详细权限报告

---

**维护者**: 小红🌸
**GitHub**: https://github.com/nqge/miniprogram-privacy-checker
