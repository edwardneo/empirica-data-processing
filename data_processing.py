import json

def filter_by(key, value, events):
    """Filter list of dicts 'events', where dict event has key-value pair ('key', 'value')"""
    return list(filter(lambda event: event[key] == value, events))

def parse_attr(event):
    """Isolate specific keys in attribute event 'event'"""
    cleaned_event = {}
    
    for key in ['key', 'val']:
        if key in event:
            cleaned_event[key] = event[key]
    
    if event['createdByID'] in ids:
        cleaned_event['player'] = ids[event['createdByID']]
    else:
        cleaned_event['player'] = ''
    
    return cleaned_event

def parse_action(action):
    """Convert action event 'action' to string"""
    if action['val'] == 'null':
        return ''
    val = json.loads(action['val'])
    if val['type'] == 'move':
        return f"{action['player']} move: {val['position']}"
    if val['type'] == 'collect':
        return f"{action['player']} collect: {val['item']}"
    if val['type'] == 'drop':
        return f"{action['player']} drop: {val['item']}"


# Open file
with open('tajriba.json', 'r') as data_file:
    lines = data_file.readlines()
    data = list(map(json.loads, lines))

# Remove version setting
events = list(filter(lambda event: 'version' not in event, data))

# Obtain player IDs
ids = {}
for event in filter_by('kind', 'Participant', events):
    ids[event['obj']['id']] = event['obj']['Identifier']

# Isolate attribute setting events
attr_events = list(map(lambda event: event['obj'], filter_by('kind', 'Attribute', events)))

# Isolate specific keys in attribute events
cleaned_attr_events = list(map(parse_attr, attr_events))

datatype = input('What data would you like (actions/boards)? ')

if datatype == 'actions':
    # Convert actions to string form
    moves = list(map(parse_action,
            filter(lambda action: action['val'] != 'null',
                    filter_by('key', 'action', cleaned_attr_events)
                )
            )
        )
    
    for move in moves: print(move)
    
elif datatype == 'boards':
    # Isolate boards
    boards = list(map(lambda board_event: json.loads(board_event['val']), filter(lambda action: True, filter_by('key', 'board', cleaned_attr_events))))
    
    for board in boards: print(board)