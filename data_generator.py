from faker import Faker
from datetime import datetime
from db_config import get_connection

fake = Faker()     #initializing Faker() class to an object

TOTAL_RECORDS = 300     #total number of records we want
START_YEAR = 2025     #starting year of transaction

CATEGORIES = [        #defining categories from which one should be selected 
    "Groceries", "Food", "Transport", "Travel",
    "Entertainment", "Shopping", "Bills",
    "Healthcare", "Education", "Subscriptions"
]

PAYMENT_MODES = [        #defining payment modes from which one should be selected 
    "Cash", "UPI", "Debit Card", "Credit Card"
]

# Creating tables in SQL
def create_table():
    connection = get_connection()     #creating an object to connect with the database 
    cursor = connection.cursor()     ##creating a cursor object to interact with the database and allowing python to excute queries in the database
    create_query = """        #Query for creating a table in SQL 
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        category VARCHAR(100),
        payment_mode VARCHAR(50),
        description VARCHAR(255),
        amount_paid DECIMAL(10,2),
        cashback DECIMAL(10,2)
    );
    """
    cursor.execute(create_query)    #executing the query
    connection.commit()    #Saving the chn=anges made
    cursor.close()    #closing the connection
    connection.close()     #closing the SQL connection

# Function to generate random date across 12 months using Faker
def random_date():
    start_date = datetime(START_YEAR, 1, 1)
    end_date = datetime(START_YEAR, 12, 31)
    return fake.date_between(start_date=start_date, end_date=end_date)

# Generating fake data using Faker
def generate_data():
    data =     [] #list 
    for _ in range(TOTAL_RECORDS):
        date = random_date()     #Generating random date using faker
        category = fake.random_element(elements=CATEGORIES)       #Selecting random element from Categories list
        payment_mode = fake.random_element(elements=PAYMENT_MODES)     #Selecting random element from Payment modes list
        description = fake.sentence(nb_words=5)     #Generating fake description in 5 words using faker
        amount = round(fake.pyfloat(min_value=100, max_value=5000, right_digits=2), 2)      # Generating random float 2 digit amount value ranging from 100-5000
       
        cashback = (        
            round(amount * fake.pyfloat(min_value=0.01, max_value=0.1, right_digits=2), 2)    # Generating random float 2 digit cashback value ranging from 0.01-0.1
            if fake.boolean(chance_of_getting_true=30)    # Generating random 30% chance of cashback using Faker
            else 0.00
        )
        data.append((date, category, payment_mode, description, amount, cashback))    #storing generated data into the list 'data'
    return data

# Inserting Data into the Database
def insert_data(data):
    connection = get_connection()     #connecting with SQL
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO expenses (date, category, payment_mode, description, amount_paid, cashback)    #inserting the fake data generated into its corresponding columns
    VALUES (%s, %s, %s, %s, %s, %s)        #placeholder to substitue the generated data into respective column order
    """
    cursor.executemany(insert_query, data)    #Executing the query multiple times
    connection.commit()    #saving the changes made
    cursor.close()    #closing the connection
    connection.close()

# Executing all functions
if __name__ == "__main__":
    print("Creating table if not exists")
    create_table()
    print("Generating fake expense data")
    data = generate_data()
    print("Inserting data into database")
    insert_data(data)
    print(" 300 records successfully inserted into expense_tracker.expenses")
