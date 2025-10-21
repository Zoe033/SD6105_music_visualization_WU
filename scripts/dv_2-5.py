# 第1步：导入与设置
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 初始化应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 第2步：数据处理 (关键步骤)
# 加载 top50contry.csv 文件
df = pd.read_csv('top50contry.csv', encoding='latin1')

# (关键) 定义“流派归类”函数
def map_genre(genre_str):
    genre_str = str(genre_str).lower()
    if 'pop' in genre_str: return 'Pop'
    if 'rap' in genre_str or 'hip hop' in genre_str: return 'Hip Hop / Rap'
    if 'latin' in genre_str or 'reggaeton' in genre_str or 'colombian' in genre_str or 'argentine' in genre_str or 'panamanian' in genre_str or 'espanol' in genre_str: return 'Latin'
    if 'edm' in genre_str or 'electro' in genre_str or 'house' in genre_str or 'dance' in genre_str: return 'Electronic / Dance'
    if 'r&b' in genre_str: return 'R&B'
    if 'rock' in genre_str or 'wave' in genre_str: return 'Rock'
    if 'indie' in genre_str: return 'Indie / Alternative'
    if 'sertanejo' in genre_str or 'funk carioca' in genre_str or 'brega funk' in genre_str: return 'Brazilian'
    if 'k-pop' in genre_str: return 'K-Pop'
    if 'j-pop' in genre_str: return 'J-Pop'
    if 'desi' in genre_str or 'bollywood' in genre_str or 'punjabi' in genre_str: return 'South Asian'
    return 'Other'  # 这个'Other'会很小

# 应用映射
df['meta_genre'] = df['top genre'].apply(map_genre)

# (关键) 聚合国家数据
df_countries_agg = df.groupby('country')['meta_genre'].value_counts(normalize=True).reset_index(name='Percentage')

# (关键) 聚合全球平均
df_global_avg = df['meta_genre'].value_counts(normalize=True).reset_index()
df_global_avg.columns = ['Genre', 'Percentage']
df_global_avg['Country'] = 'Global Average'  # 添加一个虚拟的国家名

# 合并数据
df_plot = pd.concat([
    df_countries_agg.rename(columns={'country': 'Country', 'meta_genre': 'Genre'}), 
    df_global_avg
], ignore_index=True)

# 第3步：应用布局 (App Layout - 英文)
app.layout = dbc.Container([
    html.H1("Top 50 Music Tastes: A Global Dashboard (2019)", style={'textAlign': 'center', 'marginTop': '20px'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H4("Select a Country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country.title(), 'value': country} for country in sorted(df_plot['Country'].unique())],
                value='Global Average',  # 默认值
                clearable=False
            )
        ], width=4),
        dbc.Col([
            dcc.Graph(id='genre-detail-chart')
        ], width=8)
    ])
], fluid=True)

# 第4步：回调函数 (The Callback - 英文)
@app.callback(
    Output('genre-detail-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_chart(selected_country):
    # (关键) 定义美化字典
    color_map = {
        'Other': 'lightgrey',
        'Pop': 'gold',
        'Hip Hop / Rap': 'deepskyblue',
        'Latin': 'red',
        'Electronic / Dance': 'purple',
        'R&B': 'orange',
        'Rock': 'darkred',
        'Indie / Alternative': 'green',
        'Brazilian': 'yellowgreen',
        'K-Pop': 'pink',
        'J-Pop': 'magenta',
        'South Asian': 'brown'
    }

    # 数据过滤
    data_to_plot = df_plot[df_plot['Country'] == selected_country]
    title_text = f"Top 50 Genre Share: {selected_country.title()}"

    # 创建图表 (fig)
    fig = px.bar(
        data_to_plot,
        x='Percentage',
        y='Country',  # 这将是 'Global Average' 或 'Japan' 等
        color='Genre',
        orientation='h',
        barmode='stack',
        title=title_text,
        template='simple_white',
        color_discrete_map=color_map,
        category_orders={'Genre': list(color_map.keys())} # 确保颜色和顺序一致
    )

    # 美化图表 (Aesthetics - 英文)
    fig.update_layout(
        xaxis=dict(ticksuffix='%', range=[0, 1], title='Percentage of Top 50 Songs'),
        yaxis=dict(showticklabels=False, title=''),  # 隐藏Y轴标签
        legend_title_text='Meta-Genre',
        font=dict(family="Arial", size=12),
        margin=dict(l=10, r=10, t=50, b=10), # 调整边距
        height=400  # 设置固定高度
    )
    fig.update_traces(hovertemplate='<b>%{data.name}</b>: %{x:.1%}<extra></extra>')

    return fig

# 第5步：运行应用
if __name__ == '__main__':
    app.run_server(debug=True)