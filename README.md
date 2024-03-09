# Food Helper

* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [History](#history)
* [Todo](#todo)
* [Contact](#contact)

## General info
The Food Helper application allows you to help organize food which can you make. Application collect recipes (with its ingredients) which you can add to your account. After add your ingredients (in My Ingredients) system in Dashboard displays you all recipes recipes which can you made and recipes grouped up by number of missing ingredients.

## Technologies
<ul>
    <li>Python 3.11</li>
    <li>Django 4.2.7</li>
    <li>PostgreSQL</li>
    <li>pre-commit</li>
</ul>

## Setup
<ol>
    <li>Download project using Code button and choose Download ZIP option or clone the project.</li>
    <li>Extract files if you download zip file.</li>
    <li>Open food_helper-main folder as a project.</li>
    <li>Acoording to file .env.dist create .env file (in food_helper-main folder) with described variables.</li>
    <li>In PostgreSQL database food_helper must exist.</li>
    <li>Create virtual environment in IDE terminal with command "python -m venv venv_name" where venv_name is a name of created virtual environment.</li>
    <li>Execute venv/scripts/activate where venv is the name of created virtual environment.</li>
    <li>Install requirements from txt file by executing pip install -r requirements.txt in terminal.</li>
    <li>After installation write in terminal python manage.py runserver and open browser with displayed url address</li>
</ol>

## History
11.01.2024 - Created application with basic functionalities

## Todo
<ul>
    <li>Docker</li>
    <li>Api</li>
    <li>Mobile app</li>
</ul>

## Contact
Contact to author of project
<br>
gmail: mateuszszymaniak@protonmail.com
<br>
linkedin: https://www.linkedin.com/in/mateuszszymaniak/
