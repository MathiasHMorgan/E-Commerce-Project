from operation_product import ProductOperation
from operation_order import OrderOperation
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from operation_user import UserOperation
from io_interface import IOInterface

import os
import re
import pandas as pd

# This prevents chain messaging, was occuring during chart generation
pd.set_option('mode.chained_assignment', None)


def login_control():  # login function
    """
    This function handles login validation for customers and admins
    """

    while True:

        global customer_object  # creates dictionary object if valid credentials are put in

        login_creds = IOInterface.get_user_input(
            "Please provide your user name and password to login separated by a space or enter 3 to return to the main menu: ", 2)  # enter user name and pass word

        if login_creds[0] == '3':  # if 3 entered exit program
            IOInterface.print_message("\nReturning to main menu...\n")
            main()

        # extract user object dictionary from user name and password
        user_obj = UserOperation.login(login_creds[0], login_creds[1])

        # navigate to file path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        user_data = []  # create user data list

        # open file
        with open(file_path, 'r') as file:
            user_lines = file.readlines()

            # loop over lines in file
            for user_line in user_lines:
                # regex pattern to find text within double quotes
                regex = re.findall(r'"([^"]+)"', user_line)
                record = {regex[i]: regex[i+1]
                          for i in range(0, len(regex), 2)}  # processes over every second iteration

                user_data.append(record)  # append lines to list

        df = pd.DataFrame(user_data)  # create data frame

        # loop over data frame
        for _, row in df.iterrows():
            if row['user_name'] == login_creds[0]:  # if user name is equal to log in credentials

                # convert customer object to a dictionary from data frame
                customer_object = row.to_dict()

        if user_obj:

            if user_obj["user_role"] == "customer":  # if customer activate customer menu
                IOInterface.print_message(
                    "\nChoose from the customer menu options below...\n")
                customer_control()
            elif user_obj["user_role"] == "admin":  # if admin activate admin menu
                IOInterface.print_message(
                    "\nChoose from the admin menu options below...\n")
                admin_control()
            break

        else:
            IOInterface.print_message(
                "\nInvalid username or password. Please try again.\n")  # if invalid error message


def customer_control():
    """
    This function handles all customer options
    """

    while True:

        IOInterface.customer_menu()  # customer menu

        # defining acceptable inputs for customer options
        valid_options = ['1', '2', '3', '4', '5', '6', '7', '']
        product_options = ['3beauty', '3bags', '3house', '3jewelry',
                           '3kids', '3men', '3shoes', '3women', '3accessories']  # defining acceptable inputs for product options

        customer_option = IOInterface.get_user_input(
            "What option would you like to select? ", 1)[0]
        # while loop to check only valid inputs entered
        while customer_option not in valid_options and customer_option not in product_options:
            IOInterface.print_message(
                f"You entered: {customer_option}, that is invalid! Select option 1 to 7")  # if invalid option entered message will print
            customer_option = IOInterface.get_user_input(
                "What option would you like to select? ", 1)[0]

        if customer_option == '1' or customer_option == '':  # Show profile #

            IOInterface.print_message("\nProfile details below...\n")

            IOInterface.print_object(f"user id: {customer_object['user_id']} " + f"user name: {customer_object['user_name']} " +
                                     f"user email: {customer_object['user_email']} " + f"user mobile: {customer_object['user_mobile']}")

        elif customer_option == '2':  # Update Profile #

            attribute = IOInterface.get_user_input(
                """
                What would you like to update? Please enter one the following:

                "user_name"
                "user_email"
                "user_mobile"
                "user_password"

                Enter what you would like the new value to be seperated by a space.

                example: 'user_name test_user'

                Enter here: """, 2)

            if CustomerOperation.update_profile(
                    attribute[0], attribute[1], customer_object):

                IOInterface.print_message(
                    """
                Update Successful
                """)

            else:

                IOInterface.print_message("Update Failed")

        elif customer_option == '3' or customer_option in product_options:  # Show products #

            if customer_option == '3':  # show products in pages #

                page_num = IOInterface.get_user_input(
                    "Select the product page number you would like to see: ", 1)[0]
                while not page_num.isdigit():
                    IOInterface.print_message(
                        f"You entered: {page_num}, this is invalid, select a product page number")
                    page_num = IOInterface.get_user_input(
                        "Select the product page number you would like to see: ", 1)[0]

                products = ProductOperation.get_product_list(int(page_num))

                IOInterface.show_list(
                    customer_object['user_role'], 'Product', products)

            else:  # show products by key word #

                split_option = re.split(
                    r'(\d+)', customer_option)  # split customer input
                # list comprehension to retrieve all products that fit selected cateogry
                keywords = [elem for elem in split_option if elem]

                products = ProductOperation.get_product_list_by_keyword(  # call function
                    keywords[1])

                IOInterface.show_list(
                    customer_object['user_role'], f'Product: {keywords[1]}', products)  # return to user

        elif customer_option == '4':  # Show product by id #

            prod_id = IOInterface.get_user_input(
                "Select a product to view by id: ", 1)[0]

            # definee regex pattern 7 numbers after
            pattern = r"\d{7}"
            # ensure user_id matches sequence
            regex = re.findall(pattern, prod_id)

            if regex:

                IOInterface.print_message(
                    f"Product {prod_id} found...")

                product = ProductOperation.get_product_by_id(prod_id)
                IOInterface.print_object(product)

            else:

                IOInterface.print_message(
                    f"Product {prod_id} not found...")

        elif customer_option == '5':  # Show history orders #

            page_num = IOInterface.get_user_input(
                "Select the order page number you would like to see: ", 1)[0]
            while not customer_option.isdigit():
                IOInterface.print_message(
                    f"You entered: {page_num}, this is invalid, select a product page number")
                page_num = IOInterface.get_user_input(
                    "Select the order page number you would like to see: ", 1)[0]

            orders = OrderOperation.get_order_list(
                customer_object['user_id'], int(page_num))

            IOInterface.show_list(
                customer_object['user_role'], 'Orders', orders)

        elif customer_option == '6':  # denerate consumption figures #

            OrderOperation.generate_single_customer_consumption_figure(
                customer_object['user_id'])

        elif customer_option == '7':  # logout to main menu #
            main()
            IOInterface.print_message("\nLogging out...\n")


