import requests
import json


class QuestionnaireService:

    def __init__(self,host) -> None:
        self._host = host

    def get_grouped_questions(self,questionnaire_id,version):
        url = f"{self._host}/v1/questionnaire/{questionnaire_id}/{version}"
        questionnaire_response = requests.get(url)
        questionnaire = questionnaire_response.json()
        grouped_questions_response = {}
        for q in questionnaire['questions']:
            for group in q['groups']:
                if group not in grouped_questions_response.keys():
                    grouped_questions_response[group] = []
                grouped_questions_response[group].append(q)
        print(f'Grouped question response {grouped_questions_response}')
        return grouped_questions_response

    def submit_response(self,grouped_question_responses,mrn,questionnaire_id,version_id):
        response = {
            "responses":grouped_question_responses,
            "questionnaireVersionedId": {
                '_id':questionnaire_id,
                'versioin':version_id
            },
            "organizationId":"",
            "createdBy":mrn
        }
        bodyStr = json.dumps(response)
        try:
            post_response = requests.post(f'{self._host}/v1/questionnaire/{questionnaire_id}/{version_id}/responses/',data=bodyStr,headers={'Content-Type':'application/json'})
        except requests.RequestException as e:
            print(f'there was an error trying to post data {e}')
            raise e

        if post_response.status_code != 201:
            raise Exception(f"Could not submit questionnaire response - {post_response.status_code} {post_response.content}")
            