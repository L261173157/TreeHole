/**
 * API配置文件
 *
 * 集中管理所有API相关的配置:
 * - API基础URL和超时设置
 * - 所有API端点路径
 * - 错误和成功消息
 * - 业务配置参数
 *
 * 注意:
 * - BASE_URL 当前为硬编码,生产环境应使用环境变量
 * - 这些异步函数未包含错误处理,错误处理由调用方完成
 */

// ==================== API基础配置 ====================

/**
 * API基础配置
 *
 * 包含后端服务器的基础URL和请求配置
 * 使用Vite环境变量系统,通过import.meta.env读取
 *
 * 环境变量定义在.env文件中:
 * - VITE_API_BASE_URL: API基础URL
 * - VITE_API_TIMEOUT: 请求超时时间
 * - VITE_MAX_LENGTH: 留言最大长度
 * - VITE_REFRESH_INTERVAL: 自动刷新间隔
 */
export const API_CONFIG = {
  // 后端API的基础URL
  // 从环境变量VITE_API_BASE_URL读取,如果未设置则使用默认值
  // 注意: Vite要求环境变量以VITE_开头才能在客户端代码中访问
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',

  // 请求超时时间(毫秒)
  // 超过此时间未响应的请求将被中止
  TIMEOUT: parseInt(import.meta.env.VITE_API_TIMEOUT || '10000'),

  // 失败重试次数
  // 网络错误或服务器错误时自动重试的次数
  RETRY_COUNT: 3,
}

// ==================== API端点定义 ====================

/**
 * API端点路径
 *
 * 定义所有API接口的相对路径
 * 部分端点接受参数并返回完整路径
 */
export const API_ENDPOINTS = {
  // 获取留言列表 / 创建新留言
  MESSAGES: '/messages/',

  // 获取单条留言详情(需要留言ID)
  MESSAGE_BY_ID: (id) => `/messages/${id}`,

  // 点赞留言(需要留言ID)
  LIKE_MESSAGE: (id) => `/messages/${id}/like`,

  // 点踩留言(需要留言ID)
  DISLIKE_MESSAGE: (id) => `/messages/${id}/dislike`,
}

// ==================== 工具函数 ====================

/**
 * 构建完整的API URL
 *
 * 将基础URL和端点路径拼接成完整的API URL
 *
 * @param {string} endpoint - API端点路径
 * @returns {string} 完整的API URL
 *
 * @example
 * getApiUrl('/messages/')  // 返回: 'http://127.0.0.1:8000/messages/'
 */
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`
}

// ==================== 消息定义 ====================

/**
 * 错误消息映射
 *
 * 定义各种错误类型对应的用户友好提示信息
 * 这些消息将显示给最终用户
 */
export const ERROR_MESSAGES = {
  // 网络连接失败(如无法连接到服务器)
  NETWORK_ERROR: '网络连接失败，请检查网络设置',

  // 请求超时
  TIMEOUT_ERROR: '请求超时，请稍后重试',

  // 服务器内部错误(500错误)
  SERVER_ERROR: '服务器错误，请稍后重试',

  // 输入数据验证失败(400错误)
  VALIDATION_ERROR: '输入数据格式错误',

  // 请求的资源不存在(404错误)
  NOT_FOUND: '请求的资源不存在',

  // 未知错误
  UNKNOWN_ERROR: '发生未知错误，请稍后重试'
}

/**
 * 成功消息
 *
 * 定义各种操作成功时的提示信息
 */
export const SUCCESS_MESSAGES = {
  MESSAGE_CREATED: '留言发布成功！',
  MESSAGE_LIKED: '点赞成功！',
  MESSAGE_DISLIKED: '踩成功！'
}

// ==================== 业务配置 ====================

/**
 * 留言相关配置
 *
 * 定义留言业务相关的参数限制
 * 与后端配置保持一致
 */
export const MESSAGE_CONFIG = {
  // 留言内容最大长度(字符数)
  // 从环境变量读取,应与后端的 MAX_CONTENT_LENGTH 保持一致
  MAX_LENGTH: parseInt(import.meta.env.VITE_MAX_LENGTH || '140'),

  // 留言内容最小长度(字符数)
  MIN_LENGTH: 1,

  // 自动刷新间隔(毫秒)
  // 前端每隔此时间自动获取最新留言列表
  // 可通过环境变量 VITE_REFRESH_INTERVAL 自定义
  REFRESH_INTERVAL: parseInt(import.meta.env.VITE_REFRESH_INTERVAL || '30000'),  // 默认30秒
}

// ==================== API方法(已废弃) ====================

/**
 * 注意: 以下函数目前未被使用
 *
 * MessageBoard.vue 组件直接使用 fetch API 调用接口
 * 这些函数保留用于未来可能的代码重构
 *
 * 如果要使用这些函数,需要:
 * 1. 添加错误处理逻辑
 * 2. 添加超时控制
 * 3. 添加请求取消功能
 */

/**
 * 获取留言列表
 * @deprecated 组件直接使用fetch API
 * @returns {Promise<Object>} 留言列表数据
 */
export async function fetchMessages() {
  const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES))
  return await res.json()
}

/**
 * 发布留言
 * @deprecated 组件直接使用fetch API
 * @param {Object} data - 留言数据 {content: string}
 * @returns {Promise<Object>} 创建的留言数据
 */
export async function postMessage(data) {
  const res = await fetch(getApiUrl(API_ENDPOINTS.MESSAGES), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return await res.json()
}

/**
 * 点赞留言
 * @deprecated 组件直接使用fetch API
 * @param {number} id - 留言ID
 * @returns {Promise<Object>} 更新后的留言数据
 */
export async function likeMessage(id) {
  const res = await fetch(getApiUrl(API_ENDPOINTS.LIKE_MESSAGE(id)), { method: 'POST' })
  return await res.json()
}

/**
 * 点踩留言
 * @deprecated 组件直接使用fetch API
 * @param {number} id - 留言ID
 * @returns {Promise<Object>} 更新后的留言数据
 */
export async function dislikeMessage(id) {
  const res = await fetch(getApiUrl(API_ENDPOINTS.DISLIKE_MESSAGE(id)), { method: 'POST' })
  return await res.json()
}