def admin_control():
    """
    This function handles all admin options
    """

    while True:

        IOInterface.admin_menu()

        valid_options = ['1', '2', '3', '4', '5',
                         '6', '7', '8', '9', '10', '11', '12', '']  # defining valid inputs

        admin_option = IOInterface.get_user_input(
            "What option would you like to select? ", 1)[0]
        while admin_option not in valid_options:
            IOInterface.print_message(
                f"You entered: {admin_option}, that is invalid! Select option 1 to 12")
            admin_option = IOInterface.get_user_input(
                "What option would you like to select? ", 1)[0]

        if admin_option == '1' or admin_option == '':  # dhow Products #

            page_num = IOInterface.get_user_input(
                "Select the product page number you would like to see: ", 1)[0]
            while not page_num.isdigit():
                IOInterface.print_message(
                    f"You entered: {page_num}, this is invalid, select a product page number")
                page_num = IOInterface.get_user_input(
                    "Select the product page number you would like to see: ", 1)[0]

            products = ProductOperation.get_product_list(int(page_num))

            IOInterface.show_list(
                customer_object['user_role'], 'Orders', products)

        # custom option
        elif admin_option == '2':  # delete product by id #

            prod_id = IOInterface.get_user_input(
                "Select the ID pf the product you would like to delete: ", 1)[0]

            # definee regex pattern 7 numbers after
            pattern = r"\d{7}"
            # ensure user_id matches sequence
            regex = re.findall(pattern, prod_id)

            if regex:
                delete_check = ProductOperation.delete_product(prod_id)

                if delete_check:
                    IOInterface.print_message(f'Product {prod_id} deleted...')
            else:
                IOInterface.print_message(f'Product {prod_id} id not found...')

        elif admin_option == '3':  # add customers #

            register_creds = IOInterface.get_user_input(
                """
                Please provide your user name, password, email and mobile seperated by a space.

                user name: must be at least 5 characters and only contain letters or underscores
                password: must be at least 5 characters and contain at least one letter and one number
                email: must be in standard format name@domain.com
                mobile: must begin with 04 or 03 and be 10 numbers in total

                Enter Here: """, 4)

            while not CustomerOperation.register_customer(*register_creds):

                IOInterface.print_error_message(
                    "CustomerOperation.register_customer", 'Invalid Credentials please enter again...')
                register_creds = IOInterface.get_user_input(
                    """
                    Please provide your user name, password, email and mobile seperated by a space.

                    user name: must be at least 5 characters and only contain letters or underscores
                    password: must be at least 5 characters and contain at least one letter and one number
                    email: must be in standard format name@domain.com
                    mobile: must begin with 04 or 03 and be 10 numbers in total

                    Enter Here: """, 4)

            CustomerOperation.register_customer(*register_creds)

            IOInterface.print_message(
                """
                You have registered a customer successfully...
                """)

        elif admin_option == '4':  # show customers #

            page_num = IOInterface.get_user_input(
                "Select the product page number you would like to see: ", 1)[0]
            while not page_num.isdigit():
                IOInterface.print_message(
                    f"You entered: {page_num}, this is invalid, select a product page number")
                page_num = IOInterface.get_user_input(
                    "Select the product page number you would like to see: ", 1)[0]

            customers = CustomerOperation.get_customer_list(int(page_num))

            IOInterface.show_list(
                customer_object['user_role'], 'Product', customers)

        # Custom option
        elif admin_option == '5':  # delete customer #

            user_id = IOInterface.get_user_input(
                "Enter the user ID of the customer you would like to delete: ", 1)[0]

            # definee regex pattern u_ with 10 numbers after
            pattern = r"u_\d{10}"
            # ensure user_id matches sequence
            regex = re.findall(pattern, user_id)

            if regex:  # if true delete user

                delete_check = CustomerOperation.delete_customer(user_id)

                if delete_check:
                    IOInterface.print_message(
                        f'User {user_id} has been deleted...')
            else:
                IOInterface.print_message(
                    f"User {user_id} not found...")  # else user not found

        elif admin_option == '6':  # show orders #

            page_num = IOInterface.get_user_input(
                "Select the product page number you would like to see: ", 1)[0]
            while not page_num.isdigit():
                IOInterface.print_message(
                    f"You entered: {page_num}, this is invalid, select a product page number")
                page_num = IOInterface.get_user_input(
                    "Select the product page number you would like to see: ", 1)[0]

            orders = OrderOperation.get_all_orders_list(int(page_num))

            IOInterface.show_list(
                customer_object['user_role'], 'Orders', orders)

        elif admin_option == '7':  # delete order by id #

            order_id = IOInterface.get_user_input(
                "Enter an order id that you want to delete: ", 1)[0]

            # definee regex pattern u_ with 10 numbers after
            pattern = r"o_\d{5}"
            # ensure user_id matches sequence
            regex = re.findall(pattern, order_id)

            if regex:  # if true delete user

                delete_order_check = OrderOperation.delete_order(order_id)

                if delete_order_check:
                    IOInterface.print_message(
                        f"\nOrder id:{order_id} has been deleted...\n")
            else:
                IOInterface.print_message(
                    f"\nOrder id:{order_id} not found...\n")

        elif admin_option == '8':  # generate test data #

            OrderOperation.generate_test_order_data()
            IOInterface.print_message("\nTest order data generated...\n")

        elif admin_option == '9':  # generate statistical figures #

            try:
                ProductOperation.generate_category_figure()
                ProductOperation.generate_discount_figure()
                ProductOperation.generate_likes_count_figure()
                ProductOperation.generate_discount_likes_count_figure()

                OrderOperation.generate_all_customers_consumption_figure()
                OrderOperation.generate_all_top_10_best_sellers_figure()

                IOInterface.print_message(
                    "\nStatistical figures generated, see figure folder...\n")
            except:
                IOInterface.print_error_message(
                    "\nProductOperation/OrderOperation", "Figure/s could bot be generated\n")

        elif admin_option == '10':  # delete all customers #

            CustomerOperation.delete_all_customers()

            IOInterface.print_message("\nAll customers have been deleted...\n")

        elif admin_option == '11':  # delete all data #

            # define files to truncate
            files = ["orders.txt", "products.txt", "users.txt"]

            for file in files:  # loop over each file

                # navigate to file paths
                parent_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(parent_path, "data", file)

                open(file_path, 'w').close()  # truncate

            image_files = ['generate_category_figure.png', 'generate_discount_figure.png',
                           'generate_likes_count_figure.png', 'generate_discount_likes_count_figure.png']  # define generated images

            # define file path
            figure_folder_path = os.path.join(parent_path, "data", "figure")

            for image in image_files:  # loop over all images in folder
                image_path = os.path.join(
                    figure_folder_path, image)
                if os.path.exists(image_path):
                    os.remove(image_path)  # remove if file exists
                    IOInterface.print_message(f"\nDeleted: {image}\n")
                else:
                    IOInterface.print_message(f"\nFile not found: {image}\n")

        elif admin_option == '12':  # logout #
            main()
            IOInterface.print_message("\nLogging out...\n")


