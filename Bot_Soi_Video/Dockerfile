# Sử dụng Python 3.10 trên nền Linux nhẹ (Slim)
FROM python:3.10-slim

# Cài đặt FFmpeg và các thư viện hệ thống cần thiết
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào
COPY . .

# Mở cổng 10000 (Cổng mặc định của Render)
EXPOSE 10000

# Lệnh chạy bot
CMD ["python", "main.py"]