from tvratings.entry.input_valdiators import validate_iso_8601_date 
from tvratings.entry.request_objects import ValidRequest 
from tvratings.entry.request_objects import InvalidRequest 
from tvratings.entry.response_objects import ResponseFailure 
from tvratings.entry.response_objects import ResponseSuccess 
from tvratings.repo.tvratings_backend import load_one_date 

import logging

def get_valid_date(tvratings_day):
    """Request object for invoking an interface that requires a datetime.date input

        Parameters
        ----------
        tvratings_day: str
            ISO 8601 YYYY-MM-DD format

        Returns
        -------
        valid_date_request: ValidRequest or InvalidRequest
            ValidRequest with request_filters
            {
                ratings_date: datetime.date
            }
            or InvalidRequest
    """
    logging.info("get_valid_date - beginning input validation")
    valid_date, date_parse_error = validate_iso_8601_date(iso_formatted_str=tvratings_day)
    
    if date_parse_error is not None:
        logging.info("get_valid_date - InvalidRequest returned")
        return(InvalidRequest(error_message=date_parse_error))

    logging.info("get_valid_date - ValidRequest returned")
    
    return(ValidRequest(request_filters={"ratings_date": valid_date}))


def get_one_night_ratings(valid_date_request):
    """Gets TelevisionRating entities for one night

        Parameters
        ----------
        valid_date_request: tvratings.entry.externals_entry.get_valid_date output

        Returns
        -------
        tvratings_response: ResponseSuccess or ResponseFailure
            ResponseSuccess.response_value list of TelevisionRating entities 
            [] if no TelevisionRating entites match ratings_date provided in the request_filter 
    """
    logging.info("get_one_night_ratings - new television request")
    television_ratings, load_one_date_error = load_one_date(
        ratings_occurred_on=valid_date_request.request_filters["ratings_date"]
    )
    
    if load_one_date_error is not None:
        logging.info("get_one_night_ratings - load_one_date_error")
        return(ResponseFailure(error_message=load_one_date_error))

    logging.info("get_one_night_ratings - ValidRequest returned")
    
    return(ValidRequest(request_filters={"ratings_date": valid_date}))
    