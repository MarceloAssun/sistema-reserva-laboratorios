import { useEffect, useState } from "react";
import StatusBadge from "../components/StatusBadge";
import { extrairErro, reservaService } from "../services/api";

export default function Solicitacoes() {
  const [reservas, setReservas] = useState([]);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  async function carregar() {
    setCarregando(true);
    try {
      const { data } = await reservaService.listar({ status: "PENDENTE" });
      setReservas(data);
    } catch (error) {
      setErro(extrairErro(error));
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregar();
  }, []);

  async function decidir(id, acao) {
    const texto =
      acao === "aprovar"
        ? "Aprovar esta solicitação?"
        : "Rejeitar esta solicitação?";
    if (!window.confirm(texto)) return;
    try {
      if (acao === "aprovar") await reservaService.aprovar(id);
      else await reservaService.rejeitar(id);
      await carregar();
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  return (
    <section>
      <h2>Solicitações pendentes</h2>
      {erro && <p className="erro">{erro}</p>}
      {carregando && <p className="estado">Carregando...</p>}
      {!carregando && reservas.length === 0 && (
        <p className="estado">Não há solicitações pendentes.</p>
      )}
      <div className="lista">
        {reservas.map((reserva) => (
          <article className="card" key={reserva.id}>
            <div className="card-head">
              <strong>{reserva.laboratorio_nome}</strong>
              <StatusBadge status={reserva.status} />
            </div>
            <p>Professor: {reserva.professor_nome}</p>
            <p>
              {reserva.data} · {reserva.hora_inicio} — {reserva.hora_fim}
            </p>
            <p>{reserva.observacao || "Sem observação"}</p>
            <div className="acoes">
              <button
                type="button"
                className="btn"
                onClick={() => decidir(reserva.id, "aprovar")}
              >
                Aprovar
              </button>
              <button
                type="button"
                className="btn btn-danger"
                onClick={() => decidir(reserva.id, "rejeitar")}
              >
                Rejeitar
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
