import re
import ssl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from pylab import rcParams
from urllib.request import urlopen
from bs4 import BeautifulSoup 

url = "http://www.hubertiming.com/results/2017GPTR10K"
ssl_context = ssl._create_unverified_context()
html = urlopen(url, context=ssl_context)

soup = BeautifulSoup(html, 'lxml')
type(soup)

# Get the title
title = soup.title
print(title)

#Print out the text
text = soup.get_text()
print(text)

soup.find_all('a')
# To extract all hyperlinks from the webpage
all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))
#To print out table rows only, pass the 'tr' argument in soup.find_all()
#Slicing to print
rows = soup.find_all('tr')
print(rows[:10])

#convert Table Data to a python Pandas dataframe
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)

print(clean2)
type(clean2)

df = pd.DataFrame(list_rows)
df1 = df[0].str.split(',', expand=True)
df1[0] = df1[0].str.strip('[')
df1.head(10)

col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
df2 = pd.DataFrame(all_header)
df3 = df2[0].str.split(',', expand=True)
frames = [df3, df1]
df4 = pd.concat(frames)
df5 = df4.rename(columns=df4.iloc[0])
df6 = df5.dropna(axis=0, how='any')
df7 = df6.drop(df6.index[0])
df7.rename(columns={'[Place': 'Place'}, inplace=True)
df7.rename(columns={' Team]': 'Team'}, inplace=True)
df7['Team'] = df7['Team'].str.strip(']')

df7.columns = [col.strip() for col in df7.columns]


time_list = df7['Time'].tolist()
time_mins = []
for i in time_list:
   time_parts = i.split(':')
   if len(time_parts) == 3:
        h, m, s = time_parts
        math = (int(h) * 3600 + int(m) * 60 + int(s))/60
   elif len(time_parts) == 2:
        m, s = time_parts
        math = (int(m) * 60 + int(s))/60
   time_mins.append(math)

df7['Runner_mins'] = time_mins
df7.head()

# Descriptive statistics
print(df7.describe(include=[np.number]))

# Boxplot
rcParams['figure.figsize'] = 15, 5
df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])

# Distribution plot
x = df7['Runner_mins']
ax = sns.displot(x, kind='hist', kde=True, rug=False, color='m', bins=25)
plt.show()

# Separate distributions for males and females
f_fuko = df7.loc[df7['Gender']==' F']['Runner_mins']
m_fuko = df7.loc[df7['Gender']==' M']['Runner_mins']
sns.histplot(f_fuko, kde=True, color='m', bins=25, edgecolor='black', label='Female')
sns.kdeplot(m_fuko, color='b', label='Male')
plt.legend(title='Gender')



# Descriptive statistics by gender
g_stats = df7.groupby("Gender", as_index=True).describe()
print(g_stats)

# Boxplot by gender
df7.boxplot(column='Runner_mins', by='Gender')
plt.ylabel('Chip Time')
plt.suptitle("")