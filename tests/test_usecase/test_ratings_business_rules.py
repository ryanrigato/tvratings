from unittest.mock import patch
import unittest


class TestRatingsBusinessRules(unittest.TestCase):
    def test_select_highest_ratings(self):
        """Highest TelevisionRating element returned"""
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.usecase.ratings_business_rules import select_highest_ratings
        mock_tv_ratings = get_mock_television_ratings(
            10
        )


        for max_rating_element in range(10):
            with self.subTest(max_rating_element=max_rating_element):

                mock_tv_ratings[max_rating_element].rating = max({
                    mock_tv_rating.rating 
                    for mock_tv_rating in mock_tv_ratings
                }) + 1


                highest_rating = select_highest_ratings(mock_tv_ratings)


                self.assertEqual(
                    highest_rating, 
                    mock_tv_ratings[max_rating_element],
                    msg=f"""\n
                    element {max_rating_element} does not possess the
                    highest rating attribute
                    of the list of mock_tv_ratings
                    """
                )


    def test_select_lowest_ratings(self):
        """lowest TelevisionRating element returned"""
        from fixtures.ratings_fixtures import get_mock_television_ratings
        from tvratings.usecase.ratings_business_rules import select_lowest_ratings
        mock_tv_ratings = get_mock_television_ratings(
            10
        )


        for min_rating_element in range(10):
            with self.subTest(min_rating_element=min_rating_element):

                mock_tv_ratings[min_rating_element].rating = min({
                    mock_tv_rating.rating 
                    for mock_tv_rating in mock_tv_ratings
                }) - 1

                
                lowest_rating = select_lowest_ratings(mock_tv_ratings)


                self.assertEqual(
                    lowest_rating, 
                    mock_tv_ratings[min_rating_element],
                    msg=f"""\n
                    element {min_rating_element} does not possess the
                    lowest rating attribute
                    of the list of mock_tv_ratings
                    """
                )



    def test_rating_data_quality(self):
        """Business rules for minimum and maximum possible ratings"""
        pass