@echo off
echo 启动我的记账本...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
if not defined VIRTUAL_ENV (
    echo 建议使用虚拟环境，正在检查是否存在venv...
    if exist "venv\Scripts\activate.bat" (
        echo 发现虚拟环境，正在激活...
        call venv\Scripts\activate.bat
    ) else (
        echo 未找到虚拟环境，使用系统Python环境
    )
)

REM 检查依赖是否安装
echo 检查依赖包...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误：依赖包安装失败
        pause
        exit /b 1
    )
)

REM 启动应用
echo 启动Streamlit应用...
echo 应用将在浏览器中自动打开
echo 如果没有自动打开，请访问：http://localhost:8501
echo.
echo 按 Ctrl+C 停止应用
echo.

streamlit run app.py

pause
