Project details

This project requires you to create an e-commerce system allowing customers to log in and perform shopping operations like purchasing products, viewing order history and showing user consumption reports. 
Admin users need to be created to manage the whole system, who can create/delete/view customers, products and all the orders. Except for the management part, admin users can view the statistical figures about this system. 
Since the whole system is executed in the command line system, designing a well-formatted interface is better and always showing proper messages to guide users to use your system. In this project, we use open-source data from data.world, which contains 9 files of products. 
All the product's data should be retrieved from these files.

In this project, we will decouple the relationship between various classes. As you can see from the following image, we have four main parts, and when using the system, end users only need to interact with the IOInterface class. 
The Main Control class handles the main business logic. The operation classes use the model classes as templates to manipulate the data reading/writing. With this design pattern, the input() and print() functions only exist in the I/O interface class. No other classes have these functions. 
The file reading/writing operations happen in the operation classes, which simulate the database activities.
