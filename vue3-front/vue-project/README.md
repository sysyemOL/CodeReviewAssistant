# AI代码Review助手 - 前端项目

基于 Vue 3 + Vite + Element Plus 构建的现代化代码审查助手前端应用。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 7
- **UI组件库**: Element Plus 2.4
- **代码编辑器**: Monaco Editor 0.44
- **状态管理**: Pinia 2.1
- **路由**: Vue Router 4.2
- **HTTP客户端**: Axios 1.6
- **Markdown渲染**: Marked 11
- **代码高亮**: Highlight.js 11.9

## 项目结构

```
src/
├── api/                    # API请求封装
│   ├── request.js         # Axios实例配置
│   ├── session.js         # 会话相关API
│   ├── review.js          # 代码审查API
│   └── file.js            # 文件上传API
├── components/            # 组件
│   ├── common/           # 公共组件
│   │   └── CodeEditor.vue # Monaco编辑器
│   ├── chat/             # 聊天相关组件
│   │   ├── MessageList.vue
│   │   ├── MessageItem.vue
│   │   └── InputBox.vue
│   └── sidebar/          # 侧边栏组件
│       └── SessionList.vue
├── views/                # 页面视图
│   └── ReviewWorkspace.vue # 主工作区
├── stores/               # Pinia状态管理
│   ├── app.js           # 应用全局状态
│   ├── session.js       # 会话状态
│   ├── message.js       # 消息状态
│   └── file.js          # 文件状态
├── router/              # 路由配置
│   └── index.js
├── utils/               # 工具函数
│   ├── format.js        # 格式化工具
│   └── file.js          # 文件处理工具
├── App.vue              # 根组件
└── main.js              # 入口文件
```

## 功能特性

### 已实现功能

- ✅ 三栏布局设计（会话列表 + 对话区 + 代码编辑器）
- ✅ 会话管理（创建、删除、重命名、搜索）
- ✅ 消息展示（支持Markdown渲染和代码高亮）
- ✅ 文件上传（拖拽上传 + 点击上传）
- ✅ Monaco代码编辑器集成
- ✅ 多文件Tab切换
- ✅ 响应式布局

### 待实现功能

- ⏳ SSE流式输出
- ⏳ 代码审查功能对接
- ⏳ 代码Diff对比
- ⏳ 暗色主题切换
- ⏳ 文件夹上传
- ⏳ 导出审查报告

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 环境配置

后端API地址配置在 `vite.config.js` 中：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // 后端API地址
      changeOrigin: true,
    }
  }
}
```

## 开发说明

### 组件开发规范

1. 使用 Vue 3 Composition API (`<script setup>`)
2. 使用 Pinia 进行状态管理
3. 使用 Element Plus 组件库
4. 遵循单一职责原则，组件保持简洁

### API调用规范

所有API调用都通过 `src/api/` 目录下的模块进行封装：

```javascript
import { sessionAPI } from '@/api/session'

// 获取会话列表
const sessions = await sessionAPI.getSessions()
```

### 状态管理规范

使用Pinia stores管理应用状态：

```javascript
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()
sessionStore.createSession('新对话')
```

## 常见问题

### 1. Monaco Editor加载慢？

Monaco Editor是VSCode的编辑器核心，首次加载会较慢。已在vite.config.js中配置优化：

```javascript
optimizeDeps: {
  include: ['monaco-editor']
}
```

### 2. Element Plus样式问题？

确保在main.js中正确引入了样式文件：

```javascript
import 'element-plus/dist/index.css'
```

### 3. 代理配置不生效？

检查vite.config.js中的proxy配置，确保后端服务已启动。

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## License

MIT

---

**开发团队**: AI代码Review助手项目组  
**最后更新**: 2025-11-07
