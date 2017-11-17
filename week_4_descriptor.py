"""
descriptor takes commission from assignment to account
"""

class Value:
    def __init__(self):
        self.amount = 0

    def __get__(self, obj, obj_type):
        if obj is None:
            return self
        return self.amount
    
    def __set__(self, obj, amount):
        self.amount += (1 - obj.commission) * amount
        return self.amount


class Account:
    amount = Value()
    
    def __init__(self, commission):
        self.commission = commission


def main(commission, amount):
    new_account = Account(commission)
    new_account.amount = amount
    print(new_account.amount)


if __name__ == "__main__":
    commission = 0.1
    amount = 100
    main(commission, amount)
    main(0.2, 200)
    main(0.3, -100)
    print(Account.amount)