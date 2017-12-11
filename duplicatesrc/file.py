

def func():
    import webbrowser
    import os
    from os.path import join, dirname,abspath
    import json
    import sys
    
    from watson_developer_cloud import PersonalityInsightsV3

    personality_insights = PersonalityInsightsV3(
    username='d0ae6a0f-4da7-45bc-b305-ae38f9932dd6',
    password='oHBhyGabr12x',url='https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13')
   

    filepath=join('../output','json_output.json')
    #chartpath=join('./sunburst-chart-master/examples','example_v2.html')
    #print(filepath)
    f=open(filepath,'w+')
    with open(join(dirname(__file__), '../textinput/kalam.txt')) as \
    personality_text:
     json.dump(personality_insights.profile(text=personality_text.read()), f)
    #driver = webdriver.Chrome() #I actually used the chromedriver and did not test firefox, but it should work.
    #firefox_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
    #ebbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    #webbrowser.get('firefox').open_new_tab(chartpath)
    #summary=soup.find('section', { "id" : "experience" })
    #print(summary.getText().encode('utf-8'))
    f.close()
    print("here")    
    #get tweets for username passed at command line
   
func()
