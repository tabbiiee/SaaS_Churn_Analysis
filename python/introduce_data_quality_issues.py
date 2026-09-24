import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import random

# --------------------------------------------------
# SETUP
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw_data"
CLEAN_DIR = BASE_DIR / "clean_data"

random.seed(42)

# --------------------------------------------------
# STEP 1: CREATE CLEAN BASELINE
# --------------------------------------------------

files = [
    "customers.csv",
    "subscriptions.csv",
    "payments.csv",
    "usage_activity.csv",
    "support_tickets.csv",
    "customer_feedback.csv"
]

for file in files:
    source = RAW_DIR / file
    destination = CLEAN_DIR / file

    if not destination.exists():
        shutil.copy2(source, destination)

# --------------------------------------------------
# STEP 2: LOAD CUSTOMERS
# --------------------------------------------------

customers = pd.read_csv(CLEAN_DIR / "customers.csv")

print("Original customers:", customers.shape)

# --------------------------------------------------
# ISSUE 1: MISSING VALUES
# --------------------------------------------------

# Randomly remove some city values
missing_city = customers.sample(
    n=50,
    random_state=42
).index

customers.loc[missing_city, "city"] = None


# --------------------------------------------------
# ISSUE 2: INCONSISTENT CAPITALIZATION
# --------------------------------------------------

industry_rows = customers.sample(
    n=80,
    random_state=43
).index

customers.loc[industry_rows, "industry"] = (
    customers.loc[industry_rows, "industry"]
    .str.lower()
)


# --------------------------------------------------
# ISSUE 3: EXTRA WHITESPACE
# --------------------------------------------------

company_rows = customers.sample(
    n=70,
    random_state=44
).index

customers.loc[company_rows, "company_name"] = (
    "  " + customers.loc[company_rows, "company_name"] + "  "
)


# --------------------------------------------------
# ISSUE 4: INCONSISTENT ACQUISITION CHANNELS
# --------------------------------------------------

channel_rows = customers.sample(
    n=100,
    random_state=45
).index

channel_changes = {
    "Google Ads": "google ads",
    "Instagram": "INSTAGRAM",
    "Facebook": "facebook",
    "Referral": " referral",
    "LinkedIn": "LINKEDIN"
}

for index in channel_rows:
    current_channel = customers.loc[index, "acquisition_channel"]

    if current_channel in channel_changes:
        customers.loc[index, "acquisition_channel"] = (
            channel_changes[current_channel]
        )


# --------------------------------------------------
# ISSUE 5: DATE FORMAT INCONSISTENCY
# --------------------------------------------------

date_rows = customers.sample(
    n=100,
    random_state=46
).index

for index in date_rows:

    date = pd.to_datetime(
        customers.loc[index, "signup_date"]
    )

    # Three different date formats
    formats = [
        date.strftime("%d/%m/%Y"),
        date.strftime("%b %d, %Y"),
        date.strftime("%Y/%m/%d")
    ]

    customers.loc[index, "signup_date"] = random.choice(formats)


# --------------------------------------------------
# ISSUE 6: TYPO IN CITY NAMES
# --------------------------------------------------

city_typos = {
    "Nairobi": "Naiorbi",
    "Mombasa": "Mombassa",
    "Kisumu": "Kisum",
    "Nakuru": "Nakur",
    "Kampala": "Kampalaa",
    "Kigali": "Kigali ",
    "Accra": "Acra",
    "Lagos": "Lagoss",
    "Johannesburg": "Johannesberg"
}

city_rows = customers.sample(
    n=60,
    random_state=47
).index

for index in city_rows:

    current_city = customers.loc[index, "city"]

    if current_city in city_typos:
        customers.loc[index, "city"] = city_typos[current_city]


# --------------------------------------------------
# ISSUE 7: DUPLICATE CUSTOMER RECORDS
# --------------------------------------------------

duplicate_rows = customers.sample(
    n=20,
    random_state=48
)

customers = pd.concat(
    [customers, duplicate_rows],
    ignore_index=True
)


# --------------------------------------------------
# SAVE MESSY CUSTOMERS
# --------------------------------------------------

customers.to_csv(
    RAW_DIR / "customers.csv",
    index=False
)

# --------------------------------------------------
# REPORT
# --------------------------------------------------

print("\nCustomers after introducing data-quality issues:")
print("Rows:", len(customers))
print("Columns:", len(customers.columns))

print("\nMissing values:")
print(customers.isna().sum())

