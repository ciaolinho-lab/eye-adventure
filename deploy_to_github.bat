@echo off
chcp 65001 > nul
echo ====================================================
echo  🚀 亮亮精靈護眼大冒險 - 發布至 GitHub Pages
echo  目標 GitHub: ciaolinho-lab / eye-adventure
echo  目標網址: https://ciaolinho-lab.github.io/eye-adventure/
echo ====================================================
echo.

set PATH=C:\Users\HO\AppData\Local\GitHubDesktop\app-3.5.12\resources\app\git\cmd;%PATH%

echo 1. 正在重新生成專屬 GitHub Pages QR Code...
python scripts\generate_project_qr.py --url https://ciaolinho-lab.github.io/eye-adventure/

echo.
echo 2. 正在設定遠端 Repository...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/ciaolinho-lab/eye-adventure.git

echo.
echo 3. 正在準備專案檔案與 Commit...
git add .
git commit -m "Deploy Eye Adventure project for ciaolinho-lab"

echo.
echo 4. 正在推送到 GitHub...
git push -u origin main

echo.
echo ====================================================
echo  ✨ 部署完成！
echo  官方專屬網址: https://ciaolinho-lab.github.io/eye-adventure/
echo ====================================================
echo.
pause
