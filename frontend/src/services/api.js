import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem("refresh");
      if (!refresh) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        return Promise.reject(error);
      }
      try {
        const { data } = await axios.post(
          `${api.defaults.baseURL}/refresh/`,
          { refresh }
        );
        localStorage.setItem("access", data.access);
        if (data.refresh) {
          localStorage.setItem("refresh", data.refresh);
        }
        original.headers.Authorization = `Bearer ${data.access}`;
        return api(original);
      } catch (refreshError) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export function extrairErro(error, fallback = "Não foi possível concluir a operação.") {
  const data = error.response?.data;
  if (!data) return fallback;
  if (typeof data === "string") return data;
  if (data.detail) {
    return Array.isArray(data.detail) ? data.detail.join(" ") : String(data.detail);
  }
  const partes = Object.entries(data).map(([campo, valor]) => {
    const texto = Array.isArray(valor) ? valor.join(" ") : String(valor);
    return `${campo}: ${texto}`;
  });
  return partes.join(" ") || fallback;
}

export const authService = {
  login: (username, password) => api.post("/login/", { username, password }),
  logout: (refresh) => api.post("/logout/", { refresh }),
  me: () => api.get("/me/"),
  dashboard: () => api.get("/dashboard/"),
};

export const laboratorioService = {
  listar: () => api.get("/laboratorios/"),
  obter: (id) => api.get(`/laboratorios/${id}/`),
  criar: (dados) => api.post("/laboratorios/", dados),
  atualizar: (id, dados) => api.patch(`/laboratorios/${id}/`, dados),
  disponibilidade: (id, data) =>
    api.get(`/laboratorios/${id}/disponibilidade/`, { params: { data } }),
  ativar: (id) => api.post(`/laboratorios/${id}/ativar/`),
  desativar: (id) => api.post(`/laboratorios/${id}/desativar/`),
};

export const reservaService = {
  listar: (params) => api.get("/reservas/", { params }),
  obter: (id) => api.get(`/reservas/${id}/`),
  criar: (dados) => api.post("/reservas/", dados),
  aprovar: (id) => api.post(`/reservas/${id}/aprovar/`),
  rejeitar: (id) => api.post(`/reservas/${id}/rejeitar/`),
  cancelar: (id) => api.post(`/reservas/${id}/cancelar/`),
};

export const usuarioService = {
  listar: () => api.get("/usuarios/"),
  atribuirGrupo: (id, grupo) => api.post(`/usuarios/${id}/atribuir-grupo/`, { grupo }),
};

export default api;
