# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 15:13:27 2021

@author: Nikhil
"""


import os
import pandas as pd
import pymrmr
cancer_type =  ['BRCA']
index = 0
path = '/Data/nikhilanand_1921cs24/VAE_SVM/'+cancer_type[index]+'/mRNA'
mRNA_file_name = 'TCGA-BRCA.htseq_fpkm-uq_discrete.csv'

# transposing raw mRNA data and sorting them by patietnt Ids or TCGA Ids
# =============================================================================
df_mRNA = pd.read_csv(os.path.join(path,mRNA_file_name), header=None,index_col=0, delimiter=",", low_memory=False).T# read the csv data file and transpose it
df_mRNA=df_mRNA.sort_values(by=['Ensembl_ID'],ascending=True) # sorting based on tcga ids
df_mRNA.drop_duplicates(subset ="Ensembl_ID",keep=False,inplace=True)
# =============================================================================
#Mapping mRNA patient ids with survival labels
# =============================================================================
df_mRNA_id=df_mRNA['Ensembl_ID'] # extracting tcga ids from mRNA dataframe
df_survival_label = pd.read_csv(os.path.join(path,'5_year_survival.csv'),delimiter=',') # reading survival csv file
survival_df = df_survival_label[df_survival_label['sample'].isin(df_mRNA_id)] # selcting survival label of tcga ids matching with mRNA tcga ids
survival_df=survival_df.sort_values(by=['sample'],ascending=True) # sorting survival labels based on tcga ids
survival_df.drop_duplicates(subset ="sample",keep=False,inplace=True)
survival_id = survival_df['sample'] # extracting tcga ids from survival labels
df_mRNA = df_mRNA[df_mRNA['Ensembl_ID'].isin(survival_id)] # selecting mRNA data of patients matching with avivalable survival ids
# =============================================================================
#applying mRMR feature selection
# =============================================================================
class_labels = survival_df['5_year_cutoff'] # fetching the class labels
mRNA_features_df = df_mRNA.drop('Ensembl_ID', axis=1) # remving tcga ids from mRNA data
mRNA_features_df = mRNA_features_df.astype(int)
mRNA_features_df.insert(0, "class_label", class_labels.values, True) # adding class labels at the first column of the mRNA features to make it usable for mRMR feature selction algo.
print(mRNA_features_df.info())
features = pymrmr.mRMR(mRNA_features_df, 'MID', 10) #fetching mRMR features
print(features)
df_mRNA = df_mRNA[features]
df_mRNA.insert(0, "TCGA_ID", survival_id.values, True)
df_mRNA.insert(loc = len(df_mRNA.columns),column = 'label',value = class_labels.values)
output_file_name = 'mRMR_400_mRNA.csv'
df_mRNA.to_csv(os.path.join(path,output_file_name),index=False)
print("Files have been saved to: "+os.path.join(path))