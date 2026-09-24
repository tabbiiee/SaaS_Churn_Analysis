-- Create customers table using the raw schema
CREATE TABLE raw.customers (
    customer_id VARCHAR(50),
    company_name VARCHAR(255),
    industry VARCHAR(100),
    country VARCHAR(100),
    city VARCHAR(100),
    company_size VARCHAR(50),
    signup_date VARCHAR(50),
    acquisition_channel VARCHAR(100)
);
-- Create subscription table using the raw schema
CREATE TABLE raw.subscriptions(
subscription_id VARCHAR(50),
customer_id VARCHAR(50),
subscription_plan VARCHAR(50),
billing_cycle VARCHAR(50),
start_date VARCHAR(50),
end_date VARCHAR(50),
monthly_price VARCHAR(50),
status VARCHAR(50),
cancellation_date VARCHAR(50),
cancellation_reason VARCHAR(255)
);
DROP TABLE raw.subscriptions;
GO
-- Create subscription table using the raw schema
CREATE TABLE raw.subscriptions(
subscription_id VARCHAR(50),
customer_id VARCHAR(50),
subscription_plan VARCHAR(50),
billing_cycle VARCHAR(50),
monthly_price VARCHAR(50),
start_date VARCHAR(50),
end_date VARCHAR(50),
status VARCHAR(50),
cancellation_date VARCHAR(50),
cancellation_reason VARCHAR(255)
);