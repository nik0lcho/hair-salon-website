# 💇‍♀️ Glamour Look – Hair Salon Website

A role-based web application for managing appointments in a hair salon. Built with Django.

## 🚀 Steps to Run the Project

- Clone the repository 

- Start a virtual environment

- Install the requirements

- Connect to a database and ensure your settings are correctly configured in `settings.py` or another config file.

- Run initial migrations:

- Move the custom permissions migration file `0002_group_permissions.py` to another app’s migrations folder (e.g., `common/migrations/`), then re-run migrations:

- Populate the database by running the following scripts:
- python utils/populate_schedule.py
- python utils/my_daily_task.py
- python utils/populate_services.py

## 👥 User Roles

Admin – Full access to the admin panel  
Staff – Limited access to the admin panel  
Hairdresser – Cannot access admin; can view all appointments  
Client – Cannot access admin; can view and manage their own appointments (create/cancel according to salon policy)

Note: When registering a new user, they are automatically assigned the Client role. To change the user’s role, use the admin panel with a superuser account.

## 🛠 Daily Task Automation

The `utils/run_daily.py` script is designed to be run in the background. It automatically triggers once a day at 00:00 and performs the following tasks:

Creates new available appointment dates with time slots  
Deletes outdated time slots, dates, and old appointments

This ensures the database stays clean and up-to-date with fresh availability.
