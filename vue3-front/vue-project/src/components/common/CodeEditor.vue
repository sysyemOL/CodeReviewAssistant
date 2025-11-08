<template>
  <div class="code-editor" ref="editorContainer" :class="themeClass"></div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as monaco from 'monaco-editor'
import { whiteGlassTheme, darkGlassTheme, pureWhiteTheme, darkTheme } from '@/utils/editorThemes'

const props = defineProps({
  fileId: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'python'
  },
  readonly: {
    type: Boolean,
    default: false
  },
  theme: {
    type: String,
    default: 'white-glass'
  }
})

const themeClass = computed(() => {
  return `theme-${props.theme}`
})

const emit = defineEmits(['update'])

const editorContainer = ref(null)
let editor = null

onMounted(() => {
  if (!editorContainer.value) return

  // 注册自定义主题
  monaco.editor.defineTheme('white-glass', whiteGlassTheme)
  monaco.editor.defineTheme('dark-glass', darkGlassTheme)
  monaco.editor.defineTheme('pure-white', pureWhiteTheme)

  // 创建编辑器
  editor = monaco.editor.create(editorContainer.value, {
    value: props.content,
    language: props.language,
    theme: props.theme,
    automaticLayout: true,
    minimap: {
      enabled: true
    },
    fontSize: 14,
    lineNumbers: 'on',
    scrollBeyondLastLine: false,
    readOnly: props.readonly,
    wordWrap: 'on',
    formatOnPaste: true,
    formatOnType: true,
    padding: {
      top: 16,
      bottom: 16
    }
  })

  // 监听内容变化
  editor.onDidChangeModelContent(() => {
    const newContent = editor.getValue()
    emit('update', props.fileId, newContent)
  })
})

onUnmounted(() => {
  if (editor) {
    editor.dispose()
  }
})

// 监听props变化
watch(() => props.content, (newContent) => {
  if (editor && newContent !== editor.getValue()) {
    const position = editor.getPosition()
    editor.setValue(newContent)
    if (position) {
      editor.setPosition(position)
    }
  }
})

watch(() => props.language, (newLanguage) => {
  if (editor) {
    const model = editor.getModel()
    if (model) {
      monaco.editor.setModelLanguage(model, newLanguage)
    }
  }
})

watch(() => props.theme, (newTheme) => {
  if (editor) {
    monaco.editor.setTheme(newTheme)
  }
})
</script>

<style scoped>
.code-editor {
  width: 100%;
  height: 100%;
  position: relative;
}

/* 毛玻璃主题背景 */
.code-editor.theme-white-glass,
.code-editor.theme-dark-glass {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.code-editor.theme-white-glass {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.7), 
    rgba(240, 242, 255, 0.7)
  );
}

.code-editor.theme-dark-glass {
  background: linear-gradient(135deg, 
    rgba(30, 30, 30, 0.8), 
    rgba(20, 20, 40, 0.8)
  );
}

.code-editor.theme-pure-white {
  background: #ffffff;
}

.code-editor.theme-vs-dark {
  background: #1e1e1e;
}
</style>

