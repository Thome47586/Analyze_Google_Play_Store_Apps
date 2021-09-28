
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load data
GooglePlayStore = pd.read_csv('/content/gdrive/MyDrive/Week3/GooglePlayStore/Google-Playstore.csv')



############################
### 1. Basic Exploration ###
############################

# Overview 
GooglePlayStore.head()

# Review info
GooglePlayStore.info()

# Check NULL
GooglePlayStore.isnull().sum()

# Overview numerical features of the dataset 
GooglePlayStore.describe()





#####################
### 2. Clean Data ###
#####################

"""2.1 Remove duplicated data"""
GooglePlayStore.duplicated().sum()


"""2.2 Check and change datatype"""
GooglePlayStore.info()


"""2.3 Working with Missing Values"""
GooglePlayStore.isna().sum()

# Replace "unknown" to NULL
GooglePlayStore[['App Name','Installs','Minimum Installs','Currency','Size','Developer Id']] = GooglePlayStore[['App Name','Installs','Minimum Installs','Currency','Size','Developer Id']].fillna('Unknown')

GooglePlayStore.describe()

# Replace ' ' = '_' name of columns
GooglePlayStore.rename(lambda x: x.lower().strip().replace(' ', '_'), axis='columns', inplace=True)


"""2.5 Drop columns """
# Take columns
GooglePlayStore.columns

cols_drop = ['app_id', 'minimum_android', 'developer_website', 'developer_email', 'privacy_policy', 'editors_choice']

# Drop unnecessary columns from cols_drop
GooglePlayStore.drop(cols_drop, axis='columns', inplace=True)

# Check: No output means passed!
assert GooglePlayStore.columns.all() not in cols_drop

# Specifying the datetime format significantly reduces conversion time
GooglePlayStore['released'] = pd.to_datetime(GooglePlayStore['released'], format='%b %d, %Y', errors='coerce')


"""2.6 Convert size to float"""

# Strip of all text and convert to numeric
GooglePlayStore['size'] = pd.to_numeric(GooglePlayStore['size'].str.replace(r'[a-zA-Z]+', ''), errors='coerce')

# Check: No output means passed!
assert GooglePlayStore['size'].dtype == 'float64'





##########################################
###  3 Exploratory Data Analysis (EDA) ###
##########################################

"""3.1 Overview number of apps"""

# Creat column year, month, month_year trong Google Play Store
GooglePlayStore['year'] = GooglePlayStore['released'].dt.year
GooglePlayStore['month'] = GooglePlayStore['released'].dt.month
GooglePlayStore['month_year'] = pd.to_datetime(GooglePlayStore['released']).dt.to_period('M')
GooglePlayStore.info()

# Creat month_app: count app_name by month/year
month_app = GooglePlayStore.groupby(['year','month'])['app_name'].count().reset_index()
month_app.rename(columns={'app_name':'count_app'},inplace=True)
month_app.head()


# Show plot count_app by month/year
plt.style.use('seaborn-bright')
plt.figure(figsize=(20,8))
sns.lineplot(data=month_app,x='month',y='count_app',color='tab:red',hue='year')
plt.show()



# Creat Google Play Store before 2019
gps_2019 = GooglePlayStore[(GooglePlayStore['year'] <= 2019)]
gps_2019.shape

# Creat Google Play Store after 2019
gps2020_ = GooglePlayStore[(GooglePlayStore['year'] > 2019)]
gps2020_.shape

# Count app by year
year_app = GooglePlayStore.groupby('year')['app_name'].count().reset_index()
year_app.rename(columns = {'app_name':'count_app'},inplace=True)
year_app



# Show plot of count_app by year (2010-2021)
avg_year_app = year_app['count_app'].mean()
plt.figure(figsize=(10,6))

sns.barplot(data=year_app,x='year',y='count_app',color='tab:blue')
plt.axhline(avg_year_app, color='tab:red', linestyle='--')

plt.show()

#########################################################################################################################################



""" 3.2 Top 10 Categories most quantity"""

# Number of categories have quantity more than average
count_cate = GooglePlayStore.groupby('category')['app_name'].count().reset_index()
count_cate.rename(columns={'app_name': 'count_categories'},inplace=True)
avg_cate = count_cate['count_categories'].mean()
top_higer_avg_cate = count_cate[(count_cate['count_categories'] > avg_cate)]
top_higer_avg_cate['category'].count()

# Rate top_higer_avg_cate vs count_cate
top_higer_avg_cate['count_categories'].count()/count_cate['count_categories'].count()

"""Take out Top 10 and EDA"""

# Top 10 Categories have the most quantity apps (take from top_higer_avg_cate)
top10_cate_dict = ['Education','Music & Audio','Tools','Business','Entertainment','Lifestyle','Books & Reference','Personalization','Health & Fitness','Productivity','Shopping']

