import threading
import random
import time


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        if self.lock.locked() and self.balance >= 500:
            self.lock.release()
        for _ in range(100):
            self.lock.acquire()
            r = random.randint(50, 500)
            self.balance += r
            print(f'Пополнение: {r}. Баланс: {self.balance}')
            self.lock.release()
            time.sleep(0.001)

    def take(self):
        for _ in range(100):
            self.lock.acquire()
            r = random.randint(50, 500)
            print(f'Запрос на {r}')
            if r <= self.balance:
                self.balance -= r
                print(f"Снятие {r}, баланс {self.balance}")
                self.lock.release()
                time.sleep(0.001)
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.release()
                time.sleep(0.001)


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
