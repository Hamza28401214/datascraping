import unittest
import  sqlite3

class TestReadFromDb(unittest.TestCase):
    def test1(self):
        #at least 10 records are stored in the db
        con = sqlite3.connect('database//scraping_data.db')
        cur = con.cursor()
        querry = "SELECT * from data LIMIT 10"
        v = cur.execute(querry).fetchall()
        self.assertEqual(len(v), 10)


#python -m unittest     tests.tests.TestReadFromDb
if __name__ == '__main__':
    TestReadFromDb