This repo is related to a website that introduce an startup and shows the products they have. The functionality of purchasing items is also added, only one step is remained and that's connection to payment gateway.

In order to run the website after cloning, you need to configure some envoironment variables :
# The Credentials of database
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

# The Credentials of pgadmin
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD

# The Password for redis db as both cache and message boker
REDIS_PASS
SECRET_KEY

# The API-Key from the service responsible for sending messages
KAVENEGAR_API_KEY
    note :
    You can initialize the website with a fake key for now, because the functionality that actually send sms to your mobile is commented(accounts.tasks.send_otp) and instead it prints the code that was supposed to be sent to your mobile. But keep in mind whether you run this project locally or with docker the printed code(otp) will be printed in celery logs terminal not the terminal that is running the django application.

# The Credentials for superuser that docker-compose creates it with help of 'python manage.py initadmin'
DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_PASSWORD