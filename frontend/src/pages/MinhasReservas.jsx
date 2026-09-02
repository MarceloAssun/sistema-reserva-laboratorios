import { useEffect, useState } from "react";
import StatusBadge from "../components/StatusBadge";
import { extrairErro, reservaService } from "../services/api";

export default function MinhasReservas() {
  const [reservas, setReservas] = useState([]);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  async function carregar() {
    setCarregando(true);
    try {
      const { data } = await reservaService.listar();
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

  async function cancelar(id) {
    if (!window.confirm("Cancelar esta reserva?")) return;
    try {
      await reservaService.cancelar(id);
      await carregar();
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  return (
    <section>
      <h2>Minhas reservas</h2>
      {erro && <p className="erro">{erro}</p>}
      {carregando && <p className="estado">Carregando...</p>}
      {!carregando && reservas.length === 0 && (
        <p className="estado">Você ainda não possui solicitações.</p>
      )}
      <div className="lista">
        {reservas.map((reserva) => (
          <article className="card" key={reserva.id}>
            <div className="card-head">
              <strong>{reserva.laboratorio_nome}</strong>
              <StatusBadge status={reserva.status} />
            </div>
            <p>
              {reserva.data} · {reserva.hora_inicio} — {reserva.hora_fim}
            </p>
            {reserva.observacao && <p>{reserva.observacao}</p>}
            {(reserva.status === "PENDENTE" || reserva.status === "APROVADA") && (
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => cancelar(reserva.id)}
              >
                Cancelar
              </button>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
