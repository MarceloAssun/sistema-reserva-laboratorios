export default function StatusBadge({ status }) {
  const mapa = {
    PENDENTE: "badge pendente",
    APROVADA: "badge aprovada",
    REJEITADA: "badge rejeitada",
    CANCELADA: "badge cancelada",
  };
  return <span className={mapa[status] || "badge"}>{status}</span>;
}
