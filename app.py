
import streamlit as st
import requests

st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌦️ Weather Forecast App")
st.write("Check the current weather of any city.")

city = st.text_input("Enter City Name", "Vijayawada")

weather_codes = {
    0: "Clear Sky ☀️",
    1: "Mainly Clear 🌤️",
    2: "Partly Cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Foggy 🌫️",
    51: "Light Drizzle 🌦️",
    61: "Rain 🌧️",
    63: "Moderate Rain 🌧️",
    65: "Heavy Rain 🌧️",
    71: "Snow ❄️",
    80: "Rain Showers 🌦️",
    95: "Thunderstorm ⛈️"
}

if st.button("Get Weather"):

    if city.strip():

        try:
            # Get city coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"

            geo_response = requests.get(
                geo_url,
                params={"name": city, "count": 1},
                timeout=15
            )

            geo_data = geo_response.json()

            if "results" in geo_data:

                location = geo_data["results"][0]

                latitude = location["latitude"]
                longitude = location["longitude"]

                # Get current weather
                weather_url = "https://api.open-meteo.com/v1/forecast"

                weather_response = requests.get(
                    weather_url,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": (
                            "temperature_2m,"
                            "relative_humidity_2m,"
                            "apparent_temperature,"
                            "weather_code,"
                            "wind_speed_10m"
                        ),
                        "timezone": "auto"
                    },
                    timeout=15
                )

                weather_data = weather_response.json()
                current = weather_data["current"]

                st.success(
                    f"Weather in {location['name']}, "
                    f"{location.get('country', '')}"
                )

                st.metric(
                    "🌡️ Temperature",
                    f"{current['temperature_2m']} °C"
                )

                code = current["weather_code"]

                st.subheader(
                    weather_codes.get(code, "Weather condition unavailable")
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "💧 Humidity",
                        f"{current['relative_humidity_2m']}%"
                    )

                    st.metric(
                        "🌡️ Feels Like",
                        f"{current['apparent_temperature']} °C"
                    )

                with col2:
                    st.metric(
                        "💨 Wind Speed",
                        f"{current['wind_speed_10m']} km/h"
                    )

                st.caption(
                    f"Last updated: {current['time']}"
                )

            else:
                st.error("City not found. Please enter a valid city.")

        except requests.exceptions.RequestException:
            st.error("Unable to connect. Please check your internet connection.")

        except (KeyError, IndexError, ValueError):
            st.error("Weather information is currently unavailable.")

    else:
        st.warning("Please enter a city name.")
