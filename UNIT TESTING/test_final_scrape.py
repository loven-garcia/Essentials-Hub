import unittest
from final_scrape import check_connection_wiki, day_by_day, day_by_day_cases_test ,api_connection, pui_pum_tested_connection_test, api_length_of_stats,  for_total_deaths_total_recovered_test, by_age_test, by_region_test, by_sex_test, date_test, pui_pum_tested_test


class Test_Connection(unittest.TestCase):

    def test_connection_wikipedia(self):
        connection = check_connection_wiki()
        self.assertEqual(connection.status_code, 200)


    def test_day_by_day(self):
        bool = day_by_day()
        self.assertTrue(bool)


    def test_day_by_day_cases_content(self):
        content = day_by_day_cases_test()
        self.assertIsNotNone(content)


    def test_by_age_content(self):
        content = by_age_test()
        self.assertIsNotNone(content)


    def test_by_region_content(self):
        content = by_region_test()
        self.assertIsNotNone(content)


    def test_by_sex_content(self):
        content = by_sex_test()
        self.assertIsNotNone(content)


    def test_day_worldometer(self):
        content = day_by_day_cases_test()
        connection = for_total_deaths_total_recovered_test()
        self.assertEqual(connection.status_code, 200)


    def test_date_content(self):
        content = date_test()
        self.assertIsNotNone(content)


    def test_connection_endcov_tracker(self):
        connection = pui_pum_tested_connection_test()
        self.assertEqual(connection.status_code, 200)


    def test_pui_pum_content(self):
        content = pui_pum_tested_test()
        self.assertIsNotNone(content)


    def test_connection_heroku_api(self):
        connection = api_connection()
        self.assertEqual(connection.status_code, 200)


    def test_length_data_heroku(self):
        length = api_length_of_stats()
        self.assertEqual(length, 10)


if __name__ == '__main__':
    unittest.main()