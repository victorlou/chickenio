import axios from 'axios';

export default () => {
  const options = {};
  options.baseURL = process.env.VUE_APP_API_BASE_URL;
  const http = axios.create(options);

  http.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  }, (err) => {
    return Promise.reject(err)
  })

  http.interceptors.response.use((response) => {
    return response
  }, (error) => {
    if (error.response.status === 401) {
      window.location = '/login'
    }

    return Promise.reject(error)
  })
  return http;
};