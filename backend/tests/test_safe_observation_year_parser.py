import unittest
from backend.core.research_constraints import parse_safe_observation_year

class TestSafeObservationYearParser(unittest.TestCase):
    def test_valid_year_string(self):
        self.assertEqual(parse_safe_observation_year("2011"), 2011)
        self.assertEqual(parse_safe_observation_year("2017"), 2017)
        self.assertEqual(parse_safe_observation_year("2002"), 2002)

    def test_active_and_non_year_values_return_none(self):
        self.assertIsNone(parse_safe_observation_year("Active"))
        self.assertIsNone(parse_safe_observation_year("Active | 2005"))
        self.assertIsNone(parse_safe_observation_year("2009\nActive\nPersistent"))
        self.assertIsNone(parse_safe_observation_year("1/9/2015"))
        self.assertIsNone(parse_safe_observation_year("Active | In 'morainic' deposit"))
        self.assertIsNone(parse_safe_observation_year(""))
        self.assertIsNone(parse_safe_observation_year(None))

if __name__ == "__main__":
    unittest.main()
