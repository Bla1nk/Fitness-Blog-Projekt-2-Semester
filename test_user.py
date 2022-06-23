import unittest

from click import password_option
from flask_login import UserMixin

from website import models
import website

class TestEmployee(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.User_1 = website.models.User()
        self.User_2 = website.models.User()

    def test_Passwort(self):
        print('test_Passwort')
        self.assertEqual(self.User_1, self.User_2)
        self.assertEqual(self.User_2, self.User_1)
        self.User_1.first = 'Michael'
        self.User_2.first = 'David'

        self.assertEqual('Utronik','Utronik')
        self.assertEqual('Michael','Michael')


if __name__ == '__main__':
    unittest.main()