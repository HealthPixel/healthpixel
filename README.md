# HealthPixel
HealthPixel is a web application designed to streamline the process of accessing and updating patient medical records. The platform enables healthcare professionals to quickly retrieve a patient’s medical history, update records in real time, and ensure that patient data remains secure and accessible.

## Features
1. Quick Access to Patient Records
Healthcare professionals can quickly access a patient's complete medical history by entering their unique ID into HealthPixel, allowing for informed decision-making without needing the patient to recount their medical history.

2. Patient Data Privacy
HealthPixel prioritizes patient data privacy, ensuring that only authorized healthcare professionals can access medical records. The platform employs secure authentication, and audit logs (in view) to maintain confidentiality.

3. Updating Patient Records
After consultations or treatments, healthcare professionals can easily update patient records with new test results, diagnoses, or treatments. This ensures that the latest medical information is always available for future visits.

4. Real-Time Patient Access
Patients can securely view their medical information in real time through unique, secure links provided by healthcare professionals. This feature eliminates the need for a traditional login interface while maintaining data security.

## API Endpoints
HealthPixel offers a set of RESTful API endpoints for managing patient records, user authentication, and data access:

__Authentication__

- POST /api/auth/login - Authenticate healthcare professionals.
- POST /api/auth/logout - Log out of the system.
- POST /api/auth/register - Register a new healthcare professional (admin use).

__Patient Management__

- GET /api/patients/:id - Retrieve patient records.
- POST /api/patients - Register a new patient.
- PUT /api/patients/:id - Update patient records.

## Installation
__Clone the repository:__
```
git clone https://github.com/HealthPixel/healthpixel.git
cd healthpixel
```

__Install dependencies:__
```
pip install flask
pip install flask-login
pip install sqlalchemy
pip install flask_sqlalchemy
sudo apt-get install pkg-config libmysqlclient-dev
pip install mysqlclient
```

__Set up the database:__
- You need to have a MySQL server running in your terminal to store the db, If you don't have it you can follow this article to install it.
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
(change the distribution or Ubuntu version to the one you're running)
- Once your MySQL server is installed and running, you need to make sure `root` authenticates with a password by using either the `mysql_native_password` or `caching_sha2_password` authentication plugin (the article explains how to do that)

__Create a MySQL database and configure the connection settings in the set_env_var file:__
```
sudo mysql -u root -p < setup_mysql_db.sql
source set_env_var
```
__Start the application:__
```
python3 -m api.app 
```

## Usage
Once the application is up and running, healthcare professionals can log in using their credentials to access patient records, update information, and manage patient data. Patients can view their records using secure links provided by their healthcare providers.

### Dependencies

You need to have a MySQL server running in your terminal to store the db, If you don't have it you can follow this article to install it (change the distribution or Ubuntu version to the one you're running)
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

### Below are other dependencies you'd need to run the flask application;
- pip install flask
- pip install flask-login
- pip install sqlalchemy
- pip install flask_sqlalchemy
- sudo apt-get install pkg-config libmysqlclient-dev
- pip install mysqlclient

### Run App
```
ubuntu@ubuntu:/healthpixel $ source set_env_var

ubuntu@ubuntu:/healthpixel $ sudo mysql -u root -p < setup_mysql_db.sql

ubuntu@ubuntu:/healthpixel $ python3 -m api.app
```

## Authors
- Samuel Odumu [Github](https://github.com/samuelodumu) / [Email](themainsamuel@gmail.com) - Frontend Development and API Testing
- Keith Juma [Github](https://github.com/TaiKeith) / [Email](keithsteve.ks@hotmail.com) - Database and Backend Development
- Fortune Iheanacho [Github](https://github.com/na-cho-dev) / [Email](fortuneihean0314@gmail.com) - Backend and Frontend Development

## Contributing
We welcome contributions to HealthPixel! Please fork the repository, create a new branch, and submit a pull request with your changes. Make sure to follow our coding guidelines and include tests where applicable.

## License
HealthPixel is licensed under the MIT License. See the LICENSE file for more information.

## Contact
For questions or support, please open an issue on GitHub or contact us at healthpixelproject@gmail.com.
