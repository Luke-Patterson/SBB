import sys
import datetime
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import scipy
import pickle
sys.path.append('C:/AnacondaProjects/sbb')

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch.autograd import Variable
# from torchvision import transforms
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
import statistics

class XGB_Position_Model:
    def __init__(self):
        pass

    def load_training_data(self, data_files, mtype = 'board',
        max_train_size = None):
        '''
        load training data and set attributes to match training data
        params:
        data_files - list of paths containing training data pickles
        target_var - name of var to use as target variable
        mtype - name of type of model
        max_train_size - cap on number of records used in the data
        addl_features - list of additional feature labels to use
        '''
        first = True
        for f in data_files:
            if first:
                payload = pickle.load(open(f, 'rb'))
                colnames = payload['columns']
                self.colnames = colnames
                data = payload['data']
                self.feature_dict = payload['feature_types']
                first = False
            else:
                loaded = pickle.load(open(f, 'rb'))

                # make sure data has the same number of columns as first data set
                loaded['data'].shape[1] == data.shape[1]
                loaded['colnames'] = colnames
                data = scipy.sparse.vstack([data,
                    loaded['data']])

        if type(data).__name__ == 'coo_matrix':
            data = data.tocsr()
        self.idx_feat_cut =len(self.feature_dict['index'])
        self.feat_out_cut = len(self.feature_dict['index'])+len(self.feature_dict['features'])

        if max_train_size == None:
            self.max_train_size =data.shape[0]
        else:
            self.max_train_size = max_train_size
        self.data = data

    def filter_training_data(self, filter_var, use_filt_data=False):
        # filter_var - label of var  to filter training data set to == 1

        if use_filt_data:
            filt_data = self.filt_data
        else:
            filt_data = self.data

        filt_idx = [n for n,val in self.colnames.items() if val == filter_var][0]
        filt_loc = [n for n,i in enumerate(filt_data[:,filt_idx].sum(axis=1)) if i == 1]
        filt_data = filt_data[filt_loc,:]
        self.filt_data = filt_data

    def store_filter_data(self):
        self.saved_filt_data = self.filt_data

    def restore_filter_data(self):
        self.filt_data = self.saved_filt_data

    def train_bool(self,target_var, char_filter_var=None, out_filter_var=None):
        '''
        train a XGB boolean prediction model
        params
        target_var - label of y var to be trained
        '''
        ycol_idx = [n for n,val in self.colnames.items() if val == target_var][0]

        # divide data into X and y data sets
        col_list = [i for i in range(self.idx_feat_cut,self.feat_out_cut)]

        self.train_data = self.filt_data[0:self.max_train_size, :]
        self.train_data = self.filt_data[0:int(round(self.train_data.shape[0])*.99), :]
        self.unseen_data = self.filt_data[int(round(self.train_data.shape[0])*.99):self.train_data.shape[0], :]

        # if we are specifying a feature column as a target, need to remove that from the training data
        if target_var in [self.colnames[i] for i in self.feature_dict['features']]:
            col_list.remove(ycol_idx)
        self.xtrain = self.train_data[:,col_list]
        self.xunseen = self.unseen_data[:,col_list]
        self.n_xvars = len(col_list)

        self.ytrain =self.train_data[:,ycol_idx]
        self.yunseen = self.unseen_data[:,ycol_idx]

        # X = pd.DataFrame.sparse.from_spmatrix(self.xtrain)
        y=  pd.DataFrame.sparse.from_spmatrix(self.ytrain)
        X = self.xtrain
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        #cv_results = xgb.cv(dtrain=dmatrix, params=params, nfold=10, metrics={'rmse'}, as_pandas=True, seed=20)
        # xgbc0 = xgb.XGBClassifier(objective='binary:logistic',
        #                   booster='gbtree',
        #                   eval_metric='auc',
        #                   tree_method='hist',
        #                   grow_policy='lossguide',
        #                   use_label_encoder=False)
        # xgbc0.fit(X_train , y_train)
        #
        # #extracting default parameters from benchmark model
        # default_params = {}
        # gparams = xgbc0.get_params()
        #
        # for key in gparams.keys():
        #     gp = gparams[key]
        #     default_params[key] = [gp]
        #
        #
        # #creating deepcopy of default parameters before manipulations
        # params = deepcopy(default_params)
        #
        # #setting grid of selected parameters for iteration
        # param_grid = {'gamma': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4, 200],
        #               'learning_rate': [0.01, 0.03, 0.06, 0.1, 0.15, 0.2, 0.25, 0.300000012, 0.4, 0.5, 0.6, 0.7],
        #               'max_depth': [5,6,7,8,9,10,11,12,13,14],
        #               'n_estimators': [50,65,80,100,115,130,150],
        #               'reg_alpha': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4,200],
        #               'reg_lambda': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4,200]}
        # # try increasing max depth and n_estimators
        # param_grid['max_depth'] = [i * 2 for i in param_grid['max_depth']]
        # param_grid['n_estimators'] = [i * 5 for i in param_grid['n_estimators']]
        #
        # #start time
        # t0 = time.time()
        # #No. of jobs
        # gcvj = np.cumsum([len(x) for x in param_grid.values()])[-1]
        #
        # #No. of jobs
        # #bcvj = int(gcvj)
        # bcvj = int(gcvj)
        # #unwrapping list values of default parameters
        # default_params_xgb = {}
        #
        # for key in default_params.keys():
        #     default_params_xgb[key] = default_params[key][0]

        #providing default parameters to xgbc model, before randomized search cross-validation
        xgbc = xgb.XGBClassifier(objective='binary:logistic',
                          booster='gbtree',
                          eval_metric='auc',
                          tree_method='hist',
                          grow_policy='lossguide',
                          use_label_encoder=False)

        param_grid = {''
                      'gamma': [6.4],
                      'learning_rate': [0.06],
                      'max_depth': [10],
                      'n_estimators': [150],
                      'reg_alpha': [1.6],
                      'reg_lambda': [0.1]}
        clf = BayesSearchCV(estimator=xgbc, search_spaces=param_grid, n_iter=1,
            scoring="neg_mean_absolute_error", cv=3, return_train_score=True, verbose=0)
        # dmatrix= xgb.DMatrix(data=X_train,label=y_train.values.ravel())
        # clf = xgb.cv(data = dmatrix,params = {'gamma':6.4, 'learning_rate':0.06,
        #     'max_depth':10, 'n_estimators':750, 'reg_alpha':1.6, 'reg_lambda'0.1)
        clf.fit(X_train, y_train.values.ravel())

        #results dataframe
        df = pd.DataFrame(clf.cv_results_)

        #predictions - inputs to confusion matrix
        train_predictions = clf.predict(X_train)
        test_predictions = clf.predict(X_test)
        unseen_predictions = clf.predict(self.unseen_data[:,col_list])

        y_unseen = pd.DataFrame.sparse.from_spmatrix(self.yunseen).values.ravel()
        #confusion matrices
        cfm_train = confusion_matrix(y_train, train_predictions)
        cfm_test = confusion_matrix(y_test, test_predictions)
        cfm_unseen = confusion_matrix(y_unseen, unseen_predictions)

        #accuracy scores
        accs_train = accuracy_score(y_train, train_predictions)
        accs_test = accuracy_score(y_test, test_predictions)
        accs_unseen = accuracy_score(y_unseen, unseen_predictions)

        #F1 scores for each train/test label
        f1s_train_p1 = f1_score(y_train, train_predictions, pos_label=1)
        f1s_train_p0 = f1_score(y_train, train_predictions, pos_label=0)
        f1s_test_p1 = f1_score(y_test, test_predictions, pos_label=1)
        f1s_test_p0 = f1_score(y_test, test_predictions, pos_label=0)
        f1s_unseen_p1 = f1_score(y_unseen, unseen_predictions, pos_label=1)
        f1s_unseen_p0 = f1_score(y_unseen, unseen_predictions, pos_label=0)

        #Area Under the Receiver Operating Characteristic Curve
        test_ras = roc_auc_score(y_test.values, clf.predict_proba(X_test)[:,1])
        unseen_ras = roc_auc_score(y_unseen, clf.predict_proba(
            self.unseen_data[:,col_list])[:,1])

        #best parameters
        bp = clf.best_params_

        #storing computed values in results dictionary
        results_dict = {'classifier': deepcopy(clf),
                                    'cfm_train': cfm_train,
                                    'cfm_test': cfm_test,
                                    'cfm_unseen': cfm_unseen,
                                    'train_accuracy': accs_train,
                                    'test_accuracy': accs_test,
                                    'unseen_accuracy': accs_unseen,
                                    'train F1-score label 1': f1s_train_p1,
                                    'train F1-score label 0': f1s_train_p0,
                                    'test F1-score label 1': f1s_test_p1,
                                    'test F1-score label 0': f1s_test_p0,
                                    'unseen F1-score label 1': f1s_unseen_p1,
                                    'unseen F1-score label 0': f1s_unseen_p0,
                                    'test roc auc score': test_ras,
                                    'unseen roc auc score': unseen_ras,
                                    'best_params': bp}

        #stop time
        t1 = time.time()


        # xgb_opt = xgb.XGBClassifier(**bp, use_label_encoder=False, eval_metric='logloss')
        # xgb_opt.fit(X, y.values.ravel())
        # self.model = xgb_opt
        self.model = clf
        # print('Training runtime:',datetime.datetime.now() - start)
        # sample predict
        sample_X = self.unseen_data[0:50,col_list]
        # start = datetime.datetime.now()
        preds = clf.predict_proba(sample_X)
        #print(preds)
        #print('Predict runtime for 50 obs:',datetime.datetime.now() - start)

        print('Unseen auc:',results_dict['unseen roc auc score'])
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
        feats=pd.Series(self.colnames)
        feats=feats.str.replace('"','')
        feats.to_csv(folder+filename+'_feats_used.csv',index=False)

    def load_model(self, label, filepath):
        self.model = pickle.load(open(filepath, 'rb'))

