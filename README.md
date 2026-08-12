# 英语 70 天学习系统

一个基于 Vue 3 + TypeScript 的英语学习 Web 应用，采用 Unit 驱动的学习模式。

## 功能特性

- 📚 70 天固定学习计划
- 📝 每日新单词（最多 35 个）
- 🔄 上一学习日完整复习
- 📖 核心句型学习
- 🎯 练习与错题管理
- 📊 学习进度跟踪

## 技术栈

- Vue 3 + TypeScript
- Vite 构建工具
- Vue Router 路由管理
- Pinia 状态管理
- Nginx 生产部署
- Docker 容器化

## 快速开始

### 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### Docker 部署

```bash
# 构建镜像
docker build -t english-learning-app .

# 运行容器
docker run -p 3000:80 english-learning-app

# 或使用 docker-compose
docker-compose up -d
```

访问 http://localhost:3000 即可使用。

## 数据处理

项目包含数据处理脚本：

```bash
# 分析数据源
python3 scripts/content/normalize-source.py

# 构建 70 天计划
python3 scripts/content/build-70-day-plan.py

# 验证计划
python3 scripts/content/validate-plan.py

# 生成报告
python3 scripts/content/generate-report.py
```

## 项目结构

```
├── src/                    # 源代码
│   ├── features/          # 功能模块
│   ├── router/            # 路由配置
│   └── main.ts            # 入口文件
├── scripts/               # 数据处理脚本
│   └── content/           # 内容处理
├── Unit_*                 # 单元数据源
├── Dockerfile             # Docker 构建配置
├── docker-compose.yml     # Docker Compose 配置
├── nginx.conf             # Nginx 配置
└── package.json           # 项目配置
```

## 学习计划

70 天学习计划基于 12 个单元（Unit）的内容：

1. The Power of Language
2. Mistakes to Success
3. Friendship and Loyalty
4. The Joy of Work
5. Keeping Your Dreams Alive
6. The Value of Money
7. Inner Voice
8. The Great Minds
9. Facing Life's Challenges
10. Ode to Public Transport
11. Cyber World
12. A Break from Life

## 数据来源

- 词汇手册：760 个单词 + 144 个短语
- 12 个单元文件（每个包含笔记、短语、句型、对话、练习）

## 许可证

MIT
