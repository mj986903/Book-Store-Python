from repository import BookRepository

class BookService:
    @staticmethod
    def get_all_books(currentPage,rowsPerPage,parsed_start_date,parsed_end_date,order_by="asc",order_attribute="id"):
        books,total_count = BookRepository.get_all_books((currentPage - 1) * rowsPerPage,rowsPerPage,parsed_start_date,parsed_end_date,order_by,order_attribute)
        total_pages = (total_count // rowsPerPage) + (1 if total_count % rowsPerPage > 0 else 0)

        if currentPage > total_pages and total_pages > 0:
            return None
        books_dict =  [book.to_dict() for book in books]
        data = {
            "currentPage": currentPage,
            "rowsPerPage": rowsPerPage,
            "totalPages": total_pages,
            "books": books_dict
        }
        return data
    
    @staticmethod
    def get_books_by_author(author_id,currentPage,rowsPerPage):
        books,total_count = BookRepository.get_books_by_author(author_id,(currentPage - 1) * rowsPerPage,rowsPerPage)
        total_pages = (total_count // rowsPerPage) + (1 if total_count % rowsPerPage > 0 else 0)

        if currentPage > total_pages and total_pages > 0:
            return None
        books_dict =  [book.to_dict() for book in books]
        data = {
            "currentPage": currentPage,
            "rowsPerPage": rowsPerPage,
            "totalPages": total_pages,
            "books": books_dict
        }
        return data

    @staticmethod
    def get_book(book_id):
        book = BookRepository.get_book(book_id)
        return book.to_dict() if book else None
    
    @staticmethod
    def search_book(title):
        book = BookRepository.search_book(title)
        return book.to_dict() if book else None
    
    @staticmethod
    def add_book(book):
        try:
            if BookRepository.get_book_by_isbn(book.isbn):
                return "isbn_exists"
            BookRepository.add_book(book)
            return "added"
        except:
            return None

    @staticmethod
    def update_book(book_id,data):
        book = BookRepository.get_book(book_id)

        if not book:
            return "not_found", None
        
        if "isbn" in data:
            existing_book = BookRepository.get_book_by_isbn(data["isbn"])
            if existing_book and existing_book.id != book.id:
                return "isbn_exists", None
            book.isbn = data["isbn"]

        if "title" in data:
            book.title = data["title"]

        if "price" in data:
            book.price = data["price"]

        if "author_id" in data:
            book.author_id = data["author_id"]

        BookRepository.add_book(book)
        return "update", book.to_dict()
    
    @staticmethod
    def delete_book(book_id):
        return BookRepository.delete_book(book_id)
    