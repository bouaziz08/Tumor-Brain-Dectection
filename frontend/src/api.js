import axios from "axios";

const api= axios.create({
    baseURL: "URL_Backend"
})


export default api;
