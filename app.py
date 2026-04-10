import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pegada de Carbono · Dashboard",
    page_icon="🌿",
    layout="wide",
)

# ── Helpers ────────────────────────────────────────────────────────────────────
ESTADOS = [
    "AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT",
    "PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO",
]
SETORES        = ["industrial", "comercial", "residencial", "rural", "outros"]
FONTES         = ["hidrelétrica", "eólica", "solar", "nuclear", "térmica"]
MESES_LABEL    = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
                  7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

def get_season(m: int) -> str:
    if m in [12, 1, 2]:  return "Verao"
    if m in [3,  4, 5]:  return "Outono"
    if m in [6,  7, 8]:  return "Inverno"
    return "Primavera"

def liquid_fuel_emissions(energy_kwh: float) -> dict:
    fuels = {
        "etanol":    {"efficiency": 0.27, "emission_factor": 0.20},
        "gasolina":  {"efficiency": 0.30, "emission_factor": 0.64},
        "diesel":    {"efficiency": 0.38, "emission_factor": 0.73},
    }
    return {
        fuel: round(energy_kwh / d["efficiency"] * d["emission_factor"], 2)
        for fuel, d in fuels.items()
    }

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    # Tenta caminhos relativos comuns
    candidates = [
        os.path.join("models", "best_carbon_footprint_model.joblib"),
        os.path.join("..", "models", "best_carbon_footprint_model.joblib"),
        "best_carbon_footprint_model.joblib",
    ]
    for p in candidates:
        if os.path.exists(p):
            return joblib.load(p), None
    return None, "Modelo não encontrado. Coloque `best_carbon_footprint_model.joblib` na pasta `models/`."

model, model_error = load_model()

def predict_sources(energy_kwh, month, state, usage_type):
    season = get_season(month)
    results = {}
    for src in FONTES:
        df_in = pd.DataFrame([{
            "consumo_kwh": energy_kwh, "mes": month,
            "estado": state, "setor": usage_type,
            "fonte_energia": src, "season": season,
        }])
        results[src] = round(float(model.predict(df_in)[0]), 2)
    return results

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/leaf.png", width=60)
    st.title("Parâmetros")
    st.markdown("---")

    consumo  = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                value=5_000.0, step=100.0)
    estado   = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"))
    setor    = st.selectbox("Setor", SETORES)
    fonte    = st.selectbox("Fonte de energia atual", FONTES)
    mes      = st.slider("Mês", 1, 12, 6,
                         format="%d", help="Mês da medição")
    st.caption(f"Estação: **{get_season(mes)}** · Mês: **{MESES_LABEL[mes]}**")

    st.markdown("---")
    run = st.button("🔍 Calcular", use_container_width=True, type="primary")

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🌿 Dashboard · Pegada de Carbono")
st.caption("Estimativa de emissões de CO₂ com base em consumo energético e contexto geográfico.")

if model_error:
    st.error(f"⚠️ {model_error}")
    st.stop()

# ── Auto-run on first load ──────────────────────────────────────────────────────
if "results" not in st.session_state or run:
    elec   = predict_sources(consumo, mes, estado, setor)
    fuels  = liquid_fuel_emissions(consumo)
    season = get_season(mes)

    # Emissão da fonte selecionada
    co2_sel = elec[fonte]

    # Ranking completo
    combined = {**elec, **fuels}
    ranking  = dict(sorted(combined.items(), key=lambda x: x[1]))
    hydro_base = elec["hidrelétrica"]
    ranking_pct = {
        src: {"co2": v, "vs_hydro_%": round((v - hydro_base) / hydro_base * 100, 1)}
        for src, v in ranking.items()
    }

    st.session_state["results"] = {
        "co2_sel": co2_sel, "elec": elec, "fuels": fuels,
        "combined": combined, "ranking": ranking_pct,
        "consumo": consumo, "fonte": fonte,
        "estado": estado, "setor": setor, "mes": mes, "season": season,
    }

r = st.session_state["results"]

# ── KPI cards ──────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

best_src  = min(r["elec"], key=r["elec"].get)
best_co2  = r["elec"][best_src]
saving    = round(r["co2_sel"] - best_co2, 2)
saving_pct = round(saving / r["co2_sel"] * 100, 1) if r["co2_sel"] > 0 else 0

col1.metric("Emissão atual", f"{r['co2_sel']:,.1f} kg CO₂",
            help=f"Fonte: {r['fonte']}")
col2.metric("Menor emissão elétrica", f"{best_co2:,.1f} kg CO₂",
            delta=f"-{saving_pct}% vs atual" if saving > 0 else "✅ Já é a melhor",
            delta_color="inverse",
            help=f"Fonte: {best_src}")
col3.metric("Consumo informado", f"{r['consumo']:,.0f} kWh")
col4.metric("Estação / Mês",
            f"{r['season']} · {MESES_LABEL[r['mes']]}")

st.markdown("---")

# ── Charts row 1 ───────────────────────────────────────────────────────────────
c1, c2 = st.columns([1.3, 1])

