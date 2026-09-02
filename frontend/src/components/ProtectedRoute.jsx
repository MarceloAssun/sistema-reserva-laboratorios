import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function ProtectedRoute({ children, papeis }) {
  const { usuario, carregando } = useAuth();

  if (carregando) {
    return <div className="estado">Carregando sessão...</div>;
  }

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  if (papeis && !papeis.includes(usuario.perfil)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
