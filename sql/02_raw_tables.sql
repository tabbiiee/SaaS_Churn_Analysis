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
-- Create payments table using the raw schema
CREATE TABLE raw.payments (
    payment_id VARCHAR(50),
    transaction_id VARCHAR(100),
    customer_id VARCHAR(50),
    subscription_id VARCHAR(50),
    payment_date VARCHAR(50),
    payment_method VARCHAR(100),
    amount VARCHAR(50),
    paid_amount VARCHAR(50),
    payment_status VARCHAR(100)
);
GO

-- Create support_tickets table using the raw schema
CREATE TABLE raw.support_tickets (
    ticket_id VARCHAR(50),
    customer_id VARCHAR(50),
    ticket_date VARCHAR(50),
    issue_category VARCHAR(100),
    priority VARCHAR(50),
    resolution_hours VARCHAR(50),
    ticket_status VARCHAR(50),
    customer_satisfaction VARCHAR(50)
);
GO

-- Create usage_activity table using the raw schema
CREATE TABLE raw.usage_activity (
    activity_id VARCHAR(50),
    customer_id VARCHAR(50),
    month VARCHAR(50),
    login_count VARCHAR(50),
    session_minutes VARCHAR(50),
    invoices_created VARCHAR(50),
    reports_generated VARCHAR(50),
    active_users VARCHAR(255),
    features_used VARCHAR(50)
);
GO

-- Create customer feedback table using the raw schema
CREATE TABLE raw.customer_feedback (
    feedback_id VARCHAR(50),
    customer_id VARCHAR(50),
    feedback_date VARCHAR(50),
    feedback_type VARCHAR(100),
    rating VARCHAR(50),
    sentiment VARCHAR(50),
    feedback_text VARCHAR(MAX)
);
GO