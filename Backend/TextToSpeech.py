

import os
import asyncio
import edge_tts
import pygame
import random
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice") # Get the AssistantVoice from the environment variables.

# Function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" # The path where the speech file will be saved

    # Check if the audio file already exists
    if os.path.exists(file_path):
        os.remove(file_path) # Remove it to avoid overwriting errors

    # Create TTS object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
    await communicate.save(file_path) # Save the generated speech as an .mp3 file

# Function to manage Text-to-Speech functionality
def TTS(TText, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(TText))

            # Initialize pygame
            pygame.mixer.init()

            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play() # Play the audio

            # Loop until the audio stops playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False: # Check if the external function returns True
                    break
                pygame.time.Clock().tick(10) # Limit the loop to 10 ticks per second

            return True # Return True if the audio played successfully

        except Exception as e: # Handle any exceptions during the process
            print(f"Error in TTS: {e}")
        finally:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    if len(Data) > 4 and len(Text) >= 250:
        TTS("".join(Text.split(".")[0:2])+ ". "+random.choice(responses), func)
    else:
        TTS(Text, func)

if __name__=="__main__":
    while True:
        TextToSpeech(input("enter the text:"))