print("\nDuplicate customer IDs:")
print(customers["customer_id"].duplicated().sum())

print("\nMessy customers.csv saved successfully!")

# ==================================================
# SUBSCRIPTIONS DATA QUALITY ISSUES
# ==================================================

print("\n" + "=" * 60)
print("INTRODUCING SUBSCRIPTION DATA QUALITY ISSUES")
print("=" * 60)

# --------------------------------------------------
# LOAD CLEAN SUBSCRIPTIONS
# --------------------------------------------------

subscriptions = pd.read_csv(
    CLEAN_DIR / "subscriptions.csv",
     dtype={"monthly_price": "object"}
)

print("Original subscriptions:", subscriptions.shape)


# --------------------------------------------------
# ISSUE 1: INCONSISTENT PLAN CAPITALIZATION
# --------------------------------------------------

plan_rows = subscriptions.sample(
    n=100,
    random_state=50
).index

plan_changes = {
    "Starter": "starter",
    "Professional": "PROFESSIONAL",
    "Business": "business",
    "Enterprise": "enterprise"
}

for index in plan_rows:

    current_plan = subscriptions.loc[index, "plan"]

    if current_plan in plan_changes:
        subscriptions.loc[index, "plan"] = (
            plan_changes[current_plan]
        )


# --------------------------------------------------
# ISSUE 2: INCONSISTENT BILLING CYCLE
# --------------------------------------------------

billing_rows = subscriptions.sample(
    n=80,
    random_state=51
).index

billing_changes = {
    "Monthly": "monthly",
    "Annual": "ANNUAL"
}

for index in billing_rows:

    current_cycle = subscriptions.loc[index, "billing_cycle"]

    if current_cycle in billing_changes:
        subscriptions.loc[index, "billing_cycle"] = (
            billing_changes[current_cycle]
        )


# --------------------------------------------------
# ISSUE 3: CURRENCY FORMATTING
# --------------------------------------------------

price_rows = subscriptions.sample(
    n=120,
    random_state=52
).index

for index in price_rows:

    price = subscriptions.loc[index, "monthly_price"]

    if price == 1500:
        subscriptions.loc[index, "monthly_price"] = "1,500"

    elif price == 4500:
        subscriptions.loc[index, "monthly_price"] = "KES 4,500"

    elif price == 9000:
        subscriptions.loc[index, "monthly_price"] = "9,000"

    elif price == 20000:
        subscriptions.loc[index, "monthly_price"] = "KES 20,000"


# --------------------------------------------------
# ISSUE 4: EXTRA WHITESPACE IN STATUS
# --------------------------------------------------

status_rows = subscriptions.sample(
    n=60,
    random_state=53
).index

for index in status_rows:

    current_status = subscriptions.loc[index, "status"]

    if current_status == "Active":
        subscriptions.loc[index, "status"] = " Active "

    elif current_status == "Cancelled":
        subscriptions.loc[index, "status"] = "Cancelled "


# --------------------------------------------------
# ISSUE 5: MIXED DATE FORMATS
# --------------------------------------------------

date_columns = [
    "start_date",
    "end_date",
    "cancellation_date"
]

for column_number, column in enumerate(date_columns):

    # Only work with non-null dates
    valid_rows = subscriptions[
        subscriptions[column].notna()
    ].index

    if len(valid_rows) == 0:
        continue

    selected_rows = subscriptions.loc[valid_rows].sample(
        n=min(100, len(valid_rows)),
        random_state=54 + column_number
    ).index

    for index in selected_rows:

        date = pd.to_datetime(
            subscriptions.loc[index, column]
        )

        formats = [
            date.strftime("%d/%m/%Y"),
            date.strftime("%b %d, %Y"),
            date.strftime("%Y/%m/%d")
        ]

        subscriptions.loc[index, column] = random.choice(
            formats
        )


# --------------------------------------------------
# ISSUE 6: MISSING CANCELLATION REASON
# --------------------------------------------------

cancelled_rows = subscriptions[
    subscriptions["status"].astype(str).str.strip() == "Cancelled"
].index

selected_cancelled = subscriptions.loc[
    cancelled_rows
].sample(
    n=min(30, len(cancelled_rows)),
    random_state=57
).index

subscriptions.loc[
    selected_cancelled,
    "cancellation_reason"
] = None


# --------------------------------------------------
# ISSUE 7: DUPLICATE SUBSCRIPTION RECORDS
# --------------------------------------------------

