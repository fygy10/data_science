#IMPORT LIBRARIES
import pandas as pd
import numpy as np
import mysql.connector as sq
import re



#IMPORT DATA
mydata = ""
df = pd.read_csv(mydata)
df.info()


#CLEAN DATA
print(f'The shape before dropping rows with all values as NaN is:', df.shape)
df.dropna(how = 'all', inplace = True)
print(f'The shape after dropping rows with all values as NaN is:', df.shape)


#remove Nan values
print(f'The size of a column before dropping rows with any values as NaN is:', df['salary'].size)
df[['fte', 'salary', 'experience_district', 'experience_nj', 'experience_total']] = df[['fte', 'salary', 'experience_district', 'experience_nj', 'experience_total']].replace('[^\d.]', np.NAN, regex=True)
df.dropna(how = 'any', inplace=True)
print(f'The size of a column after dropping rows with any values as NaN is:', df['salary'].size)

df['fte'] = df['fte'].astype(float)
df[['salary', 'experience_district', 'experience_nj', 'experience_total', 'id']] = df[['salary', 'experience_district', 'experience_nj', 'experience_total', 'id']].astype(int)
print(df.dtypes)


#adjust index
df['id'] = range(1, len(df)+ 1)
print(len(df['id']))
print(df[['fte', 'salary', 'experience_district', 'experience_nj', 'experience_total', 'id']].isna().any())
df[['last_name', 'first_name', 'county', 'district', 'school', 'primary_job', 'certificate', 'subcategory', 'teaching_route', 'highly_qualified']] = df[['last_name', 'first_name', 'county', 'district', 'school', 'primary_job', 'certificate', 'subcategory', 'teaching_route', 'highly_qualified']].apply(lambda x: x.str.strip())


#remove whitespace
columns = ['last_name', 'first_name', 'county', 'district', 'school', 'primary_job', 'certificate', 'subcategory', 'teaching_route', 'highly_qualified']
changes = df['last_name'].astype(str).apply(lambda x: x.strip() != x).sum()
print(f'last_name has {changes} instances of removed whitespace')



#regex
columns = ['last_name', 'first_name', 'county', 'district', 'school', 'primary_job', 'certificate', 'subcategory', 'teaching_route', 'highly_qualified']
df[columns] = df[columns].apply(lambda x: re.sub(r'[^a-zA-Z0-9,_-]', '', x) if isinstance(x, str) else x)



#drop duplicates
df.drop_duplicates


#save cleaned to csv
df.to_csv(".csv", index = False)



#CONNECT TO MYSQL
mydb = sq.connect('', buffered = True)
mycursor = mydb.cursor()


mycursor.execute('show databases')
for db in mycursor:
    print(db)


#create database and table
mycursor.execute('CREATE SCHEMA ')


mycursor.execute('''
CREATE TABLE 
)
''')


mycursor.execute("""
            LOAD DATA INFILE 
        """)

mydb.commit()