import pandas as pd
import numpy as np
from collections import Counter
import sys
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale

#trainset = pd.read_csv("trainset_dnn.csv")
#print( trainset.shape )
#testset = pd.read_csv("testset_dnn.csv")
#valset = pd.read_csv("validationset_dnn.csv")

'''
trainset = pd.read_csv("trainset.csv")
trainset = trainset["T_CHASSIS"]
trainset_list = list(trainset)
testset = pd.read_csv("testset.csv")
testset = testset["T_CHASSIS"]
testset_list = list(testset)
valset = pd.read_csv("validationset.csv")
valset = valset["T_CHASSIS"]
valset_list = list(valset)

train_labels = pd.read_csv("int_labels_train.csv", names=["label"])
train_labels = train_labels["label"]
test_labels = pd.read_csv("int_labels_test.csv", names=["label"])
test_labels = test_labels["label"]
val_labels = pd.read_csv("int_labels_validate.csv", names=["label"])
val_labels = val_labels["label"]
'''

'''
triplets = Counter()
ids = []
for i, x in enumerate(trainset_list):
    if x in testset_list and x in valset_list:
        print( i, x )
        triplets[x] += 1
        if x == "O6YU-167502":
            ids.append(i)
print( triplets )
print( ids )
'''

train_hists = pd.read_csv("train_lT_CHASSIS_s10000_h10x10.csv", index_col=0)
sp = 1
st = 0 #400
n  = 2 #4
nn = n * n
fig = plt.figure(figsize=(16, 16))
plt.subplots_adjust( hspace=0.4 )
for i in range(st, st+nn):
    ax = fig.add_subplot(n,n,sp)
    idx = i #ids.pop() # this plots same T_CHASSIS defined in tripliets loop above
    ax.set_title( str(i) )
    im = train_hists.loc[idx,:] #idx was i
    #im = minmax_scale(im)
    #im = im / np.linalg.norm(im)
    im = np.reshape( im, (20, 20) )
    #print( im )
    plt.imshow( im, interpolation='none' )
    ax.set_aspect('equal')
    plt.colorbar(orientation='vertical', ax=ax)
    sp += 1
fig.suptitle( 'Training data '+str(st)+" +"+str(nn) )
fig.savefig( "training_"+str(st)+"+"+str(nn)+".png", dpi=288 )
plt.show()

print( "CODINGS" )
# each lbl should end up with a list of 1, 2, or 3 items with same value.
foo = {}
for i in range(0, len(trainset)):
    lbl = trainset[i]
    if lbl in foo:
        foo[lbl].append( train_labels[i] )
    else:
        foo[lbl] = [ train_labels[i] ]
for i in range(0, len(testset)):
    lbl = testset[i]
    if lbl in foo:
        foo[lbl].append( test_labels[i] )
    else:
        foo[lbl] = [ test_labels[i] ]
for i in range(0, len(valset)):
    lbl = valset[i]
    if lbl in foo:
        foo[lbl].append( val_labels[i] )
    else:
        foo[lbl] = [ val_labels[i] ]
        
    #print( trainset[i], train_labels[i] )
    #print( testset[i], test_labels[i] )
    #print( valset[i], val_labels[i] )
    #print( testset.value_counts().head(10) )
    #print( test_labels.value_counts().head(10) )
    #print( "HEADS, VALIDATION" )
    #print( valset.value_counts().head(10) )
    #print( val_labels.value_counts().head(10) )
print( "Unique labels in train+test+validation sets:", len(foo) )
for lbl in foo:
    lst = foo[lbl]
    if lst.count(lst[0]) != len(lst):
        print( lbl, lst )
    #if len(lst) == 3:
    #    print( "all", lbl, lst )

print( "INTERSECTION TRAIN - VALIDATION" )
print( "train_labels", len(train_labels), "unique", len(train_labels.unique()) )
print( train_labels.value_counts().head() )
print( "val_labels", len(val_labels), "unique", len(val_labels.unique()) )
print( val_labels.value_counts().head() )
res = pd.Series( np.intersect1d( train_labels.values, val_labels.values ) )
# types I guess, the intersect/values makes it like sets
# but len(val_labels)-len(intersection) are not in val_labels
print( "intersection", len(res), len(res)/len(train_labels) )
c = set(val_labels.values) - set(train_labels.values)
print( "Unique labels in validation that are not in training", len(c) )
s = sum( el in train_labels.values for el in val_labels.values )
print( "Sum labels in validation that are in training", s, "{:.2f}".format(s/len(val_labels.values)) )

print( "" )
print( "INTERSECTION TRAIN - TEST" )
print( "test_labels", len(test_labels), "unique", len(test_labels.unique()) )
print( test_labels.value_counts().head() )
res = pd.Series(np.intersect1d( train_labels.values, test_labels.values ) )
print( "intersection", len(res), len(res)/len(train_labels) )
c = set(test_labels.values) - set(train_labels.values)
print( "Unique labels in test that are not in training", len(c) )
s = sum( el in train_labels.values for el in test_labels.values )
print( "Sum labels in test that are in training", s, "{:.2f}".format(s/len(test_labels.values)) )









'''
petber@ITE11527:~/Documents/HH/Health/tensorflow_roger_stockholm$ python3 info_dnn.py
HEADS, TRAIN
O6GY-168010    64
O9E-167510     46
O24E-174814    35
W31QZ-73       29
A-141364       26
Name: T_CHASSIS, dtype: int64
74789    64
76482    46
74705    35
79158    29
372      26
Name: label, dtype: int64

HEADS, TEST
A-141364       6
O9E-167510     4
O6GY-168010    4
O6YU-167502    3
O9E-167516     3
Name: T_CHASSIS, dtype: int64
372      6
76482    4
74789    4
75264    3
75337    3
Name: label, dtype: int64

HEADS, VALIDATION
A-960863       4
O6YU-167289    4
A-169797       3
O6GY-169214    3
A-163468       3
Name: T_CHASSIS, dtype: int64
75258    4
57707    4
74881    3
75703    3
76482    3
Name: label, dtype: int64

INTERSECTION TRAIN - VALIDATION
train_labels 68419 unique 38725
74789    64
76482    46
74705    35
79158    29
372      26
Name: label, dtype: int64

val_labels 3802 unique 3612
75258    4
57707    4
74881    3
75703    3
76482    3
Name: label, dtype: int64

intersection 2358 0.034464110846402315
Unique labels in validation that are not in training 1254
Sum labels in validation that are in training 2520 0.66

INTERSECTION TRAIN - TEST
test_labels 3801 unique 3609
372      6
76482    4
74789    4
75264    3
75337    3
Name: label, dtype: int64
intersection 2379 0.034771043131293936
Unique labels in test that are not in training 1230
Sum labels in test that are in training 2548 0.67
'''
