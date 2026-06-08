# Chronotype Explorer

**Research Domain:** Circadian Rhythms, Time Management & Personal Productivity  
**Author:** Diego José Palencia Robles — PhD Candidate, Universidad Galileo  
**Protocol:** [OSF.IO/26SCX](https://doi.org/10.17605/OSF.IO/26SCX) | PRISMA-ScR | PCC Framework  
**Live App:** *[Deploy to Render/Hugging Face and paste URL here]*  
**License:** MIT

---

## What This Is

A full-stack exploratory data analysis (EDA) web application for circadian research. It takes a dataset of 500 adults with chronotype scores (MEQ), sleep schedules, work modalities, and productivity outcomes, and transforms it into an interactive research tool with:

- **Data quality dashboard** (missing values, duplicates, data dictionary)
- **Distribution analysis** (histograms, box plots, pie charts)
- **Correlation analysis** (heatmaps, scatter plots, statistical tests)
- **Research question explorer** (protocol-driven hypothesis testing)
- **SQL practice lab** (run queries against a relational database in real time)

This is **Project 1** of the PhD → Data Science Portfolio Roadmap. It proves you can handle real data, clean it, analyze it, visualize it, and build a UI around it.

---

## 🗂️ Repository Structure

```
chronotype-explorer/
├── app.py                          # Main Streamlit application (593 lines)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   ├── chronotype_data.csv         # Synthetic dataset (500 records, 16 variables)
│   ├── chronotype_explorer.db      # SQLite relational database (7 tables)
│   └── sql_practice.sql            # 11 SQL exercises from basic to advanced
├── notebooks/
│   └── 01_exploration.ipynb        # Jupyter companion for deep analysis
├── src/                            # (reserved for modular expansion in P2–P5)
└── assets/                         # Screenshots and diagrams
```

---

## 🚀 Step-by-Step: From Zero to Live App

### STEP 0: Prerequisites (What You Need Before Starting)

| Tool | Why You Need It | How to Get It |
|------|----------------|---------------|
| **Python 3.10+** | The programming language | [python.org](https://python.org) or use Google Colab |
| **Git** | Version control | [git-scm.com](https://git-scm.com) |
| **GitHub Account** | Host your code publicly | [github.com](https://github.com) |
| **VS Code** | Code editor (recommended) | [code.visualstudio.com](https://code.visualstudio.com) |
| **A terminal** | Run commands | Terminal (Mac/Linux) or PowerShell (Windows) |

> **If you are completely new to coding:** Start with [Automate the Boring Stuff](https://automatetheboringstuff.com/) (free online book). Read Chapters 1–6. That is enough to understand every line in this project.

---

### STEP 1: Create Your GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name it `chronotype-explorer`
3. Make it **Public** (recruiters need to see it)
4. Check **"Add a README file"**
5. Click **Create repository**
6. Click the green **<> Code** button, copy the HTTPS URL

---

### STEP 2: Clone the Repository to Your Computer

Open your terminal and run:

```bash
cd Documents   # or wherever you want the project folder
git clone https://github.com/YOUR_USERNAME/chronotype-explorer.git
cd chronotype-explorer
```

---

### STEP 3: Create a Python Virtual Environment

This keeps your project dependencies isolated. Run these commands **inside** your project folder:

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal line. This means the environment is active.

---

### STEP 4: Install Dependencies

Create a file named `requirements.txt` in your project root. Paste this inside it:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.11.0
```

Then run:

```bash
pip install -r requirements.txt
```

This downloads and installs all the libraries. It takes 2–3 minutes.

---

### STEP 5: Add the Data Files

Create a folder named `data/` inside your project. Copy these files into it:

- `chronotype_data.csv` (the synthetic dataset)
- `chronotype_explorer.db` (the SQLite database)

You can generate the synthetic data yourself using the script in the `data_generation/` section below, or use the provided files.

---

### STEP 6: Create the Streamlit App

Create a file named `app.py` in your project root. Paste the entire application code (provided in this repository) into it.

**What the app does, section by section:**

| Section | What It Shows | Skills Demonstrated |
|---------|--------------|---------------------|
| **Overview** | Data dictionary, descriptive stats, first 10 rows | Data literacy, documentation |
| **Distributions** | MEQ histogram, productivity box plots, sleep comparison | matplotlib, seaborn, pandas grouping |
| **Correlations** | Heatmap, scatter plots, Pearson r values | Statistical analysis, visualization |
| **Research Questions** | Protocol-driven analysis by work modality, auto-generated summary | Research methodology, narrative synthesis |
| **SQL Lab** | Live query execution against the database | SQL, relational databases, JOINs |

---

### STEP 7: Run the App Locally

In your terminal (with `venv` activated), run:

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`.

**Play with it:**
- Use the sidebar filters to subset by age, sex, work modality, chronotype
- Watch the metrics and charts update in real time
- Go to the SQL Lab tab and run the pre-built queries
- Try writing your own SQL query

---

### STEP 8: Commit Your Code to GitHub

Every time you make progress, save it to GitHub. This is your portfolio's version history.

```bash
git add .
git commit -m "Initial commit: Chronotype Explorer with EDA dashboard and SQL lab"
git push origin main
```

---

### STEP 9: Deploy to the Web (Free)

A project with a **live URL** is 10× more impressive than one that only runs on your laptop.

**Option A: Streamlit Community Cloud (Easiest)**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your `chronotype-explorer` repo
5. Set main file path to `app.py`
6. Click **Deploy**
7. In 2 minutes, you get a URL like `https://chronotype-explorer-abc123.streamlit.app`

**Option B: Render.com**
1. Go to [render.com](https://render.com)
2. Connect your GitHub account
3. Click **"New Web Service"**
4. Select your repo
5. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT`
6. Click **Create Web Service**

Paste the live URL into your README, your CV, and your LinkedIn.

---

### STEP 10: Write Your LinkedIn Post

Document your learning process. Process posts get more engagement than finished-product posts.

**Template:**

> I just built my first data science web app.
>
> It's called **Chronotype Explorer** — an interactive dashboard that analyzes the relationship between circadian rhythms (are you a morning or night person?) and productivity across work modalities (onsite, hybrid, remote).
>
> What I learned:
> • Python pandas for data manipulation
> • matplotlib/seaborn for scientific visualization
> • Streamlit for turning a script into a web app
> • SQLite for relational database querying
> • How to deploy a live URL from GitHub
>
> The data is synthetic but based on the real parameters from my doctoral scoping review protocol on circadian rhythms and productivity (OSF.IO/26SCX).
>
> Live app: [URL]
> GitHub: [URL]
>
> Next: Project 2 — an interactive dashboard with Plotly and SQL.

---

## 📊 The Data

### Why Synthetic Data?

You do not need to wait for a real dataset to start building. Synthetic data lets you:
- Start coding immediately
- Control distributions to match your research hypotheses
- Practice data cleaning on intentionally messy data
- Demonstrate methodology without privacy concerns

### How the Data Was Generated

The dataset was generated using `numpy` with parameters drawn from published literature:

| Variable | Distribution | Source |
|----------|-------------|--------|
| MEQ Score | Normal(μ=50, σ=12), clipped 16–86 | Horne & Östberg (1976) |
| Sleep Onset | Derived from MEQ: later MEQ = later sleep | Roenneberg et al. (2003) |
| Social Jetlag | \|MSF - MSW\| with realistic variance | Wittmann et al. (2006) |
| Productivity | Base 6.5 + MEQ effect − SJL penalty + noise | Maier et al. (2022) |
| Light Exposure | Remote < Hybrid < Onsite | Crowley et al. (2023) |
| Procrastination | Evening types + SJL → higher procrastination | Maier et al. (2022) |

**Key correlations built into the data:**
- MEQ ↔ Productivity: r ≈ +0.27 (morningness predicts productivity)
- Social Jetlag ↔ Productivity: r ≈ −0.21 (misalignment hurts)
- Social Jetlag ↔ Procrastination: r ≈ +0.25 (misalignment increases procrastination)

### Database Schema (7 Tables)

```sql
participants (participant_id, age, sex, work_modality)
chronotype_assessments (participant_id, meq_score, chronotype)
sleep_schedules (participant_id, sleep_onset_work, sleep_offset_work, ...)
environmental_factors (participant_id, light_exposure_lux_hr)
productivity_outcomes (participant_id, productivity_score, procrastination_score)
work_modality_reference (modality_code, modality_name, description)
chronotype_reference (chronotype_code, meq_range, typical_sleep_onset)
```

This relational structure lets you practice:
- `JOIN` operations across multiple tables
- `GROUP BY` aggregation
- `WHERE` filtering
- Subqueries and correlated queries

---

## 🧠 What You Learn From This Project

| Skill | Where You Use It | Why It Matters for Jobs |
|-------|-----------------|------------------------|
| **Python basics** | Every file | The foundation of all data work |
| **pandas** | Data loading, filtering, grouping | 90% of a data analyst's job |
| **Descriptive statistics** | Overview tab, notebook | Communicating data characteristics |
| **Data visualization** | All chart tabs | A pattern in a chart is worth 1000 rows |
| **Statistical testing** | Correlation tab, notebook | Separates analysts from scientists |
| **Streamlit** | The entire UI | Turns Python scripts into shareable tools |
| **SQL** | SQL Lab tab | Required in almost every data job description |
| **Git/GitHub** | Version control | How teams collaborate; how recruiters verify your work |
| **Deployment** | Live URL | A portfolio without a live URL is invisible |

---

## 🔗 Connection to Your Doctoral Research

This project directly operationalizes your scoping review protocol:

| Protocol Element | Project Implementation |
|-----------------|----------------------|
| PCC Framework (Population, Concept, Context) | Sidebar filters for age, sex, chronotype, work modality |
| Circadian variables (MEQ, social jetlag) | Core variables in every chart and analysis |
| Productivity outcomes | `productivity_score`, `procrastination_score` |
| Work modality context | `work_modality` stratification in all analyses |
| Evidence-gap identification | SQL Lab queries that mimic evidence mapping |
| PRISMA-ScR transparency | Data dictionary, audit trail, version control |

---

## 📚 References (From Your Protocol)

- Crowley, S. J., Molina, T. A., & Burgess, H. J. (2023). A week in the life of full-time office workers: Work timing, sleep, and circadian disruption in the context of remote versus on-site work. *Chronobiology International*, 40(1), 1–13.
- Maier, T., Kühnel, J., & Zimmermann, B. (2022). How did you sleep tonight? The relevance of sleep quality and sleep–wake rhythm for procrastination at work. *Frontiers in Psychology*, 12, Article 785154.
- Matsumoto, Y., et al. (2023). Relationship between telework jetlag and perceived psychological distress among Japanese hybrid workers. *Clocks & Sleep*, 5(4), 604–614.
- Roenneberg, T., et al. (2003). Life between clocks: Daily temporal patterns of human chronotypes. *Journal of Biological Rhythms*, 18(1), 80–90.
- Wittmann, M., et al. (2006). Social jetlag: Misalignment of biological and social time. *Chronobiology International*, 23(1–2), 497–509.

---

## 🎯 Next Steps

1. **Complete this project** (2–3 weeks)
2. **Post on LinkedIn** with your live URL
3. **Start Project 2:** Social Jetlag Dashboard (Plotly + SQL + deployment)
4. **Parallel track:** Take a free SQL course ([Mode Analytics](https://mode.com/sql-tutorial/) or [SQLZoo](https://sqlzoo.net/))

---

*Diego José Palencia Robles · 2026 · Portfolio Project 1*
