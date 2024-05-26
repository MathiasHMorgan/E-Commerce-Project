from model_admin import Admin
from operation_customer import UserOperation


class AdminOperation:

    @staticmethod
    def register_admin(user_password="admin1234"):
        """
        This function creates an admin instance by calling the Admin class
        with the encrypted password
        :param user_password: password string hard coded into function
        """
        encrypted_password = AdminOperation.encrypt_admin(user_password)
        admin = Admin(user_password=encrypted_password)
        print(admin)

    @staticmethod
    def encrypt_admin(password):
        """
        This function encrypts the admin pasword so it does not apepar in plain text in the users file
        :param password: password string
        """
        return UserOperation.encrypt_password(password)
