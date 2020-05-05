&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![](UI/essential_main_logo2.png)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) 
## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Team Members
```
                                               Loven Garcia
                                           Richard Vincent Chua
                                             Louisse Velasco
                                           Fil Janses Tapaganao
                                               Jeloux Docto
                                               Jarl Centeno
                                               Flynn Alcaraz
```
## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Instructor
```
                                           Engr. Dionnis Padilla
```
## Overview

Essentials Hub is a python program designed to provide people convenience during times of calamities, pandemic diseases, and other hazardous events. The goal of this application is to implement various services like a store management system wherein consumers will be able to view and select essential products that are most needed during calamities. A facts and statistics page where users can be informed regarding the problems that they are facing. Lastly, a blog section where they can comment on certain issues regarding the application. 

## Setup and Installation

To be able to run the application, you need to have a new environment with Python 3.6 on it. 
If you have anaconda installed, open the terminal and execute the code below
```
conda create -n E-Hub_env python=3.6
```

Once you have created a new envriment, just activate it
```
conda activate E-Hub_env
```

### Requirements

<ul><li> <b>Pillow</b></li>
<li> <b>secure-smtplib</b></li>
<li> <b>bs4</b></li>
<li> <b>requests</b></li>
<li> <b>pandas</b></li>
<li> <b>pandastable</b></li>
<li> <b>matplotlib</b></li>
<li> <b>tensorflow version1.14.0</b></li>
<li> <b>nltk</b></li>
<li> <b>tflearn</b></li>
<li> <b>numpy</b></li>
<li> <b>Gotham Family Font (https://freefontsfamily.com/gotham-font-family/)</b></li></ul>

Examples
```
pip install pandas
```
```
pip install tensorflow==1.14.0
```

## Objectives

The objectives of the project are the following:
- To create an online shopping program specified for calamities.
- To collect info regarding COVID-19 cases and their localities in the Philippines.
- To visualize the gathered information into appropriate graphs.
- To create an Artificial Intelligence for convenience in terms of query.
- To develop a blog section for a direct communication between the client and administrator.

## User Stories

### List of all User Stories

- **User stories (Customers)**
  + **Sign-up form**
    + As a customer, I want to be able to create my personal account.
  + **Forgot password feauture**
    + As a customer, I want to be able to change my password in case I forgot it.
  + **Sign-in form**
    + As a customer, I want to be able to log-in to the application for me to use the services offered by the program.
   
  + **Online Shop main GUI**
    + As a customer, I want to be able to shop online using the app, I want to see different features like add to cart, view my cart, view all products, search for items, and view or add ratings to products.
  + **View all Products**
    + As a customer, I want to be able to view all the essential products that are available to the store.
  + **Search for products (By name)**
    + As a customer, I want to be able to search for the product that I want through its name.
  + **View my cart**
    + As a customer, I want to be able to view my cart along with the its details (ID, name, price, quantity)
  + **Save Receipt**
    + As a customer, I want to be able to save my receipt to a text file.
  + **Facts and Statistics main GUI**
    + As a customer, I want to be able to view substantial statistics that are helpful in understanding the details of a certain calamity or pandemic diseases. I also want to see a button for the visualization and for the chatbot.
  + **Graphs Visualization**
    + As a customer, I want to be able to see useful graphs that are understadable and can explain the vital statistics about certain events/pandemic.
  + **Chatbot**
    + As a user, I want to be able to interact with a bot regarding the happenings during COVID19.
    
  + **Give comments/suggestions**
    + As a customer, I want to be able to send comments or sugestions regarding anything with the program. 
  + **Products Viewer**
    + As a customer, I want to be able to view the products alongside the comment box for me to easily remember the details for my comment/suggestions.
   
  + **About Us**
    + As a user, I want to be able to see the programmers involved in this application.
    
    
- **User stories (Administrator)**
  + **View all products**
    + As an admin, I want to be able to view all the remaining products in the database
  + **Add/Update/delete products**
    + As an admin, I wanto to be able to add/update/delete products to the database.

  + **View comments**
    + As an admin, I want to be able to view all the comments/suggestions of the customers
  + **Reply to comments**
    + As an admin, I want to be able to send  replies to the comments of the customers through their emails.
    
    
## Sample ScreenGrabs

### Launcher
![](UI/PICTURES_README/LAUNCHER.png)

### Sign-in Form
![](UI/PICTURES_README/SIGN-IN_FORM.jpg)

### Sign-up Form
![](UI/PICTURES_README/SIGN-UP_FORM.jpg)
![](UI/PICTURES_README/SIGN-UP_FORM2.jpg)

### Forgot Password Feature
![](UI/PICTURES_README/FORGOT_PASSWORD_FEATURE_0.jpg)
![](UI/PICTURES_README/FORGOT_PASSWORD_FEATURE_1.jpg)
![](UI/PICTURES_README/FORGOT_PASSWORD_FEATURE_2.jpg)
![](UI/PICTURES_README/FORGOT_PASSWORD_FEATURE_3.jpg)

### Main Page for Guests
![](UI/PICTURES_README/MAIN_GUI_FOR_GUESTS.jpg)

### Inventory Management System
![](UI/PICTURES_README/INVENTORY_MANAGEMENT_SYSTEM.jpg)

### Statistics Page
![](UI/PICTURES_README/STATISTICS_WINDOW.jpg)
![](UI/PICTURES_README/STATISTICS_WINDOW2.jpg)

### Graphs/Visualization
![](UI/PICTURES_README/GRAPHS_1.jpg)
![](UI/PICTURES_README/GRAPHS_2.jpg)
![](UI/PICTURES_README/GRAPHS_3.jpg)

### Chatbot 
![](UI/PICTURES_README/chatbot.jpg)
![](UI/PICTURES_README/chatbot2.jpg)

### Main Page for Admins
![](UI/PICTURES_README/MAIN_GUI_FOR_ADMIN.jpg)

### Inventory Management for Admins
![](UI/PICTURES_README/INVENTORY_MANAGEMENT_SYSTEM_FOR_ADMIN.jpg)








