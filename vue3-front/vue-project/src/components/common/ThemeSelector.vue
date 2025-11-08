<template>
  <div class="theme-selector">
    <el-dropdown trigger="click" @command="handleThemeSelect">
      <el-button circle :title="'当前主题：' + currentTheme.name">
        <span class="theme-icon">{{ currentTheme.icon }}</span>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item 
            v-for="theme in themes" 
            :key="theme.id"
            :command="theme.id"
            :class="{ active: theme.id === currentThemeId }"
          >
            <div class="theme-option">
              <span class="theme-preview" :style="{ background: theme.background }"></span>
              <span class="theme-icon">{{ theme.icon }}</span>
              <span class="theme-name">{{ theme.name }}</span>
              <el-icon v-if="theme.id === currentThemeId" class="check-icon">
                <Check />
              </el-icon>
            </div>
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Check } from '@element-plus/icons-vue'
import { editorThemes } from '@/utils/editorThemes'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'white-glass'
  }
})

const emit = defineEmits(['update:modelValue'])

const themes = editorThemes

const currentThemeId = computed(() => props.modelValue)

const currentTheme = computed(() => {
  return themes.find(t => t.id === currentThemeId.value) || themes[0]
})

const handleThemeSelect = (themeId) => {
  emit('update:modelValue', themeId)
}
</script>

<style scoped>
.theme-selector {
  display: flex;
  align-items: center;
}

.theme-icon {
  font-size: 18px;
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 8px;
  min-width: 180px;
}

.theme-option.active {
  background: rgba(64, 158, 255, 0.1);
}

.theme-preview {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 2px solid #e4e7ed;
  flex-shrink: 0;
}

.theme-name {
  flex: 1;
  font-size: 14px;
}

.check-icon {
  color: #409eff;
  font-size: 16px;
}
</style>

