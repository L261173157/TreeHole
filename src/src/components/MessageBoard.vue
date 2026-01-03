<template>
  <div class="message-board">
    <div class="main-content">
      <!-- 标题 -->
      <header class="app-header">
        <h1 class="app-title">树洞</h1>
        <p class="app-subtitle">匿名分享你的想法</p>
      </header>

      <!-- 发布区域 -->
      <div class="create-section">
        <textarea
          v-model="newMessage"
          class="message-input"
          placeholder="分享你的想法..."
          maxlength="140"
          @input="updateCount"
        />
        <div class="input-footer">
          <span class="char-count" :class="{ 'near-limit': remainingChars <= 20 }">
            {{ remainingChars }}/140
          </span>
          <button
            class="send-btn"
            :disabled="!newMessage.trim() || isSubmitting"
            @click="submitMessage"
          >
            {{ isSubmitting ? '发布中...' : '发布' }}
          </button>
        </div>
      </div>

      <!-- 留言列表 -->
      <div class="messages-section">
        <div v-if="messages.length === 0" class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>还没有留言,来发表第一条吧!</p>
        </div>

        <div v-else class="message-list">
          <article v-for="msg in messages" :key="msg.id" class="message-card">
            <!-- 留言内容 -->
            <div class="message-content">{{ msg.content }}</div>

            <!-- 留言元信息 -->
            <div class="message-meta">
              <span class="message-id">#{{ msg.id }}</span>
              <span class="message-time">{{ formatTime(msg.timestamp) }}</span>
              <span v-if="msg.location" class="message-location">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ msg.location }}
              </span>
            </div>

            <!-- 操作按钮 -->
            <div class="message-actions">
              <button class="action-btn" @click="likeMessage(msg.id)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ msg.like_count || 0 }}</span>
              </button>

              <button class="action-btn" @click="dislikeMessage(msg.id)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ msg.dislike_count || 0 }}</span>
              </button>

              <button class="action-btn" @click="toggleReplies(msg.id)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ msg.reply_count || 0 }}</span>
              </button>
            </div>

            <!-- 回复区域 -->
            <div v-if="expandedReplies.has(msg.id)" class="replies-section">
              <!-- 回复列表 -->
              <div v-if="loadingReplies.has(msg.id)" class="loading-replies">
                加载中...
              </div>
              <div v-else-if="replies[msg.id] && replies[msg.id].length > 0" class="replies-list">
                <div v-for="reply in replies[msg.id]" :key="reply.id" class="reply-item">
                  <div class="reply-content">{{ reply.content }}</div>
                  <div class="reply-meta">
                    <span class="reply-time">{{ formatTime(reply.timestamp) }}</span>
                    <span v-if="reply.location" class="reply-location">
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      {{ reply.location }}
                    </span>
                  </div>
                </div>
              </div>
              <div v-else class="no-replies">
                还没有回复,快来抢沙发!
              </div>

              <!-- 回复输入框 -->
              <div class="reply-input-section">
                <textarea
                  :ref="el => replyInputRefs[msg.id] = el"
                  v-model="replyContents[msg.id]"
                  class="reply-input"
                  placeholder="写下你的回复..."
                  maxlength="140"
                  rows="2"
                />
                <div class="reply-actions">
                  <span class="char-count-small">{{ 140 - (replyContents[msg.id]?.length || 0) }}</span>
                  <button
                    class="reply-btn"
                    :disabled="!replyContents[msg.id]?.trim() || submittingReplies.has(msg.id)"
                    @click="submitReply(msg.id)"
                  >
                    {{ submittingReplies.has(msg.id) ? '发送中...' : '发送' }}
                  </button>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const newMessage = ref('')
const messages = ref([])
const isSubmitting = ref(false)
const isLoading = ref(false)

// 回复相关状态
const expandedReplies = ref(new Set())
const replies = ref({})
const loadingReplies = ref(new Set())
const submittingReplies = ref(new Set())
const replyContents = ref({})
const replyInputRefs = ref({})

