import axios from "axios";

function useApi() {
  const baseURL = "http://localhost:8000/api";

  const instance = axios.create({ baseURL });

  return instance;
}

export default useApi;
