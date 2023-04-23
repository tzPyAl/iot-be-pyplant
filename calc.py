def add(i:int, j:int):
    return i+j

class InsufincentFunds(Exception):
    pass

class Bank():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    def deposit(self, amount):
        self.balance += amount
    def widhdraw(self, amount):
        if amount > self.balance:
            raise InsufincentFunds("Insufince balance")
        self.balance -= amount
    def collect(self):
        self.balance *= 1.1
