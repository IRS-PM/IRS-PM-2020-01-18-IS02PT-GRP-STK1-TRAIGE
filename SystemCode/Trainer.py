import pandas as pd
import pickle
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from joblib import dump, load
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

def stratify(df):
    
    import math
    
    class0_df= df.loc[df['priority'] == 0]
    class1_df= df.loc[df['priority'] == 1]
    class2_df= df.loc[df['priority'] == 2]
    
    countArr=[]
    countArr.append(len(class0_df.index))
    countArr.append(len(class1_df.index))
    countArr.append(len(class2_df.index))
    minCount = math.floor(0.9*min(countArr))
    
    class0_df=class0_df.sample(minCount)
    class1_df=class1_df.sample(minCount)
    class2_df=class2_df.sample(minCount)
    
    frames = [class0_df, class1_df ,class2_df]
    df = pd.concat(frames)

    return df    
    

def train(inputFilePath,outputClassifierFilePath,outputVectorFilePath):
    
	df = pd.read_csv(inputFilePath,sep=',')
	df = stratify(df)
	tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
	features = tfidf.fit_transform(df.sentence).toarray()

	pickle.dump(tfidf,open(outputVectorFilePath,"wb"))
	labels = df.priority
	X_train, X_test, y_train, y_test = train_test_split(df['sentence'], df['priority'], random_state = 0)
	model = LinearSVC()
	X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
	model.fit(X_train, y_train)
	dump(model, outputClassifierFilePath) 
	y_pred = model.predict(X_test)
	print(y_pred)

	conf_mat = confusion_matrix(y_test, y_pred)

	target_names = ['0', '1', '2']
	report=classification_report(y_test, y_pred, target_names=target_names,output_dict=True)
	subdata = {}
	subdata['conf_mat']=conf_mat.tolist() 
	subdata['class_report']=report
	return subdata





