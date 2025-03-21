from repositories.author_repo import AuthorRepository

class AuthorService:
    @staticmethod
    def get_all_authors():
        authors =  AuthorRepository.get_all_authors()
        return [author.to_dict() for author in authors]

    @staticmethod
    def add_author(author):
        return AuthorRepository.add_author(author)
        
    @staticmethod
    def delete_author(author_id):
        return AuthorRepository.delete_author(author_id)
   