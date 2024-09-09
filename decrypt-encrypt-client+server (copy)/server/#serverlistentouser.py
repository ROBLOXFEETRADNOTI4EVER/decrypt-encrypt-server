import asyncio
import websockets

file_path = "/home/blueberry/Desktop/localhost/server/usernames-passwords.txt"

def username_exits(username):
    #checks if the username exists in the database
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()  #check for same username in txt
            for line in lines:
                line = line.strip()  
               
                if line.startswith(f"Username: {username},"):  # Exact match check
                    return True  # Username found
    except FileNotFoundError:
        #if the file not exist, return False (username is new)
        return False
    return False

async def handle_client(websocket, path):
    try:
        #Receive the username
        username = await websocket.recv()
        print(f"Server received: {username}")
        if username_exits(username):
            #if the username exists, inform the client and exit
            response = "Username already exists. You must log in."
            await websocket.send(response)
            await websocket.send("YOU ALRADY REGISTERED IDIOT")
            print(f"Username {username} already exists. Prompting login.")
            return  # exit after sending message
            #so when this line executes then the user shouldN't be registered
        await websocket.send("Username-avilable")
        print("Waiting for password")
        # Receive the password from the client
        passwordd = await websocket.recv()
        print(f"Received password: {passwordd}")
        with open(file_path, "a") as file:
            file.write(f"Username: {username}, Password: {passwordd}\n")
        await websocket.send("Registration successful.")
    except Exception as e:
        print(f"An error occurred: {e}")
# Start the websocket server on localhost:8765 idk how to host
start_server = websockets.serve(handle_client, "localhost", 8765)

# loop thingy
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server started on ws://localhost:8765")
    asyncio.get_event_loop().run_forever()
