# Information Management System For A Blood Bank
Report Link: https://docs.google.com/document/d/1MZrnwYzGbihhWo9OdPqnqgWM3_yf3t5LY6qA_63C_xY/edit?usp=sharing
## Flask Commands:
Install Dependencies:
```
 pip install -r requirements.txt
```
Start the server:
```
export FLASK_APP='app.py'
```
Run the app:
```
flask run
```
## Database commands
### Open MySQL in terminal:
```
mysql -u root -p
```
If the above commands doesn't works then:
```
sudo mysql -u root -p
```
followed by updating the password using:
```
$ ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new-password';
```
Once this is done stop and start the mysql server:
```
$  sudo service mysql stop
$  sudo service mysql start
```


###Impot Dump
```
import the Dump files(.sql) in Dump folder
```
### View all databases:
```
SHOW DATABASES;
```
Creating a new database:
```
CREATE DATABASE bloodbank;
```
Use any database:
```
USE bloodbank;
```

## Snapshots

### Home Page
![Home Page](Screenshots/Home%20Page.png)

### Register
![Register](Screenshots/Register.png)

### Login
![Login](Screenshots/Login.png)

### Dashboard
![Dashboard](Screenshots/Dashboard%20Page.png)

### Add Donor
![Add Donor](Screenshots/Blood%20Donate%20Page.png)

### Donor Logs
![Donor Logs](Screenshots/Donors%20List%20page.png)

### Request Blood
![Request Blood](Screenshots/Request%20Blood.png)

### Blood Requests
![Blood Requests](Screenshots/Blood%20Request%20Page.png)

### Accepted Requests
![Accepted Requests](Screenshots/Accepted%20Requests%20page.png)
