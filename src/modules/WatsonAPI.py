def callWatsonAPI(inputFilePath, outputFilePath):
    from watson_developer_cloud import PersonalityInsightsV3
    import webbrowser
    import os
    from os.path import join, dirname,abspath
    import json
    import sys

    personality_insights = PersonalityInsightsV3(
        username='d0ae6a0f-4da7-45bc-b305-ae38f9932dd6',
        password='oHBhyGabr12x',url='https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13')

    f = open(outputFilePath,'w+')
    with open(inputFilePath,'r') as personality_text:
        json.dump(personality_insights.profile(text=personality_text.read()), f)
    f.close()