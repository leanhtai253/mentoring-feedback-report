from flask import Flask
from flask_restful import Resource, Api
from controller.homeController import HomeController
from controller.feedbackController import FeedbackController
app = Flask(__name__)
api = Api(app)

api.add_resource(HomeController, '/')
api.add_resource(FeedbackController, '/seminar/<int:seminarId>')
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)