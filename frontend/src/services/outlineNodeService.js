// src/services/outlineNodeService.js
import apiClient from './api'

export default {
  /**
   * 获取指定项目的所有大纲节点
   * @param {number} projectId 项目ID
   */
  getOutlineForProject(projectId) {
    return apiClient.get(`/outline-nodes/project/${projectId}`)
  },

  /**
   * 创建一个新的大纲节点
   * @param {object} nodeData 包含 title, project_id, parent_id
   */
  createNode(nodeData) {
    return apiClient.post('/outline-nodes/', nodeData)
  },

  /**
   * 更新一个大纲节点
   * @param {number} nodeId 节点ID
   * @param {object} updateData 包含要更新字段的对象
   */
  updateNode(nodeId, updateData) {
    return apiClient.put(`/outline-nodes/${nodeId}`, updateData)
  },

  /**
   * 删除一个大纲节点
   * @param {number} nodeId 节点ID
   */
  deleteNode(nodeId) {
    return apiClient.delete(`/outline-nodes/${nodeId}`)
  },
}
