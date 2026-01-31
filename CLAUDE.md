# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a coursework repository for **University of Minnesota CERT-X465-003: Data Interpretation and Application** (Jan 2026). The course focuses on data analysis, visualization, and deriving actionable insights from datasets.

### Research Focus

The primary research project investigates the **meta-analysis of Kaggle competitions** to understand competitive patterns and success factors. Key research questions include:

- What coding languages and libraries are most commonly used in winning solutions?
- What types of models and machine learning platforms are most regularly used to win competitions?
- Are competition winners typically individuals or teams?
- Are winners professionals or amateurs in machine learning and data science?
- What types of hardware are being used by successful competitors?

**Project Goals:**
- Determine if individual amateurs with mid-tier hardware can realistically compete
- Identify barriers to entry and success factors for Kaggle competitions
- Provide insights for both competitors and competition organizers
- Understand platform evolution over Kaggle's ~15-year history

## Environment and Dependencies

### Python Environment
- **Python Version**: 3.12 (requires >=3.12, <3.13)
- **Package Manager**: UV (managed via `uv.lock` and `pyproject.toml`)
- **Virtual Environment**: `.venv/` directory

### Installing Dependencies
```bash
uv sync
```

### Key Dependencies
- **Data Science**: pandas (2.3.3), numpy (2.2.6), scikit-learn (1.8.0)
- **Visualization**: matplotlib (3.10.8), seaborn (0.13.2), plotly (6.5.2)
- **Jupyter**: jupyterlab (4.5.3), ipywidgets (8.1.8)
- **Kaggle Integration**: kaggle (1.8.3), kagglehub (0.4.2)
- **GPU Acceleration**: Uses cudf.pandas and cuml.accel extensions for accelerated data processing

## Running Jupyter Notebooks

### Start JupyterLab
```bash
jupyter lab
```

### GPU Accelerators
Some notebooks use GPU acceleration extensions. Load them at the start of notebooks:
```python
%load_ext cudf.pandas
%load_ext cuml.accel
```

## Project Structure

```
.
├── data/                           # Datasets directory
│   ├── kaggle_data/               # Kaggle datasets (git-ignored)
│   │   ├── kaggle-logo.png
│   │   ├── meta-kaggle/           # Meta Kaggle dataset (40+ CSV files)
│   │   └── meta-kaggle-code/
│   └── mbd-decisions_downloader.py
├── src/                            # Python source files
│   └── mba_decisions.csv          # MBA decisions dataset
├── models/                         # Model storage directory
├── CERT-X465-003_GeneralNotebook.ipynb       # Main analysis notebook
├── CERT-X465-003_KaggleDatasetEDA.ipynb     # Kaggle dataset EDA
├── sample.ipynb                   # (git-ignored)
├── pyproject.toml                 # UV project configuration
├── uv.lock                        # UV lockfile
└── README.md                      # Course information
```

## Datasets

### MBA Decisions Dataset
- **Location**: `src/mba_decisions.csv`
- **Size**: 10,000 rows × 20 columns
- **Purpose**: Analysis of MBA candidate decisions and demographics
- **Key Columns**: Person ID, Age, Gender, Undergraduate Major, GPA, Work Experience, Salary, MBA Decision

### Meta Kaggle Dataset
- **Location**: `data/kaggle_data/meta-kaggle/`
- **Source**: Released by the Kaggle team, downloaded via Kaggle API
- **Purpose**: Primary dataset for the course research project analyzing Kaggle competition patterns
- **Reliability**: High (directly from Kaggle), contains all publicly available platform data
- **Contents**: 40+ CSV files including:
  - **Competitions**: Competition details and metadata
  - **Kernels**: Notebook/script submissions (Python and R code)
  - **Models**: Machine learning models used
  - **Users & Teams**: Participant information and team memberships
  - **Datasets**: Dataset metadata and versions
  - **Submissions**: Competition submission records
  - **Organizations**: Competition sponsors and organizers
  - Additional tables: Tags, Votes, Forums, Achievements, etc.
- **Note**: This directory is git-ignored but should be available locally

### Meta Kaggle Code Dataset
- **Location**: `data/kaggle_data/meta-kaggle-code/`
- **Purpose**: Extension dataset containing raw source code from Python and R notebooks
- **Contents**: Source code used for dataset analysis, competition submissions, and uploaded notebooks
- **Use Case**: Text analysis of coding patterns, library usage, and solution approaches

## Notebook Workflows

