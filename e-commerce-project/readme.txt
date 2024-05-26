Assessment details

This assessment requires you to create an e-commerce system allowing customers to log in and perform shopping operations like purchasing products, viewing order history and showing user consumption reports. 
Besides, admin users need to be created to manage the whole system, who can create/delete/view customers, products and all the orders. Except for the management part, admin users can view the statistical figures about this system. 
Since the whole system is executed in the command line system, designing a well-formatted interface is better and always showing proper messages to guide users to use your system. In this assessment, we use open-source data from data.world, which contains 9 files of products. 
All the product's data should be retrieved from these files.

In this assessment, we will decouple the relationship between various classes. As you can see from the following image, we have four main parts, and when using the system, end users only need to interact with the IOInterface class. 
The Main Control class handles the main business logic. The operation classes use the model classes as templates to manipulate the data reading/writing. With this design pattern, the input() and print() functions only exist in the I/O interface class. No other classes have these functions. 
The file reading/writing operations happen in the operation classes, which simulate the database activities.

Important notes
Do not use absolute paths and follow the exact structure for the path as provided in the examples in each section. All the path issues that cause your program to crash or an exception will lead to no mark for functionality.
You must implement all required methods, but you may add additional ones if required.
Please make sure your file reading/writing operations include encoding type utf8. Changing the application running environment could cause issues if you do not have the encoding type. Any character encoding issues/exceptions will cause serious mark deductions.
If one method is not working and it hinders the program from continuing to run to show other functionalities, the following functionalities will get no mark. For example, if your system cannot log in, the functionality that needs to be marked after login will get no mark, and you will only get marks for the menu part. Therefore, it is important to finish the methods one by one and make sure they can work properly.
If any exceptions/errors happen when running your program, you will lose 50% of the allocated function logic marks. For example, if the main menu function returns any error, the maximum mark you can get is 5% instead of 10% in the function logic.
Add correct validation and output messages to make your code user-friendly.
The assessment must be done using Pycharm, Python Version 3.9.
The Python code for this assessment must be implemented according to the PEP8-Style Guide for Python Code (PEP, 2023).
The allowed libraries are random, math, os, string, time, numpy, pandas, matplotlib, re. You will not receive marks for the components if you use any other libraries besides those mentioned.
In this assessment, it is required to add as many validation codes as you can to make sure your system always works. Any exception that happens in your system will lead to a mark deduction.
The Model and Operation classes should not contain any input/output operations, such as print()/input().
Commenting on your code is an essential part of the assessment criteria. In addition to inline and function commenting on your code, you should include comments at the beginning of your program file, which specify your name, Student ID, the creation date, and the last modified date of the program, as well as a high-level description of the program.
