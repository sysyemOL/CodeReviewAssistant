<template>
  <div class="portal-page">
    <!-- 动态渐变背景 -->
    <div class="animated-background"></div>
    
    <!-- 顶部标题 -->
    <header class="portal-header">
      <h1 class="portal-title">
        <span class="name-highlight">Liu Shuo</span>'s 
        <span class="event-name">雷客AI应用研发挑战赛作品</span>
      </h1>
    </header>

    <!-- 主内容区 - 湖面效果 -->
    <main class="portal-main">
      <!-- 上半部分 - 实际内容 -->
      <div class="water-surface">
        <div class="products-container">
          <!-- AI代码Review助手 -->
          <div class="product-card active" @click="goToCodeReview">
            <div class="card-content">
              <div class="product-icon code-review-icon">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                  <!-- 代码符号 -->
                  <circle cx="50" cy="50" r="45" fill="url(#blueGradient)" />
                  <text x="50" y="65" text-anchor="middle" fill="white" font-size="50" font-family="monospace" font-weight="bold">&lt;/&gt;</text>
                  <defs>
                    <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#409EFF;stop-opacity:1" />
                      <stop offset="100%" style="stop-color:#66b1ff;stop-opacity:1" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <h2 class="product-title">AI代码Review助手</h2>
              <p class="product-desc">智能代码审查 · 实时对话 · 多语言支持</p>
              <div class="status-badge active-badge">已上线</div>
            </div>
          </div>

          <!-- AI会议Summary助手 -->
          <div class="product-card coming-soon">
            <div class="card-content">
              <div class="product-icon meeting-icon">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                  <!-- 会议符号 -->
                  <circle cx="50" cy="50" r="45" fill="url(#grayGradient)" />
                  <text x="50" y="67" text-anchor="middle" fill="white" font-size="40" font-weight="bold">📝</text>
                  <defs>
                    <linearGradient id="grayGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#a0cfff;stop-opacity:0.5" />
                      <stop offset="100%" style="stop-color:#c0e0ff;stop-opacity:0.5" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <h2 class="product-title">AI会议Summary助手</h2>
              <p class="product-desc">会议记录 · 智能总结 · 任务提取</p>
              <div class="status-badge coming-badge">待开发</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 下半部分 - 镜面反射 -->
      <div class="water-reflection">
        <div class="products-container reflection">
          <!-- 反射效果 -->
          <div class="product-card active reflection-card">
            <div class="card-content">
              <div class="product-icon code-review-icon">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="50" cy="50" r="45" fill="url(#blueGradient2)" />
                  <text x="50" y="65" text-anchor="middle" fill="white" font-size="50" font-family="monospace" font-weight="bold">&lt;/&gt;</text>
                  <defs>
                    <linearGradient id="blueGradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#409EFF;stop-opacity:1" />
                      <stop offset="100%" style="stop-color:#66b1ff;stop-opacity:1" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <h2 class="product-title">AI代码Review助手</h2>
              <p class="product-desc">智能代码审查 · 实时对话 · 多语言支持</p>
              <div class="status-badge active-badge">已上线</div>
            </div>
          </div>

          <div class="product-card coming-soon reflection-card">
            <div class="card-content">
              <div class="product-icon meeting-icon">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="50" cy="50" r="45" fill="url(#grayGradient2)" />
                  <text x="50" y="67" text-anchor="middle" fill="white" font-size="40" font-weight="bold">📝</text>
                  <defs>
                    <linearGradient id="grayGradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#a0cfff;stop-opacity:0.5" />
                      <stop offset="100%" style="stop-color:#c0e0ff;stop-opacity:0.5" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <h2 class="product-title">AI会议Summary助手</h2>
              <p class="product-desc">会议记录 · 智能总结 · 任务提取</p>
              <div class="status-badge coming-badge">待开发</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 水面线 -->
      <div class="water-line"></div>
    </main>

    <!-- 页脚 -->
    <footer class="portal-footer">
      <p>© 2025 Liu Shuo - 雷客AI应用研发挑战赛</p>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToCodeReview = () => {
  router.push('/workspace')
}
</script>

