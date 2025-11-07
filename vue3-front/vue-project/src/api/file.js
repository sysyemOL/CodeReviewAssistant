import request from './request'

export const fileAPI = {
  // 上传文件
  uploadFile(formData, onProgress) {
    return request({
      url: '/files/upload',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      }
    })
  },
  
  // 获取文件内容
  getFile(fileId) {
    return request({
      url: `/files/${fileId}`,
      method: 'get'
    })
  },
  
  // 解析代码结构
  parseCode(data) {
    return request({
      url: '/files/parse',
      method: 'post',
      data
    })
  }
}

