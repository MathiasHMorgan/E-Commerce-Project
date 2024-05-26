import os


class Product:
    """
    Product class with defaily values for each instance
    """

    def __init__(self, prod_id="", pro_model="", pro_category="", pro_name="", pro_current_price="", pro_raw_price="", pro_discount="", pro_likes_count=""):
        self.prod_id = prod_id
        self.pro_model = pro_model
        self.pro_category = pro_category
        self.pro_name = pro_name
        self.pro_current_price = pro_current_price
        self.pro_raw_price = pro_raw_price
        self.pro_discount = pro_discount
        self.pro_likes_count = pro_likes_count

    def __str__(self):
        product_str = f'{{"prod_id":"{self.prod_id}", "pro_model":"{self.pro_model}", "pro_category_id": "{self.pro_category}", "pro_name":"{self.pro_name}", "pro_current_price":"{self.pro_current_price}", "pro_raw_price":"{self.pro_raw_price}", "pro_discount":"{self.pro_discount}", "pro_likes_count":"{self.pro_likes_count}"}}'

        # navigate to file path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        # append instance to file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(product_str + "\n")

        return product_str
