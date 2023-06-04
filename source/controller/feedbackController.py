from flask_restful import Resource
from service.TransformData import get_seminar_feedbacks

class FeedbackController(Resource):
    def get(self, seminarId):
        results = get_seminar_feedbacks(seminarId=seminarId)
        return results