SEPARATOR = "--------------------"

def register():
    print("регистрация")

def login():
    print("вход")

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