# Report Manager Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Database Models](#database-models)
6. [Views and Templates](#views-and-templates)
7. [Utils and Caching](#utils-and-caching)
8. [Exporting Data](#exporting-data)
9. [User Authentication](#user-authentication)
10. [Contributors](#contributors)
11. [License](#license)

## 1. Introduction

The "Report Manager" project is a web application developed using Django, a popular Python web framework. It provides a platform for managing projects and tasks, exporting project data to CSV, and caching project statistics.

## 2. Project Overview

The project is structured as follows:

- **Project Name**: Report Manager
- **Django App**: reporter

## 3. Installation

To run the project locally, follow these steps:

1. Clone the project repository from [GitHub](https://github.com/yourusername/report-manager.git).

2. Create a virtual environment for the project.

   ```shell
   python -m venv venv


3. Activate the virtual environment.
    * on Windows:

   
      ```shell
      venv\Scripts\activate

      
    * On macOS and Linux:
    
      ```shell
      source venv/bin/activate

      
4. Install project dependencies:

   
      ```shell
        pip install -r requirements.txt


6. Apply database migrations:

    ```shell
    python manage.py migrate

  
8. Start the development server.

   ```shell
    python manage.py runserver
      
The project will be accessible at http://localhost:8000/.

  
## 4. Configuration

The project configuration is stored in the `settings.py` file. It includes database settings, static files, and other project-specific configurations. Make sure to configure your settings as needed.


## 5. Database Models

### Project Model

- Fields:
  - `name`: The name of the project.
  - `description`: A short description of the project.
  - `created_at`: The creation date of the project.
  - `status`: The project status (Active, Draft, Completed).
  - `cost`: The project cost.

### Task Model

- Fields:
  - `name`: The name of the task.
  - `user`: The user associated with the task.
  - `project`: The project associated with the task.
  - `status`: The task status (To Do, In Progress, Done, Cancelled).
  - `created_at`: The creation date of the task.

## 6. Views and Templates

The project includes several views and templates for rendering the user interface, including:

- `data_view`: Displays project and task data, along with statistics.
- `export_csv`: Allows users to export project data to a CSV file.
- `index.html`: The main template for the user interface.
- `table.html`: Template for displaying project data in a table.
- `cards.html`: Template for displaying project statistics in cards.
- `card.html`: Template for individual statistic cards.

## 7. Utils and Caching

The project uses a utility function `get_project_stats` to calculate and cache project statistics, reducing database queries. Cached values include the total number of projects and the number of active projects.

## 8. Exporting Data

The `export_csv` view allows users to export project data to a CSV file. Users can filter the data by task status and download the CSV file with the selected data.

## 9. User Authentication

User authentication and authorization utilizing Django's built-in authentication system. The User model is referenced in the Task model.

## 10. Contributors

- [Ait Hammou Khaled](https://github.com/AiHKhaled) - Project Lead

## 11. License

This project is licensed under the [MIT License](LICENSE). You can find the full license text in the `LICENSE` file.

---
