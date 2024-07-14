# 使用官方的 Python 運行環境作為父鏡像
FROM python:3.8-slim

# 設置工作目錄
WORKDIR /usr/src/app

# 將當前目錄的內容拷貝到容器中
COPY . .

# 安裝 requirements.txt 中指定的所有依賴包
RUN pip install --no-cache-dir -r requirements.txt

# 當容器啟動時運行 market_monitor.py
CMD ["python", "app.py"]