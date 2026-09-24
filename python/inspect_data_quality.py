import pandas as pd
from pathlib import Path

# --------------------------------------------------
# SETUP
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw_data"

customers = pd.read_csv(RAW_DIR / "customers.csv")

# --------------------------------------------------
# 1. BASIC INFORMATION
# --------------------------------------------------

print("=" * 60)
print("CUSTOMER DATA QUALITY INSPECTION")
print("=" * 60)

print("\nDataset shape:")
print(customers.shape)

print("\nData types:")
print(customers.dtypes)

# --------------------------------------------------
# 2. MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = customers.isna().sum()

print(missing[missing > 0])

# --------------------------------------------------
# 3. DUPLICATE CUSTOMER IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE CUSTOMER IDs")
print("=" * 60)

duplicate_ids = customers[
    customers["customer_id"].duplicated(keep=False)
].sort_values("customer_id")

print(duplicate_ids[["customer_id", "company_name", "city"]].head(20))

print("\nNumber of duplicated rows:",
      customers["customer_id"].duplicated().sum())

# --------------------------------------------------
# 4. INDUSTRY VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("INDUSTRY VALUES")
print("=" * 60)

print(customers["industry"].value_counts())

# --------------------------------------------------
# 5. ACQUISITION CHANNEL VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("ACQUISITION CHANNEL VALUES")
print("=" * 60)

print(customers["acquisition_channel"].value_counts())

# --------------------------------------------------
# 6. CITY VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("CITY VALUES")
print("=" * 60)

print(customers["city"].value_counts(dropna=False))

# --------------------------------------------------
# 7. COMPANY NAMES WITH WHITESPACE
# --------------------------------------------------

print("\n" + "=" * 60)
print("COMPANY NAMES WITH EXTRA WHITESPACE")
print("=" * 60)

whitespace_names = customers[
    customers["company_name"].str.startswith(" ")
    | customers["company_name"].str.endswith(" ")
]

print(whitespace_names[["customer_id", "company_name"]].head(20))

print("\nNumber affected:",
      len(whitespace_names))

# --------------------------------------------------
# 8. SIGNUP DATE VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("SIGNUP DATE SAMPLE")
print("=" * 60)

print(customers["signup_date"].sample(20, random_state=100))

# --------------------------------------------------
# END
# --------------------------------------------------

