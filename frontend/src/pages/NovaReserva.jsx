import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { extrairErro, laboratorioService, reservaService } from "../services/api";

export default function NovaReserva() {
  const navigate = useNavigate();
  const [labs, setLabs] = useState([]);
  const [form, setForm] = useState({
    laboratorio: "",
    data: "",
    hora_inicio: "08:00",
    hora_fim: "10:00",
    observacao: "",
  });
  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    laboratorioService
      .listar()
      .then((res) => setLabs(res.data.filter((lab) => lab.ativo)));
  }, []);

  async function enviar(event) {
    event.preventDefault();
    setErro("");
    setEnviando(true);
    try {
      await reservaService.criar({
        ...form,
        laboratorio: Number(form.laboratorio),
        hora_inicio: `${form.hora_inicio}:00`,
        hora_fim: `${form.hora_fim}:00`,
      });
      navigate("/minhas-reservas");
    } catch (error) {
      setErro(extrairErro(error));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <section>
      <h2>Nova reserva</h2>
      <p>A solicitação nasce como PENDENTE e aguarda análise do administrador.</p>
      <form className="card form" onSubmit={enviar}>
        <label>
          Laboratório
          <select
            value={form.laboratorio}
            onChange={(e) => setForm({ ...form, laboratorio: e.target.value })}
            required
          >
            <option value="">Selecione</option>
            {labs.map((lab) => (
              <option key={lab.id} value={lab.id}>
                {lab.nome} — Bloco {lab.bloco}
              </option>
            ))}
          </select>
        </label>
        <label>
          Data
          <input
            type="date"
            value={form.data}
            onChange={(e) => setForm({ ...form, data: e.target.value })}
            required
          />
        </label>
        <label>
          Hora início
          <input
            type="time"
            value={form.hora_inicio}
            onChange={(e) => setForm({ ...form, hora_inicio: e.target.value })}
            required
          />
        </label>
        <label>
          Hora fim
          <input
            type="time"
            value={form.hora_fim}
            onChange={(e) => setForm({ ...form, hora_fim: e.target.value })}
            required
          />
        </label>
        <label>
          Observação (opcional)
          <textarea
            rows="3"
            value={form.observacao}
            onChange={(e) => setForm({ ...form, observacao: e.target.value })}
          />
        </label>
        {erro && <p className="erro">{erro}</p>}
        <button className="btn" type="submit" disabled={enviando}>
          {enviando ? "Enviando..." : "Solicitar reserva"}
        </button>
      </form>
    </section>
  );
}
