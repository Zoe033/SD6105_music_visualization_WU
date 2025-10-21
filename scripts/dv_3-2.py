import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
df = pd.read_csv('data.csv')

# Define the key audio features to analyze
features = ['danceability', 'energy', 'loudness', 'acousticness', 'valence', 'speechiness', 'instrumentalness', 'liveness', 'tempo']

# Define function to map year to Era
def map_year_to_era(year):
    if 1970 <= year <= 1989:
        return '1970-1989 (Classic Era)'
    elif 1990 <= year <= 2009:
        return '1990-2009 (Transition Era)'
    elif 2010 <= year <= 2020:
        return '2010-2020 (Modern Era)'
    else:
        return None

# Apply the function to create Era column
df['Era'] = df['year'].apply(map_year_to_era)

# Filter out data not in the defined eras
df_filtered = df[df['Era'].notna()].copy()

# Initialize empty DataFrame for correlations
corr_df = pd.DataFrame()

# Loop through each unique Era
for era in df_filtered['Era'].unique():
    # Filter data for this era
    df_era = df_filtered[df_filtered['Era'] == era]
    
    # Calculate correlation matrix for this era
    era_corr = df_era[features + ['popularity']].corr(numeric_only=True)
    
    # Extract just the popularity column from this matrix
    era_pop_corr = era_corr[['popularity']].drop('popularity')
    
    # Rename the column to the era name
    era_pop_corr.columns = [era]
    
    # Append this (transposed) to corr_df
    if corr_df.empty:
        corr_df = era_pop_corr.T
    else:
        corr_df = pd.concat([corr_df, era_pop_corr.T])

# Create the heatmap using plotly.express.imshow
fig = px.imshow(
    corr_df,
    x=corr_df.columns,  # The Eras
    y=corr_df.index,    # The Features
    text_auto=False,    # We'll add custom text formatting
    aspect="auto",      # Make rectangles fit the space
    title="The Evolving Formula for a Hit Song: Feature Correlation with Popularity",
    color_continuous_scale='RdBu_r',  # Red-White-Blue divergent scale
    color_continuous_midpoint=0,       # Set 0 as neutral midpoint
    labels=dict(x="Time Era", y="Audio Feature", color="Correlation")
)

# Add custom text with rounded values for better readability
fig.update_traces(
    text=[[f"{val:.2f}" for val in row] for row in corr_df.values],
    texttemplate="%{text}",
    textfont=dict(size=12, color="white", family="Arial, sans-serif")
)

# Enhanced hover template with better formatting
fig.update_traces(
    hovertemplate="<b>🎵 Feature:</b> %{y}<br><b>📅 Era:</b> %{x}<br><b>📊 Correlation:</b> %{z:.3f}<br><b>💡 Interpretation:</b> %{customdata}<extra></extra>",
    customdata=[[
        "Strong positive correlation" if abs(val) > 0.3 and val > 0 else
        "Strong negative correlation" if abs(val) > 0.3 and val < 0 else
        "Moderate positive correlation" if abs(val) > 0.1 and val > 0 else
        "Moderate negative correlation" if abs(val) > 0.1 and val < 0 else
        "Weak correlation"
        for val in row
    ] for row in corr_df.values]
)

# Enhanced layout with beautiful styling
fig.update_layout(
    template='plotly_white',  # Clean white background
    title={
        'text': "🎵 The Evolving Formula for a Hit Song: Feature Correlation with Popularity 📈",
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'size': 22,
            'family': 'Arial, sans-serif',
            'color': '#2c3e50'
        }
    },
    font=dict(
        family="Arial, sans-serif",
        size=16,
        color="#2c3e50"
    ),
    width=1000,  # Increased width
    height=700,  # Increased height
    margin=dict(l=180, r=100, t=150, b=120),  # Further increased margins for better spacing
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Enhanced x-axis (Eras) styling with bold labels
fig.update_xaxes(
    side="top",
    tickfont=dict(size=15, family="Arial, sans-serif", color="#34495e"),
    title_text="<b>Time Era</b>",  # Bold title
    title_font=dict(size=18, family="Arial, sans-serif", color="#2c3e50"),
    gridcolor='lightgray',
    gridwidth=0.5,
    showgrid=True,
    tickmode='linear',
    dtick=1
)

# Enhanced y-axis (Features) styling with bold labels
fig.update_yaxes(
    tickfont=dict(size=15, family="Arial, sans-serif", color="#34495e"),
    title_text="<b>Audio Feature</b>",  # Bold title
    title_font=dict(size=18, family="Arial, sans-serif", color="#2c3e50"),
    gridcolor='lightgray',
    gridwidth=0.5,
    showgrid=True,
    tickangle=0,
    tickmode='linear',
    dtick=1
)

# Enhanced colorbar styling
fig.update_coloraxes(
    colorbar=dict(
        title=dict(
            text="Correlation Strength",
            font=dict(size=16, family="Arial, sans-serif", color="#2c3e50")
        ),
        tickfont=dict(size=14, family="Arial, sans-serif", color="#34495e"),
        thickness=25,
        len=0.7,
        x=1.05,
        xanchor="left"
    )
)

# Add annotations for better interpretation - moved to bottom right
fig.add_annotation(
    text="💡 <b>How to read:</b><br>• Red = Positive correlation<br>• Blue = Negative correlation<br>• White = No correlation<br>• Darker = Stronger",
    xref="paper", yref="paper",
    x=0.98, y=0.02,
    showarrow=False,
    align="right",
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="gray",
    borderwidth=1,
    font=dict(size=12, family="Arial, sans-serif", color="#2c3e50")
)

# Save the file with custom HTML wrapper for centering
html_content = fig.to_html(include_plotlyjs=True, div_id="plotly-div")

# Create custom HTML with centering styles
custom_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Hit Song Formula Heatmap</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }}
        #plotly-div {{
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

# Write the custom HTML file
with open("hit_song_formula_heatmap.html", "w", encoding="utf-8") as f:
    f.write(custom_html)

print("热图已成功创建并保存为 'hit_song_formula_heatmap.html'")
print(f"数据概览:")
print(f"- 总数据点: {len(df_filtered)}")
print(f"- 时代分布:")
for era in df_filtered['Era'].unique():
    count = len(df_filtered[df_filtered['Era'] == era])
    print(f"  {era}: {count} 首歌曲")
print(f"- 分析的特征: {', '.join(features)}")
