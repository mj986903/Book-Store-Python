from repositories.user_repo import UserRepository

class UserService:
    @staticmethod
    def register(user):
        return UserRepository.add_user(user)
    
    def login(user):
        return UserRepository.check_user(user)