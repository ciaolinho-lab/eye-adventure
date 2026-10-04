@echo off
chcp 65001 > nul
echo ====================================================
echo  ✨ 亮亮精靈護眼大冒險 - 課堂本地伺服器啟動器
echo ====================================================
echo.
echo 1. 正在更新局域網與雲端 QR Code 圖片...
python scripts\generate_project_qr.py

echo.
echo 2. 正在啟動 Web 服務 (Port: 8080)...
echo 課堂區網與本機學生入口: http://localhost:8080/index.html
echo 教師管理後台入口:       http://localhost:8080/teacher_dashboard.html
echo A4 列印海報入口:        http://localhost:8080/classroom_poster.html
echo.
echo 按 Ctrl+C 可停止伺服器。
echo ====================================================
echo.

start http://localhost:8080/index.html
python -m http.server 8080
