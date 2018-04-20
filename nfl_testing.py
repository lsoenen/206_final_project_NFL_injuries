import unittest
from final_proj import *


class TestDataAccess(unittest.TestCase):
    def test_storage(self):
        # interactive_prompt()
        conn = sqlite3.connect('NFL.db')
        cur = conn.cursor()
        statement = 'SELECT Name FROM Injuries'
        cur.execute(statement)
        players = cur.execute(statement).fetchall()


        self.assertEqual(players[0][0], 'Kyle Wilber')
        self.assertEqual(players[6][0], 'Jeremiah Ratliff')
        self.assertEqual(players[40][0], 'James Harrison')
        self.assertEqual(players[78][0], 'Oniel Cousins')
        self.assertEqual(players[108][0], 'Prince Amukamara')


class TestDataStorage(unittest.TestCase):
    def test_storage(self):
        # interactive_prompt()
        conn = sqlite3.connect('NFL.db')
        cur = conn.cursor()
        statement = 'SELECT Name, Injury FROM Injuries'
        cur.execute(statement)
        players_1 = cur.execute(statement).fetchall()

        self.assertEqual(players_1[0][1], 'Thumb')
        self.assertEqual(players_1[10][1], 'Wrist')
        self.assertEqual(players_1[125][1], 'Calf')
        self.assertEqual(players_1[408][1], 'Ribs')
        self.assertEqual(players_1[563][1], 'Ankle')

class TestDataProcessing(unittest.TestCase):
    def test_injuries_by_year(self):
        # interactive_prompt()
        conn = sqlite3.connect('NFL.db')
        cur = conn.cursor()
        statement = 'SELECT Injury, Count(Injury), Year FROM Injuries WHERE Year <> 2009 Group By Injury Order By Count(injury) DESC'
        cur.execute(statement)

        injuries = cur.execute(statement).fetchall()

        self.assertEqual(injuries[0][0], 'Knee')
        self.assertEqual(injuries[0][1], 955)
        self.assertEqual(injuries[39][0], 'Oblique')
        self.assertEqual(injuries[39][1], 6)
        self.assertEqual(injuries[61][0], 'Facial Lacerations')
        self.assertEqual(injuries[61][1], 1)



unittest.main()
