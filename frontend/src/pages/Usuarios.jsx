import { useEffect, useState } from "react";
import { extrairErro, usuarioService } from "../services/api";

const GRUPOS = ["Alunos", "Professores", "Administradores"];

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [erro, setErro] = useState("");
  const [ok, setOk] = useState("");

  async function carregar() {
    const { data } = await usuarioService.listar();
    setUsuarios(data);
  }

  useEffect(() => {
    carregar().catch((error) => setErro(extrairErro(error)));
  }, []);

  async function atribuir(id, grupo) {
    setErro("");
    setOk("");
    try {
      await usuarioService.atribuirGrupo(id, grupo);
      setOk("Perfil atualizado.");
      await carregar();
    } catch (error) {
      setErro(extrairErro(error));
    }
  }

  return (
    <section>
      <h2>Usuários</h2>
      <p>Os perfis são controlados pelos grupos do Django.</p>
      {erro && <p className="erro">{erro}</p>}
      {ok && <p className="ok">{ok}</p>}
      <div className="tabela-wrap">
        <table>
          <thead>
            <tr>
              <th>Usuário</th>
              <th>Nome</th>
              <th>Perfil</th>
              <th>Atribuir grupo</th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map((user) => (
              <tr key={user.id}>
                <td>{user.username}</td>
                <td>
                  {user.first_name} {user.last_name}
                </td>
                <td>{user.perfil}</td>
                <td>
                  <select
                    defaultValue=""
                    onChange={(e) => {
                      if (e.target.value) atribuir(user.id, e.target.value);
                      e.target.value = "";
                    }}
                  >
                    <option value="">Selecionar</option>
                    {GRUPOS.map((grupo) => (
                      <option key={grupo} value={grupo}>
                        {grupo}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
