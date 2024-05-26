import matplotlib.pyplot as plt
import os
import pandas as pd


class ProductOperation:

    @staticmethod
    # Custom method to create products data frame
    def create_products_df() -> dict[str, object]:
        """
        This function navigates to where all product csv's are stored, and performs a union join on all files
        across common fields and returns the data frame
        """

        # navigate to csv folder
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "product")

        # define a list containing all csv values
        csv_files = ["accessories.csv", "bags.csv", "beauty.csv", "house.csv",
                     "jewelry.csv", "kids.csv", "men.csv", "shoes.csv", "women.csv"]

        # define empty list
        data = []

        # loop over all files and extract common fields
        for file in csv_files:
            df = pd.read_csv(os.path.join(file_path, file), usecols=[
                             "id", "model", "category", "name", "current_price", "raw_price", "discount", "likes_count"])

            # append the result into the list
            data.append(df)

        # concatanate/union join all together
        products_df = pd.concat(data, ignore_index=True)

        # return the combined data frame
        return products_df

    @staticmethod
    def extract_products_from_files():
        """
        This function extracts data from the combined products data frame and writes it in text format
        into the products text file
        """

        # call create data frame function
        products_df = ProductOperation.create_products_df()

        # navigate to file path containing text file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        # convert data frame rows to dictionaries
        products_list = products_df.to_dict(orient="records")

        # open file and truncate data (if any)
        open(file_path, "w", encoding='utf-8').close()

        # open file
        with open(file_path, "w", encoding="utf-8") as file:

            # loop over products list and re creates a dictionary
            for row in products_list:
                formatted_row = "{" + ", ".join(  # join dictionary braces and comma to row
                    [f'"{key}": "{value}"' for key, value in row.items()]) + "}"  # string list comprehension over row to craete key value pairs
                # write each result to new line
                file.write(formatted_row + "\n")

    @staticmethod
    def get_product_list(page_number):
        """
        This function returns a list of products depending on the page number specififed
        as well as the total number of pages and current page that selected
        :param page_number: integer of the page number the user wishes to view
        """

        # navigate to text file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        # define product lis
        products = []

        # open file
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # define total pages, start and end index used to isolate pages
        total_pages = (len(lines) + 9) // 10
        start_index = (page_number - 1) * 10
        end_index = min(page_number * 10, len(lines))

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            product_line = file.readlines()

            # loop over the range start and end index
            for idx in range(start_index, end_index):

                # loop over line index and line with enumerate function
                for line_idx, line in enumerate(product_line):
                    # remove unnecessary string values
                    line = line.replace("\n", "")
                    if idx == line_idx:

                        products.append(line)  # append object to products list

        # return results showing products, current page number and total pages available
        return (f"Products: {products}", f"Current page: {page_number}", f"Total pages: {total_pages}")

    @staticmethod
    def delete_product(product_id) -> bool:
        """
        This function will remove a product from the products text file if it contains the specified product id
        :param product_id: product id user wants to delete
        """

        # create file path to prodcuts text file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            prod_line = file.readlines()

        modified_product = [
            line for line in prod_line if product_id not in line]  # list comprehension to return all values if they do not contain the specified product id

        # open file with write permissions and write all lines back to file that do not contain specified product id
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(modified_product)

        # if there is data inside the linst comprehension return true else false
        if len(modified_product) > 0:
            return True
        else:
            return False

    @staticmethod
    def get_product_list_by_keyword(keyword) -> list:
        """
        This function returns a list of products by a key word
        :param keyword: key word sequence used to find product objects
        """

        # create file path to products text file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        # open file
        with open(file_path, 'r', encoding='utf-8') as file:
            product_line = file.readlines()

        key_word_products = [
            line.strip('\n') for line in product_line if line.__contains__(keyword)]  # list comprehension to return all values that contain the key word sequence and strip \n lines

        # return result
        return key_word_products

    @staticmethod
    # TODO: strip the /n from the output and consider using [] istead if time permits
    def get_product_by_id(product_id) -> set:
        """
        This function returns a product object found by its unique product id.
        :param product_id: product id used to find specific object
        """
        # set produc id to string value
        product_id = str(product_id)

        # create file path to product text file
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        # open the file
        with open(file_path, 'r', encoding='utf-8') as file:
            product_line = file.readlines()

        product = [
            line.strip('\n') for line in product_line if line.__contains__(product_id)]  # list comprehension to return the value that contains the product id and strip \n lines

        # the length of product variable is greather than zero data exists in inside
        if len(product) > 0:

            # this mitgates any possibility of duplicates being returned using set function
            product = set(product)

            return product
        else:
            return None

    @staticmethod
    def generate_category_figure():
        """
        This function generates a bar chart into the figure folder containing the counts
        of each product category

        """
        # call custom method to create products data frame
        products_df = ProductOperation.create_products_df()

        # value counts method on required field
        df = products_df[['category']].value_counts()
        df = df.to_frame()

        # group by category and sum counts
        df = df.groupby("category").agg("sum")

        # reset index
        df = df.reset_index()

        # sort by count in descending order
        df_sorted = df.sort_values(by='count', ascending=False)

        # set plot size and crate bar chart
        plt.figure(figsize=(15, 10))
        plot = plt.bar(df_sorted['category'],
                       df_sorted['count'], color="blue")
        plt.xticks(rotation=45, ha='right')

        # loop over plot and generate bar variables
        for bar in plot:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     str(int(height)), ha='center', va='bottom')

        # set axis and title names
        plt.xlabel('Category')
        plt.ylabel('Product Count')
        plt.title('Product Count by Category')

        # navigate to folder
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "figure")

        chart_folder = os.path.join(file_path, 'generate_category_figure.png')

        # save to folder
        plt.savefig(chart_folder)

    @staticmethod
    def generate_discount_figure():
        """
        This function generates a pie chart into the figure folder containing the proportion
        of product discount within three sperate ranges
        """

        # call custom method to create products data frame
        products_df = ProductOperation.create_products_df()

        # reduces the data frame to targeted fields
        df = products_df[['category', 'discount']]

        # Create bins, labels and define new field based on those variables
        bins = [0, 30, 60, 100]
        labels = ['< 30%', '30-60%', '> 60%']
        df['Discount Range'] = pd.cut(df['discount'], bins=bins, labels=labels)

        # call value count method
        discount_counts = df['Discount Range'].value_counts()

        # set plot size and create pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(discount_counts, labels=discount_counts.index,
                autopct='%1.2f%%', startangle=140)  # rounded to two percentages
        # set names and titles
        plt.title('Proportion of Products by Discount Range')
        plt.axis('equal')

        # define target folder path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "figure")

        chart_folder = os.path.join(file_path, 'generate_discount_figure.png')

        plt.savefig(chart_folder)

    @staticmethod
    def generate_likes_count_figure():
        """
        This function generates a bar chart into the figure folder containing the likes count
        for each product category
        """

        # call custom method to create products data frame
        products_df = ProductOperation.create_products_df()

        # reduce the data frame to two targeted fields, use value counts method
        df = products_df[['category', 'likes_count']].value_counts()
        df.to_frame()
        # group by category and sum counts
        df = df.groupby('category').agg('sum')
        df = df.reset_index()

        # sort counts in descending order
        df_sorted = df.sort_values(by='count', ascending=False)

        # set plot size and create bar chart
        plt.figure(figsize=(15, 10))
        plot = plt.bar(df_sorted['category'],
                       df_sorted['count'], color="blue")
        plt.xticks(rotation=45, ha='right')

        # loop over plot and generate bar variables
        for bar in plot:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     str(int(height)), ha='center', va='bottom')

        # set axis and title names
        plt.xlabel('Category')
        plt.ylabel('Likes Count')
        plt.title('Likes Count by Category')

        # define target folder path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "figure")

        chart_folder = os.path.join(
            file_path, 'generate_likes_count_figure.png')

        plt.savefig(chart_folder)

    @staticmethod
    def generate_discount_likes_count_figure():
        """
        This function generates a scatter plot into the figure folder containing the relationship
        between products likes counts and discount rates
        """

        # call custom method to create products data frame
        products_df = ProductOperation.create_products_df()

        # reduce the data frame to two targeted fields
        df = products_df[['discount', 'likes_count']]

        # set plot size and create scatterplot
        plt.figure(figsize=(10, 6))
        plt.scatter(x=df['discount'], y=df['likes_count'],
                    marker='v', alpha=0.3)

        # set axis and title names
        plt.ylabel('Likes Count')
        plt.xlabel('Discount (%)')
        plt.title('Likes Count & Discount Scatter Plot')

        # define target folder path
        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "figure")

        # set figure name
        chart_folder = os.path.join(
            file_path, 'generate_discount_likes_count_figure.png')

        # save figure in target folder
        plt.savefig(chart_folder)

    @ staticmethod
    def delete_all_products():
        """
        This function deletes/truncates all data in the products text file
        """

        parent_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(parent_path, "data", "products.txt")

        open(file_path, 'w').close()