duplicate_rows = subscriptions.sample(
    n=15,
    random_state=58
)

subscriptions = pd.concat(
    [subscriptions, duplicate_rows],
    ignore_index=True
)


# --------------------------------------------------
# SAVE MESSY SUBSCRIPTIONS
# --------------------------------------------------

subscriptions.to_csv(
    RAW_DIR / "subscriptions.csv",
    index=False
)

print("\nSubscriptions after introducing issues:")
print("Rows:", len(subscriptions))
print("Columns:", len(subscriptions.columns))

print("\nMissing values:")
print(subscriptions.isna().sum())

print("\nDuplicate subscription IDs:")
print(
    subscriptions["subscription_id"]
    .duplicated()
    .sum()
)

print("\nMessy subscriptions.csv saved successfully!")

# ==================================================
# PAYMENTS DATA QUALITY ISSUES
# ==================================================

print("\n" + "=" * 60)
print("INTRODUCING PAYMENT DATA QUALITY ISSUES")
print("=" * 60)

# --------------------------------------------------
# LOAD CLEAN PAYMENTS
# --------------------------------------------------

payments = pd.read_csv(
    CLEAN_DIR / "payments.csv",
    dtype={
        "amount": "object",
        "paid_amount": "object"
    }
)

print("Original payments:", payments.shape)


# --------------------------------------------------
# ISSUE 1: PAYMENT METHOD INCONSISTENCIES
# --------------------------------------------------

method_rows = payments.sample(
    n=300,
    random_state=60
).index

method_changes = {
    "M-Pesa": "M-PESA",
    "Bank Transfer": "bank transfer",
    "Credit Card": "credit card",
    "Debit Card": "DEBIT CARD"
}

for index in method_rows:

    current_method = payments.loc[
        index,
        "payment_method"
    ]

    if current_method in method_changes:
        payments.loc[
            index,
            "payment_method"
        ] = method_changes[current_method]


# --------------------------------------------------
# ISSUE 2: PAYMENT STATUS INCONSISTENCIES
# --------------------------------------------------

status_rows = payments.sample(
    n=250,
    random_state=61
).index

status_changes = {
    "Successful": "successful",
    "Late": "LATE",
    "Failed": " failed",
}

for index in status_rows:

    current_status = payments.loc[
        index,
        "payment_status"
    ]

    if current_status in status_changes:
        payments.loc[
            index,
            "payment_status"
        ] = status_changes[current_status]


# --------------------------------------------------
# ISSUE 3: WHITESPACE
# --------------------------------------------------

whitespace_rows = payments.sample(
    n=150,
    random_state=62
).index

for index in whitespace_rows:

    payments.loc[
        index,
        "payment_method"
    ] = (
        " " +
        str(payments.loc[index, "payment_method"]) +
        " "
    )


# --------------------------------------------------
# ISSUE 4: CURRENCY FORMATTING
# --------------------------------------------------

amount_rows = payments.sample(
    n=300,
    random_state=63
).index

for index in amount_rows:

    amount = payments.loc[
        index,
        "amount"
    ]

    paid_amount = payments.loc[
        index,
        "paid_amount"
    ]

    # Format billed amount
    if pd.notna(amount):

        amount = float(amount)

        if amount.is_integer():
            amount = int(amount)

        formats = [
            f"{amount:,}",
            f"KES {amount:,}",
            f"{amount}"
        ]

        payments.loc[
            index,
            "amount"
        ] = random.choice(formats)

    # Format paid amount
    if pd.notna(paid_amount):

        paid_amount = float(paid_amount)

        if paid_amount.is_integer():
            paid_amount = int(paid_amount)

        formats = [
            f"{paid_amount:,}",
            f"KES {paid_amount:,}",
            f"{paid_amount}"
        ]

        payments.loc[
            index,
            "paid_amount"
        ] = random.choice(formats)


# --------------------------------------------------
# ISSUE 5: MIXED PAYMENT DATE FORMATS
# --------------------------------------------------

date_rows = payments.sample(
    n=300,
    random_state=64
).index

for index in date_rows:

    date = pd.to_datetime(
        payments.loc[index, "payment_date"]
    )

    formats = [
        date.strftime("%d/%m/%Y"),
        date.strftime("%b %d, %Y"),
        date.strftime("%Y/%m/%d")
    ]

    payments.loc[
        index,
        "payment_date"
    ] = random.choice(formats)


