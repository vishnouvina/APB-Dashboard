def read_and_load_annotation(filename):
    tweet = open(
        "/Users/evan/Documents/datavisualization_coding_weeks/datavisualization/Data/tweets/"+filename, 'r')
    lignes = tweet.readlines()
    text_tweet = []
    for ligne in lignes:
        text_tweet.append(ligne.split())
    print(text_tweet)
    dico = {'topic': [], 'negative_keywords': [], 'positive_keywords': []}
    for ligne in text_tweet:
        if 'Topic' in ligne:
            topic = ''
            for j in range(4, len(ligne)):
                topic = topic + ligne[j]
            ident = ligne[0]
            for ligne2 in text_tweet:
                if ('Arg1' + ident in ligne2 or 'Arg2' + ident in ligne2) and 'isNegativeOpinion' in ligne2:
                    opinion = 'negative'
                    dico['topic'].append({'name': topic, 'opinion': opinion})
                elif ('Arg1' + ident in ligne2 or 'Arg2' + ident in ligne2) and 'isPositiveOpinion' in ligne2:
                    opinion = 'positive'
                    dico['topic'].append({'name': topic, 'opinion': opinion})
    for ligne in text_tweet:
        if 'Subjectiveme_positive' in ligne:
            identifiant = ligne[0]
            pos_keyword = ''
            for j in range(4, len(ligne)):
                pos_keyword = pos_keyword + ligne[j]
            for ligne2 in text_tweet:
                if ('Arg1' + identifiant in ligne2 or 'Arg2' + identifiant in ligne2) and 'Negates' in ligne2:
                    neg_keyword = 'pas' + pos_keyword
                    dico['negative_keywords'].append(neg_keyword)
            dico['positive_keywords'].append(pos_keyword)
        if 'Subjectiveme_negative' in ligne:
            neg_keyword = ''
            for j in range(4, len(ligne)):
                neg_keyword = neg_keyword + ligne[j]
            dico['negative_keywords'].append(neg_keyword)
    print(dico)


read_and_load_annotation("143048389142134785.ann")
