<template>
  <div class="markdown-test">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Markdown 渲染测试</span>
          <el-button type="primary" @click="addTestMessage">添加测试消息</el-button>
        </div>
      </template>
      
      <div class="test-content">
        <MarkdownRenderer :content="testMarkdown" :dark-mode="false" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

const testMarkdown = ref(`# 代码质量分析报告

## 1. 整体评估

这段代码的整体质量**良好**，但存在几个需要改进的地方。

### 主要发现

- ⚠️ **缺少错误处理**：没有对异常情况进行处理
- 📝 **注释不足**：关键逻辑缺少说明性注释
- 🔄 **性能可优化**：存在一些可以改进的地方
- ✅ **代码结构清晰**：整体架构合理

---

## 2. 代码示例

### Python 示例

\`\`\`python
def calculate_sum(numbers):
    """
    计算数字列表的总和
    
    Args:
        numbers (list): 输入的数字列表
        
    Returns:
        int: 总和
    """
    try:
        return sum(numbers)
    except TypeError:
        print("输入必须是数字列表")
        return 0
\`\`\`

### JavaScript 示例

\`\`\`javascript
function calculateSum(numbers) {
    try {
        return numbers.reduce((sum, num) => sum + num, 0);
    } catch (error) {
        console.error('Error:', error);
        return 0;
    }
}
\`\`\`

---

## 3. 性能对比

| 方法 | 时间复杂度 | 空间复杂度 | 实际耗时 |
|------|----------|----------|---------|
| 方法A | O(n) | O(1) | ~100ms |
| 方法B | O(n²) | O(n) | ~250ms |
| **提升** | - | - | **+60%** |

---

## 4. 最佳实践

### 行内代码

使用 \`Array.map()\` 方法可以简化代码。

### 引用块

> 💡 **性能提示**
> 
> 使用列表推导式替代循环可以提升性能。

### 任务列表

- [x] 完成代码审查
- [x] 添加单元测试
- [ ] 性能优化
- [ ] 文档完善

---

## 5. 总结

✨ **总体评价**：代码基础良好，通过改进可以达到生产级别的质量标准。

**下一步建议**：
1. 添加完整的错误处理
2. 编写单元测试
3. 性能测试验证
4. 文档补充完善

如果您有任何疑问，欢迎继续提问！ 😊`)

const addTestMessage = () => {
  console.log('Test markdown content:', testMarkdown.value)
}
</script>

<style scoped>
.markdown-test {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.test-content {
  max-height: 80vh;
  overflow-y: auto;
}
</style>

