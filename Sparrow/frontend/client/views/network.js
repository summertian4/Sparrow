import axios from 'axios'
import * as notification from './notification.js'

// 超时
axios.defaults.timeout = 8000

// http response 拦截器
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 404:
          // TODO: 404 页面
          console.log('请求404')
          break
        case 500:
          // TODO: 500 页面
          console.log('请求500')
          break
      }
    }
    console.log(error)
    return Promise.reject(error)
  }
)

// 封装请求
export function request (url, options) {
  var opt = options || {}
  return new Promise((resolve, reject) => {
    axios({
      method: opt.method || 'get',
      url: url,
      params: opt.params || {},
      data: (opt.headers ? opt.data : opt.data) || {},
      responseType: opt.dataType || 'json',
      headers: opt.headers || {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    })
      .then(response => {
        if (response.data.code === 200) {
          resolve(response.data)
        } else {
          reject(response.data)
        }
      })
      .catch(error => {
        console.log(error)
        notification.toast({
          message: '网络访问错误',
          type: 'danger',
          duration: 2000
        })
      })
  })
}

export default {request}
