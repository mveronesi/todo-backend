# TODO app

## Run in Docker
To run the whole app with docker
- docker compose up -d --build

this will serve the app on localhost:80 with an nginx container.

## Run without docker
To run the app outside docker:
- cd backend-app
- uvicorn main:app

while in the frontend repo
- npm i
- npm run dev

this will serve the app on localhost:5173.