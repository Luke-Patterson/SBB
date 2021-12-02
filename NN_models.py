import sys
import datetime
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import scipy
import pickle
sys.path.append('C:/AnacondaProjects/sbb')

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision import transforms
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#creating deepcopy of model instances
from copy import deepcopy

#selected plotting functions
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

#classes for grid search and cross-validation, function for splitting data and evaluating models
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,train_test_split
from skopt import BayesSearchCV
from sklearn.metrics import accuracy_score,f1_score,roc_auc_score,confusion_matrix,roc_curve

#Python standard libraries
import time
import warnings

# model for selecting position of char
class NN_Position_Model:
    def __init__(self):
        pass

    def load_training_data(self, data_files, names_file, mtype = 'board', pandas = False,
        max_train_size = None):
        first = True
        for f in data_files:
            if first:
                train_data = pickle.load(open(f, 'rb'))
                train_columns = pickle.load(open(names_file, 'rb'))
                first = False
            else:
                train_data = scipy.sparse.vstack([train_data,
                    pickle.load(open(f, 'rb'))])


        if max_train_size != None:
            train_data = train_data[0:max_train_size, :]

        # make sure the column names are as expected for this programming
        base_columns = pickle.load(
            open("C:/Users/Luke/AnacondaProjects/sbb/prod/training_data/board_base_column_names.p",'rb'))
        assert base_columns == train_columns
        self.train_columns = train_columns
        # split training data into X and Y vars
        if pandas:
            self.full_train = train_data[:,0:999]
            self.xtrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,0:998])
            self.xtrain.columns = train_columns[0:998]
            self.xtrain = self.xtrain.set_index(['game_id','player_id'], drop = True)
            self.ytrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,998])
            assert train_columns[998] == 'battle_not_lost'
            self.ytrain.columns = ['battle_not_lost']
            # drop columns that are all the same value
            nunique = self.xtrain.apply(pd.Series.nunique)
            cols_to_drop = nunique[nunique == 1].index
            print('dropping',len(cols_to_drop),'columns with all same values')
            self.xtrain=self.xtrain.drop(cols_to_drop, axis=1)
            self.n_xvars = len(self.xtrain.columns)
        else:
            self.full_train = train_data[:,0:999]
            self.xtrain = train_data[:,0:998]
            # for now, just train against winning the fight
            self.ytrain = train_data[:,998]
            self.n_xvars = 998

    def set_bool_model(self):
        print('Number of Parameters:',self.n_xvars)
        self.model = nn.Sequential(nn.Linear(self.n_xvars,round(self.n_xvars/4)),
                              nn.ReLU(),
                              nn.Linear(round(self.n_xvars/4), round(self.n_xvars/8)),
                              nn.ReLU(),
                              # nn.Linear(self.n_xvars*8, self.n_xvars*16),
                              # nn.ReLU(),
                              # nn.Linear(self.n_xvars*16, 1),
                              nn.Linear(round(self.n_xvars/8), 1),
                              nn.Sigmoid())
        self.model.batch_size=32
        self.model.to(torch.device('cuda:0'))
        #self.model.to(torch.device('cpu'))

    def train_bool(self,epochs=5000, pandas = False):
        xtrain=self.xtrain
        ytrain=self.ytrain
        self.n_xvars=998
        self.set_bool_model()
        batch_size=self.model.batch_size
        transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.5,), (0.5,)),
                              ])
        device=torch.device('cuda:0')
        #device=torch.device('cpu')
        if pandas:
            trainset=torch.from_numpy(np.concatenate((xtrain.values,ytrain.values),axis=1)).to(device)
        else:
            # convert csr to coo tensor
            Acoo = self.full_train.tocoo()
            trainset = torch.sparse.LongTensor(torch.LongTensor([Acoo.row.tolist(), Acoo.col.tolist()]),
                                               torch.LongTensor(Acoo.data.astype(np.int32))).to(device)

        trainset=torch.utils.data.DataLoader(trainset,batch_size=batch_size, shuffle=True)
        criterion = nn.BCELoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        running_loss = 0
        moving_avg_acc= []
        for e in range(epochs):
            start=datetime.datetime.now()
            running_loss = 0
            correct=0
            for n, obs in enumerate(trainset):
                if n % 10000 == 0 and n != 0:
                    print(n,'batches of', len(trainset),'for this epoch completed')
                    print('Runtime:',datetime.datetime.now() - start)
                # split up the batch into labels and features
                split=torch.split(obs.to_dense(),self.n_xvars,dim=1)
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
        feats=pd.Series(self.train_columns)
        feats=feats.str.replace('"','')
        feats.to_csv(folder+filename+'_feats_used.csv',index=False)

