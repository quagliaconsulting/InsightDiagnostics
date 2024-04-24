from utils.db_utils import get_mongo_db
from utils.debug_logging import debug_log

def search_for_responses(search_term):
    try:
        db = get_mongo_db()
        response_collection = db['questionnaire_response']
        query = {
            '$or': [{
                "patientExternalId": search_term
            },
            {
                "patientName": search_term
            }]
        }
        debug_log(f'Querying questionnaire_response with {query}')
        responses = list(response_collection.find(query))
        debug_log(f'Response count: {len(responses)}')
        return responses
    except Exception as e:
        print(e)
        return []