with c1:
    st.subheader("📊 Emissões por fonte de energia")
    df_bar = pd.DataFrame([
        {"Fonte": src, "CO₂ (kg)": v, "Tipo": "Elétrica" if src in r["elec"] else "Combustível"}
        for src, v in sorted(r["combined"].items(), key=lambda x: x[1])
    ])
    color_map = {
        "hidrelétrica": "#2196F3", "eólica": "#4CAF50", "solar": "#FFC107",
        "nuclear": "#9C27B0", "térmica": "#F44336",
        "etanol": "#FF9800", "gasolina": "#795548", "diesel": "#607D8B",
    }
    fig_bar = px.bar(
        df_bar, x="CO₂ (kg)", y="Fonte", orientation="h",
        color="Fonte", color_discrete_map=color_map,
        text="CO₂ (kg)", template="plotly_white",
    )
    fig_bar.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_bar.update_layout(
        showlegend=False, height=380,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=0, r=60, t=10, b=10),
    )
    # Destaca fonte selecionada
    for trace in fig_bar.data:
        if trace.name == r["fonte"]:
            trace.marker.line = dict(color="black", width=2)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("🥧 Participação relativa")
    df_pie = pd.DataFrame([
        {"Fonte": src, "CO₂ (kg)": v}
        for src, v in r["combined"].items()
    ])
    fig_pie = px.pie(
        df_pie, values="CO₂ (kg)", names="Fonte",
        color="Fonte", color_discrete_map=color_map,
        hole=0.45, template="plotly_white",
    )
    fig_pie.update_traces(textposition="outside", textinfo="label+percent")
    fig_pie.update_layout(
        showlegend=False, height=380,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Charts row 2 ───────────────────────────────────────────────────────────────
c3, c4 = st.columns([1, 1])

with c3:
    st.subheader("📅 Variação mensal da emissão")
    meses_vals = []
    for m in range(1, 13):
        season = get_season(m)
        df_in = pd.DataFrame([{
            "consumo_kwh": r["consumo"], "mes": m,
            "estado": r["estado"], "setor": r["setor"],
            "fonte_energia": r["fonte"], "season": season,
        }])
        meses_vals.append({"Mês": MESES_LABEL[m], "CO₂ (kg)": round(float(model.predict(df_in)[0]), 2)})

    df_line = pd.DataFrame(meses_vals)
    fig_line = px.line(
        df_line, x="Mês", y="CO₂ (kg)", markers=True,
        template="plotly_white", color_discrete_sequence=["#2196F3"],
    )
    # Marca o mês selecionado
    sel_val = df_line[df_line["Mês"] == MESES_LABEL[r["mes"]]]["CO₂ (kg)"].values[0]
    fig_line.add_scatter(
        x=[MESES_LABEL[r["mes"]]], y=[sel_val],
        mode="markers", marker=dict(size=12, color="red"),
        name="Mês selecionado",
    )
    fig_line.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=10))
    st.plotly_chart(fig_line, use_container_width=True)

with c4:
    st.subheader("🌡️ % vs Hidrelétrica")
    df_rank = pd.DataFrame([
        {"Fonte": src, "% vs Hidro": d["vs_hydro_%"]}
        for src, d in r["ranking"].items()
    ]).sort_values("% vs Hidro")

    colors = ["#4CAF50" if v <= 0 else ("#FFC107" if v < 200 else "#F44336")
              for v in df_rank["% vs Hidro"]]
    fig_gauge = px.bar(
        df_rank, x="Fonte", y="% vs Hidro",
        color="Fonte", color_discrete_sequence=colors,
        template="plotly_white", text="% vs Hidro",
    )
    fig_gauge.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_gauge.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_gauge.update_layout(
        showlegend=False, height=320,
        margin=dict(l=0, r=0, t=10, b=10),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── Detail table ───────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Tabela de ranking completo")

df_table = pd.DataFrame([
    {
        "Fonte": src,
        "CO₂ estimado (kg)": f"{d['co2']:,.2f}",
        "vs Hidrelétrica (%)": f"{d['vs_hydro_%']:+.1f}%",
        "Tipo": "Elétrica" if src in r["elec"] else "Combustível líquido",
    }
    for src, d in r["ranking"].items()
])
st.dataframe(df_table, use_container_width=True, hide_index=True)

# ── Insight box ────────────────────────────────────────────────────────────────
if saving > 0:
    st.success(
        f"💡 Trocando de **{r['fonte']}** para **{best_src}**, a emissão estimada cai de "
        f"**{r['co2_sel']:,.1f} kg** para **{best_co2:,.1f} kg CO₂** "
        f"— uma redução de **{saving_pct}%** ({saving:,.1f} kg CO₂)."
    )
else:
    st.success(f"✅ **{r['fonte']}** já é a fonte com menor emissão entre as opções elétricas!")

st.caption("Modelo: Random Forest · R² ≈ 0.994 · Dataset: synthetic_energy_emissions_dataset.csv")
