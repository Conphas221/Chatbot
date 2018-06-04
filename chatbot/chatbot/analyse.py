from dandelion import DataTXT

def AnalyseText(text):
    datatxt = DataTXT(app_id='cd32413268454e19a31776d33b5f0ba0', app_key='cd32413268454e19a31776d33b5f0ba0')
    response = datatxt.nex(text)

    return response.annotations
