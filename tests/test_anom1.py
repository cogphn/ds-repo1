import random
import pandas as pd 

from sklearn.preprocessing import OrdinalEncoder
from pyod.models.iforest import IForest



if __name__ == "__main__":

    data = [] 
    c = 5000


    with open("data/sample_ip_addresses.csv") as infile:
        fakeclients = infile.read().split("\n")

    with open("data/sample_names.csv") as infile:
        allnames = infile.read().split("\n")

    fakeuseragents1 = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1',
        'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/8.2 Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    ]
    fakeuseragents1_weights = [25,25,2,23,25]

    data = []
    while c > 0:
        row = {}
        row['un'] = random.choice(allnames)
        row['client'] = random.choice(fakeclients)
        row['useragent'] = random.choices(fakeuseragents1, fakeuseragents1_weights,k=1)[0]
        data.append(row)
        c -=1
    #

    fakedf = pd.DataFrame(data)



    encoder = OrdinalEncoder()
    fakedf_encoded = encoder.fit_transform(fakedf)
    fakedf_encoded = pd.DataFrame(data=fakedf_encoded,columns=['user','client','useragent']).copy()




    iforest = IForest(n_estimators=10000)
    iforest.fit(fakedf_encoded)

    labels = iforest.labels_

    print(fakedf[labels==0].shape)
    print(fakedf[labels==1].shape)

    print(fakedf[labels==1].groupby(['useragent']).agg({'client':['count']}))
