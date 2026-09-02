import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import StatusBadge from "../components/StatusBadge";
import { authService, extrairErro } from "../services/api";

export default function Dashboard() {
  const { isAluno, isProfessor, isAdministrador } = useAuth();
  const [dados, setDados] = useState(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    authService
      .dashboard()
      .then((res) => setDados(res.data))
      .catch((error) => setErro(extrairErro(error)));
  }, []);

  if (erro) return <p className="erro">{erro}</p>;
  if (!dados) return <p className="estado">Carregando dashboard...</p>;

  return (
    <section>
      <h2>Dashboard — {dados.perfil}</h2>
      {isAdministrador && (
        <div className="cards">
          <article className="card stat">
            <span>Laboratórios</span>
            <strong>{dados.total_laboratorios}</strong>
          </article>
          <article className="card stat">
            <span>Ativos</span>
            <strong>{dados.laboratorios_ativos}</strong>
          </article>
          <article className="card stat">
            <span>Pendentes</span>
            <strong>{dados.solicitacoes_pendentes}</strong>
          </article>
          <article className="card stat">
            <span>Aprovadas</span>
            <strong>{dados.reservas_aprovadas}</strong>
          </article>
        </div>
      )}
      {isProfessor && (
        <>
          <div className="cards">
            <article className="card stat">
              <span>Total</span>
              <strong>{dados.total_reservas}</strong>
            </article>
            <article className="card stat">
              <span>Pendentes</span>
              <strong>{dados.reservas_pendentes}</strong>
            </article>
            <article className="card stat">
              <span>Aprovadas</span>
              <strong>{dados.reservas_aprovadas}</strong>
            </article>
          </div>
          <h3>Próximas reservas aprovadas</h3>
          {dados.proximas_reservas?.length ? (
            <div className="lista">
              {dados.proximas_reservas.map((reserva) => (
                <article className="card" key={reserva.id}>
                  <strong>{reserva.laboratorio_nome}</strong>
                  <p>
                    {reserva.data} · {reserva.hora_inicio} — {reserva.hora_fim}
                  </p>
                  <StatusBadge status={reserva.status} />
                </article>
              ))}
            </div>
          ) : (
            <p className="estado">Nenhuma reserva aprovada futura.</p>
          )}
        </>
      )}
      {isAluno && (
        <>
          <div className="cards">
            <article className="card stat">
              <span>Laboratórios ativos</span>
              <strong>{dados.laboratorios_ativos}</strong>
            </article>
          </div>
          <p>
            Consulte horários em{" "}
            <Link to="/disponibilidade">Disponibilidade</Link>.
          </p>
          <div className="cards">
            {dados.laboratorios?.map((lab) => (
              <article className="card" key={lab.id}>
                <strong>{lab.nome}</strong>
                <p>
                  Bloco {lab.bloco} · {lab.capacidade} lugares
                </p>
              </article>
            ))}
          </div>
        </>
      )}
    </section>
  );
}
