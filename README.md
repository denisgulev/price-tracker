# ONGOING...

#### Jan 17 2024
Setup a github workflow to create docker images and push then to dockerhub.
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
- Bright Data (Web Scraping Browser)

## Using the Scraper

Install all dependencies, create the `auth.json` file, start the flask backend, run the react frontend and interact with the tool.

### auth.json

Fill in your [Bright Data Scraping Browser](https://brightdata.com/products/scraping-browser) credentials in a `backend/scraper/auth.json` file (see `auth_example.json`).

### Python Flask Backend

- `cd backend`
- `pip install -r requirements.txt`
- `playwright install`
- `python app.py` or `python3 app.py`

### Running the React Frontend

- `cd frontend`
- `npm i`
- `npm run start`

## Setting Up Automation

To automate the collection of prices from this software simply run the `scheduler/main.py` file at your desired increment while the python flask backend is running.

### Windows

I have created a simple `.bat` script called `run.bat` that you can schedule to execute using the Windows Task Scheduler that will automatically run the backend api and send the appropriate request to it.


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

- Note: in alternative we can start both backend and frontend using 'docker-compose.yaml' file:
```
docker compose up --build
```