def admin_exists():  # Custom function to check if admin exists
    """
    This function checks if an admin exists in the users text file.
    """

    # navigate to
    parent_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(parent_path, "data", "users.txt")

    # open file
    with open(file_path, 'r') as file:
        user_lines = file.readlines()

        user_data = []  # create user data list

        # loop over lines in text file
        for user_line in user_lines:
            # regex pattern to find text within double quotes
            regex = re.findall(r'"([^"]+)"', user_line)
            # processes over every second iteration with dictionary comprehension
            record = {regex[i]: regex[i+1] for i in range(0, len(regex), 2)}

            user_data.append(record)  # append to list

        df = pd.DataFrame(user_data)  # create data frame

        for _, row in df.iterrows():  # loop over data frame
            if row['user_role'] == 'admin':  # if admin exists return True else False
                return True

        return False


def main():
    """
    Execute to start the program
    """

    while True:  # while loop to begin program

        IOInterface.print_message("\nMain Menu...\n")

        if not admin_exists():
            AdminOperation.register_admin()  # check if admin exists in user file

        IOInterface.main_menu()  # prints main menu options

        # list containing the three valid options fo rthe main menu
        valid_options = ['1', '2', '3']

        menu_option = IOInterface.get_user_input(
            "What option would you like to select? ", 1)[0]  # unser input to select option
        while menu_option not in valid_options:  # if option in valid error message will print to enter a valid option, this will continue until valid option is entered
            IOInterface.print_message(
                f"You entered: {menu_option}, that is invalid! Select option 1,2 or 3")
            menu_option = IOInterface.get_user_input(
                "What option would you like to select? ", 1)[0]

        if menu_option == "1":  # option 1 activates login function
            login_control()
            break

        elif menu_option == "2":  # option 2 activates register customer function in customer operation class

            register_creds = IOInterface.get_user_input(  # user asked to inpit customer registration credentials
                """
                                                        
            Please provide your user name, password, email and mobile seperated by a space. Enter 3 to return to menu.

            user name: must be at least 5 characters and only contain letters or underscores 
            password: must be at least 5 characters and contain at least one letter and one number
            email: must be in standard format name@domain.com
            mobile: must begin with 04 or 03 and be 10 numbers in total
                                                    
            Enter Here: """, 4)

            if register_creds[0] == '3':
                IOInterface.print_message("\nReturning to menu...\n")
                main()

            # if the result of this function is not True error message will pront to enter again
            # this will continue until the correct credentials are entered
            while not CustomerOperation.register_customer(*register_creds) or register_creds[0] == '3':
                IOInterface.print_error_message(
                    "CustomerOperation.register_customer", 'Invalid Credentials please enter again...')
                register_creds = IOInterface.get_user_input(
                    """
                                                            
            Please provide your user name, password, email and mobile seperated by a space. Enter 3 to return to menu.

            user name: must be at least 5 characters and only contain letters or underscores 
            password: must be at least 5 characters and contain at least one letter and one number
            email: must be in standard format name@domain.com
            mobile: must begin with 04 or 03 and be 10 numbers in total
                                                        
            Enter Here: """, 4)

                if register_creds[0] == '3':
                    IOInterface.print_message("\nReturning to menu...\n")
                    main()

            # if correct credentials are called customer will be registered
            CustomerOperation.register_customer(*register_creds)

            IOInterface.print_message(  # print success message
                """ 
                
                You have registered successfully! 

                Login with your username and password to access the customer options

                """)

        elif menu_option == "3":  # exists program
            IOInterface.print_message("\nExiting Program...\n")
            exit()


if __name__ == "__main__":  # executes program
    main()
