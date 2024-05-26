class IOInterface:

    @staticmethod
    def get_user_input(message, num_of_args) -> str:
        """
        This function takes in user inputs and splits the message
        based on a specified number of arguments. it handles instances
        where the entered arguments is greater or less than required
        :param message: string message entered by user
        :param num_of_args: number of arguments expected when message is split by a space
        """

        user_args = input(message).split()

        # if num args is less than user args append blank string to make up the difference
        if (len(user_args) < num_of_args):
            diff = num_of_args - len(user_args)
            user_args = user_args + [""] * diff
        # if num args is geater than user args slice user args to keep consistent amount of elements
        elif len(user_args) > num_of_args:
            user_args = user_args[:num_of_args]

        return user_args

    @staticmethod
    def main_menu():
        """
        This function prints returns menu options
        """

        output_string = """
        
        Main Menu Options:

        (1). Login
        (2). Register
        (3). Quit
        
        """

        IOInterface.print_message(output_string)

    @staticmethod
    def admin_menu():
        """
        This function prints admin options
        """

        output_string = """
        
        Admin Menu Option:
        
        (1). Show products
        (2). Delete product by id
        (3). Add customers
        (4). Show customers
        (5). Delete customer
        (6). Show orders
        (7). Delete order by id
        (8). Generate test data
        (9). Generate all statistical figures
        (10). Delete all customers
        (11). Delete all data
        (12). Logout
        
        """

        IOInterface.print_message(output_string)

    @staticmethod
    def customer_menu():
        """
        This function prints customer options
        """

        output_string = """
           
        Customer Menu Options:

        (1). Show profile
        (2). Update profile
        (3). Show products
        (4). Show product by id
        (5). Show history orders
        (6). Generate all consumption figures
        (7). Logout
        
        """

        IOInterface.print_message(output_string)

    @staticmethod
    def show_list(user_role, list_type, object_list):
        """
        This function returns relevant list time and object
        based on user role
        :param user_role: admin or customer string
        :param list_type: list type
        :param object: list object 
        """

        if user_role == 'admin':  # define user role

            IOInterface.print_message(
                f"List Type: {list_type}")  # print list type

            IOInterface.print_object(object_list)  # print object

        if user_role == 'customer':  # define customer role

            IOInterface.print_message(
                f"List Type: {list_type}")  # print list type

            IOInterface.print_object(object_list)  # print object

    @staticmethod
    def print_error_message(error_source, error_message):
        """
        This function prints an error message
        :param error_source: the source of the error
        :param error_message: string message to return to user
        """

        print(f"Error occurred in {error_source}: {error_message}")

    @staticmethod
    def print_message(message):
        """
        This function prints a message
        :param message: string message
        """

        print(message)

    @staticmethod
    def print_object(target_object):
        """
        This function prints an object as a string
        :param target_object: object to be converted to a string if not already
        """

        IOInterface.print_message(str(target_object))
