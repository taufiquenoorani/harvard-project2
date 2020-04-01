# Project 2

## Login.html
As soon as the user logs in, they will be displayed with the login page. User will have to provide username to proceed to the next page

## Create.html
After user enters the display name, they will be redirected to this page. User will have to enter the channel name to proceed.

## Channels.html
This page will provide users with the list of channels and users. By default, general channel is always available for all users. Clicking on the channel will take you to that channel. Users can click on the + sign icon next to "Channels" to create a new channel. Users can see the list of users available. Users can logout by hitting the power sign next to the username. For the "Personal Touch", I have added the ability for users to DELETE channels which will remove all the messages in that channel. Users CANNOT delete the default "general" channel.

## Layout.html
Layout is the template page that populates scripts, flash messages and header to each page.

## Style.css
It has styling for all tags, classes, ids.

## 404.html
If user browse to an incorrect URL, they will be displayed with a custom 404 error.

# Index.js
Handles messages incoming and outgoing messages.

# Application.py
This file is the main logic behind this project. The file contains routes to all pages and how to handle user requests when they come in.
