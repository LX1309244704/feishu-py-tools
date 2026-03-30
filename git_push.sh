#!/bin/bash
# 提交验证报告到GitHub
cd /workspace/projects/workspace/weiyuan

echo "📋 开始提交验证报告..."

# 添加验证报告
git add VERIFICATION_REPORT.md

# 检查状态
git status

# 提交
git commit -m "🎓� 微元Weiyuan - 毕业质阶段验证报告

# 尝试推送
echo "📝 推送到GitHub..."
git push origin main

echo "🎉 完成！"