# model for selecting position of char
class NN_Position_Model:
    def __init__(self):
        pass

    # def load_training_data(self, data_files, names_file, mtype = 'board', pandas = False,
    #     max_train_size = None):
    #     first = True
    #     for f in data_files:
    #         if first:
    #             train_data = pickle.load(open(f, 'rb'))
    #             train_columns = pickle.load(open(names_file, 'rb'))
    #             first = False
    #         else:
    #             train_data = scipy.sparse.vstack([train_data,
    #                 pickle.load(open(f, 'rb'))])
    #
    #
    #     if max_train_size != None:
    #         train_data = train_data[0:max_train_size, :]
    #
    #     # make sure the column names are as expected for this programming
    #     base_columns = pickle.load(
    #         open("training_data/board_base_column_names.p",'rb'))
    #     assert base_columns == train_columns
    #     self.train_columns = train_columns
    #     # split training data into X and Y vars
    #     if pandas:
    #         self.full_train = train_data[:,0:999]
    #         self.xtrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,0:998])
    #         self.xtrain.columns = train_columns[0:998]
    #         self.xtrain = self.xtrain.set_index(['game_id','player_id'], drop = True)
    #         self.ytrain = pd.DataFrame.sparse.from_spmatrix(train_data[:,998])
    #         assert train_columns[998] == 'battle_not_lost'
    #         self.ytrain.columns = ['battle_not_lost']
    #         # drop columns that are all the same value
    #         nunique = self.xtrain.apply(pd.Series.nunique)
    #         cols_to_drop = nunique[nunique == 1].index
    #         print('dropping',len(cols_to_drop),'columns with all same values')
    #         self.xtrain=self.xtrain.drop(cols_to_drop, axis=1)
    #         self.n_xvars = len(self.xtrain.columns)
    #     else:
    #         self.full_train = train_data[:,0:999]
    #         self.xtrain = train_data[:,0:998]
    #         # for now, just train against winning the fight
    #         self.ytrain = train_data[:,998]
    #         self.n_xvars = 998
    #
    # def set_bool_model(self):
    #     print('Number of Parameters:',self.n_xvars)
    #     self.model = nn.Sequential(nn.Linear(self.n_xvars,round(self.n_xvars/4)),
    #                           nn.ReLU(),
    #                           nn.Linear(round(self.n_xvars/4), round(self.n_xvars/8)),
    #                           nn.ReLU(),
    #                           # nn.Linear(self.n_xvars*8, self.n_xvars*16),
    #                           # nn.ReLU(),
    #                           # nn.Linear(self.n_xvars*16, 1),
    #                           nn.Linear(round(self.n_xvars/8), 1),
    #                           nn.Sigmoid())
    #     self.model.batch_size=32
    #     self.model.to(torch.device('cuda:0'))
    #     #self.model.to(torch.device('cpu'))
    #
    # def train_bool(self,epochs=5000, pandas = False):
    #     xtrain=self.xtrain
    #     ytrain=self.ytrain
    #     self.n_xvars=998
    #     self.set_bool_model()
    #     batch_size=self.model.batch_size
    #     transform = transforms.Compose([transforms.ToTensor(),
    #                             transforms.Normalize((0.5,), (0.5,)),
    #                           ])
    #     device=torch.device('cuda:0')
    #     #device=torch.device('cpu')
    #     if pandas:
    #         trainset=torch.from_numpy(np.concatenate((xtrain.values,ytrain.values),axis=1)).to(device)
    #     else:
    #         # convert csr to coo tensor
    #         Acoo = self.full_train.tocoo()
    #         trainset = torch.sparse.LongTensor(torch.LongTensor([Acoo.row.tolist(), Acoo.col.tolist()]),
    #                                            torch.LongTensor(Acoo.data.astype(np.int32))).to(device)
    #
    #     trainset=torch.utils.data.DataLoader(trainset,batch_size=batch_size, shuffle=True)
    #     criterion = nn.BCELoss()
    #     optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
    #     running_loss = 0
    #     moving_avg_acc= []
    #     for e in range(epochs):
    #         start=datetime.datetime.now()
    #         running_loss = 0
    #         correct=0
    #         for n, obs in enumerate(trainset):
    #             if n % 10000 == 0 and n != 0:
    #                 print(n,'batches of', len(trainset),'for this epoch completed')
    #                 print('Runtime:',datetime.datetime.now() - start)
    #             # split up the batch into labels and features
    #             split=torch.split(obs.to_dense(),self.n_xvars,dim=1)
    #             yvar=Variable(split[1])
    #             features=Variable(split[0])
    #             optimizer.zero_grad()
    #             # get the predictions
    #             output = self.model(features.float())
    #             # evaluate the predictions
    #             loss = criterion(output, yvar.float())
    #             loss.backward()
    #             optimizer.step()
    #             running_loss += loss.item()
    #             correct += (torch.round(output) == yvar.float()).float().sum()
    #         else:
    #             accuracy=correct / (len(trainset)*batch_size)
    #             print('Epoch:',e,"| Training loss:", running_loss/len(trainset),
    #                 "| Accuracy:",accuracy, '| Epoch runtime:',datetime.datetime.now()-start)
    #             moving_avg_acc.append(accuracy)
    #         # if e % 100:
    #         #     self.save_model()
    #
    #     self.last_10_acc=sum(moving_avg_acc[-10:])/10
    #
    # def save_model(self,folder,filename):
    #     pickle.dump(self.model, open(folder+filename+".p", "wb" ) )
    #     # save the features used
    #     feats=pd.Series(self.train_columns)
    #     feats=feats.str.replace('"','')
    #     feats.to_csv(folder+filename+'_feats_used.csv',index=False)
