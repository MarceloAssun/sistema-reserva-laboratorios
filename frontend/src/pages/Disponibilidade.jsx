import { useEffect, useState } from "react";
import { extrairErro, laboratorioService } from "../services/api";

export default function Disponibilidade() {
  const [labs, setLabs] = useState([]);
  const [laboratorio, setLaboratorio] = useState("");
  const [data, setData] = useState("");
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  useEffect(() => {
    laboratorioService.listar().then((res) => setLabs(res.data.filter((l) => l.ativo)));
  }, []);

  async function consultar(event) {
    event.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      const { data: grade } = await laboratorioService.disponibilidade(
        laboratorio,
        data
      );
      setResultado(grade);
    } catch (error) {
      setErro(extrairErro(error));
      setResultado(null);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <section>
      <h2>Disponibilidade</h2>
      <p>A ocupação considera apenas reservas com status APROVADA.</p>
      <form className="card form inline" onSubmit={consultar}>
        <label>
          Laboratório
          <select
            value={laboratorio}
            onChange={(e) => setLaboratorio(e.target.value)}
            required
          >
            <option value="">Selecione</option>
            {labs.map((lab) => (
              <option key={lab.id} value={lab.id}>
                {lab.nome}
              </option>
            ))}
          </select>
        </label>
        <label>
          Data
          <input
            type="date"
            value={data}
            onChange={(e) => setData(e.target.value)}
            required
          />
        </label>
        <button className="btn" type="submit" disabled={carregando}>
          {carregando ? "Consultando..." : "Consultar"}
        </button>
      </form>
      {erro && <p className="erro">{erro}</p>}
      {resultado && (
        <div className="grade">
          {resultado.grade.map((slot) => (
            <div
              key={`${slot.hora_inicio}-${slot.hora_fim}`}
              className={slot.ocupado ? "slot ocupado" : "slot livre"}
            >
              <strong>
                {slot.hora_inicio} — {slot.hora_fim}
              </strong>
              <span>{slot.ocupado ? "Reservado" : "Disponível"}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
