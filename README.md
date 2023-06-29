# TRIVIA APP  
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, inclusive of an API to facilitate communication between the application frontend and backend.

* Base API functionality is as follows:
    * Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer.
    * Delete questions.
    * Add questions and require that they include the question and answer text.
    * Search for questions based on a text query string.
    * Play the quiz game, randomizing either all questions or within a specific category.  

The app is intended to only be run locally. 

*Note: All code examples provided below (other than JSON request/response bodies) are specifically applicable to the Command Prompt application in Windows environments.*
***
***
***

# Backend
The `backend` directory contains a Flask and SQLAlchemy server.
* The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.  
* API endpoints are specified in `__init__.py` (`flaskr` folder).  
* `models.py` contains class defintions for Questions and Categories, as well as an initial database setup function `setup_db(app)`.


## Setup
### Install Required Software
* **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).
    * Due to various library dependencies, we highly recommend running this application using Python 3.7 - later versions will require modifications to dependency installations (`requirements.txt`).  
* **Virtual Environment** - Recommend working within a virtual environment when using Python for local projects. This keeps dependencies for each project separate and organized. Instructions for setting up a virtual environment for your operating system can be found in the [python docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).  
    * Sample virtual environment setup:  
    ```console
    py -3.7 -m venv venv
    .\venv\Scripts\activate
    ```  