### General Notebook (CERT-X465-003_GeneralNotebook.ipynb)
- Analyzes the MBA decisions dataset
- Creates visualizations using Plotly (pie charts, scatter plots, histograms)
- Explores demographic distributions and relationships between variables

### Kaggle EDA Notebook (CERT-X465-003_KaggleDatasetEDA.ipynb)
- **Purpose**: Analyzes Meta Kaggle datasets to answer research questions about competition patterns
- **Data Loading**: One-time CSV→Parquet conversion using `pyarrow` with multiprocessing (4-5 workers) for 10-20x faster subsequent reads
- **Parquet Storage**: `data/kaggle_data/meta-kaggle-parquet/` - columnar format provides ~60-80% compression and free column selection
- **Currency Conversion**: Uses `currency_converter` library to normalize competition rewards to USD (handles EUR, GBP, INR)
- **Key Analyses**:
  - Programming language and library usage patterns
  - Model types and ML platform preferences
  - Individual vs. team competition dynamics
  - Professional vs. amateur participant characteristics
  - Hardware requirements and usage patterns
- **Visualization**: Plotly for interactive charts; uses log scales for wide-range scatter plots (prize pools vs. competitors)
- **Technical Approach**:
  - Uses GPU-accelerated pandas and cuml for performance
  - Imports advanced ML libraries (TSNE, PCA, TruncatedSVD, NMF, TfidfVectorizer)
  - Applies clustering and dimensionality reduction techniques
  - Text analysis of code patterns from Meta Kaggle Code dataset

### Notebook Conventions
- **Section numbering**: `## 1.)`, `### 1.A)`, `#### 1.A.i) ***Title***` — hierarchical with roman numeral subsections
- **Medal column**: Mixed type (int/float/string depending on source). Use `Medal.notna() & (Medal != '')` for detection, `pd.to_numeric(Medal, errors='coerce')` for numeric comparison
- **Key join paths**:
  - Kernel → medal outcome: `kernel_versions.Id → submissions.SourceKernelVersionId → submissions.TeamId → teams.Medal`
  - Team leader tier: `teams.TeamLeaderId → users.Id` (join to get `PerformanceTier`)
  - Competition tags: `comp_tags.CompetitionId` + `comp_tags.TagId → tags.Id`

## Common Visualization Patterns

### Plotly Visualizations
The notebooks use Plotly Express and Plotly Graph Objects for interactive visualizations:
- Pie charts for categorical distributions
- Scatter plots with size and color encoding for multidimensional data
- Histograms for distribution analysis
- Custom annotations and layout configurations (width, height, margins)
- Log scales (`type='log'`) for wide-range data (e.g., prize pools $1K-$10M)
- Currency formatting in tick labels using `tickformat='$,.0f'`

### Sample Size Conventions
- Random sampling uses `random_state=33` for reproducibility
- Sample size of 777 is used in the general notebook

## Performance Optimization Patterns

### Large CSV Processing
- **Parquet conversion**: `pd.read_csv(chunksize=1M)` → `pa.Table.from_pandas()` → `pq.ParquetWriter()` for files >200MB
- **Multiprocessing**: Use 4-5 workers max for I/O-bound CSV conversion to avoid disk thrashing
- **Column selection**: `pd.read_parquet(columns=[...])` only reads specified columns from disk (10-20x faster than CSV)
- **Date parsing**: Apply `pd.to_datetime()` after parquet read, not during (parquet stores as int64 timestamp)

## Course Context

This repository contains work for a 6-week course covering:
1. **Week 1**: Question identification and framing
2. **Week 2**: Finding and assessing data quality
3. **Week 3**: Deriving insights from data
4. **Week 4**: Interpreting graphs and visuals
5. **Week 5**: Making data-driven recommendations
6. **Week 6**: Business intelligence and dashboards

Assignments involve creating videos, reports, and presentations based on data analysis.

## Assignment Submissions

### Assignment 1 (Week 1) - Question Identification
- **Topic**: Meta-analysis of Kaggle competitions
- **Target Audience**:
  - Individual competitors assessing their chances
  - Competition organizers and Kaggle team
  - Those considering careers in machine learning/data science
- **Value**: Helps determine if amateur competitors with mid-tier hardware can realistically compete and succeed

### Assignment 2A (Week 2) - Data Source Identification
- **Primary Dataset**: Meta Kaggle (40+ CSV files)
- **Extension Dataset**: Meta Kaggle Code (raw Python/R notebooks)
- **Data Quality Assessment**: High reliability (directly from Kaggle), minimal bias concerns
- **Relevance**: Directly addresses research questions about competition patterns and success factors

See `README.md` for complete assignment submission essays.
