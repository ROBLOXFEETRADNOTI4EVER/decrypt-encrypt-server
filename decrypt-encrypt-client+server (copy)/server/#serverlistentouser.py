import asyncio
import websockets

file_path = "/home/blueberry/Desktop/decrypt-encrypt-client+server/server/usernames-passwords.txt"

def username_exists(username):
    #checks if suername in txt
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith(f"Username: {username},"):
                    return True
    except FileNotFoundError:
        
        return False
    return False

def verify_password(username, password):
    
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith(f"Username: {username},"):
                    saved_password = line.split("Password: ")[1]
                    if saved_password == password:
                        return True
    except FileNotFoundError:
       
        return False
    return False

def save_user_data(username, password):
   
    try:
        with open(file_path, "a") as file:  
            file.write(f"Username: {username}, Password: {password}\n")
            print(f"Saved {username} with password to file.")
    except Exception as e:
        print(f"Error saving user data: {e}")

async def handle_client(websocket, path):
    try:
        #Receive info from the clientpythonthingy (register or login)
        action = await websocket.recv()
        print(f"Server received action: {action}")

        if action == "register":
            #Registration process
            await websocket.send("Registering new user...")
            username = await websocket.recv()
            print(f"Register attempt for: {username}")

            if username_exists(username):
                await websocket.send("Username already exists. You must log in.")
                print(f"Username {username} already exists.")
                return #Exit after informing the client
            else:
                await websocket.send("Username available. Enter your password.")
                password = await websocket.recv()

                 #Save the new user's username and password
                save_user_data(username, password)

                await websocket.send("Registration successful.")
                print(f"User {username} registered successfully.")

        elif action == "login":
            #login process
            await websocket.send("Logging in...")
            username = await websocket.recv()
            print(f"Login attempt for: {username}")

            if username_exists(username):
                await websocket.send("Username found. Enter your password.")
                password = await websocket.recv()

                if verify_password(username, password):
                    await websocket.send("Login successful.")
                    print(f"User {username} logged in successfully.")
                else:
                    await websocket.send("Invalid password. Try again.")
                    print(f"User {username} provided an invalid password.")
            else:
                await websocket.send("Username not found. Please register.")
                print(f"Login failed. Username {username} not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

#Start the websocket server on localhost:8765
start_server = websockets.serve(handle_client, "localhost", 8765)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server started on ws://localhost:8765")
    asyncio.get_event_loop().run_forever()
