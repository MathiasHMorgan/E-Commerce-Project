import re
import os
import pandas as pd
import time

from model_customer import Customer
from operation_user import UserOperation


class CustomerOperation:

    @staticmethod
    def validate_email(user_email) -> bool:
        """
        This function will validate an email string by its four diferent components
        :param user_email: email string
        """

        regex_check = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  # define complex regex pattern to validate email addresses

        # applies above regex pattern to user email string to check if valid return True else False
        if re.fullmatch(regex_check, user_email):
            return True
        else:
            return False

    @staticmethod
    def validate_mobile(user_mobile) -> bool:
        """
        This function validates user mobile string input
        :param user_mobile: user mobile string
        """

        mobile_len = len(user_mobile)  # length of provided string

        # check if first two characters start with 04 or 03 and check length is 10 return True else False
        if user_mobile[:2] in ['04', '03'] and mobile_len == 10:
            return True
        else:
            return False

    @staticmethod
    def register_customer(user_name, user_password, user_email, user_mobile) -> bool:
        """
        This function registers a customer by performing validation and calling the Customer class
        :param user_name: user name string
        :param user_password: password string
        :param user_email: email string
        :param user_mobile: mobile number string
        """

        user_exist = UserOperation.check_username_exist(
            user_name)  # check if user name exits

        # check if provided paramters are valid will return True if valid and False if not valid
        valid_user = UserOperation.validate_username(user_name)
        valid_password = UserOperation.validate_password(user_password)
        valid_email = CustomerOperation.validate_email(user_email)
        valid_mobile = CustomerOperation.validate_mobile(user_mobile)

        time_raw = time.time()  # create current time
        # craete time tuple by seconds epoch
        time_tuple = time.localtime(time_raw)
        # formate tim with seconds tuple in required format
        time_formatted = time.strftime('%d-%m-%Y_%H:%M:%S', time_tuple)

        # generate uniquye user id
        user_id = UserOperation.generate_unique_user_id()

        # if all conditions are tur register customer
        if user_exist == False and valid_user == True and valid_password == True and valid_email == True and valid_mobile == True:

            customer = Customer(user_id, user_name, user_password,
                                time_formatted, "customer", user_email, user_mobile)

            print(customer)

            return True

        else:

            return False

    @staticmethod
    def update_profile(attribute_name, value, customer_object) -> bool:
        """
        This function updates a specific attribute with a user specified value if relevant checks pass
        :param attribute_name: the attribute type user wishes to change
        :param value: the value the user wants to change to
        :param customer_object: the dictionary object to be updates
        """

        # speicify list of attributes that can be updates return false if any fail
        if attribute_name not in ["user_name", "usser_email", "user_mobile", "user_password"]:
            return False
        else:
            # user name validation check
            if attribute_name == "user_name" and UserOperation.check_username_exist(value):
                return False
            # email validation check
            elif attribute_name == "user_email" and not CustomerOperation.validate_email(value):
                return False
            # mobile number validation check
            elif attribute_name == "user_mobile" and not CustomerOperation.validate_mobile(value):
                return False
            # password validation check
            elif attribute_name == "user_password" and not UserOperation.validate_password(value):
                return False

            else:
                # naivate to users file
                parent_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(parent_path, "data", "users.txt")

                customer_dict = customer_object  # change name of customer_object

                # change dictionary value based on attribute key
                customer_dict[attribute_name] = value

                # create profile data list
                profile_data = []

                # open file
                with open(file_path, 'r', encoding='utf-8') as file:

                    # loop over file
                    for line in file:

                        # regex pattern to find text within double quotes
                        regex = re.findall(r'"([^"]+)"', line)
                        record = {regex[i]: regex[i+1]  # dictionary comprehension from regex pattern assigns first element as key and second as value
                                  for i in range(0, len(regex), 2)}  # processes over every second iteration

                        # append result to prifle data list
                        profile_data.append(record)

                df = pd.DataFrame(profile_data)  # create data frame

                df.loc[df['user_id'] == customer_dict['user_id'],  # checks user in data frame and customer dict is equivalent
                       attribute_name] = value if attribute_name != "user_password" else UserOperation.encrypt_password(value)  # changes value in data frame if value is password then encrypt the value

                user_list = df.to_dict(orient="records")  # create dictionary

                with open(file_path, "w", encoding="utf-8") as file:  # open file

                    # loop over dictionary
                    for row in user_list:
                        formatted_row = "{" + ", ".join(  # join dictionary braces and comma to row
                            [f'"{key}": "{value}"' for key, value in row.items()]) + "}"  # string list comprehension over row to craete key value pairs
                        # write each result to new line
                        file.write(formatted_row + "\n")

                # return true if executed change
                return True

    @staticmethod
    def delete_customer(customer_id) -> bool:
        """
        This function deletes a specific customer by the customer id
        :param customer_id: customer id string
        """

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            customer_line = file.readlines()

        modified_users = [
            line for line in customer_line if customer_id not in line]  # list comprehension to return all records apart from the record containing the specified customer id

        # open file with write access and truncate
        with open(file_path, 'w', encoding='utf-8') as file:
            # write back all records apart from the record containing the customer_id
            file.writelines(modified_users)

        # if length list comprehension is greater than 0 return True else False
        if len(modified_users) > 0:

            return True
        else:
            return False

    @staticmethod
    def get_customer_list(page_number) -> tuple:
        """
        This function creates and returns a batch of ten customers per page
        :param page_number: integer page number
        """

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        # create customers list
        customers = []

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # define total pages, start and end index
        total_pages = (len(lines) + 9) // 10
        start_index = (page_number - 1) * 10
        end_index = min(page_number * 10, len(lines))

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            customer_line = file.readlines()

        # loop over the range of the start and end index
        for idx in range(start_index, end_index):

            # loop over the index and line of the customers list
            for line_idx, line in enumerate(customer_line):

                if idx == line_idx:

                    # replace unnecessary strings
                    line = line.replace("\n", "")
                    # find where customer is in each line
                    if line.__contains__('customer'):

                        customers.append(line)  # append to list

        # return customers, current page number and total pages
        return (f"Customers: {customers}", f"Current page: {page_number}", f"Total pages: {total_pages}")

    @staticmethod
    def delete_all_customers():
        """
        This functions deletes are customers in the users text files except for the admin account
        """

        # navigate to user text file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            customer_line = file.readlines()

        modified_product = [
            line for line in customer_line if 'customer' not in line]  # list comprehension that isolates records that are not customers (admin)

        # truncate and write admin back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(modified_product)
