import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression


def merge():
    df1 = pd.read_csv('./mysite/VitDProducts.csv',on_bad_lines='skip')
    df2 = pd.read_csv('./mysite/VitDNeeds.csv')
    df1.columns = ["ProductCode", "ProductName", "ProductPrice","NumberOfCapsules","TypeofVitamin", "IU", "Market"]
    df2.columns = ["Age_cat", "gender", "defficiency", "IU_needed"]
    df = pd.concat([df1, df2], axis=1)
    df.to_csv('./mysite/DataBaseMerged_data.csv')


def process():
    df = pd.read_csv('./mysite/DataBaseMerged_data.csv')
    del df["ProductName"]
    labelencoder = LabelEncoder()
    df['TypeofVitamin'] = labelencoder.fit_transform(df['TypeofVitamin'])
    df['Market'] = labelencoder.fit_transform(df['Market'])
    df['gender'] = labelencoder.fit_transform(df['gender'])
    df['defficiency'] = labelencoder.fit_transform(df['defficiency'])
    for val in ["Age_cat", "gender", "defficiency", "IU_needed"]:
        df[val].fillna(df[val].mode()[0], inplace=True)
    df.to_csv('./mysite/Processed_Data.csv')


def get_product(age: int, gender: bool, defficiency: bool):
    if(os.path.isfile('./mysite/DataBaseMerged_data.csv')) == False:
        merge()
    if(os.path.isfile('./mysite/Processed_Data.csv')) == False:
        process()
    df = pd.read_csv('./mysite/Processed_Data.csv')
    model = LinearRegression().fit(df[['Age_cat', 'gender', 'defficiency']], df['IU_needed'])
    if age < 1:
        age_cat = 1
    elif 1 <= age < 70:
        age_cat = 2
    else:
        age_cat = 3
    predicted = model.predict([[age_cat, int(gender), int(defficiency)]])
    new_predicted = min(df['IU'].unique(), key=lambda x:abs(x - predicted))
    needed_iu = df.loc[df['IU'] == new_predicted]
    needed_iu = needed_iu[needed_iu['ProductPrice'] == needed_iu['ProductPrice'].min()]
    df1 = pd.read_csv('./mysite/DataBaseMerged_data.csv')
    needed_product = df1.loc[df1['ProductCode'] == needed_iu.iloc[0]['ProductCode']]
    data = {
        'Name': needed_product.iloc[0]['ProductName'],
        'Price': needed_product.iloc[0]['ProductPrice'],
        'Capsules': needed_product.iloc[0]['NumberOfCapsules'],
        'Type': needed_product.iloc[0]['TypeofVitamin'],
        'IU': needed_product.iloc[0]['IU'],
        'Market': needed_product.iloc[0]['Market']
    }
    return data


def test():
    return 'Test'


if __name__ == '__main__':
    print(get_product(18, False, True))

