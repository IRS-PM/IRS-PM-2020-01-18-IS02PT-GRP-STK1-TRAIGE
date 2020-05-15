
from joblib import dump, load
import pandas as pd 
import pickle
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def check(featuresFilePath,modelFilePath,dataFilePath):
	# featuresFilePath='data/feature8.pkl'
	df888 = pd.read_csv(dataFilePath,sep=',')
	# modelFilePath = 'data/huatmodel.joblib'
	loaded_model = load(modelFilePath)
	vectorizer = pickle.load(open(featuresFilePath, "rb"))
	features_loaded_vec = vectorizer.transform(df888)
	prediction =loaded_model.predict(features_loaded_vec)
	print(prediction)
	return prediction[0]


# =============================================================================
#

# 
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.naive_bayes import MultinomialNB
# 
# count_vect = CountVectorizer()
# X_data_counts = count_vect.fit_transform(df)
# tfidf_transformer = TfidfTransformer()
# X_data = tfidf_transformer.fit_transform(X_data_counts)
# prediction = loaded_model.predict(X_data)
# print(prediction)
# # 
# =============================================================================
# 
# 
# 
# # =============================================================================
# # from sklearn.model_selection import train_test_split
# # from sklearn.feature_extraction.text import CountVectorizer
# # from sklearn.feature_extraction.text import TfidfTransformer
# # 
# # count_vect = CountVectorizer()
# # 
# # count_vect.transform(
# #                 ["Crust is not good."
# #                  ]))
# # 
# # X_train_counts = count_vect.fit_transform(X_train)
# # tfidf_transformer = TfidfTransformer()
# # X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# # =============================================================================
# 
# 
# pipe.predict(pr[pred_cols])
# 
# result = loaded_model.score(X_test, Y_test)\
# 
# 
# print(result)
# =============================================================================

    
# dump(model, 'filename.joblib') 