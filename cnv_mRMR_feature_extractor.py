# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 15:17:02 2021

@author: Nikhil
"""


import pandas as pd 
import os
import pymrmr

cancer_type =  ['BRCA']
index = 0
path = '/Data/nikhilanand_1921cs24/VAE_SVM/'+cancer_type[index]+'/cnv'
cnv_file_name = 'TCGA-BRCA.gistic.tsv'
# transposing raw CNV data and sorting them by patietnt Ids or TCGA Ids
# =============================================================================
df_cnv = pd.read_csv(os.path.join(path,cnv_file_name), header=None,index_col=0, delimiter="\t",low_memory=False).T# read the csv data file and transpose it
df_cnv=df_cnv.sort_values(by=['Gene Symbol'],ascending=True) # sorting based on tcga ids
df_cnv.drop_duplicates(subset ="Gene Symbol",keep=False,inplace=True)
# =============================================================================
#Mapping CNV patient ids with survival labels
# =============================================================================
df_cnv_id=df_cnv['Gene Symbol'] # extracting tcga ids from CNV dataframe
df_survival_label = pd.read_csv(os.path.join(path,'5_year_survival.csv'),delimiter=',') # reading survival csv file
survival_df = df_survival_label[df_survival_label['sample'].isin(df_cnv_id)] # selcting survival label of tcga ids matching with CNV tcga ids
survival_df=survival_df.sort_values(by=['sample'],ascending=True) # sorting survival labels based on tcga ids
survival_df.drop_duplicates(subset ="sample",keep=False,inplace=True)
survival_id = survival_df['sample'] # extracting tcga ids from survival labels
df_cnv = df_cnv[df_cnv['Gene Symbol'].isin(survival_id)] # selecting CNV data of patients matching with avivalable survival ids
# =============================================================================
#applying mRMR feature selection
# =============================================================================
class_labels = survival_df['5_year_cutoff'] # fetching the class labels
cnv_features_df = df_cnv.drop('Gene Symbol', axis=1) # remving tcga ids from mRNA data
cnv_features_df = cnv_features_df.astype(int)
cnv_features_df.insert(0, "class_label", class_labels.values, True) # adding class labels at the first column of the mRNA features to make it usable for mRMR feature selction algo.
print(cnv_features_df.info())
features = pymrmr.mRMR(cnv_features_df, 'MID', 200) #fetching mRMR features
print(features)
df_cnv = df_cnv[features]
df_cnv.insert(0, "TCGA_ID", survival_id.values, True)
df_cnv.insert(loc = len(df_cnv.columns),column = 'label',value = class_labels.values)
output_file_name = 'mRMR_200_cnv.csv'
df_cnv.to_csv(os.path.join(path,output_file_name),index=False)
print("Files have been saved to: "+os.path.join(path))