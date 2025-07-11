# Import necessary modules #Hey this is justing for testing1 # Hey this is change number 2 # 3rd changes
from AppOpener import close, open as appopen  # Import functions to open and close apps.
from webbrowser import open as webopen # Import web browser functionality.
from pywhatkit import search, playonyt  # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values  # Import to load environment variables.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
from os import system  # Import for system-related commands.
from groq import Groq  # Import for AI Chat functionalities.
import webbrowser  # Import webbrowser for opening URLs.
import subprocess  # Import subprocess for interacting with the system.
import requests  # Import requests for making HTTP requests.
import keyboard  # Import keyboard for keyboard-related actions.
import asyncio  # Import asyncio for asynchronous programming.
import os  # Import os for handling system functionalities.
import urllib.parse
# Load environment variables from the .env file.
env_vars = dotenv_values('.env')
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API Key.

# Define CSS classes for parsing specific elements in the HTML content.
classes = ['LZCkZb', 'hgKElc', 'LTKOO sYfrc', 'Z2OLfc', 'gT0LQe', 'p5AXld', 'FzvWSb WpPnmf', 'pc1qee', 'tw-Data-text tw-text-small tw-ta',
           't6vMe', 'OSUGdc tLX0dc', 'vLY9Gd', 'webanswers-webanswers_table__webanswers-table__webanswers-table', 'dDoNo ikb4Bb gsrt', 'sXLaOe',
           't7xgfc', 'vYfGig', 'qvWpe', 'kno-rdesc', 'sPZ2Bd']

# Define a user-agent for managing web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq Client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
messages=[]
SystemChatBot = [{"role":"system","content":f"Hello I am {os.environ['Username']}, You're a content writer. You have to write content like letter"}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor,File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user","content":f"{prompt}"})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot+messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer= ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>","")
        messages.append({"role":"assistant","content":Answer})
        return Answer
    Topic: str = Topic.replace("Content","")
    ContentByAI= ContentWriterAI(Topic)

    file_name = rf"Data\{Topic.lower().strip().replace(' ', '_')}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(file_name)
    return True


def YoutubeSearch(Topic):
    Url4Search=f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href') for link in links]

        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results")
            return None
        
        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                link = links[0]
                webopen.open(link)
            else:
                print("No link found")
        else:
            print("Failed to get search results")

        return True

        

def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app,match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False

        
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume mute")
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")
    if command == "mute":
        mute()
    elif command =="unmute":
        unmute()
    elif command =="volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands:list[str]):
    funcs=[]
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file"==command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general"):
            pass
        elif command.startswith("realtime"):
            pass
        elif command.startswith("close"):
            fun=asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith ("youtube search"):
            fun = asyncio.to_thread(YoutubeSearch,command.removeprefix("youtube search"))
            funcs.append(fun)
        elif command.startswith("system"):
            fun = asyncio.to_thread(System, command.removeprefix("system"))
            funcs.append(fun)
        else:
            print(f"No function Found. For {command}")

    results= await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result

async def Automation(commands:list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

# if __name__ == "__main__":
#     asyncio.run(Automation(["open facebook","open instagram","play afsanay","content song for me"]))
