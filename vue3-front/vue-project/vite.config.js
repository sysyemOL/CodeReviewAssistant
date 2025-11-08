import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    host: 'localhost',  // 使用localhost而不是127.0.0.1，避免CORS问题
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 保持一致使用localhost
        changeOrigin: true,
        secure: false,
      }
    }
  },
  optimizeDeps: {
    include: ['monaco-editor']
  }
})
