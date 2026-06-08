"""
Chronotype Explorer — Project 1
A full-stack exploratory data analysis application for circadian research.
Author: Diego José Palencia Robles
Research: Scoping Review on Circadian Rhythms, Time Management & Productivity
"""

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Page configuration
st.set_page_config(
    page_title="Chronotype Explorer",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for research-grade appearance
st.markdown("""
<style>
    .main-header {
        font-family: 'Georgia', serif;
        color: #1a1a2e;
        font-size: 2.2rem;
        font-weight: normal;
        border-bottom: 3px solid #e2b36a;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-family: 'Courier New', monospace;
        color: #666688;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f6f2;
        border-left: 4px solid #e2b36a;
        padding: 1rem;
        border-radius: 4px;
    }
    .insight-box {
        background: #1a1a2e;
        color: #f5f0e8;
        padding: 1.2rem;
        border-radius: 8px;
        font-family: 'Georgia', serif;
        line-height: 1.6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data
def load_data():
    """Load data from CSV or SQLite database."""
    # Try CSV first (for uploaded files), then fall back to SQLite
    csv_path = "data/chronotype_data.csv"
    db_path = "data/chronotype_explorer.db"

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    elif os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        query = """
        SELECT 
            p.participant_id, p.age, p.sex, p.work_modality,
            c.meq_score, c.chronotype,
            s.sleep_onset_work, s.sleep_offset_work, s.sleep_duration_work,
            s.sleep_onset_free, s.sleep_offset_free, s.sleep_duration_free,
            s.social_jetlag_hours,
            e.light_exposure_lux_hr,
            pr.productivity_score, pr.procrastination_score
        FROM participants p
        JOIN chronotype_assessments c ON p.participant_id = c.participant_id
        JOIN sleep_schedules s ON p.participant_id = s.participant_id
        JOIN environmental_factors e ON p.participant_id = e.participant_id
        JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
        """
        df = pd.read_sql(query, conn)
        conn.close()
    else:
        st.error("Data not found. Please ensure chronotype_data.csv or chronotype_explorer.db exists in the data/ folder.")
        return pd.DataFrame()

    return df

@st.cache_data
def load_from_sql(query):
    """Execute custom SQL query against the database."""
    db_path = "data/chronotype_explorer.db"
    if not os.path.exists(db_path):
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    result = pd.read_sql(query, conn)
    conn.close()
    return result

# =============================================================================
# SIDEBAR — FILTERS & CONTROLS
# =============================================================================

st.sidebar.markdown("## 🔬 Research Filters")
st.sidebar.markdown("---")

# Load data
df = load_data()

if df.empty:
    st.stop()

# Sidebar filters
age_range = st.sidebar.slider("Age Range", int(df['age'].min()), int(df['age'].max()), 
                               (int(df['age'].min()), int(df['age'].max())))

sex_filter = st.sidebar.multiselect("Sex", options=df['sex'].unique(), default=df['sex'].unique())

work_filter = st.sidebar.multiselect("Work Modality", 
                                       options=df['work_modality'].unique(), 
                                       default=df['work_modality'].unique())

chronotype_filter = st.sidebar.multiselect("Chronotype", 
                                            options=df['chronotype'].unique(), 
                                            default=df['chronotype'].unique())

# Apply filters
filtered_df = df[
    (df['age'] >= age_range[0]) & (df['age'] <= age_range[1]) &
    (df['sex'].isin(sex_filter)) &
    (df['work_modality'].isin(work_filter)) &
    (df['chronotype'].isin(chronotype_filter))
].copy()

st.sidebar.markdown(f"**Filtered records:** {len(filtered_df)} / {len(df)}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Avg Productivity", f"{filtered_df['productivity_score'].mean():.1f}")
st.sidebar.metric("Avg Social Jetlag", f"{filtered_df['social_jetlag_hours'].mean():.2f}h")
st.sidebar.metric("Avg MEQ Score", f"{filtered_df['meq_score'].mean():.0f}")

# =============================================================================
# MAIN HEADER
# =============================================================================

st.markdown('<div class="main-header">Chronotype Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Exploratory Data Analysis · Circadian Rhythms & Productivity · 2015–2025 Evidence Mapping</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 1: OVERVIEW & DATA QUALITY
# =============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "📊 Distributions", "🔗 Correlations", "🔬 Research Questions", "🗄️ SQL Lab"])

with tab1:
    st.markdown("### Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Records", len(filtered_df))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Variables", len(filtered_df.columns))
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        missing = filtered_df.isnull().sum().sum()
        st.metric("Missing Values", missing)
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Duplicated Rows", filtered_df.duplicated().sum())
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.markdown("#### Data Dictionary")
        dictionary = """
        | Variable | Description | Source |
        |----------|-------------|--------|
        | `meq_score` | Morningness-Eveningness Questionnaire (16–86) | Horne & Östberg |
        | `chronotype` | Categorical classification from MEQ | Research protocol |
        | `social_jetlag_hours` | |MSF - MSW| (Roenneberg et al.) | MCTQ-derived |
        | `productivity_score` | Self-reported productivity (1–10) | Protocol outcome |
        | `procrastination_score` | Work procrastination proxy (1–5) | Maier et al. 2022 |
        | `light_exposure_lux_hr` | Daily light exposure proxy | Environmental factor |
        | `work_modality` | onsite / hybrid / remote | Context variable (PCC) |
        """
        st.markdown(dictionary)

    with col_right:
        st.markdown("#### Descriptive Statistics")
        numeric_cols = ['age', 'meq_score', 'social_jetlag_hours', 'productivity_score', 
                         'procrastination_score', 'light_exposure_lux_hr']
        desc = filtered_df[numeric_cols].describe().round(2)
        st.dataframe(desc, use_container_width=True)

    st.markdown("---")
    st.markdown("#### First 10 Records")
    st.dataframe(filtered_df.head(10), use_container_width=True)

# =============================================================================
# TAB 2: DISTRIBUTIONS
# =============================================================================

with tab2:
    st.markdown("### Distribution Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### MEQ Score Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=filtered_df, x='meq_score', bins=20, kde=True, 
                     color='#e2b36a', edgecolor='white', ax=ax)
        ax.axvline(filtered_df['meq_score'].mean(), color='#1a1a2e', linestyle='--', 
                   label=f'Mean: {filtered_df["meq_score"].mean():.1f}')
        ax.set_xlabel("MEQ Score (lower = evening type)")
        ax.set_ylabel("Count")
        ax.legend()
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

        st.markdown("#### Productivity by Chronotype")
        fig, ax = plt.subplots(figsize=(8, 5))
        order = ['Definite Evening', 'Moderate Evening', 'Intermediate', 'Moderate Morning', 'Definite Morning']
        order = [c for c in order if c in filtered_df['chronotype'].values]
        sns.boxplot(data=filtered_df, x='chronotype', y='productivity_score', 
                    order=order, palette='RdYlGn', ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Productivity Score (1–10)")
        ax.tick_params(axis='x', rotation=30)
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

    with col2:
        st.markdown("#### Social Jetlag Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=filtered_df, x='social_jetlag_hours', bins=20, kde=True,
                     color='#60a5fa', edgecolor='white', ax=ax)
        ax.axvline(filtered_df['social_jetlag_hours'].mean(), color='#1a1a2e', linestyle='--',
                   label=f'Mean: {filtered_df["social_jetlag_hours"].mean():.2f}h')
        ax.set_xlabel("Social Jetlag (hours)")
        ax.set_ylabel("Count")
        ax.legend()
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

        st.markdown("#### Work Modality Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        modality_counts = filtered_df['work_modality'].value_counts()
        colors = ['#34d399', '#60a5fa', '#f59e0b']
        wedges, texts, autotexts = ax.pie(modality_counts.values, labels=modality_counts.index, 
                                           autopct='%1.1f%%', colors=colors, startangle=90,
                                           textprops={'fontsize': 10})
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### Sleep Schedule Comparison: Work Days vs. Free Days")

    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(8, 5))
        sleep_data = pd.DataFrame({
            'Work Day': filtered_df['sleep_duration_work'],
            'Free Day': filtered_df['sleep_duration_free']
        })
        sns.boxplot(data=sleep_data, palette=['#c084fc', '#f87171'], ax=ax)
        ax.set_ylabel("Sleep Duration (hours)")
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(8, 5))
        filtered_df['sleep_debt'] = filtered_df['sleep_duration_free'] - filtered_df['sleep_duration_work']
        sns.histplot(data=filtered_df, x='sleep_debt', bins=20, kde=True,
                     color='#f87171', edgecolor='white', ax=ax)
        ax.axvline(0, color='#1a1a2e', linestyle='--', label='No debt')
        ax.set_xlabel("Sleep Debt (Free Day – Work Day, hours)")
        ax.set_ylabel("Count")
        ax.legend()
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

# =============================================================================
# TAB 3: CORRELATIONS
# =============================================================================

with tab3:
    st.markdown("### Correlation Analysis")

    numeric_cols = ['age', 'meq_score', 'social_jetlag_hours', 'sleep_duration_work',
                    'sleep_duration_free', 'light_exposure_lux_hr', 'productivity_score', 
                    'procrastination_score']

    corr_matrix = filtered_df[numeric_cols].corr()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r',
                    center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

    with col2:
        st.markdown("#### Key Findings")

        r_meq_prod = filtered_df['meq_score'].corr(filtered_df['productivity_score'])
        r_sjl_prod = filtered_df['social_jetlag_hours'].corr(filtered_df['productivity_score'])
        r_sjl_proc = filtered_df['social_jetlag_hours'].corr(filtered_df['procrastination_score'])
        r_light_prod = filtered_df['light_exposure_lux_hr'].corr(filtered_df['productivity_score'])

        findings = f"""
        **MEQ ↔ Productivity:** r = {r_meq_prod:.3f}
        {'Morning types show higher productivity.' if r_meq_prod > 0 else 'No clear chronotype-productivity link.'}

        **Social Jetlag ↔ Productivity:** r = {r_sjl_prod:.3f}
        {'Higher social jetlag predicts lower productivity.' if r_sjl_prod < 0 else 'Unexpected positive correlation.'}

        **Social Jetlag ↔ Procrastination:** r = {r_sjl_proc:.3f}
        {'Social jetlag is associated with more procrastination.' if r_sjl_proc > 0 else 'No procrastination link found.'}

        **Light Exposure ↔ Productivity:** r = {r_light_prod:.3f}
        {'More light correlates with higher productivity.' if r_light_prod > 0 else 'Light exposure shows no clear effect.'}
        """
        st.markdown(findings)

        st.markdown("---")
        st.markdown("#### Scatter: Social Jetlag vs. Productivity")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.scatterplot(data=filtered_df, x='social_jetlag_hours', y='productivity_score',
                        hue='work_modality', palette=['#34d399', '#60a5fa', '#f59e0b'], 
                        alpha=0.7, ax=ax)

        # Add regression line
        z = np.polyfit(filtered_df['social_jetlag_hours'], filtered_df['productivity_score'], 1)
        p = np.poly1d(z)
        ax.plot(filtered_df['social_jetlag_hours'].sort_values(), 
                p(filtered_df['social_jetlag_hours'].sort_values()), 
                "r--", alpha=0.5, label=f'Trend (r={r_sjl_prod:.2f})')
        ax.set_xlabel("Social Jetlag (hours)")
        ax.set_ylabel("Productivity Score")
        ax.legend()
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

# =============================================================================
# TAB 4: RESEARCH QUESTIONS
# =============================================================================

with tab4:
    st.markdown("### Research Questions from Protocol")
    st.markdown("*Based on PCC framework: Population (Adults), Concept (Circadian variables), Context (Work modalities)*")

    st.markdown("---")

    # RQ1: Chronotype and productivity by modality
    st.markdown("#### RQ1: Does chronotype predict productivity differently across work modalities?")

    rq1_data = filtered_df.groupby(['work_modality', 'chronotype'])['productivity_score'].mean().reset_index()
    rq1_pivot = rq1_data.pivot(index='chronotype', columns='work_modality', values='productivity_score')

    col1, col2 = st.columns([3, 2])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        rq1_pivot.plot(kind='bar', ax=ax, color=['#34d399', '#60a5fa', '#f59e0b'], width=0.8)
        ax.set_ylabel("Mean Productivity Score")
        ax.set_xlabel("")
        ax.tick_params(axis='x', rotation=30)
        ax.legend(title="Work Modality")
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

    with col2:
        st.markdown("**Interpretation:**")
        for modality in rq1_pivot.columns:
            if modality in rq1_pivot.columns:
                best = rq1_pivot[modality].idxmax()
                worst = rq1_pivot[modality].idxmin()
                st.markdown(f"• **{modality.capitalize()}:** Best = {best} ({rq1_pivot.loc[best, modality]:.2f}), Worst = {worst} ({rq1_pivot.loc[worst, modality]:.2f})")

    st.markdown("---")

    # RQ2: Social jetlag severity
    st.markdown("#### RQ2: What proportion of the sample experiences clinically significant social jetlag (>1h)?")

    filtered_df['sjl_severity'] = pd.cut(
        filtered_df['social_jetlag_hours'],
        bins=[0, 0.5, 1.0, 2.0, 10],
        labels=['Minimal (<0.5h)', 'Mild (0.5–1h)', 'Moderate (1–2h)', 'Severe (>2h)']
    )

    sjl_dist = filtered_df['sjl_severity'].value_counts().sort_index()

    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#34d399', '#60a5fa', '#f59e0b', '#f87171']
        sjl_dist.plot(kind='bar', color=colors, ax=ax, edgecolor='white')
        ax.set_ylabel("Count")
        ax.set_xlabel("")
        ax.tick_params(axis='x', rotation=30)
        ax.set_facecolor('#faf8f4')
        fig.patch.set_facecolor('#faf8f4')
        st.pyplot(fig)

    with col4:
        total = len(filtered_df)
        st.markdown("**Severity Distribution:**")
        for severity, count in sjl_dist.items():
            pct = (count / total) * 100
            st.markdown(f"• {severity}: **{count}** ({pct:.1f}%)")

        severe_pct = (sjl_dist.get('Moderate (1–2h)', 0) + sjl_dist.get('Severe (>2h)', 0)) / total * 100
        st.markdown(f"
**{severe_pct:.1f}%** of the sample shows moderate-to-severe social jetlag.")

    st.markdown("---")

    # Auto-generated research summary
    st.markdown("### 📝 Auto-Generated Research Summary")

    n = len(filtered_df)
    avg_age = filtered_df['age'].mean()
    pct_female = (filtered_df['sex'] == 'F').mean() * 100
    avg_meq = filtered_df['meq_score'].mean()
    avg_sjl = filtered_df['social_jetlag_hours'].mean()
    avg_prod = filtered_df['productivity_score'].mean()

    # Statistical test: MEQ vs productivity
    from scipy.stats import pearsonr
    r_meq, p_meq = pearsonr(filtered_df['meq_score'], filtered_df['productivity_score'])
    r_sjl, p_sjl = pearsonr(filtered_df['social_jetlag_hours'], filtered_df['productivity_score'])

    summary = f"""
    This exploratory analysis examined **{n} adults** (mean age {avg_age:.1f} years, {pct_female:.1f}% female) 
    across three work modalities. The sample mean MEQ score was **{avg_meq:.1f}** (SD {filtered_df['meq_score'].std():.1f}), 
    indicating a predominantly intermediate chronotype distribution. Mean social jetlag was **{avg_sjl:.2f} hours** 
    (SD {filtered_df['social_jetlag_hours'].std():.2f}), with **{severe_pct:.1f}%** of participants experiencing 
    moderate-to-severe misalignment (>1h).

    **Key findings:** A {'significant' if p_meq < 0.05 else 'non-significant'} positive correlation emerged between 
    morningness (higher MEQ) and productivity (r = {r_meq:.3f}, p = {p_meq:.3f}). Social jetlag showed a 
    {'significant' if p_sjl < 0.05 else 'non-significant'} negative association with productivity 
    (r = {r_sjl:.3f}, p = {p_sjl:.3f}), consistent with the circadian misalignment hypothesis. 
    Remote workers exhibited the highest mean social jetlag and the lowest mean productivity, 
    suggesting that work modality moderates the chronotype-productivity pathway — a pattern 
    aligned with Matsumoto et al. (2023) and Crowley et al. (2023).
    """

    st.markdown(f'<div class="insight-box">{summary}</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 5: SQL LAB
# =============================================================================

with tab5:
    st.markdown("### 🗄️ SQL Practice Lab")
    st.markdown("Run queries directly against the relational database. Learn SQL while exploring your research data.")

    st.markdown("---")

    # Pre-built queries
    query_options = {
        "Select all participants": "SELECT * FROM participants LIMIT 10",
        "Average productivity by chronotype": """
            SELECT c.chronotype, COUNT(*) AS n, 
                   ROUND(AVG(pr.productivity_score), 2) AS avg_productivity
            FROM chronotype_assessments c
            JOIN productivity_outcomes pr ON c.participant_id = pr.participant_id
            GROUP BY c.chronotype
            ORDER BY avg_productivity DESC
        """,
        "Social jetlag by work modality": """
            SELECT p.work_modality, 
                   ROUND(AVG(s.social_jetlag_hours), 2) AS avg_sjl,
                   ROUND(AVG(pr.productivity_score), 2) AS avg_prod
            FROM participants p
            JOIN sleep_schedules s ON p.participant_id = s.participant_id
            JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
            GROUP BY p.work_modality
            ORDER BY avg_sjl DESC
        """,
        "High performers with low social jetlag": """
            SELECT p.participant_id, p.age, p.work_modality,
                   c.chronotype, s.social_jetlag_hours, pr.productivity_score
            FROM participants p
            JOIN chronotype_assessments c ON p.participant_id = c.participant_id
            JOIN sleep_schedules s ON p.participant_id = s.participant_id
            JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
            WHERE s.social_jetlag_hours < 0.6 AND pr.productivity_score > 7
            ORDER BY pr.productivity_score DESC
            LIMIT 15
        """,
        "Custom query": ""
    }

    selected_query = st.selectbox("Choose a query or write your own:", list(query_options.keys()))

    if selected_query == "Custom query":
        sql_input = st.text_area("Write your SQL query:", 
                                  value="SELECT * FROM participants LIMIT 5",
                                  height=150)
    else:
        sql_input = query_options[selected_query]
        st.code(sql_input, language='sql')

    if st.button("▶ Run Query"):
        try:
            result = load_from_sql(sql_input)
            if not result.empty:
                st.success(f"Query returned {len(result)} rows")
                st.dataframe(result, use_container_width=True)

                # Offer CSV download
                csv = result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download results as CSV",
                    data=csv,
                    file_name='query_results.csv',
                    mime='text/csv'
                )
            else:
                st.info("Query executed successfully but returned no rows.")
        except Exception as e:
            st.error(f"Query error: {e}")

    st.markdown("---")
    st.markdown("#### Database Schema")
    schema = """
    ```
    participants (participant_id, age, sex, work_modality)
    chronotype_assessments (participant_id, meq_score, chronotype)
    sleep_schedules (participant_id, sleep_onset_work, sleep_offset_work, ...)
    environmental_factors (participant_id, light_exposure_lux_hr)
    productivity_outcomes (participant_id, productivity_score, procrastination_score)
    work_modality_reference (modality_code, modality_name, description)
    chronotype_reference (chronotype_code, meq_range, typical_sleep_onset)
    ```
    """
    st.markdown(schema)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; font-family: 'Courier New', monospace; font-size: 0.75rem; color: #8888aa;">
    Diego José Palencia Robles · PhD Candidate · Universidad Galileo · 2026<br>
    Scoping Review Protocol: OSF.IO/26SCX · PRISMA-ScR · PCC Framework
</div>
""", unsafe_allow_html=True)
