# Joseph Marchant CS50W Capstone

## What is the project?
My capstone is a huge overhaul of my final project for CS50, Self-Shot. I have taken the movie editing code out of that project and adapted to work with the Django
framework and all the addiditonal feature that weren't there before. The HTML, CSS, Javascript and anything Python that deosn't relate to Moviepy were all
written brand new from the ground up.

Now the project is used more generally for keeping track of your auditions, when they are, what you need to prepare for them and if you need to add a self tape then
you can do so as before but the form to do so is much simpler. The process is now a lot more automated.

## Distinctiveness and Complexity
While I have drawn inspiration from other projects completed on this course, this is not a copy of any of them. This project is about one user being able to view, 
change, add and act upon information they alone control to help support thier career as an actor. It is a solution to the many times I have thought, "I wish there 
was an app that did..."

## What the files do

### views.py
This handles all data received from the user and responds appropriately. Whether that is as simple as requesting a page (such as index) or submitting a form (for 
something like new_audition). it interacts with other elements of the application as required. It will also handle all api request from the Javascript code for index, 
make sure every sublitted form is valid, send all data to movie.py when required and handle the authentication fo the user.

### movie.py
Adapted from Selfshot this file contains the functions to validate and set the start and end times of the clip, if the user wishes to crop them, make the slate, and 
render a final edited sleftape complete with the slate. This is mostly brought over from my previous project, it has been tweaked to work within the Django framework.

### models.py
This contains the 3 models used in this app. User which is s aslightly adapted version of Django's abstarct user to include typical actor's information (their agent 
and spotlight pin). Audition, a model that keeps track of all auditions in the system and is tied with the User model. Finally, Script for any scripts users need to 
prepare for their audition, this is linked to the Audition model. Audition and Script both have serialize functions for JSON requests when called by index.js.

### forms.py
I have abstraced the forms out of views into forms.py for neatness. The form for New Auditions and Self Tapes are found in here.

### cleave.js, crop_timings.js and pin.js
I have used the cleave framework for a bit of user experience. When inputting your spotlight pin and time codes for the crop the input fields will automatically set 
themselves to be in the format required for the databse. cleave.js is a dependancy written by the creator, crop_timins.js and pin.js are what I have written that 
uses that framework.

### index.js
Used on the index page this is for when a user clicks on the view or delete button for an audition. Rather than loading a seperate webpage it will simply make an 
api call to the server to get the required information and the hide/show relative elements. Given this was the main page of the site I wanted it to be quick and 
simple to use, therefore this was a better approach to display multiple pages. It also allows the user to eidt and delete any of the scripts stored for that audition. 
index.js will display the changes straight away and send the updated information to views.py to save in the server. 

### styles.css
This is where I have written all the stylings used throught the site. This is called in the layout.html as I have reused elements across different pages if I wanted 
them to be in the same style. I have styled the websote in a way where it will be responsive to mobile use aswell as desktop use.

### templates
In templates you will find index.html, info.html, layout.html, login.html, new_audition.html, register.html and self_tape.html. These are the templates rendered by 
views.py. I have used Jinja logic to make the page a little more dynamic when it comes to displaying information, which has allowed me to use error messages and other 
repsonses to the user where relevant.

## How to use
To use simply install the dependancies in requirement.txt and run the server. If you install all optional dependanices for MoviePy (only Image Magick is required), 
then you may have to check for any additional dependancies although this should not be required.

## Marking movie.py
Although it is part of the submission (due to the code being required) I do not consider the contents of movie.py as part of my submission. This code was the basis 
for my final project for CS50 and, while I have adapted it to work within a new framework, I do not consider it to be unique enough to the original project to 
warrant it being part of the full submission. I consider it to be more of a low level framework used like cleave.js and request that it is not 
marked. Everything else I have written is new and I do consider to be part of my submission.
