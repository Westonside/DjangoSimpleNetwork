import unittest
from selenium import webdriver
import os
import pathlib
import unittest


def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri() 


driver = webdriver.Chrome()