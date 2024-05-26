from model_user import User
import os


class Customer(User):
    """
    Customer class with default values for each instance with inheritance from User class
    """

    def __init__(self, user_id="", user_name="", user_password="", user_register_time='00-00-0000_00:00:00', user_role="customer", user_email="", user_mobile=""):
        super().__init__(user_id, user_name, user_password,
                         user_register_time, user_role)  # inherits values from User class
        self.user_email = user_email
        self.user_mobile = user_mobile

    def __str__(self):
        user_str = super().__str__()

        # add email and mobile values
        user_details = f', "user_email": "{self.user_email}", "user_mobile": "{self.user_mobile}"'
        customer_str = user_str[:-1] + user_details + \
            "}"  # add to values in class string

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        # append instance to file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(customer_str + "\n")

        return customer_str
