import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


#Number of questions to display per page (constant).
QUESTIONS_PER_PAGE = 10


def paginate_results(request, selection):
    """
    Return results in a paginated fashion for efficiency.
    If not specified in request, default page number is 1.
    Results per page is equal to QUESTIONS_PER_PAGE.
    Questions are appropropriately formatted for frontend return (dictionary) as part of this function. 
    
    Args:
    * request: Initial request from application frontend.
    * selection: Full query result from database, based on request parameters.
    
    Returns:
    * current_questions: Current page of questions (as dictionary).
    """
    page = request.args.get('page', 1, type=int)
    questions = [question.format() for question in selection] #Note: Format is a method of the Question class in models.py.
    #Manually abort if requested page is in excess of the max possible number of pages, unless less than <QUESTIONS_PER_PAGE> questions are available.
    #Note: Request format is valid but actual instructions are unprocessable.
    if ((len(questions)/QUESTIONS_PER_PAGE) < page) & (page > 1):
        abort(422)
    #Manually abort if 'page' value supplied in request is not a valid integer.
    elif type(page) != int:
        abort(400)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/api/*':{'origins':'*'}})

    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')        
        return response

    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    Frontend request code: componentDidMount() (FormView.js).
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        """
        Return summary of all categories available in the trivia database and their internal indexes.
        Frontend request code: componentDidMount() (FormView.js, QuestionView.js, QuizView.js).
        
        Returns:
        * JSON object: {'success', 'categories'}.
        """
        try:
            #Select all category types from the Category object (models.py), ordering by index value. 
            categories = Category.query.order_by(Category.id).all()    
            #Convert received categories data into a dictionary (index:category_name) for passing to frontend.  
            categories = {x.id:x.type for x in categories}
            if len(categories) > 0:
                return jsonify({'success':True
                                ,'categories':categories})
            else:
                abort(404)
        except:
            abort(422)
        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Return all available questions in database, paginated into QUESTIONS_PER_PAGE groups.
        Also determine:
        - Total questions in database.
        - Category dictionary (all).
        - Current category ('None' for this request).
        Frontend request code: getQuestions() (QuestionView.js).
        
        Returns:
        * JSON object: {'success', 'questions', 'totalQuestions', 'categories', 'currentCategory'}.
        """
        try:
            #Select all questions from the Question object (models.py), without modifying received order.    
            questions = Question.query.all()                
            questions_paginated = paginate_results(request, questions)
            #Select all category types from the Category object (models.py), ordering by index value. 
            categories = Category.query.order_by(Category.id).all()         
            #Convert received categories data into a dictionary (index:category_name) for passing to frontend.  
            categories = {x.id:x.type for x in categories}
            if len(categories) > 0:
                return jsonify({'success':True
                                ,'questions':questions_paginated
                                ,'total_questions':len(questions)
                                ,'categories':categories
                                ,'current_category':None})
            else:
                abort(404)
        except:
            abort(422)
    
        
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['GET', 'DELETE'])
    def delete_question(question_id):
        """
        Delete question specified in request (referenced by id).
        Return the id of the deleted question for verification.
        Frontend request: questionAction [=> action='DELETE'] (QuestionView.js).

        Returns:
        * JSON object: {'success', 'deleted'}.
        """
        try:
            #Select the relevant question from the Question object (models.py).    
            try:
                question = Question.query.get(question_id)
            except:
                abort(404)
            question.delete()
            return jsonify({'success':True
                            ,'deleted':question_id})
        except:
            abort(422)
        

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['GET', 'POST'])
    def create_question():
        """
        Create a new question to be added to the database.
        Requires the following information in the request:
        - question (str).
        - answer (str).
        - category (int).
        - difficulty (int).
        Return the id of the created question for reference.
        Frontend request: submitQuestion() (FormView.js).

        Returns:
        * JSON object: {'success', 'created'}.
        """
        response_data = request.get_json()
        #Check if any of the required data is not in the request, or if it is technically present but not usable (i.e. length == 0).
        #If true, abort.
        if (('question' not in response_data)\
            or ('answer' not in response_data)\
            or ('category' not in response_data)\
            or ('difficulty' not in response_data))\
        or ((len(str(response_data['question'])) == 0)\
            or (len(str(response_data['answer'])) == 0)\
            or ((int(response_data['category']) < 0) or (int(response_data['category']) > 5))\
            or ((int(response_data['difficulty']) < 0) or (int(response_data['difficulty'] > 5)))):
            abort(400)
        try:
            #Create Question object (models.py) from request parameters and insert.    
            new_question = Question(question=response_data['question']
                                    ,answer=response_data['answer']
                                    ,category=response_data['category']
                                    ,difficulty=response_data['difficulty'])
            new_question.insert()
            #Get updated overall question metrics.
            questions = Question.query.all()
            questions_paginated = paginate_results(request, questions) 
            return jsonify({'success':True
                            ,'created':new_question.id
                            ,'questions':questions_paginated
                            ,'total_questions':len(questions)})
        except:
            abort(422)   
    

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['GET', 'POST'])
    def search_questions():
        """
        Searches database for questions that returns substring matches on a provided searchTerm (str).
        Results are paginated.
        Also determine:
        - Total questions returned.
        - Current category ('None' for this request).
        Frontend request: submitSearch() (QuestionView.js).

        Returns:
        * JSON object: {'success', 'questions', 'total_questions', 'current_category'}.
        """
        response_data = request.get_json()
        #Check if searchTerm is not in the request.
        #If true, abort.
        if ('searchTerm' not in response_data):
            abort(400)

        try:
            #Search questions based on presence of searchTerm.
            #Use ilike() method to make search case insensitive.
            returned_questions = Question.query.filter(Question.question.ilike('%{}%'.format(response_data['searchTerm']))).all()
            paginated_questions = paginate_results(request, returned_questions)
            return jsonify({'success':True
                            ,'questions':paginated_questions
                            ,'total_questions':len(returned_questions)
                            ,'current_category':None})
        except:
            abort(404)    
    

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """
        Return all available questions in database for the specified category, paginated into QUESTIONS_PER_PAGE groups.
        Also determine:
        - Total questions in database for category.
        - Current category (as per request parameter).
        Frontend request code: getByCategory() (QuestionView.js).
        
        Returns:
        * JSON object: {'success', 'questions', 'totalQuestions', 'currentCategory'}.
        """
        try:
            #Select all questions from the Question object (models.py), without modifying received order.    
            questions = Question.query.filter_by(category=str(category_id)).all() #Note: 'category' (index) field is stored as string in Question class.               
            questions_paginated = paginate_results(request, questions)
            return jsonify({'success':True
                            ,'questions':questions_paginated
                            ,'total_questions':len(questions)
                            ,'current_category':category_id})
        except:
            abort(404)
    
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['GET', 'POST'])
    def get_questions_for_quiz():
        """
        Return all available questions in database for the specified category, paginated into QUESTIONS_PER_PAGE groups.
        Also determine:
        - Total questions in database for category.
        - Current category (as per request parameter).
        Frontend request code: getNextQuestion() (QuizView.js).
        
        Returns:
        * JSON object: {'success', 'questions', 'totalQuestions', 'currentCategory'}.
        """
        try:
            response_data = request.get_json()
            #Get pre-existing trivia data to filter next question derived from database.
            if ('previous_questions' not in response_data) or ('quiz_category' not in response_data):
                abort(400)
            previous_questions = response_data['previous_questions']
            quiz_category = response_data['quiz_category'] #Note: 'category' is defined as a string in the 'Question' class (models.py).

            #Randomly select next question, handling received 'quiz_category' and 'previous_questions' values.
            #Note: quiz_category == 0 selects all categories.
            if quiz_category == 0:
                #All categories.
                available_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
                    #Note: notin_() is deprecated in later versions (https://stackoverflow.com/questions/26182027/how-to-use-not-in-clause-in-sqlalchemy-orm-query). 
            else:
                #Specific category.
                available_questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category==quiz_category).all()
            if len(available_questions) > 0:
                available_questions = [question.format() for question in available_questions] #Note: Format is a method of the Question class in models.py.
                new_question = random.choice(available_questions)
            else:
                new_question = None
            return jsonify({'success':True
                            ,'question':new_question})
        except:
            abort(404)
    
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    #Bad request.
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success':False, 'error':400, 'message':'Bad request - server unable to process.'}), 400
    
    #Resource not found.
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({'success':False, 'error':404, 'message':'Request valid but resource not found.'}), 404
    
    #Unprocessable content.
    @app.errorhandler(422)
    def unprocessable_content(error):
        return jsonify({'success':False, 'error':422, 'message':'Request could not be processed - content and syntax are valid but cannot process instructions.'}), 422
    #Note: Message is specifically trying to disambiguate from error 400.
    #The following resource was used to author the 422 error message: https://http.dev/422 
    
    #Internal server error.
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'success':False, 'error':500, 'message':'Internal server error - cannot handle request.'}), 500
    

    return app
