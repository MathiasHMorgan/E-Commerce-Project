import os


class Order:
    """
    Order class with defauly values for each instance
    """

    def __init__(self, order_id="", user_id="", pro_id="", order_time='00-00-0000_00:00:00'):
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    def __str__(self):
        order_str = f'{{"order_id":"{self.order_id}", "user_id":"{self.user_id}", "pro_id":"{self.pro_id}", "order_time":"{self.order_time}"}}'

        # navigate to file path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "orders.txt")

        # append instance to file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(order_str + "\n")

        return order_str
