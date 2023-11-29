import random
from datetime import datetime

events = {}  # Global dictionary to store events

def create_event(arguments, author):
    parts = arguments.split(' ', 3)
    if len(parts) < 4:
        return "Invalid event format. Please use 'create event {name} {description} {date} {time}'"
    name, description, date, time = parts
    # Validate and parse date and time here

    events[name] = {'description': description, 'date': date, 'time': time, 'users': [author]}

    event_datetime = parse_date_time(date, time)
    if event_datetime is None:
        return "Invalid date and time format. Please use 'MM/DD/YYYY HH:MMAM/PM' format."

    return f"Event '{name}' created successfully."

def join_event(event_name, author):
    if event_name not in events:
        return f"No event found with name '{event_name}'"
    if author not in events[event_name]['users']:
        events[event_name]['users'].append(author)
        print(f"User {author} joined event {event_name}")  # Debugging line
        print(events)
    return f"You have joined the event '{event_name}'"



def parse_date_time(date, time):
    try:
        return datetime.strptime(f'{date} {time}', '%m/%d/%Y %I:%M%p')
    except ValueError:
        return None

def list_events():
    if not events:
        return "No events available."
    return "\n".join([f"{name}: {info['description']} on {info['date']} at {info['time']}" for name, info in events.items()])

def handle_response(message, author_id=None) -> str:
    message = message[23:]
    message = message.lower()

    if message.startswith('create event'):
        return create_event(message[len('create event '):], author_id)
    elif message.startswith('join event'):
        return join_event(message[len('join event '):], author_id)
    elif message == 'events':
        return list_events()
    if message == '!help':
        return "`1.type \"create event {name} {description} {date} {time}\" to create a new event and add a description \n2.type \"join event {name} to join an event and be reminded about the event \n3. type \"events\" tp display a list of joinable events`"
    return "Please make sure there are no spaces or invalid characters present in your message"