import asyncio
import websockets
from scraper import GetAvailability

async def hello(websocket, path):
    message = await websocket.recv()
    print('Message received:')
    print(message)

    if message != 'Availability please!':
        response = 'Sorry, I can\'t help you with that!'
        await websocket.send(response)
        print('Message rejected\r\n')
        return
    
    print('Request for availability recieved, fetching availability now...')
    availability = GetAvailability()
    if len(availability) < 1:
        await websocket.send('Try again later')
        print('\r\nError while scraping Camp Brain. Try again later.\r\n\r\n')
        return

    response = 'availability'
    for num in availability:
        response += (' ' + num)
    await websocket.send(response)
    print('\r\nResponse sent!\r\n\r\n')
    return

start_server = websockets.serve(hello, "192.168.1.9", 2520)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()