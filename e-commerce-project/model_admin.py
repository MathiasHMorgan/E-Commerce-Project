from model_user import User
import os


class Admin(User):
    """
    Admin class with default values for each instance inheriting from User class
    """

    def __init__(self, user_id="u_0000000000", user_name="my_admin", user_password="admin1234", user_register_time='00-00-0000_00:00:00', user_role="admin"):
        super().__init__(user_id, user_name, user_password,
                         user_register_time, user_role)  # inherit values from user

    def __str__(self):
        admin_str = super().__str__()

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        # append each instance
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(admin_str + "\n")

        return admin_str
