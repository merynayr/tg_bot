import dash
from dash import html, dcc, Output, Input
import plotly.graph_objs as go
import pandas as pd
from _05_patterns.ema_crossover_strategy import detect_ema_crossover_signals  # твоя функция сигналов

# Загружаем данные с EMA
df = pd.read_csv('./_03_datasets/BTCUSDT_15.csv', parse_dates=['timestamp'])

from _04_indicators.ema_calculator import calculate_ema  # функция расчёта EMA
from _05_patterns.ema_crossover_strategy import detect_ema_crossover_signals

# Считаем EMA с периодами 9 и 21
df = calculate_ema(df, period=9)
df = calculate_ema(df, period=21)

# После этого вычисляем сигналы
df = detect_ema_crossover_signals(df)

# Инициализация приложения
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Trading Bot Dashboard', style={'textAlign': 'center'}),
    html.Div(id='status', children='Статус бота: Активен', style={'textAlign': 'center', 'fontSize': 20}),
    html.Div(id='balance', style={'textAlign': 'center', 'fontSize': 20}),
    
    dcc.Graph(id='price-graph'),
    
    # Таймер для обновления данных (например, каждую минуту)
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)
])

@app.callback(
    [Output('balance', 'children'),
     Output('price-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    # При реальном боте сюда надо подгружать актуальные данные и баланс из API
    
    # Для примера баланс берем последний close
    balance_text = f"Текущий баланс: {df['close'].iloc[-1]:.2f} USDT"
    
    # График цены, EMA и сигналов
    buy_signals = df[df['signal'] == 1]
    sell_signals = df[df['signal'] == -1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['EMA_9'], mode='lines', name='EMA 9', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['EMA_21'], mode='lines', name='EMA 21', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=buy_signals['timestamp'], y=buy_signals['close'], mode='markers', name='Buy Signal',
                             marker=dict(symbol='triangle-up', color='green', size=12)))
    fig.add_trace(go.Scatter(x=sell_signals['timestamp'], y=sell_signals['close'], mode='markers', name='Sell Signal',
                             marker=dict(symbol='triangle-down', color='red', size=12)))

    fig.update_layout(template='plotly_dark', title='Цена и сигналы EMA Crossover',
                      xaxis_title='Время', yaxis_title='Цена')

    return balance_text, fig

if __name__ == '__main__':
    app.run_server(debug=True)
