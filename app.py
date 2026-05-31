```python
# =============================================================================
# PROJETO G2 — TEMA 4: Evolução do Desemprego no Brasil (2015–2024)
# Dashboard Streamlit — app.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Desemprego no Brasil | Projeto G2",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTILO CSS CUSTOMIZADO 
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Cabeçalho Principal */
        .main-title {
            font-size: 3.2rem;
            font-weight: 800;
            color: #4A148C;
            margin-bottom: 0.1rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            letter-spacing: -0.02em;
        }
        .sub-title {
            font-size: 1.1rem;
            color: #7B1FA2;
            margin-bottom: 2rem;
        }
        /* KPI Cards */
        .kpi-container {
            background: linear-gradient(135deg, #4A148C 0%, #7B1FA2 100%);
            border-radius: 14px;
            padding: 20px 22px;
            color: white;
            text-align: center;
            box-shadow: 0 6px 16px rgba(123, 31, 162, 0.2);
            transition: transform 0.2s;
        }
        .kpi-container:hover {
            transform: translateY(-2px);
        }
        .kpi-value {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 6px 0 2px;
            color: #FFFFFF;
        }
        .kpi-label {
            font-size: 0.8rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
        }
        .kpi-sub {
            font-size: 0.85rem;
            opacity: 0.85;
            margin-top: 4px;
        }
        /* Seções */
        .section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: #4A148C;
            border-left: 5px solid #9C27B0;
            padding-left: 12px;
            margin: 35px 0 15px;
        }
        /* Caixas de interpretação */
        .insight-box {
            background: #F3E5F5;
            border-left: 4px solid #8E24AA;
            border-radius: 0 10px 10px 0;
            padding: 14px 18px;
            font-size: 0.95rem;
            color: #4A148C;
            margin-top: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        .insight-box b { color: #4A148C; }
        /* Rodapé */
        .footer-box {
            background: #4A148C;
            color: #E1BEE7;
            border-radius: 12px;
            padding: 22px 26px;
            margin-top: 35px;
            font-size: 0.95rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        /* Alerta de risco crítico */
        .alerta-critico {
            background: #FFEBEE;
            border-left: 4px solid #C62828;
            border-radius: 0 8px 8px 0;
            padding: 12px 16px;
            font-size: 0.92rem;
            color: #C62828;
            margin-top: 10px;
        }
        /* Ajustes finos do Streamlit */
        .stButton>button {
            background-color: #7B1FA2;
            color: white;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #4A148C;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# CARREGAMENTO E CACHE DOS DADOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dados/simulacao_desemprego_brasil.csv")
    df["data"] = pd.to_datetime(df["data"])
    df["ano_trimestre"] = df["ano"].astype(str) + "-T" + df["trimestre"].astype(str)
    return df


df_full = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# BARRA LATERAL — FILTROS INTERATIVOS
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/color/96/bar-chart.png", width=60
)
st.sidebar.title("🎛️ Filtros Interativos")
st.sidebar.markdown("---")

# Filtro de Ano
anos_disponiveis = sorted(df_full["ano"].unique())
anos_sel = st.sidebar.multiselect(
    "📅 Ano",
    options=anos_disponiveis,
    default=anos_disponiveis,
)

# Filtro de Trimestre
trim_labels = {1: "1º Trimestre", 2: "2º Trimestre", 3: "3º Trimestre", 4: "4º Trimestre"}
trims_disponiveis = sorted(df_full["trimestre"].unique())
trims_sel = st.sidebar.multiselect(
    "🗓️ Trimestre",
    options=trims_disponiveis,
    format_func=lambda x: trim_labels[x],
    default=trims_disponiveis,
)

# Filtro de Região
regioes_disponiveis = sorted(df_full["regiao"].unique())
regioes_sel = st.sidebar.multiselect(
    "🗺️ Região",
    options=regioes_disponiveis,
    default=regioes_disponiveis,
)

# Filtro de Estado
ufs_disponiveis = sorted(df_full[df_full["regiao"].isin(regioes_sel)]["uf"].unique())
ufs_sel = st.sidebar.multiselect(
    "📍 Estado (UF)",
    options=ufs_disponiveis,
    default=ufs_disponiveis,
)

# Filtro de Setor
setores_disponiveis = sorted(df_full["setor_predominante"].unique())
setores_sel = st.sidebar.multiselect(
    "🏭 Setor Econômico",
    options=setores_disponiveis,
    default=setores_disponiveis,
)

# Filtro de Nível de Risco
niveis_ordem = ["Baixo", "Médio", "Alto", "Crítico"]
niveis_disponiveis = [n for n in niveis_ordem if n in df_full["nivel_risco"].unique()]
niveis_sel = st.sidebar.multiselect(
    "⚠️ Nível de Risco",
    options=niveis_disponiveis,
    default=niveis_disponiveis,
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Use os filtros acima para segmentar a análise por período, região, "
    "estado, setor ou nível de risco."
)

# ─────────────────────────────────────────────────────────────────────────────
# APLICAÇÃO DOS FILTROS
# ─────────────────────────────────────────────────────────────────────────────
df = df_full[
    df_full["ano"].isin(anos_sel)
    & df_full["trimestre"].isin(trims_sel)
    & df_full["regiao"].isin(regioes_sel)
    & df_full["uf"].isin(ufs_sel)
    & df_full["setor_predominante"].isin(setores_sel)
    & df_full["nivel_risco"].isin(niveis_sel)
].copy()

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# CABEÇALHO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<p class="main-title">📊 Evolução do Desemprego no Brasil — 2015 a 2024</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Dashboard analítico interativo | Projeto G2 — Tema 4 | '
    f'Exibindo <b>{len(df):,}</b> registros filtrados de <b>{len(df_full):,}</b> totais</p>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    > O desemprego é um dos principais termômetros da saúde econômica de um país.
    > Este painel permite investigar a evolução das taxas de desemprego no Brasil,
    > identificar regiões e estados mais vulneráveis, analisar a relação com inflação e renda,
    > e compreender padrões sazonais entre 2015 e 2024.
    """
)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs — INDICADORES-CHAVE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🔑 Indicadores-Chave de Desempenho (KPIs)</p>', unsafe_allow_html=True)

# Cálculos dos KPIs
taxa_media = df["taxa_desemprego"].mean()
total_desempregados = df["desempregados"].sum()
uf_maior = df.groupby("uf")["taxa_desemprego"].mean().idxmax()
taxa_uf_maior = df.groupby("uf")["taxa_desemprego"].mean().max()
regiao_mais_afetada = df.groupby("regiao")["taxa_desemprego"].mean().idxmax()
taxa_regiao = df.groupby("regiao")["taxa_desemprego"].mean().max()
renda_media_nacional = df["renda_media"].mean()
vagas_total = df["vagas_formais"].sum()

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        f"""<div class="kpi-container">
            <div class="kpi-label">Taxa Média de Desemprego</div>
            <div class="kpi-value">{taxa_media:.1f}%</div>
            <div class="kpi-sub">Média do período filtrado</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""<div class="kpi-container">
            <div class="kpi-label">Total de Desempregados</div>
            <div class="kpi-value">{total_desempregados/1e6:.1f}M</div>
            <div class="kpi-sub">Soma acumulada</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""<div class="kpi-container">
            <div class="kpi-label">Estado Mais Afetado</div>
            <div class="kpi-value">{uf_maior}</div>
            <div class="kpi-sub">Taxa média: {taxa_uf_maior:.1f}%</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""<div class="kpi-container">
            <div class="kpi-label">Região Mais Afetada</div>
            <div class="kpi-value">{regiao_mais_afetada}</div>
            <div class="kpi-sub">Taxa média: {taxa_regiao:.1f}%</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        f"""<div class="kpi-container">
            <div class="kpi-label">Renda Média Nacional</div>
            <div class="kpi-value">R$ {renda_media_nacional:,.0f}</div>
            <div class="kpi-sub">Média mensal (período filtrado)</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col6:
    st.markdown(
        f"""<div class="kpi-container">
            <div class="kpi-label">Vagas Formais Geradas</div>
            <div class="kpi-value">{vagas_total/1e6:.1f}M</div>
            <div class="kpi-sub">Total do período filtrado</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. EVOLUÇÃO TEMPORAL DO DESEMPREGO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📈 1. Evolução Temporal da Taxa de Desemprego</p>', unsafe_allow_html=True)

col_g1, col_g2 = st.columns([3, 2])

with col_g1:
    # Linha temporal por ano/trimestre (média nacional)
    df_temporal = (
        df.groupby(["ano", "trimestre"])
        .agg(taxa_media=("taxa_desemprego", "mean"))
        .reset_index()
    )
    df_temporal["periodo"] = df_temporal["ano"].astype(str) + "-T" + df_temporal["trimestre"].astype(str)
    df_temporal = df_temporal.sort_values(["ano", "trimestre"])

    fig_linha = px.line(
        df_temporal,
        x="periodo",
        y="taxa_media",
        markers=True,
        labels={"periodo": "Período", "taxa_media": "Taxa de Desemprego (%)"},
        title="Taxa Média de Desemprego — Brasil (por trimestre)",
        color_discrete_sequence=["#7B1FA2"],
    )
    fig_linha.update_traces(line_width=2.5, marker_size=7)
    fig_linha.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=14,
        height=380,
    )
    fig_linha.add_hline(
        y=df_temporal["taxa_media"].mean(),
        line_dash="dash",
        line_color="#E91E63",
        annotation_text=f"Média: {df_temporal['taxa_media'].mean():.1f}%",
        annotation_position="top left",
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col_g2:
    # Evolução por região ao longo dos anos
    df_reg_ano = (
        df.groupby(["ano", "regiao"])
        .agg(taxa_media=("taxa_desemprego", "mean"))
        .reset_index()
    )
    fig_reg_linha = px.line(
        df_reg_ano,
        x="ano",
        y="taxa_media",
        color="regiao",
        markers=True,
        labels={"ano": "Ano", "taxa_media": "Taxa (%)", "regiao": "Região"},
        title="Taxa de Desemprego por Região (anual)",
        color_discrete_sequence=px.colors.sequential.Aquadro if hasattr(px.colors.sequential, 'Aquadro') else ["#4A148C", "#7B1FA2", "#9C27B0", "#BA68C8", "#E1BEE7"]
    )
    fig_reg_linha.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=380,
        title_font_size=14,
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
    )
    st.plotly_chart(fig_reg_linha, use_container_width=True)

st.markdown(
    """<div class="insight-box">
    📌 <b>Interpretação:</b> A taxa de desemprego nacional atingiu seu pico em 2017–2018, 
    reflexo da recessão econômica iniciada em 2015. A partir de 2019, observa-se tendência 
    de queda interrompida pela pandemia de COVID-19 em 2020. As regiões Norte e Nordeste 
    historicamente apresentam taxas mais elevadas que Sul e Sudeste, evidenciando a 
    desigualdade estrutural do mercado de trabalho brasileiro.
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. COMPARAÇÃO REGIONAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🗺️ 2. Comparação entre Regiões</p>', unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    df_regiao = (
        df.groupby("regiao")
        .agg(
            taxa_media=("taxa_desemprego", "mean"),
            total_desempregados=("desempregados", "sum"),
            renda_media=("renda_media", "mean"),
        )
        .reset_index()
        .sort_values("taxa_media", ascending=False)
    )

    # Cores personalizadas na paleta roxa/magenta/vinho para as regiões
    cores_regioes = {
        "Norte": "#4A148C",
        "Nordeste": "#7B1FA2",
        "Centro-Oeste": "#9C27B0",
        "Sudeste": "#BA68C8",
        "Sul": "#E1BEE7",
    }

    fig_bar_regiao = px.bar(
        df_regiao,
        x="regiao",
        y="taxa_media",
        color="regiao",
        color_discrete_map=cores_regioes,
        text="taxa_media",
        labels={"regiao": "Região", "taxa_media": "Taxa Média (%)"},
        title="Taxa Média de Desemprego por Região",
    )
    fig_bar_regiao.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar_regiao.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=380,
        title_font_size=14,
        yaxis=dict(range=[0, df_regiao["taxa_media"].max() * 1.25]),
    )
    st.plotly_chart(fig_bar_regiao, use_container_width=True)

with col_r2:
    # Boxplot por região
    fig_box = px.box(
        df,
        x="regiao",
        y="taxa_desemprego",
        color="regiao",
        color_discrete_map=cores_regioes,
        labels={"regiao": "Região", "taxa_desemprego": "Taxa de Desemprego (%)"},
        title="Distribuição da Taxa de Desemprego por Região",
    )
    fig_box.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=380,
        title_font_size=14,
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown(
    """<div class="insight-box">
    📌 <b>Interpretação:</b> Norte e Nordeste concentram as maiores taxas médias de desemprego, 
    associadas a menor diversificação econômica e infraestrutura produtiva. 
    A região Sul apresenta consistentemente as menores taxas, sustentada por um sector industrial 
    e agroindustrial mais robusto. A dispersão elevada no Nordeste revela heterogeneidade interna 
    significativa entre seus estados.
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. COMPARAÇÃO ENTRE ESTADOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📍 3. Ranking e Comparação entre Estados</p>', unsafe_allow_html=True)

col_e1, col_e2 = st.columns([3, 2])

with col_e1:
    df_uf = (
        df.groupby(["uf", "regiao"])
        .agg(taxa_media=("taxa_desemprego", "mean"))
        .reset_index()
        .sort_values("taxa_media", ascending=True)
    )

    fig_bar_uf = px.bar(
        df_uf,
        x="taxa_media",
        y="uf",
        color="regiao",
        color_discrete_map=cores_regioes,
        orientation="h",
        text="taxa_media",
        labels={"uf": "Estado", "taxa_media": "Taxa Média (%)", "regiao": "Região"},
        title="Ranking de Desemprego por Estado (média do período)",
    )
    fig_bar_uf.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar_uf.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=520,
        title_font_size=14,
        xaxis=dict(range=[0, df_uf["taxa_media"].max() * 1.22]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22),
    )
    st.plotly_chart(fig_bar_uf, use_container_width=True)

with col_e2:
    # Top 5 mais críticos e top 5 melhores
    df_uf_rank = df_uf.sort_values("taxa_media", ascending=False)
    st.markdown("**🔴 Top 5 — Maior Desemprego**")
    top5_criticos = df_uf_rank.head(5)[["uf", "regiao", "taxa_media"]].copy()
    top5_criticos.columns = ["UF", "Região", "Taxa Média (%)"]
    top5_criticos["Taxa Média (%)"] = top5_criticos["Taxa Média (%)"].map("{:.1f}%".format)
    st.dataframe(top5_criticos, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🟢 Top 5 — Menor Desemprego**")
    top5_melhores = df_uf_rank.tail(5)[["uf", "regiao", "taxa_media"]].copy()
    top5_melhores = top5_melhores.sort_values("taxa_media")
    top5_melhores.columns = ["UF", "Região", "Taxa Média (%)"]
    top5_melhores["Taxa Média (%)"] = top5_melhores["Taxa Média (%)"].map("{:.1f}%".format)
    st.dataframe(top5_melhores, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pizza nível de risco com paleta degradê roxa
    df_risco = df["nivel_risco"].value_counts().reset_index()
    df_risco.columns = ["Nível de Risco", "Registros"]
    cores_risco = {"Baixo": "#E1BEE7", "Médio": "#BA68C8", "Alto": "#9C27B0", "Crítico": "#4A148C"}
    fig_pizza = px.pie(
        df_risco,
        values="Registros",
        names="Nível de Risco",
        color="Nível de Risco",
        color_discrete_map=cores_risco,
        title="Distribuição por Nível de Risco",
        hole=0.4,
    )
    fig_pizza.update_layout(height=290, title_font_size=13)
    st.plotly_chart(fig_pizza, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. HEATMAP TRIMESTRAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🗓️ 4. Heatmap — Sazonalidade Trimestral do Desemprego</p>', unsafe_allow_html=True)

df_heat = (
    df.groupby(["ano", "trimestre"])
    .agg(taxa_media=("taxa_desemprego", "mean"))
    .reset_index()
)
df_heat_pivot = df_heat.pivot(index="trimestre", columns="ano", values="taxa_media")
df_heat_pivot.index = [f"{i}º Tri" for i in df_heat_pivot.index]

fig_heat, ax = plt.subplots(figsize=(14, 3.5))
# Mudança para cmap="Purples" condizente com o novo visual
sns.heatmap(
    df_heat_pivot,
    annot=True,
    fmt=".1f",
    cmap="Purples",
    linewidths=0.5,
    ax=ax,
    cbar_kws={"label": "Taxa (%)"},
    annot_kws={"size": 11},
)
ax.set_title("Taxa Média de Desemprego por Trimestre e Ano (%)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Ano", fontsize=11)
ax.set_ylabel("Trimestre", fontsize=11)
plt.tight_layout()
st.pyplot(fig_heat)
plt.close()

st.markdown(
    """<div class="insight-box">
    📌 <b>Interpretação:</b> O heatmap revela sazonalidade clara: o 1º trimestre (jan–mar) 
    tende a exibir taxas levemente mais altas, reflexo das demissões pós-festas e recomposição 
    do mercado. O pico histórico ocorre entre 2016 e 2018. A trajetória de queda a partir de 
    2019 é visível, com interrupção em 2020 (COVID-19) e retomada nos anos seguintes.
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 5. DISPERSÃO — RENDA × DESEMPREGO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">💰 5. Relação entre Renda Média e Taxa de Desemprego</p>', unsafe_allow_html=True)

col_d1, col_d2 = st.columns([3, 2])

with col_d1:
    fig_scatter = px.scatter(
        df,
        x="renda_media",
        y="taxa_desemprego",
        color="regiao",
        size="desempregados",
        hover_data=["uf", "ano", "trimestre", "setor_predominante"],
        color_discrete_map=cores_regioes,
        labels={
            "renda_media": "Renda Média Mensal (R$)",
            "taxa_desemprego": "Taxa de Desemprego (%)",
            "regiao": "Região",
        },
        title="Dispersão: Renda Média × Taxa de Desemprego (tamanho = nº desempregados)",
        opacity=0.65,
    )
    fig_scatter.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
        title_font_size=14,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    # Linha de tendência
    z = np.polyfit(df["renda_media"], df["taxa_desemprego"], 1)
    p = np.poly1d(z)
    x_range = np.linspace(df["renda_media"].min(), df["renda_media"].max(), 100)
    fig_scatter.add_trace(
        go.Scatter(
            x=x_range,
            y=p(x_range),
            mode="lines",
            name="Tendência",
            line=dict(color="#311B92", dash="dash", width=1.5),
        )
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_d2:
    # Relação inflação × desemprego
    df_inf = (
        df.groupby("ano")
        .agg(taxa_media=("taxa_desemprego", "mean"), inflacao_media=("inflacao", "mean"))
        .reset_index()
    )
    fig_inf = make_subplots(specs=[[{"secondary_y": True}]])
    fig_inf.add_trace(
        go.Bar(
            x=df_inf["ano"],
            y=df_inf["taxa_media"],
            name="Taxa de Desemprego (%)",
            marker_color="#7B1FA2",
            opacity=0.8,
        ),
        secondary_y=False,
    )
    fig_inf.add_trace(
        go.Scatter(
            x=df_inf["ano"],
            y=df_inf["inflacao_media"],
            name="Inflação (%)",
            mode="lines+markers",
            line=dict(color="#E91E63", width=2.5),
            marker_size=8,
        ),
        secondary_y=True,
    )
    fig_inf.update_layout(
        title="Desemprego × Inflação (visão anual)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
        title_font_size=14,
        legend=dict(orientation="h", yanchor="bottom", y=-0.22),
    )
    fig_inf.update_yaxes(title_text="Taxa de Desemprego (%)", secondary_y=False)
    fig_inf.update_yaxes(title_text="Inflação (%)", secondary_y=True)
    st.plotly_chart(fig_inf, use_container_width=True)

st.markdown(
    """<div class="insight-box">
    📌 <b>Interpretação:</b> O gráfico de dispersão evidencia correlação negativa moderada entre renda 
    e desemprego: regiões com menor renda média tendem a apresentar maiores taxas. 
    A relação inflação–desemprego no Brasil é complexa: em 2015–2016 ambas as variáveis subiram 
    juntas (estagflação), enquanto a partir de 2019 a inflação caiu com o desemprego ainda elevado, 
    e em 2021–2022 a inflação voltou a subir pressionada pela recuperação pós-pandemia.
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 6. ANÁLISE POR SETOR ECONÔMICO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🏭 6. Análise por Setor Econômico</p>', unsafe_allow_html=True)

col_s1, col_s2 = st.columns(2)

with col_s1:
    df_setor = (
        df.groupby("setor_predominante")
        .agg(taxa_media=("taxa_desemprego", "mean"), renda_media=("renda_media", "mean"))
        .reset_index()
        .sort_values("taxa_media", ascending=False)
    )
    fig_setor = px.bar(
        df_setor,
        x="setor_predominante",
        y="taxa_media",
        color="setor_predominante",
        text="taxa_media",
        labels={"setor_predominante": "Setor", "taxa_media": "Taxa Média (%)"},
        title="Taxa Média de Desemprego por Setor Econômico",
        color_discrete_sequence=px.colors.sequential.Aquadro if hasattr(px.colors.sequential, 'Aquadro') else ["#4A148C", "#7B1FA2", "#9C27B0", "#BA68C8", "#E1BEE7"]
    )
    fig_setor.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_setor.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=360,
        title_font_size=14,
        yaxis=dict(range=[0, df_setor["taxa_media"].max() * 1.25]),
    )
    st.plotly_chart(fig_setor, use_container_width=True)

with col_s2:
    df_setor_ano = (
        df.groupby(["ano", "setor_predominante"])
        .agg(taxa_media=("taxa_desemprego", "mean"))
        .reset_index()
    )
    fig_setor_linha = px.line(
        df_setor_ano,
        x="ano",
        y="taxa_media",
        color="setor_predominante",
        markers=True,
        labels={"ano": "Ano", "taxa_media": "Taxa (%)", "setor_predominante": "Setor"},
        title="Evolução do Desemprego por Setor (anual)",
        color_discrete_sequence=px.colors.sequential.Aquadro if hasattr(px.colors.sequential, 'Aquadro') else ["#4A148C", "#7B1FA2", "#9C27B0", "#BA68C8", "#E1BEE7"]
    )
    fig_setor_linha.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=360,
        title_font_size=14,
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
    )
    st.plotly_chart(fig_setor_linha, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 7. ANÁLISE DA RENDA MÉDIA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">💵 7. Evolução da Renda Média</p>', unsafe_allow_html=True)

df_renda_ano = (
    df.groupby(["ano", "regiao"])
    .agg(renda_media=("renda_media", "mean"))
    .reset_index()
)

fig_renda = px.area(
    df_renda_ano,
    x="ano",
    y="renda_media",
    color="regiao",
    color_discrete_map=cores_regioes,
    labels={"ano": "Ano", "renda_media": "Renda Média (R$)", "regiao": "Região"},
    title="Evolução da Renda Média por Região (2015–2024)",
)
fig_renda.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=360,
    title_font_size=14,
    legend=dict(orientation="h", yanchor="bottom", y=-0.22),
)
st.plotly_chart(fig_renda, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 8. TABELA DINÂMICA DETALHADA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📋 8. Tabela Dinâmica — Exploração Detalhada</p>', unsafe_allow_html=True)

st.markdown("Utilize a tabela abaixo para explorar os dados filtrados em detalhe, ordenar colunas e investigar registros específicos.")

df_tabela = (
    df.groupby(["ano", "trimestre", "regiao", "uf", "setor_predominante", "nivel_risco"])
    .agg(
        taxa_media=("taxa_desemprego", "mean"),
        renda_media=("renda_media", "mean"),
        desempregados=("desempregados", "sum"),
        vagas_formais=("vagas_formais", "sum"),
        inflacao_media=("inflacao", "mean"),
    )
    .reset_index()
    .sort_values(["ano", "trimestre", "regiao", "uf"])
)

df_tabela.columns = [
    "Ano", "Trimestre", "Região", "UF", "Setor", "Nível de Risco",
    "Taxa Desemp. (%)", "Renda Média (R$)", "Desempregados", "Vagas Formais", "Inflação (%)",
]
df_tabela["Taxa Desemp. (%)"] = df_tabela["Taxa Desemp. (%)"].round(2)
df_tabela["Renda Média (R$)"] = df_tabela["Renda Média (R$)"].round(2)
df_tabela["Inflação (%)"] = df_tabela["Inflação (%)"].round(2)

st.dataframe(
    df_tabela,
    use_container_width=True,
    height=380,
    hide_index=True,
)

st.download_button(
    label="⬇️ Baixar dados filtrados (CSV)",
    data=df_tabela.to_csv(index=False).encode("utf-8"),
    file_name="desemprego_filtrado.csv",
    mime="text/csv",
)

# ─────────────────────────────────────────────────────────────────────────────
# 9. INTERPRETAÇÃO ECONÔMICA E PERÍODOS DE CRISE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🔍 9. Interpretação Econômica e Períodos de Crise</p>', unsafe_allow_html=True)

col_int1, col_int2 = st.columns(2)

with col_int1:
    # Taxa anual com marcação de crise
    df_anual = df.groupby("ano")["taxa_desemprego"].mean().reset_index()
    df_anual.columns = ["ano", "taxa_media"]

    fig_crise = go.Figure()
    fig_crise.add_trace(
        go.Scatter(
            x=df_anual["ano"],
            y=df_anual["taxa_media"],
            mode="lines+markers",
            line=dict(color="#7B1FA2", width=3),
            marker=dict(size=10),
            name="Taxa de Desemprego",
        )
    )

    # Faixas de crise e recuperação com transparências roxas/vinhos
    eventos = [
        (2015, 2016, "rgba(123,31,162,0.12)", "Crise 2015–16"),
        (2020, 2021, "rgba(74,20,140,0.12)", "Pandemia 2020"),
        (2022, 2024, "rgba(225,190,231,0.25)", "Recuperação"),
    ]
    for x0, x1, cor, rotulo in eventos:
        fig_crise.add_vrect(
            x0=x0 - 0.4,
            x1=x1 + 0.4,
            fillcolor=cor,
            opacity=1,
            layer="below",
            line_width=0,
            annotation_text=rotulo,
            annotation_position="top left",
            annotation_font_size=11,
        )

    fig_crise.update_layout(
        title="Taxa Anual com Marcação de Crises e Recuperação",
        xaxis_title="Ano",
        yaxis_title="Taxa Média (%)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=380,
        title_font_size=14,
    )
    st.plotly_chart(fig_crise, use_container_width=True)

with col_int2:
    st.markdown(
        """
        **Cronologia dos principais eventos econômicos:**

        🔴 **2015–2016 — Crise econômica** Recessão severa, ajuste fiscal, inflação alta e desemprego em ascensão.
        Taxa superou 12% na média nacional.

        📉 **2017–2019 — Lenta recuperação** Desemprego ainda elevado, mas em queda gradual. Reformas estruturais
        (trabalhista, previdenciária) iniciam recomposição do mercado.

        🦠 **2020 — Pandemia de COVID-19** Pico histórico de desemprego. Programas emergenciais (Auxílio Emergencial,
        BEm) atenuaram o impacto, mas o mercado informal foi severamente afetado.

        🟢 **2021–2024 — Recuperação e recomposição** Queda consistente da taxa de desemprego. Retomada das vagas formais,
        especialmente em Serviços e Comércio. Inflação pressionada pela recuperação
        e pela guerra na Ucrânia (2022), mas mercado de trabalho resistiu.
        """
    )

# ─────────────────────────────────────────────────────────────────────────────
# 10. CONCLUSÃO EXECUTIVA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🏁 10. Conclusão Executiva</p>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="footer-box">
    <b style="font-size:1.1rem;">📊 Síntese Analítica — Evolução do Desemprego no Brasil (2015–2024)</b><br><br>

    A análise dos dados revela um mercado de trabalho brasileiro marcado por profundas 
    desigualdades regionais e alta sensibilidade a choques econômicos. Os principais achados são:<br><br>

    ✅ <b>Desigualdade regional persistente:</b> Norte e Nordeste apresentaram taxas consistentemente 
    maiores que Sul e Sudeste, refletindo diferenças estruturais em infraestrutura, educação e 
    diversificação econômica.<br><br>

    ✅ <b>Dois grandes choques:</b> A recessão de 2015–2016 e a pandemia de 2020 foram os principais 
    eventos de disrupção, elevando o desemprego a patamares históricos.<br><br>

    ✅ <b>Recuperação real após 2021:</b> O mercado de trabalho demonstrou resiliência, com queda 
    consistente da taxa de desemprego e retomada da geração de vagas formais.<br><br>

    ✅ <b>Correlação renda–desemprego:</b> Estados com menor renda média tendem a exibir maiores 
    taxas de desemprego, reforçando o ciclo de vulnerabilidade socioeconômica.<br><br>

    ✅ <b>Sazonalidade trimestral:</b> O 1º trimestre historicamente concentra as maiores taxas, 
    padrão associado às demissões pós-período natalino.<br><br>

    <i>Taxa média no período filtrado: <b>{taxa_media:.1f}%</b> | 
    Estado mais afetado: <b>{uf_maior}</b> | 
    Região mais afetada: <b>{regiao_mais_afetada}</b> | 
    Renda média: <b>R$ {renda_media_nacional:,.0f}</b></i>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<br><center><small style='color:#aaa;'>Projeto G2 — Tema 4 | "
    "Análise de Dados com Python · Pandas · Matplotlib · Seaborn · Plotly · Streamlit</small></center>",
    unsafe_allow_html=True,
)

```
