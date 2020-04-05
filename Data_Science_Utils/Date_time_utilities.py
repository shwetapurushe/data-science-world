#creating order for the months in a year


#incase months have the whole name as is 'January' use string split and get first three letters

#unordered
df.month = df.month.str.capitalize()
df.day = df.day.str.capitalize()


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#creates a new column with categories 
df['months'] = pd.Categorical(df['month'], categories=months, ordered=True)


#useful for vizs
#order dataframe according to Months 
df.sort_values('months')


#Another way 
df["Month"] = pd.to_datetime(df.month, format='%b', errors='coerce').dt.month
df = df.sort_values(by="Month")
df.head()

