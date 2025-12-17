# 🌪️ [The Chaos Kitchen](https://the-chaos-kitchen.streamlit.app/)

**Where algorithms cook dinner and the rules don't matter.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Chaos_Level-Maximum-yellow)

## 📖 About The Project

**The Chaos Kitchen** is an interactive data science experiment that uses **Network Graph Theory** and **Unsupervised Machine Learning** to analyze culinary connections. 

Instead of traditional recipe apps that tell you what to cook, this AI builds a weighted graph of thousands of potential ingredient combinations, detects hidden "Flavor Gangs" (communities), and mathematically judges your custom food combinations.

It features a custom **"Pop Art" UI** designed to break the monotony of standard data dashboards.

## 🚀 Key Features

### 🕸️ The Flavor Blob (Network Graph)
* **Interactive Visualization:** A dynamic physics-based graph (`PyVis`) showing how ingredients connect.
* **Community Detection:** Uses the **Greedy Modularity Algorithm** to identify clusters of ingredients that frequent the same recipes (e.g., "The Spice Squad", "The Mob").

### ⚖️ The AI Judge
* **Sanity Check:** Select up to 5 ingredients, and the AI calculates the shortest path and weight between them.
* **Verdict System:** * 🟢 **Surprisingly Legal:** Strong mathematical connection.
    * 🟡 **Suspicious:** No direct graph path found.
    * 🔴 **Criminal Offense:** High "Weirdness Score" detected (e.g., Pickles + Chocolate).

### 🧬 Flavor DNA
* **Radar Analysis:** A `Plotly` radar chart that dynamically maps the savory, spicy, sweet, crunchy, and "weird" profile of your creation.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (with custom HTML/CSS injection)
* **Graph Logic:** [NetworkX](https://networkx.org/)
* **Visualization:** [PyVis](https://pyvis.readthedocs.io/) & [Plotly](https://plotly.com/)
* **Data Manipulation:** Pandas & NumPy

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Nielr2004/The-Chaos-Kitchen.git
    cd The-Chaos-Kitchen
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 🧠 The Science Behind the Chaos

* **Graph Theory:** Ingredients are nodes; recipes are edges. The weight of an edge increases every time two ingredients appear together.
* **Unsupervised Learning:** We use modularity optimization to partition the network into communities without pre-labeled training data. The AI "learns" that Basil and Tomato belong together without being told they are Italian.


## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with 💻 and ☕ by SNEHASHIS*
