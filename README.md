![Python](https://img.shields.io/badge/Python-3.x-blue)


# E-commerce Command Line System

Welcome to the **E-commerce Command Line System**! This project enables users to perform various shopping operations and allows administrators to manage users, products, and orders directly from the command line.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Data Source](#data-source)
- [System Architecture](#system-architecture)
- [How to Run](#how-to-run)
- [Usage Guide](#usage-guide)
- [Contributing](#contributing)

---

## Project Overview

This project is a command-line-based e-commerce system where customers can:
- Log in and browse products.
- Purchase items and view order history.
- Access consumption reports.

**Admins** have additional functionality to:
- Create, delete, and view customers and products.
- View system-wide statistical data.

The system is designed with a clear, user-friendly interface and displays helpful messages to guide users through each operation.

---

## Features

### Customer Operations
- **Product Browsing**: View products from various categories.
- **Order Management**: Place orders and view past order history.
- **Reports**: Generate personal consumption reports.

### Admin Operations
- **User Management**: Create, delete, and view user profiles.
- **Product Management**: Add, remove, and manage product details.
- **Statistics**: Access system-wide analytics and statistics.

---

## Data Source

The project utilizes **open-source data from data.world**, consisting of **9 files** that contain product information. These files serve as the primary data source for product listings.

---

## System Architecture

This project follows a decoupled design with four main parts:

1. **I/O Interface**: This is the user-facing component that handles all inputs and outputs.
2. **Main Control Class**: Manages business logic.
3. **Operation Classes**: Handle data read/write operations and simulate database activities.
4. **Model Classes**: Define the data structure templates.

The **I/O Interface** class is the only class containing `input()` and `print()` functions, ensuring a clear separation of responsibilities.

Here's an overview of the architecture:

![System Architecture](link-to-your-image.png)

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git

