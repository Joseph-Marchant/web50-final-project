# Joseph Marchant CS50W Capstone

## What is the project?
My Capstone is a huge overhaul of my final project for CS50, Self-Shot. I have taken the movie editing code out of that project and adapted to work with the Django framework and all the addiditonal features that weren't there before. The HTML, CSS, Javascript and anything Python (that doesn't relate to Moviepy) were all written brand new from the ground up.

Now the project is used more generally for keeping track of your auditions, when they are, what you need to prepare for them and if you need to add a self tape then you can do so as before but the form is much simpler. The process is now a lot more automated.

## Distinctiveness and Complexity
While I have drawn inspiration from other projects completed on this course, this is not a copy of any of them. This project is about one user being able to view,  change, add and act upon information they alone control to help support thier career as an actor. It is a solution to the many times I have thought, "I wish there was an app that did..." It does not serve the purpose that previous projects did.

For complexity, I have utilized 3 django models, that are related together, which are more specifiic to my use case than previous projects. With the user model, rather than simply use Django's abstract user I have adapted it to further serve the purpose of my application. I have also dealt with file management, something never covered in a previous project. I have used Django's FileSystemStorage to deal with users uploading a self tape and then returning the edited selftape back to the user and cleaning up the files after this process has been completed. Additionally I have implemented a framework, not used previously, with cleave.js

To make it mobile responsive I have utilized various CSS properties to rescale or reorder the information on screen based on the size of the viewport.

## File overview

- `audition/views.py`: This handles all data received from the user and responds appropriately, whether that is as simple as requesting a page (such as index) or submitting a form (for something like new_audition). It interacts with other elements of the application as required. It will also handle all api requests from the Javascript code for index, make sure every submitted form is valid, send all data to movie.py when required and handle the authentication of the user.

- `audition/movie.py`: Adapted from Selfshot, this file contains the functions to validate and set the start and end times of the clip, if the user wishes to crop them, make the slate, and render a final edited selftape complete with the slate. This has been adapted from my CS50 final project to work within the django framework.

- `audition/models.py`: This contains the 3 models used in this app. User, which is a slightly adapted version of Django's abstarct user to include typical actor's information (their agent and spotlight pin). Audition, a model that keeps track of all auditions in the system and is tied with the User model. Finally, Script for any scripts users need to prepare for their audition; this is linked to the Audition model. Audition and Script both have serialize functions for JSON requests when called by index.js.

- `audition/forms.py`: I have abstraced the forms out of views into forms.py for neatness. The forms for New Auditions and Self Tapes are found in here.

- `audition/admin.py`: This is where I have added the models to be accessible in django's admin interface. You need to create a SuperUser to access this.

- `audition/urls.py`: This is where all of the paths for the application are set out. This includes HTML paths, JS paths and the path for the FileStorageSystem.

- `audition/static/audition/cleave.js, crop_timings.js and pin.js`: I have used the cleave framework for a bit of user experience. When inputting your spotlight pin and time codes for the crop, the input fields will automatically set themselves to be in the format required for the database. cleave.js is a dependancy written by the creator, crop_timings.js and pin.js are what I have written that uses that framework.

- `audition/static/audition/index.js`: Used on the index page, this is for when a user clicks on the view or delete button for an audition. Rather than loading a separate webpage, it will simply make an api call to the server to get the required information and then hide/show relative elements. Given this was the main page of the site, I wanted it to be quick and simple to use, therefore this was a better approach to display multiple pages. It also allows the user to edit and delete any of the scripts stored for that audition. index.js will display the changes straight away and send the updated information to views.py to save in the server. 

- `audition/static/audition/styles.css`: This is where I have written all the stylings used throughout the site. This is called in layout.html as I have reused elements across different pages if I wanted them to be in the same style. I have styled the website in a way where it will be responsive to mobile use as well as desktop use.

- `audition/templates/audition`: In templates you will find index.html, info.html, layout.html, login.html, new_audition.html, register.html and self_tape.html. These are the templates rendered by views.py. I have used Jinja logic to make the page a little more dynamic when it comes to displaying information, which has allowed me to use error messages and other responses to the user where relevant.

- `files`: This is the folder where files are downloaded to and served from.

- `final`: These are set up by Django to deal with the running of the application. Settings.py holds all the settings for the server, urls.py has the routes for the server.

- `manage.py`: Used for setting up and running the server.

- `db.sqlite3`: The database that stores all information created by the models.

## Deploying to web
To run, simply install the dependancies in requirements.txt and run the server. If you install all optional dependanices for MoviePy (only Image Magick is required), then you may have to check for any additional dependancies although this should not be required.

Once everything is installed just type `python manage.py runserver` into the terminal and follow the link.

## How to use
As a user you need to start by registering for an account. By default you will be taken to the login page, you can access the register page by either using the nav bar at the top or clicking the link at the bottom of the login form. Once registered and logged in you will be taken to the main page where you can see all of your auditions, although you won't have any yet.

The "Your Information" tab allows you to add and update information about your agent, full name and Spotlight pin. This information is required if you wish to use the Self-Shot portion of this website. If you just wish to use this as an audition planner then this information is not required.

To add an audition click "Add Audition" in the nav bar and fill out the form. The scripts and script titles are optional, if you choose to add them then I have provided the syntax you need to seperate scripts so you don't need to fill out the form several times for one audition. After submitting you should be able to see your audition in "Your Auditions".

To get a more detailed view of your audition you can click on the view button of any of your upcoming auditions. This will show you all the scripts you submitted for that audition. Here you can edit and delete those scripts. You can also submit a self tape to Self-Shot to get the slate added and crop your video if needed.

If you click on Self-Shot then you will be taken to a form where you need to upload your self tape, choose where you want the slate, how long you would like the slate to be, and add any crop timings (if you want to). Once you click submit the server will add the slate for you and redirect you afterwards to a page with the video. To download your edited self tape just right click and save video.

## Disclaimer
This application makes use of the Bootstrap Framework (found here [https://getbootstrap.com/docs/5.1/getting-started/introduction/](https://getbootstrap.com/docs/5.1/getting-started/introduction/)) which I used to save a bit of time with CSS.

It also uses cleave.js (found here [https://nosir.github.io/cleave.js/](https://nosir.github.io/cleave.js/)) which I used to create the auto formatting in Your Information and Self-Shot.
