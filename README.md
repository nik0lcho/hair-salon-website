Glamour look - Hair salon website

steps to run the project

----------------------------

password protected .env file --> https://e.pcloud.link/publink/show?code=XZ4gzwZdLkntQwenBYDjMx7jjzBJXl254JX

password: Softuni student number

1) conncet to a database

2) migrate (after the initial migrations change the location of the `0002_group_permissions.py` to an other migrations directory for example `common/migrations`. This is the custom migration that defines the permissions of the staff group and run the migrations again)

3) open `utils/populate_schedule.py` and run it 

4) open `utils/my_daily_task.py` and run it

5) open `utils/populate_services.py` and run it