* **Postgres** - See installation instructions for your operating system here: [PostgreSQL Downloads](https://www.postgresql.org/download/).  

### Install Dependencies
Once virtual environment is setup and running, install the required dependencies by navigating to the `backend` directory and running:  
```console
pip install -r requirements.txt
```  

### Set up and Populate the Database
* The following instructions assume you are using a Postgres username `'student'` and have installed *PostgreSQL 15*.
* With Postgres running, create a `trivia` database (assume `localhost:5432` by default):  
```console
createdb -h localhost -p 5432 -U student trivia
```  
* From the `backend` folder in the terminal, populate the database using the `trivia.psql` file provided by running:  
```console
psql -U student -d trivia < trivia.psql
```  

### Start the Server
Again from the `backend` directory, start the Flask server by running:  
```console
set FLASK_APP=flaskr
set FLASK_ENV=development
python -m flask run
```  
Setting `FLASK_ENV` to `development` is convenient as it displays an interactive debugger in the console and restarts the server whenever changes are made.

### Key Pip Dependencies
* [**Flask**](https://flask.palletsprojects.com/en/2.3.x/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
* [**SQLAlchemy**](https://www.sqlalchemy.org/) is the Python SQL toolkit and Object-Realtional Mapping (ORM) used to handle the lightweight SQL database. Primarily used in `app.py` and `models.py`.
* [**Flask-CORS**](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross-origin requests from frontend server.  

***
***

## Deploying Tests
To maintain test integrity, you'll need to manually set up and populate the testing database:
* To initialise the test database, run:  
```console
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```  
_Note: `dropdb trivia_test` can be ommitted for initial database creation._  


* To deploy the tests, run:  
```bash
python test_flaskr.py
```  
All tests are kept in `test_flaskr.py` and should be maintained as updates are made to app functionality.

***
***
***

# Frontend
The `frontend` directory contains a complete React frontend to consume the data from the Flask server.

* By default, the frontend will run on `localhost:3000`.  
* With respect to the API, you can work within the `components` folder in order to understand, and if desired, edit the endpoints utilized by the components.   


## Setup
* The frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected.  
* Recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Frontend Dependencies
1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). To run the frontend application, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the `package.json` file located in the `frontend` directory. After cloning, open your terminal and run:

```console
npm install
```  

*Note: `npm i`is shorthand for `npm install`*

### Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```console
npm start
```  
 
***
***  
***

# API
## Setup
* **Base URL:** At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.  
* **Authentication:** This version of the application does not require authentication or API keys.  


## Expected endpoints and behaviors  

#### Get all categories present in database
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None.
- Returns: An object with a single key, `categories`, that contains an object of {id:category_string} key:value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
- *Sample request*: `curl -v http://127.0.0.1:5000/categories`

***

#### Get all questions present in database
`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, total number of questions in database, all categories in database and current category string.
- Request Arguments: `page` (integer).
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string.

```json
{
  "questions": [
    {
      "id": 36,
      "question": "Who is the leading wicket taker in international cricket test matches?",
      "answer": "Muttiah Muralitharan",
      "difficulty": 3,
      "category": 6
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Sports"
}
```
- *Sample request*: `curl -v http://127.0.0.1:5000/questions`

***

#### Get all questions present in database for a specific category
`GET '/categories/${id}/questions'`

- Fetches questions for a category specified by `id` request argument.
- Request Arguments: `id` (integer).
- Returns: An object with questions for the specified category, total questions in category, and current category string.

```json
{
  "questions": [
    {
      "id": 66,
      "question':'What does DNA stand for?",
      "answer':'DeoxyriboNucleic Acid",
      "difficulty": 4,
      "category": 1   
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Science"
}
```
- *Sample request*: `curl -v http://127.0.0.1:5000/categories/1/questions`

***

#### Delete question from database
`DELETE '/questions/${id}'`

- Deletes a specified question using the `id` of the question.
- Request Arguments: `id` (integer).
- Returns: Returns the former `id` of the deleted question.

```json
{
  "deleted": 1
}
```
- *Sample request*: `curl -X DELETE -v http://127.0.0.1:5000/questions/20`

***

#### Add a new question to database
`POST '/questions'`

- Sends a post request in order to add a new question.
- Request Body:

```json
{
  "question": "What is the capital of Australia?",
  "answer": "Canberra",
  "difficulty": 3,
  "category": 3
}
```

- Returns: The `id` value of the newly created entry and the updated total of questions in the database.  

```json
{
  "created": 101,
  "total_questions": 101
}
```
- *Sample request*: `curl -X POST -H "Content-Type:application/json" -d "{\"question\":\"What is the capital of Australia?\", \"answer\":\"Canberra\", \"category\":3, \"difficulty\":3}" -v http://127.0.0.1:5000/question`

***

#### Return questions in database that contain a specified value (string)
`POST '/questions'`

- Sends a post request in order to search for a specific question by `searchTerm`.
- Any question where `searchTerm` appears within the overall string will be returned.
- Request Body:

```json
{
  "searchTerm": "capital"
}
```
- Returns: An array of questions, the number of `totalQuestions` that met the search term and the current category string.

```json
{
  "questions": [
    {
      "id": 101,
      "question": "What is the capital of Australia?",
      "answer": "Canberra",
      "difficulty": 3,
      "category": 3
    }
  ],
  "totalQuestions": 101,
  "currentCategory": "Geography"
}
```
- *Sample request*: `curl -X POST -H "Content-Type:application/json" -d "{\"searchTerm\": \"title\"}" -v http://127.0.0.1:5000/questions/search`

***

#### Get next trivia question
`POST '/quizzes'`

- Sends a post request in order to get the next trivia question.
- The category selection when the request is made (including 'All') determines the questions available for selection.
- Returned question is selected randomly from the available subset of questions with equal probability.
- When all questions for the current category/ies have been returned, an empty `question` value will be returned.
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": "current category"
 }
```

- Returns: a single new question object.

```json
{
  "question": {
      "id": 101,
      "question": "What is the capital of Australia?",
      "answer": "Canberra",
      "difficulty": 3,
      "category": 3
  }
}
```
- *Sample request*: `curl -X POST -H "Content-Type:application/json" -d "{\"previous_questions\":[2,4], \"quiz_category\":5}" -v http://127.0.0.1:5000/quizzes`

***
***

### Error Handling
* API errors are returned in json format and have the following standard structure:  
```
{
    'success': False,
    'error': 400,
    'message': 'Bad request - server unable to process.'
}
```  
* The API has in-built handling for the following errors:
    * 400: Bad request.
    * 404: Resource not found.
    * 422: Unprocessable content.
    * 500: Internal server error.