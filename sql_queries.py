import pandas as pd          # importing pandas so we can work with data in table format (like Excel but in Python)
from db_config import get_connection     # importing our database connection function from db_config.py so we can talk to MySQL



# COMMON EXECUTION FUNCTION

def run(query):     # this is a reusable function — whenever we want to run any SQL query, we just call run() instead of writing the same connection code 30 times
    conn = get_connection()     # opening a connection to the MySQL database (like opening a door to get in)
    df = pd.read_sql(query, conn)     # running the SQL query and storing the result as a pandas DataFrame (a table we can work with in Python)
    conn.close()     # closing the database connection once we're done (like closing the door behind you)
    return df     # sending the result table back to whoever called this function


# SUMMARY

def summary():     # this function runs one special query that gives us the big-picture numbers for the dashboard header
    return run("""
        SELECT COUNT(*) AS total_transactions,     #-- counting how many rows (transactions) exist in total
               SUM(amount_paid) AS total_spent,    #-- adding up all the money spent across every transaction
               SUM(cashback) AS total_cashback,    #-- adding up all cashback earned across every transaction
               AVG(amount_paid) AS avg_transaction #-- calculating the average amount spent per transaction
        FROM expenses     #-- pulling all this from our expenses table
    """)



# CORE 15 QUERIES

# This is a dictionary — think of it like a named list where each item has a label (the query name) and a value (the actual SQL query)
# We store all 15 core queries here so app.py can just ask for them by name instead of writing SQL there
core_queries = {

"Total Spent by Category (in Rs)":     # query name — this is what shows as the chart title in the dashboard
"""SELECT category, SUM(amount_paid) AS total_spent     #-- picking category name and adding up money spent in each category
   FROM expenses GROUP BY category    # -- grouping rows so each category appears once with its total
   ORDER BY total_spent DESC""",     #-- sorting from highest to lowest so the biggest spender shows first


"Total Spent by Payment Mode":     # same idea but for payment methods (Cash, UPI, Credit Card etc.)
"""SELECT payment_mode, SUM(amount_paid) AS total_spent     #-- picking payment mode and totalling the spend for each
   FROM expenses GROUP BY payment_mode""",     #-- grouping so each payment mode appears once


"Monthly Spending":     # shows how much was spent each month so we can see trends over the year
"""SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent     #-- extracting month number from the date and totalling spend per month
   FROM expenses GROUP BY month ORDER BY month""",     #-- grouping by month and sorting Jan to Dec in order


"Cashback by Category":     # tells us which category earned the most cashback
"""SELECT category, SUM(cashback) AS total_cashback     #-- picking category and adding up all cashback earned in it
   FROM expenses GROUP BY category""",     #-- grouping so each category appears once


"Top 5 Transactions":     # fetches the 5 biggest individual purchases ever made
"""SELECT date, category, amount_paid     #-- we only need the date, what it was spent on, and how much
   FROM expenses ORDER BY amount_paid DESC LIMIT 5""",     #-- sorting by highest amount and taking only the top 5 rows


"Weekday vs Weekend":     # compares how much is spent on weekdays vs weekends
"""SELECT CASE WHEN DAYOFWEEK(date) IN (1,7)     #-- DAYOFWEEK returns 1 for Sunday and 7 for Saturday, so those are weekends
       THEN 'Weekend' ELSE 'Weekday' END AS day_type,     #-- labelling those days as 'Weekend' and everything else as 'Weekday'
       SUM(amount_paid) AS total_spent     #-- adding up the total money spent for each group
       FROM expenses GROUP BY day_type""",     #-- grouping so we get one row for Weekday and one row for Weekend


"Quarterly Spending":     # shows spending split into 4 quarters of the year (Jan-Mar, Apr-Jun, Jul-Sep, Oct-Dec)
"""SELECT QUARTER(date) AS quarter, SUM(amount_paid) AS total_spent     #-- extracting quarter number (1 to 4) from the date and totalling spend per quarter
   FROM expenses GROUP BY quarter ORDER BY quarter""",     #-- grouping by quarter and sorting from Q1 to Q4


"Highest Spending Month":     # finds the single month where the most money was spent
"""SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent     #-- extracting month and totalling its spend
   FROM expenses GROUP BY month ORDER BY total_spent DESC LIMIT 1""",     #-- sorting highest to lowest and taking only the #1 row


"Lowest Spending Month":     # same as above but finds the month with the least spending
"""SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent     #-- extracting month and totalling its spend
   FROM expenses GROUP BY month ORDER BY total_spent ASC LIMIT 1""",     #-- this time sorting lowest to highest and taking only the #1 row (the minimum)


"Average by Category":     # tells us the average transaction size in each category — useful to know if Healthcare transactions tend to be bigger than Food ones
"""SELECT category, AVG(amount_paid) AS avg_spent     #-- picking category and calculating the average spend per transaction in it
   FROM expenses GROUP BY category""",     #-- grouping so each category appears once


"Cashback Transactions":     # fetches the full details of every transaction that earned some cashback (cashback > 0)
"""SELECT * FROM expenses WHERE cashback > 0""",     #-- SELECT * means give me ALL columns, and WHERE cashback > 0 filters out the transactions with no cashback


"Above Average Transactions":     # finds all transactions where the amount is higher than the overall average — these are the "big spends"
"""SELECT * FROM expenses     #-- getting all columns for each qualifying transaction
   WHERE amount_paid > (SELECT AVG(amount_paid) FROM expenses)""",     #-- the inner query (inside brackets) first calculates the overall average, then the outer query picks only rows above it


"Top Category Share (%)":     # figures out which single category takes up the biggest percentage of total spending and what that percentage is
"""SELECT category,
       ROUND(SUM(amount_paid) /     #-- adding up money spent in this category
       (SELECT SUM(amount_paid) FROM expenses) * 100,2) AS percentage     #-- dividing by the grand total of all spending and multiplying by 100 to get a percentage, rounded to 2 decimal places
       FROM expenses GROUP BY category     #-- doing this calculation for every category
       ORDER BY percentage DESC LIMIT 1""",     #-- sorting highest percentage first and taking only the top 1 (the winner)


"Payment Mode Cashback":     # shows how much cashback was earned through each payment method
"""SELECT payment_mode, SUM(cashback) AS total_cashback     #-- picking payment mode and totalling cashback earned with it
   FROM expenses GROUP BY payment_mode""",     #-- grouping so each payment mode appears once


"Transactions Per Category":     # counts how many times each category was used — tells us which category is used most frequently
"""SELECT category, COUNT(*) AS total_transactions     #-- picking category and counting how many rows (transactions) belong to it
   FROM expenses GROUP BY category"""     #-- grouping so each category appears once with its count
}


