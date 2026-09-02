import { useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { extrairErro, laboratorioService } from "../services/api";

const vazio = { nome: "", capacidade: "", bloco: "", ativo: true };

export default function Laboratorios() {
  const { isAdministrador } = useAuth();
  const [labs, setLabs] = useState([]);
  const [busca, setBusca] = useState("");
  const [form, setForm] = useState(vazio);
  const [editando, setEditando] = useState(null);
  const [erro, setErro] = useState("");
  const [ok, setOk] = useState("");
  const [carregando, setCarregando] = useState(true);

  async function carregar() {
    setCarregando(true);
    try {
      const { data } = await laboratorioService.listar();
      setLabs(data);
    } catch (error) {
      setErro(extrairErro(error));
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregar();
  }, []);

  const filtrados = labs.filter((lab) =>
    `${lab.nome} ${lab.bloco}`.toLowerCase().includes(busca.toLowerCase())
  );

  async function salvar(event) {
    event.preventDefault();
    setErro("");
    setOk("");
    const payload = {
      ...form,
      capacidade: Number(form.capacidade),
    };
    try {
      if (editando) {
        await laboratorioService.atualizar(editando, payload);
        setOk("Laboratório atualizado.");
      } else {
        await laboratorioService.criar(payload);
        setOk("Laboratório cadastrado.");
      }
      setForm(vazio);
      setEditando(null);
      await carregar();
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  async function alternarAtivo(lab) {
    if (
      !window.confirm(
        lab.ativo
          ? `Desativar ${lab.nome}? Ele deixará de aceitar novas reservas.`
          : `Reativar ${lab.nome}?`
      )
    ) {
      return;
    }
    try {
      if (lab.ativo) await laboratorioService.desativar(lab.id);
      else await laboratorioService.ativar(lab.id);
      await carregar();
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  return (
    <section>
      <h2>Laboratórios</h2>
      <input
        className="busca"
        placeholder="Buscar por nome ou bloco"
        value={busca}
        onChange={(e) => setBusca(e.target.value)}
      />
      {carregando && <p className="estado">Carregando...</p>}
      {!carregando && filtrados.length === 0 && (
        <p className="estado">Nenhum laboratório encontrado.</p>
      )}
      <div className="cards">
        {filtrados.map((lab) => (
          <article className="card" key={lab.id}>
            <strong>{lab.nome}</strong>
            <p>Bloco {lab.bloco}</p>
            <p>Capacidade: {lab.capacidade}</p>
            <span className={lab.ativo ? "badge aprovada" : "badge cancelada"}>
              {lab.ativo ? "Ativo" : "Inativo"}
            </span>
            {isAdministrador && (
              <div className="acoes">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setEditando(lab.id);
                    setForm({
                      nome: lab.nome,
                      capacidade: lab.capacidade,
                      bloco: lab.bloco,
                      ativo: lab.ativo,
                    });
                  }}
                >
                  Editar
                </button>
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => alternarAtivo(lab)}
                >
                  {lab.ativo ? "Desativar" : "Ativar"}
                </button>
              </div>
            )}
          </article>
        ))}
      </div>
      {isAdministrador && (
        <form className="card form" onSubmit={salvar}>
          <h3>{editando ? "Editar laboratório" : "Cadastrar laboratório"}</h3>
          <label>
            Nome
            <input
              value={form.nome}
              onChange={(e) => setForm({ ...form, nome: e.target.value })}
              required
            />
          </label>
          <label>
            Bloco
            <input
              value={form.bloco}
              onChange={(e) => setForm({ ...form, bloco: e.target.value })}
              required
            />
          </label>
          <label>
            Capacidade
            <input
              type="number"
              min="1"
              value={form.capacidade}
              onChange={(e) => setForm({ ...form, capacidade: e.target.value })}
              required
            />
          </label>
          {erro && <p className="erro">{erro}</p>}
          {ok && <p className="ok">{ok}</p>}
          <div className="acoes">
            <button className="btn" type="submit">
              Salvar
            </button>
            {editando && (
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => {
                  setEditando(null);
                  setForm(vazio);
                }}
              >
                Cancelar edição
              </button>
            )}
          </div>
        </form>
      )}
    </section>
  );
}
