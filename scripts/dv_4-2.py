"""
Act 4: Interactive Scatter Plot with Named Clusters
音乐宇宙：AI发现的歌曲星系
"""

import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load & Prepare Data
print("正在加载数据...")
df = pd.read_csv('data.csv')

# Define features for clustering
features = ['danceability', 'energy', 'acousticness', 'valence', 'speechiness', 
           'instrumentalness', 'liveness', 'loudness', 'tempo']

# Sample the data for performance
print("正在采样数据...")
df_sample = df.sample(n=10000, random_state=42).copy()

# Standardize the features
print("正在标准化特征...")
scaler = StandardScaler()
features_scaled = scaler.fit_transform(df_sample[features])

# K-Means Clustering
print("正在执行K-Means聚类...")
kmeans = KMeans(n_clusters=8, random_state=42, n_init=10)
df_sample['Cluster_ID'] = kmeans.fit_predict(features_scaled)

# Profile & Rename Clusters (The "Easy to Understand" Step)
print("正在分析聚类特征...")
# Profile: Calculate the mean of all features grouped by Cluster_ID
cluster_profile = df_sample.groupby('Cluster_ID')[features].mean()

# Calculate overall feature means for comparison
overall_feature_means = df_sample[features].mean()

def get_descriptive_cluster_name(cluster_id, cluster_row, overall_means, top_n=2, threshold_multiplier=0.1):
    """
    创建更具描述性的聚类名称
    """
    # Calculate deviation from overall mean for each feature
    deviations = (cluster_row - overall_means) / overall_means.std()
    
    # Find features that are significantly above the overall mean
    significant_features = deviations[deviations > threshold_multiplier].sort_values(ascending=False)
    
    if len(significant_features) >= 2:
        # Take the top N most significant features
        top_features = significant_features.head(top_n).index.tolist()
        feature_names_formatted = [f"High {f.title()}" for f in top_features]
        return f"Cluster {cluster_id} ({', '.join(feature_names_formatted)})"
    elif len(significant_features) == 1:
        # Only one significant feature
        feature_name = significant_features.index[0]
        return f"Cluster {cluster_id} (High {feature_name.title()})"
    else:
        # Fallback: use the highest feature relative to overall mean
        relative_scores = (cluster_row - overall_means) / overall_means.std()
        highest_feature = relative_scores.idxmax()
        return f"Cluster {cluster_id} (High {highest_feature.title()})"

# Create Name Map with improved naming strategy
name_map = {}
for cluster_id, cluster_row in cluster_profile.iterrows():
    name_map[cluster_id] = get_descriptive_cluster_name(cluster_id, cluster_row, overall_feature_means, top_n=2, threshold_multiplier=0.1)

print("聚类特征分析结果:")
for cluster_id, cluster_row in cluster_profile.iterrows():
    print(f"聚类 {cluster_id}: {name_map[cluster_id]}")
    print(f"  特征均值: {cluster_row.to_dict()}")
    print()

# Apply Renaming
df_sample['Cluster_Name'] = df_sample['Cluster_ID'].map(name_map)

# Clean Artists Column (for Hover)
df_sample['artists_cleaned'] = df_sample['artists'].str.replace(r"[\"\[\]\']", "", regex=True)

# Create Visualization (Plotly Express)
print("正在创建可视化...")
fig = px.scatter(
    df_sample,
    x='danceability',
    y='energy',
    color='Cluster_Name',
    size='popularity',
    hover_name='name',
    hover_data={
        'artists_cleaned': True, 
        'year': True, 
        'Cluster_Name': True, 
        'danceability': False, 
        'energy': False, 
        'popularity': True
    }
)

# Aesthetics & Interactivity
fig.update_layout(
    template='simple_white',
    title=dict(
        text="<b>The Music Universe: AI-Discovered Song Galaxies</b>",
        font=dict(size=22),
        x=0.5
    ),
    legend_title_text='AI-Discovered Clusters (Click to Toggle)',
    xaxis_title="Danceability",
    yaxis_title="Energy",
    font=dict(family="Arial", size=12)
)

fig.update_traces(
    marker=dict(
        opacity=0.7,
        line=dict(width=0.5, color='Black')
    ),
    hovertemplate="<b>%{hovertext}</b><br>by %{customdata[0]}<br><br><b>Galaxy:</b> %{customdata[2]}<br><b>Year:</b> %{customdata[1]}<br><b>Popularity:</b> %{customdata[3]}<extra></extra>"
)

# Save File
print("正在保存HTML文件...")
fig.write_html("music_universe_named_clusters.html")
print("完成！文件已保存为 'music_universe_named_clusters.html'")

# Display some statistics
print(f"\n数据统计:")
print(f"总样本数: {len(df_sample)}")
print(f"聚类数量: {len(df_sample['Cluster_Name'].unique())}")
print(f"聚类分布:")
cluster_counts = df_sample['Cluster_Name'].value_counts()
for cluster_name, count in cluster_counts.items():
    print(f"  {cluster_name}: {count} 首歌曲")
