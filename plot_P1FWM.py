#!/usr/bin/env python3
#
# PJB 2018, plot histograms from csv file, hardcoded 20x20,
#           see selection line 151, reshape in line 201, and 19 in ticks()
#
import pandas as pd
import numpy as np
from collections import Counter
import sys
import math
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
#from matplotlib.colors import LogNorm
from sklearn import preprocessing
import argparse
import os
import joblib


'''
import sklearn.preprocessing as prep

def standard_scale(X_train, X_test):
    preprocessor = prep.StandardScaler().fit(X_train)
    X_train = preprocessor.transform(X_train)
    X_test = preprocessor.transform(X_test)
    return X_train, X_test
'''

'''
T_CHASSIS Repair date Analysis result
B-619621 2018-01-27   FOD Compressor
A-677319 2018-04-09   FOD Turbine
B-840419 2018-07-27   FOD Turbine
B-762449 2018-06-25   FOD Compressor
A-717140 2018-08-02   FOD Compressor
B-665712 2018-06-07   FOD Compressor
B-662097 2018-06-08   FOD Compressor
A-760812 2018-07-18   FOD Compressor

B-619621,A-677319,B-840419,B-762449,A-717140,B-665712,B-662097,A-760812
'''


parser = argparse.ArgumentParser()
parser.add_argument( '-a', "--anonymous", action='store_true', default=False, help='Hide axes' )
parser.add_argument( '-t', "--truck", type=str, default=None, help='PLot one truck ID' )
parser.add_argument( '-f', "--filename", type=str, default="data_frame--2018-09-25--11-17-39.csv", help='CSV filename' )
parser.add_argument( '-n', "--normalise", action='store_true', default=False, help='Normalise' )
parser.add_argument( "--max_pics", type=int, default=16, help='Max histograms on a plot' )
parser.add_argument( "--cols", type=int, default=4, help='Number of histogram columns in plot' )
parser.add_argument( "--rows", type=int, default=None, help='Number of rows to read from CSV file' )
parser.add_argument( "--top", type=int, default=None, help='Top n' )
parser.add_argument( "--start", type=int, default=0, help='Start histogram' )
parser.add_argument( "--trucks", type=str, default=None, help='Multiple chassis IDs, comma seperated' )
args = parser.parse_args()

print( "Reading data...", end="", flush=True)
if not os.path.exists("df_train.pickle"):
    lines = []#list(range(1, 100000))
    df_train = pd.read_csv( args.filename,
                            sep=";", dtype={'VEHICL_ID': str},
                            #skiprows=lines,
                            nrows=args.rows
    )
    #print( "pickling...", end="", flush=True )
    #joblib.dump( df_train,"df_train.pickle" )
    #df_train.to_pickle("df_train.pickle")
else:
    print( "from pickle...", end="", flush=True)
    df_train = pd.read_pickle("df_train.pickle")
print( "Ready" )
print( df_train.shape )
print( df_train.head(2) )

# VEHICL_ID;T_CHASSIS;PARAMETER_CODE;truck_date;....;valid;repaired
the_label      = "repaired"
the_id         = "T_CHASSIS" 
the_date       = "truck_date"

#print( df_train[the_label].value_counts() )
#print( len(df_train[the_label].value_counts()) )
    
'''
[2 rows x 406 columns]
A-767346    129
A-769350    116
B-697108    105
A-747853    104
B-699946    101
A-773130    101
B-693478     97
A-761610     96
A-776912     95
B-697036     95
A-775088     94
A-758050     94
A-766953     91
B-697216     91
B-701388     91
B-702604     91
B-704830     91
A-786632     91
A-772973     91
A-769520     90
B-706867     90
A-763820     90
A-762902     90
A-769728     90
'''

uniqs = pd.unique( df_train[the_id] ) 
if args.truck:
    uniqs = [ args.truck ]
if args.trucks:
    uniqs = args.trucks.split(",")
if args.top:
    uniqs = uniqs[0:args.top]
print( uniqs )

#normalise = False #True
#max_pics  = 36