# --------------------------------------------------
# ISSUE 6: TRANSACTION ID WHITESPACE
# --------------------------------------------------

transaction_rows = payments.sample(
    n=100,
    random_state=65
).index

for index in transaction_rows:

    transaction_id = str(
        payments.loc[
            index,
            "transaction_id"
        ]
    )

    payments.loc[
        index,
        "transaction_id"
    ] = " " + transaction_id + " "


# --------------------------------------------------
# ISSUE 7: DUPLICATE PAYMENT RECORDS
# --------------------------------------------------

duplicate_rows = payments.sample(
    n=50,
    random_state=66
)

payments = pd.concat(
    [payments, duplicate_rows],
    ignore_index=True
)


# --------------------------------------------------
# SAVE MESSY PAYMENTS
# --------------------------------------------------

payments.to_csv(
    RAW_DIR / "payments.csv",
    index=False
)

print("\nPayments after introducing issues:")
print("Rows:", len(payments))
print("Columns:", len(payments.columns))

print("\nMissing values:")
print(payments.isna().sum())

print("\nDuplicate payment IDs:")
print(
    payments["payment_id"]
    .duplicated()
    .sum()
)

print("\nDuplicate transaction IDs:")
print(
    payments["transaction_id"]
    .astype(str)
    .str.strip()
    .duplicated()
    .sum()
)

print("\nMessy payments.csv saved successfully!")

# ==================================================
# USAGE ACTIVITY DATA QUALITY ISSUES
# ==================================================

print("\n" + "=" * 60)
print("INTRODUCING USAGE ACTIVITY DATA QUALITY ISSUES")
print("=" * 60)

usage = pd.read_csv(
    CLEAN_DIR / "usage_activity.csv",
    dtype={
        "activity_id": "object",
        "customer_id": "object",
        "month": "object",
        "login_count": "object",
        "session_minutes": "object",
        "invoices_created": "object",
        "reports_generated": "object",
        "active_users": "object",
        "features_used": "object"
    }
)

print("Original usage:", usage.shape)

# --------------------------------------------------
# 1. Inconsistent customer ID whitespace
# --------------------------------------------------

np.random.seed(40)

whitespace_indices = np.random.choice(
    usage.index,
    size=150,
    replace=False
)

usage.loc[whitespace_indices, "customer_id"] = (
    usage.loc[whitespace_indices, "customer_id"] + " "
)

# --------------------------------------------------
# 2. Inconsistent month/date formats
# --------------------------------------------------

np.random.seed(41)

date_indices = np.random.choice(
    usage.index,
    size=300,
    replace=False
)

usage.loc[date_indices, "month"] = pd.to_datetime(
    usage.loc[date_indices, "month"]
).dt.strftime("%m/%d/%Y")

# --------------------------------------------------
# 3. Numeric values stored as text
# --------------------------------------------------

np.random.seed(42)

login_indices = np.random.choice(
    usage.index,
    size=250,
    replace=False
)

usage.loc[login_indices, "login_count"] = (
    usage.loc[login_indices, "login_count"].astype(str)
)

session_indices = np.random.choice(
    usage.index,
    size=250,
    replace=False
)

usage.loc[session_indices, "session_minutes"] = (
    usage.loc[session_indices, "session_minutes"].astype(str)
)

# --------------------------------------------------
# 4. Missing values in activity metrics
# --------------------------------------------------

np.random.seed(43)

missing_login_indices = np.random.choice(
    usage.index,
    size=50,
    replace=False
)

usage.loc[missing_login_indices, "login_count"] = None

missing_session_indices = np.random.choice(
    usage.index,
    size=40,
    replace=False
)

usage.loc[missing_session_indices, "session_minutes"] = None

# --------------------------------------------------
# 5. Duplicate activity records
# --------------------------------------------------

np.random.seed(44)

duplicate_indices = np.random.choice(
    usage.index,
    size=30,
    replace=False
)

duplicate_rows = usage.loc[duplicate_indices].copy()

usage = pd.concat(
    [usage, duplicate_rows],
    ignore_index=True
)

# --------------------------------------------------
# 6. Save messy usage data
# --------------------------------------------------

usage.to_csv(
    RAW_DIR / "usage_activity.csv",
    index=False
)

print("\nUsage activity after introducing issues:")
print("Rows:", len(usage))
print("Columns:", len(usage.columns))

print("\nMissing values:")
print(usage.isna().sum())

