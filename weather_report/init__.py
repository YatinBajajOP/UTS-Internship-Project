import requests
import streamlit as st


def weather_data(query):
	res = requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
	return res.json()


def print_weather(result, city):
	st.write("{}'s temperature: {}°C ".format(city, result['main']['temp']))
	st.write("Wind speed: {} m/s".format(result['wind']['speed']))
	st.write("Description: {}".format(result['weather'][0]['description']))
	st.write("Weather: {}".format(result['weather'][0]['main']))


def weather(name):
	city = name
	print()
	try:
		query = 'q='+city
		w_data = weather_data(query)
		print_weather(w_data, city)
		print()
	except:
		print('City name not found...')
