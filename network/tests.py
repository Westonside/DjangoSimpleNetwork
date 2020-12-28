from django.test import TestCase, Client
import unittest

from selenium import webdriver
import os
import pathlib
import unittest


def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri() 




class networkTesting(TestCase):
    
    #ensure that the index function returns correctly
    def testIndex(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
    
    # def createEmail(self):
    #     c= Client()
    #     driver = webdriver.Chrome()
    #     driver.get('http://127.0.0.1:8000/')
    #     self.assertEqual(driver.find_element_by_id('1').value,1)
    def test_bad_postget_request(self):
        c=Client()
        response=c.get('/post/1')
        self.assertEqual(response.status_code,405)
    
    def getFollowed_posts(self):
        c = Client()
        response = c.get('/getPosts/following')
        self.assertEqual(response.streaming, "test")
    

# Create your tests here.
