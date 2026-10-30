import os
import re

SEPARATOR = "--------------------"
USERS_FILE = "data/users.txt"

LOGIN_RE = re.compile(r"[A-Za-z0-9_]{4,20}")
EMAIL_RE = re.compile(r"[^\s@:]+@[^\s@:.]+(\.[^\s@:.]+)+")
PASSWORD_RE = re.compile(r"(?=.*[A-Za-z])(?=.*\d).{8,}")

def load_existing():
    logins, emails = set(), set()
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 3:
                    logins.add(parts[0])
                    emails.add(parts[1])
    return logins, emails

def ask_login(logins):
    while True:
        login = input("введите имя пользователя: ").strip()
        if not LOGIN_RE.fullmatch(login):
            print("имя пользователя должно быть от 4 до 20 символов, только буквы, цифры и _")
            continue
        if login in logins:
            print("имя пользователя уже занято, попробуйте другое")
            continue
        return login

def ask_email(emails):
    while True:
        email = input("введите email: ").strip()
        if not EMAIL_RE.fullmatch(email):
            print("неверный формат email, попробуйте снова")
            continue
        if email in emails:
            print("email уже зарегистрирован, попробуйте другой")
            continue
        return email

def ask_password():
    while True:
        password = input("введите пароль: ").strip()
        if not PASSWORD_RE.fullmatch(password):
            print("пароль должен быть не менее 8 символов, содержать буквы и цифры")
            continue
        if password != input("повторите пароль: ").strip():
            print("пароли не совпадают, попробуйте снова")
            continue
        return password

def register():
    logins, emails = load_existing()

    login = ask_login(logins)
    email = ask_email(emails)
    password = ask_password()
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "a", encoding="utf-8") as file:
        file.write(f"{login}:{email}:{password}\n")
    print("регистрация успешна. здравствуйте, ", login)

def login():
    if not os.path.exists(USERS_FILE):
        print("нет зарегистрированных пользователей. сначала зарегистрируйтесь.")
        return
    
    for attempt in range(3):
        login = input("логин: ").strip()
        password = input("пароль: ").strip()
        user_found = None
        with open(USERS_FILE, encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 3 and parts[0] == login and parts[2] == password:
                    print(f"вход успешен. здравствуйте, {login}")
                    return
        print("неверное имя пользователя или пароль. попытка", attempt + 1, "из 3")
        print("число попыток превышено. возврат в меню.")
        

def show_menu():
    actions = {"1": register, "2": login}

    while True:
        print(SEPARATOR)
        print("1. регистрация")
        print("2. вход")
        print("0. выйти")
        print(SEPARATOR)

        choice = input("выберите действие: ").strip()

        if choice == "0":
            print("выход")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("неверный выбор, попробуйте снова")

if __name__ == "__main__":
    try:
        show_menu()
    except (KeyboardInterrupt, EOFError):
        print("выход")