let refreshTimer = null

// 计算剩余字符数
const remainingChars = computed(() => 140 - (newMessage.value?.length || 0))

// API配置
// 开发环境: http://127.0.0.1:8000
// 生产环境: /api (通过nginx代理)
const API_BASE = import.meta.env.VITE_API_BASE_URL || (import.meta.env.MODE === 'production' ? '/api' : 'http://127.0.0.1:8000')

// 获取留言列表
const fetchMessages = async () => {
  if (isLoading.value) return
  isLoading.value = true

  try {
    const res = await fetch(`${API_BASE}/messages/`)
    if (!res.ok) throw new Error('获取留言失败')

    const response = await res.json()
    messages.value = response.data || []
  } catch (error) {
    console.error('获取留言失败:', error)
  } finally {
    isLoading.value = false
  }
}

// 发布留言
const submitMessage = async () => {
  const content = newMessage.value.trim()
  if (!content) return

  isSubmitting.value = true

  try {
    const res = await fetch(`${API_BASE}/messages/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || '发布失败')
    }

    newMessage.value = ''
    await fetchMessages()
  } catch (error) {
    alert(error.message || '发布失败')
  } finally {
    isSubmitting.value = false
  }
}

// 点赞
const likeMessage = async (id) => {
  try {
    await fetch(`${API_BASE}/messages/${id}/like`, { method: 'POST' })
    await fetchMessages()
  } catch (error) {
    console.error('点赞失败:', error)
  }
}

// 点踩
const dislikeMessage = async (id) => {
  try {
    await fetch(`${API_BASE}/messages/${id}/dislike`, { method: 'POST' })
    await fetchMessages()
  } catch (error) {
    console.error('点踩失败:', error)
  }
}

// 切换回复展开/收起
const toggleReplies = async (messageId) => {
  if (expandedReplies.value.has(messageId)) {
    expandedReplies.value.delete(messageId)
  } else {
    expandedReplies.value.add(messageId)

    // 如果还没有加载过回复,则加载
    if (!replies.value[messageId]) {
      await loadReplies(messageId)
    }
  }

  // 强制更新
  expandedReplies.value = new Set(expandedReplies.value)
}

// 加载回复列表
const loadReplies = async (messageId) => {
  loadingReplies.value.add(messageId)

  try {
    const res = await fetch(`${API_BASE}/messages/${messageId}/replies`)
    if (!res.ok) throw new Error('获取回复失败')

    const response = await res.json()
    replies.value[messageId] = response.data || []
  } catch (error) {
    console.error('获取回复失败:', error)
    replies.value[messageId] = []
  } finally {
    loadingReplies.value.delete(messageId)
    loadingReplies.value = new Set(loadingReplies.value)
  }
}

// 提交回复
const submitReply = async (messageId) => {
  const content = replyContents.value[messageId]?.trim()
  if (!content) return

  submittingReplies.value.add(messageId)

  try {
    const res = await fetch(`${API_BASE}/messages/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        content,
        parent_id: messageId
      })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || '回复失败')
    }

    // 清空回复输入框
    replyContents.value[messageId] = ''

    // 重新加载回复列表
    await loadReplies(messageId)

    // 重新加载主列表以更新回复数
    await fetchMessages()
  } catch (error) {
    alert(error.message || '回复失败')
  } finally {
    submittingReplies.value.delete(messageId)
    submittingReplies.value = new Set(submittingReplies.value)
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date

    // 小于1分钟
    if (diff < 60000) {
      return '刚刚'
    }

    // 小于1小时
    if (diff < 3600000) {
      return `${Math.floor(diff / 60000)}分钟前`
    }

    // 小于24小时
    if (diff < 86400000) {
      return `${Math.floor(diff / 3600000)}小时前`
    }

    // 大于24小时,显示完整日期
    return date.toLocaleDateString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return ''
  }
}

