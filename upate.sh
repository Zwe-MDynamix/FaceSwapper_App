#!/bin/bash

# Update all repository references
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.yml" -o -name "*.yaml" \) \
  -exec sed -i 's/zwelakhem\/face-swapper-app/Zwe-MDynamix\/FaceSwapper_App/g' {} +

echo "✅ Updated all repository references"

# Commit the changes
git add .
git commit -m "fix: update repository URLs to correct GitHub repo"

# Push to correct remote
git remote set-url origin https://github.com/Zwe-MDynamix/FaceSwapper_App.git
git push -u origin main

echo "✅ Pushed to correct repository!"
