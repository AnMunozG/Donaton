import { useState, useEffect } from "react";
import { Navigate, Link } from "react-router-dom";
import { useAuth } from "../componentes/AuthContext";
import api from "../servicios/api.js";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";

const CHART_COLORS = ["#DD4444", "#F48080", "#3AB795", "#194B4F", "#FFC107", "#0dcaf0"];

export default function Impacto() {
  const { user, isAuth } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuth) return;
    api.get("/auth/impacto").then(setData).catch(() => {}).finally(() => setLoading(false));
  }, [isAuth]);

  if (!isAuth) return <Navigate to="/login" replace />;

  if (loading) return (
    <div className="content-surface text-center py-5">
      <div className="spinner-border c-primary" role="status"></div>
      <p className="c-muted mt-2">Cargando tu impacto...</p>
    </div>
  );

  if (!data) return (
    <div className="content-surface text-center py-5">
      <p className="c-muted">No se pudo cargar la informaci&oacute;n de impacto.</p>
    </div>
  );

  const porTipoData = Object.entries(data.por_tipo || {}).map(([name, value]) => ({ name: name || "Sin tipo", value }));

  const totalKg = data.total_kg ?? 0;
  const totalMonetario = data.total_monetario ?? 0;

  const rechartsTooltip = { background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text)", fontSize: 12 };

  return (
    <div className="perfil">
      <div className="content-surface">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
          <div>
            <h1 className="fw-bold mb-1">Mi Impacto</h1>
            <p className="m-0 c-muted">
              <i className="bi bi-person-fill me-1 c-accent"></i>{user.nombre || user.rut}
            </p>
          </div>
          <Link to="/perfil" className="btn btn-outline-accent btn-sm">
            <i className="bi bi-arrow-left me-1"></i>Volver al perfil
          </Link>
        </div>

        {/* Stats cards */}
        <div className="row g-3 mb-4">
          {[
            { icon: "bi-gift-fill", label: "Donaciones", value: data.total_donaciones, color: "#DD4444" },
            { icon: "bi-box-seam-fill", label: "Kg donados", value: `${totalKg.toFixed(0)} kg`, color: "#3AB795" },
            { icon: "bi-cash-coin", label: "Donado en dinero", value: `$${totalMonetario.toLocaleString()}`, color: "#FFC107" },
            { icon: "bi-building-fill", label: "Centros ayudados", value: data.centros_distintos, color: "#0dcaf0" },
          ].map((card, i) => (
            <div key={i} className="col-sm-6 col-xl-3">
              <div className="p-4 rounded-4 card-surface card-accent-left" style={{ '--accent-color': card.color }}>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <div className="small c-muted">{card.label}</div>
                    <div className="fw-bold fs-4">{card.value}</div>
                  </div>
                  <div className="color-dynamic" style={{ '--dynamic-color': card.color, fontSize: "1.5rem" }}>
                    <i className={`bi ${card.icon}`}></i>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="row g-4">
          {/* Gráfico de donaciones por tipo */}
          <div className="col-lg-6">
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-pie-chart-fill me-2 c-primary"></i>Donaciones por tipo
              </h2>
              {porTipoData.length === 0 ? (
                <p className="c-muted small mb-0">Sin datos</p>
              ) : (
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie data={porTipoData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} innerRadius={40} label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}>
                      {porTipoData.map((_, idx) => (
                        <Cell key={idx} fill={CHART_COLORS[idx % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={rechartsTooltip} />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          {/* Timeline */}
          <div className="col-lg-6">
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-bar-chart-fill me-2 c-primary"></i>Donaciones por mes
              </h2>
              {(data.por_mes || []).length === 0 ? (
                <p className="c-muted small mb-0">Sin datos</p>
              ) : (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={data.por_mes || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis dataKey="mes" tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                    <YAxis tick={{ fill: "var(--text-muted)", fontSize: 11 }} />
                    <Tooltip contentStyle={rechartsTooltip} />
                    <Bar dataKey="cantidad" fill="#DD4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          {/* Centros impactados */}
          <div className="col-lg-6">
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-building-fill me-2 c-primary"></i>Centros donde has donado
              </h2>
              {(data.centros || []).length === 0 ? (
                <p className="c-muted small mb-0">A&uacute;n no has donado a ning&uacute;n centro.</p>
              ) : (
                <div className="d-flex flex-column gap-2 scroll-panel">
                  {(data.centros || []).map((c, i) => (
                    <div key={c.id} className="d-flex justify-content-between align-items-center p-2 rounded-3 bg-page">
                      <div className="d-flex align-items-center gap-2">
                        <span className="badge bg-primary rounded-pill">{i + 1}</span>
                        <div>
                          <div className="small fw-semibold">{c.nombre || `Centro #${c.id}`}</div>
                          <div className="smaller c-muted">{c.region || ""}</div>
                        </div>
                      </div>
                      <div className="text-end">
                        <div className="small fw-semibold">{c.total_donaciones}</div>
                        <div className="smaller c-muted">donaciones</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Última donación */}
          <div className="col-lg-6">
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-clock-history me-2 c-primary"></i>&Uacute;ltima actividad
              </h2>
              <div className="text-center py-4">
                {data.ultima_donacion ? (
                  <>
                    <div className="fw-bold fs-3 c-accent">{data.ultima_donacion}</div>
                    <div className="small c-muted">Fecha de tu &uacute;ltima donaci&oacute;n</div>
                  </>
                ) : (
                  <p className="c-muted small mb-0">A&uacute;n no has realizado donaciones.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
