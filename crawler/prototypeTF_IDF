# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0)
corpus = ["ಇಂಗ್ಲೀಶ್ ಕನ್ನಡ ನಿಘಂಟು, "jamam"]
tfidf_matrix =  tf.fit_transform(corpus)
feature_names = tf.get_feature_names()
print len(feature_names)
print feature_names
dense = tfidf_matrix.todense()
print len(dense[0].tolist()[0])
episode = dense[0].tolist()[0]
phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
print len(phrase_scores)
print sorted(phrase_scores, key=lambda t: t[1] * -1)[:5]

sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:20]:
   print('{0: <20} {1}'.format(phrase.encode('utf8'), score))
