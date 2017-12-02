Openness = ['Adventurousness','Artistic interests','Emotionality','Imagination','Intellect','Authority-challenging']
Conscientiousness = ['Achievement striving','Cautiousness','Dutifulness','Orderliness','Self-discipline','Self-efficacy']
Extraversion = ['Activity level','Assertiveness','Cheerfulness','Excitement-seeking','Outgoing','Gregariousness']
Agreeableness = ['Altruism','Cooperation','Modesty','Uncompromising','Sympathy','Trust']
EmotionalRange = ['Fiery','Prone to worry','Melancholy','Immoderation','Self-consciousness','Susceptible to stress']

OpAttri = [ Openness[0] , Openness[2] , Openness[3]]
ConAttri = [ Conscientiousness[0] , Conscientiousness[1] , Conscientiousness[2]]
ExtraAttri = [ Extraversion[0] , Extraversion[1] , Extraversion[3]]
AgreeAttri = [ Agreeableness[1] , Agreeableness[2] , Agreeableness[4]]
EmoAttri = [ EmotionalRange[2] , EmotionalRange[4] , EmotionalRange[5]] 

personality_traits = ["Openness","Conscientiousness","Extraversion","Agreeableness","Emotional range"]

combinedTraits = [OpAttri,ConAttri,ExtraAttri,AgreeAttri,EmoAttri]