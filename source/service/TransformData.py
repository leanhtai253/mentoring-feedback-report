from database.Connector import DatabaseConnector
from database.Queries import Queries
import json
import pandas as pd

mydb = DatabaseConnector(
    database='growthme', 
    user='postgres', 
    password='capstoneproject2023', 
    host='35.192.185.10', port=None
)

def fetch_seminar_feedbacks(seminarId):
    conn = mydb.connect()
    myqr = Queries(conn)
    data = myqr.getSeminarFeedback(seminarId=seminarId)
    conn.close()
    return data

def get_seminar_feedbacks(seminarId):
    data = fetch_seminar_feedbacks(seminarId=seminarId)
    if len(data) < 1:
        return None
    feedbacks_arr = []
    for d in data:
        feedbacks_arr += (json.loads(d[0]['results']))
    feedbacks_df = pd.DataFrame.from_records(feedbacks_arr)
    TYPE_ANSWERS = {
    'RATING': range(1,6),
    'YES/NO': ['Yes', 'No']
    }
    final_df = pd.DataFrame(columns=['id','type','answer','count'])
    question_ids = feedbacks_df.id.unique()
    for id in question_ids:
        row_df = feedbacks_df[feedbacks_df['id'] == id].groupby(['id', 'type', 'answer']).count()[['question']].reset_index().rename(columns={'question':'count'})
        got_answers = list(row_df['answer'].unique())
        got_type = row_df['type'].unique()[0]
        if got_type in TYPE_ANSWERS:
            missing_rows_arr = []
            for ans in TYPE_ANSWERS[got_type]:
                if ans not in got_answers:
                    missing_row_dict = {}
                    missing_row_dict['id'] = id
                    missing_row_dict['type'] = got_type
                    missing_row_dict['answer'] = ans
                    missing_row_dict['count'] = 0
                    missing_rows_arr.append(missing_row_dict)
            final_df = pd.concat([final_df, pd.concat([row_df,pd.DataFrame.from_records(missing_rows_arr)])])

    questions_df = feedbacks_df[['id','question', 'type']].value_counts().to_frame().reset_index()[['id','question', 'type']].set_index('id')
    response_json = []
    final_question_ids = final_df.id.unique()
    for id in final_question_ids:
        question_dict = {}
        question_dict['id'] = id
        question_dict['question'] = questions_df.loc[id].question
        question_dict['type'] = questions_df.loc[id].type
        question_dict['statistics'] = {}
        for item in final_df[final_df['id'] == id].sort_values('answer').values:
            question_dict['statistics'][item[-2]] = item[-1]
        response_json.append(question_dict)
    return response_json