# ADVANCED 15 QUERIES

# Same dictionary structure as core_queries but these are more complex, deeper analysis queries
advanced_queries = {

"Daily Average per Month":     # instead of total spending per month, this looks at the average transaction size each month — tells us if spending habits change throughout the year
"""SELECT MONTH(date) AS month,
       AVG(amount_paid) AS daily_avg     #-- calculating average transaction amount for each month (not sum, but average)
   FROM expenses GROUP BY month ORDER BY month""",     #-- grouping by month and sorting Jan to Dec


"Max Transaction per Category":     # finds the single biggest purchase ever made within each category
"""SELECT category, MAX(amount_paid) AS max_spent     #-- picking category and finding the highest single transaction amount in it
   FROM expenses GROUP BY category""",     #-- grouping so each category appears once


"Min Transaction per Category":     # opposite of above — finds the smallest purchase ever made within each category
"""SELECT category, MIN(amount_paid) AS min_spent     #-- picking category and finding the lowest single transaction amount in it
   FROM expenses GROUP BY category""",     #-- grouping so each category appears once


"Total Cashback Percentage (%)":     # calculates what percentage of all money spent was returned as cashback overall
"""SELECT ROUND(SUM(cashback) /     #-- adding up all cashback earned
   SUM(amount_paid) * 100,2) AS cashback_percent     #-- dividing by total money spent, multiplying by 100 to get a percentage, rounded to 2 decimal places
   FROM expenses""",     #-- no grouping needed because we want one single number for the entire dataset


"Spending Trend by Year":     # adds up total spending per year — since our data is all 2025, this returns one bar showing the full year total
"""SELECT YEAR(date) AS year,     #-- extracting the year from the date
   SUM(amount_paid) AS total_spent    # -- totalling all spending in that year
   FROM expenses GROUP BY year""",     #-- grouping by year (will be just 2025 in our case)


"Weekend Average":     # calculates the average transaction size on weekends only — lets us compare with weekday average
"""SELECT AVG(amount_paid) AS avg_weekend     #-- calculating average amount paid across all weekend transactions
   FROM expenses WHERE DAYOFWEEK(date) IN (1,7)""",     #-- filtering to only Saturday (7) and Sunday (1) transactions


"Weekday Average":     # same as above but for weekdays only
"""SELECT AVG(amount_paid) AS avg_weekday     #-- calculating average amount paid across all weekday transactions
   FROM expenses WHERE DAYOFWEEK(date) NOT IN (1,7)""",     #-- filtering to everything that is NOT Saturday or Sunday


"Top 3 Categories":     # finds the 3 categories where the most money was spent — useful for identifying where to cut costs
"""SELECT category, SUM(amount_paid) AS total_spent     #-- picking category and adding up total spent in it
   FROM expenses GROUP BY category     #-- grouping so each category appears once
   ORDER BY total_spent DESC LIMIT 3""",     #-- sorting highest to lowest and keeping only the top 3


"Transactions with No Cashback":     # counts how many transactions earned zero cashback — tells us how many purchases gave no reward
"""SELECT COUNT(*) AS total_no_cashback     #-- counting the number of rows where cashback was 0
   FROM expenses WHERE cashback = 0""",     #-- filtering to only rows where the cashback column is exactly 0


"Highest Cashback Transaction":     # fetches the full details of the single transaction that earned the most cashback ever
"""SELECT * FROM expenses     #-- getting all columns for this transaction
   ORDER BY cashback DESC LIMIT 1""",     #-- sorting by cashback highest first and taking only the top row (the biggest cashback earner)


"Payment Mode Efficiency Ratio (%)":     # calculates what percentage of money spent through each payment mode came back as cashback — tells us which payment method is the most rewarding
"""SELECT 
payment_mode,     #-- picking the payment mode name
ROUND(SUM(cashback) / SUM(amount_paid) * 100, 2) AS cashback_efficiency_percent     #-- dividing total cashback earned by total money spent for that mode, multiplied by 100 to get %, rounded to 2 decimal places
FROM expenses
GROUP BY payment_mode""",     #-- doing this calculation for each payment mode separately


"Spending Distribution":     # groups transactions into price buckets of Rs.500 each and counts how many transactions fall in each bucket — gives a histogram-like view of spending habits
"""SELECT FLOOR(amount_paid/500)*500 AS range_start,     #-- FLOOR rounds down to the nearest 500, so Rs.1,234 becomes Rs.1,000 — this is the start of the Rs.500 bucket
   COUNT(*) AS frequency     #-- counting how many transactions fall into each bucket
   FROM expenses GROUP BY range_start""",     #-- grouping so each price bucket appears once with its count


"Most Used Payment Mode":     # finds which payment method (Cash, UPI, etc.) was used the most number of times
"""SELECT payment_mode, COUNT(*) AS total     #-- picking payment mode and counting how many transactions used it
   FROM expenses GROUP BY payment_mode     #-- grouping so each mode appears once
   ORDER BY total DESC LIMIT 1""",     #-- sorting highest count first and keeping only the #1 most used mode


"Monthly Cashback":     # shows how much cashback was earned each month — lets us spot which months were best for rewards
"""SELECT MONTH(date) AS month,     #-- extracting the month number from the date
   SUM(cashback) AS total_cashback     #-- adding up all cashback earned in that month
   FROM expenses GROUP BY month ORDER BY month""",     #-- grouping by month and sorting Jan to Dec in order


"High-Value Transaction Ratio (%)":     # calculates what percentage of all transactions were "high value" meaning above the overall average spend
"""SELECT 
ROUND(
    SUM(CASE      #-- going through every row one by one
        WHEN amount_paid > (SELECT AVG(amount_paid) FROM expenses)     #-- the inner query calculates the overall average first; then for each row we check if this transaction is above that average
        THEN 1 ELSE 0 END     #-- if yes, count it as 1; if no, count it as 0
    ) / COUNT(*) * 100, 2     #-- adding up all the 1s (high-value transactions), dividing by total transactions, multiplying by 100 to get a percentage, rounded to 2 decimal places
) AS high_value_percent
FROM expenses"""     #-- running this across the entire dataset to get one single percentage number
}
