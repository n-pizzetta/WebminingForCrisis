# Mining Knowledge from Social Media Data During Crisis Events

## Project Overview
This project focuses on mining actionable knowledge from social media data, particularly during crisis events such as floods, earthquakes, or wildfires. By analyzing the structure, usage, and content of the social web graph, the project aims to provide insights and tools that can assist emergency operators in decision-making.

### Objectives
1. **Dashboard Development**:
   - Visualize temporal distributions of tweets during crisis events.
   - Perform topic modeling using word clusters, embeddings, and more.
   - Build a search/query system to retrieve top tweets based on relevance.

2. **Tweet Priority Prediction**:
   - Classify tweets into three priority levels: High, Medium, and Low.
   - Utilize content, usage, and structure-based features for predictive modeling.

## Project Structure
```
.
├── notebooks/               # Jupyter notebooks for analysis and visualization
├── scripts/                 # Python scripts for dashboard and training the model
├── reports/                 # Reports and visualizations
├── requirements.txt         # Dependencies for scripts
└── README.md                # Project overview (this file)
```

## Getting Started

### Dataset
The dataset contains:
- **Nodes**: Information about events, users, tweets, and hashtags.
- **Relationships**: Connections between nodes (e.g., mentions, retweets).

## Key Features
1. **Dashboard**:
   - Analyze crisis events and visualize tweet distributions over time.
   - Perform topic modeling with word clusters and embeddings.
   - Query tweets based on user-defined keywords.

2. **Prediction Model**:
   - Train models to classify tweet priorities.
   - Evaluate model performance using metrics like F1 Score and Cohen’s Kappa.

## Usage

### Clone the repo and install dependencise

```bash
git clone https://github.com/n-pizzetta/WebminingForCrisis.git
cd WebminingForCrisis

# Optional
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac
# or .venv\Scripts\activate  # For Windows

# Run
pip install -r requirements.txt
```


### Running the Dashboard
Navigate to the project folder and execute the dashboard script:
```bash
python scripts/dashboard.py
```

### Training the Prediction Model
Run the training script:
```bash
python scripts/train_model.py
```

## Authors
- Tom Devynck
- Pierre Larose
- Nathan Pizzetta


## License
This project is licensed under the MIT License.
