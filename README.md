# Barebones Chatroom Utilizing Django and Websockets

## Prerequisites

- Docker

## Installation

In your terminal, navigate to an empty folder and run the following command:

```
git clone git@github.com:lymanjohnson/django-websockets-chatroom.git
cd django-websockets-chatroom
docker compose build --no-cache
docker compose up
```

Then, in your browser, navigate to http://localhost:8000/chat/

## General Notes
- User authentication and storage is handled synchronously using basic django session-based authentication.
- You can use another browser on the same machine to login in as multiple users.
  - Some browsers may also allow you to have multiple windows open at the same time with separate sessions for each window.
- The user database is stored in a sqlite file. Rebuilding the container from scratch will clear the database.
- Chat functionality is handled asynchronously through websockets and redis. 
- The chat logs are completely ephemeral in this implementation. They are not stored in any persistent storage, nor are they stored in the browser local storage. 
  - Refreshing the page will clear the chat log
  - You will not see any messages that were sent while you were not currently in a chat room

## Attributions

- This chatroom is based heavily on the Django Channels tutorial chatroom found here: https://channels.readthedocs.io/en/3.x/tutorial/index.html
- Login and Signup Screens are based on Bootstrap 5 Example Templates
- AI tools were consulted during the creation of this app, particularly while writing Dockerfile and compose.yaml