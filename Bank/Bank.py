import json


class BankApp:
    def __init__(self):
        self.users = {}  # Словарь пользователей
        self.accounts = {}  # Словарь счетов
        self.stocks = []  # Список акций
        self.current_user = None
        self.initialize_stocks()  # Инициализируем акции

    def initialize_stocks(self):
        # Добавление первоначальных акций в систему
        initial_stocks = [
            {'name': 'Газпром', 'price': 150.0, 'popularity': 80},
            {'name': 'Tesla', 'price': 250.0, 'popularity': 70},
            {'name': 'Intel', 'price': 120.0, 'popularity': 90},
            {'name': 'AMD', 'price': 300.0, 'popularity': 50},
            {'name': 'Apple', 'price': 180.0, 'popularity': 60},
        ]
        self.stocks.extend(initial_stocks)

    def register_user(self, username, password, role):
        if username in self.users:
            print("Ошибка: Пользователь уже существует.")
        else:
            self.users[username] = {
                'password': password,
                'role': role,
                'history': []
            }
            self.accounts[username] = {'balance': 1000.0}  # Инициализируем счёт с 1000 Дублонов
            print(f"Пользователь {username} зарегистрирован.")

    def login(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            print(f"Добро пожаловать, {username}!")
        else:
            print("Ошибка: Неверное имя пользователя или пароль.")

    def logout(self):
        if self.current_user:
            print(f"Пользователь {self.current_user} вышел из системы.")
            self.current_user = None

    def add_stock(self, stock):
        self.stocks.append(stock)
        print(f"Акция '{stock['name']}' добавлена.")

    def remove_stock(self, stock_name):
        for stock in self.stocks:
            if stock['name'].lower() == stock_name.lower():
                self.stocks.remove(stock)
                print(f"Акция '{stock_name}' удалена.")
                return
        print(f"Ошибка: Акция '{stock_name}' не найдена.")

    def edit_stock(self, stock_name):
        for stock in self.stocks:
            if stock['name'].lower() == stock_name.lower():
                print(f"Редактирование информации о акции '{stock_name}':")
                try:
                    stock['price'] = float(input("Введите новую цену: "))
                    stock['popularity'] = int(input("Введите новую популярность: "))
                    print(f"Акция '{stock_name}' обновлена.")
                except ValueError:
                    print("Ошибка: Введите корректные значения для цены и популярности.")
                return
        print(f"Ошибка: Акция '{stock_name}' не найдена.")

    def view_stocks(self):
        print("Доступные акции:")
        if not self.stocks:
            print("Нет доступных акций для просмотра.")
            return
        for index, stock in enumerate(self.stocks):
            print(
                f"{index + 1}: {stock['name']} - Цена: {stock['price']} Дублонов, Популярность: {stock['popularity']}")

    def filter_stocks(self):
        print("По какому критерию вы хотите отфильтровать акции?")
        print("1 - Популярность")
        print("2 - Цена")
        print("3 - Название")

        try:
            choice = int(input("Введите номер критерия (1-3): "))
            filtered_stocks = self.stocks

            if choice == 1:
                min_popularity = int(input("Введите минимальную популярность: "))
                filtered_stocks = list(filter(lambda x: x['popularity'] >= min_popularity, filtered_stocks))
            elif choice == 2:
                max_price = float(input("Введите максимальную цену: "))
                filtered_stocks = list(filter(lambda x: x['price'] <= max_price, filtered_stocks))
            elif choice == 3:
                keyword = input("Введите часть названия компании: ").strip()
                filtered_stocks = list(filter(lambda x: keyword.lower() in x['name'].lower(), filtered_stocks))
            else:
                print("Ошибка: Неверный выбор критерия.")
                return

            if filtered_stocks:
                print("Отфильтрованные акции:")
                for index, stock in enumerate(filtered_stocks):
                    print(
                        f"{index + 1}: {stock['name']} - Цена: {stock['price']} Дублонов, Популярность: {stock['popularity']}")
            else:
                print("Нет акций, соответствующих заданным критериям.")

        except ValueError:
            print("Ошибка: Введите корректное значение.")

    def view_account_balance(self):
        if self.current_user:
            balance = self.accounts[self.current_user]['balance']
            print(f"Текущий баланс пользователя {self.current_user}: {balance} Дублонов")
        else:
            print("Ошибка: Пользователь не авторизован.")

    def purchase_stock(self, stock_index):
        if self.current_user:
            if 0 <= stock_index < len(self.stocks):
                stock = self.stocks[stock_index]
                if self.accounts[self.current_user]['balance'] >= stock['price']:
                    self.accounts[self.current_user]['balance'] -= stock['price']
                    self.users[self.current_user]['history'].append(
                        f"Покупка: {stock['name']} за {stock['price']} Дублонов")
                    print(f"Вы успешно купили акцию '{stock['name']}' за {stock['price']} Дублонов.")
                else:
                    print("Ошибка: Недостаточно средств для покупки.")
            else:
                print("Ошибка: Неверный номер акции.")
        else:
            print("Ошибка: Пользователь не авторизован.")

    def view_user_history(self):
        if self.current_user:
            history = self.users[self.current_user]['history']
            print(
                f"История транзакций пользователя {self.current_user}: {history}" if history else "История транзакций пуста.")
        else:
            print("Ошибка: Пользователь не авторизован.")

    def update_account(self, new_password):
        if self.current_user:
            self.users[self.current_user]['password'] = new_password
            print("Пароль успешно изменён.")
        else:
            print("Ошибка: Пользователь не авторизован.")

    def analyze_statistics(self):
        total_purchases = 0
        total_spent = 0.0
        for user in self.users.values():
            for transaction in user['history']:
                if transaction.startswith("Покупка:"):
                    total_purchases += 1
                    amount = float(transaction.split("за")[1].strip().split()[0])
                    total_spent += amount
        if total_purchases > 0:
            avg_spent = total_spent / total_purchases
        else:
            avg_spent = 0.0
        print(f"Всего покупок: {total_purchases}, Средняя стоимость покупок: {avg_spent} Дублонов")

    def manage_users(self):
        print("1 - Создать пользователя")
        print("2 - Удалить пользователя")
        print("3 - Изменить пароль пользователя")
        choice = input("Выберите действие: ")
        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            role = input("Введите роль (пользователь/администратор): ")
            self.register_user(username, password, role)
        elif choice == '2':
            username = input("Введите имя пользователя для удаления: ")
            if username in self.users:
                del self.users[username]
                del self.accounts[username]
                print(f"Пользователь '{username}' удалён.")
            else:
                print("Ошибка: Пользователь не найден.")
        elif choice == '3':
            username = input("Введите имя пользователя для изменения пароля: ")
            if username in self.users:
                new_password = input("Введите новый пароль: ")
                self.users[username]['password'] = new_password
                print(f"Пароль пользователя '{username}' обновлён.")
            else:
                print("Ошибка: Пользователь не найден.")

    def run(self):
        while True:
            print("\nДобро пожаловать в банковское приложение!")
            if self.current_user is None:
                print("1. Регистрация")
                print("2. Вход")
                choice = input("Выберите действие: ")
                if choice == '1':
                    username = input("Введите имя пользователя: ")
                    password = input("Введите пароль: ")
                    role = input("Введите роль (пользователь/администратор): ")
                    self.register_user(username, password, role)
                elif choice == '2':
                    username = input("Введите имя пользователя: ")
                    password = input("Введите пароль: ")
                    self.login(username, password)
                else:
                    print("Ошибка: Неверный выбор действия.")
            else:
                print("\n1. Просмотреть акции")
                print("2. Фильтровать акции")

                if self.users[self.current_user]['role'] == 'пользователь':
                    print("3. Купите акцию")
                    print("4. Просмотреть баланс счёта")
                    print("5. Просмотреть историю транзакций")
                    print("6. Обновить пароль")
                    print("7. Выход")
                else:  # Для администратора
                    print("3. Выход")
                    print("4. Добавить акцию")
                    print("5. Удалить акцию")
                    print("6. Изменить акцию")
                    print("7. Просмотреть статистику")
                    print("8. Управление пользователями")

                choice = input("Выберите действие: ")

                if choice == '1':
                    self.view_stocks()
                elif choice == '2':
                    self.filter_stocks()
                elif choice == '3' and self.users[self.current_user]['role'] == 'пользователь':
                    try:
                        index = int(input("Введите номер акции для покупки: ")) - 1
                        self.purchase_stock(index)
                    except ValueError:
                        print("Ошибка: Введите корректный номер акции.")
                elif choice == '4' and self.users[self.current_user]['role'] == 'пользователь':
                    self.view_account_balance()
                elif choice == '5' and self.users[self.current_user]['role'] == 'пользователь':
                    self.view_user_history()
                elif choice == '6' and self.users[self.current_user]['role'] == 'пользователь':
                    new_password = input("Введите новый пароль: ")
                    self.update_account(new_password)
                elif choice == '4' and self.users[self.current_user]['role'] == 'администратор':
                    name = input("Введите название акции: ").strip()
                    try:
                        price = float(input("Введите цену акции: ").strip())
                        popularity = int(input("Введите популярность акции: ").strip())
                        self.add_stock({'name': name, 'price': price, 'popularity': popularity})
                    except ValueError:
                        print("Ошибка: Введите корректные значения для цены и популярности.")
                elif choice == '5' and self.users[self.current_user]['role'] == 'администратор':
                    stock_name = input("Введите название акции для удаления: ").strip()
                    self.remove_stock(stock_name)
                elif choice == '6' and self.users[self.current_user]['role'] == 'администратор':
                    stock_name = input("Введите название акции для редактирования: ").strip()
                    self.edit_stock(stock_name)
                elif choice == '7' and self.users[self.current_user]['role'] == 'администратор':
                    self.analyze_statistics()
                elif choice == '8' and self.users[self.current_user]['role'] == 'администратор':
                    self.manage_users()
                elif choice == '3':
                    self.logout()
                else:
                    print("Ошибка: Неверный выбор действия.")


if __name__ == "__main__":
    app = BankApp()
    app.run()