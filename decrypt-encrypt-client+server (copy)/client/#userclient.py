import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Ask user for their username
        username = input("Enter a username: ")
        # Sends  username to server
        await websocket.send(username)
        print(f'Client sent: {username}')



        # Receive the server's response for access control
        access_response = await websocket.recv()
        print(f"Server response: {access_response}")  
        # Handle    server response
        if access_response == "AD":  # Access Denied
            print("Username already exists. You must log in")
            return  #Exit after sending message
        elif access_response == "Username-avilable":  # Access Granted
    #Continue to ask for password
            password = input("Enter a password: ")
            if len(password) < 8:
                print("Make sure your password is at least 8 characters long.")
            elif not any(char.isdigit() for char in password):
                print("Make sure your password contains at least one number.")
            elif len(password) > 24:
                print("Make sure your password isn't longer then 24 characters.")
            elif not any(char.isupper() for char in password):
                print("Make sure your password contains at least one uppercase letter.")
            else:
                print("Your password seems fine.")
                await websocket.send(password)
        else:
            print("Unexpected server response.")
#pray for stackoverflow
if __name__ == "__main__":
    asyncio.run(hello())
