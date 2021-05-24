#  all json file export logic goes here

# json format example
# {
#     "getSauce": {
#         "username": "actual username", 
#         "Date of Export": "date of exprt",
#         "results": [
#             {"title": "actual title goes here", "date": "actual date goes here"},
#             {"title": "actual title goes here", "date": "actual date goes here"}
#         ]
#     }
# }

import json
from datetime import datetime
from getSauce import db
from models import *

def exportData(username):
    """
    Export Search history of User to Json File

    username : username of the user whos search history has to be exported
    """

    
    # sql = "SELECT resulttitle, date FROM results WHERE username = " + username
    raw_results = results.query.filter_by(username= username).with_entities(results.resulttitle, results.date).all()

    actual_results = []

    if raw_results is None:
        return False
    
    for i in raw_results:
        dictrow = {"title": i.resulttitle, "time of search": i.date.isoformat()}
        actual_results.append(dictrow)

    # print(actual_results)
    jsonfile = open('./ExportedJson/Exportedjson.json', 'w+')  # create the json file

    data = json.dump(
        {
            "getSauce": {
                "username": username,
                "Exported on Date": datetime.now().isoformat(),
                "results": actual_results
            }
        },jsonfile, indent= 4
    )
    file = data

    # jsonfile.write(file)
    jsonfile.close()


# exportData('5tupidmuffin')
