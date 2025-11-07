<template>
  <div class="message-list">
    <div v-if="messages.length === 0" class="empty-state">
      <el-empty description="开始你的代码审查之旅吧！">
        <template #image>
          <el-icon :size="100" color="#909399">
            <ChatDotRound />
          </el-icon>
        </template>
      </el-empty>
    </div>

    <div v-else class="messages">
      <MessageItem
        v-for="message in messages"
        :key="message.message_id"
        :message="message"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChatDotRound } from '@element-plus/icons-vue'
import { useMessageStore } from '@/stores/message'
import MessageItem from './MessageItem.vue'

const props = defineProps({
  sessionId: {
    type: String,
    default: null
  }
})

const messageStore = useMessageStore()

const messages = computed(() => {
  if (!props.sessionId) return []
  return messageStore.getSessionMessages(props.sessionId).value
})
</script>

<style scoped>
.message-list {
  height: 100%;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>

