

def func():
    import webbrowser
    import os
    from os.path import join, dirname,abspath
    import json
    import sys
    
    from watson_developer_cloud import PersonalityInsightsV2
    personality_insights = PersonalityInsightsV2(
    username='e6b4ab4c-c4b3-4130-a89e-3aa18f1a791a',
    password='8SLrsgF6MaSy',url='https://gateway.watsonplatform.net/personality-insights/api')
   

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
    f.close();
    
    #get tweets for username passed at command line
   
