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

----------------------------

the project contains different roles

admin --> has superuser

staff --> can access the admin, but has limited permissions

hairdresser --> cannot access the admin, in the site he can keep track of everyone's appointments but cannot make any

client --> cannot access the admin, in the site he can see his appointments and manage them create/cancel (if possible check the terms and policy of the hair salon under working hours)

note: when registering a new user he automatically gets the client role if you want to change his role you can do so through the admin with superuser permissions
----------------------------
