<template>
  <div class="message-board">
    <div class="main-content">
      <el-card class="form-card" shadow="always">
        <template #header>
          <div class="card-header">
            <el-avatar icon="el-icon-user" class="avatar" />
            <span class="form-title">发布新动态</span>
          </div>
        </template>
        <el-form @submit.prevent="submitMessage">
          <el-form-item>
            <el-input
              v-model="newMessage"
              maxlength="140"
              show-word-limit
              type="textarea"
              :rows="3"
              placeholder="此刻你想说点什么..."
              resize="none"
              class="weibo-input"
            />
          </el-form-item>
          <el-form-item style="margin-bottom: 0;">
            <el-button 
              type="primary" 
              :disabled="!newMessage.trim()" 
              @click="submitMessage"
              style="width: 100%;"
              size="large"
            >
              <el-icon><Promotion /></el-icon>
              发布
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="list-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="list-title">最新动态</span>
            <el-badge :value="messages.length" class="item" type="primary" />
          </div>
        </template>
        <div class="scroll-list">
          <el-empty v-if="messages.length === 0" description="暂无内容，快来发表第一条吧！">
            <el-icon style="font-size: 60px; color: #409EFF;"><ChatDotRound /></el-icon>
          </el-empty>
          <div v-else class="message-list">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="message-item"
            >
              <div class="message-header">
                <el-avatar icon="el-icon-user" class="avatar" />
                <div class="meta">
                  <el-tag size="small" type="info">#{{ msg.id }}</el-tag>
                  <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
                </div>
              </div>
              <div class="message-content">{{ msg.content }}</div>
              <div class="message-actions">
                <el-button size="small" type="success" plain @click="likeMessage(msg.id)">
                  <el-icon><CaretTop /></el-icon>
                  {{ msg.like_count }}
                </el-button>
                <el-button size="small" type="danger" plain @click="dislikeMessage(msg.id)">
                  <el-icon><CaretBottom /></el-icon>
                  {{ msg.dislike_count }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ChatDotRound, CaretTop, CaretBottom, Promotion } from '@element-plus/icons-vue'
import { API_ENDPOINTS, getApiUrl, SUCCESS_MESSAGES, MESSAGE_CONFIG } from '../config/api.js'
import { 
  showErrorMessage, 
  showSuccessMessage, 
  retryApiCall, 
  validateInput 
} from '../utils/errorHandler.js'

const newMessage = ref('')
const messages = ref([])
const isLoading = ref(false)
const isSubmitting = ref(false)
let refreshTimer = null

/**
 * 获取留言列表
 */
const fetchMessages = async () => {
  try {
    isLoading.value = true
    const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES))
    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '获取留言失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }
    const response = await res.json()
    messages.value = response.data || []
    console.log(`成功获取 ${messages.value.length} 条留言`)
  } catch (error) {
    showErrorMessage(error, '获取留言列表')
  } finally {
    isLoading.value = false
  }
}

/**
 * 提交新留言
 */
const submitMessage = async () => {
  const content = newMessage.value.trim()
  // 验证输入
  const validation = validateInput(content, MESSAGE_CONFIG.MAX_LENGTH, MESSAGE_CONFIG.MIN_LENGTH)
  if (!validation.isValid) {
    showErrorMessage(new Error(validation.message), '输入验证')
    return
  }
  try {
    isSubmitting.value = true
    const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })
    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '发布留言失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }
    showSuccessMessage(SUCCESS_MESSAGES.MESSAGE_CREATED)
    newMessage.value = ''
    await fetchMessages()
  } catch (error) {
    showErrorMessage(error, '发布留言')
  } finally {
    isSubmitting.value = false
  }
}

/**
 * 点赞留言
 * @param {number} id - 留言ID
 */
const likeMessage = async (id) => {
  try {
    const res = await fetch(getApiUrl(API_ENDPOINTS.LIKE_MESSAGE(id)), { method: 'POST' })
    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '点赞失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }
    showSuccessMessage(SUCCESS_MESSAGES.MESSAGE_LIKED)
    await fetchMessages()
  } catch (error) {
    showErrorMessage(error, '点赞操作')
  }
}

/**
 * 踩留言
 * @param {number} id - 留言ID
 */
const dislikeMessage = async (id) => {
  try {
    const res = await fetch(getApiUrl(API_ENDPOINTS.DISLIKE_MESSAGE(id)), { method: 'POST' })
    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '踩失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }
    showSuccessMessage(SUCCESS_MESSAGES.MESSAGE_DISLIKED)
    await fetchMessages()
  } catch (error) {
    showErrorMessage(error, '踩操作')
  }
}

/**
 * 格式化时间显示
 * @param {string} timestamp - 时间戳
 * @returns {string} 格式化后的时间
 */
const formatTime = (timestamp) => {
  try {
    return new Date(timestamp).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    console.error('时间格式化错误:', error)
    return '时间格式错误'
  }
}

/**
 * 设置自动刷新
 */
const setupAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    if (!isLoading.value && !isSubmitting.value) {
      fetchMessages()
    }
  }, MESSAGE_CONFIG.REFRESH_INTERVAL)
}

/**
 * 清除自动刷新
 */
const clearAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 组件挂载时初始化
onMounted(() => {
  fetchMessages()
  setupAutoRefresh()
})

// 组件卸载时清理
onUnmounted(() => {
  clearAutoRefresh()
})
</script>

<style scoped>
.message-board {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 新增：垂直居中主内容 */
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%);
  padding: 32px 0 0 0;
}

.main-content {
  width: 480px;
  max-width: 96vw;
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin: 0 auto; /* 新增：水平居中 */
}

.form-card {
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.04);
  margin-bottom: 0;
}

.form-title {
  font-size: 18px;
  font-weight: bold;
  margin-left: 8px;
}

.weibo-input {
  font-size: 16px;
  border-radius: 12px;
}

.list-card {
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.04);
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.list-title {
  font-size: 18px;
  font-weight: bold;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.scroll-list {
  flex: 1;
  overflow-y: scroll;
  overflow-x: hidden;
  height: 420px;
  padding: 10px 16px;
  margin: 0;
  background: none;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.message-item {
  padding: 18px 16px 12px 16px;
  background: #f9fafb;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  transition: box-shadow 0.2s;
  box-shadow: 0 1px 4px 0 rgba(0,0,0,0.03);
}

.message-item:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  background: #fff;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.avatar {
  background: #e0e7ef;
  color: #409EFF;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
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
}

.message-actions {
  display: flex;
  gap: 8px;
}

:deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: #f8fafc;
}

:deep(.el-button) {
  border-radius: 12px;
  font-weight: 500;
}

:deep(.el-card__body) {
  padding: 16px;
}

.scroll-list::-webkit-scrollbar {
  width: 8px;
}

.scroll-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  margin: 8px 0;
}

.scroll-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.18);
  border-radius: 4px;
  transition: background 0.3s ease;
}

.scroll-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.32);
}
</style>
