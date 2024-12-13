# Racing Point Sheet
A simple app for managing sim racing events and keep track of points and scores.

# System Requirements
1. Docker
2. Node and Npm 

# Setup

1. Clone the repository. 
2. Update your hosts file to point to `pointsheet-app.com`. This is currently used by the `nginx.conf` file. Feel free to modify at will. 
```ini
127.0.0.1 pointsheet-app.com
127.0.0.1 api.pointsheet-app.com
```

# Run application. 
1. Change into the project directory - `racing-pointsheet`
2. Run `docker compose up`

# Initialize application database
1. Connect into the backend docker container. `docker container exec -it pointsheet-api`
2. Run the command to create db migration `alembic upgrade head`
3. This will create a database file in the folder `backend/pointsheet/instance/point_sheet.db.sqlite`
4. Open the db file in your favourite db view tool. 


# URLs: 
1. [pointsheet-app.com](pointsheet-app.com) is used for the Frontend powered by nextjs. 
2. [api.poiintsheet-app.com](api.pointsheet-app.com) is the backend rest api. The root path `/` contains OpenAPI spec for testing the URL.


### TODO:

- [ ] Add simple scripts for running routine commands for project.
- [ ] Add click/typre to make it easy to run commands in the container