import numpy as np
import pandas as pd
import collections
import csv
from strsimpy.jaro_winkler import JaroWinkler
from tmp_match.load import save
Output = collections.namedtuple('Output', ['prediction', 'confidence'])

def matching(dataset, input):
    #Enroll templates to list
    df = pd.read_csv(dataset)
    templates = df['templates'].values.tolist()

    #Input word
    input = str(input)

    #Iterate all templates and calculate text similarity
    jarowinkler = JaroWinkler()
    result=[jarowinkler.similarity(input.lower(), template.lower()) for template in templates]

    #Return the highest similarity
    prediction = templates[np.argmax(result)]
    confidence = result[np.argmax(result)]
    output = Output(prediction, confidence)
    
    return output

class Matching(object):
    def __init__(self, df):
        # self.df = pd.read_csv(dataset)
        self.templates = df["templates"].values.tolist()
        self.algo = JaroWinkler()
    
    def match(self, s:str, thresh=0.8):
        result  = [self.algo.similarity(s.lower(), template.lower()) for template in self.templates]

        high = np.argmax(result)
        if result[high] >= thresh:
            return self.templates[high]
        else:
            self.templates.append(s)
            return s
    
    def extend(self):
        df_update = pd.DataFrame(data=self.templates, columns=['templates'])
        save(df_update, 'dataset/processed/ocr-struk/template-matching/template_indomaret.csv')
