import unittest
from website.models import User


class TestEmployee(unittest.TestCase):

    def setUp(self):
        print('setUp')
        self.User_1 = User()
        self.User_2 = User()

    def test_Passwort(self):
        print('test_Passwort')
        self.assertEqual(self.User_1, self.User_2)
        self.assertEqual(self.User_2, self.User_1)

        self.User_1.first = 'Michael'
        self.User_2.first = 'David'

        self.assertEqual(self.User_1.first, self.User_1.first)
        self.assertEqual(self.User_2.first, self.User_2.first)
        self.assertEqual(self.User_1.first, self.User_2.first) #Fail Beispiel


if __name__ == '__main__':
    unittest.main()