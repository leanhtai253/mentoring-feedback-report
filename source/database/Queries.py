
class Queries:
    def __init__(self, connector):
        self.connector = connector

    def getSeminarFeedback(self, seminarId):
        query = f"Select content from seminar_feedbacks where seminar_id = {seminarId}"
        cursor = self.connector.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data