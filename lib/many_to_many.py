from datetime import datetime

class Book:
    all_books = []

    def __init__(self, title):
        self.title = title
        self.add_to_all_books()

    def add_to_all_books(self):
        self.__class__.all_books.append(self)


class Author:
    all_authors = []

    def __init__(self, name):
        self.name = name
        self.contracts_list = []
        self.add_to_all_authors()

    def add_to_all_authors(self):
        self.__class__.all_authors.append(self)

    def contracts(self):
        return self.contracts_list

    def books(self):
        return [contract.book for contract in self.contracts_list]

    def sign_contract(self, book, date, royalties):
        if not isinstance(book, Book):
            raise Exception("Invalid book type. Must be an instance of the Book class.")
        if not isinstance(royalties, int):
            raise Exception("Invalid royalties type. Must be an integer.")
        if not (0 <= royalties <= 100):
            raise Exception("Invalid royalties value. Must be between 0 and 100 (inclusive).")

        contract = Contract(self, book, date, royalties)
        self.contracts_list.append(contract)
        return contract

    def total_royalties(self):
        return sum(contract.royalties for contract in self.contracts_list)


class Contract:
    all_contracts = []

    def __init__(self, author, book, date, royalties):
        self.author = author
        self.book = book
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.royalties = float(royalties)

        self.__class__.all_contracts.append(self)

    @property
    def net_royalties(self):
        # Calculate net royalties based on daily sales
        sales_per_day = 1  # Assume 1 sale per day
        total_days = (datetime.now().date() - self.date).days
        net_royalties = sales_per_day * total_days * self.royalties / 365.25  # Consider leap years
        return round(net_royalties, 2)

    def __repr__(self):
        return f"<Contract {self.book.title}>"

    def add_to_all_contracts(self):
        self.__class__.all_contracts.append(self)

    @classmethod
    def contracts_by_date(cls, date):
        return [contract for contract in cls.all_contracts if contract.date == date]


# Example usage:
try:
    # Create books and authors
    book1 = Book("Book 1")
    book2 = Book("Book 2")
    author1 = Author("Author 1")
    author2 = Author("Author 2")

    # Sign contracts
    contract1 = author1.sign_contract(book1, "2022-03-15", 10)
    contract2 = author1.sign_contract(book2, "2022-03-15", 15)
    contract3 = author2.sign_contract(book1, "2022-03-20", 8)

    # Accessing methods
    print("Author 1's contracts:")
    for contract in author1.contracts():
        print(f"{contract.book.title} - {contract.date} - Royalties: {contract.royalties}%")

    print("\nAuthor 1's books:")
    for book in author1.books():
        print(book.title)

    print(f"\nAuthor 1's total royalties: {author1.total_royalties()}%")

    print("\nContracts on 2022-03-15:")
    for contract in Contract.contracts_by_date("2022-03-15"):
        print(f"{contract.author.name} - {contract.book.title} - Royalties: {contract.royalties}%")

except Exception as e:
    print(f"Exception: {str(e)}")