class XGB_Position_Model:
    def __init__(self):
        pass

    def load_training_data(self, data_files, names_file, mtype = 'board', pandas = False,
        max_train_size = None):
        first = True
        for f in data_files:
            if first:
                train_data = pickle.load(open(f, 'rb'))
                train_columns = pickle.load(open(names_file, 'rb'))
                first = False
            else:
                train_data = scipy.sparse.vstack([train_data,
                    pickle.load(open(f, 'rb'))])


        if max_train_size != None:
            train_data = train_data[0:max_train_size, :]

        # make sure the column names are as expected for this programming
        base_columns = pickle.load(
            open("C:/Users/Luke/AnacondaProjects/sbb/prod/training_data/board_base_column_names.p",'rb'))
        assert base_columns == train_columns
        self.train_columns = train_columns
        # split training data into X and Y vars
        if pandas:
            self.full_train = train_data[:,0:999]
            self.xtrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,0:998])
            self.xtrain.columns = train_columns[0:998]
            self.xtrain = self.xtrain.set_index(['game_id','player_id'], drop = True)
            self.ytrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,998])
            assert train_columns[998] == 'battle_not_lost'
            self.ytrain.columns = ['battle_not_lost']
            # drop columns that are all the same value
            nunique = self.xtrain.apply(pd.Series.nunique)
            cols_to_drop = nunique[nunique == 1].index
            print('dropping',len(cols_to_drop),'columns with all same values')
            self.xtrain=self.xtrain.drop(cols_to_drop, axis=1)
            self.n_xvars = len(self.xtrain.columns)
        else:
            self.full_train = train_data[:,0:999]
            self.xtrain = train_data[:,0:998]
            # for now, just train against winning the fight
            self.ytrain = train_data[:,998]
            self.n_xvars = 998

    def train_bool(self,**kwargs):
        self.n_xvars=998
        X = pd.DataFrame.sparse.from_spmatrix(self.xtrain)
        y=  pd.DataFrame.sparse.from_spmatrix(self.ytrain)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        # xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
        #         max_depth = 5, alpha = 10, n_estimators = 10)
        # xg_reg.fit(X_train,y_train)
        # preds = xg_reg.predict(X_test)
        # rmse = np.sqrt(mean_squared_error(y_test.values, preds))
        # self.model = xg_reg
        dmatrix = xgb.DMatrix(data=X, label=y)
        params={'objective':'reg:squarederror'}
        start = datetime.datetime.now()
        #cv_results = xgb.cv(dtrain=dmatrix, params=params, nfold=10, metrics={'rmse'}, as_pandas=True, seed=20)
        xgbc0 = xgb.XGBClassifier(objective='binary:logistic',
                          booster='gbtree',
                          eval_metric='auc',
                          tree_method='hist',
                          grow_policy='lossguide',
                          use_label_encoder=False)
        xgbc0.fit(X_train , y_train)

        #extracting default parameters from benchmark model
        default_params = {}
        gparams = xgbc0.get_params()

        for key in gparams.keys():
            gp = gparams[key]
            default_params[key] = [gp]


        #creating deepcopy of default parameters before manipulations
        params = deepcopy(default_params)

        #setting grid of selected parameters for iteration
        param_grid = {'gamma': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4, 200],
                      'learning_rate': [0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.25, 0.300000012, 0.4, 0.5, 0.6, 0.7],
                      'max_depth': [5,6,7,8,9,10,11,12,13,14],
                      'n_estimators': [50,65,80,100,115,130,150],
                      'reg_alpha': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4,200],
                      'reg_lambda': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4,200]}
        #start time
        t0 = time.time()
        #No. of jobs
        gcvj = np.cumsum([len(x) for x in param_grid.values()])[-1]

        #No. of jobs
        bcvj = int(gcvj)

        #unwrapping list values of default parameters
        default_params_xgb = {}

        for key in default_params.keys():
            default_params_xgb[key] = default_params[key][0]

        #providing default parameters to xgbc model, before randomized search cross-validation
        xgbc = xgb.XGBClassifier(**default_params_xgb)

        clf = BayesSearchCV(estimator=xgbc, search_spaces=param_grid, n_iter=bcvj,
            scoring='accuracy', cv=3, return_train_score=True, verbose=1)
        clf.fit(X_train, y_train.values.ravel())

        #results dataframe
        df = pd.DataFrame(clf.cv_results_)

        #predictions - inputs to confusion matrix
        train_predictions = clf.predict(X_train)
        test_predictions = clf.predict(X_test)
        # unseen_predictions = clf.predict(df_test.iloc[:,1:])

        #confusion matrices
        cfm_train = confusion_matrix(y_train, train_predictions)
        cfm_test = confusion_matrix(y_test, test_predictions)
        # cfm_unseen = confusion_matrix(df_test.iloc[:,:1], unseen_predictions)

        #accuracy scores
        accs_train = accuracy_score(y_train, train_predictions)
        accs_test = accuracy_score(y_test, test_predictions)
        # accs_unseen = accuracy_score(df_test.iloc[:,:1], unseen_predictions)

        #F1 scores for each train/test label
        f1s_train_p1 = f1_score(y_train, train_predictions, pos_label=1)
        f1s_train_p0 = f1_score(y_train, train_predictions, pos_label=0)
        f1s_test_p1 = f1_score(y_test, test_predictions, pos_label=1)
        f1s_test_p0 = f1_score(y_test, test_predictions, pos_label=0)
        # f1s_unseen_p1 = f1_score(df_test.iloc[:,:1], unseen_predictions, pos_label=1)
        # f1s_unseen_p0 = f1_score(df_test.iloc[:,:1], unseen_predictions, pos_label=0)

        #Area Under the Receiver Operating Characteristic Curve
        test_ras = roc_auc_score(y_test.values, clf.predict_proba(X_test)[:,1])
        # unseen_ras = roc_auc_score(df_test.iloc[:,:1], clf.predict_proba(df_test.iloc[:,1:])[:,1])

        #best parameters
        bp = clf.best_params_

        #storing computed values in results dictionary
        results_dict = {'classifier': deepcopy(clf),
                                    'cv_results': df.copy(),
                                    'cfm_train': cfm_train,
                                    'cfm_test': cfm_test,
                                    # 'cfm_unseen': cfm_unseen,
                                    'train_accuracy': accs_train,
                                    'test_accuracy': accs_test,
                                    # 'unseen_accuracy': accs_unseen,
                                    'train F1-score label 1': f1s_train_p1,
                                    'train F1-score label 0': f1s_train_p0,
                                    'test F1-score label 1': f1s_test_p1,
                                    'test F1-score label 0': f1s_test_p0,
                                    # 'unseen F1-score label 1': f1s_unseen_p1,
                                    # 'unseen F1-score label 0': f1s_unseen_p0,
                                    'test roc auc score': test_ras,
                                    # 'unseen roc auc score': unseen_ras,
                                    'best_params': bp}

        #stop time
        t1 = time.time()

        #elapsed time
        bcvt = t1 - t0

        xgb_opt = xgb.XGBClassifier(**bp, use_label_encoder=False, eval_metric='logloss')
        xgb_opt.fit(X, y.values.ravel())
        self.model = xgb_opt
        # print(datetime.datetime.now() - start)
        # print('RMSE: %.2f' % cv_results['test-rmse-mean'].min())
        #
        # params={'objective':'reg:squarederror',
        #  'max_depth': 6,
        #  'colsample_bylevel':0.5,
        #  'learning_rate':0.01,
        #  'random_state':20}
        # start = datetime.datetime.now()
        # cv_results = xgb.cv(dtrain=dmatrix, params=params, nfold=10, metrics={'rmse'}, as_pandas=True, seed=20, num_boost_round=1000)
        # print(datetime.datetime.now() - start)
        # print('RMSE: %.2f' % cv_results['test-rmse-mean'].min())
        # import pdb; pdb.set_trace()

    def save_model(self,folder,filename):
        pickle.dump(self.model, open(folder+filename+".p", "wb" ) )
        # save the features used
        feats=pd.Series(self.train_columns)
        feats=feats.str.replace('"','')
        feats.to_csv(folder+filename+'_feats_used.csv',index=False)
