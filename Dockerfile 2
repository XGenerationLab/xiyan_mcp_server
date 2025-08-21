# 使用Python 3.11作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

#COPY requirements.txt .
RUN pip install xiyan-mcp-server


# 运行应用
CMD ["python", "-m", "xiyan_mcp_server"]