print("\nDuplicate activity IDs:")
print(
    usage["activity_id"].duplicated().sum()
)

print("\nMessy usage_activity.csv saved successfully!")

# ==================================================
# SUPPORT TICKETS DATA QUALITY ISSUES
# ==================================================

print("\n" + "=" * 60)
print("INTRODUCING SUPPORT TICKETS DATA QUALITY ISSUES")
print("=" * 60)

support = pd.read_csv(
    CLEAN_DIR / "support_tickets.csv",
    dtype={
        "ticket_id": "object",
        "customer_id": "object",
        "ticket_date": "object",
        "issue_category": "object",
        "priority": "object",
        "resolution_hours": "object",
        "ticket_status": "object",
        "customer_satisfaction": "object"
    }
)

print("Original support tickets:", support.shape)

# --------------------------------------------------
# 1. Customer ID whitespace
# --------------------------------------------------

np.random.seed(50)

customer_indices = np.random.choice(
    support.index,
    size=120,
    replace=False
)

support.loc[customer_indices, "customer_id"] = (
    support.loc[customer_indices, "customer_id"] + " "
)

# --------------------------------------------------
# 2. Inconsistent issue category formatting
# --------------------------------------------------

np.random.seed(51)

category_indices = np.random.choice(
    support.index,
    size=200,
    replace=False
)

category_variants = {
    "Performance": "performance",
    "Account Access": "account access",
    "How-To Question": "how-to question",
    "Feature Request": "FEATURE REQUEST",
    "Bug Report": "bug report",
    "Technical Issue": "technical issue",
    "Integration": "INTEGRATION",
    "Billing": " billing"
}

for idx in category_indices:
    original = support.loc[idx, "issue_category"]

    if original in category_variants:
        support.loc[idx, "issue_category"] = (
            category_variants[original]
        )

# --------------------------------------------------
# 3. Inconsistent priority formatting
# --------------------------------------------------

np.random.seed(52)

priority_indices = np.random.choice(
    support.index,
    size=150,
    replace=False
)

priority_variants = {
    "Low": "low",
    "Medium": "MEDIUM",
    "High": " high",
    "Critical": "CRITICAL"
}

for idx in priority_indices:
    original = support.loc[idx, "priority"]

    if original in priority_variants:
        support.loc[idx, "priority"] = (
            priority_variants[original]
        )

# --------------------------------------------------
# 4. Inconsistent ticket status formatting
# --------------------------------------------------

np.random.seed(53)

status_indices = np.random.choice(
    support.index,
    size=150,
    replace=False
)

status_variants = {
    "Resolved": "resolved",
    "Pending": " PENDING",
    "Open": "open"
}

for idx in status_indices:
    original = support.loc[idx, "ticket_status"]

    if original in status_variants:
        support.loc[idx, "ticket_status"] = (
            status_variants[original]
        )

# --------------------------------------------------
# 5. Missing customer satisfaction
# --------------------------------------------------

np.random.seed(54)

satisfaction_indices = np.random.choice(
    support.index,
    size=100,
    replace=False
)

support.loc[
    satisfaction_indices,
    "customer_satisfaction"
] = None

# --------------------------------------------------
# 6. Resolution hours stored as text
# --------------------------------------------------

np.random.seed(55)

resolution_indices = np.random.choice(
    support.index,
    size=200,
    replace=False
)

support.loc[
    resolution_indices,
    "resolution_hours"
] = (
    support.loc[
        resolution_indices,
        "resolution_hours"
    ].astype(str)
)

# --------------------------------------------------
# 7. Mixed ticket dates
# --------------------------------------------------

np.random.seed(56)

date_indices = np.random.choice(
    support.index,
    size=250,
    replace=False
)

support.loc[date_indices, "ticket_date"] = (
    pd.to_datetime(
        support.loc[date_indices, "ticket_date"]
    ).dt.strftime("%m/%d/%Y")
)

# --------------------------------------------------
# 8. Duplicate ticket records
# --------------------------------------------------

np.random.seed(57)

duplicate_indices = np.random.choice(
    support.index,
    size=25,
    replace=False
)

duplicate_rows = support.loc[
    duplicate_indices
].copy()

support = pd.concat(
    [support, duplicate_rows],
    ignore_index=True
)

# --------------------------------------------------
# 9. Save messy support data
# --------------------------------------------------

support.to_csv(
    RAW_DIR / "support_tickets.csv",
    index=False
)

