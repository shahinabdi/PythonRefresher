"""
Online Banking System - Python Classes Exercise (Completed)

This project is a fully implemented example demonstrating key
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
        self._amount = amount
        self._type = trans_type
        self._timestamp = datetime.now()
        self._description = description

    def __str__(self) -> str:
        # User-friendly string representation of the transaction
        return (f"{self._timestamp.strftime('%Y-%m-%d %H:%M')} - "
                f"{self._type:10} - ${self._amount:,.2f} "
                f"({self._description})")

    def __repr__(self) -> str:
        # Developer-friendly representation
        return f"Transaction(amount={self._amount}, type='{self._type}')"


# --- Abstract Base Class for Account Holders ---
class AccountHolder(ABC):
    """Abstract base class for any entity that can hold a bank account."""
    
    # Class variable to track the total number of account holders created
    total_holders = 0

    def __init__(self, name: str, address: str, email: str):
        self._name = name
        self._address = address
        self._email = email
        self._holder_id = self._generate_holder_id()
        # Increment the class-level counter for each new instance
        AccountHolder.total_holders += 1

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @property
    def holder_id(self) -> str:
        # Read-only property
        return self._holder_id

    def _generate_holder_id(self) -> str:
        # Private method to generate a unique ID for the holder
        return f"HOLDER-{AccountHolder.total_holders + 1:04d}"

    @abstractmethod
    def get_holder_type(self) -> str:
        # Abstract method to be implemented by subclasses
        pass

    def __eq__(self, other) -> bool:
        # Two account holders are equal if they have the same holder_id
        if not isinstance(other, AccountHolder):
            return NotImplemented
        return self._holder_id == other._holder_id
    
    def __str__(self) -> str:
        # User-friendly string representation
        return f"{self.name} ({self.holder_id})"


# --- Concrete Subclasses for Account Holders ---
class IndividualClient(AccountHolder):
    """Represents a personal client."""
    def __init__(self, name: str, address: str, email: str, date_of_birth: datetime):
        super().__init__(name, address, email)
        self._date_of_birth = date_of_birth

    def get_holder_type(self) -> str:
        # Implement the abstract method
        return "Individual"


class BusinessClient(AccountHolder):
    """Represents a business client."""
    def __init__(self, name: str, address: str, email: str, company_name: str, tax_id: str):
        super().__init__(name, address, email)
        self._company_name = company_name
        self._tax_id = tax_id

    def get_holder_type(self) -> str:
        # Implement the abstract method
        return "Business"


# --- Abstract Base Class for Accounts ---
class Account(ABC):
    """Abstract base class for all bank accounts."""
    
    def __init__(self, holder: AccountHolder, initial_balance: float = 0.0):
        self._account_number = self._generate_account_number()
        self._holder = holder
        self._balance = initial_balance
        self._transaction_history = []
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
        # Private method to generate a random 10-digit account number string
        return ''.join(random.choices(string.digits, k=10))

    def _add_transaction(self, amount: float, trans_type: str, description: str = "") -> None:
        # Private method to create and add a transaction to the history
        transaction = Transaction(amount, trans_type, description)
        self._transaction_history.append(transaction)

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        # Abstract method for withdrawing money
        pass

    def deposit(self, amount: float) -> bool:
        # Method for depositing money (common for all account types)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._add_transaction(amount, TransactionType.DEPOSIT, "Client Deposit")
        return True

    def get_transaction_history(self) -> List[Transaction]:
        # Return a copy of the transaction history to prevent external modification
        return self._transaction_history.copy()

    def __str__(self) -> str:
        # User-friendly representation of the account
        return f"{self.__class__.__name__} ({self.account_number}) - Balance: ${self.balance:,.2f}"
    
    def __len__(self) -> int:
        # Return the number of transactions for this account
        return len(self._transaction_history)


# --- Concrete Subclasses for Accounts ---
class CheckingAccount(Account):
    """A standard checking account with an overdraft limit."""
    def __init__(self, holder: AccountHolder, initial_balance: float = 0.0, overdraft_limit: float = 100.0):
        super().__init__(holder, initial_balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        # Implement withdrawal logic, considering the overdraft limit
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance + self._overdraft_limit >= amount:
            self._balance -= amount
            self._add_transaction(amount, TransactionType.WITHDRAWAL, "Withdrawal")
            return True
        else:
            print("Withdrawal failed: Exceeds overdraft limit.")
            return False


class SavingsAccount(Account):
    """A savings account that accrues interest."""
    def __init__(self, holder: AccountHolder, initial_balance: float = 0.0, interest_rate: float = 0.015):
        super().__init__(holder, initial_balance)
        self._interest_rate = interest_rate

    def withdraw(self, amount: float) -> bool:
        # Implement withdrawal logic, no overdraft allowed
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance >= amount:
            self._balance -= amount
            self._add_transaction(amount, TransactionType.WITHDRAWAL, "Withdrawal")
            return True
        else:
            print("Withdrawal failed: Insufficient funds.")
            return False

    def apply_interest(self) -> None:
        # Calculate and deposit interest into the account
        interest_amount = self.balance * self._interest_rate
        if interest_amount > 0:
            self._balance += interest_amount
            self._add_transaction(interest_amount, TransactionType.INTEREST, f"Interest at {self._interest_rate:.2%}")
            print(f"Applied ${interest_amount:,.2f} interest to account {self.account_number}")


# --- Main Bank Class ---
class Bank:
    """Manages all clients, accounts, and bank-wide operations."""
    
    def __init__(self, name: str):
        self._name = name
        self._accounts = {}  # Store accounts by account number
        self._clients = {}   # Store clients by holder_id

    def open_account(self, holder: AccountHolder, account_type: str, initial_deposit: float, **kwargs) -> Optional[Account]:
        # Create a new account and add it to the bank's records
        if holder.holder_id not in self._clients:
            self._clients[holder.holder_id] = holder
        
        account = None
        if account_type.lower() == 'checking':
            account = CheckingAccount(holder, initial_deposit, **kwargs)
        elif account_type.lower() == 'savings':
            account = SavingsAccount(holder, initial_deposit, **kwargs)
        else:
            print(f"Invalid account type: {account_type}")
            return None
        
        self._accounts[account.account_number] = account
        return account

    def find_account(self, account_number: str) -> Optional[Account]:
        # Find and return an account by its number
        return self._accounts.get(account_number)

    def generate_statement(self, account_number: str) -> None:
        # Print a detailed statement for a specific account
        account = self.find_account(account_number)
        if not account:
            print("Account not found.")
            return

        print("-" * 60)
        print(f"Statement for Account: {account.account_number}")
        print(f"Holder: {account.holder.name} ({account.holder.get_holder_type()})")
        print(f"Current Balance: ${account.balance:,.2f}")
        print("-" * 60)
        print("Transaction History:")
        if not account.get_transaction_history():
            print("No transactions to display.")
        for transaction in account.get_transaction_history():
            print(transaction)
        print("-" * 60)

    @staticmethod
    def is_valid_account_number(acc_num: str) -> bool:
        # Static method to validate an account number format
        return len(acc_num) == 10 and acc_num.isdigit()
        
    @classmethod
    def create_national_bank(cls, name: str):
        # Class method to create a Bank instance with some default settings
        print(f"Initializing {name}, a trusted national institution.")
        return cls(name)

    def __len__(self) -> int:
        # The length of the bank is the number of accounts it holds
        return len(self._accounts)

    def __contains__(self, item: Union[Account, AccountHolder]) -> bool:
        # Check if an account or a client is in the bank's records
        if isinstance(item, Account):
            return item.account_number in self._accounts
        if isinstance(item, AccountHolder):
            return item.holder_id in self._clients
        return False


# --- Demonstration Function ---
def demonstrate_banking_system():
    """
    Function to demonstrate the features of the banking system.
    Create clients, open accounts, perform transactions, and print reports.
    """
    print("--- Setting up the Bank ---")
    my_bank = Bank.create_national_bank("Capital Trust Bank")

    print("\n--- Creating Clients ---")
    client1 = IndividualClient("Alice Smith", "123 Oak St", "alice@email.com", datetime(1990, 5, 15))
    client2 = BusinessClient("Bob's Burgers", "456 Pine Ave", "contact@bobsburgers.com", "Bob's Burgers LLC", "B-TAX-12345")
    print(f"Created client: {client1}")
    print(f"Created client: {client2}")
    print(f"Total account holders now: {AccountHolder.total_holders}")

    print("\n--- Opening Accounts ---")
    alice_checking = my_bank.open_account(client1, 'checking', 1000.0, overdraft_limit=250.0)
    bobs_savings = my_bank.open_account(client2, 'savings', 5000.0, interest_rate=0.02)
    print(f"Opened new account: {alice_checking}")
    print(f"Opened new account: {bobs_savings}")
    print(f"Bank now has {len(my_bank)} accounts.")

    print("\n--- Performing Transactions ---")
    print(f"Alice's initial balance: ${alice_checking.balance:,.2f}")
    alice_checking.deposit(200)
    print("Deposited $200.")
    alice_checking.withdraw(50)
    print("Withdrew $50.")
    print(f"Alice's balance: ${alice_checking.balance:,.2f}")
    
    print("\nAttempting to overdraw...")
    print("Attempting to withdraw $1500 (should fail)...")
    alice_checking.withdraw(1500) 
    print("Attempting to withdraw $1300 (should succeed with overdraft)...")
    alice_checking.withdraw(1300)
    print(f"Alice's new balance after overdraft: ${alice_checking.balance:,.2f}")
    
    print("\n--- Applying Interest ---")
    print(f"Bob's Burgers initial balance: ${bobs_savings.balance:,.2f}")
    bobs_savings.apply_interest()
    print(f"Bob's Burgers new balance: ${bobs_savings.balance:,.2f}")

    print("\n--- Generating Statements ---")
    my_bank.generate_statement(alice_checking.account_number)
    my_bank.generate_statement(bobs_savings.account_number)

    print("\n--- Testing Static Methods ---")
    valid_num = "1234567890"
    invalid_num = "12345"
    print(f"Is '{valid_num}' a valid account number? {Bank.is_valid_account_number(valid_num)}")
    print(f"Is '{invalid_num}' a valid account number? {Bank.is_valid_account_number(invalid_num)}")


if __name__ == "__main__":
    demonstrate_banking_system()
