/**
 * 工具函数单元测试
 */

import { describe, it, expect } from 'vitest'
import { validateInput } from '@/utils/errorHandler.js'

describe('validateInput', () => {
  it('应该验证有效的输入', () => {
    const result = validateInput('Hello, World!', 140, 1)
    expect(result.isValid).toBe(true)
    expect(result.message).toBe('')
  })

  it('应该拒绝空字符串', () => {
    const result = validateInput('   ', 140, 1)
    expect(result.isValid).toBe(false)
    expect(result.message).toContain('不能少于')
  })

  it('应该拒绝过短的内容', () => {
    const result = validateInput('Hi', 140, 5)
    expect(result.isValid).toBe(false)
    expect(result.message).toContain('不能少于5个字符')
  })

  it('应该拒绝过长的内容', () => {
    const longContent = 'a'.repeat(141)
    const result = validateInput(longContent, 140, 1)
    expect(result.isValid).toBe(false)
    expect(result.message).toContain('不能超过140个字符')
  })

  it('应该接受正好最大长度的内容', () => {
    const exactContent = 'a'.repeat(140)
    const result = validateInput(exactContent, 140, 1)
    expect(result.isValid).toBe(true)
  })

  it('应该接受正好最小长度的内容', () => {
    const result = validateInput('a', 140, 1)
    expect(result.isValid).toBe(true)
  })

  it('应该trim空白字符', () => {
    const result = validateInput('  test  ', 140, 1)
    expect(result.isValid).toBe(true)
  })
})