print("\nSupport tickets after introducing issues:")
print("Rows:", len(support))
print("Columns:", len(support.columns))

print("\nMissing values:")
print(support.isna().sum())

print("\nDuplicate ticket IDs:")
print(
    support["ticket_id"].duplicated().sum()
)

print("\nMessy support_tickets.csv saved successfully!")

# ==================================================
# CUSTOMER FEEDBACK DATA QUALITY ISSUES
# ==================================================

print("\n" + "=" * 60)
print("INTRODUCING CUSTOMER FEEDBACK DATA QUALITY ISSUES")
print("=" * 60)

feedback = pd.read_csv(
    CLEAN_DIR / "customer_feedback.csv",
    dtype={
        "feedback_id": "object",
        "customer_id": "object",
        "feedback_date": "object",
        "feedback_type": "object",
        "rating": "object",
        "sentiment": "object",
        "feedback_text": "object"
    }
)

print("Original customer feedback:", feedback.shape)

# --------------------------------------------------
# 1. Customer ID whitespace
# --------------------------------------------------

np.random.seed(60)

customer_indices = np.random.choice(
    feedback.index,
    size=100,
    replace=False
)

feedback.loc[customer_indices, "customer_id"] = (
    feedback.loc[customer_indices, "customer_id"] + " "
)

# --------------------------------------------------
# 2. Inconsistent feedback type formatting
# --------------------------------------------------

np.random.seed(61)

type_indices = np.random.choice(
    feedback.index,
    size=150,
    replace=False
)

type_variants = {
    "Product Review": "product review",
    "Survey": "SURVEY",
    "Feature Request": "feature request",
    "General Feedback": " GENERAL FEEDBACK",
    "Cancellation Feedback": "cancellation feedback"
}

for idx in type_indices:
    original = feedback.loc[idx, "feedback_type"]

    if original in type_variants:
        feedback.loc[idx, "feedback_type"] = (
            type_variants[original]
        )

# --------------------------------------------------
# 3. Inconsistent sentiment formatting
# --------------------------------------------------

np.random.seed(62)

sentiment_indices = np.random.choice(
    feedback.index,
    size=150,
    replace=False
)

sentiment_variants = {
    "Positive": "positive",
    "Negative": "NEGATIVE",
    "Neutral": " neutral"
}

for idx in sentiment_indices:
    original = feedback.loc[idx, "sentiment"]

    if original in sentiment_variants:
        feedback.loc[idx, "sentiment"] = (
            sentiment_variants[original]
        )

# --------------------------------------------------
# 4. Missing ratings
# --------------------------------------------------

np.random.seed(63)

rating_indices = np.random.choice(
    feedback.index,
    size=80,
    replace=False
)

feedback.loc[
    rating_indices,
    "rating"
] = None

# --------------------------------------------------
# 5. Mixed feedback dates
# --------------------------------------------------

np.random.seed(64)

date_indices = np.random.choice(
    feedback.index,
    size=200,
    replace=False
)

feedback.loc[date_indices, "feedback_date"] = (
    pd.to_datetime(
        feedback.loc[date_indices, "feedback_date"]
    ).dt.strftime("%m/%d/%Y")
)

# --------------------------------------------------
# 6. Extra whitespace in feedback text
# --------------------------------------------------

np.random.seed(65)

text_indices = np.random.choice(
    feedback.index,
    size=150,
    replace=False
)

feedback.loc[text_indices, "feedback_text"] = (
    "  " +
    feedback.loc[
        text_indices,
        "feedback_text"
    ].astype(str) +
    "  "
)

# --------------------------------------------------
# 7. Duplicate feedback records
# --------------------------------------------------

np.random.seed(66)

duplicate_indices = np.random.choice(
    feedback.index,
    size=20,
    replace=False
)

duplicate_rows = feedback.loc[
    duplicate_indices
].copy()

feedback = pd.concat(
    [feedback, duplicate_rows],
    ignore_index=True
)

# --------------------------------------------------
# 8. Save messy feedback data
# --------------------------------------------------

feedback.to_csv(
    RAW_DIR / "customer_feedback.csv",
    index=False
)

print("\nCustomer feedback after introducing issues:")
print("Rows:", len(feedback))
print("Columns:", len(feedback.columns))

print("\nMissing values:")
print(feedback.isna().sum())

print("\nDuplicate feedback IDs:")
print(
    feedback["feedback_id"].duplicated().sum()
)

print("\nMessy customer_feedback.csv saved successfully!")