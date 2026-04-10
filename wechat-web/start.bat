@echo off
chcp 65001 > nul
REM 微信公众号文章排版发布工具 - Windows 启动脚本

echo ==========================================
echo  微信公众号文章排版发布工具
echo ==========================================

echo.
echo  检查依赖...

REM 检查 Flask
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo   正在安装 Flask...
    pip install -r requirements.txt
)

echo.
echo ==========================================
echo  启动服务中...
echo ==========================================
echo.
echo  访问地址: http://127.0.0.1:5000
echo  或访问: http://localhost:5000
echo.
echo  按 Ctrl+C 停止服务
echo ==========================================

python app.py
