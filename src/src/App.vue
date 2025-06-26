<template>
  <div class="treehole-app">
    <header class="app-header">
      <h1>匿名树洞</h1>
    </header>
    <main class="app-main">
      <section class="input-section">
        <el-input
          v-model="newMessage"
          maxlength="140"
          show-word-limit
          type="textarea"
          :rows="3"
          placeholder="你想说点什么..."
          resize="none"
          class="weibo-input"
        />
        <el-button 
          type="primary" 
          :disabled="!newMessage.trim()" 
          @click="submitMessage"
          size="large"
          class="submit-btn"
        >
          发布
        </el-button>
      </section>
      <section class="list-section">
        <div class="message-list">
          <div
            v-for="msg in [...messages].reverse()"
            :key="msg.id"
            class="message-item"
          >
            <div class="message-meta">
              <el-tag size="small" type="info">#{{ msg.id }}</el-tag>
              <span class="timestamp">🕒 {{ formatTime(msg.timestamp) }}</span>
            </div>
            <div class="message-content">{{ msg.content }}</div>
            <div class="message-actions">
              <el-button size="small" type="success" plain @click="likeMessage(msg.id)">
                👍 {{ msg.like_count }}
              </el-button>
              <el-button size="small" type="danger" plain @click="dislikeMessage(msg.id)">
                👎 {{ msg.dislike_count }}
              </el-button>
              <span class="reply-count">💬 {{ msg.reply_count || 0 }}</span>
            </div>
            <div v-if="msg.replies && msg.replies.length" class="replies">
              <div v-for="reply in msg.replies" :key="reply.id" class="reply-item">
                <div class="reply-meta">
                  <el-tag size="small" type="info">#{{ reply.id }}</el-tag>
                  <span class="timestamp">🕒 {{ formatTime(reply.timestamp) }}</span>
                </div>
                <div class="reply-content">{{ reply.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchMessages, postMessage, likeMessage as apiLike, dislikeMessage as apiDislike } from './config/api'

// 新留言内容
const newMessage = ref('')
// 留言列表
const messages = ref([])
// 加载状态
const loading = ref(false)

// 获取留言列表
const loadMessages = async () => {
  loading.value = true
  try {
    const res = await fetchMessages()
    if (res.code === 0) {
      messages.value = res.data
    } else {
      ElMessage.error(res.message || '获取留言失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
  loading.value = false
}

// 发布留言
const submitMessage = async () => {
  if (!newMessage.value.trim()) {
    ElMessage.warning('请输入内容')
    return
  }
  try {
    const res = await postMessage({ content: newMessage.value })
    if (res.code === 0) {
      ElMessage.success('留言成功')
      newMessage.value = ''
      loadMessages()
    } else {
      ElMessage.error(res.message || '留言失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}

// 点赞
const likeMessage = async (id) => {
  try {
    const res = await apiLike(id)
    if (res.code === 0) {
      loadMessages()
    } else {
      ElMessage.error(res.message || '点赞失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}

// 点踩
const dislikeMessage = async (id) => {
  try {
    const res = await apiDislike(id)
    if (res.code === 0) {
      loadMessages()
    } else {
      ElMessage.error(res.message || '点踩失败')
    }
  } catch (e) {
    ElMessage.error('网络错误')
  }
}

// 时间格式化
const formatTime = (t) => {
  if (!t) return ''
  const date = new Date(t)
  return date.toLocaleString()
}

onMounted(loadMessages)
</script>

<style scoped>
html {
  width: 100vw;
  min-height: 100vh;
  max-width: 100vw;
  overflow-x: hidden;
}
body, #app {
  width: 100vw;
  min-height: 100vh;
  max-width: 100vw;
  margin: 0;
  padding: 0;
}
.treehole-app {
  max-width: 1280px;
  min-height: 100vh;
  margin: 0 auto;
  background: #fff;
  border-radius: 0;
  box-shadow: none;
  padding-bottom: 32px;
}
.app-header {
  padding: 24px 0 8px 0;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}
.app-header h1 {
  font-size: 2rem;
  font-weight: bold;
  letter-spacing: 2px;
  color: #409EFF;
  margin: 0;
}
.app-main {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 24px 0 24px;
}
.input-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}
.weibo-input {
  font-size: 16px;
  border-radius: 12px;
}
.submit-btn {
  align-self: flex-end;
  width: 120px;
}
.list-section {
  max-height: 70vh;
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: 8px;
}
.message-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
  align-items: stretch;
}
.message-item {
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  padding: 16px 14px 10px 14px;
  box-shadow: 0 1px 4px 0 rgba(0,0,0,0.03);
  text-align: left;
}
.message-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.timestamp {
  font-size: 12px;
  color: #909399;
}
.message-content {
  font-size: 15px;
  line-height: 1.7;
  color: #303133;
  margin-bottom: 10px;
  word-break: break-word;
  text-align: left;
}
.message-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 4px;
}
.reply-count {
  color: #409EFF;
  font-size: 13px;
}
.replies {
  margin-left: 24px;
  margin-top: 8px;
  border-left: 2px solid #e5e7eb;
  padding-left: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.reply-item {
  background: #f4f8fb;
  border-radius: 8px;
  padding: 8px 10px;
  border: 1px solid #e0e7ef;
}
.reply-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}
.reply-content {
  font-size: 14px;
  color: #555;
  text-align: left;
}
</style>