<style scoped>
/* 动态渐变背景 - 蓝白色调 */
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.portal-page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(-45deg, 
    rgba(225, 240, 255, 0.98) 0%,   /* 浅蓝 */
    rgba(240, 248, 255, 0.98) 25%,   /* 爱丽丝蓝 */
    rgba(230, 245, 255, 0.98) 50%,   /* 天蓝 */
    rgba(240, 250, 255, 0.98) 75%,   /* 极浅蓝 */
    rgba(235, 245, 255, 0.98) 100%   /* 淡蓝 */
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  z-index: 0;
}

/* 顶部标题 */
.portal-header {
  position: relative;
  z-index: 10;
  padding: 40px 20px 20px;
  text-align: center;
}

.portal-title {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
  color: #1a73e8;
  text-shadow: 0 2px 8px rgba(26, 115, 232, 0.2);
}

.name-highlight {
  color: #409EFF;
  font-weight: 700;
  font-size: 36px;
}

.event-name {
  color: #5a9fd4;
  font-weight: 500;
}

/* 主内容区 */
.portal-main {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 40px;
}

/* 水面效果 */
.water-surface {
  position: relative;
  z-index: 2;
  padding-bottom: 60px;
}

.water-reflection {
  position: relative;
  z-index: 1;
  padding-top: 60px;
  transform: scaleY(-1);
  opacity: 0.4;
  mask-image: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, transparent 100%);
  pointer-events: none;
}

.water-line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, 
    transparent 0%,
    rgba(100, 180, 255, 0.3) 20%,
    rgba(100, 180, 255, 0.5) 50%,
    rgba(100, 180, 255, 0.3) 80%,
    transparent 100%
  );
  box-shadow: 0 0 20px rgba(100, 180, 255, 0.3);
  z-index: 5;
}

/* 产品容器 */
.products-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 80px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 产品卡片 */
.product-card {
  position: relative;
  width: 320px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card.active {
  cursor: pointer;
}

.product-card.active:hover {
  transform: translateY(-15px) scale(1.05);
}

.product-card.coming-soon {
  cursor: not-allowed;
  opacity: 0.8;
}

.card-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 40px 30px;
  box-shadow: 0 20px 60px rgba(64, 158, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(64, 158, 255, 0.2);
  transition: all 0.4s ease;
  text-align: center;
}

.product-card.active:hover .card-content {
  box-shadow: 0 30px 80px rgba(64, 158, 255, 0.3);
  border-color: rgba(64, 158, 255, 0.4);
}

/* 产品图标 */
.product-icon {
  width: 140px;
  height: 140px;
  margin: 0 auto 30px;
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s ease;
}

.product-card.active:hover .product-icon {
  transform: scale(1.1);
  animation-play-state: paused;
}

.product-icon svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 8px 16px rgba(64, 158, 255, 0.3));
}

/* 产品标题 */
.product-title {
  font-size: 26px;
  font-weight: 600;
  color: #1a73e8;
  margin: 0 0 15px;
  transition: all 0.3s ease;
}

.product-card.coming-soon .product-title {
  color: #8bb4d9;
}

/* 产品描述 */
.product-desc {
  font-size: 15px;
  color: #5a9fd4;
  margin: 0 0 20px;
  line-height: 1.6;
}

.product-card.coming-soon .product-desc {
  color: #a0c4de;
}

/* 状态徽章 */
.status-badge {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.active-badge {
  background: linear-gradient(135deg, #409EFF, #66b1ff);
  color: white;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.coming-badge {
  background: linear-gradient(135deg, rgba(160, 207, 255, 0.5), rgba(192, 224, 255, 0.5));
  color: #5a9fd4;
  border: 1px solid rgba(90, 159, 212, 0.3);
}

/* 反射卡片调整 */
.reflection-card {
  pointer-events: none;
}

/* 页脚 */
.portal-footer {
  position: relative;
  z-index: 10;
  padding: 30px 20px;
  text-align: center;
  color: #5a9fd4;
  font-size: 14px;
}

.portal-footer p {
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .portal-title {
    font-size: 24px;
  }
  
  .name-highlight {
    font-size: 28px;
  }
  
  .products-container {
    flex-direction: column;
    align-items: center;
    gap: 40px;
  }
  
  .product-card {
    width: 280px;
  }
  
  .water-reflection {
    display: none;
  }
  
  .water-line {
    display: none;
  }
}

/* 添加悬浮动画 - 仅应用于图标 */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.product-icon {
  animation: float 3s ease-in-out infinite;
}

.product-card.coming-soon .product-icon {
  animation: float 4s ease-in-out infinite;
  animation-delay: 0.5s;
}
</style>

