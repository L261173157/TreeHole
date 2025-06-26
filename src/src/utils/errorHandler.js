/**
 * 错误处理工具
 * 统一处理API请求错误和用户提示
 */

import { ElMessage } from 'element-plus'
import { ERROR_MESSAGES } from '../config/api.js'

/**
 * 处理API错误
 * @param {Error} error - 错误对象
 * @param {string} context - 错误上下文
 * @returns {string} 错误消息
 */
export function handleApiError(error, context = '') {
  console.error(`API错误 ${context}:`, error)
  
  let errorMessage = ERROR_MESSAGES.UNKNOWN_ERROR
  
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    errorMessage = ERROR_MESSAGES.NETWORK_ERROR
  } else if (error.name === 'AbortError') {
    errorMessage = ERROR_MESSAGES.TIMEOUT_ERROR
  } else if (error.response) {
    // HTTP错误响应
    const status = error.response.status
    
    switch (status) {
      case 400:
        errorMessage = error.response.data?.detail || ERROR_MESSAGES.VALIDATION_ERROR
        break
      case 404:
        errorMessage = ERROR_MESSAGES.NOT_FOUND
        break
      case 500:
        errorMessage = ERROR_MESSAGES.SERVER_ERROR
        break
      default:
        errorMessage = error.response.data?.detail || ERROR_MESSAGES.UNKNOWN_ERROR
    }
  } else if (error.message) {
    errorMessage = error.message
  }
  
  return errorMessage
}

/**
 * 显示错误提示
 * @param {Error} error - 错误对象
 * @param {string} context - 错误上下文
 */
export function showErrorMessage(error, context = '') {
  const errorMessage = handleApiError(error, context)
  ElMessage.error(errorMessage)
}

/**
 * 显示成功提示
 * @param {string} message - 成功消息
 */
export function showSuccessMessage(message) {
  ElMessage.success(message)
}

/**
 * 显示警告提示
 * @param {string} message - 警告消息
 */
export function showWarningMessage(message) {
  ElMessage.warning(message)
}

/**
 * 带重试功能的API请求
 * @param {Function} apiCall - API调用函数
 * @param {number} maxRetries - 最大重试次数
 * @param {number} delay - 重试延迟（毫秒）
 * @returns {Promise} API响应
 */
export async function retryApiCall(apiCall, maxRetries = 3, delay = 1000) {
  let lastError
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await apiCall()
    } catch (error) {
      lastError = error
      
      if (i === maxRetries) {
        throw error
      }
      
      // 如果是网络错误或服务器错误，则重试
      if (error.name === 'TypeError' || 
          (error.response && error.response.status >= 500)) {
        console.log(`API调用失败，${delay}ms后进行第${i + 1}次重试...`)
        await new Promise(resolve => setTimeout(resolve, delay))
        delay *= 2 // 指数退避
      } else {
        // 客户端错误不重试
        throw error
      }
    }
  }
  
  throw lastError
}

/**
 * 验证输入内容
 * @param {string} content - 输入内容
 * @param {number} maxLength - 最大长度
 * @param {number} minLength - 最小长度
 * @returns {Object} 验证结果
 */
export function validateInput(content, maxLength = 140, minLength = 1) {
  const trimmedContent = content.trim()
  
  if (trimmedContent.length < minLength) {
    return {
      isValid: false,
      message: `内容不能少于${minLength}个字符`
    }
  }
  
  if (trimmedContent.length > maxLength) {
    return {
      isValid: false,
      message: `内容不能超过${maxLength}个字符`
    }
  }
  
  return {
    isValid: true,
    message: ''
  }
}
