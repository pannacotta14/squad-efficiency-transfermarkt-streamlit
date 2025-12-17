# Squad Efficiency in La Liga 2025-26

An interactive Streamlit dashboard analyzing squad efficiency in La Liga using Transfermarkt-derived data, focusing on age, market value, availability and match performance.

## Explore the project

* Live dashboard: [Streamlit App](https://squad-efficiency-transfermarkt-app-bk35z2rxcqbbuepnbxgynd.streamlit.app)

* GitHub repository: [Github](https://github.com/pannacotta14/squad-efficiency-transfermarkt-streamlit)

## Demo

Short walkthrough showing homepage navigation, matchday overview and match level analysis.

![Demo](demo/demo.gif)

## Dashboard previews

### Matchday overview
High-level snapshot of all fixtures on a selected matchday, focusing on squad characteristics and match outcomes.

Preview: [Matchday Overview](matchday.md)

### Match analysis

Detailed comparison of two teams in a specific match, including squad composition, availability, and outcome context.

Preview: [Match Analysis](match-analysis.md)

## Run locally

For those who want to replicate the dashboard: Clone the repository, install dependencies, then run the app:

```
git clone https://github.com/pannacotta14/squad-efficiency-transfermarkt-streamlit.git

pip install -r requirements.txt

cd squad-efficiency-transfermarkt-streamlit/my_app

streamlit run app.py
```

The app will be available at **http://localhost:8501**

## Final notes

This landing page presents the dashboard as a finished product, while the GitHub repository contains full technical details and reproducible setup instructions.