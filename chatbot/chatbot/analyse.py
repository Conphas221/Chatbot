from dandelion import DataTXT

def AnalyseText(text):
    datatxt = DataTXT(app_id='cd32413268454e19a31776d33b5f0ba0', app_key='cd32413268454e19a31776d33b5f0ba0')

    response = datatxt.nex(text)
    

    return response.annotations

def post():
    POST https://api.dandelion.eu/datatxt/cl/models/v1()

{
    "description": "project78model",
    "lang": "en",
    "categories": [
        {
        "name": "C#",
        "topics":{
            "c#": 2.0,
            "https://nl.wikipedia.org/wiki/C%E2%99%AF": 1.0,
            "https://docs.microsoft.com/en-us/dotnet/csharp/": 1.0
            }
        },
        {
            "name": "java",
            "topics":{
                "https://nl.wikipedia.org/wiki/Java_(programmeertaal)": 1.0,
                "java": 2.0}
            }
        ]
    }
