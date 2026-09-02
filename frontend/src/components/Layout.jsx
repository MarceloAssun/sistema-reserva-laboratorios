import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Layout({ children }) {
  const { usuario, logout, isAluno, isProfessor, isAdministrador } = useAuth();
  const navigate = useNavigate();

  async function sair() {
    await logout();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <strong>Reserva de Labs</strong>
          <span>Ambiente acadêmico</span>
        </div>
        <nav>
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/laboratorios">Laboratórios</NavLink>
          <NavLink to="/disponibilidade">Disponibilidade</NavLink>
          {isProfessor && <NavLink to="/reservas/nova">Nova reserva</NavLink>}
          {isProfessor && <NavLink to="/minhas-reservas">Minhas reservas</NavLink>}
          {isAdministrador && <NavLink to="/solicitacoes">Solicitações</NavLink>}
          {isAdministrador && <NavLink to="/reservas">Reservas</NavLink>}
          {isAdministrador && <NavLink to="/usuarios">Usuários</NavLink>}
        </nav>
        <div className="sidebar-user">
          <p>{usuario?.first_name || usuario?.username}</p>
          <small>{usuario?.perfil}</small>
          <button type="button" className="btn btn-ghost" onClick={sair}>
            Sair
          </button>
        </div>
      </aside>
      <main className="content">
        <header className="topbar">
          <h1>Sistema de Reserva de Laboratórios</h1>
          {!isAluno && !isProfessor && !isAdministrador && (
            <span className="aviso">Perfil não atribuído</span>
          )}
        </header>
        {children}
      </main>
    </div>
  );
}
