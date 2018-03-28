TV Trail

TV Trail is a web application designed to track the progress of your favourite TV Shows. Our TV Show Database is populated using the TMDb API.

The live version of this application can be found at:

--> http://tvtrail.pythonanywhere.com

Note: You have to register or login to use any of our services.
Our live version is populated with around 40  TV Shows to demonstrate the functionality of our web application.

To set up the application on your own machine, follow these steps:

1. Clone the repository into your workspace

git clone https://github.com/JawadMahmoud/TV_Trail.git

2. Navigate to your local repo and run the following commands

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python populate_script.py

Note: We have reduced the number of TV Shows that you can populate your local version of the application with. We have provided a list of only 4 TV Shows to ensure the population of the database does not take too much time. (Population should take around 3-4 minutes)

3. Run the server from your local machine

python manage.py runserver

Note: You will again need to register a user for you to be able to use the application.

Thank you for trying our application. This was created in three weeks by a team of four students.

