import numpy as np
import pandas as pd
import collections
from strsimpy.jaro_winkler import JaroWinkler

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