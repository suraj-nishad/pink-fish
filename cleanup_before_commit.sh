#!/bin/bash
# Cleanup script before git commit
# This removes temporary files, logs, and redundant documentation

echo "🧹 Cleaning up unnecessary files before git commit..."

# Change to project directory
cd "$(dirname "$0")"

# 1. Remove backup CSV files
echo "📦 Removing CSV backups..."
rm -f data/plant_data_30days.csv.backup_*
rm -f data/*.backup

# 2. Remove old/redundant documentation (keep only essential ones)
echo "📄 Removing redundant documentation..."
rm -f API_TEST_RESULTS.md
rm -f DATA_GAP_FIXED_SUMMARY.md
rm -f DATA_SCHEMA_CONSISTENCY_CHECK.md
rm -f DEPLOYMENT_ALTERNATIVES.md
rm -f FRONTEND_COMPLETE.md
rm -f FRONTEND_SETUP_GUIDE.md
rm -f OPENAPI_VERIFICATION_COMPLETE.md
rm -f PRODUCTION_LINE_FIX.md
rm -f PRODUCTION_LINE_FIX_FINAL.md
rm -f PROJECT_STATUS_FINAL.md
rm -f RAILWAY_DEPLOYMENT.md
rm -f REALTIME_DATA_SETUP.md
rm -f REALTIME_DATA_SUMMARY.md
rm -f SETUP_COMPLETE_SUMMARY.md
rm -f STATUS_CALCULATION_EXPLAINED.md
rm -f UI_DESIGN_SPEC.md
rm -f VERCEL_DEPLOYMENT.md
rm -f VERCEL_SIZE_FIX.md

# 3. Remove test files
echo "🧪 Removing test files..."
rm -f test_all_apis.py
rm -f test_production_line.py
rm -f test_results.json
rm -f test-cases-templates.csv

# 4. Remove log files
echo "📋 Removing log files..."
rm -f server.log
rm -f *.log
rm -f data_update*.log

# 5. Remove unnecessary Python scripts (keep essential ones)
echo "🐍 Removing temporary Python scripts..."
# Keep: data_updater.py, backfill_missing_hours.py, cleanup_old_data.py
rm -f generate_month_data.py  # This was one-time use
rm -f split_openapi.py         # This was one-time use

# 6. Remove vercel config (using Railway)
echo "☁️ Removing Vercel config..."
rm -f vercel.json
rm -f .vercelignore

# 7. Remove old app.py in root (duplicate of backend/app.py)
echo "🔄 Removing duplicate app.py..."
rm -f app.py

# 8. Remove unused components
echo "🎨 Removing unused frontend components..."
rm -f frontend/src/components/TrendsDrawer.jsx
rm -f frontend/src/components/TrendsDrawer.scss

# 9. Remove .DS_Store files
echo "💻 Removing macOS metadata..."
find . -name ".DS_Store" -delete

# 10. Show what's left
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Files ready for commit:"
git status --short

echo ""
echo "💡 Next steps:"
echo "   1. Review the changes above"
echo "   2. Run: git add ."
echo "   3. Run: git commit -m 'Add scheduler and trend analyzer features'"
echo "   4. Run: git push"
