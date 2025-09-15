"""
Online Banking System - Python Classes Exercise

This project is designed to test and demonstrate understanding of key
Object-Oriented Programming (OOP) concepts in Python.

Concepts covered:
- Class and Subclass Creation
- Inheritance and Polymorphism
- Abstract Base Classes (ABCs)
- Properties and Encapsulation
- Class, Static, and Instance Methods
- Special (Magic/Dunder) Methods like __str__, __eq__, __len__
- Composition (e.g., a Bank has Accounts)
- Exception Handling
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Union
import random
import string

# --- Helper Enum for Transaction Types ---
class TransactionType:
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    INTEREST = "INTEREST"
    FEE = "FEE"


# --- Transaction Class ---
class Transaction:
    """Represents a single transaction in an account."""
    def __init__(self, amount: float, trans_type: str, description: str = ""):
        # TODO: Initialize transaction attributes
        self._amount = amount
        self._type = trans_type
        # HINT: Use the datetime module to capture the current time
        self._timestamp = ... 
        self._description = description

    def __str__(self) -> str:
        # TODO: User-friendly string representation of the transaction
        # HINT: Use an f-string to format the timestamp, type, and amount.
        #       For the timestamp, self._timestamp.strftime('%Y-%m-%d %H:%M') is useful.
        #       For the amount, you can format it to two decimal places, e.g., f"${self._amount:,.2f}"
        return f"..."

    def __repr__(self) -> str:
        # TODO: Developer-friendly representation
        # HINT: A good repr shows how to recreate the object.
        return f"Transaction(amount={self._amount}, type='{self._type}')"


# --- Abstract Base Class for Account Holders ---
class AccountHolder(ABC):
    """Abstract base class for any entity that can hold a bank account."""
    
    # TODO: Class variable to track the total number of account holders created
    total_holders = 0

    def __init__(self, name: str, address: str, email: str):
        # TODO: Initialize instance attributes for the account holder
        self._name = name
        self._address = address
        self._email = email
        # HINT: Call the helper method to get a unique ID for this holder.
        self._holder_id = self._generate_holder_id()
        # HINT: Increment the class-level counter for each new instance created.
        ...

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        # TODO: Update the instance's name attribute with the new value
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @property
    def holder_id(self) -> str:
        # TODO: This property should be read-only (it has a getter but no setter).
        return self._holder_id

    def _generate_holder_id(self) -> str:
        # TODO: Private method to generate a unique ID for the holder
        # HINT: Use an f-string to combine a prefix like 'HOLDER-' with the zero-padded
        #       total_holders count. For example, f"{AccountHolder.total_holders + 1:04d}"
        #       will produce "0001", "0002", etc.
        return f"HOLDER-{...}"

    @abstractmethod
    def get_holder_type(self) -> str:
        # TODO: This abstract method must be implemented by any concrete subclass.
        pass

    def __eq__(self, other) -> bool:
        # TODO: Two account holders are equal if they have the same holder_id
        # HINT: First, check if 'other' is an instance of AccountHolder.
        #       If it is, compare their _holder_id attributes.
        if not isinstance(other, AccountHolder):
            return NotImplemented
        return ...
    
    def __str__(self) -> str:
        # TODO: User-friendly string representation
        # HINT: Return a string like "Alice Smith (HOLDER-0001)"
        return f"{self.name} ({self.holder_id})"


# --- Concrete Subclasses for Account Holders ---
class IndividualClient(AccountHolder):
    """Represents a personal client."""
    def __init__(self, name: str, address: str, email: str, date_of_birth: datetime):
        # TODO: Call the parent constructor and initialize subclass-specific attributes
        # HINT: Use super().__init__(...) to initialize the common attributes.
        super().__init__(name, address, email)
        self._date_of_birth = date_of_birth

    def get_holder_type(self) -> str:
        # TODO: Implement the abstract method from the parent class
        # HINT: Return a string that identifies this holder type, e.g., "Individual".
        return "..."


class BusinessClient(AccountHolder):
    """Represents a business client."""
    def __init__(self, name: str, address: str, email: str, company_name: str, tax_id: str):
        # TODO: Call the parent constructor and initialize subclass-specific attributes
        super().__init__(name, address, email)
        self._company_name = company_name
        self._tax_id = tax_id

    def get_holder_type(self) -> str:
        # TODO: Implement the abstract method
        return "..."


# --- Abstract Base Class for Accounts ---
class Account(ABC):
    """Abstract base class for all bank accounts."""
    
    def __init__(self, holder: AccountHolder, initial_balance: float = 0.0):
        # TODO: Initialize common account attributes
        self._account_number = self._generate_account_number()
        self._holder = holder
        self._balance = initial_balance
        self._transaction_history = []
        # HINT: If there's a positive initial balance, you should record it as the first transaction.
        if initial_balance > 0:
            self._add_transaction(initial_balance, TransactionType.DEPOSIT, "Initial Deposit")

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def account_number(self) -> str:
        return self._account_number
        
    @property
    def holder(self) -> AccountHolder:
        return self._holder

    def _generate_account_number(self) -> str:
        # TODO: Private method to generate a random 10-digit account number string
        # HINT: The 'string' module has `string.digits`. The 'random' module has `random.choices()`.
        #       You can generate a list of 10 random digits and then ''.join() them together.
        return ...

    def _add_transaction(self, amount: float, trans_type: str, description: str = "") -> None:
        # TODO: Private method to create and add a transaction to the history
        # HINT: 1. Create a new Transaction object.
        #       2. Append it to the self._transaction_history list.
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        # TODO: This method will be implemented differently by each subclass.
        pass

    def deposit(self, amount: float) -> bool:
        # TODO: Method for depositing money (common for all account types)
        # HINT: 1. Validate that the amount is positive. If not, raise a ValueError.
        #       2. Add the amount to the balance.
        #       3. Record the transaction using _add_transaction.
        #       4. Return True on success.
        return True

    def get_transaction_history(self) -> List[Transaction]:
        # TODO: Return a copy of the transaction history
        # HINT: Returning `self._transaction_history.copy()` prevents the original list
        #       from being modified by external code.
        return ...

    def __str__(self) -> str:
        # TODO: User-friendly representation of the account
        # HINT: "CheckingAccount (1234567890) - Balance: $1,250.50"
        return f"{self.__class__.__name__} ({self.account_number}) - Balance: ${self.balance:,.2f}"
    
    def __len__(self) -> int:
        # TODO: The length of an account should be its number of transactions.
        return len(...)


# --- Concrete Subclasses for Accounts ---
class CheckingAccount(Account):
    """A standard checking account with an overdraft limit."""
    def __init__(self, holder: AccountHolder, initial_balance: float = 0.0, overdraft_limit: float = 100.0):
        super().__init__(holder, initial_balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        # TODO: Implement withdrawal logic, considering the overdraft limit
        # HINT: 1. Check if the amount is positive. Raise ValueError if not.
        #       2. Check if the withdrawal is possible: (self.balance + self._overdraft_limit) >= amount.
        #       3. If possible, update the balance and record the transaction, then return True.
        #       4. If not possible, print an error message and return False.
        return False


class SavingsAccount(Account):
    """A savings account that accrues interest."""
    def __init__(self, holder: AccountHolder, initial_balance: float = 0.0, interest_rate: float = 0.015):
        super().__init__(holder, initial_balance)
        self._interest_rate = interest_rate

    def withdraw(self, amount: float) -> bool:
        # TODO: Implement withdrawal logic, no overdraft allowed
        # HINT: 1. Check if the amount is positive. Raise ValueError if not.
        #       2. Check for sufficient funds: self.balance >= amount.
        #       3. If sufficient, update balance and record the transaction, then return True.
        #       4. Otherwise, print an error and return False.
        return False

    def apply_interest(self) -> None:
        # TODO: Calculate and deposit interest into the account
        # HINT: 1. Calculate the interest amount (self.balance * self._interest_rate).
        #       2. If the interest is positive, add it to the balance.
        #       3. Record the interest transaction using _add_transaction.
        pass


# --- Main Bank Class ---
class Bank:
    """Manages all clients, accounts, and bank-wide operations."""
    
    def __init__(self, name: str):
        # TODO: Initialize bank attributes
        self._name = name
        # HINT: Use a dictionary to store accounts, with the account number as the key.
        self._accounts = {}
        # HINT: Use a dictionary to store clients, with the holder_id as the key.
        self._clients = {}

    def open_account(self, holder: AccountHolder, account_type: str, initial_deposit: float, **kwargs) -> Optional[Account]:
        # TODO: Create a new account and add it to the bank's records
        # HINT: 1. Add the holder to the bank's client dictionary if not already present.
        #       2. Use an if/elif/else block to check the 'account_type' string.
        #       3. Based on the type, instantiate the correct Account subclass (CheckingAccount or SavingsAccount).
        #       4. Add the new account object to the bank's accounts dictionary.
        #       5. Return the created account object.
        return None

    def find_account(self, account_number: str) -> Optional[Account]:
        # TODO: Find and return an account by its number
        # HINT: The .get() method on a dictionary is useful here as it returns None if the key is not found.
        return ...

    def generate_statement(self, account_number: str) -> None:
        # TODO: Print a detailed statement for a specific account
        # HINT: 1. Use self.find_account() to get the account object.
        #       2. If the account exists, print its details (holder name, balance).
        #       3. Loop through the account's transaction history and print each one.
        pass

    @staticmethod
    def is_valid_account_number(acc_num: str) -> bool:
        # TODO: Static method to validate an account number format
        # HINT: A valid account number should be 10 characters long AND contain only digits.
        #       The .isdigit() string method will be useful.
        return ...
        
    @classmethod
    def create_national_bank(cls, name: str):
        # TODO: Class method to create a Bank instance with some default settings
        # HINT: A class method receives the class itself (cls) as the first argument.
        #       It should create and return an instance of that class: return cls(name)
        return ...

    def __len__(self) -> int:
        # TODO: The length of the bank is the number of accounts it holds.
        return len(...)

    def __contains__(self, item: Union[Account, AccountHolder]) -> bool:
        # TODO: Check if an account or a client is in the bank's records
        # HINT: Use isinstance() to check if 'item' is an Account or an AccountHolder.
        #       Based on the type, check if its ID exists as a key in the
        #       corresponding dictionary (_accounts or _clients).
        return False


# --- Demonstration Function ---
def demonstrate_banking_system():
    """
    Function to demonstrate the features of the banking system.
    Create clients, open accounts, perform transactions, and print reports.
    """
    print("--- Setting up the Bank ---")
    # TODO: Use the Bank's class method to create an instance named 'my_bank'.
    my_bank = ...

    print("\n--- Creating Clients ---")
    # TODO: Create one IndividualClient and one BusinessClient.
    client1 = ...
    client2 = ...
    print(f"Created client: {client1}")
    print(f"Total account holders now: {AccountHolder.total_holders}")

    print("\n--- Opening Accounts ---")
    # TODO: Call my_bank.open_account() for each client. Create one checking and one savings account.
    alice_checking = ...
    bobs_savings = ...
    print(f"Opened new account: {alice_checking}")
    print(f"Bank now has {len(my_bank)} accounts.")

    print("\n--- Performing Transactions ---")
    # TODO: Call the .deposit() and .withdraw() methods on your account objects to test them.
    #       Try both successful and failed withdrawals.
    print("Depositing $200 into Alice's account...")
    ...
    print("Withdrawing $50 from Alice's account...")
    ...
    
    print("\nAttempting to overdraw...")
    # TODO: Try to withdraw more money than is available to test overdraft and insufficient funds.
    ...

    print("\n--- Applying Interest ---")
    # TODO: Call the .apply_interest() method on the savings account.
    ...
    print(f"Bob's Burgers new balance: ${bobs_savings.balance:,.2f}")

    print("\n--- Generating Statements ---")
    # TODO: Call the bank's generate_statement() method for one of the accounts.
    ...

    print("\n--- Testing Static Methods ---")
    # TODO: Call the static method Bank.is_valid_account_number() with both a valid and an invalid number.
    print(f"Is '1234567890' valid? ...")
    print(f"Is '12345' valid? ...")


if __name__ == "__main__":
    demonstrate_banking_system()
