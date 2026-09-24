import pandas as pd
from pathlib import Path


# ============================================================
# 1. LOAD DATA
# ============================================================

data_path = Path("raw_data")

customers = pd.read_csv(
    data_path / "customers.csv"
)

subscriptions = pd.read_csv(
    data_path / "subscriptions.csv"
)

payments = pd.read_csv(
    data_path / "payments.csv"
)

usage = pd.read_csv(
    data_path / "usage_activity.csv"
)

support = pd.read_csv(
    data_path / "support_tickets.csv"
)

feedback = pd.read_csv(
    data_path / "customer_feedback.csv"
)


print("=" * 60)
print("DATASET VALIDATION")
print("=" * 60)


# ============================================================
# 2. DATASET SIZES
# ============================================================

print("\nDATASET SIZES")

print("Customers:", customers.shape)
print("Subscriptions:", subscriptions.shape)
print("Payments:", payments.shape)
print("Usage:", usage.shape)
print("Support:", support.shape)
print("Feedback:", feedback.shape)


# ============================================================
# 3. DUPLICATE ID CHECKS
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE ID CHECKS")
print("=" * 60)

print(
    "Duplicate customer IDs:",
    customers["customer_id"].duplicated().sum()
)

print(
    "Duplicate subscription IDs:",
    subscriptions["subscription_id"].duplicated().sum()
)

print(
    "Duplicate payment IDs:",
    payments["payment_id"].duplicated().sum()
)

print(
    "Duplicate transaction IDs:",
    payments["transaction_id"].duplicated().sum()
)

print(
    "Duplicate activity IDs:",
    usage["activity_id"].duplicated().sum()
)

print(
    "Duplicate ticket IDs:",
    support["ticket_id"].duplicated().sum()
)

print(
    "Duplicate feedback IDs:",
    feedback["feedback_id"].duplicated().sum()
)


# ============================================================
# 4. MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print("\nCustomers:")
print(customers.isna().sum())

print("\nSubscriptions:")
print(subscriptions.isna().sum())

print("\nPayments:")
print(payments.isna().sum())

print("\nUsage:")
print(usage.isna().sum())

print("\nSupport:")
print(support.isna().sum())

print("\nFeedback:")
print(feedback.isna().sum())


# ============================================================
# 5. FOREIGN KEY CHECKS
# ============================================================

print("\n" + "=" * 60)
print("FOREIGN KEY CHECKS")
print("=" * 60)


customer_ids = set(
    customers["customer_id"]
)


subscription_ids = set(
    subscriptions["subscription_id"]
)


# Payments → Customers

invalid_payment_customers = (
    ~payments["customer_id"].isin(customer_ids)
).sum()

print(
    "Payments with invalid customer IDs:",
    invalid_payment_customers
)


# Payments → Subscriptions

invalid_payment_subscriptions = (
    ~payments["subscription_id"].isin(subscription_ids)
).sum()

print(
    "Payments with invalid subscription IDs:",
    invalid_payment_subscriptions
)


# Usage → Customers

invalid_usage_customers = (
    ~usage["customer_id"].isin(customer_ids)
).sum()

print(
    "Usage records with invalid customer IDs:",
    invalid_usage_customers
)


# Support → Customers

invalid_support_customers = (
    ~support["customer_id"].isin(customer_ids)
).sum()

print(
    "Support tickets with invalid customer IDs:",
    invalid_support_customers
)


# Feedback → Customers

invalid_feedback_customers = (
    ~feedback["customer_id"].isin(customer_ids)
).sum()

print(
    "Feedback records with invalid customer IDs:",
    invalid_feedback_customers
)


# ============================================================
# 6. PAYMENT VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("PAYMENT VALIDATION")
print("=" * 60)


failed_with_payment = payments[
    (payments["payment_status"] == "Failed")
    &
    (payments["paid_amount"] > 0)
]

print(
    "Failed payments with money paid:",
    len(failed_with_payment)
)


negative_amounts = payments[
    (payments["amount"] < 0)
    |
    (payments["paid_amount"] < 0)
]

print(
    "Payments with negative amounts:",
    len(negative_amounts)
)


paid_more_than_billed = payments[
    payments["paid_amount"] > payments["amount"]
]

print(
    "Payments where paid amount exceeds billed amount:",
    len(paid_more_than_billed)
)


# ============================================================
# 7. SUBSCRIPTION VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SUBSCRIPTION VALIDATION")
print("=" * 60)


cancelled_without_date = subscriptions[
    (subscriptions["status"] == "Cancelled")
    &
    (subscriptions["cancellation_date"].isna())
]

print(
    "Cancelled subscriptions without cancellation date:",
    len(cancelled_without_date)
)


active_with_cancel_date = subscriptions[
    (subscriptions["status"] == "Active")
    &
    (subscriptions["cancellation_date"].notna())
]

print(
    "Active subscriptions with cancellation date:",
    len(active_with_cancel_date)
)


# ============================================================
# 8. DATE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DATE VALIDATION")
print("=" * 60)


customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

subscriptions["start_date"] = pd.to_datetime(
    subscriptions["start_date"]
)

subscriptions["cancellation_date"] = pd.to_datetime(
    subscriptions["cancellation_date"]
)

payments["payment_date"] = pd.to_datetime(
    payments["payment_date"]
)

usage["month"] = pd.to_datetime(
    usage["month"]
)

support["ticket_date"] = pd.to_datetime(
    support["ticket_date"]
)

feedback["feedback_date"] = pd.to_datetime(
    feedback["feedback_date"]
)


# Subscription before customer signup

subscription_before_signup = subscriptions.merge(
    customers[
        ["customer_id", "signup_date"]
    ],
    on="customer_id"
)

invalid_subscription_dates = subscription_before_signup[
    subscription_before_signup["start_date"]
    <
    subscription_before_signup["signup_date"]
]

print(
    "Subscriptions starting before signup:",
    len(invalid_subscription_dates)
)


# ============================================================
# 9. USAGE AFTER CANCELLATION
# ============================================================

print("\n" + "=" * 60)
print("USAGE VALIDATION")
print("=" * 60)


usage_check = usage.merge(
    subscriptions[
        [
            "customer_id",
            "status",
            "cancellation_date"
        ]
    ],
    on="customer_id"
)


usage_after_cancellation = usage_check[
    (
        usage_check["status"] == "Cancelled"
    )
    &
    (
        usage_check["month"]
        >
        usage_check["cancellation_date"]
    )
]


print(
    "Usage records after cancellation:",
    len(usage_after_cancellation)
)


# ============================================================
# 10. VALUE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VALUE VALIDATION")
print("=" * 60)


negative_usage = usage[
    (usage["login_count"] < 0)
    |
    (usage["session_minutes"] < 0)
    |
    (usage["invoices_created"] < 0)
    |
    (usage["reports_generated"] < 0)
    |
    (usage["active_users"] < 0)
    |
    (usage["features_used"] < 0)
]

print(
    "Usage records with negative values:",
    len(negative_usage)
)


invalid_ratings = feedback[
    (feedback["rating"] < 1)
    |
    (feedback["rating"] > 5)
]

print(
    "Feedback ratings outside 1-5:",
    len(invalid_ratings)
)


negative_resolution = support[
    support["resolution_hours"] < 0
]

print(
    "Support tickets with negative resolution time:",
    len(negative_resolution)
)


# ============================================================
# 11. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)