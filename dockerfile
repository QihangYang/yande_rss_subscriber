# 使用官方的轻量级 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV INTERVAL=21600

# 复制当前目录内容到容器
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 设置容器启动时运行的命令
ENTRYPOINT python main.py -i ${INTERVAL}