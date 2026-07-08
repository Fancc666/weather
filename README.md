# Weather APP

## 准备

您应该先安装好docker，并配置好镜像地址，推荐同时安装Python。

## 从气象局获取天气数据

例子：获取逐小时降水量数据<http://m.nmc.cn/publish/observations/hourly-precipitation.html>

![](https://qnhdpic.twt.edu.cn/download/origin/0c3cd0111c4453790f998d246052c015.png)

### 支持的环境变量

- BASE：数据地址，如例子里的地址（默认）。
- INTERVAL：获取数据时间间隔（秒）。
- FOLDER：图片数据存放目录（默认/data）。

### 构建镜像

```bash
docker build -t weather:v0.3 .
```

### 启动容器

启动容器建议挂载卷。

```bash
docker run -d --name myweather \
    -e TZ=Asia/Shanghai \
    -v ~/weather:/app/data \
    weather:v0.3
```

如果需要修改环境变量，参考六小时降水量。

```bash
docker run -d --name myweather-modify \
    -e TZ=Asia/Shanghai \
    -e BASE="http://m.nmc.cn/publish/observations/6hour-precipitation.html" \
    -e INTERVAL=21600 \
    -e FOLDER=data \
    -v ~/weather:/app/data \
    weather:v0.3
```
