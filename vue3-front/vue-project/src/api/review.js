import request from './request'

export const reviewAPI = {
  // 审查单个文件
  reviewSingleFile(data) {
    return request({
      url: '/review/single',
      method: 'post',
      data
    })
  },
  
  // 审查多个文件
  reviewMultipleFiles(data) {
    return request({
      url: '/review/multiple',
      method: 'post',
      data
    })
  }
}
