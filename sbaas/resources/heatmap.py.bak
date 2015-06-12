from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

import pandas as pd
import numpy as np
import cPickle as pickle

def heatmap(data_I,row_labels_I,column_labels_I):

    datasets = set(['_'.join([x.target,x.strain1+'/'+x.strain2,x.carbon_source,x.nitrogen_source,x.electron_acceptor]) for x in all_data])
    mets_data = pd.DataFrame(data=data_I, index=row_labels_I, columns=column_labels_I)

    mets_data = mets_data.dropna(how='all').fillna(0.)
    mets_data = mets_data.replace([np.inf], 10.)
    mets_data = mets_data.replace([-np.inf], -10.)
    col_labels = list(mets_data.index)
    row_labels = list(datasets)

    heatmap_data = []
    for i,g in enumerate(mets_data.index):
        for j,c in enumerate(mets_data.columns):
            heatmap_data.append({"row": j+1, "col": i+1, "value": mets_data.ix[g][c]})


    dm = mets_data
    D1 = squareform(pdist(dm, metric='euclidean'))
    D2 = squareform(pdist(dm.T, metric='euclidean'))

    Y = linkage(D1, method='single')
    Z1 = dendrogram(Y, labels=dm.index)

    Y = linkage(D2, method='single')
    Z2 = dendrogram(Y, labels=dm.columns)

    hccol = Z1['leaves'] # no hclustering; same as heatmap_data['col']
    hcrow = Z2['leaves'] # no hclustering; same as heatmap_data['row']

    hccol = [x+1 for x in hccol]
    hcrow = [x+1 for x in hcrow]

    #return hcrow,hccol,row_labels,col_labels,heatmap_data,dm
    return {'hcrow': hcrow, 'hccol': hccol, 'row_labels':row_labels,
                                        'col_labels':col_labels,
                                        'heatmap_data':heatmap_data,
                                        'maxval' : max([x['value'] for x in heatmap_data]),
                                        'minval' : min([x['value'] for x in heatmap_data]),
                                        'html_style': html_style}