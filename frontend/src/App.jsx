import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./contexts/AuthContext";
import Dashboard from "./pages/Dashboard";
import Disponibilidade from "./pages/Disponibilidade";
import Laboratorios from "./pages/Laboratorios";
import Login from "./pages/Login";
import MinhasReservas from "./pages/MinhasReservas";
import NovaReserva from "./pages/NovaReserva";
import ReservasAdmin from "./pages/ReservasAdmin";
import Solicitacoes from "./pages/Solicitacoes";
import Usuarios from "./pages/Usuarios";

function Pagina({ children }) {
  return <Layout>{children}</Layout>;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Pagina>
                  <Dashboard />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/laboratorios"
            element={
              <ProtectedRoute>
                <Pagina>
                  <Laboratorios />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/disponibilidade"
            element={
              <ProtectedRoute>
                <Pagina>
                  <Disponibilidade />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/reservas/nova"
            element={
              <ProtectedRoute papeis={["Professor"]}>
                <Pagina>
                  <NovaReserva />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/minhas-reservas"
            element={
              <ProtectedRoute papeis={["Professor"]}>
                <Pagina>
                  <MinhasReservas />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/solicitacoes"
            element={
              <ProtectedRoute papeis={["Administrador"]}>
                <Pagina>
                  <Solicitacoes />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/reservas"
            element={
              <ProtectedRoute papeis={["Administrador"]}>
                <Pagina>
                  <ReservasAdmin />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route
            path="/usuarios"
            element={
              <ProtectedRoute papeis={["Administrador"]}>
                <Pagina>
                  <Usuarios />
                </Pagina>
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
