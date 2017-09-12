from base_test import TestCase

class SampleTest(TestCase):
    
    def test_assert(self):
        assert True
        
    def test_home(self):
        response = self.app.get("/")
        self.assertEquals(response.status_code, 200)