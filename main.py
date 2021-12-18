import datetime
import time as ti
import webbrowser as we

from time import sleep

import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
from newsapi import NewsApiClient


def command():
    # saying = input()
    r = sr.Recognizer()
    saying = ""
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            saying = r.recognize_google(r.listen(source), language="en-IN")
        except Exception as e:
            print(e)
            output("Say that again please...")
    return saying


def output(out):
    # print(out)
    engine.say(out)
    engine.runAndWait()


user = "Huzaifa"
assistant = "David"
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
output(f"Hello this is {assistant}")


def hello():
    hour = datetime.datetime.now().hour
    if (hour >= 6) and (hour < 12):
        output(f"Good Morning {user}")
    elif (hour >= 12) and (hour < 18):
        output(f"Good afternoon {user}")
    elif (hour >= 18) and (hour < 21):
        output(f"Good Evening {user}")
    output("How may i Assist you?")


def sendWhatMsg():
    user_list = {"user": "<use any phone number>"}
    try:
        output("To whom you want to send the message")
        name = command().lower()
        output("What is the message")
        we.open(
            "https://web.whatsapp.com/send?phone="
            + user_list[name]
            + "&text="
            + command()
        )
        sleep(6)
        pyautogui.press("enter")
        output("Message sent")
    except Exception as e:
        print(e)
        output("Unable to send the Message")


# you can get your weather api key from https://openweathermap.org/api
def weather():
    city = "Islamabad"
    api_key = "<your api key from https://openweathermap.org/api>"
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    ).json()
    temp = res["weather"][0]["description"]
    temp2 = res["main"]["temp"]
    output(
        f"Temprature is {format(temp2)} degree Celsius \n Weather is {format(temp)} in {city}"
    )


def news():
    # https://newsapi.org/account
    newsapi = NewsApiClient(
        api_key="<Your api key from # https://newsapi.org/account >"
    )
    output("What topic you need the news about")
    topic = command().lower()
    data = newsapi.get_top_headlines(q=topic, language="en", page_size=5)
    newsdata = data["articles"]
    for y in newsdata:
        output(y["description"])


def note():
    output("What is your idea?")
    data = command().title()
    output("You said me to remember this Idea: " + data)
    with open("data.txt", "a", encoding="Utf-8") as r:
        print(data, file=r)


hello()

while True:
    saying = command().lower()
    if "time" in saying:
        output("Current time is " + datetime.datetime.now().strftime("%I:%M"))
    elif "date" in saying:
        output(
            "Current date is "
            + str(datetime.datetime.now().day)
            + " "
            + str(datetime.datetime.now().month)
            + " "
            + str(datetime.datetime.now().year)
        )
    elif "message" in saying:
        sendWhatMsg()
    elif "search" in saying:
        output("What you want to search")
        we.open("https://www.google.com/search?q=" + command())
    elif "youtube" in saying:
        output("what you want to search on YouTube?")
        pywhatkit.playonyt(command())
    elif "weather" in saying:
        weather()
    elif "news" in saying:
        news()

    elif "covid" in saying:
        r = requests.get("https://coronavirus-19-api.herokuapp.com/all").json()
        output(
            f'Confirmed cases: {r["cases"]} \nDeaths: {r["deaths"]} \nRecovered {r["recovered"]}'
        )
    elif "developed" in saying:
        output("Huzaifa and huma made this incredible program")

    elif "joke" in saying:
        output(pyjokes.get_joke())
    elif "note" in saying:
        note()
    elif "remember" in saying:
        ideas = open("data.txt", "r")
        output(f"You said me to remember these ideas: \n{ideas.read()}")
    elif "screenshot" in saying:
        pyautogui.screenshot(str(ti.time()) + ".png").show()
    elif "cpu" in saying:
        output(f"Cpu is at {str(psutil.cpu_percent())}")
    elif "ok bye" in saying:
        hour = datetime.datetime.now().hour
        if (hour >= 21) and (hour < 6):
            output(f"Good Night {user}! Have a nice sleep")
        else:
            output(f"By {user}! You can call me back whenever you need!")
        quit()
