import { useEffect, useState } from "react";
import StatusBadge from "../components/StatusBadge";
import { extrairErro, reservaService } from "../services/api";

export default function ReservasAdmin() {
  const [reservas, setReservas] = useState([]);
  const [statusFiltro, setStatusFiltro] = useState("");
  const [erro, setErro] = useState("");

  async function carregar(status) {
    try {
      const params = status ? { status } : {};
      const { data } = await reservaService.listar(params);
      setReservas(data);
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  useEffect(() => {
    carregar(statusFiltro);
  }, [statusFiltro]);

  async function cancelar(id) {
    if (!window.confirm("Cancelar esta reserva? O histórico será mantido.")) return;
    try {
      await reservaService.cancelar(id);
      await carregar(statusFiltro);
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  return (
    <section>
      <h2>Histórico de reservas</h2>
      <select value={statusFiltro} onChange={(e) => setStatusFiltro(e.target.value)}>
        <option value="">Todos os status</option>
        <option value="PENDENTE">Pendente</option>
        <option value="APROVADA">Aprovada</option>
        <option value="REJEITADA">Rejeitada</option>
        <option value="CANCELADA">Cancelada</option>
      </select>
      {erro && <p className="erro">{erro}</p>}
      {reservas.length === 0 && <p className="estado">Nenhuma reserva encontrada.</p>}
      <div className="tabela-wrap">
        <table>
          <thead>
            <tr>
              <th>Professor</th>
              <th>Laboratório</th>
              <th>Data</th>
              <th>Horário</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {reservas.map((reserva) => (
              <tr key={reserva.id}>
                <td>{reserva.professor_nome}</td>
                <td>{reserva.laboratorio_nome}</td>
                <td>{reserva.data}</td>
                <td>
                  {reserva.hora_inicio} — {reserva.hora_fim}
                </td>
                <td>
                  <StatusBadge status={reserva.status} />
                </td>
                <td>
                  {(reserva.status === "PENDENTE" || reserva.status === "APROVADA") && (
                    <button
                      type="button"
                      className="btn btn-ghost"
                      onClick={() => cancelar(reserva.id)}
                    >
                      Cancelar
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
