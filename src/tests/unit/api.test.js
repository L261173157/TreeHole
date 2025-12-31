/**
 * API配置单元测试
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getApiUrl, API_CONFIG, MESSAGE_CONFIG } from '@/config/api.js'

// Mock import.meta.env
const mockEnv = {
  VITE_API_BASE_URL: 'http://test.example.com',
  VITE_API_TIMEOUT: '5000',
  VITE_MAX_LENGTH: '200',
  VITE_REFRESH_INTERVAL: '60000',
}

describe('API配置', () => {
  beforeEach(() => {
    // 重置环境变量
    globalThis.importMetaEnv = { ...mockEnv }
  })

  describe('getApiUrl', () => {
    it('应该正确拼接基础URL和端点', () => {
      const result = getApiUrl('/messages/')
      expect(result).toBe('http://test.example.com/messages/')
    })

    it('应该处理带参数的端点', () => {
      const result = getApiUrl('/messages/1')
      expect(result).toBe('http://test.example.com/messages/1')
    })

    it('应该处理根路径', () => {
      const result = getApiUrl('/')
      expect(result).toBe('http://test.example.com/')
    })
  })

  describe('API_CONFIG', () => {
    it('应该从环境变量读取BASE_URL', () => {
      expect(API_CONFIG.BASE_URL).toBe('http://test.example.com')
    })

    it('应该正确解析TIMEOUT为整数', () => {
      expect(API_CONFIG.TIMEOUT).toBe(5000)
    })

    it('应该有默认的RETRY_COUNT', () => {
      expect(API_CONFIG.RETRY_COUNT).toBe(3)
    })
  })

  describe('MESSAGE_CONFIG', () => {
    it('应该从环境变量读取MAX_LENGTH', () => {
      expect(MESSAGE_CONFIG.MAX_LENGTH).toBe(200)
    })

    it('应该有固定的MIN_LENGTH', () => {
      expect(MESSAGE_CONFIG.MIN_LENGTH).toBe(1)
    })

    it('应该从环境变量读取REFRESH_INTERVAL', () => {
      expect(MESSAGE_CONFIG.REFRESH_INTERVAL).toBe(60000)
    })

    it('REFRESH_INTERVAL应该是整数', () => {
      expect(Number.isInteger(MESSAGE_CONFIG.REFRESH_INTERVAL)).toBe(true)
    })
  })
})
