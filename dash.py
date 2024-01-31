import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
import json
from flask import Flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Укажите URL FastAPI бэкенда
BACKEND_URL = "http://127.0.0.1:8002"

app.layout = html.Div(children=[
    # Форма регистрации
    html.Div(children=[
        html.H2("Register"),
        dcc.Input(id="register-username", type="text", placeholder="Username"),
        dcc.Input(id="register-password", type="password", placeholder="Password"),
        html.Button("Register", id="register-button"),
        html.Div(id="register-response")
    ]),

    # Форма входа в систему
    html.Div(children=[
        html.H2("Login"),
        dcc.Input(id="login-username", type="text", placeholder="Username"),
        dcc.Input(id="login-password", type="password", placeholder="Password"),
        html.Button("Login", id="login-button"),
        html.Div(id="login-response")
    ]),

    # Статус пользователя
    html.Div(children=[
        html.H2("User Info"),
        html.Button("Get User Info", id="userinfo-button"),
        html.Div(id="user-info")
    ])
    # тут могут быть дополнительные компоненты для предсказаний и прочего
])


@app.callback(
    Output("register-response", "children"),
    Input("register-button", "n_clicks"),
    [State("register-username", "value"), State("register-password", "value")],
)
def register(n_clicks, username, password):
    if not n_clicks:
        return ""
    response = requests.post(f"{BACKEND_URL}/api/auth/register", json={"username": username, "password": password})
    if response.status_code == 200:
        return "User registered successfully!"
    else:
        return "Registration failed."


@app.callback(
    Output("login-response", "children"),
    [Input("login-button", "n_clicks")],
    [State("login-username", "value"), State("login-password", "value")],
)
def login(n_clicks, username, password):
    if not n_clicks:
        return ""
    response = requests.post(f"{BACKEND_URL}/api/auth/login", json={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        # Сохраните токен в сессии или куки здесь, если необходимо
        return "User logged in successfully!"
    else:
        return "Login failed."


@app.callback(
    Output("user-info", "children"),
    Input("userinfo-button", "n_clicks"),
    prevent_initial_call=True  # Предотвращает вызов при загрузке страницы
)
def user_info(n_clicks):
    # Предполагается, что вы сохраняете токен аутентификации после входа
    token = "YOUR TOKEN HERE"  # Замените это на функцию, которая получает ваш токен
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/api/auth/me", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return json.dumps(user_info, indent=2)
    else:
        return "Failed to fetch user info."


# Добавьте дополнительные callback здесь для взаимодействий с другими компонентами Dash

if __name__ == '__main__':
    app.run_server(debug=True)
