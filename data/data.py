import os

def save_user_to_file(username: str, user_id: int):
    user_folder = f'data/users/{user_id}'
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    with open(file_path, 'w') as file:
        file.write(f"Username: {username}\n")
        file.write(f"User ID: {user_id}\n")

def save_channel_info(user_id: int, channel_username: str, subscriber_count: int):
    user_folder = f'data/users/{user_id}'
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    with open(file_path, 'a') as file:
        file.write(f"Channel: {channel_username}\n")
        file.write(f"Subscribers: {subscriber_count}\n")

    os.makedirs('data/usernames/channels', exist_ok=True)
    with open('data/usernames/channels/channel.txt', 'a') as file:
        file.write(f"{channel_username}, Price: [Not set yet], Subscribers: {subscriber_count}\n")

def save_group_info(user_id: int, group_username: str, subscriber_count: int):
    user_folder = f'data/users/{user_id}'
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    with open(file_path, 'a') as file:
        file.write(f"Group: {group_username}\n")
        file.write(f"Subscribers: {subscriber_count}\n")

    os.makedirs('data/usernames/groups', exist_ok=True)
    with open('data/usernames/groups/groups.txt', 'a') as file:
        file.write(f"{group_username}, Price: [Not set yet], Subscribers: {subscriber_count}\n")

def save_bot_info(user_id: int, bot_username: str, subscriber_count: int):
    user_folder = f'data/users/{user_id}'
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    with open(file_path, 'a') as file:
        file.write(f"Bot: {bot_username}\n")
        file.write(f"Subscribers: {subscriber_count}\n")

    os.makedirs('data/usernames/bots', exist_ok=True)
    with open('data/usernames/bots/bots.txt', 'a') as file:
        file.write(f"{bot_username}, Price: [Not set yet], Subscribers: {subscriber_count}\n")

def get_user_info(user_id: int) -> str:
    user_folder = f'data/users/{user_id}'
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

def edit_info(user_id: int, edit_choice: str, new_info: str):
    user_folder = f'data/users/{user_id}'
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if edit_choice.lower() in line.lower():
                    file.write(f"{edit_choice}: {new_info}\n")
                else:
                    file.write(line)
    else:
        raise FileNotFoundError(f"No data found for user {user_id}")

def delete_info(user_id: int, delete_choice: str):
    user_folder = f'data/users/{user_id}'
    file_path = os.path.join(user_folder, f'{user_id}.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if delete_choice.lower() not in line.lower():
                    file.write(line)
    else:
        raise FileNotFoundError(f"No data found for user {user_id}")

