# 📊 Evolução do Desemprego no Brasil (2015–2024)

**Projeto G2 — Tema 4 | Análise e Visualização de Dados**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75?logo=plotly)](https://plotly.com)

---

## 📋 Descrição do Projeto

Este projeto analisa a **evolução das taxas de desemprego no Brasil entre 2015 e 2024**, 
investigando tendências econômicas, desigualdades regionais, períodos de crise e recuperação, 
além da relação entre desemprego, renda e inflação.

O projeto foi desenvolvido como parte do **Projeto G2 — Tema 4**, com foco em:

- Análise exploratória de dados socioeconômicos
- Construção de dashboard interativo com Streamlit
- Visualizações dinâmicas com Plotly, Matplotlib e Seaborn
- Interpretação econômica dos resultados

---

## 🗂️ Estrutura do Projeto

```
projeto-desemprego-brasil/
│
├── app.py                          # Dashboard principal (Streamlit)
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação do projeto
├── index.html                      # Página GitHub Pages
│
├── dados/
│   └── simulacao_desemprego_brasil.csv   # Dataset principal
│
├── notebooks/
│   └── analise_desemprego.ipynb    # Análise exploratória completa
│
├── database/                       # (opcional) banco SQLite
└── imagens/                        # Capturas de tela do dashboard
```

---

## 📊 Base de Dados

| Coluna              | Tipo    | Descrição                              |
|---------------------|---------|----------------------------------------|
| `ano`               | int     | Ano da ocorrência (2015–2024)          |
| `trimestre`         | int     | Trimestre (1–4)                        |
| `data`              | date    | Data de referência                     |
| `regiao`            | str     | Região do Brasil (5 regiões)           |
| `uf`                | str     | Unidade Federativa (20 estados)        |
| `populacao_ativa`   | int     | População economicamente ativa         |
| `empregados`        | int     | Número de empregados                   |
| `desempregados`     | int     | Número de desempregados                |
| `taxa_desemprego`   | float   | Percentual de desemprego               |
| `renda_media`       | float   | Renda média mensal (R$)                |
| `setor_predominante`| str     | Principal setor econômico              |
| `vagas_formais`     | int     | Novas vagas formais abertas            |
| `inflacao`          | float   | Índice de inflação (%)                 |
| `nivel_risco`       | str     | Baixo / Médio / Alto / Crítico         |

**Total de registros:** 800 | **Período:** 2015–2024 | **Estados:** 20 | **Regiões:** 5

---

## 🚀 Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/victorialms/projeto-desemprego-brasil.git
cd projeto-desemprego-brasil
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt OU py -m pip install -r requirements.txt
```

### 4. Execute o dashboard
```bash
streamlit run app.py OU py -m streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`.

---

## 📈 Funcionalidades do Dashboard

### 🔑 KPIs Principais
- Taxa média de desemprego do período
- Total de desempregados (acumulado)
- Estado com maior taxa de desemprego
- Região mais afetada
- Renda média nacional
- Total de vagas formais geradas

### 🎛️ Filtros Interativos
- Filtro por Ano
- Filtro por Trimestre
- Filtro por Região
- Filtro por Estado (UF)
- Filtro por Setor Econômico
- Filtro por Nível de Risco

### 📊 Visualizações
| Visualização | Objetivo |
|---|---|
| Linha temporal (trimestral) | Evolução do desemprego nacional |
| Linhas por região (anual) | Comparação regional ao longo do tempo |
| Barras por região | Comparação das taxas médias regionais |
| Boxplot por região | Distribuição e outliers regionais |
| Barras por estado (ranking) | Comparação estadual ordenada |
| Gráfico de pizza | Distribuição por nível de risco |
| Heatmap trimestral | Sazonalidade e padrões temporais |
| Dispersão renda × desemprego | Correlação entre variáveis |
| Barras/Linhas desemprego × inflação | Relação macroeconômica |
| Área por região (renda) | Evolução da renda média |
| Linha anual com marcação de crises | Períodos de crise e recuperação |
| Tabela dinâmica exportável | Exploração detalhada dos dados |

---

## 🔍 Perguntas Respondidas

- ✅ Quais regiões apresentam maior desemprego?
- ✅ Quais estados apresentam menores taxas?
- ✅ Existem períodos de crise econômica mais evidentes?
- ✅ O desemprego aumentou ou diminuiu ao longo do tempo?
- ✅ Existem diferenças relevantes entre regiões?
- ✅ Há sazonalidade em determinados trimestres?
- ✅ Qual a relação entre renda, inflação e desemprego?

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **Pandas** | Manipulação e análise de dados |
| **NumPy** | Cálculos numéricos |
| **Matplotlib** | Heatmap e gráficos estáticos |
| **Seaborn** | Heatmap com anotações |
| **Plotly** | Gráficos interativos |
| **Streamlit** | Dashboard web interativo |
| **SQLAlchemy** | (disponível) Integração com banco de dados |

---

## 🌐 Links do Projeto

| Plataforma | Link |
|---|---|
| 📁 GitHub | [https://github.com/victorialms/Projeto-Desemprego-Brasil](#) |
| 🌐 GitHub Pages | [https://victorialms.github.io/Projeto-Desemprego-Brasil/](#) |
| 📊 Streamlit Cloud | [https://projeto-desemprego-brasil.streamlit.app/](#) |

---

## 📝 Principais Achados

1. **Norte e Nordeste** apresentam as maiores taxas médias de desemprego (acima de 14%)
2. **Sul** (SC, PR, RS) concentra os estados com menores taxas (abaixo de 10%)
3. **2017** foi o pico histórico de desemprego da série analisada
4. **2020** registrou segundo pico, associado à pandemia de COVID-19
5. Correlação negativa entre renda média e taxa de desemprego
6. **1º trimestre** historicamente apresenta taxas ligeiramente mais elevadas (sazonalidade)
7. Setor de **Construção** e **Comércio** concentram os maiores índices de desemprego

---

## 👨‍💻 Autor

**Projeto G2 — Tema 4**  
Disciplina: Análise de Dados com Python  
Período: 2024/2025

---

## 📄 Licença

Este projeto é de uso acadêmico. Dataset simulado para fins educacionais.
