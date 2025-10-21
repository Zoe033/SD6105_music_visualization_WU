# 导入所需的库
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# 第1步：导入与加载
print("正在加载数据...")
try:
    df = pd.read_csv('ClassicHit.csv')
    print(f"数据加载成功，共 {len(df)} 行数据")
except FileNotFoundError:
    print("错误：'ClassicHit.csv' 文件未找到。请确保该文件与脚本在同一目录下。")
    raise

# 第2步：数据清洗与流派细分 (关键步骤)
print("正在处理数据...")

# 过滤时间：筛选 1923-2023 年的数据（横跨一个世纪）
df = df.dropna(subset=['Year', 'Genre'])
df = df[(df['Year'] >= 1923) & (df['Year'] <= 2023)]

# 创建"高保真"流派映射函数
def high_fidelity_genre_mapping(genre):
    """高保真流派映射，几乎消除 'Other' 类别"""
    if not isinstance(genre, str):
        return 'Other'
    
    genre_lower = genre.lower()
    
    # 精确匹配规则
    if 'pop' in genre_lower and 'soft rock' not in genre_lower:
        return 'Pop'
    elif 'soft rock' in genre_lower:
        return 'Soft Rock'
    elif 'alt' in genre_lower and 'rock' in genre_lower:
        return 'Alternative Rock'
    elif 'hard rock' in genre_lower:
        return 'Hard Rock'
    elif 'punk' in genre_lower:
        return 'Punk'
    elif 'hip hop' in genre_lower or 'hip-hop' in genre_lower:
        return 'Hip Hop'
    elif 'r&b' in genre_lower or 'rnb' in genre_lower:
        return 'R&B'
    elif 'funk' in genre_lower:
        return 'Funk'
    elif 'jazz' in genre_lower:
        return 'Jazz'
    elif 'blues' in genre_lower:
        return 'Blues'
    elif 'country' in genre_lower:
        return 'Country'
    elif 'electronic' in genre_lower or 'edm' in genre_lower:
        return 'Electronic'
    elif 'rock' in genre_lower:
        return 'Rock'  # 通用 Rock 类别
    elif 'soul' in genre_lower:
        return 'Soul'
    elif 'disco' in genre_lower:
        return 'Disco'
    elif 'reggae' in genre_lower:
        return 'Reggae'
    elif 'folk' in genre_lower:
        return 'Folk'
    else:
        return 'Other'

# 应用流派映射
df['main_genre'] = df['Genre'].apply(high_fidelity_genre_mapping)

# 聚合数据
df_agg = df.groupby(['Year', 'main_genre']).size().reset_index(name='Count')
total_yearly_count = df_agg.groupby('Year')['Count'].transform('sum')
df_agg['Percentage'] = df_agg['Count'] / total_yearly_count

# 处理缺失值：为每个流派创建完整的年份序列
print("正在处理缺失值...")
all_years = range(1923, 2024)
all_genres = df_agg['main_genre'].unique()

# 创建完整的年份-流派组合
complete_data = []
for year in all_years:
    for genre in all_genres:
        existing = df_agg[(df_agg['Year'] == year) & (df_agg['main_genre'] == genre)]
        if len(existing) > 0:
            complete_data.append({
                'Year': year,
                'main_genre': genre,
                'Count': existing.iloc[0]['Count'],
                'Percentage': existing.iloc[0]['Percentage']
            })
        else:
            # 缺失值处理：使用线性插值或设为0
            complete_data.append({
                'Year': year,
                'main_genre': genre,
                'Count': 0,
                'Percentage': 0.0
            })

df_complete = pd.DataFrame(complete_data)

# 对每个流派进行线性插值处理缺失值
for genre in all_genres:
    genre_data = df_complete[df_complete['main_genre'] == genre].copy()
    genre_data = genre_data.sort_values('Year')
    
    # 使用线性插值填充缺失的百分比值
    genre_data['Percentage'] = genre_data['Percentage'].replace(0, np.nan)
    genre_data['Percentage'] = genre_data['Percentage'].interpolate(method='linear', limit_direction='both')
    genre_data['Percentage'] = genre_data['Percentage'].fillna(0)
    
    # 更新完整数据
    df_complete.loc[df_complete['main_genre'] == genre, 'Percentage'] = genre_data['Percentage'].values

