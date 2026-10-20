/*
============================================================
PROJECT: LedgerFlow SaaS Churn Analysis
FILE: 04_profile_raw_data.sql
PURPOSE:
    Profile raw customer data before cleaning.

OBJECTIVES:
    - Identify missing values
    - Identify duplicate customer IDs
    - Identify inconsistent categorical values
    - Identify formatting issues
    - Understand the quality of the raw dataset

SOURCE:
    raw.customers

OUTPUT:
    Profiling results used to design the cleaning logic.

============================================================
*/
-- =================================================
-- CUSTOMERS: RAW DATA PROFILING
-- =================================================
-- ==================================================
-- CUSTOMERS: BASIC STRUCTURE
-- =================================================
SELECT TOP 10 *
FROM raw.customers

SELECT
    COUNT (*) AS total_rows,
    COUNT (DISTINCT customer_id) AS unique_customer
FROM raw.customers
-- ==================================================
-- CUSTOMERS: IDENTIFYING MISSINNG VALUES
-- =================================================
SELECT
    SUM(
        CASE 
            WHEN customer_id IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_customer_id,
     SUM(
        CASE 
            WHEN company_name IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_company_name,
     SUM(
        CASE 
            WHEN industry IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_industry,
     SUM(
        CASE 
            WHEN country IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_country,
     SUM(
        CASE 
            WHEN city IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_city,
     SUM(
        CASE 
            WHEN company_size IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_company_size,
     SUM(
        CASE 
            WHEN signup_date IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_signup_date,
     SUM(
        CASE 
            WHEN acquisition_channel IS NULL THEN 1 
            ELSE 0 
        END
     ) AS missing_acquisition_channel
FROM raw.customers;
-- ==================================================
-- CUSTOMERS: CHECKING DUPLICATES
-- =================================================
SELECT TOP 10 * FROM raw.customers
SELECT 
    customer_id,
    COUNT(customer_id) AS occurrence_count
FROM raw.customers
GROUP BY customer_id
HAVING COUNT(customer_id) > 1;

-- Inspect records with duplicated customer IDs
SELECT *
FROM raw.customers
WHERE customer_id IN (
    SELECT 
        customer_id
    FROM raw.customers
    GROUP BY customer_id
    HAVING COUNT(customer_id) > 1
    )
ORDER BY customer_id

-- =================================================
-- CUSTOMERS: DUPLICATE FINDINGS
-- =================================================
-- 20 customer IDs appear more than once.
-- The duplicated records are exact duplicates.
-- These duplicates will be removed during the cleaning stage.

-- =================================================
-- CUSTOMERS: CATEGORICAL CHECK - INDUSTRY
-- =================================================

SELECT DISTINCT industry
FROM raw.customers;

-- FINDING:
-- Industry values are consistently formatted.
-- No capitalization or whitespace inconsistencies were identified.

SELECT TOP 10 * FROM raw.customers
-- =================================================
-- CUSTOMERS: CATEGORICAL CHECK - ACQUISITION CHANNEL
-- =================================================

SELECT DISTINCT acquisition_channel
FROM raw.customers;

SELECT 
    acquisition_channel,
    COUNT (*) AS record_count
FROM raw.customers
GROUP BY acquisition_channel
ORDER BY acquisition_channel

-- FINDING:
-- Acquisition channel values are not consistently formatted.
-- Capitalization and whitespace inconsistencies were identified.
-- These values will be standardized during the cleaning stage.

-- =================================================
-- CUSTOMERS: CATEGORICAL CHECK - CITY
-- =================================================

SELECT DISTINCT city
FROM raw.customers;

-- FINDING:
-- City values contain 50 missing values.
-- Several city names contain spelling errors or inconsistent formatting.
-- Examples include 'Nakur', 'Mombassa', 'Acra', 'Kampalaa' ,'Kisum' and 'Lagoss'.
-- These values will be standardized during the cleaning stage.
SELECT DISTINCT city
FROM raw.customers
WHERE city LIKE '% ';

-- FINDING:
-- One city value contains trailing whitespace.

SELECT DISTINCT city
FROM raw.customers
WHERE city LIKE ' %';

-- FINDING:
-- No city values contain leading whitespace.

-- =================================================
-- CUSTOMERS: CATEGORICAL CHECK - COMPANY SIZE
-- =================================================

SELECT DISTINCT company_size
FROM raw.customers;

-- FINDING:
-- Company size values are consistently formatted as employee ranges.
-- No categorical inconsistencies were identified.

-- =================================================
-- CUSTOMERS: CATEGORICAL CHECK - COUNTRY
-- =================================================

SELECT DISTINCT country
FROM raw.customers;

-- FINDING:
-- Country values are consistently formatted.
-- No categorical inconsistencies were identified.
SELECT DISTINCT country
FROM raw.customers
WHERE country LIKE '% ';

-- FINDING:
-- No country value contains trailing whitespace.

SELECT DISTINCT country
FROM raw.customers
WHERE country LIKE ' %';

-- FINDING:
-- No country values contain leading whitespace

-- =================================================
-- CUSTOMERS: DATE FORMAT CHECK
-- =================================================

-- YYYY-MM-DD
SELECT COUNT(*) AS hyphen_dates
FROM raw.customers
WHERE signup_date LIKE '%-%';


-- MM/DD/YYYY
SELECT COUNT(*) AS slash_dates
FROM raw.customers
WHERE signup_date LIKE '%/%';


-- Mon DD, YYYY
SELECT COUNT(*) AS month_name_dates
FROM raw.customers
WHERE signup_date LIKE '___ __, ____';


-- FINDING:
-- signup_date contains multiple date formats.
-- YYYY-MM-DD and MM/DD/YYYY formats are present,
-- along with 28 records using the Mon DD, YYYY format.
-- All 5,020 records are accounted for across these formats.
-- Date values will be standardized during the cleaning stage.
/*
=================================================
-- CUSTOMERS: OVERALL PROFILING FINDINGS
=================================================

-- 20 customer IDs are duplicated, resulting in 20
-- extra exact-duplicate records (40 rows are involved
-- in the duplicated pairs).

-- Industry values are formatted consistently, with
-- no inconsistencies identified.

-- Acquisition channel values are not formatted
-- consistently. Capitalization and whitespace
-- inconsistencies were identified

-- Company size values are formatted consistently.

-- City values contain missing values, trailing
-- whitespace, and several spelling errors.

-- 50 city values contain missing values.

-- Country values are formatted consistently, with
-- no inconsistencies identified.

-- signup_date contains three different date formats:
-- YYYY-MM-DD, MM/DD/YYYY, and Mon DD, YYYY.
============================================================
END OF CUSTOMERS PROFILING
============================================================
=================================================
*/
-- =================================================
-- SUBSCRIPTIONS: RAW DATA PROFILING
-- =================================================
-- =============================================
-- SUBSCRIPTIONS: BASIC STRUCTURE
-- =============================================

SELECT TOP 10 *
FROM raw.subscriptions;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT subscription_id) AS distinct_subscription_ids
FROM raw.subscriptions;
=================================================
-- SUBSCRIPTIONS: CHECKING FOR DUPLICATES
=================================================
SELECT 
    subscription_id,
    COUNT(*) AS total_record
FROM raw.subscriptions
GROUP BY subscription_id
HAVING  COUNT(*) > 1

SELECT *
FROM raw.subscriptions
WHERE subscription_id IN(
    SELECT 
        subscription_id
    FROM raw.subscriptions
    GROUP BY subscription_id
    HAVING  COUNT(*) > 1
)
ORDER BY subscription_id

/* FINDINGS

-- 15 subscription IDs are duplicated, resulting
-- in 15 extra records.

-- The duplicated records are exact duplicates across
-- all columns.

-- The duplicate records will be removed during the
-- cleaning stage.
=================================================
*/
SELECT 
    SUM(CASE WHEN subscription_id IS NULL THEN 1 ELSE 0 END) AS missing_subscription_id,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id,
    SUM(CASE WHEN subscription_plan IS NULL THEN 1 ELSE 0 END) AS missing_subscription_plan,
    SUM(CASE WHEN billing_cycle IS NULL THEN 1 ELSE 0 END) AS missing_billing_cycle,
    SUM(CASE WHEN monthly_price IS NULL THEN 1 ELSE 0 END) AS missing_monthly_price,
    SUM(CASE WHEN start_date IS NULL THEN 1 ELSE 0 END) AS missing_start_date,
    SUM(CASE WHEN end_date IS NULL THEN 1 ELSE 0 END) AS missing_end_date,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END) AS missing_status,
    SUM(CASE WHEN cancellation_date IS NULL THEN 1 ELSE 0 END) AS missing_cancellation_date,
    SUM(CASE WHEN cancellation_reason IS NULL THEN 1 ELSE 0 END) AS missing_cancellation_reason
FROM raw.subscriptions;

SELECT
    status,
    COUNT(*) AS record_count
FROM raw.subscriptions
WHERE cancellation_date IS NULL
GROUP BY status
ORDER BY status;

SELECT
    status,
    COUNT(*) AS record_count
FROM raw.subscriptions
WHERE end_date IS NULL
GROUP BY status;

/*
=================================================
-- SUBSCRIPTIONS: MISSING VALUE FINDINGS
=================================================

-- end_date contains 4,145 NULL values.
-- These records correspond to active subscriptions,
-- so the missing values are expected.

-- cancellation_date contains 4,145 NULL values.
-- These records correspond to active subscriptions,
-- so the missing values are expected.

-- cancellation_reason contains missing values for
-- active subscriptions and some cancelled subscriptions.
-- Missing cancellation reasons for cancelled subscriptions
-- will require further investigation during cleaning.
=================================================
*/

SELECT
    subscription_plan,
    COUNT(*) AS record_count
FROM raw.subscriptions
GROUP BY subscription_plan
ORDER BY subscription_plan;

SELECT
    billing_cycle,
    COUNT(*) AS record_count
FROM raw.subscriptions
GROUP BY billing_cycle
ORDER BY billing_cycle;

SELECT
    status,
    COUNT(*) AS record_count
FROM raw.subscriptions
GROUP BY status
ORDER BY status;

/*
=================================================
-- SUBSCRIPTIONS: CATEGORICAL VALUE FINDINGS
=================================================

-- subscription_plan contains inconsistent capitalization.
-- The 'business' value should be standardized to 'Business'.

-- billing_cycle values are formatted consistently, with
-- 'Annual' and 'Monthly' as the observed values.

-- status contains whitespace inconsistency.
-- 53 records contain ' Active ' instead of 'Active'.

-- The status values otherwise consist of 'Active' and
-- 'Cancelled'.
=================================================
*/
--===========Cancellation reason=================
SELECT
    cancellation_reason,
    COUNT(*) AS record_count
FROM raw.subscriptions
GROUP BY cancellation_reason
ORDER BY cancellation_reason;

SELECT
    status,
    COUNT(*) AS record_count,
    SUM(CASE 
            WHEN cancellation_reason IS NULL 
            THEN 1 ELSE 0 
        END) AS missing_reason
FROM raw.subscriptions
GROUP BY status;
/*
→ cancellation_reason: consistent
*/
--============Dates====================
SELECT TOP 300
    start_date
FROM raw.subscriptions
ORDER BY subscription_id;

SELECT TOP 300
    end_date
FROM raw.subscriptions
ORDER BY subscription_id;

SELECT TOP 300
    cancellation_date
FROM raw.subscriptions
WHERE cancellation_date IS NOT NULL
ORDER BY subscription_id;
/*
=================================================
-- SUBSCRIPTIONS: DATE FORMAT FINDINGS
=================================================

-- start_date,end_date and cancellation_date contains three different date formats:
-- YYYY-MM-DD
-- MM/DD/YYYY
-- Mon DD, YYYY.
-- The date values will be standardized to a consistent
-- DATE format during the cleaning stage.
=================================================
*/
--=================================================
-- SUBSCRIPTIONS: VALIDATE MONTHLY PRICE
--=================================================
SELECT 
    subscription_plan,
    monthly_price,
    COUNT (*) AS record_count
FROM raw.subscriptions
GROUP BY 
    subscription_plan,
    monthLy_price
ORDER BY 
    subscription_plan,
    monthLy_price

/*
=================================================
-- SUBSCRIPTIONS: MONTHLY PRICE FINDINGS
=================================================

-- monthly_price contains no missing values.

-- Monthly prices are consistently formatted and
-- correctly correspond to subscription plans:

-- Starter       = 1,500
-- Professional  = 4,500
-- Business      = 9,000
-- Enterprise    = 20,000

-- No pricing mismatches were identified.
=================================================
*/
/*
=================================================
-- SUBSCRIPTIONS: BUSINESS RULE VALIDATION
=================================================

-- Business Rule 1:
-- Active subscriptions should not have a
-- cancellation date.

-- Result:
-- 0 active subscriptions have a cancellation date,
-- so this rule is satisfied.


-- Business Rule 2:
-- Cancelled subscriptions should have a
-- cancellation date.

-- Result:
-- 0 cancelled subscriptions are missing a
-- cancellation date, so this rule is satisfied.


-- Status Standardization Check:
-- Status values were checked after trimming
-- leading/trailing whitespace.

-- Result:
-- 'Active' and ' Active ' represent the same status
-- value and will be standardized to 'Active' during
-- the cleaning stage.
=================================================
*/
-- Business Rule 1:
SELECT
    COUNT(*) AS active_with_cancellation_date
FROM raw.subscriptions
WHERE TRIM(status) = 'Active'
AND cancellation_date IS NOT NULL

-- Business Rule 2:
SELECT
    COUNT(*) AS cancelled_without_cancellation_date
FROM raw.subscriptions
WHERE TRIM(status) = 'Cancelled'
AND cancellation_date IS NULL

-- Status Standardization Check
SELECT
    TRIM(status) AS status,
    COUNT(*) AS record_count
FROM raw.subscriptions
GROUP BY TRIM(status)
ORDER BY status;

--=========================================
--SUBSCRIPTIONS: CANCELLATION REASON
--=========================================
SELECT
    TRIM(cancellation_reason) AS cancellation_reason,
    COUNT(*) AS record_count
FROM raw.subscriptions
WHERE TRIM(status) = 'Cancelled'
GROUP BY TRIM(cancellation_reason)
ORDER BY record_count DESC;
/*
=================================================
-- SUBSCRIPTIONS: CANCELLATION REASON FINDINGS
=================================================

-- 870 subscriptions are cancelled.

-- 840 cancelled subscriptions have a recorded
-- cancellation reason.

-- 30 cancelled subscriptions contain a blank
-- or whitespace-only cancellation reason.

-- Cancellation reasons are otherwise formatted
-- consistently.

-- Blank cancellation reasons will be standardized
-- to NULL during the cleaning stage.
=================================================
============================================================
END OF SUBCRIPTIONS PROFILING
============================================================
*/

/*
============================================================
PAYMENTS: RAW DATA PROFILING
============================================================

Objective:
Assess the quality and structure of the raw payments data
before proceeding to the data cleaning stage.

Profiling areas:
1. Basic structure
2. Missing values
3. Duplicate values
4. Inspection of duplicated records

============================================================
*/


-- =========================================================
-- 1. PAYMENTS: BASIC STRUCTURE
-- =========================================================

-- Inspect the first 10 records
SELECT TOP 10 *
FROM raw.payments;


-- Check the total number of records
SELECT
    COUNT(*) AS total_rows
FROM raw.payments;


-- Inspect column names, data types, and nullability
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'raw'
  AND TABLE_NAME = 'payments'
ORDER BY ORDINAL_POSITION;


/*
FINDINGS:
- The payments table contains 70,548 records.
- The table contains nine columns.
- All nine columns are stored as VARCHAR.
- Date and numerical columns will require validation
  and appropriate data type conversion during cleaning.
*/


-- =========================================================
-- 2. PAYMENTS: MISSING VALUE CHECK
-- =========================================================

-- Check for NULL payment IDs
SELECT
    COUNT(*) AS missing_payment_id
FROM raw.payments
WHERE payment_id IS NULL;

-- Check for NULL transaction IDs
SELECT 
    COUNT(*) AS missing_transaction_id
FROM raw.payments
WHERE transaction_id IS NULL

-- Check for NULL customer IDs
SELECT 
    COUNT(*) AS missing_customer_id
FROM raw.payments
WHERE customer_id IS NULL

-- Check for NULL subcription IDs
SELECT 
    COUNT(*) AS missing_subscription_id
FROM raw.payments
WHERE subscription_id IS NULL


-- Check for empty or whitespace-only payment IDs
SELECT
    COUNT(*) AS blank_payment_id
FROM raw.payments
WHERE TRIM(payment_id) = '';

-- Check for empty or whitespace-only transaction IDs
SELECT 
    COUNT(*) AS blank_transaction_id
FROM raw.payments
WHERE TRIM(transaction_id) = ''

-- Check for empty or whitespace-only customer IDs
SELECT 
    COUNT(*) AS blank_customer_id
FROM raw.payments
WHERE TRIM(customer_id) = ''

-- Check for empty or whitespace-only subscription IDs
SELECT 
    COUNT(*) AS blank_subscription_id
FROM raw.payments
WHERE TRIM(subscription_id) = ''

/*
FINDING:
-- No NULL or blank payment_id values were identified.
-- No NULL or blank transaction_id values were identified.
-- No NULL or blank customer_id values were identified.
-- No NULL or blank subscription_id values were identified.
*/


-- =========================================================
-- 3. PAYMENTS: DUPLICATE CHECK 
-- =========================================================

-- Identify payment IDs appearing more than once
SELECT
    payment_id,
    COUNT(*) AS occurrence_count
FROM raw.payments
GROUP BY payment_id
HAVING COUNT(*) > 1;

-- Identify transaction IDs appearing more than once

SELECT
    transaction_id,
    COUNT (*) AS occurrence_count
FROM raw.payments
GROUP BY transaction_id
HAVING COUNT (*) > 1

-- Identify subscription IDs appearing more than once
SELECT
    subscription_id,
    COUNT (*) AS occurrence_count
FROM raw.payments
GROUP BY subscription_id
HAVING COUNT (*) > 1
ORDER BY occurence_count DESC
/*
-- DUPLICATE FINDINGS
-- 50 payment IDs appear more than once.
-- Each duplicated payment ID appears exactly twice.
-- These IDs account for 100 records in total.

-- 50 transaction IDs appear more than once.
-- Further inspection is required to confirm whether
-- the duplicated transaction IDs appear exactly twice
-- and whether the associated records are exact duplicates.

The duplicated IDs will be investigated further before deciding how to handle them during cleaning.

-- Multiple subscription IDs appear more than once.
-- Among the returned IDs, occurrence counts range from 2 to 37 payment records.
-- Repeated subscription IDs may represent legitimate recurring payments and are not automatically duplicates.
-- Further inspection is required before determining whether any repeated records are exact duplicates.

*/

-- Identify customer IDs appearing more than once
SELECT
    customer_id,
    COUNT(*) AS occurrence_count
FROM raw.payments
GROUP BY customer_id
HAVING COUNT(*) > 1

-- Identify distinct customer IDs 
SELECT DISTINCT 
    COUNT(DISTINCT customer_id) AS total_customer_ids
FROM raw.payments
/*
-- Customer duplicate findings
-- Multiple customer IDs appear more than once in the payments table.
-- Approximately 5,000 distinct customer IDs were identified.
-- Repeated customer IDs are expected because a customer can have multiple payment records.
-- These repetitions are not considered duplicates by themselves and will not automatically be removed.
-- Customer IDs will be validated against the customers table during further data-quality checks.
*/

-- =========================================================
-- 4. PAYMENTS: INSPECT DUPLICATED RECORDS
-- =========================================================

-- Retrieve all records associated with duplicated payment IDs
SELECT *
FROM raw.payments
WHERE payment_id IN (
    SELECT
        payment_id
    FROM raw.payments
    GROUP BY payment_id
    HAVING COUNT(*) > 1
)
ORDER BY payment_id;

-- Retrieve all records associated with duplicated transaction IDs
SELECT *
FROM raw.payments
WHERE transaction_id IN (
    SELECT
    transaction_id
    FROM raw.payments
    GROUP BY transaction_id
    HAVING COUNT (*) > 1
)
ORDER BY transaction_id


-- Retrieve all records associated with duplicated subscription IDs
SELECT *
FROM raw.payments
WHERE subscription_id IN (
    SELECT
    subscription_id
    FROM raw.payments
    GROUP BY subscription_id
    HAVING COUNT (*) > 1
)
ORDER BY subscription_id

/*
FINDINGS:
-- 50 payment IDs and 50 transaction IDs appear more than once.
-- Each duplicated payment ID appears exactly twice.
-- Inspection confirms that all 50 duplicated payment_id pairs are exact duplicates across all nine columns.
-- Inspection also confirms that the duplicated transaction_id records are exact duplicates.
-- Subscription_id values are also exact duplicates.
-- These exact duplicate records will be removed during the cleaning stage.
*/

-- =========================================================
-- PAYMENTS: CUSTOMER PAYMENT DISTRIBUTION
-- =========================================================

SELECT
    customer_id,
    COUNT(*) AS total_payments
FROM raw.payments
GROUP BY customer_id
ORDER BY total_payments DESC;


-- FINDINGS:
-- Customers have between 1 and 37 payment records.
-- The highest number of payment records for a single customer is 37.
-- The lowest number of payment records for a single customer is 1.
-- Multiple payment records per customer are expected and are not considered duplicates by themselves.


-- =========================================================
-- PAYMENTS: REFERENTIAL INTEGRITY
-- =========================================================
-- CUSTOMER_ID REFERENTIAL INTEGRITY
SELECT
    p.customer_id
FROM raw.payments AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM raw.customers AS c
    WHERE c.customer_id = p.customer_id
);

-- FINDINGS:
-- No unmatched customer_id values were found in raw.payments.
-- All customer IDs referenced in the payments table have matching records in raw.customers.

-- SUBSCRIPTION_ID REFERENTIAL INTEGRITY
SELECT
    p.subscription_id
FROM raw.payments AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM raw.subscriptions AS s
    WHERE s.subscription_id = p.subscription_id
);
- FINDINGS:
-- No unmatched subscription_id values were found in raw.payments.
-- All subscription IDs referenced in the payments table have matching records in raw.subscriptions.

-- =========================================================
-- PAYMENTS: FORMATTING CONSISTENCY
-- =========================================================
-- CUSTOMER_ID FORMATTING CONSISTENCY
SELECT
    customer_id
FROM raw.payments
WHERE customer_id <> TRIM(customer_id);


-- FINDINGS:
-- No leading or trailing spaces were detected in customer_id.
-- Customer IDs appear consistently formatted with respect to surrounding whitespace.

-- SUBSCRIPTION_ID FORMATTING CONSISTENCY
SELECT
    subscription_id
FROM raw.payments
WHERE subscription_id <> TRIM(subscription_id);

-- FINDINGS:
-- No leading or trailing spaces were detected in subscription_id.
-- Subscription IDs appear consistently formatted with respect to surrounding whitespace.

--============================================================
--END OF PAYMENTS PROFILING
--============================================================


