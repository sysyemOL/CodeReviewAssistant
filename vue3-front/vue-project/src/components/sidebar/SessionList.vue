<template>
  <div class="session-list">
    <div class="search-box">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索会话..."
        :prefix-icon="Search"
        clearable
      />
    </div>

    <div class="sessions">
      <div v-if="filteredSessions.length === 0" class="empty">
        <el-empty description="暂无会话" :image-size="80" />
      </div>

      <template v-else>
        <div
          v-for="session in filteredSessions"
          :key="session.session_id"
          class="session-item"
          :class="{ active: session.session_id === sessionStore.currentSessionId }"
          @click="handleSelectSession(session.session_id)"
        >
          <div class="session-info">
            <div class="session-title">{{ session.title }}</div>
            <div class="session-time">{{ formatTime(session.updated_at) }}</div>
          </div>
          
          <div class="session-actions">
            <el-dropdown trigger="click" @command="(cmd) => handleAction(cmd, session)">
              <el-icon class="action-icon">
                <MoreFilled />
              </el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="rename">
                    <el-icon><Edit /></el-icon>
                    重命名
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided>
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search, MoreFilled, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useSessionStore } from '@/stores/session'
import { formatTime } from '@/utils/format'

const sessionStore = useSessionStore()
const searchKeyword = ref('')

const filteredSessions = computed(() => {
  if (!searchKeyword.value) {
    return sessionStore.sortedSessions
  }
  return sessionStore.sortedSessions.filter(session =>
    session.title.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

const handleSelectSession = (sessionId) => {
  sessionStore.setCurrentSession(sessionId)
}

const handleAction = async (command, session) => {
  if (command === 'rename') {
    ElMessageBox.prompt('请输入新的会话名称', '重命名', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: session.title,
      inputValidator: (value) => {
        if (!value || value.trim() === '') {
          return '名称不能为空'
        }
        return true
      }
    }).then(async ({ value }) => {
      try {
        await sessionStore.updateSession(session.session_id, { title: value })
        ElMessage.success('重命名成功')
      } catch (error) {
        ElMessage.error('重命名失败')
      }
    }).catch(() => {})
  } else if (command === 'delete') {
    ElMessageBox.confirm(
      '确定要删除这个会话吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    ).then(async () => {
      try {
        await sessionStore.deleteSession(session.session_id)
        ElMessage.success('删除成功')
      } catch (error) {
        ElMessage.error('删除失败')
      }
    }).catch(() => {})
  }
}
</script>

<style scoped>
.session-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.search-box {
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
}

.sessions {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.empty {
  padding: 40px 0;
}

.session-item {
  padding: 12px;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.session-item:hover {
  background: #f5f7fa;
}

.session-item.active {
  background: #ecf5ff;
}

.session-info {
  flex: 1;
  min-width: 0;
}

.session-title {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 4px;
}

.session-time {
  font-size: 12px;
  color: #909399;
}

.session-actions {
  opacity: 0;
  transition: opacity 0.2s;
}

.session-item:hover .session-actions {
  opacity: 1;
}

.action-icon {
  font-size: 18px;
  color: #909399;
  cursor: pointer;
  padding: 4px;
}

.action-icon:hover {
  color: #606266;
}
</style>