# 获取所有独特流派
unique_genres = df_complete['main_genre'].unique()
print(f"发现 {len(unique_genres)} 个独特流派: {list(unique_genres)}")

# 第3步：创建堆叠面积图
print("正在创建堆叠面积图...")

# 使用 plotly.express 创建堆叠面积图
fig = px.area(
    df_complete,
    x='Year',
    y='Percentage',
    color='main_genre',
    title='The Evolution of Music Genres (1923-2023)',
    labels={'Percentage': 'Share %', 'Year': 'Year', 'main_genre': 'Genre'},
    template='simple_white',
    color_discrete_sequence=px.colors.qualitative.Set3
)

# 第4步：美化与交互性
print("正在美化图表...")

fig.update_layout(
    template='simple_white',
    title=dict(
        text='<b>The Evolution of Music Genres (1923-2023)</b><br><sub>Click on a genre in the legend to view its individual trend</sub>', 
        font=dict(size=24), 
        x=0.5
    ),
    font=dict(family="Arial", size=12, color="black"),
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=-0.15, 
        xanchor="center", 
        x=0.5,
        title_text="Click to filter genres"
    ),
    hovermode="x unified",
    height=600
)

# 更新坐标轴
fig.update_xaxes(title_text='Year')
fig.update_yaxes(
    title_text='Share %',
    ticksuffix='%',
    range=[0, 1]
)

# 更新悬停模板
fig.update_traces(
    hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>Share: %{y:.1%}<extra></extra>"
)

# 第5步：添加点击弹窗功能
print("正在添加交互功能...")

# 添加自定义 JavaScript 来实现点击弹窗
custom_js = """
<script>
// 添加点击事件监听器
document.addEventListener('DOMContentLoaded', function() {
    const plotDiv = document.querySelector('.plotly-graph-div');
    
    plotDiv.on('plotly_click', function(data) {
        const point = data.points[0];
        const genre = point.data.name;
        
        // 创建弹窗内容
        const popupContent = `
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                       background: white; border: 2px solid #333; border-radius: 10px; 
                       padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); z-index: 1000;
                       max-width: 80%; max-height: 80%; overflow: auto;">
                <h3 style="margin-top: 0; color: #333;">${genre} - Individual Trend</h3>
                <div id="individual-chart" style="width: 100%; height: 400px;"></div>
                <button onclick="this.parentElement.remove()" 
                        style="position: absolute; top: 10px; right: 10px; 
                               background: #ff4444; color: white; border: none; 
                               border-radius: 50%; width: 30px; height: 30px; cursor: pointer;">×</button>
            </div>
        `;
        
        // 添加弹窗到页面
        document.body.insertAdjacentHTML('beforeend', popupContent);
        
        // 创建单独的趋势图
        const genreData = ${JSON.stringify(df_complete.filter(d => d.main_genre === genre))};
        
        const individualTrace = {
            x: genreData.map(d => d.Year),
            y: genreData.map(d => d.Percentage),
            type: 'scatter',
            mode: 'lines+markers',
            name: genre,
            line: {color: point.data.line.color, width: 3},
            marker: {size: 6}
        };
        
        const layout = {
            title: `${genre} Trend (1923-2023)`,
            xaxis: {title: 'Year'},
            yaxis: {title: 'Share %', ticksuffix: '%'},
            template: 'simple_white',
            height: 400
        };
        
        Plotly.newPlot('individual-chart', [individualTrace], layout);
    });
});
</script>
"""

# 第6步：保存文件
print("正在保存文件...")
fig.write_html("genre_trends_stacked.html")

# 添加自定义 JavaScript 到 HTML 文件
with open("genre_trends_stacked.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 在 </body> 标签前插入自定义 JavaScript
html_content = html_content.replace("</body>", custom_js + "</body>")

with open("genre_trends_stacked.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 堆叠面积图已成功保存为 genre_trends_stacked.html")
print("🎵 图表特性：")
print(f"   - {len(unique_genres)} 个流派的堆叠趋势图")
print("   - 1923-2023 年完整世纪跨度")
print("   - 缺失值线性插值处理")
print("   - 点击流派图例可筛选显示")
print("   - 点击数据点可弹出单独趋势图")
print("   - 统一悬停显示所有流派数据")