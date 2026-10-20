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

--Inserting data to payments table
BULK INSERT raw.payments
FROM 'C:\Users\CHIRURE\OneDrive\Desktop\1_DATA\2_SaaS_churn_analysis\raw_data\payments.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO

--Inserting data to support_tickets table
BULK INSERT raw.support_tickets
FROM 'C:\Users\CHIRURE\OneDrive\Desktop\1_DATA\2_SaaS_churn_analysis\raw_data\support_tickets.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO


--Inserting data to usage_activity table
BULK INSERT raw.usage_activity
FROM 'C:\Users\CHIRURE\OneDrive\Desktop\1_DATA\2_SaaS_churn_analysis\raw_data\usage_activity.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO

--Inserting data to customer_feedback table
BULK INSERT raw.customer_feedback
FROM 'C:\Users\CHIRURE\OneDrive\Desktop\1_DATA\2_SaaS_churn_analysis\raw_data\customer_feedback.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);
GO