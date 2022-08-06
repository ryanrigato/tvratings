from tvratings.entities.entity_model import TelevisionRating

import logging


def select_highest_ratings(tv_ratings_list: 
    list[TelevisionRating]) -> TelevisionRating:
    """Returns highest TelevisionRating in tv_rating_list
    Assumes tv_ratings_list is populated
    """
    highest_rating: int = max([
        tv_rating.rating for tv_rating in tv_ratings_list
        if tv_rating.rating is not None
    ])

    for tv_rating in tv_ratings_list:
        if tv_rating.rating == highest_rating:
            return(tv_rating)
    

