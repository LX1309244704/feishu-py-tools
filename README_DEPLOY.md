# 🚀 部署指南 - 飞书Python工具箱

## 📋 前置要求

- GitHub账号
- Railway.app账号（免费注册：https://railway.app）

---

## 🌟 方案1：Railway.app部署（推荐）

### 步骤1：注册Railway账号

1. 访问 https://railway.app
2. 点击"Get Started"注册账号
3. 使用GitHub账号登录（推荐）

### 步骤2：创建新项目

1. 登录Railway后，点击"New Project"
2. 选择"Deploy from GitHub repo"
3. 选择你的仓库：`LX1309244704/weiyuan`
4. Railway会自动检测到Dockerfile并开始部署

### 步骤3：配置环境变量

1. 在Railway项目中，点击"Variables"标签
2. 添加以下环境变量：

```
FLASK_SECRET_KEY=your-random-secret-key
FLASK_ENV=production
FLASK_DEBUG=False
```

可选（如果需要使用AI功能）：
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 步骤4：等待部署完成

Railway会自动：
1. 拉取最新代码
2. 构建Docker镜像
3. 部署应用
4. 生成HTTPS URL

### 步骤5：获取访问地址

1. 部署完成后，Railway会生成一个URL
2. 点击"Domains"标签可以看到你的应用地址
3. 点击URL即可访问

### 部署后的URL示例

```
https://feishu-tools-production.up.railway.app/
```

---

## 🚀 方案2：Render.com部署

### 步骤1：注册Render账号

1. 访问 https://render.com
2. 点击"Get Started"注册账号
3. 使用GitHub账号登录

### 步骤2：创建Web Service

1. 点击"New +" → "Web Service"
2. 选择你的GitHub仓库：`LX1309244704/weiyuan`
3. 配置：
   - **Name**: `feishu-tools`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web.app:app --bind 0.0.0.0:5000 --workers 2`

### 步骤3：配置环境变量

在"Environment"部分添加：
```
FLASK_SECRET_KEY=your-random-secret-key
FLASK_ENV=production
FLASK_DEBUG=False
```

### 步骤4：部署并获取URL

1. 点击"Create Web Service"
2. Render会自动部署
3. 部署完成后会生成URL，例如：
   ```
   https://feishu-tools.onrender.com/
   ```

---

## 🎯 方案3：VPS + Docker部署

### 步骤1：准备VPS

购买一台云服务器（推荐配置）：
- CPU: 1核
- 内存: 1GB
- 硬盘: 10GB
- 系统: Ubuntu 20.04+

### 步骤2：安装Docker

```bash
# 更新系统
sudo apt update

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 步骤3：部署应用

```bash
# 克隆代码
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan

# 构建镜像
docker build -t feishu-tools .

# 运行容器
docker run -d \
  --name feishu-tools \
  -p 5000:5000 \
  -e FLASK_SECRET_KEY="your-secret-key" \
  -e FLASK_ENV="production" \
  --restart always \
  feishu-tools
```

### 步骤4：配置Nginx（可选）

```bash
# 安装Nginx
sudo apt install nginx

# 配置Nginx
sudo nano /etc/nginx/sites-available/feishu-tools
```

添加配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/feishu-tools /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 步骤5：配置HTTPS（可选）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com
```

---

## 📊 方案对比

| 方案 | 优点 | 缺点 | 成本 | 适用场景 |
|------|------|------|------|----------|
| **Railway** | 简单、自动部署、免费额度 | 流量限制 | $0-5/月 | 小型应用 ⭐ |
| **Render** | 简单、自动部署 | 免费额度少 | $0-7/月 | 小型应用 |
| **VPS** | 灵活、性能好 | 需要配置 | $5-10/月 | 中大型应用 |

---

## 🔧 本地测试

### 步骤1：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤2：设置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加你的配置
nano .env
```

### 步骤3：运行应用

```bash
# 开发模式
python web/app.py

# 或使用Gunicorn（生产模式）
gunicorn web.app:app --bind 0.0.0.0:5000 --workers 2
```

### 步骤4：访问应用

打开浏览器访问：
```
http://localhost:5000
```

---

## 🐛 常见问题

### 1. 部署失败

**问题**：Railway部署失败

**解决**：
- 检查Dockerfile是否正确
- 查看Railway日志：点击项目 → 点击部署 → 查看日志
- 确保requirements.txt包含所有依赖

### 2. 端口冲突

**问题**：5000端口已被占用

**解决**：
```bash
# 修改Dockerfile中的EXPOSE端口
EXPOSE 8080

# 修改启动命令
CMD ["python", "-m", "gunicorn", "web.app:app", "--bind", "0.0.0.0:8080"]
```

### 3. 环境变量未生效

**问题**：环境变量读取失败

**解决**：
- 确保在Railway的"Variables"中正确设置
- 检查变量名是否正确（不要有空格）
- 重新部署应用

### 4. API调用失败

**问题**：飞书API返回错误

**解决**：
- 检查FEISHU_APP_ID和FEISHU_APP_SECRET是否正确
- 确认应用权限是否足够
- 查看飞书开放平台的应用状态

---

## 📝 维护

### 更新应用

```bash
# 1. 修改代码并提交
git add .
git commit -m "Update code"
git push

# 2. Railway会自动检测到更新并重新部署
# 3. 等待部署完成即可
```

### 查看日志

```bash
# Railway: 点击项目 → 点击部署 → 查看日志
# Render: 点击项目 → Logs
# VPS: docker logs -f feishu-tools
```

### 停止应用

```bash
# Railway: 点击项目 → Settings → Delete
# Render: 点击项目 → Settings → Delete
# VPS: docker stop feishu-tools
```

---

## 🎯 推荐选择

### 个人开发者
**推荐**：Railway.app
- 免费额度充足
- 简单易用
- 自动部署

### 企业应用
**推荐**：VPS + Docker
- 性能稳定
- 完全控制
- 可扩展性好

---

## 📞 技术支持

如有问题，请：
1. 查看日志
2. 检查配置
3. 提交Issue：https://github.com/LX1309244704/weiyuan/issues

---

**🦞 飞书Python工具箱 - 让飞书管理更智能、更高效！**
