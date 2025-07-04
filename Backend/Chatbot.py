from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars= dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistance")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key = GroqAPIKey)
messages = []
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot=[
    {"role":"system", "content": System}
]

try:
    with open(r"Data\ ChatLog.json", "r") as f:
        messages=load(f)
except FileNotFoundError:
    with open (r"Data\ ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
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

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Main chatbot function to handle user queries.
def Chatbot(Query):
    global messages  # Use global messages list

    try:
        # Load chat log from file once per call (optional if you want fresh from disk)
        with open("Data\ChatLog.json", "r") as f:
            messages = load(f)

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": Query})

        # Prepare full messages list with system, real-time info, and all previous messages
        api_messages = [
            {"role": "system", "content": System},
            {"role": "system", "content": RealtimeInformation()}
        ] + messages

        # Make a request to the API
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Specify the AI model to use.
            messages=api_messages,
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
        Answer = Answer.replace("<|s>", "")

        # Append the assistant's response to the chat log
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log to a JSON file
        with open("Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print("Error:", e)
        # Reset chat log in case of error (optional)
        with open("Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return Chatbot(Query)

# --- Main program ---
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(Chatbot(user_input))
