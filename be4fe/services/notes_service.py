from utils.db_utils import get_mongo_db
from utils.debug_logging import debug_log
import uuid
import re

def get_note_templates():
    try:
        db = get_mongo_db()
        response_collection = db['note_templates']
        query = {}
        debug_log(f'Querying note_templates with {query}')
        responses = list(response_collection.find(query))
        debug_log(f'Response count: {len(responses)}')
        return responses
    except Exception as e:
        print(e)
        return []
    

def create_note_templates(template):
    try:
        db = get_mongo_db()
        response_collection = db['note_templates']
        debug_log(f'Creating note_template {template}')
        template['_id'] = uuid.uuid4()
        result = response_collection.insert_one(template)
        debug_log(f'Created {result.inserted_id}')
        return result
    except Exception as e:
        print(e)
        return []
    

def create_note(note):
    db = get_mongo_db()
    template_collection = db['note_templates']
    note_collection = db['notes']
    template_query = {"_id":uuid.UUID(note['noteId'])}
    template = template_collection.find_one(template_query)
    debug_log(f'Creating note from template: {template}')
    resulting_note = {"templateId":uuid.UUID(note['noteId'])}

    for field in template['fields']:
        for key in field:
            compiled_regex = re.compile(field[key])
            match = compiled_regex.search(note['note'])
            if match:
                resulting_note[key] = match.group(1)
            else:
                resulting_note[key] = ""
    try:
        debug_log(f'Creating note {resulting_note}')
        resulting_note['_id'] = uuid.uuid4()
        result = note_collection.insert_one(resulting_note)
        debug_log(f'Created {result.inserted_id}')
        return {"_id":result.inserted_id}
    except Exception as e:
        print(e)
        return []