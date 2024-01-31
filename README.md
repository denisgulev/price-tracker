# ONGOING...

#### Jan 31 2024
Cleaning code + README

#### Jan 21 2024
Added rate_limit for all endpoints, settings:
```
default_limits=["6 per minute, 48 per hour"]
```



#### Jan 17 2024
Setup a github workflow to create docker images and push then to [dockerhub](https://hub.docker.com/repositories/dman93).
The action will be triggered when a PR is successfully merged into 'main' branch.

The images will have the following name structure:
```
${{DOCKER_USERNAME}}/tracker-backend:latest
```
and
```
${{DOCKER_USERNAME}}/tracker-frontend:latest
```

<b>NOTES</b>
1) inside the workflow, ${{ github.repository }} was returning REPO_OWNER/REPO_NAME and that was producing and error when trying to push image to dockerhub
2) explore methods to assign different tags to the image (either auto-generated or retrieved from this repository)


# Project Information

This project provides a user interface to interact with an automated price tracking web scraper. Currently the tracker scrapes amazon.ca, but could be configured to scrape multiple sources.

## Libraries/Frameworks/Modules

This project uses:

- React
- Flask
- Playwright

## Using the Scraper

### Start Local Environment

- start postgresql in docker 
```
docker run --name scraper_db -e POSTGRES_PASSWORD=password -p 5432:5432 postgres 
```

- build image from Dockerfile
```
docker build -t price_tracker .
```

- start docker container from image
```
docker run --rm -it -p 5000:5000 price_tracker
```

- start FE app
```
cd frontend
npm run start
```

- <b>NOTE</b>: in alternative we can start both backend and frontend using 'docker-compose.yaml' file:
```
docker compose up --build
```
