import sys
import datetime
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import scipy
import pickle
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision import transforms


# model for selecting position of char
class NN_Position_Model:
    def __init__(self):
        pass

    def load_training_data(self, data_file, names_file, mtype = 'board'):
        train_data = pickle.load(open(data_file, 'rb'))
        train_columns = pickle.load(open(names_file, 'rb'))

        # make sure the column names are as expected for this programming
        base_columns = pickle.load(
            open("C:/Users/Luke/AnacondaProjects/sbb/prod/training_data/board_base_column_names.p",'rb'))
        assert base_columns == train_columns

        # split training data into X and Y vars
        self.xtrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,0:998])
        self.xtrain.columns = list(train_columns.keys())[0:998]
        self.xtrain = self.xtrain.set_index(['game_id','player_id'], drop = True)
        # for now, just train against winning the fight
        self.ytrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,998])
        self.ytrain.columns = ['battle_not_lost']

        # drop columns that are all the same value
        nunique = self.xtrain.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        print('dropping',len(cols_to_drop),'columns with all same values')
        self.xtrain=self.xtrain.drop(cols_to_drop, axis=1)
        self.n_xvars = len(self.xtrain.columns)

    def set_bool_model(self):
        print('Number of Parameters:',self.n_xvars)
        self.model = nn.Sequential(nn.Linear(self.n_xvars,self.n_xvars*4),
                              nn.ReLU(),
                              nn.Linear(self.n_xvars*4, self.n_xvars*8),
                              nn.ReLU(),
                              nn.Linear(self.n_xvars*8, self.n_xvars*16),
                              nn.ReLU(),
                              nn.Linear(self.n_xvars*16, 1),
                              nn.Sigmoid())
        self.model.batch_size=32
        self.model.to(torch.device('cuda:0'))

    def train_bool(self,epochs=5000):
        xtrain=self.xtrain
        ytrain=self.ytrain
        self.n_xvars=len(xtrain.columns)
        self.set_bool_model()
        batch_size=self.model.batch_size
        transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.5,), (0.5,)),
                              ])
        device=torch.device('cuda:0')
        trainset=torch.from_numpy(np.concatenate((xtrain.values,ytrain.values),axis=1)).to(device)
        trainset=torch.utils.data.DataLoader(trainset,batch_size=batch_size, shuffle=True)
        criterion = nn.BCELoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        running_loss = 0
        moving_avg_acc= []
        for e in range(epochs):
            start=datetime.datetime.now()
            running_loss = 0
            correct=0
            for obs in trainset:
                # split up the batch into labels and features
                split=torch.split(obs,self.n_xvars,dim=1)
                yvar=Variable(split[1])
                features=Variable(split[0])
                optimizer.zero_grad()
                # get the predictions
                output = self.model(features.float())
                # evaluate the predictions
                loss = criterion(output, yvar.float())
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                correct += (torch.round(output) == yvar.float()).float().sum()
            else:
                accuracy=correct / (len(trainset)*batch_size)
                print('Epoch:',e,"| Training loss:", running_loss/len(trainset),
                    "| Accuracy:",accuracy, '| Epoch runtime:',datetime.datetime.now()-start)
                moving_avg_acc.append(accuracy)
            # if e % 100:
            #     self.save_model()

        self.last_10_acc=sum(moving_avg_acc[-10:])/10

    def save_model(self,folder,filename):
        pickle.dump(self.model, open(folder+filename+".p", "wb" ) )
        # save the features used
        feats=pd.Series(self.xtrain.columns)
        feats=feats.str.replace('"','')
        feats.to_csv(folder+filename+'_feats_used.csv',index=False)
