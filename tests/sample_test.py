from base_test import TestCase
from flask import url_for

class SampleTest(TestCase):
    
    def test_assert(self):
        assert True
        
    def test_home(self):
        response = self.app.get("/")
        self.assertEquals(response.status_code, 200)
        
    def test_form(self):
        response = self.app.post('/test_form', data={'var1': "variable"})
        
        self.assertIn('The parameters was: variable' ,response.data)