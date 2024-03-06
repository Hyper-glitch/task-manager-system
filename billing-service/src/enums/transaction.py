from enum import Enum


class TransactionTypes(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    PAYMENT = "PAYMENT"
