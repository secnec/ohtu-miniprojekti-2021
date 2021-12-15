import unittest
import tips_app.search as search

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.tip_list = [
            ("sahara", "https://en.wikipedia.org/wiki/Sahara"),
            ("atlantis", "https://en.wikipedia.org/wiki/Atlantis"),
            ("Barnacle", "https://en.wikipedia.org/wiki/Barnacle"),
            ("Great Potoo", "https://en.wikipedia.org/wiki/Great_potoo")
        ]

    def test_get_all_titles_returns_all_titles(self):
        expected_title_list = [
            "sahara",
            "atlantis",
            "Barnacle",
            "Great Potoo"
        ]
        true_title_list = search.get_all_titles(self.tip_list)

        self.assertEqual(expected_title_list, true_title_list)
    
    def test_search_close_matches_finds_cases_which_include_the_search_term(self):
        expected_result = "Great Potoo"
        search_term = "Great P"
        true_result = search.search_close_matches(self.tip_list, search_term)[0]

        self.assertEqual(expected_result, true_result)
    
    def test_search_close_matches_finds_cases_with_case_insensitivty(self):
        expected_result = "sahara"
        search_term = "SAHARR"
        true_result = search.search_close_matches(self.tip_list, search_term)[0]

        self.assertEqual(expected_result, true_result)
    
    def test_tip_dictionary_returns_correct_dict(self):
        expected_dict = {
            "sahara": "sahara",
            "atlantis": "atlantis",
            "barnacle": "Barnacle",
            "great potoo": "Great Potoo"
        }

        true_dict = search.tip_dictionary(self.tip_list)

        self.assertEqual(expected_dict, true_dict)
