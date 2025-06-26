/**
 * API配置文件
 * 包含所有API端点和配置
 */

// API基础配置
export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8000',
  TIMEOUT: 10000, // 请求超时时间（毫秒）
  RETRY_COUNT: 3, // 重试次数
}

// API端点
export const API_ENDPOINTS = {
  MESSAGES: '/messages/',
  MESSAGE_BY_ID: (id) => `/messages/${id}`,
  LIKE_MESSAGE: (id) => `/messages/${id}/like`,
  DISLIKE_MESSAGE: (id) => `/messages/${id}/dislike`,
}

// 完整的API URL
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`
}

// 错误消息映射
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  TIMEOUT_ERROR: '请求超时，请稍后重试',
  SERVER_ERROR: '服务器错误，请稍后重试',
  VALIDATION_ERROR: '输入数据格式错误',
  NOT_FOUND: '请求的资源不存在',
  UNKNOWN_ERROR: '发生未知错误，请稍后重试'
}

// 成功消息
export const SUCCESS_MESSAGES = {
  MESSAGE_CREATED: '留言发布成功！',
  MESSAGE_LIKED: '点赞成功！',
  MESSAGE_DISLIKED: '踩成功！'
}

// 留言相关配置
export const MESSAGE_CONFIG = {
  MAX_LENGTH: 140,
  MIN_LENGTH: 1,
  REFRESH_INTERVAL: 30000, // 自动刷新间隔（毫秒）
}

// ========== API 方法区 ========== //

// 获取留言列表
export async function fetchMessages() {
  const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES))
  return await res.json()
}

// 发布留言
export async function postMessage(data) {
  const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

// 点赞
export async function likeMessage(id) {
  const res = await fetch(getApiUrl(API_ENDPOINTS.LIKE_MESSAGE(id)), { method: 'POST' })
  return await res.json()
}

// 点踩
export async function dislikeMessage(id) {
  const res = await fetch(getApiUrl(API_ENDPOINTS.DISLIKE_MESSAGE(id)), { method: 'POST' })
  return await res.json()
}
