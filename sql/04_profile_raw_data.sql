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