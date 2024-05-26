import random
import string
import os
import re
import pandas as pd


class UserOperation:

    @staticmethod
    def generate_unique_user_id():
        """
        This function generates a unique user id starting with u_ and 10 random numbers after that,
        the user id is returned as a string.
        """

        # list comrpehension to generate a string of 10 random digits
        nums = [str(i) for i in random.sample(range(0, 10), 10)]
        nums = ''.join(nums)  # join all digits together

        # contcatanate the two strings together to form the complete user id
        user_id = 'u_' + nums

        # return the result
        return user_id

    @staticmethod
    def encrypt_password(password):
        """
        This function encryptes the user entered password in plain text with a set of random letters and numbers
        :param password: user entered password
        """

        # takes in entered password and doubles it
        adj_password = password * 2
        random_string = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=len(adj_password)))  # reforms the doubled string with a random combination of uppercase/lowercase letters and digits

        # define empty string variable
        encrypted_random = ''
        # define string index
        string_index = 0

        # loop over the randomly create string with correspinding index
        for idx, letter in enumerate(random_string):
            encrypted_random += letter  # add characters to empty string calue
            if idx % 2 == 1:  # find every odd position
                # add original password characters back
                encrypted_random += password[string_index]
                string_index += 1  # increase index by one

        encrypted_password = '^^' + encrypted_random + \
            '$$'  # add special characters before and after

        # return result
        return encrypted_password

    @staticmethod
    def decrypt_password(encrypted_password):
        """
        This function takes in the encrypted password, uses regex and index to decrypt it
        and return the originally entered password.
        :param encrypted_password: the encrypted password string
        """

        # this regex removes special characters from encyption
        encrypted_password = re.sub("[^A-Za-z0-9]", "", encrypted_password)

        decrypted_password = ''  # define as an empty string to add to later

        string_index = 2  # starts at the second index of the encrypted string password

        # use while loop to iterate if string index is less than encrypted password length
        while string_index < len(encrypted_password):
            # add the character to decrypted password at the specified index
            decrypted_password += encrypted_password[string_index]
            string_index += 3  # skip three places each iteration

        # return decrypted password
        return decrypted_password

    @staticmethod
    def check_username_exist(user_name) -> bool:
        """
        This function checks if the user name the customer or admin has entered already exists in the users
        text file and returns True if it does and False if it does not
        :param user_name: user name string
        """

        # navigating to users.txt file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "users.txt")

        data = []  # object to store user data

        with open(file_path, 'r', encoding='utf-8') as file:
            customer_lines = file.readlines()

            for line in customer_lines:  # loop over lines in text file

                # regex pattern to find text within double quotes
                regex = re.findall(r'"([^"]+)"', line)
                # dictionary comprehension from regex pattern assigns first element as key and second as value
                record = {regex[i]: regex[i+1]
                          for i in range(0, len(regex), 2)}  # processes over every second iteration

                data.append(record)  # append to empty list

        df = pd.DataFrame(data)  # create dataframe

        try:
            # prevents programming from failing if no usernames present
            # returns a boolean value if user name is found in user name field
            user_name_check = df['user_name'].isin([user_name]).any()

            if user_name_check:  # if the above variable is True return True else False
                return True
            else:
                return False

        except Exception:
            return False

    @ staticmethod
    def validate_username(user_name) -> bool:
        """
        This function takes in a user name string and validates it is correct based on specific criteria,
        a boolean of True is returned if valid and False if invalid
        :param user_name: user name string
        """

        user_len = len(user_name)  # calcualte user name
        pattern = r'^[a-zA-Z_]'  # define regex pattern to search for

        # if length is greather than five and conforms to the regex pattern return True else False
        if user_len >= 5 and bool(re.match(pattern, user_name)):
            return True
        else:
            return False

    @ staticmethod
    def validate_password(user_password) -> bool:
        """
        This function takes in a password string and validates it is correct based on specific criteria,
        a boolean of True is returned if valid and False if invalid
        :param user_password: password string
        """

        password_len = len(user_password)  # calculate password length
        # check for number of characters in password string that are digits
        number = sum(num.isdigit() for num in user_password)
        # check for number of letters in password string
        letter = sum(letter.isalpha() for letter in user_password)

        # if there is at least 1 number, 1 letter and the character length grater than 5 return True else false
        if number > 0 and letter > 0 and password_len > 4:
            return True
        else:
            return False

    @staticmethod
    # TODO: Is this supposed to return a customer object
    def login(user_name, user_password) -> dict[str, object]:
        """
        This function takes user name and password, validates both and allows user to login as a customer or password
        returning the relevant dictionary object or nothing if neither are found
        :param user_name: user name string
        :param user_password: pass word string
        """

        # calling validation methods from User operation class
        if UserOperation.validate_username(user_name) and UserOperation.validate_password(user_password):

            # navigating to users.txt file
            parent_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(parent_path, "data", "users.txt")

            user_data = []  # empty user data list to store records

            with open(file_path, 'r', encoding='utf-8') as file:
                user_lines = file.readlines()  # opening files and reading all lines

                for user_line in user_lines:

                    # regex pattern to find text within double quotes
                    regex = re.findall(r'"([^"]+)"', user_line)
                    # dictionary comprehension from regex pattern assigns first element as key and second as value
                    record = {regex[i]: regex[i+1]
                              for i in range(0, len(regex), 2)}  # processes over every second iteration

                    user_data.append(record)  # append record into a list

                df = pd.DataFrame(user_data)  # convert lis to a data frame

                for _, row in df.iterrows():  # loop over each row in data frame

                    # checking if key value pair is equal to 'customer'
                    if row['user_role'] == 'customer':

                        customer_object = []  # create empty customer list

                        # call decrypt method check is equal to entered password
                        if row['user_name'] == user_name and UserOperation.decrypt_password(row['user_password']) == user_password:
                            customer_object.append(row.to_dict())
                            return customer_object[0]

                    # checking if key value pair is equal to 'admin'
                    elif row['user_role'] == 'admin':

                        admin_object = []  # create empty admin list

                        # no decryption required on admin credentials
                        if row['user_name'] == user_name and UserOperation.decrypt_password(row['user_password']):
                            admin_object.append(row.to_dict())
                            return admin_object[0]

                # return empty dictionary if not found
                return {}
