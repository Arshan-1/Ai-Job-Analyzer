import pandas as pd
import streamlit as st
import plotly.express as px

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="Job Market Analyzer",
    page_icon="📊",
    layout="wide"
)

# ── LOAD DATA ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_jobs.csv")
        df = df[(df['normalized_salary'] == 0) | (df['normalized_salary'] < 600000)]
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# ── HEADER ────────────────────────────────────────────────
st.title("📊 Job Market Analyzer")
st.markdown("Insights from **123,000+ real job postings** — powered by LinkedIn data")
st.divider()

# ── TOP METRICS ───────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
salary_df = df[df['normalized_salary'] > 0]

col1.metric("Total Job Postings", f"{len(df):,}")
col2.metric("Avg Salary", f"${salary_df['normalized_salary'].mean():,.0f}")
col3.metric("Median Salary", f"${salary_df['normalized_salary'].median():,.0f}")
col4.metric("Remote Jobs", f"{(df['remote_allowed'] == 'Remote').sum():,}")

st.divider()

# ── ROW 1: TOP TITLES + WORK TYPE ─────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🏆 Top 20 Job Titles")
    top_titles = df['title'].value_counts().head(20).reset_index()
    top_titles.columns = ['Job Title', 'Count']
    fig = px.bar(
        top_titles, x='Count', y='Job Title',
        orientation='h', color='Count',
        color_continuous_scale='Blues'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⏰ Work Type")
    work_counts = df['formatted_work_type'].value_counts().reset_index()
    work_counts.columns = ['Work Type', 'Count']
    fig2 = px.pie(work_counts, names='Work Type', values='Count', hole=0.4)
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)

# ── ROW 2: EXPERIENCE LEVEL + REMOTE ──────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Experience Level Breakdown")
    exp = df['formatted_experience_level'].value_counts().reset_index()
    exp.columns = ['Level', 'Count']
    fig3 = px.bar(exp, x='Level', y='Count', color='Count', color_continuous_scale='Teal')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🌍 Remote vs On-site")
    remote = df['remote_allowed'].value_counts().reset_index()
    remote.columns = ['Type', 'Count']
    fig4 = px.pie(remote, names='Type', values='Count', hole=0.4,
                  color_discrete_map={'Remote': '#00CC96', 'On-site': '#636EFA'})
    st.plotly_chart(fig4, use_container_width=True)

# ── ROW 3: SALARY DISTRIBUTION ────────────────────────────
st.subheader("💰 Salary Distribution")
salary_df = df[(df['normalized_salary'] > 20000) & (df['normalized_salary'] < 400000)]
fig5 = px.histogram(
    salary_df, x='normalized_salary', nbins=60,
    labels={'normalized_salary': 'Annual Salary (USD)'},
    color_discrete_sequence=['#636EFA']
)
fig5.update_layout(bargap=0.1)
st.plotly_chart(fig5, use_container_width=True)

# ── ROW 4: TOP COMPANIES ──────────────────────────────────
st.subheader("🏢 Top 15 Hiring Companies")
top_companies = df['company_name'].value_counts().head(15).reset_index()
top_companies.columns = ['Company', 'Postings']
fig6 = px.bar(
    top_companies, x='Postings', y='Company',
    orientation='h', color='Postings',
    color_continuous_scale='Purples'
)
fig6.update_layout(yaxis={'categoryorder': 'total ascending'}, height=450)
st.plotly_chart(fig6, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit · Data from LinkedIn Job Postings (Kaggle) · AI Analyst powered by Mistral")

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# ── AI CHATBOT ────────────────────────────────────────────
st.divider()
st.subheader("🤖 Ask the AI Analyst")
st.markdown("Ask anything about this job market data — powered by Mistral (local via Ollama)")

# Build a data summary to give the LLM context
@st.cache_data
def get_data_summary(df):
    salary_df = df[(df['normalized_salary'] > 20000) & (df['normalized_salary'] < 400000)]
    top_titles = df['title'].value_counts().head(10)
    top_companies = df['company_name'].value_counts().head(10)
    exp_levels = df['formatted_experience_level'].value_counts()
    work_types = df['formatted_work_type'].value_counts()
    remote_counts = df['remote_allowed'].value_counts()

    def format_counts(series):
        return "\n".join(f"  - {name}: {count:,}" for name, count in series.items())

    return f"""You are a job market analyst. Here is the dataset summary you have access to:

- Total job postings: {len(df):,}
- Average salary: ${salary_df['normalized_salary'].mean():,.0f}
- Median salary: ${salary_df['normalized_salary'].median():,.0f}

Top 10 job titles:
{format_counts(top_titles)}

Top 10 hiring companies:
{format_counts(top_companies)}

Experience levels:
{format_counts(exp_levels)}

Work types:
{format_counts(work_types)}

Remote vs On-site:
{format_counts(remote_counts)}

Answer questions based only on this data. Be concise, friendly and insightful.
When relevant, mention specific numbers from the data."""

data_summary = get_data_summary(df)

# Chat history stored in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("e.g. What is the average salary? Which companies hire the most?"):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call LangChain + Mistral (local, free)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                llm = OllamaLLM(model="mistral")

                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", data_summary),
                    ("human", "{question}")
                ])

                chain = prompt_template | llm

                reply = chain.invoke({"question": prompt})

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"LangChain error: {e}")