import axios from "axios";

const backendAPI = import.meta.env.VITE_BACKEND_CONNECTION

const apiClient = axios.create({
    baseURL: backendAPI,
    withCredentials: true,
  });



export default apiClient;