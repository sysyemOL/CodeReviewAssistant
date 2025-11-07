<template>
  <div class="code-editor" ref="editorContainer"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as monaco from 'monaco-editor'

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
  }
})

const emit = defineEmits(['update'])

const editorContainer = ref(null)
let editor = null

onMounted(() => {
  if (!editorContainer.value) return

  // 创建编辑器
  editor = monaco.editor.create(editorContainer.value, {
    value: props.content,
    language: props.language,
    theme: 'vs-dark',
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
    formatOnType: true
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
</script>

<style scoped>
.code-editor {
  width: 100%;
  height: 100%;
}
</style>

