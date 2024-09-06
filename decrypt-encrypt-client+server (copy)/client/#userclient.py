import asyncio
import websockets


bad_characters = ['(', ')', '&', '@', '#', '{', '}', ' ', '%', '!', '$', '*']

def is_valid_username(username):
    if re.search(r"[()&@#{}\s]", username): #checks for speecial cracters
        return False
    return True


def is_valid_password(password):
    if ' ' in password: #Simple check for spaces in the password
        return False
    return True

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        #Main menu to select action
        action = int(input("Would you like to register? /PRESS 1/, Login /PRESS 2/: "))
        
        if action == 1:
            await websocket.send("register")
            print(await websocket.recv()) #Server response for registration
            username = input("Enter a username to register: ")
            if len(username) < 5:
                print("make sure your username minimum 5 letters long")
                return

            elif len(username) > 14:
                return
                print("make sure your username isn't longer then 14 letters")

            elif ' ' in username: #checks for space in username
                print("You can't have space in your username")
                return

            elif any(char in username for char in bad_characters):
                print(f"Your username can't contain any of these characters: {', '.join(bad_characters)}")
                return

            else:
                print("your username is alright")
            await websocket.send(username)
            server_response = await websocket.recv()
            print(server_response)

            if "Username available" in server_response:
            #Continue to ask for password with all checks
                while True:
                    password = input("Enter a password: ")
                    if len(password) < 8:
                        print("Make sure your password is at least 8 characters long.")
                    elif not any(char.isdigit() for char in password):
                        print("Make sure your password contains at least one number.")
                    elif len(password) > 24:
                        print("Make sure your password isn't longer than 24 characters.")
                    elif not any(char.isupper() for char in password):
                        print("Make sure your password contains at least one uppercase letter.")
                    else:
                        print("Your password seems fine.")
                        await websocket.send(password)
                        print(await websocket.recv()) #Registration success
                        break #Exit loop after valid password input

        elif action == 2:
            await websocket.send("login")
            print(await websocket.recv()) #Server response for login
            username = input("Enter your username to log in: ")
            await websocket.send(username)
            server_response = await websocket.recv()
            print(server_response)

            if "Username found" in server_response:
                #Continue to ask for password USEFULLL!!!!
                password = input("Enter your password: ")
                await websocket.send(password)
                print(await websocket.recv())  #Login success or failure Rip

if __name__ == "__main__":
    asyncio.run(main())