for the_vehicle_id in uniqs:
    ##
    print( the_vehicle_id )

    try:
        df_train1 = df_train[ ( df_train[the_id] == the_vehicle_id ) ]
    except:
        print( "ERROR..." )
        continue
    
    df_train1 = df_train1.sort_values(by=[the_date])
    num_pics = df_train1.shape[0]
    if num_pics <= 0:
        print( "skipping", the_vehicle_id, num_pics )
        continue
    df_train1.to_csv( "P1FWM_"+the_vehicle_id+".csv", sep=";", index=False )
    
    # Plot the last ones, according to date
    if num_pics > args.max_pics:
        #df_train1 = df_train1.iloc[-args.max_pics:]
        #num_pics = df_train1.shape[0]
        st = num_pics - args.max_pics #st is the start in the array
        num_pics = args.max_pics

    #if args.start:
    st = args.start
 
    train_data    = df_train1.iloc[ :,  4:404]
    train_labels  = df_train1.loc[ :, the_label]
    train_chassis = df_train1.loc[ :, the_id]
    train_sdate   = df_train1.loc[ :, the_date]
    train_part    = "" #df_train1.loc[ :, "PARTITIONNING"]
    print( train_data.head(2) )
    print( train_sdate.head(2) )
    #
    sp = 1
    n  = 3 #4
    cols = args.cols
    rows = int(num_pics / cols) + 1*((num_pics % cols)!=0)
    #nn = n * n
    nn = rows * cols
    #sz = n*3
    pc = 0 # pic count
    #
    fig = plt.figure(figsize=(cols*3, rows*3)) #plt.figure(figsize=(sz,sz))
    plt.subplots_adjust( hspace=0.7, wspace=0.5 )
    #
    # Plot the last nn
    #if num_pics > nn:
    #    st = num_pics - nn
    #    print( "Starting at", st )
    #
    for i in range(st, st+nn):
        idx = i #ids.pop() # this plots same T_CHASSIS defined in triplets loop above
        try:
            im = train_data.iloc[idx,:] #idx was i
        except:
            ax.set_aspect('equal')
            ax.get_xaxis().set_ticks([])
            ax.get_yaxis().set_ticks([])
            ax.set_xlabel( "" )
            ax.set_ylabel( "" )
            sp += 1
            continue
        ax = fig.add_subplot(rows,cols,sp) #was n, n, sp
        pc += 1
        hist_label = train_labels.iloc[idx] #idx was i
        timestamp  = train_sdate.iloc[idx] 
        timestamp  = timestamp[0:10] # lose the time
        partition  = "" #train_part.iloc[idx][0]
        #qprint( i, hist_label )
        if hist_label == 0:
            ax.set_title( str(i)+"/l="+str(hist_label)+" "+str(timestamp)+" "+partition )
        else:
            ax.set_title( str(i)+"/l="+str(hist_label)+" "+str(timestamp)+" "+partition, color="red" )
        #im = minmax_scale(im)
        #im = im / np.linalg.norm(im)
        im = np.reshape( im, (20, 20) )
        im = np.flipud(im) #rot90(im) #flipud(im) #rot90()
        #print( im )
        #
        if args.normalise:
            _min = 0
            _max = 1
            im += -(np.min(im))
            im /= np.max(im) / (_max - _min)
            #im += _min
        #
        im_masked = np.ma.masked_where(im == 0, im)
        plt.imshow( im_masked, interpolation='none')# vmin=0, vmax=10) #cmap="binary"
        ax.set_aspect('equal')
        ax.get_xaxis().set_ticks([0, 19])
        ax.get_yaxis().set_ticks([])
        #
        ax.set_xticks(np.arange(-.5, 19, 1), minor=True);
        ax.set_yticks(np.arange(-.5, 19, 1), minor=True);
        ax.grid(which='minor', color='w', linestyle='-', linewidth=1)
        #
        if not args.anonymous:
            ax.set_xlabel( "engine speed" )
            ax.set_ylabel( "engine torque" )
            plt.colorbar(orientation='vertical', ax=ax, format='%.1f', fraction=0.0408, pad=0.04)
            #plt.clim(0, 10);
        else:
            plt.colorbar(orientation='vertical', ax=ax, ticks=[])
        sp += 1
    if not args.anonymous:
        fig.suptitle( the_id+": "+str(the_vehicle_id)+' P1FWM' ) #Training data '+str(st)+" +"+str(nn) )
    fn = "training_"+str(the_vehicle_id)+"_"+str(st)+"+"+str(pc)
    if args.normalise:
        fn += "_N"
    fn += ".png"
    print( "Saving", fn )
    if os.path.exists( fn ):
        os.remove( fn )
    fig.savefig( fn, dpi=288 )
    #plt.show()
