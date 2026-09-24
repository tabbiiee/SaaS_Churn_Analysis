--Inserting data to customers table
BULK INSERT raw.customers
FROM 'C:\Users\CHIRURE\OneDrive\Desktop\1_DATA\2_SaaS_churn_analysis\raw_data\customers.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO
--Inserting data to subscription table
BULK INSERT raw.subscriptions
FROM 'C:\Users\CHIRURE\OneDrive\Desktop\1_DATA\2_SaaS_churn_analysis\raw_data\subscriptions.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO