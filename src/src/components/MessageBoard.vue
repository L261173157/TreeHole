<!--
  TreeHole 留言板组件

  这是一个匿名留言板的主要界面组件,提供以下功能:
  - 发布新留言(最多140字符)
  - 查看留言列表(自动刷新)
  - 点赞/点踩留言

  技术栈:
  - Vue 3 Composition API
  - Element Plus UI组件库
  - Fetch API 进行数据请求

  特性:
  - 响应式设计
  - 自动刷新(30秒间隔)
  - 输入验证
  - 错误处理和用户提示
-->
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
/**
 * TreeHole 留言板组件逻辑
 *
 * 主要功能:
 * 1. 留言管理 - 创建、读取留言
 * 2. 交互功能 - 点赞、点踩
 * 3. 自动刷新 - 定时获取最新留言
 * 4. 输入验证 - 确保留言内容合法
 */

import { ref, onMounted, onUnmounted } from 'vue'
import { ChatDotRound, CaretTop, CaretBottom, Promotion } from '@element-plus/icons-vue'
import { API_ENDPOINTS, getApiUrl, SUCCESS_MESSAGES, MESSAGE_CONFIG } from '../config/api.js'
import {
  showErrorMessage,
  showSuccessMessage,
  retryApiCall,
  validateInput
} from '../utils/errorHandler.js'

// ==================== 响应式状态 ====================

// 新留言输入内容
const newMessage = ref('')

// 留言列表数据
const messages = ref([])

// 加载状态 - 用于防止重复请求
const isLoading = ref(false)

// 提交状态 - 用于防止重复提交
const isSubmitting = ref(false)

// 自动刷新定时器
let refreshTimer = null

// ==================== API调用函数 ====================

/**
 * 获取留言列表
 *
 * 从服务器获取最新的留言列表并更新界面
 * 使用isLoading状态防止并发请求
 */
const fetchMessages = async () => {
  try {
    isLoading.value = true

    // 发起GET请求获取留言列表
    const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES))

    // 检查HTTP响应状态
    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '获取留言失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }

    // 解析响应数据
    const response = await res.json()
    messages.value = response.data || []
    console.log(`成功获取 ${messages.value.length} 条留言`)
  } catch (error) {
    // 显示错误提示给用户
    showErrorMessage(error, '获取留言列表')
  } finally {
    isLoading.value = false
  }
}

/**
 * 提交新留言
 *
 * 验证用户输入并发送到服务器创建新留言
 * 成功后清空输入框并刷新留言列表
 */
const submitMessage = async () => {
  // 去除首尾空格
  const content = newMessage.value.trim()

  // 验证输入内容(长度、格式等)
  const validation = validateInput(content, MESSAGE_CONFIG.MAX_LENGTH, MESSAGE_CONFIG.MIN_LENGTH)
  if (!validation.isValid) {
    showErrorMessage(new Error(validation.message), '输入验证')
    return
  }

  try {
    isSubmitting.value = true

    // 发起POST请求创建留言
    const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })

    // 检查HTTP响应状态
    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '发布留言失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }

    // 显示成功提示
    showSuccessMessage(SUCCESS_MESSAGES.MESSAGE_CREATED)

    // 清空输入框
    newMessage.value = ''

    // 刷新留言列表以显示新留言
    await fetchMessages()
  } catch (error) {
    showErrorMessage(error, '发布留言')
  } finally {
    isSubmitting.value = false
  }
}

/**
 * 点赞留言
 *
 * 增加指定留言的点赞计数
 * 点赞成功后刷新列表以更新UI显示
 *
 * @param {number} id - 要点赞的留言ID
 */
const likeMessage = async (id) => {
  try {
    // 发起POST请求进行点赞
    const res = await fetch(getApiUrl(API_ENDPOINTS.LIKE_MESSAGE(id)), { method: 'POST' })

    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '点赞失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }

    showSuccessMessage(SUCCESS_MESSAGES.MESSAGE_LIKED)

    // 刷新列表以更新点赞数显示
    await fetchMessages()
  } catch (error) {
    showErrorMessage(error, '点赞操作')
  }
}

/**
 * 点踩留言
 *
 * 增加指定留言的点踩计数
 * 点踩成功后刷新列表以更新UI显示
 *
 * @param {number} id - 要点踩的留言ID
 */
const dislikeMessage = async (id) => {
  try {
    // 发起POST请求进行点踩
    const res = await fetch(getApiUrl(API_ENDPOINTS.DISLIKE_MESSAGE(id)), { method: 'POST' })

    if (!res.ok) {
      const errorData = await res.json()
      const error = new Error(errorData.detail || '踩失败')
      error.response = { status: res.status, data: errorData }
      throw error
    }

    showSuccessMessage(SUCCESS_MESSAGES.MESSAGE_DISLIKED)

    // 刷新列表以更新点踩数显示
    await fetchMessages()
  } catch (error) {
    showErrorMessage(error, '踩操作')
  }
}

// ==================== 工具函数 ====================

/**
 * 格式化时间显示
 *
 * 将ISO时间戳转换为本地化的中文时间格式
 * 格式示例: 2025/12/30 14:30
 *
 * @param {string} timestamp - ISO格式的时间戳
 * @returns {string} 格式化后的时间字符串,如果解析失败则返回错误提示
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

// ==================== 自动刷新管理 ====================

/**
 * 设置自动刷新定时器
 *
 * 每隔指定时间(默认30秒)自动刷新留言列表
 * 只在没有进行其他操作(加载/提交)时才执行刷新
 * 这样可以避免并发请求和重复操作
 */
const setupAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    // 检查是否正在加载或提交,避免并发请求
    if (!isLoading.value && !isSubmitting.value) {
      fetchMessages()
    }
  }, MESSAGE_CONFIG.REFRESH_INTERVAL)  // 使用配置文件中的刷新间隔
}

/**
 * 清除自动刷新定时器
 *
 * 组件卸载时必须清除定时器,防止内存泄漏
 */
const clearAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// ==================== 生命周期钩子 ====================

/**
 * 组件挂载时初始化
 *
 * 1. 首次获取留言列表
 * 2. 启动自动刷新定时器
 */
onMounted(() => {
  fetchMessages()
  setupAutoRefresh()
})

/**
 * 组件卸载时清理
 *
 * 清除定时器,防止内存泄漏
 */
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
