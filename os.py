import os
import time
import threading
import msvcrt
import ctypes
import keyboard
import sys


BLUE = '\033[34m'
GREEN = '\033[32m'
LIGHTCYAN = '\033[96m'
ENDC = '\033[0m'
BRIGHTBLACKBG = '\033[100m'
BLACK = '\033[30m'
BRIGHTWHITEBG = '\033[107m'

def set_console_title_and_icon(title, icon_path):
    ctypes.windll.kernel32.SetConsoleTitleW(title)
    
    # Load the icon
    icon = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, 0x00000010 | 0x00000002)
    
    # Set the icon
    ctypes.windll.user32.SendMessageW(ctypes.windll.kernel32.GetConsoleWindow(), 0x80, 0, icon)

# Usage example:
set_console_title_and_icon("PyOS Version 1", "assets/icon.ico")


os.system('cls')
print(f"{LIGHTCYAN}PyOS V1{ENDC}")



current_directory = os.curdir
previous_directory = None

def show_prompt():
    return f"\n{current_directory}\ $ > "

def print_word_by_word(text):
    for word in text.split():
        print(word, end=' ', flush=True)
        time.sleep(0.1)  # Adjust the delay as needed
    print()


def format_size(size):
    # Function to format file size for better readability
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def command_cat():
    file_name = input("Enter the filename: ")

    file_path = os.path.join(current_directory, file_name)
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def command_dir():
    files_and_folders = os.listdir(current_directory)

    # Filter out system files
    filtered_files = [item for item in files_and_folders if not item.startswith("os.")]

    # Filter out hidden files and folders
    hidden_items = ['assets']
    visible_items = [item for item in filtered_files if item not in hidden_items]

    # Display folders
    folders = [item for item in visible_items if os.path.isdir(os.path.join(current_directory, item))]
    print_word_by_word(f"{BRIGHTBLACKBG}{BLACK}Folders:{ENDC}")
    if folders:
        for folder in folders:
            folder_path = os.path.join(current_directory, folder)
            folder_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
            formatted_size = format_size(folder_size)
            print_word_by_word(f"{BLUE}{folder}{ENDC} {LIGHTCYAN}({formatted_size}){ENDC}")
    else:
        print_word_by_word("None")

    # Display non-system files with size
    non_system_files = [item for item in visible_items if os.path.isfile(os.path.join(current_directory, item))]
    print_word_by_word(f"{BRIGHTBLACKBG}{BLACK}Files:{ENDC}")
    if non_system_files:
        for file_name in non_system_files:
            file_path = os.path.join(current_directory, file_name)
            size = os.path.getsize(file_path)
            formatted_size = format_size(size)
            print_word_by_word(f"{GREEN}{file_name}{ENDC} {LIGHTCYAN}({formatted_size}){ENDC}")
    else:
        print_word_by_word("None")



def command_clock():
    stop_clock = threading.Event()
    print("\nPress Escape to stop the clock\n")
    def update_clock():
        while not stop_clock.is_set():
            os.system("cls")
            print(time.strftime(f"{LIGHTCYAN}%d | %m | %Y{ENDC}, {BLUE}%H:%M:%S{ENDC}"))
            time.sleep(1)

    clock_thread = threading.Thread(target=update_clock)
    clock_thread.start()


    while True:
        if msvcrt.kbhit() and ord(msvcrt.getch()) == 27:  # 27 is the ASCII code for Escape
            os.system("cls")
            break

    stop_clock.set()
    clock_thread.join()