print("\n" + "=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)

# ==================================================
# SUBSCRIPTIONS DATA QUALITY INSPECTION
# ==================================================

print("\n" + "=" * 60)
print("SUBSCRIPTION DATA QUALITY INSPECTION")
print("=" * 60)

subscriptions = pd.read_csv(
    RAW_DIR / "subscriptions.csv"
)

print("\nDataset shape:")
print(subscriptions.shape)

print("\nData types:")
print(subscriptions.dtypes)


# --------------------------------------------------
# 1. MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = subscriptions.isna().sum()

print(missing[missing > 0])


# --------------------------------------------------
# 2. DUPLICATE SUBSCRIPTION IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE SUBSCRIPTION IDs")
print("=" * 60)

duplicate_ids = subscriptions[
    subscriptions["subscription_id"].duplicated(keep=False)
].sort_values("subscription_id")

print(
    duplicate_ids[
        [
            "subscription_id",
            "customer_id",
            "plan",
            "status"
        ]
    ].head(20)
)

print(
    "\nNumber of duplicated rows:",
    subscriptions["subscription_id"].duplicated().sum()
)


# --------------------------------------------------
# 3. PLAN VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("PLAN VALUES")
print("=" * 60)

print(
    subscriptions["plan"].value_counts()
)


# --------------------------------------------------
# 4. BILLING CYCLE VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("BILLING CYCLE VALUES")
print("=" * 60)

print(
    subscriptions["billing_cycle"].value_counts()
)


# --------------------------------------------------
# 5. MONTHLY PRICE VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MONTHLY PRICE VALUES")
print("=" * 60)

print(
    subscriptions["monthly_price"].value_counts()
)


# --------------------------------------------------
# 6. STATUS VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("STATUS VALUES")
print("=" * 60)

print(
    subscriptions["status"].value_counts()
)


# --------------------------------------------------
# 7. CANCELLATION REASONS
# --------------------------------------------------

print("\n" + "=" * 60)
print("CANCELLATION REASONS")
print("=" * 60)

print(
    subscriptions["cancellation_reason"]
    .value_counts(dropna=False)
)


# --------------------------------------------------
# 8. DATE SAMPLES
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATE SAMPLES")
print("=" * 60)

print(
    subscriptions[
        [
            "start_date",
            "end_date",
            "cancellation_date"
        ]
    ].sample(
        20,
        random_state=100
    )
)


# --------------------------------------------------
# END
# --------------------------------------------------

print("\n" + "=" * 60)
print("SUBSCRIPTION INSPECTION COMPLETE")
print("=" * 60)

# ==================================================
# PAYMENTS DATA QUALITY INSPECTION
# ==================================================

print("\n" + "=" * 60)
print("PAYMENT DATA QUALITY INSPECTION")
print("=" * 60)

payments = pd.read_csv(
    RAW_DIR / "payments.csv"
)

print("\nDataset shape:")
print(payments.shape)

print("\nData types:")
print(payments.dtypes)


# --------------------------------------------------
# 1. MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = payments.isna().sum()

print(missing[missing > 0])


# --------------------------------------------------
# 2. DUPLICATE PAYMENT IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE PAYMENT IDs")
print("=" * 60)

duplicate_payment_ids = payments[
    payments["payment_id"].duplicated(keep=False)
].sort_values("payment_id")

print(
    duplicate_payment_ids[
        [
            "payment_id",
            "transaction_id",
            "customer_id",
            "amount",
            "payment_status"
        ]
    ].head(20)
)

print(
    "\nDuplicate payment IDs:",
    payments["payment_id"].duplicated().sum()
)


# --------------------------------------------------
# 3. DUPLICATE TRANSACTION IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE TRANSACTION IDs")
print("=" * 60)

transaction_ids = payments[
    payments["transaction_id"]
    .astype(str)
    .str.strip()
    .duplicated(keep=False)
].sort_values("transaction_id")

print(
    transaction_ids[
        [
            "payment_id",
            "transaction_id",
            "customer_id",
            "amount"
        ]
    ].head(20)
)

print(
    "\nDuplicate transaction IDs:",
    payments["transaction_id"]
    .astype(str)
    .str.strip()
    .duplicated()
    .sum()
)


# --------------------------------------------------
# 4. PAYMENT METHODS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT METHODS")
print("=" * 60)

print(
    payments["payment_method"].value_counts()
)


# --------------------------------------------------
# 5. PAYMENT STATUSES
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT STATUSES")
print("=" * 60)

print(
    payments["payment_status"].value_counts()
)


# --------------------------------------------------
# 6. AMOUNT VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("AMOUNT SAMPLE")
print("=" * 60)

print(
    payments[
        [
            "amount",
            "paid_amount"
        ]
    ].sample(
        30,
        random_state=200
    )
)


# --------------------------------------------------
# 7. PAYMENT DATE SAMPLE
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT DATE SAMPLE")
print("=" * 60)

print(
    payments["payment_date"].sample(
        30,
        random_state=201
    )
)


# --------------------------------------------------
# 8. WHITESPACE IN TRANSACTION IDs
# --------------------------------------------------

print("\n" + "=" * 60)
print("TRANSACTION IDs WITH WHITESPACE")
print("=" * 60)

transaction_whitespace = payments[
    payments["transaction_id"].astype(str) !=
    payments["transaction_id"].astype(str).str.strip()
]

print(
    transaction_whitespace[
        [
            "payment_id",
            "transaction_id"
        ]
    ].head(20)
)

print(
    "\nNumber affected:",
    len(transaction_whitespace)
)


# --------------------------------------------------
# END
# --------------------------------------------------

print("\n" + "=" * 60)
print("PAYMENT INSPECTION COMPLETE")
print("=" * 60)

# ==================================================
# USAGE ACTIVITY DATA QUALITY INSPECTION
# ==================================================

print("\n" + "=" * 60)
print("USAGE ACTIVITY DATA QUALITY INSPECTION")
print("=" * 60)

usage = pd.read_csv(
    RAW_DIR / "usage_activity.csv",
    dtype=str
)

print("\nDataset shape:")
print(usage.shape)

print("\nData types:")
print(usage.dtypes)

# 1. Missing values
print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = usage.isna().sum()
print(missing[missing > 0])

# 2. Duplicate activity IDs
print("\n" + "=" * 60)
print("DUPLICATE ACTIVITY IDs")
print("=" * 60)

duplicate_activity_ids = usage[
    usage["activity_id"].duplicated(keep=False)
].sort_values("activity_id")

print(
    duplicate_activity_ids[
        [
            "activity_id",
            "customer_id",
            "month",
            "login_count"
        ]
    ].head(20)
)

print(
    "\nNumber of duplicated activity IDs:",
    usage["activity_id"].duplicated().sum()
)

# 3. Customer IDs with whitespace
print("\n" + "=" * 60)
print("CUSTOMER IDs WITH WHITESPACE")
print("=" * 60)

customer_whitespace = usage[
    usage["customer_id"].astype(str)
    != usage["customer_id"].astype(str).str.strip()
]

print(
    customer_whitespace[
        [
            "activity_id",
            "customer_id",
            "month"
        ]
    ].head(20)
)

print(
    "\nNumber affected:",
    len(customer_whitespace)
)

# 4. Month sample
print("\n" + "=" * 60)
print("MONTH SAMPLE")
print("=" * 60)

print(
    usage["month"]
    .sample(30, random_state=300)
)

# 5. Login count sample
print("\n" + "=" * 60)
print("LOGIN COUNT SAMPLE")
print("=" * 60)

print(
    usage[
        [
            "login_count",
            "session_minutes",
            "invoices_created",
            "reports_generated",
            "active_users",
            "features_used"
        ]
    ].sample(30, random_state=301)
)

# 6. Missing login/session records
print("\n" + "=" * 60)
print("MISSING ACTIVITY METRICS")
print("=" * 60)

print(
    usage[
        [
            "activity_id",
            "customer_id",
            "month",
            "login_count",
            "session_minutes"
        ]
    ][
        usage["login_count"].isna() |
        usage["session_minutes"].isna()
    ].head(20)
)

print("\n" + "=" * 60)
print("USAGE INSPECTION COMPLETE")
print("=" * 60)

# ==================================================
# SUPPORT TICKETS DATA QUALITY INSPECTION
# ==================================================

print("\n" + "=" * 60)
print("SUPPORT TICKETS DATA QUALITY INSPECTION")
print("=" * 60)

support = pd.read_csv(
    RAW_DIR / "support_tickets.csv",
    dtype=str
)

print("\nDataset shape:")
print(support.shape)

print("\nData types:")
print(support.dtypes)

# 1. Missing values
print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = support.isna().sum()
print(missing[missing > 0])

# 2. Duplicate ticket IDs
print("\n" + "=" * 60)
print("DUPLICATE TICKET IDs")
print("=" * 60)

duplicate_ticket_ids = support[
    support["ticket_id"].duplicated(keep=False)
].sort_values("ticket_id")

print(
    duplicate_ticket_ids[
        [
            "ticket_id",
            "customer_id",
            "issue_category",
            "ticket_status"
        ]
    ].head(20)
)

print(
    "\nNumber of duplicated ticket IDs:",
    support["ticket_id"].duplicated().sum()
)

# 3. Customer IDs with whitespace
print("\n" + "=" * 60)
print("CUSTOMER IDs WITH WHITESPACE")
print("=" * 60)

customer_whitespace = support[
    support["customer_id"].astype(str)
    != support["customer_id"].astype(str).str.strip()
]

print(
    customer_whitespace[
        [
            "ticket_id",
            "customer_id"
        ]
    ].head(20)
)

print(
    "\nNumber affected:",
    len(customer_whitespace)
)

# 4. Issue categories
print("\n" + "=" * 60)
print("ISSUE CATEGORY VALUES")
print("=" * 60)

print(
    support["issue_category"].value_counts()
)

# 5. Priority values
print("\n" + "=" * 60)
print("PRIORITY VALUES")
print("=" * 60)

print(
    support["priority"].value_counts()
)

# 6. Ticket status values
print("\n" + "=" * 60)
print("TICKET STATUS VALUES")
print("=" * 60)

print(
    support["ticket_status"].value_counts()
)

# 7. Resolution hours sample
print("\n" + "=" * 60)
print("RESOLUTION HOURS SAMPLE")
print("=" * 60)

print(
    support[
        [
            "resolution_hours",
            "ticket_status"
        ]
    ].sample(30, random_state=400)
)

# 8. Customer satisfaction sample
print("\n" + "=" * 60)
print("CUSTOMER SATISFACTION SAMPLE")
print("=" * 60)

print(
    support[
        [
            "customer_satisfaction",
            "ticket_status",
            "priority"
        ]
    ].sample(30, random_state=401)
)

# 9. Ticket date sample
print("\n" + "=" * 60)
print("TICKET DATE SAMPLE")
print("=" * 60)

print(
    support["ticket_date"]
    .sample(30, random_state=402)
)

print("\n" + "=" * 60)
print("SUPPORT INSPECTION COMPLETE")
print("=" * 60)

# ==================================================
# CUSTOMER FEEDBACK DATA QUALITY INSPECTION
# ==================================================

print("\n" + "=" * 60)
print("CUSTOMER FEEDBACK DATA QUALITY INSPECTION")
print("=" * 60)

feedback = pd.read_csv(
    RAW_DIR / "customer_feedback.csv",
    dtype=str
)

print("\nDataset shape:")
print(feedback.shape)

print("\nData types:")
print(feedback.dtypes)

# 1. Missing values
print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = feedback.isna().sum()
print(missing[missing > 0])

# 2. Duplicate feedback IDs
print("\n" + "=" * 60)
print("DUPLICATE FEEDBACK IDs")
print("=" * 60)

duplicate_feedback_ids = feedback[
    feedback["feedback_id"].duplicated(keep=False)
].sort_values("feedback_id")

print(
    duplicate_feedback_ids[
        [
            "feedback_id",
            "customer_id",
            "feedback_type",
            "rating",
            "sentiment"
        ]
    ].head(20)
)

print(
    "\nNumber of duplicated feedback IDs:",
    feedback["feedback_id"].duplicated().sum()
)

# 3. Customer IDs with whitespace
print("\n" + "=" * 60)
print("CUSTOMER IDs WITH WHITESPACE")
print("=" * 60)

customer_whitespace = feedback[
    feedback["customer_id"].astype(str)
    != feedback["customer_id"].astype(str).str.strip()
]

print(
    customer_whitespace[
        [
            "feedback_id",
            "customer_id"
        ]
    ].head(20)
)

print(
    "\nNumber affected:",
    len(customer_whitespace)
)

# 4. Feedback type values
print("\n" + "=" * 60)
print("FEEDBACK TYPE VALUES")
print("=" * 60)

print(
    feedback["feedback_type"].value_counts()
)

# 5. Sentiment values
print("\n" + "=" * 60)
print("SENTIMENT VALUES")
print("=" * 60)

print(
    feedback["sentiment"].value_counts()
)

# 6. Rating values
print("\n" + "=" * 60)
print("RATING VALUES")
print("=" * 60)

print(
    feedback["rating"].value_counts(dropna=False)
    .sort_index()
)

# 7. Feedback date sample
print("\n" + "=" * 60)
print("FEEDBACK DATE SAMPLE")
print("=" * 60)

print(
    feedback["feedback_date"]
    .sample(30, random_state=500)
)

# 8. Feedback text whitespace
print("\n" + "=" * 60)
print("FEEDBACK TEXT WITH WHITESPACE")
print("=" * 60)

text_whitespace = feedback[
    feedback["feedback_text"].astype(str)
    != feedback["feedback_text"].astype(str).str.strip()
]

print(
    text_whitespace[
        [
            "feedback_id",
            "feedback_text"
        ]
    ].head(20)
)

print(
    "\nNumber affected:",
    len(text_whitespace)
)

print("\n" + "=" * 60)
print("CUSTOMER FEEDBACK INSPECTION COMPLETE")
print("=" * 60)