# SD6105_music_visualization_WU
# The Sonic Zeitgeist: A Visual Journey Through Music's Data

**A data visualization project for SD6105: Data Visualisation, exploring the evolution of musical tastes through a four-act interactive data story.**

This repository contains all source code, datasets, and generated outputs for the project. The final deliverable is a 5-minute video presentation that walks through four key acts of data discovery.

---

### 🚀 Live Interactive Demo

A live, interactive version of the static charts (Acts 1, 3, and 4) is hosted on GitHub Pages:

**[https://Zoe033.github.io/SD6105_music_visualization_WU/](https://Zoe033.github.io/SD6105_music_visualization_WU/)**

*(Note: Act 2 is a Plotly Dash application and must be run locally. See instructions below.)*

---

## 📖 The Four-Act Data Story

This project is structured as a four-act narrative, each answering a key question about the evolution of music.

### **[🎬 Act 1: The Empire of Genres (Time)](https://zoe033.github.io/SD6105_music_visualization_WU/docs/genre_trends_stacked.html)**
* **Chart:** stack chart
* **Question:** How has the popularity of major music genres changed over the last 100 years?
* **Insight:** This grid clearly shows the decline of Rock, the steady reign of Pop, and the dramatic, unstoppable rise of Hip Hop since the late 1990s. The linked hover-state allows for precise cross-genre comparison.

### **[🎬 Act 2: The Global Fingerprint (Space)](https://zoe033.github.io/SD6105_music_visualization_WU/docs/top50_music_dashboard_standalone.html)**
* **Chart:** Interactive Plotly Dash Dashboard
* **Question:** In our globalized world, are we all listening to the same music?
* **Insight:** By creating a click-to-update dashboard, we avoid a cluttered map. We see a "Global Average" dominated by Pop and Hip Hop, but can instantly discover the unique "local fingerprint" of any country (e.g., J-Pop in Japan, Latin music in Colombia).

### **[🎬 Act 3: The 'Gene' of a Hit Song (The DNA)](https://zoe033.github.io/SD6105_music_visualization_WU/docs/hit_song_formula_heatmap.html)**
* **Chart:** Faceted Correlation Heatmap
* **Question:** Has the "formula" for a hit song changed over time?
* **Insight:** Yes. This heatmap proves that the "genes" of a hit song have evolved. In the 1970s, audio features had weak links to popularity. In the modern era, `Loudness` and `Danceability` show a strong, clear correlation with a song's success.

### **[🎬 Act 4: The 'Universe' of Music (AI's View)](https://zoe033.github.io/SD6105_music_visualization_WU/docs/music_universe_named_clusters.html)**
* **Chart:** AI-Named Interactive Scatter Plot
* **Question:** If we ignore human-defined genres, how would an AI categorize music?
* **Insight:** By running a K-Means clustering algorithm, we discover distinct "music galaxies." To make this understandable, we profiled each cluster and gave it a descriptive name. The chart reveals a clear separation between, for example, the "High-Acousticness Cluster" and the "High-Energy/Dance Cluster."

---

## 🛠️ How to Run This Project

### Prerequisites

You must have Python 3.7+ installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Music-DataViz-Project.git](https://github.com/YOUR_USERNAME/Music-DataViz-Project.git)
cd Music-DataViz-Project
````

### 2\. Create a Virtual Environment & Install Libraries

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required libraries
pip install -r requirements.txt
```

### 3\. View the Interactive Charts

#### Acts 1, 3, & 4 (Static HTML Charts)

The pre-generated `.html` files are located in the `/output/html_charts/` folder (and also in `/docs/` for the live demo). You can simply double-click any of them to open them in your local browser.

#### Act 2 (Interactive Dash App)

This chart is a web application and **must be run locally**.

```bash
# Navigate to the scripts folder
cd scripts

# Run the Dash app
python act_2_global_dashboard.py
```

After running, open your web browser and go to **`http://127.0.0.1:8050/`** to see the interactive dashboard.

-----

### 🧰 Tools & Data

  * **Core Tools:** Python, Pandas, Plotly (Express & Graph Objects), Dash, Scikit-learn
  * **Data Sources:**
      * [15,000 Music Tracks - 19 Genres (w/ Spotify Data)](https://www.google.com/search?q=https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-192120https://www.kaggle.com/datasets/thebumpkin/10400-classic-hits-10-genres-1923-to-2023) (Used for Act 1)
      * [Top 50 Spotify Songs - 2019](https://www.kaggle.com/datasets/leonardopena/top50spotify2019) (Used for Act 2)
      * [Spotify Dataset 1921-2020, 160k+ Tracks](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-1921-2020-160k-tracks) (Used for Acts 3, 4)

<!-- end list -->
