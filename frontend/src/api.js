import axios from "axios";

const apiClient = axios.create({
    baseURL: "http://127.0.0.1:5000/", 
    timeout: 5000, 
    headers: {'Authorization':'Bearer <token>'},
})

export default apiClient