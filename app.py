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
    initial_sidebar_state="expanded",
)

# Reduzir padding da sidebar
st.markdown("""
<style>
    /* Reduzir padding geral da sidebar */
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Reduzir espaçamento entre elementos */
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
# Inicializar tema no session_state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Definir cores baseadas no tema
if st.session_state.dark_mode:
    # Dark Mode Colors
    THEME_COLORS = {
        "bg_primary": "#0E1117",
        "bg_secondary": "#1E2530",
        "bg_tertiary": "#262C38",
        "text_primary": "#E8F5E9",
        "text_secondary": "#A5D6A7",
        "accent_primary": "#66BB6A",
        "accent_secondary": "#2E7D32",
        "border": "#2E7D32",
        "shadow": "rgba(102, 187, 106, 0.2)",
    }
else:
    # Light Mode Colors
    THEME_COLORS = {
        "bg_primary": "#FAFAFA",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#E8F5E9",
        "text_primary": "#1B5E20",
        "text_secondary": "#2E7D32",
        "accent_primary": "#2E7D32",
        "accent_secondary": "#66BB6A",
        "border": "#C8E6C9",
        "shadow": "rgba(0, 0, 0, 0.1)",
    }

st.markdown(f"""
<style>
    /* Variáveis de tema */
    :root {{
        --bg-primary: {THEME_COLORS["bg_primary"]};
        --bg-secondary: {THEME_COLORS["bg_secondary"]};
        --bg-tertiary: {THEME_COLORS["bg_tertiary"]};
        --text-primary: {THEME_COLORS["text_primary"]};
        --text-secondary: {THEME_COLORS["text_secondary"]};
        --accent-primary: {THEME_COLORS["accent_primary"]};
        --accent-secondary: {THEME_COLORS["accent_secondary"]};
        --border: {THEME_COLORS["border"]};
        --shadow: {THEME_COLORS["shadow"]};
    }}
    
    /* Background principal */
    .stApp {{
        background-color: var(--bg-primary);
        transition: background-color 0.3s ease;
    }}
    
    /* Estilo das tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: var(--bg-tertiary);
        padding: 0.5rem;
        border-radius: 10px;
        transition: background-color 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: var(--bg-secondary);
        border-radius: 8px;
        padding: 0 24px;
        font-weight: 500;
        border: 2px solid transparent;
        transition: all 0.3s;
        color: var(--text-primary);
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: var(--bg-tertiary);
        border-color: var(--border);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {THEME_COLORS["accent_primary"]} 0%, {THEME_COLORS["accent_secondary"]} 100%);
        color: white !important;
        border: 2px solid {THEME_COLORS["accent_primary"]};
    }}
    
    /* Botões customizados */
    .stButton > button {{
        background: linear-gradient(135deg, {THEME_COLORS["accent_primary"]} 0%, {THEME_COLORS["accent_secondary"]} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px var(--shadow);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px var(--shadow);
    }}
    
    /* Sidebar customizada */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        transition: background 0.3s ease;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        padding: 0.5rem;
        color: var(--text-primary);
    }}
    
    /* Reduzir espaçamento dos inputs na sidebar */
    [data-testid="stSidebar"] .stNumberInput,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSlider {{
        margin-bottom: 0.5rem;
    }}
    
    [data-testid="stSidebar"] .stNumberInput > label,
    [data-testid="stSidebar"] .stSelectbox > label,
    [data-testid="stSidebar"] .stSlider > label {{
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
        font-weight: 500;
    }}
    
    [data-testid="stSidebar"] .stButton {{
        margin-top: 0.5rem;
    }}
    
    /* Métricas customizadas */
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-secondary);
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem;
        color: var(--text-primary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Cards de alerta customizados */
    .stAlert {{
        border-radius: 8px;
        border-left-width: 4px;
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }}
    
    /* Dataframes */
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
        background-color: var(--bg-secondary);
    }}
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border-color: var(--border);
    }}
    
    /* Sliders */
    .stSlider > div > div > div {{
        background-color: var(--bg-tertiary);
    }}
    
    /* Animação de fade-in */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-in;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: var(--text-primary);
        border-top: 2px solid var(--border);
        margin-top: 3rem;
        transition: all 0.3s ease;
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
        transition: all 0.3s ease;
    }}
    
    .badge-success {{
        background-color: {"#2E4A2E" if st.session_state.dark_mode else "#C8E6C9"};
        color: {"#A5D6A7" if st.session_state.dark_mode else "#1B5E20"};
    }}
    
    .badge-info {{
        background-color: {"#1E3A5F" if st.session_state.dark_mode else "#BBDEFB"};
        color: {"#90CAF9" if st.session_state.dark_mode else "#0D47A1"};
    }}
    
    /* Textos */
    h1, h2, h3, h4, h5, h6, p, span, div {{
        color: var(--text-primary);
        transition: color 0.3s ease;
    }}
    
    /* Responsividade */
    @media (max-width: 768px) {{
        .main-header h1 {{
            font-size: 1.8rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            font-size: 0.8rem;
            padding: 0 12px;
        }}
        
        .theme-toggle {{
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
# Limites baseados em dados históricos do setor energético brasileiro
MIN_CONSUMO_KWH = 1.0
MAX_CONSUMO_KWH = 500_000.0  # Limite para grandes indústrias
DEFAULT_CONSUMO_KWH = 5_000.0  # Consumo médio residencial mensal
STEP_CONSUMO_KWH = 100.0

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

# Template customizado para gráficos Plotly
PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Arial, sans-serif", "size": 12, "color": "#1B5E20"},
        "title": {"font": {"size": 16, "color": "#1B5E20", "family": "Arial, sans-serif"}},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(250,250,250,0.5)",
        "xaxis": {
            "gridcolor": "#E8F5E9",
            "linecolor": "#C8E6C9",
            "zerolinecolor": "#C8E6C9"
        },
        "yaxis": {
            "gridcolor": "#E8F5E9",
            "linecolor": "#C8E6C9",
            "zerolinecolor": "#C8E6C9"
        },
        "colorway": ["#2E7D32", "#66BB6A", "#81C784", "#A5D6A7", "#C8E6C9"],
        "hovermode": "closest"
    }
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
    """
    Retorna a estação do ano baseada no mês (hemisfério sul).
    
    Args:
        m: Mês (1-12)
        
    Returns:
        str: Nome da estação (Verao, Outono, Inverno, Primavera)
    """
    if m in [12, 1, 2]: return "Verao"
    if m in [3,  4, 5]: return "Outono"
    if m in [6,  7, 8]: return "Inverno"
    return "Primavera"

def liquid_fuel_emissions(energy_kwh: float) -> dict:
    """
    Calcula emissões de CO₂ para combustíveis líquidos baseado no consumo energético.
    
    Args:
        energy_kwh: Energia consumida em kWh
        
    Returns:
        dict: Dicionário com combustível -> emissão de CO₂ em kg
    """
    fuels = {
        "etanol":   {"efficiency": 0.27, "emission_factor": 0.20},
        "gasolina": {"efficiency": 0.30, "emission_factor": 0.64},
        "diesel":   {"efficiency": 0.38, "emission_factor": 0.73},
    }
    return {f: round(energy_kwh / d["efficiency"] * d["emission_factor"], 2)
            for f, d in fuels.items()}

def create_bar_chart(df, x, y, color=None, color_map=None, orientation="h", 
                     title=None, height=380, show_text=True):
    """
    Cria um gráfico de barras padronizado.
    
    Args:
        df: DataFrame com os dados
        x: Coluna para eixo X
        y: Coluna para eixo Y
        color: Coluna para colorir as barras
        color_map: Mapa de cores personalizado
        orientation: Orientação ("h" ou "v")
        title: Título do gráfico
        height: Altura do gráfico
        show_text: Se deve mostrar valores nas barras
        
    Returns:
        plotly.graph_objects.Figure: Gráfico configurado
    """
    fig = px.bar(df, x=x, y=y, orientation=orientation,
                 color=color, color_discrete_map=color_map,
                 text=x if orientation == "h" else y,
                 template="plotly_white", title=title)
    
    if show_text:
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    
    fig.update_layout(
        showlegend=False, 
        height=height,
        yaxis={"categoryorder": "total ascending"} if orientation == "h" else {},
        margin=dict(l=0, r=60 if orientation == "h" else 0, t=10, b=10)
    )
    
    return fig

def safe_division(numerator, denominator, default=0):
    """
    Realiza divisão segura, retornando valor padrão se denominador for zero.
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor padrão se denominador for zero
        
    Returns:
        float: Resultado da divisão ou valor padrão
    """
    return numerator / denominator if denominator != 0 else default

def create_metric_card(label, value, delta=None, icon="📊", color="green"):
    """
    Cria um card de métrica visualmente atraente com gradiente e hover effect.
    
    Args:
        label: Rótulo da métrica
        value: Valor principal
        delta: Variação (opcional)
        icon: Ícone emoji
        color: Cor do tema (green, blue, orange, red)
        
    Returns:
        str: HTML do card
    """
    colors = {
        "green": {"bg": "linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%)"},
        "blue": {"bg": "linear-gradient(135deg, #1976D2 0%, #42A5F5 100%)"},
        "orange": {"bg": "linear-gradient(135deg, #F57C00 0%, #FFB74D 100%)"},
        "red": {"bg": "linear-gradient(135deg, #D32F2F 0%, #EF5350 100%)"},
    }
    
    bg = colors.get(color, colors["green"])["bg"]
    
    delta_html = ""
    if delta:
        delta_html = f'''
        <div style="margin-top: 0.5rem; padding: 0.25rem 0.75rem; background: rgba(255,255,255,0.2); border-radius: 20px; display: inline-block; font-size: 0.85rem; color: white;">
            {delta}
        </div>
        '''
    
    return f"""
    <div style="background: {bg}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); color: white; transition: transform 0.3s, box-shadow 0.3s; cursor: pointer; height: 100%;" onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.25)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">{label}</div>
        <div style="font-size: 2.2rem; font-weight: 700; margin-top: 0.5rem;">{value}</div>
        {delta_html}
    </div>
    """

def create_insight_card(title, message, type="success"):
    """
    Cria card de insight destacado.
    
    Args:
        title: Título do insight
        message: Mensagem
        type: Tipo (success, warning, info)
        
    Returns:
        str: HTML do card
    """
    styles = {
        "success": {
            "bg": "linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)",
            "border": "#4CAF50",
            "icon": "💡"
        },
        "warning": {
            "bg": "linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%)",
            "border": "#FF9800",
            "icon": "⚠️"
        },
        "info": {
            "bg": "linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%)",
            "border": "#2196F3",
            "icon": "ℹ️"
        }
    }
    
    style = styles.get(type, styles["success"])
    
    return f"""
    <div style="background: {style['bg']}; border-left: 4px solid {style['border']}; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">{style['icon']}</div>
            <div>
                <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">{title}</div>
                <div style="color: #555; line-height: 1.5;">{message}</div>
            </div>
        </div>
    </div>
    """

def apply_chart_style(fig):
    """
    Aplica estilo customizado consistente aos gráficos Plotly.
    Adapta cores baseado no tema (light/dark mode).
    
    Args:
        fig: Figura Plotly
        
    Returns:
        fig: Figura com estilo aplicado
    """
    # Cores baseadas no tema
    if st.session_state.dark_mode:
        bg_color = "rgba(30, 37, 48, 0.5)"
        grid_color = "#2E7D32"
        line_color = "#66BB6A"
        text_color = "#E8F5E9"
    else:
        bg_color = "rgba(250,250,250,0.5)"
        grid_color = "#E8F5E9"
        line_color = "#C8E6C9"
        text_color = "#1B5E20"
    
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12, color=text_color),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=bg_color,
        xaxis=dict(gridcolor=grid_color, linecolor=line_color, zerolinecolor=line_color),
        yaxis=dict(gridcolor=grid_color, linecolor=line_color, zerolinecolor=line_color),
        hoverlabel=dict(
            bgcolor="white" if not st.session_state.dark_mode else "#262C38",
            font_size=12,
            font_family="Arial",
            bordercolor="#2E7D32"
        )
    )
    return fig

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

# ── Validação do modelo ────────────────────────────────────────────────────────
if model is None:
    st.error(f"❌ {model_error}")
    st.info(
        "**Como resolver:**\n\n"
        "1. Certifique-se de que o arquivo `best_carbon_footprint_model.joblib` existe\n"
        "2. Coloque-o na pasta `models/` na raiz do projeto\n"
        "3. Reinicie a aplicação"
    )
    st.stop()

# ── Prediction helpers ─────────────────────────────────────────────────────────
def predict_one(consumo_kwh, mes, estado, setor, fonte_energia):
    """
    Realiza predição de emissão de CO₂ para um único registro.
    
    Args:
        consumo_kwh: Consumo de energia em kWh
        mes: Mês (1-12)
        estado: Sigla do estado (ex: "SP")
        setor: Setor econômico
        fonte_energia: Fonte de energia utilizada
        
    Returns:
        float: Emissão de CO₂ estimada em kg, arredondada para 2 casas decimais
    """
    try:
        df_in = pd.DataFrame([{
            "consumo_kwh": consumo_kwh, "mes": mes, "estado": estado,
            "setor": setor, "fonte_energia": fonte_energia,
            "season": get_season(mes),
        }])
        prediction = model.predict(df_in)[0]
        return round(float(prediction), 2)
    except Exception as e:
        st.error(f"❌ Erro ao calcular emissão: {str(e)}")
        return 0.0

def predict_all_sources(consumo_kwh, mes, estado, setor):
    """
    Realiza predições para todas as fontes de energia disponíveis.
    
    Args:
        consumo_kwh: Consumo de energia em kWh
        mes: Mês (1-12)
        estado: Sigla do estado
        setor: Setor econômico
        
    Returns:
        dict: Dicionário com fonte_energia -> emissão_co2
    """
    return {src: predict_one(consumo_kwh, mes, estado, setor, src) for src in FONTES}

def predict_batch(df_batch):
    """
    Realiza predições em lote para múltiplos registros (otimizado).
    
    Args:
        df_batch: DataFrame com colunas: consumo_kwh, mes, estado, setor, fonte_energia
        
    Returns:
        np.array: Array com predições de CO₂
    """
    try:
        df_batch = df_batch.copy()
        df_batch["season"] = df_batch["mes"].apply(get_season)
        predictions = model.predict(df_batch)
        return predictions
    except Exception as e:
        st.error(f"❌ Erro ao calcular emissões em lote: {str(e)}")
        return np.zeros(len(df_batch))

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

@st.cache_resource
def compute_shap(_model, _consumo, _mes, _estado, _setor, _fonte):
    # 1. Montar o DataFrame de entrada
    df_input = pd.DataFrame({
        "consumo_kwh": [_consumo],
        "mes": [_mes],
        "estado": [_estado],
        "setor": [_setor],
        "fonte_energia": [_fonte],
        "season": [get_season(_mes)]  # ✅ Corrigido: usa a estação correta baseada no mês
    })

    # 2. Acessar componentes do Pipeline
    preprocessor = _model.named_steps['preprocessor']
    regressor    = _model.named_steps['regressor']
    
    # 3. TRANSFORMAÇÃO ROBUSTA (Resolve o ValueError)
    x_transformed = preprocessor.transform(df_input)
    
    # Se o preprocessor retornar uma matriz esparsa (comum no OneHotEncoder), converte para densa
    if hasattr(x_transformed, "toarray"):
        x_transformed = x_transformed.toarray()
    
    # Agora sim, converte para float para o SHAP
    x_transformed = x_transformed.astype(float)

    # 4. Cálculo do SHAP
    explainer = shap.TreeExplainer(regressor)
    shap_vals = explainer.shap_values(x_transformed)
    
    # Tratamento de retorno
    expected_value = explainer.expected_value
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = expected_value[0]

    feature_names = preprocessor.get_feature_names_out()
    
    return shap_vals[0], expected_value, x_transformed[0], feature_names# ── Dark Mode Toggle ───────────────────────────────────────────────────────────
# Criar layout otimizado para o topo
col_logo, col_title, col_stats, col_toggle = st.columns([0.8, 2.5, 3.2, 1.5])

with col_logo:
    st.markdown("""
    <div style="text-align: center; padding-top: 0.3rem;">
        <div style="font-size: 3.5rem; line-height: 1;">🌿</div>
    </div>
    """, unsafe_allow_html=True)

with col_title:
    title_color = THEME_COLORS["text_primary"]
    subtitle_color = THEME_COLORS["text_secondary"]
    st.markdown(f"""
    <div style="padding-top: 0.5rem;">
        <h1 style="margin: 0; font-size: 1.8rem; color: {title_color}; font-weight: 700;">
            Carbon Footprint Analysis
        </h1>
        <p style="margin: 0; font-size: 0.85rem; color: {subtitle_color}; margin-top: 0.2rem;">
            Estimativa Inteligente de Emissões de CO₂
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_stats:
    st.markdown("""
    <div style="padding-top: 0.7rem; text-align: right;">
        <span class="badge badge-success" style="font-size: 0.75rem;">✓ R² = 0.9948</span>
        <span class="badge badge-info" style="font-size: 0.75rem;">⚡ < 50ms</span>
        <span class="badge badge-success" style="font-size: 0.75rem;">🌱 CRISP-DM</span>
    </div>
    """, unsafe_allow_html=True)

with col_toggle:
    st.markdown("<div style='padding-top: 0.3rem;'></div>", unsafe_allow_html=True)
    # Ícone baseado no tema atual
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    theme_label = "Dark" if not st.session_state.dark_mode else "Light"
    
    if st.button(f"{theme_icon} {theme_label}", key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

# Separador visual elegante
st.markdown(f"""
<div style="height: 2px; background: linear-gradient(90deg, 
    transparent 0%, 
    {THEME_COLORS["accent_primary"]} 20%, 
    {THEME_COLORS["accent_secondary"]} 50%, 
    {THEME_COLORS["accent_primary"]} 80%, 
    transparent 100%); 
    margin: 1rem 0 2rem 0; 
    border-radius: 2px;">
</div>
""", unsafe_allow_html=True)

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
        # Logo e branding (adaptado ao tema) - COMPACTO
        logo_bg = "white" if not st.session_state.dark_mode else "#262C38"
        logo_border = "none" if not st.session_state.dark_mode else "2px solid #2E7D32"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem; background: {logo_bg}; border: {logo_border}; border-radius: 8px; margin-bottom: 0.5rem;">
            <div style="font-size: 2.5rem; line-height: 1;">🌿</div>
            <h2 style="color: #2E7D32; margin: 0; font-size: 1.1rem; font-weight: 700;">Carbon</h2>
            <h3 style="color: #66BB6A; margin: 0; font-size: 0.95rem; font-weight: 600;">Footprint</h3>
            <p style="color: #666; font-size: 0.65rem; margin-top: 0.2rem; margin-bottom: 0;">
                Análise de Emissões
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.3rem 0;'></div>", unsafe_allow_html=True)
        
        # Título Parâmetros mais compacto
        st.markdown("""
        <h3 style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: 600;">Parâmetros</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.3rem 0;'></div>", unsafe_allow_html=True)
        
        consumo = st.number_input("Consumo (kWh)", 
                                   min_value=MIN_CONSUMO_KWH, 
                                   max_value=MAX_CONSUMO_KWH,
                                   value=DEFAULT_CONSUMO_KWH, 
                                   step=STEP_CONSUMO_KWH,
                                   label_visibility="visible")
        estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"))
        setor   = st.selectbox("Setor", SETORES)
        fonte   = st.selectbox("Fonte de energia", FONTES)
        mes     = st.slider("Mês", 1, 12, 6, format="%d")
        
        # Info compacta da estação
        st.markdown(f"""
        <p style="font-size: 0.75rem; color: #666; margin: 0.3rem 0;">
            <strong>Estação:</strong> {get_season(mes)} · <strong>Mês:</strong> {MESES_LABEL[mes]}
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
        
        run = st.button("🔍 Calcular", use_container_width=True, type="primary")

    if "results" not in st.session_state or run:
        elec     = predict_all_sources(consumo, mes, estado, setor)
        fuels    = liquid_fuel_emissions(consumo)
        co2_sel  = elec[fonte]
        combined = {**elec, **fuels}
        ranking  = dict(sorted(combined.items(), key=lambda x: x[1]))
        hydro    = elec["hidrelétrica"]
        ranking_pct = {
            src: {
                "co2": v, 
                "vs_hydro_%": round(safe_division(v - hydro, hydro, 0) * 100, 1)
            }
            for src, v in ranking.items()
        }
        st.session_state["results"] = {
            "co2_sel": co2_sel, "elec": elec, "fuels": fuels,
            "combined": combined, "ranking": ranking_pct,
            "consumo": consumo, "fonte": fonte,
            "estado": estado, "setor": setor, "mes": mes,
        }

    # Verificação de session_state
    if "results" not in st.session_state:
        st.warning("⚠️ Configure os parâmetros na sidebar e clique em 'Calcular'")
        st.stop()
    
    r = st.session_state["results"]
    best_src   = min(r["elec"], key=r["elec"].get)
    best_co2   = r["elec"][best_src]
    saving     = round(r["co2_sel"] - best_co2, 2)
    saving_pct = round(safe_division(saving, r["co2_sel"], 0) * 100, 1)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🏭 Emissão atual", f"{r['co2_sel']:,.1f} kg CO₂", help=f"Fonte: {r['fonte']}")
    k2.metric("💧 Menor emissão", f"{best_co2:,.1f} kg CO₂",
              delta=f"-{saving_pct}% vs atual" if saving > 0 else "✅ Já é a melhor",
              delta_color="inverse", help=f"Fonte: {best_src}")
    k3.metric("⚡ Consumo", f"{r['consumo']:,.0f} kWh", help=f"Setor: {r['setor']}")
    k4.metric("📅 Período", f"{get_season(r['mes'])}", help=f"{MESES_LABEL[r['mes']]} · {r['estado']}")
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
        fig_bar = apply_chart_style(fig_bar)
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

    # Card de insight
    if saving > 0:
        st.markdown(create_insight_card(
            "� Oportunidade de Economia",
            f"Trocando de <strong>{r['fonte']}</strong> para <strong>{best_src}</strong>, "
            f"a emissão cai de <strong>{r['co2_sel']:,.1f} kg</strong> para "
            f"<strong>{best_co2:,.1f} kg CO₂</strong> — redução de <strong>{saving_pct}%</strong> "
            f"({saving:,.1f} kg CO₂ economizados por mês).",
            "success"
        ), unsafe_allow_html=True)
    else:
        st.markdown(create_insight_card(
            "✅ Parabéns!",
            f"<strong>{r['fonte'].capitalize()}</strong> já é a fonte com menor emissão entre as elétricas! "
            f"Você está fazendo uma escolha sustentável.",
            "success"
        ), unsafe_allow_html=True)

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
        a_consumo = st.number_input("Consumo (kWh)", 
                                     min_value=MIN_CONSUMO_KWH, 
                                     max_value=MAX_CONSUMO_KWH,
                                     value=10_000.0, 
                                     step=STEP_CONSUMO_KWH, 
                                     key="a_cons")
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
        b_consumo = st.number_input("Consumo (kWh)", 
                                     min_value=MIN_CONSUMO_KWH, 
                                     max_value=MAX_CONSUMO_KWH,
                                     value=10_000.0, 
                                     step=STEP_CONSUMO_KWH, 
                                     key="b_cons")
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
        g_consumo = st.number_input("Consumo (kWh)", 
                                     min_value=MIN_CONSUMO_KWH, 
                                     max_value=MAX_CONSUMO_KWH,
                                     value=DEFAULT_CONSUMO_KWH, 
                                     step=STEP_CONSUMO_KWH, 
                                     key="g_cons")
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

        # Otimização: criar DataFrame com todas as combinações e predizer em lote
        with st.spinner("Calculando todas as combinações..."):
            combinacoes = []
            for src in FONTES:
                for m in range(1, 13):
                    combinacoes.append({
                        "consumo_kwh": g_consumo,
                        "mes": m,
                        "estado": g_estado,
                        "setor": g_setor,
                        "fonte_energia": src,
                    })
            
            df_combinacoes = pd.DataFrame(combinacoes)
            predicoes = predict_batch(df_combinacoes)
            df_combinacoes["co2"] = predicoes
            
            resultados = []
            for idx, row in df_combinacoes.iterrows():
                co2 = row["co2"]
                reducao = round(safe_division(co2_atual - co2, co2_atual, 0) * 100, 1)
                resultados.append({
                    "Fonte": row["fonte_energia"], 
                    "Mês": MESES_LABEL[row["mes"]], 
                    "Mês Num": row["mes"],
                    "CO₂ (kg)": round(co2, 2), 
                    "Redução (%)": reducao,
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
                    # Usar predição em lote (mais eficiente)
                    predicoes = predict_batch(df_up[["consumo_kwh", "mes", "estado", "setor", "fonte_energia"]])
                    df_up["emissao_co2_estimada"] = predicoes

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
        sh_consumo = st.number_input("Consumo (kWh)", 
                                      min_value=MIN_CONSUMO_KWH, 
                                      max_value=MAX_CONSUMO_KWH,
                                      value=DEFAULT_CONSUMO_KWH, 
                                      step=STEP_CONSUMO_KWH, 
                                      key="sh_cons")
        sh_estado  = st.selectbox("Estado", ESTADOS, index=ESTADOS.index("SP"), key="sh_est")
        sh_setor   = st.selectbox("Setor", SETORES, key="sh_set")
    with sh2:
        sh_fonte = st.selectbox("Fonte de energia", FONTES, key="sh_fon")
        sh_mes   = st.slider("Mês", 1, 12, 6, key="sh_mes", format="%d")
        st.caption(f"Estação: **{get_season(sh_mes)}**")

    st.markdown("---")
    if st.button("🧠 Explicar predição", type="primary", use_container_width=True):
        with st.spinner("Calculando explicabilidade SHAP..."):
            co2_pred = predict_one(sh_consumo, sh_mes, sh_estado, sh_setor, sh_fonte)
            
            try:
                shap_row, expected_val, x_row, feat_names = compute_shap(
                    model, sh_consumo, sh_mes, sh_estado, sh_setor, sh_fonte
                )
                st.session_state["shap_result"] = {
                    "co2_pred": co2_pred, "shap_row": shap_row,
                    "expected_val": expected_val, "x_row": x_row,
                    "feat_names": feat_names,
                    "label": f"{sh_fonte} · {MESES_LABEL[sh_mes]} · {sh_estado} · {sh_setor}",
                }
            except Exception as e:
                st.error(f"❌ Erro ao calcular SHAP: {str(e)}")
                st.info("Tente com outros parâmetros ou verifique se o modelo está carregado corretamente.")

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

# ── Footer Profissional ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class="footer fade-in">
    <p style="font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600; color: #2E7D32;">
        🌿 Carbon Footprint Analysis
    </p>
    <p style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">
        Desenvolvido com ❤️ usando <strong>Streamlit</strong> e <strong>Machine Learning</strong>
    </p>
    <p style="font-size: 0.85rem; color: #999;">
        Modelo: Random Forest (R² = 0.9948) | 
        Metodologia: CRISP-DM | 
        Dados: EPE & ANEEL
    </p>
    <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
        🌱 Contribuindo para um futuro mais sustentável
    </p>
</div>
""", unsafe_allow_html=True)

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
        t_consumo = st.number_input("Consumo (kWh)", 
                                     min_value=MIN_CONSUMO_KWH, 
                                     max_value=MAX_CONSUMO_KWH,
                                     value=DEFAULT_CONSUMO_KWH, 
                                     step=STEP_CONSUMO_KWH, 
                                     key="t_cons")
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
        pct_energia     = round(safe_division(co2_energia, co2_total, 0) * 100, 1)
        pct_transporte  = round(safe_division(co2_transporte, co2_total, 0) * 100, 1)

        st.session_state["pegada_total"] = {
            "co2_energia": co2_energia, "co2_transporte": co2_transporte,
            "co2_total": co2_total, "pct_energia": pct_energia,
            "pct_transporte": pct_transporte, "modal": modal_sel,
            "km": t_km, "consumo": t_consumo, "fonte": t_fonte,
            "estado": t_estado, "setor": t_setor, "mes": t_mes,
        }

    if "pegada_total" in st.session_state:
        pt = st.session_state["pegada_total"]

        # 1. Primeiro o Título e a Linha (Isso fica fixo no topo)
        st.title("🌿 Análise de Pegada de Carbono")
        st.markdown("---")

        # 2. Depois o Resumo de Impacto (Cards de Métricas)
        st.markdown("### Resumo de Impacto")
        c1, c2, c3 = st.columns(3)
        c1.metric("Emissão Energia", f"{pt['co2_energia']:,.1f} kg CO₂")
        c2.metric("Emissão Transporte", f"{pt['co2_transporte']:,.1f} kg CO₂")
        c3.metric("Pegada Total", f"{pt['co2_total']:,.1f} kg CO₂", delta_color="inverse")

        st.markdown("---")

        # 3. Só agora as Tabs (O conteúdo que muda)
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard Geral", "🚗 Detalhe Transporte", "🔍 Explicabilidade (SHAP)"])

        with tab1:
            # REMOVIDO o st.title daqui de dentro
            st.subheader("Distribuição por Fonte de Energia")
            
            c1, c2 = st.columns(2)

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
            st.markdown("#### Emissão por Escopo")
            df_bar_escopo = pd.DataFrame([
                {"Escopo": "Energia", "CO₂ (kg)": pt["co2_energia"]},
                {"Escopo": "Transporte", "CO₂ (kg)": pt["co2_transporte"]},
            ])
            fig_bar_escopo = px.bar(df_bar_escopo, x="Escopo", y="CO₂ (kg)",
                                    color="Escopo",
                                    color_discrete_sequence=["#2196F3", "#FF9800"],
                                    text="CO₂ (kg)", template="plotly_white")
            fig_bar_escopo.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
            fig_bar_escopo.update_layout(showlegend=False, height=320,
                                         margin=dict(l=0, r=0, t=10, b=10))
            st.plotly_chart(fig_bar_escopo, use_container_width=True)

        with tab2:
            st.subheader("Detalhamento do Transporte")
            
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
                fig_mod.update_layout(showlegend=False, height=400,
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
                reducao_pct = round(safe_division(saving_transport, pt["co2_total"], 0) * 100, 1)
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
            st.markdown("#### 📋 Tabela de fatores de emissão por modal")
            df_ref = pd.DataFrame([
                {"Modal": TRANSPORT_LABELS[m],
                 "Fator (kg CO₂/km)": f,
                 "Emissão p/ 500km (kg)": round(f * 500, 1),
                 "Fonte": "IPCC AR6 / CETESB 2023"}
                for m, f in TRANSPORT_FACTORS.items()
            ])
            st.dataframe(df_ref, use_container_width=True, hide_index=True)

        with tab3:
            st.subheader("Explicabilidade SHAP - Em Desenvolvimento")
            st.info("Esta seção mostrará a análise SHAP da pegada total em breve.")

