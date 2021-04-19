import axios from 'axios';

export default () => {
  const options = {};
  options.baseURL = process.env.VUE_APP_API_BASE_URL;
  const instance = axios.create(options);
  return instance;
};