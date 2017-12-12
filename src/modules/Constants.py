Openness = ['Adventurousness','Artistic interests','Emotionality','Imagination','Intellect','Authority-challenging']
Conscientiousness = ['Achievement striving','Cautiousness','Dutifulness','Orderliness','Self-discipline','Self-efficacy']
Extraversion = ['Activity level','Assertiveness','Cheerfulness','Excitement-seeking','Outgoing','Gregariousness']
Agreeableness = ['Altruism','Cooperation','Modesty','Uncompromising','Sympathy','Trust']
EmotionalRange = ['Fiery','Prone to worry','Melancholy','Immoderation','Self-consciousness','Susceptible to stress']

OpAttri = Openness#[ Openness[0] , Openness[2] , Openness[3]]
ConAttri = Conscientiousness#[ Conscientiousness[0] , Conscientiousness[1] , Conscientiousness[2]]
ExtraAttri = Extraversion#[ Extraversion[0] , Extraversion[1] , Extraversion[2]]
AgreeAttri = Agreeableness#[ Agreeableness[1] , Agreeableness[2] , Agreeableness[4]]
EmoAttri = EmotionalRange#[ EmotionalRange[2] , EmotionalRange[4] , EmotionalRange[5]] 

personality_traits = ["Openness","Conscientiousness","Extraversion","Agreeableness","Emotional range"]

combinedTraits = [OpAttri,ConAttri,ExtraAttri,AgreeAttri,EmoAttri]

recordLimit = 10

CriticalCount = 3

SelectedAttributes = ['Cautiousness','Melancholy','Self-consciousness','Susceptible to stress','Prone to worry','Authority-challenging','Immoderation','Sympathy','Trust','Cheerfulness']

Constraints = { 'Authority-challenging' : [92.00,100.00],
                'Cautiousness' : [93.00,99.00],
                'Sympathy' : [0.00,0.15],
                'Trust' : [0.00,0.15],
                'Prone to worry' : [85.00,100.00],
                'Melancholy' : [88.00,100.00],
                'Immoderation' : [80.00,100.00],
                'Self-consciousness' : [75.00,100.00],
                'Susceptible to stress' : [80.00,100.00],
                'Cheerfulness' : [0.00,20.00]}