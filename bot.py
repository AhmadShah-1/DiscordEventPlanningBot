import discord
import responses
from responses import events
from responses import parse_date_time

import asyncio
from datetime import datetime, timedelta

# Create an Intents object with desired permissions
intents = discord.Intents.default()
intents.messages = True  # For handling messages
intents.dm_messages = True  # If you want to handle direct messages

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)



async def reminder_task(client):
    await client.wait_until_ready()
    while not client.is_closed():
        current_time = datetime.now()  # Consider timezone if needed
        for event_name, details in events.items():
            event_time = parse_date_time(details['date'], details['time'])
            if event_time:
                time_difference = (event_time - current_time).total_seconds()
                if -300 <= time_difference <= 30:
                    for user_id in details['users']:
                        try:
                            user = await client.fetch_user(user_id)
                            await user.send(f"Reminder: Event '{event_name}' is starting soon!")
                            print(f"Reminder sent to {user_id} for event {event_name}")
                        except Exception as e:
                            print(f"Error sending reminder to {user_id}: {e}")
            else:
                print(f"Error parsing date/time for event {event_name}")
        await asyncio.sleep(60)



def run_discord_bot():
    Token = 'MTE3NDAzMjg5MjU4Njg5NzQ4MA.G_Vk4I.D-robdV1cjyvP2kalVy1_uep1NJkh4QpSyitWw'
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):

        # Prevent bot from responding to its own messages
        if message.author == client.user:
            return

        # Get the message content and author's ID
        user_message = str(message.content)
        author_id = message.author.id  # Extract the author's ID
        response = responses.handle_response(user_message, author_id)
        await message.channel.send(response)

        # Check if the message is empty
        if not user_message:
            return

        # Handle private message requests
        if user_message.startswith('?'):
            user_message = user_message[1:].strip()  # Remove '?' and strip extra whitespace
            response = responses.handle_response(user_message)
            await message.author.send(response)  # Send a private message
            return

        # Handling 'create event' command
        if user_message.startswith('create event'):
            response = responses.create_event(user_message[len('create event '):], author_id)
            await message.channel.send(response)
            return

        if user_message.startswith('join event'):
            response = responses.join_event(user_message[len('join event '):].strip(), author_id)
            await message.channel.send(response)
            return

        # Default response for unhandled messages
        response = responses.handle_response(user_message)
        await message.channel.send(response)

        client.loop.create_task(reminder_task(client))
        client.run(Token)


    client.run(Token)