count_cate = GooglePlayStore.groupby('category')['app_name'].count().reset_index() # Count app by Category
top10_cate = count_cate[(count_cate['category'].isin(top10_cate_dict))] # Filter in top10_cate_dict
count_cate.rename(columns={'app_name': 'count_categories'},inplace=True) # Rename app_name to count_categories of count_cate
top10_cate.rename(columns={'app_name': 'count_categories'},inplace=True) # Rename app_name to count_categories of top10_cate
top10_cate

top10_cate['mean_categorys'] = top10_cate['count_categories'] / top10_cate['count_categories'].sum()

# Rate of Top 10 Categories with the most number of Apps on Google Play Store
top10_cate['count_categories'].count()/count_cate['count_categories'].count()


# Distribution chart of Top 10 Categories
avg_cate = count_cate['count_categories'].mean()
plt.style.use('tableau-colorblind10')
plt.figure(figsize=(15,5))
sns.barplot(data=top10_cate,x='category',y='count_categories',color='tab:blue',
            order = top10_cate_dict)
plt.axhline(avg_cate, color='tab:red', linestyle='--')
plt.show()

# Check how the percentage  of Education Category
top10_cate[(top10_cate['category'] == 'Education')]['count_categories'].sum() / top10_cate['count_categories'].sum()

#########################################################################################################################################



""" 3.3 Explore installation of the Top 10 """

# Mean of maximum_installs  
install_mean_cate = GooglePlayStore['maximum_installs'].mean()
install_mean_cate

# Creat install_top10_cate with mean of ['maximum_installs','rating','rating_count'] per 'category'
install_top10_cate = GooglePlayStore.groupby('category')['maximum_installs','rating','rating_count','price'].mean().reset_index()
install_top10_cate = install_top10_cate[install_top10_cate['category'].isin(top10_cate_dict)]
install_top10_cate

# Creat top10_cate_final by inner join 'install_top10_cate' & top10_cate
top10_cate_final = pd.merge(left=top10_cate,
                     right=install_top10_cate,
                     how='inner',
                     on='category')
                     
top10_cate_final

# Show top10_cate_final
plt.figure(figsize=(20,5))
plt.subplot(211) 
sns.barplot(data=top10_cate_final,x='category',y='count_categories',color='tab:blue',
            order=top10_cate_dict) # Show count_categories per category
plt.twinx()
sns.lineplot(data=top10_cate_final,x='category',y='maximum_installs',color='tab:red') # Show maximum_installs per category

plt.subplot(212) 
sns.barplot(data=top10_cate_final,x='category',y='rating',color='tab:blue',
            order=top10_cate_dict) # Show rating per category
plt.twinx()
sns.lineplot(data=top10_cate_final,x='category',y='rating_count',color='tab:red') # Show rating_count per category
plt.show


# Distribution chart of Top 10 Categories
avg_cate = count_cate['count_categories'].mean()
install_count_cate = GooglePlayStore['maximum_installs'].mean()
plt.style.use('tableau-colorblind10') # Use style 'tableau-colorblind10'
plt.figure(figsize=(15,10))

# Show count_categories per category
plt.subplot(211)
sns.barplot(data=top10_cate,x='category',y='count_categories',color='tab:blue',
            order = top10_cate_dict) 
plt.axhline(avg_cate, color='tab:red', linestyle='--')

# Show maximum_installs per category
plt.subplot(212)
sns.barplot(data=install_top10_cate,x='category',y='maximum_installs',color='tab:blue',
            order = top10_cate_dict) 
plt.axhline(install_count_cate, color='tab:red', linestyle='--')
plt.show()



# Creat dictionary ['Productivity','Tools','Education']
tool_productivity_edu_dict = ['Productivity','Tools','Education']

gps_2019.shape

# Filter gps_2019 have category that is tool_productivity_edu_dict
gps_2019_tool_productivity_edu =  gps_2019[(gps_2019['category'].isin(tool_productivity_edu_dict))]
gps_2019_tool_productivity_edu.shape

gps_2019_tool_productivity_edu.head()

# Creat count_gps_2019_tool_productivity_edu  (before 2019)
count_gps_2019_tool_productivity_edu = gps_2019_tool_productivity_edu.groupby('category')['app_name'].count().reset_index()
count_gps_2019_tool_productivity_edu.rename(columns={'app_name':'count_app'},inplace=True)
count_gps_2019_tool_productivity_edu



gps2020_.shape

gps2020__tool_productivity_edu =  gps2020_[(gps2020_['category'].isin(tool_productivity_edu_dict))]
gps2020__tool_productivity_edu.shape

# Creat count_gps2020__tool_productivity_edu (after 2019)
count_gps2020__tool_productivity_edu = gps2020__tool_productivity_edu.groupby('category')['app_name'].count().reset_index()
count_gps2020__tool_productivity_edu.rename(columns={'app_name':'count_app'},inplace=True)
count_gps2020__tool_productivity_edu

# Distribution chart of Top 2 Categories
avg_year_app_2019_tpe = count_gps_2019_tool_productivity_edu['count_app'].mean() 
avg_year_app_2020__tpe = count_gps2020__tool_productivity_edu['count_app'].mean() 
avg_year_app_2019 = gps_2019.groupby('category')['app_name'].count().mean() 
avg_year_app_2020_ = gps2020_.groupby('category')['app_name'].count().mean()



