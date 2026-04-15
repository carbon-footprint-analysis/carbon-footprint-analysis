import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import shap
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # necessário para Streamlit (sem display gráfico)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pegada de Carbono · Dashboard",
    page_icon="🌿",
    layout="wide",
)

# ── Constants ──────────────────────────────────────────────────────────────────
ESTADOS = [
    "AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT",
    "PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO",
]
SETORES     = ["industrial", "comercial", "residencial", "rural", "outros"]
FONTES      = ["hidrelétrica", "eólica", "solar", "nuclear", "térmica"]
MESES_LABEL = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
               7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
COLOR_MAP   = {
    "hidrelétrica":"#2196F3","eólica":"#4CAF50","solar":"#FFC107",
    "nuclear":"#9C27B0","térmica":"#F44336",
    "etanol":"#FF9800","gasolina":"#795548","diesel":"#607D8B",
}

# ── Transporte ─────────────────────────────────────────────────────────────────
TRANSPORT_FACTORS = {
    "bicicleta":  0.000,
    "metro_trem": 0.006,
    "onibus":     0.089,
    "carro":      0.192,
    "moto":       0.113,
    "aviao":      0.255,
}
TRANSPORT_LABELS = {
    "bicicleta":  "🚲 Bicicleta / A pé",
    "metro_trem": "🚇 Metrô / Trem",
    "onibus":     "🚌 Ônibus urbano",
    "carro":      "🚗 Carro (gasolina)",
    "moto":       "🏍️ Moto (gasolina)",
    "aviao":      "✈️ Avião doméstico",
}
TRANSPORT_COLOR = {
    "bicicleta":  "#4CAF50",
    "metro_trem": "#2196F3",
    "onibus":     "#FF9800",
    "carro":      "#F44336",
    "moto":       "#9C27B0",
    "aviao":      "#607D8B",
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_season(m: int) -> str:
    if m in [12, 1, 2]: return "Verao"
    if m in [3,  4, 5]: return "Outono"
    if m in [6,  7, 8]: return "Inverno"
    return "Primavera"

def liquid_fuel_emissions(energy_kwh: float) -> dict:
    fuels = {
        "etanol":   {"efficiency": 0.27, "emission_factor": 0.20},
        "gasolina": {"efficiency": 0.30, "emission_factor": 0.64},
        "diesel":   {"efficiency": 0.38, "emission_factor": 0.73},
    }
    return {f: round(energy_kwh / d["efficiency"] * d["emission_factor"], 2)
            for f, d in fuels.items()}

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
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

# ── Prediction helpers ─────────────────────────────────────────────────────────
def predict_one(consumo_kwh, mes, estado, setor, fonte_energia):
    df_in = pd.DataFrame([{
        "consumo_kwh": consumo_kwh, "mes": mes, "estado": estado,
        "setor": setor, "fonte_energia": fonte_energia,
        "season": get_season(mes),
    }])
    return round(float(model.predict(df_in)[0]), 2)

def predict_all_sources(consumo_kwh, mes, estado, setor):
    return {src: predict_one(consumo_kwh, mes, estado, setor, src) for src in FONTES}

# ── SHAP helpers ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_feature_names(_pipeline):
    num_features = ["consumo_kwh", "mes"]
    cat_features = ["estado", "setor", "fonte_energia", "season"]
    ohe_names = (
        _pipeline.named_steps["preprocessor"]
        .named_transformers_["cat"]
        .get_feature_names_out(cat_features)
    )
    return num_features + list(ohe_names)

@st.cache_data(show_spinner="Calculando SHAP values...")
def compute_shap(_pipeline, consumo_kwh, mes, estado, setor, fonte_energia):
    season = get_season(mes)
    df_in = pd.DataFrame([{
        "consumo_kwh": consumo_kwh, "mes": mes, "estado": estado,
        "setor": setor, "fonte_energia": fonte_energia, "season": season,
    }])
    preprocessor  = _pipeline.named_steps["preprocessor"]
    regressor     = _pipeline.named_steps["regressor"]
    x_transformed = preprocessor.transform(df_in)
    x_transformed = x_transformed.astype(float) 
    # ------------------------------------------------------

    # Agora o explainer não vai mais reclamar do tipo de dado
    explainer = shap.TreeExplainer(model_obj.named_steps['regressor'])
    shap_vals = explainer.shap_values(x_transformed)
    explainer     = shap.TreeExplainer(regressor)
    shap_vals     = explainer.shap_values(x_transformed)
    feature_names = get_feature_names(_pipeline)
    return shap_vals[0], explainer.expected_value, x_transformed[0], feature_names

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🌿 Dashboard · Pegada de Carbono")
st.caption("Estimativa de emissões de CO₂ com base em consumo energético e contexto geográfico.")

if model_error:
    st.error(f"⚠️ {model_error}")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Visão Geral",
    "⚖️ Simulador de Cenários",
    "🎯 Meta de Redução",
    "📂 Análise em Lote (CSV)",
    "🔍 Explicabilidade (SHAP)",
    "🚗 Pegada Total (Energia + Transporte)",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/leaf.png", width=60)
        st.title("Parâmetros")
        st.markdown("---")
        consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                   value=5_000.0, step=100.0)
        estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"))
        setor   = st.selectbox("Setor", SETORES)
        fonte   = st.selectbox("Fonte de energia atual", FONTES)
        mes     = st.slider("Mês", 1, 12, 6, format="%d")
        st.caption(f"Estação: **{get_season(mes)}** · Mês: **{MESES_LABEL[mes]}**")
        st.markdown("---")
        run = st.button("🔍 Calcular", use_container_width=True, type="primary")

    if "results" not in st.session_state or run:
        elec     = predict_all_sources(consumo, mes, estado, setor)
        fuels    = liquid_fuel_emissions(consumo)
        co2_sel  = elec[fonte]
        combined = {**elec, **fuels}
        ranking  = dict(sorted(combined.items(), key=lambda x: x[1]))
        hydro    = elec["hidrelétrica"]
        ranking_pct = {
            src: {"co2": v, "vs_hydro_%": round((v - hydro) / hydro * 100, 1)}
            for src, v in ranking.items()
        }
        st.session_state["results"] = {
            "co2_sel": co2_sel, "elec": elec, "fuels": fuels,
            "combined": combined, "ranking": ranking_pct,
            "consumo": consumo, "fonte": fonte,
            "estado": estado, "setor": setor, "mes": mes,
        }

    r = st.session_state["results"]
    best_src   = min(r["elec"], key=r["elec"].get)
    best_co2   = r["elec"][best_src]
    saving     = round(r["co2_sel"] - best_co2, 2)
    saving_pct = round(saving / r["co2_sel"] * 100, 1) if r["co2_sel"] > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Emissão atual", f"{r['co2_sel']:,.1f} kg CO₂", help=f"Fonte: {r['fonte']}")
    k2.metric("Menor emissão elétrica", f"{best_co2:,.1f} kg CO₂",
              delta=f"-{saving_pct}% vs atual" if saving > 0 else "✅ Já é a melhor",
              delta_color="inverse", help=f"Fonte: {best_src}")
    k3.metric("Consumo informado", f"{r['consumo']:,.0f} kWh")
    k4.metric("Estação / Mês", f"{get_season(r['mes'])} · {MESES_LABEL[r['mes']]}")
    st.markdown("---")

    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.subheader("📊 Emissões por fonte")
        df_bar = pd.DataFrame([
            {"Fonte": src, "CO₂ (kg)": v}
            for src, v in sorted(r["combined"].items(), key=lambda x: x[1])
        ])
        fig_bar = px.bar(df_bar, x="CO₂ (kg)", y="Fonte", orientation="h",
                         color="Fonte", color_discrete_map=COLOR_MAP,
                         text="CO₂ (kg)", template="plotly_white")
        fig_bar.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_bar.update_layout(showlegend=False, height=380,
                               yaxis={"categoryorder":"total ascending"},
                               margin=dict(l=0,r=60,t=10,b=10))
        for trace in fig_bar.data:
            if trace.name == r["fonte"]:
                trace.marker.line = dict(color="black", width=2)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("🥧 Participação relativa")
        df_pie = pd.DataFrame([{"Fonte": k, "CO₂ (kg)": v} for k, v in r["combined"].items()])
        fig_pie = px.pie(df_pie, values="CO₂ (kg)", names="Fonte",
                         color="Fonte", color_discrete_map=COLOR_MAP,
                         hole=0.45, template="plotly_white")
        fig_pie.update_traces(textposition="outside", textinfo="label+percent")
        fig_pie.update_layout(showlegend=False, height=380, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("📅 Variação mensal da emissão")
        meses_vals = [
            {"Mês": MESES_LABEL[m],
             "CO₂ (kg)": predict_one(r["consumo"], m, r["estado"], r["setor"], r["fonte"])}
            for m in range(1, 13)
        ]
        df_line = pd.DataFrame(meses_vals)
        fig_line = px.line(df_line, x="Mês", y="CO₂ (kg)", markers=True,
                           template="plotly_white", color_discrete_sequence=["#2196F3"])
        sel_val = df_line[df_line["Mês"] == MESES_LABEL[r["mes"]]]["CO₂ (kg)"].values[0]
        fig_line.add_scatter(x=[MESES_LABEL[r["mes"]]], y=[sel_val], mode="markers",
                             marker=dict(size=12, color="red"), name="Mês selecionado")
        fig_line.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=10))
        st.plotly_chart(fig_line, use_container_width=True)

    with c4:
        st.subheader("🌡️ % vs Hidrelétrica")
        df_rank = pd.DataFrame([
            {"Fonte": src, "% vs Hidro": d["vs_hydro_%"]}
            for src, d in r["ranking"].items()
        ]).sort_values("% vs Hidro")
        colors = ["#4CAF50" if v <= 0 else ("#FFC107" if v < 200 else "#F44336")
                  for v in df_rank["% vs Hidro"]]
        fig_pct = px.bar(df_rank, x="Fonte", y="% vs Hidro",
                         color="Fonte", color_discrete_sequence=colors,
                         template="plotly_white", text="% vs Hidro")
        fig_pct.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_pct.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_pct.update_layout(showlegend=False, height=320, margin=dict(l=0,r=0,t=10,b=10))
        st.plotly_chart(fig_pct, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Ranking completo")
    df_table = pd.DataFrame([
        {"Fonte": src,
         "CO₂ estimado (kg)": f"{d['co2']:,.2f}",
         "vs Hidrelétrica (%)": f"{d['vs_hydro_%']:+.1f}%",
         "Tipo": "Elétrica" if src in r["elec"] else "Combustível líquido"}
        for src, d in r["ranking"].items()
    ])
    st.dataframe(df_table, use_container_width=True, hide_index=True)

    if saving > 0:
        st.success(
            f"💡 Trocando de **{r['fonte']}** para **{best_src}**, a emissão cai de "
            f"**{r['co2_sel']:,.1f} kg** para **{best_co2:,.1f} kg CO₂** "
            f"— redução de **{saving_pct}%** ({saving:,.1f} kg CO₂)."
        )
    else:
        st.success(f"✅ **{r['fonte']}** já é a fonte com menor emissão entre as elétricas!")

    st.caption("Modelo: Random Forest · R² ≈ 0.994")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SIMULADOR DE CENÁRIOS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("⚖️ Simulador de Cenários — Comparação lado a lado")
    st.markdown("Configure dois perfis distintos e compare as emissões estimadas de CO₂.")
    st.markdown("---")

    col_a, col_sep, col_b = st.columns([5, 0.3, 5])

    with col_a:
        st.markdown("### 🔵 Cenário A")
        a_consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                     value=10_000.0, step=100.0, key="a_cons")
        a_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"), key="a_est")
        a_setor   = st.selectbox("Setor", SETORES, key="a_set")
        a_fonte   = st.selectbox("Fonte de energia", FONTES, key="a_fon")
        a_mes     = st.slider("Mês", 1, 12, 1, key="a_mes", format="%d")
        st.caption(f"Estação: **{get_season(a_mes)}**")

    with col_sep:
        st.markdown(
            "<div style='border-left:2px dashed #ccc;height:340px;margin-top:40px'></div>",
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown("### 🟠 Cenário B")
        b_consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                     value=10_000.0, step=100.0, key="b_cons")
        b_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("BA"), key="b_est")
        b_setor   = st.selectbox("Setor", SETORES, index=2, key="b_set")
        b_fonte   = st.selectbox("Fonte de energia", FONTES,
                                  index=FONTES.index("solar"), key="b_fon")
        b_mes     = st.slider("Mês", 1, 12, 7, key="b_mes", format="%d")
        st.caption(f"Estação: **{get_season(b_mes)}**")

    st.markdown("---")
    if st.button("▶️ Comparar cenários", type="primary", use_container_width=True):
        co2_a = predict_one(a_consumo, a_mes, a_estado, a_setor, a_fonte)
        co2_b = predict_one(b_consumo, b_mes, b_estado, b_setor, b_fonte)
        st.session_state["sim"] = {
            "co2_a": co2_a, "co2_b": co2_b,
            "a": (a_consumo, a_mes, a_estado, a_setor, a_fonte),
            "b": (b_consumo, b_mes, b_estado, b_setor, b_fonte),
        }

    if "sim" in st.session_state:
        s      = st.session_state["sim"]
        ca, cb = s["co2_a"], s["co2_b"]
        diff   = round(abs(ca - cb), 2)
        pct    = round(diff / max(ca, cb) * 100, 1)
        winner = "A 🔵" if ca < cb else ("B 🟠" if cb < ca else "Empate")

        m1, m2, m3 = st.columns(3)
        m1.metric("Emissão — Cenário A", f"{ca:,.1f} kg CO₂",
                  delta=f"{ca - cb:+,.1f} kg vs B", delta_color="inverse")
        m2.metric("Emissão — Cenário B", f"{cb:,.1f} kg CO₂",
                  delta=f"{cb - ca:+,.1f} kg vs A", delta_color="inverse")
        m3.metric("Diferença absoluta", f"{diff:,.1f} kg CO₂",
                  delta=f"{pct:.1f}% menor · Cenário {winner}")

        df_sim = pd.DataFrame([
            {"Cenário": "A 🔵", "CO₂ (kg)": ca,
             "Detalhe": f"{s['a'][4]} · {MESES_LABEL[s['a'][1]]} · {s['a'][2]}"},
            {"Cenário": "B 🟠", "CO₂ (kg)": cb,
             "Detalhe": f"{s['b'][4]} · {MESES_LABEL[s['b'][1]]} · {s['b'][2]}"},
        ])
        fig_sim = px.bar(df_sim, x="Cenário", y="CO₂ (kg)", color="Cenário",
                         color_discrete_sequence=["#2196F3","#FF9800"],
                         text="CO₂ (kg)", template="plotly_white",
                         hover_data=["Detalhe"])
        fig_sim.update_traces(texttemplate="%{text:,.1f}", textposition="outside", width=0.35)
        fig_sim.update_layout(showlegend=False, height=380, margin=dict(l=0,r=0,t=10,b=10))
        st.plotly_chart(fig_sim, use_container_width=True)

        st.markdown("#### 🕸️ Radar — emissão por fonte elétrica em cada cenário")
        all_a = predict_all_sources(s["a"][0], s["a"][1], s["a"][2], s["a"][3])
        all_b = predict_all_sources(s["b"][0], s["b"][1], s["b"][2], s["b"][3])
        fontes_r = list(all_a.keys())
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[all_a[f] for f in fontes_r] + [all_a[fontes_r[0]]],
            theta=fontes_r + [fontes_r[0]], fill="toself", name="Cenário A",
            line_color="#2196F3", fillcolor="rgba(33,150,243,0.15)"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[all_b[f] for f in fontes_r] + [all_b[fontes_r[0]]],
            theta=fontes_r + [fontes_r[0]], fill="toself", name="Cenário B",
            line_color="#FF9800", fillcolor="rgba(255,152,0,0.15)"
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)),
                                  height=400, margin=dict(l=40,r=40,t=20,b=20))
        st.plotly_chart(fig_radar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — META DE REDUÇÃO
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🎯 Meta de Redução de CO₂")
    st.markdown(
        "Informe sua situação atual e a meta desejada. "
        "O dashboard encontrará as combinações de **fonte + mês** que atingem o objetivo."
    )
    st.markdown("---")

    g1, g2 = st.columns(2)
    with g1:
        g_consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                     value=5_000.0, step=100.0, key="g_cons")
        g_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"), key="g_est")
        g_setor   = st.selectbox("Setor", SETORES, key="g_set")
        g_fonte   = st.selectbox("Fonte atual", FONTES,
                                  index=FONTES.index("térmica"), key="g_fon")
        g_mes     = st.slider("Mês atual", 1, 12, 6, key="g_mes", format="%d")
    with g2:
        st.markdown("#### 🎯 Configurar meta")
        meta_pct = st.slider(
            "Redução desejada (%)", min_value=5, max_value=95, value=30, step=5,
            help="Percentual de redução em relação à emissão atual",
        )
        st.markdown("#### ℹ️ Como funciona")
        st.info(
            "O sistema testa todas as combinações possíveis de **fonte elétrica × mês** "
            "e lista aquelas que atingem a meta de redução, ordenadas da menor para a maior emissão."
        )

    st.markdown("---")
    if st.button("🔎 Encontrar combinações", type="primary", use_container_width=True):
        co2_atual = predict_one(g_consumo, g_mes, g_estado, g_setor, g_fonte)
        meta_co2  = co2_atual * (1 - meta_pct / 100)

        resultados = []
        for src in FONTES:
            for m in range(1, 13):
                co2 = predict_one(g_consumo, m, g_estado, g_setor, src)
                reducao = round((co2_atual - co2) / co2_atual * 100, 1)
                resultados.append({
                    "Fonte": src, "Mês": MESES_LABEL[m], "Mês Num": m,
                    "CO₂ (kg)": co2, "Redução (%)": reducao,
                    "Atinge meta": co2 <= meta_co2,
                })

        df_res = pd.DataFrame(resultados)
        df_ok  = df_res[df_res["Atinge meta"]].sort_values("CO₂ (kg)")
        st.session_state["goal"] = {
            "co2_atual": co2_atual, "meta_co2": meta_co2,
            "meta_pct": meta_pct, "df_res": df_res, "df_ok": df_ok,
        }

    if "goal" in st.session_state:
        g = st.session_state["goal"]

        gk1, gk2, gk3 = st.columns(3)
        gk1.metric("Emissão atual", f"{g['co2_atual']:,.1f} kg CO₂")
        gk2.metric("Meta de emissão", f"{g['meta_co2']:,.1f} kg CO₂",
                   delta=f"-{g['meta_pct']}%", delta_color="inverse")
        gk3.metric("Combinações que atingem a meta", str(len(g["df_ok"])))

        if len(g["df_ok"]) == 0:
            st.error(
                "❌ Nenhuma combinação fonte+mês atinge essa meta com o consumo informado. "
                "Tente uma meta menor ou reduza o consumo."
            )
        else:
            st.success(f"✅ {len(g['df_ok'])} combinação(ões) atingem a meta de -{g['meta_pct']}%!")

            st.markdown("#### 🗺️ Heatmap — Emissão por fonte × mês")
            pivot = g["df_res"].pivot(index="Fonte", columns="Mês Num", values="CO₂ (kg)")
            pivot.columns = [MESES_LABEL[c] for c in pivot.columns]
            fig_heat = px.imshow(pivot, color_continuous_scale="RdYlGn_r",
                                  text_auto=".0f", aspect="auto",
                                  template="plotly_white",
                                  labels={"color": "kg CO₂"})
            fig_heat.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=10))
            st.plotly_chart(fig_heat, use_container_width=True)

            st.markdown("#### ✅ Combinações que atingem a meta")
            df_show = g["df_ok"][["Fonte","Mês","CO₂ (kg)","Redução (%)"]].copy()
            df_show["CO₂ (kg)"]    = df_show["CO₂ (kg)"].map("{:,.2f}".format)
            df_show["Redução (%)"] = df_show["Redução (%)"].map("{:+.1f}%".format)
            st.dataframe(df_show.reset_index(drop=True), use_container_width=True, hide_index=True)

            best_row = g["df_ok"].iloc[0]
            st.info(
                f"🏆 Melhor opção: **{best_row['Fonte']}** em **{best_row['Mês']}** → "
                f"**{best_row['CO₂ (kg)']:,.1f} kg CO₂** "
                f"({best_row['Redução (%)']:+.1f}% vs situação atual)"
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ANÁLISE EM LOTE (CSV)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📂 Análise em Lote — Upload de CSV")
    st.markdown(
        "Faça upload de um CSV com múltiplos registros. "
        "O modelo estimará o CO₂ de cada linha e gerará um relatório agregado."
    )

    with st.expander("📄 Ver formato esperado / Baixar template"):
        template_df = pd.DataFrame([
            {"consumo_kwh": 5000,  "estado": "SP", "setor": "industrial",
             "fonte_energia": "térmica", "mes": 1},
            {"consumo_kwh": 1200,  "estado": "BA", "setor": "residencial",
             "fonte_energia": "solar",   "mes": 7},
            {"consumo_kwh": 30000, "estado": "MG", "setor": "comercial",
             "fonte_energia": "eólica",  "mes": 4},
        ])
        st.dataframe(template_df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Baixar template CSV",
            template_df.to_csv(index=False).encode("utf-8"),
            "template_carbono.csv", "text/csv",
        )

    st.markdown("---")
    uploaded = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

    if uploaded:
        try:
            df_up = pd.read_csv(uploaded)
            required_cols = {"consumo_kwh","estado","setor","fonte_energia","mes"}
            missing = required_cols - set(df_up.columns)
            if missing:
                st.error(f"❌ Colunas faltando no CSV: {missing}")
            else:
                df_up["estado"]        = df_up["estado"].str.upper().str.strip()
                df_up["setor"]         = df_up["setor"].str.lower().str.strip()
                df_up["fonte_energia"] = df_up["fonte_energia"].str.lower().str.strip()
                df_up["mes"]           = df_up["mes"].astype(int)
                df_up["season"]        = df_up["mes"].apply(get_season)

                with st.spinner("Calculando emissões..."):
                    df_up["emissao_co2_estimada"] = df_up.apply(
                        lambda row: predict_one(
                            row["consumo_kwh"], row["mes"],
                            row["estado"], row["setor"], row["fonte_energia"]
                        ), axis=1
                    )

                st.success(f"✅ {len(df_up)} registros processados com sucesso!")

                bk1, bk2, bk3, bk4 = st.columns(4)
                bk1.metric("Total de registros", f"{len(df_up):,}")
                bk2.metric("Emissão total",
                           f"{df_up['emissao_co2_estimada'].sum():,.1f} kg CO₂")
                bk3.metric("Emissão média por registro",
                           f"{df_up['emissao_co2_estimada'].mean():,.1f} kg CO₂")
                bk4.metric("Maior emissão individual",
                           f"{df_up['emissao_co2_estimada'].max():,.1f} kg CO₂")

                st.markdown("---")

                ch1, ch2 = st.columns(2)
                with ch1:
                    st.markdown("#### 📊 Emissão total por setor")
                    df_setor = (df_up.groupby("setor")["emissao_co2_estimada"]
                                .sum().reset_index().sort_values("emissao_co2_estimada"))
                    fig_s = px.bar(df_setor, x="emissao_co2_estimada", y="setor",
                                   orientation="h", template="plotly_white", color="setor",
                                   text="emissao_co2_estimada",
                                   labels={"emissao_co2_estimada":"CO₂ (kg)"})
                    fig_s.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                    fig_s.update_layout(showlegend=False, height=300,
                                        margin=dict(l=0,r=60,t=10,b=10))
                    st.plotly_chart(fig_s, use_container_width=True)

                with ch2:
                    st.markdown("#### 🔋 Emissão total por fonte")
                    df_fonte = (df_up.groupby("fonte_energia")["emissao_co2_estimada"]
                                .sum().reset_index().sort_values("emissao_co2_estimada"))
                    fig_f = px.bar(df_fonte, x="emissao_co2_estimada", y="fonte_energia",
                                   orientation="h", template="plotly_white",
                                   color="fonte_energia", color_discrete_map=COLOR_MAP,
                                   text="emissao_co2_estimada",
                                   labels={"emissao_co2_estimada":"CO₂ (kg)",
                                           "fonte_energia":"Fonte"})
                    fig_f.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                    fig_f.update_layout(showlegend=False, height=300,
                                        margin=dict(l=0,r=60,t=10,b=10))
                    st.plotly_chart(fig_f, use_container_width=True)

                ch3, ch4 = st.columns(2)
                with ch3:
                    st.markdown("#### 🗺️ Emissão por estado")
                    df_est = (df_up.groupby("estado")["emissao_co2_estimada"]
                              .sum().reset_index()
                              .sort_values("emissao_co2_estimada", ascending=False))
                    fig_e = px.bar(df_est, x="estado", y="emissao_co2_estimada",
                                   template="plotly_white", color="estado",
                                   labels={"emissao_co2_estimada":"CO₂ (kg)"})
                    fig_e.update_layout(showlegend=False, height=300,
                                        margin=dict(l=0,r=0,t=10,b=10))
                    st.plotly_chart(fig_e, use_container_width=True)

                with ch4:
                    st.markdown("#### 📅 Emissão por mês")
                    df_mes = (df_up.groupby("mes")["emissao_co2_estimada"]
                              .sum().reset_index())
                    df_mes["Mês"] = df_mes["mes"].map(MESES_LABEL)
                    fig_m = px.line(df_mes, x="Mês", y="emissao_co2_estimada", markers=True,
                                    template="plotly_white",
                                    color_discrete_sequence=["#2196F3"],
                                    labels={"emissao_co2_estimada":"CO₂ (kg)"})
                    fig_m.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=10))
                    st.plotly_chart(fig_m, use_container_width=True)

                st.markdown("---")
                st.markdown("#### 📋 Resultado completo")
                st.dataframe(
                    df_up.drop(columns=["season"])
                         .rename(columns={"emissao_co2_estimada":"CO₂ estimado (kg)"}),
                    use_container_width=True, hide_index=True,
                )

                st.download_button(
                    "⬇️ Baixar resultado com predições",
                    df_up.drop(columns=["season"]).to_csv(index=False).encode("utf-8"),
                    "resultado_co2.csv", "text/csv",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — EXPLICABILIDADE (SHAP)
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("🔍 Explicabilidade da Predição — SHAP")
    st.markdown(
        "Entenda **por que** o modelo chegou a uma estimativa específica. "
        "Para cada predição, o SHAP decompõe a contribuição individual de cada variável."
    )
    st.info(
        "💡 **Como ler o gráfico Waterfall:** "
        "Barras **vermelhas** são variáveis que **aumentam** a emissão estimada; "
        "barras **azuis** a **reduzem**. "
        "O ponto de partida é a média histórica do modelo (valor base)."
    )
    st.markdown("---")

    sh1, sh2 = st.columns(2)
    with sh1:
        sh_consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                      value=5_000.0, step=100.0, key="sh_cons")
        sh_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"), key="sh_est")
        sh_setor   = st.selectbox("Setor", SETORES, key="sh_set")
    with sh2:
        sh_fonte = st.selectbox("Fonte de energia", FONTES, key="sh_fon")
        sh_mes   = st.slider("Mês", 1, 12, 6, key="sh_mes", format="%d")
        st.caption(f"Estação: **{get_season(sh_mes)}**")

    st.markdown("---")
    if st.button("🧠 Explicar predição", type="primary", use_container_width=True):

        co2_pred = predict_one(sh_consumo, sh_mes, sh_estado, sh_setor, sh_fonte)
        shap_row, expected_val, x_row, feat_names = compute_shap(
            model, sh_consumo, sh_mes, sh_estado, sh_setor, sh_fonte
        )
        st.session_state["shap_result"] = {
            "co2_pred": co2_pred, "shap_row": shap_row,
            "expected_val": expected_val, "x_row": x_row,
            "feat_names": feat_names,
            "label": f"{sh_fonte} · {MESES_LABEL[sh_mes]} · {sh_estado} · {sh_setor}",
        }

    if "shap_result" in st.session_state:
        sr = st.session_state["shap_result"]

        st.metric("Emissão estimada", f"{sr['co2_pred']:,.2f} kg CO₂")
        st.markdown("---")

        # ── Waterfall ─────────────────────────────────────────────────────────
        st.markdown("#### 🌊 Waterfall — Contribuição de cada variável")
        st.caption(f"Cenário: **{sr['label']}** · Valor base (média do modelo): **{sr['expected_val']:,.1f} kg CO₂**")

        explanation = shap.Explanation(
            values=sr["shap_row"],
            base_values=sr["expected_val"],
            data=sr["x_row"],
            feature_names=sr["feat_names"],
        )

        fig_wf, _ = plt.subplots(figsize=(9, 5))
        shap.plots.waterfall(explanation, max_display=12, show=False)
        plt.title(f"Explicação: {sr['label']}", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_wf)
        plt.close()

        # ── Tabela de contribuições ────────────────────────────────────────────
        st.markdown("#### 📋 Contribuições detalhadas (top 15)")
        df_contrib = (
            pd.DataFrame({"Feature": sr["feat_names"], "SHAP": sr["shap_row"]})
            .assign(Direção=lambda d: d["SHAP"].apply(
                lambda v: "⬆️ Aumenta" if v > 0 else "⬇️ Reduz"))
            .assign(**{"Contribuição (kg CO₂)": lambda d: d["SHAP"].round(4)})
            .sort_values("SHAP", key=abs, ascending=False)
            .head(15)
            [["Feature", "Contribuição (kg CO₂)", "Direção"]]
            .reset_index(drop=True)
        )
        st.dataframe(df_contrib, use_container_width=True, hide_index=True)

        # ── Insight textual ────────────────────────────────────────────────────
        aumenta = df_contrib[df_contrib["Direção"] == "⬆️ Aumenta"]
        reduz   = df_contrib[df_contrib["Direção"] == "⬇️ Reduz"]
        top_pos = aumenta.iloc[0]["Feature"] if len(aumenta) > 0 else "—"
        top_neg = reduz.iloc[0]["Feature"]   if len(reduz)   > 0 else "—"

        st.info(
            f"📌 **Maior fator de aumento:** `{top_pos}`  \n"
            f"📌 **Maior fator de redução:** `{top_neg}`  \n"
            f"O modelo partiu de uma base de **{sr['expected_val']:,.1f} kg CO₂** "
            f"e chegou a **{sr['co2_pred']:,.2f} kg CO₂** após considerar todas as variáveis."
        )

