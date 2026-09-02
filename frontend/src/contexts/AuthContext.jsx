import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { authService } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [carregando, setCarregando] = useState(true);

  async function carregarUsuario() {
    const token = localStorage.getItem("access");
    if (!token) {
      setUsuario(null);
      setCarregando(false);
      return;
    }
    try {
      const { data } = await authService.me();
      setUsuario(data);
    } catch {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      setUsuario(null);
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregarUsuario();
  }, []);

  async function login(username, password) {
    const { data } = await authService.login(username, password);
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    const me = await authService.me();
    setUsuario(me.data);
    return me.data;
  }

  async function logout() {
    const refresh = localStorage.getItem("refresh");
    try {
      if (refresh) {
        await authService.logout(refresh);
      }
    } catch {
      /* sessão local é encerrada mesmo se o token já estiver inválido */
    }
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUsuario(null);
  }

  const perfil = usuario?.perfil || "";
  const value = useMemo(
    () => ({
      usuario,
      carregando,
      login,
      logout,
      isAluno: perfil === "Aluno",
      isProfessor: perfil === "Professor",
      isAdministrador: perfil === "Administrador",
    }),
    [usuario, carregando, perfil]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider");
  }
  return ctx;
}
