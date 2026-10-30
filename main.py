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
                    user_menu(user_found)
                    return
        print("неверное имя пользователя или пароль. попытка", attempt + 1, "из 3")
        print("число попыток превышено. возврат в меню.")


def change_password():
    logins, emails = load_existing()
    login = input("введите имя пользователя для смены пароля: ").strip()
    if login not in logins:
        print("имя пользователя не найдено.")
        return
    new_password = ask_password()
    users = []
    with open(USERS_FILE, encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 3:
                if parts[0] == login:
                    users.append(f"{parts[0]}:{parts[1]}:{new_password}\n")
                else:
                    users.append(line)
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        file.writelines(users)
    print("пароль успешно изменен.")

def view_profile():
    login = input("введите имя пользователя для просмотра профиля: ").strip()
    with open(USERS_FILE, encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 3 and parts[0] == login:
                print(f"Профиль пользователя: {parts[0]}")
                print(f"Email: {parts[1]}")
                return
    print("имя пользователя не найдено.")

def delete_account():
    login = input("введите имя пользователя для удаления аккаунта: ").strip()
    password = input("введите пароль для подтверждения: ").strip()
    user_found = False
    password_correct = False
    with open(USERS_FILE, encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 3 and parts[0] == login:
                user_found = True
                if parts[2] == password:
                    password_correct = True
                break

    if not user_found:
        print("имя пользователя не найдено.")
        return

    if not password_correct:
        print("неправильный пароль.")
        return

    users = []
    with open(USERS_FILE, encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 3 and parts[0] != login:
                users.append(line)
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        file.writelines(users)
    print("аккаунт успешно удален.")

def user_menu(user):
    while True:
        print(SEPARATOR)
        print("1. просмотреть профиль")
        print("2. сменить пароль")
        print("3. выйти из аккаунта")
        print("4. удалить аккаунт")
        print(SEPARATOR)

        choice = input("выберите действие: ").strip()

        if choice == "3":
            print("выход")
            break
        elif choice == "1":
            view_profile()
        elif choice == "2":
            change_password()
        elif choice == "4":
            delete_account()
        else:
            print("неверный выбор, попробуйте снова")

        

def show_menu():
    actions = {"1": register, "2": login}

    while True:
        print(SEPARATOR)
        print("1. регистрация")
        print("2. вход")
        print("0. выйти из программы")
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
