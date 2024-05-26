import random
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import time

from operation_user import UserOperation
from model_order import Order
from operation_customer import CustomerOperation
from operation_product import ProductOperation


class OrderOperation:

    @staticmethod
    def generate_unique_order_id() -> str:
        """
        This function creates a uniue order id that begins with o_ and ends with 5 random numbers
        """

        nums = [str(i) for i in random.sample(
            range(0, 10), 5)]  # list comprehension selects 5 random numbers between 0 to 9 and converts to a string
        nums = ''.join(nums)  # joins each varaible in list together

        user_id = 'o_' + nums  # concatanate start end end together

        return user_id  # return result

    @staticmethod
    def create_an_order(user_id, product_id, create_time) -> bool:
        """
        This function will call the Order class to place an order for each generated user
        :param user_id: user id string
        :param product_id: product id string
        :param create_time: time string
        """

        # call Order Operation class to generate order id
        order_id = OrderOperation.generate_unique_order_id()

        # pass in all paramters to create and instance of the order class
        order = Order(order_id, user_id, product_id, create_time)

        print(order)

        return True  # return True

    @staticmethod
    def delete_order(order_id) -> bool:
        """
        This function will delete a specific order from the orders text file
        :param order_id: order id string
        """

        # navigate to file path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "orders.txt")

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            order_line = file.readlines()

        modified_orders = [
            line for line in order_line if order_id not in line]  # list comprehension that return all values except for the object with the sepcified order id

        # open file with write acesss
        with open(file_path, 'w', encoding='utf-8') as file:
            # write modified lines back to file
            file.writelines(modified_orders)

        # if length of list comprehension is greater than 0 return True else False
        if len(modified_orders) > 0:

            return True
        else:
            return False

    @staticmethod
    def get_order_list(customer_id, page_number) -> tuple:
        """
        This function creates and returns a batch of ten orders per page for all orders
        that have been generated for a specific customer
        :param customer_id: customer id string
        :param page_number: integer page number
        """

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "orders.txt")

        # create customers list
        customers = []

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            order_lines = file.readlines()

            # loop over lines in file
            for order_line in order_lines:

                # filter by customer id
                if customer_id in order_line:

                    # append to customer dictionary
                    customers.append(order_line)

        # create orders list
        orders = []

        # define total pages, start and end index
        total_pages = (len(customers) + 9) // 10
        start_index = (page_number - 1) * 10
        end_index = min(page_number * 10, len(customers))

        # loop over the range of the start and end index
        for idx in range(start_index, end_index):

            # loop over the index and line of the customers list
            for line_idx, line in enumerate(customers):

                line = line.replace("\n", "")  # replace unnecessary strings
                if idx == line_idx:

                    orders.append(line)  # append line to orders list

        # return orders, current page number and total pages
        return (f"Orders: {orders}", f"Current page: {page_number}", f"Total pages: {total_pages}")

    @staticmethod
    # Custom method to return all orders in list form not filtered by customer id
    def get_all_orders_list(page_number) -> tuple:
        """
        This function creates and returns a batch of ten orders per page for all orders
        that have been generates
        :param page_number: integer page number
        """

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "orders.txt")

        # create customer list
        customers = []

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            order_lines = file.readlines()

            # loop over lines in file
            for order_line in order_lines:

                # append to customer dictionary
                customers.append(order_line)

        # create orders list
        orders = []

        # define total pages, start and end index
        total_pages = (len(customers) + 9) // 10
        start_index = (page_number - 1) * 10
        end_index = min(page_number * 10, len(customers))

        # loop over the range of the start and end index
        for idx in range(start_index, end_index):

            # loop over the index and line of the customers list
            for line_idx, line in enumerate(customers):
                line = line.replace("\n", "")  # replace unnecessary strings
                if idx == line_idx:

                    orders.append(line)  # append line to torders list

        # return orders, current page number and total pages
        return (f"Orders: {orders}", f"Current page: {page_number}", f"Total pages: {total_pages}")

    @staticmethod
    def generate_test_order_data():
        """
        This function creates ten test users, with valid credentials and generates a random number
        of orders over a random time range to populate the orders text file
        """

        # create user names
        user_names_list = [
            'user_one',
            'user_two',
            'user_three',
            'user_four',
            'user_five',
            'user_six',
            'user_seven',
            'user_eight',
            'user_nine',
            'user_ten',
        ]

        user_ids = []  # create user id list

        # pre define password for each user and encrpt
        user_password = UserOperation.encrypt_password("password123")
        # create nine characters of the mobile phone number
        mobile_number_start = "030400000"

        # loop over the index and user name with enumerate
        for idx, user_name in enumerate(user_names_list):
            # add standard email prefix to email based on user name
            user_email = user_name + '@example.com'
            # add the last digit of the phone number to complete a valid phone number
            user_mobile = mobile_number_start + str(idx)

            # register each user
            CustomerOperation.register_customer(
                user_name, user_password, user_email, user_mobile)

        # open users file path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        users_file_path = os.path.join(parent_path, "data", "users.txt")

        # define customer data list
        customer_data = []

        # open users text file
        with open(users_file_path, 'r', encoding='utf-8') as file:
            customers_line = file.readlines()

            # loop over each line
            for line in customers_line:
                regex = re.findall(r'"([^"]+)"', line)

                record = {regex[i]: regex[i+1]
                          for i in range(0, len(regex), 2)}  # dictionary comprehension from regex pattern assigns first element as key and second as value

                customer_data.append(record)  # append result into list

        df = pd.DataFrame(customer_data)  # create data frane

        # loop over data frame
        for idx, row in df.iterrows():
            # if users names are in the list return corresponding user id into list
            if row['user_name'] in user_names_list:
                user_ids.append(row['user_id'])

        # create file path to product text file
        products_file_path = os.path.join(parent_path, "data", "products.txt")

        product_ids = []  # create product id list

        # combine products from all the product entries from data/product/*.csv
        ProductOperation.extract_products_from_files()

        product_data = []  # create product data list

        # open products file
        with open(products_file_path, 'r', encoding='utf-8') as file:
            products = file.readlines()

            for line in products:
                # regex pattern to capture key value pairs
                pattern = r'"([^"]+)": "([^"]+)"'
                # find all lines which contain the above regex pattern
                regex = re.findall(pattern, line)
                # create dictionary
                line_dict = dict(regex)
                # append to product data list
                product_data.append(line_dict)

            df = pd.DataFrame(product_data)  # create data frame

        # loop over data frame and append all product id's
        for idx, row in df.iterrows():
            product_ids.append(row['id'])

        # open orders file path
        orders_file_path = os.path.join(parent_path, "data", "orders.txt")

        # truncate any date inside
        open(orders_file_path, 'w').close()

        # loop over the ten user id's
        for user_id in user_ids:
            # select a random number betwen 50 to 200
            order_count = random.randint(50, 200)

            # nested for loop, loop over as many times as the random order count variable specidies
            for _ in range(order_count):
                prod_id = random.choice(product_ids)  # choose a random product
                # create  random time within the last year
                time_delta = random.randint(0, 365 * 24 * 60 * 60)
                # create the current time subracted from the random time delta
                time_raw = time.time() - time_delta
                # convert seconds since the epch into a tuple
                time_tuple = time.localtime(time_raw)
                # format time in specified format
                created_time = time.strftime(
                    '%d-%m-%Y_%H:%M:%S', time_tuple)

                # place the order
                OrderOperation.create_an_order(user_id, prod_id, created_time)

    @staticmethod
    # Custom method to create orders df
    def create_orders_df() -> dict[str, object]:
        """
        This function creates a data frame of all orders from the orders text file
        """

        # create file path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "orders.txt")

        orders_data = []  # create data object

        # open text file
        with open(file_path, 'r', encoding='utf-8') as file:
            order_lines = file.readlines()

            # loop over lines in text file
            for line in order_lines:

                # regex pattern to find text within double quotes
                regex = re.findall(r'"([^"]+)"', line)
                # dictionary comprehension from regex pattern assigns first element as key and second as value
                record = {regex[i]: regex[i+1]
                          for i in range(0, len(regex), 2)}  # processes over every second iteration

                # append data in each iteration into list
                orders_data.append(record)

        orders_df = pd.DataFrame(orders_data)  # create data frame from list

        return orders_df  # return data frame

    @staticmethod
    def generate_single_customer_consumption_figure(customer_id):
        """
        This function generates a bar chart for products pruchased over each month
        isolate to a specific customer generated from teh test data
        :param customer_id: unique customer id string
        """
        # call custom method to create products data frame
        orders_df = OrderOperation.create_orders_df()

        # reduce the data frame to targeted fields filtered by specific user id
        df = orders_df[orders_df['user_id'] ==
                       customer_id][['order_id', 'order_time']]

        df['order_time'] = pd.to_datetime(
            df['order_time'], format='%d-%m-%Y_%H:%M:%S')  # format date time field into specified format

        # create month field by using apply method and lambda function to loop over each value and covert to each month
        df['month'] = df['order_time'].apply(
            lambda x: time.strftime('%b', x.timetuple()))

        # specify month order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                       'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # group by months adn reset indix with the name of count
        df = df.groupby('month').size().reset_index(name='count')

        # convert month field into a categorical data type with specified order
        df['month'] = pd.Categorical(
            df['month'], categories=month_order, ordered=True)
        df = df.sort_values('month')

        # set plot size and create bar chart
        plt.figure(figsize=(15, 10))
        plot = plt.bar(df['month'],
                       df['count'], color="blue")
        plt.xticks(rotation=45, ha='right')

        # loop over plot and generate bar variables
        for bar in plot:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     str(int(height)), ha='center', va='bottom')

        # set axis and title names
        plt.xlabel('Month - 23/24')
        plt.ylabel('Number of Orders')
        plt.title(f'Purchases By month - Customer: {customer_id}')

        # display chart
        plt.show()

    @staticmethod
    def generate_all_customers_consumption_figure():
        """
        This function generates a bar chart showing the aggregate product pruchases for each 
        month over the test data time series
        """

        # call custom method to create products data frame
        orders_df = OrderOperation.create_orders_df()

        # reduce data frame to targeted fields
        df = orders_df[['order_id', 'order_time']]

        df['order_time'] = pd.to_datetime(
            df['order_time'], format='%d-%m-%Y_%H:%M:%S')  # format date time field into specified format

        # create month field by using apply method and lambda function to loop over each value and covert to each month
        df['month'] = df['order_time'].apply(
            lambda x: time.strftime('%b', x.timetuple()))

        # specify month order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                       'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # group by months adn reset indix with the name of count
        df = df.groupby('month').size().reset_index(name='count')

        # convert month field into a categorical data type with specified order
        df['month'] = pd.Categorical(
            df['month'], categories=month_order, ordered=True)

        # sort values via month
        df = df.sort_values('month')

        # set plot size and create bar chart
        plt.figure(figsize=(15, 10))
        plot = plt.bar(df['month'],
                       df['count'], color="blue")
        plt.xticks(rotation=45, ha='right')

        # loop over plot and generate bar variables
        for bar in plot:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     str(int(height)), ha='center', va='bottom')

        # set axis and title names
        plt.xlabel('Month')
        plt.ylabel('Number of Orders')
        plt.title('Purchases By month - 23/24')

        # display chart
        plt.show()

    @staticmethod
    def generate_all_top_10_best_sellers_figure():
        """
        This chart generates a bar chart of the top 10 selling products by product id
        """

        # call custom method to create products data frame
        orders_df = OrderOperation.create_orders_df()

        # reduce the data frame to targeted feld and use value counts method
        df = orders_df['pro_id'].value_counts()

        # convert to data frame, reset index, and return the first 10 records
        df = df.to_frame()
        df = df.reset_index()
        df = df.head(10)

        # set size variables and create bar chart
        plt.figure(figsize=(15, 10))
        plot = plt.bar(df['pro_id'],
                       df['count'], color="blue")
        plt.xticks(rotation=45, ha='right')

        # loop over plot and generate bar variables
        for bar in plot:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     str(int(height)), ha='center', va='bottom')

        # set axis and title names
        plt.xlabel('Product ID')
        plt.ylabel('Number of Orders')
        plt.title('Top 10 Products Purchased')

        # display chart
        plt.show()

    @staticmethod
    def delete_all_orders():
        """
        This function deletes/truncates all date in the orders text file
        """

        # navigate to file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "orders.txt")

        # open and delete/truncate
        open(file_path, 'w').close()
