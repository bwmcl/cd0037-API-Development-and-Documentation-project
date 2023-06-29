import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    #get_categories().
    def test__get_categories__pass(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories'])) #Note: Will fail if length of 'categories' == 0.
        
    #Cannot think of a relevant test case in this scenario,
    #other than to delete the entire 'categories' table from the database which will impede further testing.
    #Any errors thrown by this method should also be captured in other tests.
        
        
    #get_questions().
    def test__get_questions__pass(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions'])) #Note: Will fail if length of 'questions' == 0.
        self.assertTrue(len(data['categories'])) #Note: Will fail if length of 'categories' == 0.
        self.assertEqual(data['current_category'], None)
        
    def test__get_questions__fail_422_page_outside_range(self):
        """
        Request a page that is known to be in excess of what can be returned in paginated results.
        """
        response = self.client().get('/questions?page=100000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request could not be processed - content and syntax are valid but cannot process instructions.')
        self.assertEqual(data['error'], 422)
        
    
    #delete_question().
    def test__delete_question__pass(self):
        #Compare total questions before and after question addition as an assert statement.
        total_questions_pre = len(Question.query.all())
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        #Double-verify by checking for the question in the database.
        question = Question.query.filter_by(id=5).one_or_none()
        self.assertEqual(question, None)
        #Triple-verify by comparing total table rows before and after procedure.
        self.assertEqual((total_questions_pre-1), len(Question.query.all()))
        
    def test__delete_question__fail_404_question_outside_range(self):
        """
        Request to delete question that is known to be outside of database range.
        """
        response = self.client().delete('/questions/100000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request could not be processed - content and syntax are valid but cannot process instructions.')
        self.assertEqual(data['error'], 422)
        
    
    #create_question().
    def test__create_question__pass(self):
        new_question = {'question':'What does DNA stand for?'
                        ,'answer':'DeoxyriboNucleic Acid'
                        ,'category':1
                        ,'difficulty':4}
        #Compare total questions before and after question addition as an assert statement.
        total_questions_pre = len(Question.query.all())
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        #Double-verify by comparing total table rows before and after procedure.
        self.assertEqual((total_questions_pre+1), len(Question.query.all()))
        
    def test__create_question__fail_400_request_data_missing(self):
        """
        Omit 'answer' key from 'new_question' dictionary.
        """
        new_question = {'question':'What does DNA stand for?'
                        ,'category':1
                        ,'difficulty':4}
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request - server unable to process.')
        self.assertEqual(data['error'], 400)
        
    
    #search_questions().
    def test__search_questions__pass(self):
        search_data = {'searchTerm':'title'}
        response = self.client().post('/questions/search', json=search_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']) #Note: searchTerm='title' is known to produce non-zero search results.
        self.assertEqual(data['current_category'], None)
        
    def test__search_questions__fail_400_omit_searchTerm(self):
        """
        Omit 'searchTerm' from submitted JSON object.
        """
        search_data = {}
        response = self.client().post('/questions/search', json=search_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request - server unable to process.')
        self.assertEqual(data['error'], 400)
        
        
    #get_questions_by_category().
    def test__get_questions_by_category__pass(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions'])) #Note: Will fail if length of 'questions' == 0.
        self.assertEqual(data['current_category'], 1)
        
    def test__get_questions_by_category__fail_404_category_not_valid(self):
        """
        Request a category id that is not an integer value.
        """
        response = self.client().get('/categories/abcde/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request valid but resource not found.')
        self.assertEqual(data['error'], 404)
        
        
    #get_questions_for_quiz().
    def test__get_questions_for_quiz__pass(self):
        json_data = {'previous_questions':[2, 4]
                     ,'quiz_category':5}
        response = self.client().post('/quizzes', json=json_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test__get_questions_for_quiz__fail_404_quiz_category_invalid(self):
        """
        Generate request with non-sensical 'quiz_category' value in JSON.
        """
        json_data = {'previous_questions':[2, 4]
                     ,'quiz_category':'abcde'}
        response = self.client().post('/quizzes', json=json_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request valid but resource not found.') 
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()