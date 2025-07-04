from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname= env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""
try:
    with open(r"Data\ Chatlog.json","r") as f:
        messages = load(f)
except:
    with open(f"Data\ Chatlog.json","w") as f:
        dump([],f)


def GoogleSearch(query):
    results=list(search(query,advanced=True,num_results=5))
    Answer = f"The search results ofr '{query}' are : \n[start]\n"

    for i in results:
        Answer += f'Title : {i.title}\n Description : {i.description} \n\n'
    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content":System},
    {"role":"user","content":"Hi"},
    {"role":"assistant","content":"Hello how can I help you?"}
]

def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes :{second} seconds.\n"
    return data

def RealTimeSearchEngine(prompt):
    global SystemChatBot, messages

    
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    # Append the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Prepare full messages list with system, real-time info, and all previous messages
    SystemChatBot.append({"role":"system","content":GoogleSearch(prompt)})

    # Make a request to the API
    completion = client.chat.completions.create(
        model="llama3-8b-8192",  # Specify the AI model to use.
        messages=SystemChatBot + [{"role":"system", "content":Information()}] + messages,
        max_tokens=1024,
        temperature=1,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the response
    Answer = Answer.strip().replace("<|s>", "")

    # Append the assistant's response to the chat log
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log to a JSON file
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Prompt: ")
        print(RealTimeSearchEngine(prompt))