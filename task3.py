class Account:
    def __init__(self, id, balance, annual_rate):
        self.__id = id
        self.__balance = balance
        self.__annual_rate = annual_rate

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.__balance >= amount:
                self.__balance -= amount
            else:
                print("Insufficient balance.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.__balance

    def display(self):
        print(f"Account ID: {self.__id}, Balance: ${self.__balance}, Annual Rate: {self.__annual_rate}%")

class SavingsAccount(Account):
    def __init__(self, id, balance, annual_rate, min_balance):
        super().__init__(id, balance, annual_rate)
        self.__min_balance = min_balance

    def withdraw(self, amount):
        if self.get_balance() - amount >= self.__min_balance:
            super().withdraw(amount)
        else:
            print("Withdrawal denied.")

class CheckingAccount(Account):
    def __init__(self, id, balance, annual_rate, overdraft_limit):
        super().__init__(id, balance, annual_rate)
        self.__overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.get_balance() - amount >= -self.__overdraft_limit:
            super().withdraw(amount)
        else:
            print("Withdrawal denied.")


account = Account(1148489, 22222, 0.5)
account.withdraw(2500)
account.deposit(3000)
account.display()
