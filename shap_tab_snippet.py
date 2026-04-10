# ══════════════════════════════════════════════════════════════════════════════
# TRECHO SHAP — adicionar ao app.py
#
# 1. Instale: pip install shap
# 2. Adicione "🔍 Explicabilidade (SHAP)" à lista de tabs no topo do app.py:
#
#    tab1, tab2, tab3, tab4, tab5 = st.tabs([
#        "📊 Visão Geral",
#        "⚖️ Simulador de Cenários",
#        "🎯 Meta de Redução",
#        "📂 Análise em Lote (CSV)",
#        "🔍 Explicabilidade (SHAP)",   ← adicionar
#    ])
#
# 3. Cole o bloco abaixo como o último "with tab5:" do arquivo.
# ══════════════════════════════════════════════════════════════════════════════

import shap
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # necessário para Streamlit (sem display gráfico)

# ── Helpers SHAP (adicionar junto dos outros helpers no topo do app.py) ────────

@st.cache_data(show_spinner=False)
def get_feature_names(_pipeline):
    """Recupera os nomes das features após o pré-processamento."""
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
    """
    Calcula SHAP values para uma única predição.
    Retorna (shap_values_row, expected_value, x_transformed_row, feature_names).
    """
    season = get_season(mes)
    df_in = pd.DataFrame([{
        "consumo_kwh": consumo_kwh, "mes": mes, "estado": estado,
        "setor": setor, "fonte_energia": fonte_energia, "season": season,
    }])
    preprocessor  = _pipeline.named_steps["preprocessor"]
    regressor     = _pipeline.named_steps["regressor"]
    x_transformed = preprocessor.transform(df_in)
    explainer     = shap.TreeExplainer(regressor)
    shap_vals     = explainer.shap_values(x_transformed)
    feature_names = get_feature_names(_pipeline)
    return shap_vals[0], explainer.expected_value, x_transformed[0], feature_names

# ── Tab SHAP ───────────────────────────────────────────────────────────────────
with tab5:
    st.subheader("🔍 Explicabilidade da Predição — SHAP")
    st.markdown(
        "Entenda **por que** o modelo chegou a uma estimativa específica. "
        "Para cada predição, o SHAP decompõe a contribuição individual de cada variável."
    )
    st.markdown("---")

    # Inputs
    sh1, sh2 = st.columns(2)
    with sh1:
        sh_consumo = st.number_input("Consumo (kWh)", min_value=1.0, max_value=500_000.0,
                                      value=5_000.0, step=100.0, key="sh_cons")
        sh_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"), key="sh_est")
        sh_setor   = st.selectbox("Setor", SETORES, key="sh_set")
    with sh2:
        sh_fonte   = st.selectbox("Fonte de energia", FONTES, key="sh_fon")
        sh_mes     = st.slider("Mês", 1, 12, 6, key="sh_mes", format="%d")
        st.caption(f"Estação: **{get_season(sh_mes)}**")

    st.markdown("---")
    if st.button("🧠 Explicar predição", type="primary", use_container_width=True):

        co2_pred = predict_one(sh_consumo, sh_mes, sh_estado, sh_setor, sh_fonte)
        shap_row, expected_val, x_row, feat_names = compute_shap(
            model, sh_consumo, sh_mes, sh_estado, sh_setor, sh_fonte
        )

        st.metric("Emissão estimada", f"{co2_pred:,.2f} kg CO₂")
        st.markdown("---")

        # ── Waterfall — explicação individual ─────────────────────────────────
        st.markdown("#### 🌊 Waterfall — Contribuição de cada variável para esta predição")
        st.caption(
            "Barras **vermelhas** aumentam a emissão estimada; "
            "barras **azuis** a reduzem. "
            f"O valor base (média do modelo) é **{expected_val:,.1f} kg CO₂**."
        )

        explanation = shap.Explanation(
            values=shap_row,
            base_values=expected_val,
            data=x_row,
            feature_names=feat_names,
        )

        fig_wf, ax_wf = plt.subplots(figsize=(9, 5))
        shap.plots.waterfall(explanation, max_display=12, show=False)
        plt.title(f"Explicação: {sh_fonte} · {MESES_LABEL[sh_mes]} · {sh_estado} · {sh_setor}", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_wf)
        plt.close()

        # ── Tabela de contribuições ────────────────────────────────────────────
        st.markdown("#### 📋 Contribuições detalhadas")

        df_contrib = (
            pd.DataFrame({"Feature": feat_names, "SHAP": shap_row})
            .assign(Direção=lambda d: d["SHAP"].apply(lambda v: "⬆️ Aumenta" if v > 0 else "⬇️ Reduz"))
            .assign(**{"Contribuição (kg CO₂)": lambda d: d["SHAP"].round(4)})
            .sort_values("SHAP", key=abs, ascending=False)
            .head(15)
            [["Feature", "Contribuição (kg CO₂)", "Direção"]]
            .reset_index(drop=True)
        )
        st.dataframe(df_contrib, use_container_width=True, hide_index=True)

        # ── Insight textual ────────────────────────────────────────────────────
        top_pos = df_contrib[df_contrib["Direção"] == "⬆️ Aumenta"].iloc[0]["Feature"] if any(df_contrib["Direção"] == "⬆️ Aumenta") else "—"
        top_neg = df_contrib[df_contrib["Direção"] == "⬇️ Reduz"].iloc[0]["Feature"] if any(df_contrib["Direção"] == "⬇️ Reduz") else "—"

        st.info(
            f"📌 **Maior fator de aumento:** `{top_pos}`  \n"
            f"📌 **Maior fator de redução:** `{top_neg}`  \n"
            f"O modelo partiu de uma base de **{expected_val:,.1f} kg CO₂** "
            f"e chegou a **{co2_pred:,.2f} kg CO₂** após considerar todas as variáveis."
        )
