FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 安装 Java
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

# 创建运行用户
RUN groupadd ctf && useradd -g ctf ctf

# 应用文件
COPY ./_files/app /app
COPY ./_files/readflag /readflag
COPY ./_files/run.sh /run.sh

RUN chmod +x /run.sh && \
    chmod u=srx,g=rx,o=rx /readflag && \
    chmod -R 755 /app

EXPOSE 8833

ENTRYPOINT ["/run.sh"]