from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_responses

# Load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Buster_Bot Setup
intents: Intents = Intents.default()
intents.message_contents = True #NOQA
clients: Client = Client(intents=intents)

# Message Functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_responses(user_message)
        await message.author.send(response) if is_private else message.channel.send(response)
    except Exception as e:
        print(e)

# Startup for the Buster_Bot
@Client.event
async def on_message(message: Message) -> None:
    if message.author == Client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


# Main Entry Point
def main() -> None:
    Client.run(token=TOKEN)

if __name__ == '__main__':
    main()