def command_fol(folder_name):
    folder_path = os.path.join(current_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    print_word_by_word(f"Folder '{folder_name}' created")

def command_cd(folder_name):
    global current_directory, previous_directory
    if folder_name == ".." or folder_name == "...":
        if previous_directory is not None:
            current_directory, previous_directory = previous_directory, current_directory
            print_word_by_word(f"Changed directory to '{current_directory}'")
        else:
            print_word_by_word("Error: No previous directory")
    else:
        new_directory = os.path.join(current_directory, folder_name)

        if os.path.exists(new_directory) and os.path.isdir(new_directory):
            previous_directory = current_directory
            current_directory = new_directory
            print_word_by_word(f"Changed directory to '{folder_name}'")
        else:
            print_word_by_word(f"Error: '{folder_name}' is not a valid directory")

def command_help():
    print(f"Available Commands:\n{BRIGHTWHITEBG}{BLACK}fol - Create a folder\ncd - Move to a directory (cd dir) \nclock - Shows time and date\ndir - Shows available directories and folders\nmake - Create an empty file\nnano - Edit a file\ncat - View contents of a file.\nexit - Exits PyOS\nrestart - Restarts PyOS{ENDC}")

# def command_make():
#     file_name = input("Enter the filename: ")
#     file_path = os.path.join(current_directory, file_name)

#     lines_of_code = []
#     print_word_by_word("Enter lines of code (Press Escape to finish):")

#     while True:
#         if msvcrt.kbhit() and ord(msvcrt.getch()) == 27:  # 27 is the ASCII code for Escape
#             break
#         line = input()
#         lines_of_code.append(line)

#     with open(file_path, 'w') as file:  # Open in write mode ('w') to create or overwrite the file
#         file.write('\n'.join(lines_of_code) + '\n')  # Write the entered lines to the file

#     print_word_by_word(f"Notepad created/updated: '{file_name}'")

def command_make():
    file_name = input("Enter the filename: ")
    file_path = os.path.join(current_directory, file_name)

    with open(file_path, 'w') as file:
        file.write('')

    print_word_by_word(f"File {file_name} created!")

restricted_files = ['icon.ico', 'os.py', 'os.bat']

def command_nano():
    file_name = input("Enter the file name: ")
    
    # Check if the file is restricted
    if file_name in restricted_files:
        print(f"You are not allowed to edit {file_name}.")
        return

    file_path = os.path.join(current_directory, file_name)

    try:
        # Check if the file exists; if not, create a new one
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

        # Read the existing content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Allow the user to edit the content
        print(f"Editing file: {file_name}.\n{BRIGHTBLACKBG}{BLACK}Ctrl+X - Save                               {ENDC}")

        user_input = ""
        cursor_position = 0
        while True:
            char = msvcrt.getch().decode('utf-8')

            if char == '\x18':  # Ctrl+X (ASCII code 24)
                break
            elif char == '\r':  # Enter key (ASCII code 13)
                print()
                user_input += '\n'
                cursor_position += 1
            elif char == '\x08':  # Backspace key (ASCII code 8)
                if cursor_position > 0:
                    # Move the cursor back and delete the character
                    print('\b \b', end='', flush=True)
                    user_input = user_input[:cursor_position - 1] + user_input[cursor_position:]
                    cursor_position -= 1
            else:
                print(char, end='', flush=True)
                user_input = user_input[:cursor_position] + char + user_input[cursor_position:]
                cursor_position += 1
            

        # Write the edited content back to the file
        with open(file_path, 'w') as file:
            file.write(user_input)

        print(f"\nFile '{file_name}' saved.")

    except Exception as e:
        print(f"An error occurred: {e}")




def command_exit():
    print_word_by_word("Exiting the OS. Goodbye!")
    exit()

def command_restart():
    print_word_by_word("Restarting the OS.")
    os.system("python os.py") & exit()

def main():
    while True:
        user_input = input(show_prompt())
        command_parts = user_input.split(" ", 1)
        command_name = command_parts[0].lower()

        if command_name == "dir":
            command_dir()
        elif command_name == "clock":
            command_clock()
        elif command_name == "fol":
            if len(command_parts) == 2:
                command_fol(command_parts[1])
            else:
                print_word_by_word("Error: 'fol' command requires a folder name")
        elif command_name == "cd":
            if len(command_parts) == 2:
                command_cd(command_parts[1])
            else:
                print_word_by_word("Error: 'cd' command requires a folder name")
        elif command_name == "make":
            command_make()
        elif command_name == "cls":
            os.system("cls")
        elif command_name == "cat":
            command_cat()
        elif command_name == "nano":
            command_nano()
        elif command_name == "exit":
            command_exit()
        elif command_name == "restart":
            command_restart()
        elif command_name == "help":
            command_help()
        else:
            print_word_by_word(f"Error: Unknown command '{command_name}'")


if __name__ == "__main__":
    main()