const updateCount = () => {
  // 触发计算属性更新
}

// 自动刷新
const setupAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    if (!isLoading.value) {
      fetchMessages()
    }
  }, 30000)
}

const clearAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

onMounted(() => {
  fetchMessages()
  setupAutoRefresh()
})

onUnmounted(() => {
  clearAutoRefresh()
})
</script>

<style scoped>
.message-board {
  min-height: 100vh;
  max-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 16px;
  display: flex;
  justify-content: center;
  text-align: left;
  overflow-y: auto;
  /* 显示滚动条 */
  scrollbar-width: auto; /* Firefox */
  -ms-overflow-style: auto; /* IE/Edge */
}

.message-board::-webkit-scrollbar {
  width: 8px; /* Chrome/Safari */
}

.message-board::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.message-board::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

.message-board::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.message-board * {
  text-align: left !important;
}

.main-content {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 16px;
}

/* 标题区域 */
.app-header {
  text-align: left;
  color: white;
  margin-bottom: 4px;
}

.app-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  letter-spacing: 2px;
}

.app-subtitle {
  font-size: 13px;
  margin: 0;
  opacity: 0.9;
  font-weight: 300;
}

/* 创建区域 */
.create-section {
  background: white;
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.message-input {
  width: 100%;
  border: none;
  outline: none;
  font-size: 15px;
  font-family: inherit;
  resize: none;
  min-height: 60px;
  max-height: 120px;
  color: #333;
  margin-bottom: 10px;
}

.message-input::placeholder {
  color: #999;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-count {
  font-size: 13px;
  color: #999;
}

.char-count.near-limit {
  color: #f56c6c;
  font-weight: 500;
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  opacity: 0.9;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 留言区域 */
.messages-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty-state {
  background: white;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: left;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.empty-state svg {
  color: #667eea;
  margin-bottom: 12px;
}

.empty-state p {
  color: #666;
  font-size: 15px;
}

/* 留言卡片 */
.message-card {
  background: white;
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.message-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.15);
}

.message-content {
  font-size: 15px;
  line-height: 1.5;
  color: #333;
  margin-bottom: 10px;
  word-break: break-word;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
}

.message-id {
  font-size: 12px;
  color: #999;
  font-weight: 500;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-location {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
}

.message-location svg {
  stroke-width: 2;
}

/* 操作按钮 */
.message-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: none;
  background: #f5f5f5;
  border-radius: 10px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e8e8e8;
  color: #333;
}

.action-btn svg {
  stroke-width: 2;
}

/* 回复区域 */
.replies-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.loading-replies,
.no-replies {
  text-align: left;
  padding: 14px;
  color: #999;
  font-size: 13px;
}

.replies-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 12px;
}

.reply-item {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 12px;
}

.reply-content {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  margin-bottom: 6px;
  word-break: break-word;
}

.reply-meta {
  display: flex;
  justify-content: flex-end;
}

.reply-time {
  font-size: 11px;
  color: #999;
}

.reply-location {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  color: #667eea;
  font-weight: 500;
  margin-left: 8px;
}

.reply-location svg {
  stroke-width: 2;
}

/* 回复输入框 */
.reply-input-section {
  background: #fafafa;
  border-radius: 10px;
  padding: 12px;
}

.reply-input {
  width: 100%;
  border: none;
  outline: none;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  background: transparent;
  margin-bottom: 8px;
  color: #333;
}

.reply-input::placeholder {
  color: #bbb;
}

.reply-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-count-small {
  font-size: 11px;
  color: #999;
}

.reply-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 5px 16px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.reply-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  opacity: 0.9;
}

.reply-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .message-board {
    padding: 10px;
  }

  .main-content {
    gap: 10px;
  }

  .create-section,
  .message-card {
    padding: 12px;
  }

  .message-actions {
    flex-wrap: wrap;
  }
}
</style>
