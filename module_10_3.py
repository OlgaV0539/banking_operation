import threading
import random
import time


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            with self.lock:
                r = random.randint(5, 500)
                self.balance += r
                print(f"Пополнение: {r}. Баланс: {self.balance}")
                if self.balance >= 500 and self.lock.locked():
                    pass
            time.sleep(0.001)

    def take(self):
        for _ in range(100):
            r = random.randint(5, 500)
            print(f"Запрос на {r}")
            with self.lock:
                if r <= self.balance:
                    self.balance -= r
                    print(f"Снятие {r}, баланс {self.balance}")
                else:
                    print(f"Запрос отклонён, недостаточно средств")


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
