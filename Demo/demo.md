# Demo of SQLite + Python

### Step 1: Design Database
Analyse the data and "normalize it".  
Chat-GPT explain it like this:  

First Normal Form (1NF): Think of this like making sure each piece of information has its own designated spot. In a table, each column should contain only one type of data. So, if you have a table for storing people's information, you wouldn't want one column for both their first name and last name mixed together.

Second Normal Form (2NF): This rule is about making sure that each piece of data relates directly to the primary key. Imagine the primary key as the main thing that identifies each row in your table. With 2NF, you want to break down your table into smaller parts so that each piece of data is directly related to that primary key. For instance, if you have a table for orders, you'd want to separate out customer information into its own table, linked by the customer ID.

Third Normal Form (3NF): This rule is like taking 2NF a step further. It's about removing any data that's not directly related to the primary key or solely dependent on the primary key. For example, if you have a table for products and their suppliers, you wouldn't want to include information about the supplier's address in the same table. Instead, you'd create a separate table just for suppliers and link it to the product table

## Step 2: Make an ERD
Using Lucid Charts. Three columns tables so we can define the Datatypes too. Rememeber the PK and FK and get the Cardinality right.


## Step 3: Make the Database in SQLite Studio
This is why we need to design it!

## Step 4: Test the Data
Write and test a bunch of queries that you think your user will need. Test them in the SQL Editor and make views if appropriate.

## Step 5: Write some Python
Write a basic interface to your database. Start with connecting and turn each "purpose" into a function to make a neat and tidy main loop.
