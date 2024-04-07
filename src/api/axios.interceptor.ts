import axios from 'axios';

const baseURL = process.env.VUE_APP_API_ENDPOINT; // Đọc đường dẫn URL từ biến môi trường .env

const axiosClient = axios.create({
  baseURL: baseURL,
  headers: {
    'content-type': 'application/json'
  }
});

axiosClient.interceptors.request.use(async (config) => {
  const authTokens = JSON.parse(localStorage.getItem('token') || ''); // Lấy token từ localStorage
  if (authTokens) {
    config.headers.Authorization = `Bearer ${authTokens}`; // Gắn Token vào Header nếu tồn tại
  }
  return config;
});

axiosClient.interceptors.response.use(
  (response) => {
    if (response && response.data) {
      return response.data; // Xử lý dữ liệu trả về nếu thành công
    }
    return response;
  },
  (error) => {
    throw error.response; // Xử lý lỗi từ API
  }
);

export default axiosClient;
