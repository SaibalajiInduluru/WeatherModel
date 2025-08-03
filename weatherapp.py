import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Professional Weather Forecasting",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional weather app theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f0f8f0 0%, #e8f5e8 100%);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #1e3a1e;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #4a7c4a;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Current weather card */
    .current-weather-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        border: 2px solid #90ee90;
        position: relative;
        overflow: hidden;
    }
    
    .current-weather-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #90ee90, #2d5a2d, #90ee90);
    }
    
    /* Weather info styling */
    .weather-info {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    .temperature {
        font-size: 4.5rem;
        font-weight: bold;
        color: #1e3a1e;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .city-name {
        font-size: 2.2rem;
        color: #1e3a1e;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .weather-description {
        font-size: 1.5rem;
        color: #4a7c4a;
        margin-bottom: 1rem;
        text-transform: capitalize;
        font-weight: 500;
    }
    
    .last-updated {
        font-size: 0.9rem;
        color: #7a9a7a;
        font-style: italic;
        margin-top: 1rem;
    }
    
    /* Forecast cards */
    .forecast-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .forecast-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #90ee90;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .forecast-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .forecast-time {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e3a1e;
        margin-bottom: 0.5rem;
    }
    
    .forecast-temp {
        font-size: 2rem;
        font-weight: bold;
        color: #2d5a2d;
        margin: 0.5rem 0;
    }
    
    .forecast-desc {
        font-size: 0.95rem;
        color: #4a7c4a;
        text-transform: capitalize;
        margin-bottom: 1rem;
    }
    
    /* Weather details grid */
    .weather-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .detail-card {
        background: #f8fff8;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #90ee90;
        transition: transform 0.2s ease;
    }
    
    .detail-card:hover {
        transform: scale(1.05);
    }
    
    .detail-title {
        font-size: 1rem;
        color: #4a7c4a;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .detail-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1e3a1e;
    }
    
    .detail-unit {
        font-size: 1rem;
        color: #7a9a7a;
    }
    
    /* Chart styling */
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        border: 2px solid #90ee90;
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a1e;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #90ee90;
        border-radius: 15px;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1e3a1e;
        box-shadow: 0 0 0 3px rgba(144, 238, 144, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #90ee90 0%, #2d5a2d 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7dd87d 0%, #1e3a1e 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* Error message styling */
    .error-message {
        background: linear-gradient(135deg, #ffe6e6 0%, #ffcccc 100%);
        border: 2px solid #ff9999;
        border-radius: 15px;
        padding: 1.5rem;
        color: #cc0000;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Weather icon styling */
    .weather-icon {
        width: 120px;
        height: 120px;
        margin: 1rem 0;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .forecast-icon {
        width: 60px;
        height: 60px;
        margin: 0.5rem 0;
    }
    
    /* Professional badge */
    .pro-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, #2d5a2d 0%, #1e3a1e 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Weather API configuration
API_KEY = "2547a922b65c5329229c5cd56f2da85d"  # Your OpenWeatherMap API key
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_current_weather(city_name, api_key):
    """
    Fetch current weather data from OpenWeatherMap API
    
    Args:
        city_name (str): Name of the city
        api_key (str): OpenWeatherMap API key
    
    Returns:
        dict: Current weather data or error message
    """
    try:
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "City not found. Please check the city name and try again."}
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your API configuration."}
        else:
            return {"error": f"API request failed with status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

def get_weather_forecast(city_name, api_key):
    """
    Fetch 5-day weather forecast data from OpenWeatherMap API
    
    Args:
        city_name (str): Name of the city
        api_key (str): OpenWeatherMap API key
    
    Returns:
        dict: Forecast data or error message
    """
    try:
        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Forecast API request failed with status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

def format_time(timestamp):
    """Format timestamp to readable time"""
    return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")

def format_date_time(timestamp):
    """Format timestamp to readable date and time"""
    return datetime.fromtimestamp(timestamp).strftime("%a, %b %d - %I:%M %p")

def display_current_weather(weather_data):
    """
    Display current weather information in a professional layout
    
    Args:
        weather_data (dict): Current weather data from API
    """
    city_name = weather_data['name']
    country = weather_data['sys']['country']
    temperature = round(weather_data['main']['temp'])
    feels_like = round(weather_data['main']['feels_like'])
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    visibility = weather_data.get('visibility', 0) / 1000  # Convert to km
    weather_description = weather_data['weather'][0]['description']
    weather_icon = weather_data['weather'][0]['icon']
    sunrise = format_time(weather_data['sys']['sunrise'])
    sunset = format_time(weather_data['sys']['sunset'])
    
    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@4x.png"
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Main weather card with city, icon, temperature, description
    st.markdown(f"""
    <div class="current-weather-card">
        <div class="pro-badge">Pro Weather</div>
        <div class="weather-info">
            <div class="city-name">{city_name}, {country}</div>
            <img src="{icon_url}" alt="Weather Icon" class="weather-icon">
            <div class="temperature">{temperature}°C</div>
            <div class="weather-description">{weather_description}</div>
            <div class="last-updated">Last updated: {current_time}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Weather details using Streamlit columns instead of HTML
    st.markdown("### Weather Details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Feels Like", f"{feels_like}°C")
        st.metric("Sunrise", sunrise)
        
    with col2:
        st.metric("Humidity", f"{humidity}%")
        st.metric("Sunset", sunset)
        
    with col3:
        st.metric("Wind Speed", f"{wind_speed} m/s")
        
    with col4:
        st.metric("Pressure", f"{pressure} hPa")
        st.metric("Visibility", f"{visibility:.1f} km")

def display_hourly_forecast(forecast_data):
    """
    Display next 24 hours forecast
    
    Args:
        forecast_data (dict): Forecast data from API
    """
    st.markdown('<div class="chart-title">Next 24 Hours Forecast</div>', unsafe_allow_html=True)
    
    # Get next 8 forecasts (24 hours, every 3 hours)
    forecasts = forecast_data['list'][:8]
    
    # Create forecast cards
    cols = st.columns(4)
    for i, forecast in enumerate(forecasts):
        col_index = i % 4
        
        with cols[col_index]:
            time_str = format_time(forecast['dt'])
            temp = round(forecast['main']['temp'])
            description = forecast['weather'][0]['description']
            icon = forecast['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            
            # Determine if it's today, tomorrow, etc.
            forecast_date = datetime.fromtimestamp(forecast['dt'])
            current_date = datetime.now()
            
            if forecast_date.date() == current_date.date():
                day_label = "Today"
            elif forecast_date.date() == (current_date + timedelta(days=1)).date():
                day_label = "Tomorrow"
            else:
                day_label = forecast_date.strftime("%a")
            
            st.markdown(f"""
            <div class="forecast-card">
                <div class="forecast-time">{day_label}</div>
                <div class="forecast-time" style="font-size: 0.9rem; color: #7a9a7a;">{time_str}</div>
                <img src="{icon_url}" alt="Weather Icon" class="forecast-icon">
                <div class="forecast-temp">{temp}°C</div>
                <div class="forecast-desc">{description}</div>
            </div>
            """, unsafe_allow_html=True)

def create_temperature_chart(forecast_data):
    """
    Create an interactive temperature chart for the next 5 days
    
    Args:
        forecast_data (dict): Forecast data from API
    """
    forecasts = forecast_data['list']
    
    # Extract data for chart
    times = []
    temperatures = []
    feels_like = []
    humidity = []
    
    for forecast in forecasts[:40]:  # Next 5 days (every 3 hours)
        dt = datetime.fromtimestamp(forecast['dt'])
        times.append(dt)
        temperatures.append(forecast['main']['temp'])
        feels_like.append(forecast['main']['feels_like'])
        humidity.append(forecast['main']['humidity'])
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Temperature Forecast (°C)', 'Humidity Forecast (%)'),
        vertical_spacing=0.1
    )
    
    # Temperature traces
    fig.add_trace(
        go.Scatter(
            x=times, y=temperatures,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#2d5a2d', width=3),
            marker=dict(size=6, color='#90ee90', line=dict(width=2, color='#2d5a2d'))
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=times, y=feels_like,
            mode='lines+markers',
            name='Feels Like',
            line=dict(color='#4a7c4a', width=2, dash='dash'),
            marker=dict(size=4, color='#7dd87d')
        ),
        row=1, col=1
    )
    
    # Humidity trace
    fig.add_trace(
        go.Scatter(
            x=times, y=humidity,
            mode='lines+markers',
            name='Humidity',
            line=dict(color='#1e3a1e', width=3),
            marker=dict(size=6, color='#90ee90', line=dict(width=2, color='#1e3a1e'))
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        showlegend=True,
        plot_bgcolor='rgba(240,248,240,0.5)',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color="#1e3a1e"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(144,238,144,0.3)',
        title_font_size=14
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(144,238,144,0.3)',
        title_font_size=14
    )
    
    return fig

def display_error_message(error_message):
    """Display error message in a professional way"""
    st.markdown(f"""
    <div class="error-message">
        <strong>Weather Alert:</strong> {error_message}
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # App header
    st.markdown('<h1 class="main-header">Professional Weather Forecasting</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced Weather Intelligence • Real-time Data • Professional Insights</p>', unsafe_allow_html=True)
    
    # Create input section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        city_name = st.text_input(
            "",
            placeholder="Enter city name for professional weather analysis...",
            help="Enter any city name to get comprehensive weather data and forecasts"
        )
        
        search_button = st.button("Get Professional Forecast", use_container_width=True)
    
    # Process weather request
    if search_button and city_name:
        with st.spinner('Analyzing weather patterns...'):
            # Get current weather and forecast data
            current_weather = get_current_weather(city_name, API_KEY)
            forecast_data = get_weather_forecast(city_name, API_KEY)
        
        # Display results
        if current_weather and 'error' not in current_weather:
            # Display current weather
            display_current_weather(current_weather)
            
            # Display forecast if available
            if forecast_data and 'error' not in forecast_data:
                st.markdown("---")
                display_hourly_forecast(forecast_data)
                
                st.markdown("---")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">5-Day Temperature & Humidity Trends</div>', unsafe_allow_html=True)
                
                # Create and display temperature chart
                chart = create_temperature_chart(forecast_data)
                st.plotly_chart(chart, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Forecast data temporarily unavailable. Showing current conditions only.")
        else:
            error_message = current_weather.get('error', 'Unable to fetch weather data')
            display_error_message(error_message)
    
    elif search_button and not city_name:
        display_error_message("Please enter a city name to access professional weather data.")
    
    # Professional footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #4a7c4a; padding: 2rem; background: white; border-radius: 15px; margin: 2rem 0; border: 1px solid #90ee90;">
        <h3 style="color: #1e3a1e; margin-bottom: 1rem;">Professional Weather Intelligence</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 1rem 0;">
            <div>
                <strong>Real-time Data</strong><br>
                Live weather conditions updated every 10 minutes
            </div>
            <div>
                <strong>Advanced Analytics</strong><br>
                5-day forecasts with hourly precision
            </div>
            <div>
                <strong>Global Coverage</strong><br>
                Weather data for 200,000+ cities worldwide
            </div>
            <div>
                <strong>Interactive Charts</strong><br>
                Professional visualizations and trends
            </div>
        </div>
        <p style="margin-top: 2rem; font-style: italic;">
            Powered by OpenWeatherMap API • Built for Professional Use
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()