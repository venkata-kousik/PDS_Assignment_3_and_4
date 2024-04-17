import requests
import dash
from dash import html
import dash_table
import json

# Defining the list of cities
cities = ['New York', 'London', 'Tokyo', 'Sydney']

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Weather Dashboard", style={'textAlign': 'center'}), 
    dash_table.DataTable(
        id='weather-table',
        columns=[
            {'name': 'City', 'id': 'City'},
            {'name': 'Temperature (°C)', 'id': 'Temperature'},
            {'name': 'Humidity (%)', 'id': 'Humidity'},
            {'name': 'Weather', 'id': 'Weather'}
        ],
        data=[]
    )
])

# Callback to fetch and display weather information in the table
@app.callback(
    dash.dependencies.Output('weather-table', 'data'),
    [dash.dependencies.Input('weather-table', 'data_timestamp')]
)
def update_weather_table(timestamp):
    weather_data = []
    for city in cities:
        # Fetching data from the OpenWeatherMap API for each city
        api_key = '672ea6d08b9db372746ca4ecfe20b60a'
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(api_url)
        data = response.json()
        
        # Saving the JSON data in a separate file just for analysis
        with open(f'{city}_weather_data.json', 'w') as file:
            json.dump(data, file)

        # Extracting the useful information from the JSON response
        weather_data.append({
            'City': data.get('name', ''),
            'Temperature': f"{data.get('main', {}).get('temp', '')}°C",
            'Humidity': f"{data.get('main', {}).get('humidity', '')}%",
            'Weather': data.get('weather', [{}])[0].get('description', '')
        })
    return weather_data

if __name__ == '__main__':
    app.run_server(debug=True)