st.caption("Modelo: Random Forest · R² ≈ 0.994 · Dashboard v3.0")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — PEGADA TOTAL (ENERGIA + TRANSPORTE)
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("🚗 Pegada Total — Energia + Transporte")
    st.markdown(
        "Calcule a **pegada de carbono completa**, somando emissões de energia elétrica "
        "(Escopo 2) com emissões de mobilidade (Escopos 1 e 3)."
    )
    st.markdown("---")

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("#### ⚡ Energia")
        t_consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                     value=5_000.0, step=100.0, key="t_cons")
        t_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"), key="t_est")
        t_setor   = st.selectbox("Setor", SETORES, key="t_set")
        t_fonte   = st.selectbox("Fonte de energia", FONTES, key="t_fon")
        t_mes     = st.slider("Mês", 1, 12, 6, key="t_mes", format="%d")

    with t2:
        st.markdown("#### 🚗 Transporte")
        modais_display = list(TRANSPORT_LABELS.values())
        modais_keys    = list(TRANSPORT_LABELS.keys())
        modal_sel_label = st.selectbox("Modal de transporte", modais_display, index=3, key="t_modal")
        modal_sel = modais_keys[modais_display.index(modal_sel_label)]

        t_km = st.number_input("Distância percorrida (km/mês)", min_value=0.0,
                                max_value=50_000.0, value=500.0, step=10.0, key="t_km")

        fator = TRANSPORT_FACTORS[modal_sel]
        st.caption(f"Fator de emissão: **{fator} kg CO₂/km** · Fonte: IPCC AR6 / CETESB 2023")

        st.markdown("##### Comparar todos os modais para essa distância")
        show_all = st.checkbox("Mostrar ranking de modais", value=True, key="t_show_all")

    st.markdown("---")
    if st.button("🌍 Calcular pegada total", type="primary", use_container_width=True):
        co2_energia     = predict_one(t_consumo, t_mes, t_estado, t_setor, t_fonte)
        co2_transporte  = round(fator * t_km, 2)
        co2_total       = round(co2_energia + co2_transporte, 2)
        pct_energia     = round(co2_energia / co2_total * 100, 1) if co2_total > 0 else 0
        pct_transporte  = round(co2_transporte / co2_total * 100, 1) if co2_total > 0 else 0

        st.session_state["pegada_total"] = {
            "co2_energia": co2_energia, "co2_transporte": co2_transporte,
            "co2_total": co2_total, "pct_energia": pct_energia,
            "pct_transporte": pct_transporte, "modal": modal_sel,
            "km": t_km, "consumo": t_consumo, "fonte": t_fonte,
            "estado": t_estado, "setor": t_setor, "mes": t_mes,
        }

    if "pegada_total" in st.session_state:
        pt = st.session_state["pegada_total"]

        # KPIs
        pk1, pk2, pk3 = st.columns(3)
        pk1.metric("Emissão — Energia", f"{pt['co2_energia']:,.1f} kg CO₂",
                   delta=f"{pt['pct_energia']}% do total")
        pk2.metric("Emissão — Transporte", f"{pt['co2_transporte']:,.1f} kg CO₂",
                   delta=f"{pt['pct_transporte']}% do total")
        pk3.metric("🌍 Pegada Total", f"{pt['co2_total']:,.1f} kg CO₂")

        st.markdown("---")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Composição da pegada de carbono")
            df_comp = pd.DataFrame([
                {"Escopo": "Energia (Escopo 2)", "CO₂ (kg)": pt["co2_energia"]},
                {"Escopo": "Transporte (Escopos 1/3)", "CO₂ (kg)": pt["co2_transporte"]},
            ])
            fig_comp = px.pie(df_comp, values="CO₂ (kg)", names="Escopo",
                              color_discrete_sequence=["#2196F3", "#FF9800"],
                              hole=0.45, template="plotly_white")
            fig_comp.update_traces(textposition="outside", textinfo="label+percent")
            fig_comp.update_layout(showlegend=False, height=320,
                                   margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_comp, use_container_width=True)

        with c2:
            if show_all:
                st.markdown("#### Ranking de modais para a mesma distância")
                df_modais = pd.DataFrame([
                    {"Modal": TRANSPORT_LABELS[m], "CO₂ Transporte (kg)": round(f * pt["km"], 2),
                     "Pegada Total (kg)": round(pt["co2_energia"] + f * pt["km"], 2),
                     "key": m}
                    for m, f in TRANSPORT_FACTORS.items()
                ]).sort_values("CO₂ Transporte (kg)")

                fig_mod = px.bar(
                    df_modais, x="CO₂ Transporte (kg)", y="Modal", orientation="h",
                    color="key", color_discrete_map={k: TRANSPORT_COLOR[k] for k in TRANSPORT_COLOR},
                    text="CO₂ Transporte (kg)", template="plotly_white",
                )
                fig_mod.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
                fig_mod.update_layout(showlegend=False, height=320,
                                      yaxis={"categoryorder": "total ascending"},
                                      margin=dict(l=0, r=60, t=10, b=10))
                # Destaca modal selecionado
                for trace in fig_mod.data:
                    if trace.name == pt["modal"]:
                        trace.marker.line = dict(color="black", width=2)
                st.plotly_chart(fig_mod, use_container_width=True)

        # Insight de redução
        best_modal_key  = min(TRANSPORT_FACTORS, key=TRANSPORT_FACTORS.get)
        best_modal_co2  = round(TRANSPORT_FACTORS[best_modal_key] * pt["km"], 2)
        saving_transport = round(pt["co2_transporte"] - best_modal_co2, 2)

        if saving_transport > 0:
            nova_total = round(pt["co2_energia"] + best_modal_co2, 2)
            reducao_pct = round(saving_transport / pt["co2_total"] * 100, 1)
            st.success(
                f"💡 Trocando **{TRANSPORT_LABELS[pt['modal']]}** por "
                f"**{TRANSPORT_LABELS[best_modal_key]}** para os mesmos **{pt['km']:,.0f} km**, "
                f"a emissão de transporte cai de **{pt['co2_transporte']:,.1f} kg** para "
                f"**{best_modal_co2:,.1f} kg CO₂** — reduzindo a pegada total em "
                f"**{reducao_pct}%** ({saving_transport:,.1f} kg CO₂)."
            )
        else:
            st.success(f"✅ **{TRANSPORT_LABELS[pt['modal']]}** já é o modal com menor emissão!")

        # Tabela de referência
        with st.expander("📋 Tabela de fatores de emissão por modal"):
            df_ref = pd.DataFrame([
                {"Modal": TRANSPORT_LABELS[m],
                 "Fator (kg CO₂/km)": f,
                 "Emissão p/ 500km (kg)": round(f * 500, 1),
                 "Fonte": "IPCC AR6 / CETESB 2023"}
                for m, f in TRANSPORT_FACTORS.items()
            ])
            st.dataframe(df_ref, use_container_width=True, hide_index=True)