plt.style.use('tableau-colorblind10')
plt.figure(figsize=(15,10))

# Show count_gps_2019_tool_productivity_edu: count_app by category
plt.subplot(121)
sns.barplot(data=count_gps_2019_tool_productivity_edu,x='category',y='count_app',color='tab:blue',
            order = tool_productivity_edu_dict) 
plt.title('Education, Tools & Productivity before 2019')
plt.axhline(avg_year_app_2019_tpe, color='tab:orange', linestyle='--')
plt.axhline(avg_year_app_2019, color='tab:red', linestyle='--') 
plt.ylim(0,170000)

# Show count_gps2020__tool_productivity_edu: count_app by category
plt.subplot(122)
sns.barplot(data=count_gps2020__tool_productivity_edu,x='category',y='count_app',color='tab:blue',
            order = tool_productivity_edu_dict) 
plt.title('Education, Tools & Productivity after 2019')
plt.ylim(0,170000)
plt.axhline(avg_year_app_2020__tpe, color='tab:orange', linestyle='--')
plt.axhline(avg_year_app_2020_, color='tab:red', linestyle='--') # show mean after 2019

plt.show()





"""Rating Top 10"""

# Filter gps_notnull_having 'ratng' is not null
gps_notnull_rate = GooglePlayStore[(pd.notnull(GooglePlayStore['rating']))]
gps_notnull_rate.head()

gps_notnull_rate.isna().sum()

# Filter gps_notnull_rate_top10 (not null & Top 10)
gps_notnull_rate_top10 = gps_notnull_rate[gps_notnull_rate['category'].isin(top10_cate_dict)]
gps_notnull_rate_top10.shape

# Creat rate_app_top10 (count_app)
rate_app_top10 = gps_notnull_rate_top10.groupby('rating')['app_name'].count().reset_index()
rate_app_top10.rename(columns={'app_name':'count_app'},inplace=True)
rate_app_top10 = rate_app_top10[(rate_app_top10['rating'] > 0)]
rate_app_top10



# Show distribution of rating & count_app
plt.figure(figsize=(15,5))
sns.barplot(data=rate_app_top10,x='rating',y='count_app')
plt.show()

# Creat rate_app_top10 (count_app)
rate_count_app_top10 = gps_notnull_rate_top10.groupby('rating')['rating_count'].sum().reset_index()
rate_count_app_top10 = rate_count_app_top10[(rate_count_app_top10['rating'] > 0)]
rate_count_app_top10

# Show distribution of rating & rating_count
plt.figure(figsize=(15,5))
sns.barplot(data=rate_count_app_top10,x='rating',y='rating_count')
plt.show()





# Creat series free_cate
free_cate = GooglePlayStore.groupby('free')['app_name'].count()
free_cate

plt.style.use('tableau-colorblind10')
pie, ax = plt.subplots(figsize=[10,6])
labels = free_cate.keys()
plt.pie(x = free_cate, autopct="%.1f%%", explode=[0.05]*2, labels=labels, pctdistance=0.5)
plt.title("The percentage of free and paid apps", fontsize=14);
plt.show()

avg_price = GooglePlayStore['price'].mean()
plt.figure(figsize=(15,5))
sns.barplot(data=install_top10_cate,x='category',y='price',color='tab:blue',
            order=top10_cate_dict)
plt.axhline(avg_price, color='tab:red', linestyle='--')
plt.show()



# Create a mask for paid apps
is_paid = (GooglePlayStore['price'] > 0) & (GooglePlayStore['price'] < 12)
price_top10_cate = GooglePlayStore[is_paid & GooglePlayStore['category'].isin(top10_cate_dict) ]
price_top10_cate

# Creat price_top10_cate_2020 (Price of Top10 after 2019)
price_top10_cate_2020 = gps2020_[is_paid & gps2020_['category'].isin(top10_cate_dict) ]
price_top10_cate_2020

# Creat price_top10_cate__2019 (Price of Top10 before 2019)
price_top10_cate__2019 = gps_2019[is_paid & gps_2019['category'].isin(top10_cate_dict) ]
price_top10_cate__2019



# Show price_top10_cate_2020 & price_top10_cate__2019
plt.figure(figsize=(15,8))
plt.subplot(311)
sns.boxplot(data=price_top10_cate[is_paid], x='category',y='price',
order = top10_cate_dict)
plt.title('Price of Top 10 Categories')
plt.subplots_adjust(top=1.6)

plt.subplot(312)
sns.boxplot(data=price_top10_cate__2019[is_paid], x='category',y='price',
order = top10_cate_dict)
plt.title('Price before 2019')
plt.subplots_adjust(top=1.6)

plt.subplot(313)
sns.boxplot(data=price_top10_cate_2020[is_paid], x='category',y='price',
order = top10_cate_dict)
plt.title('Price after 2019')
plt.subplots_adjust(top=1.6)
plt.show()
