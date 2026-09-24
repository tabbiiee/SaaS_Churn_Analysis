import pandas as pd
import numpy as np
import random
from faker import Faker
from pathlib import Path


# -----------------------------
# 1. SETUP
# -----------------------------

fake = Faker()

random.seed(42)
np.random.seed(42)


# -----------------------------
# 2. DATASET SIZE
# -----------------------------

NUM_CUSTOMERS = 5000


# -----------------------------
# 3. BUSINESS DATA
# -----------------------------

industries = [
    "Retail",
    "Professional Services",
    "Construction",
    "Hospitality",
    "Healthcare",
    "Technology",
    "Education",
    "Manufacturing",
    "Logistics",
    "Real Estate"
]

countries = [
    "Kenya",
    "Uganda",
    "Tanzania",
    "Rwanda",
    "Ghana",
    "Nigeria",
    "South Africa"
]

cities = [
    "Nairobi",
    "Mombasa",
    "Kisumu",
    "Nakuru",
    "Kampala",
    "Dar es Salaam",
    "Kigali",
    "Accra",
    "Lagos",
    "Johannesburg"
]

company_sizes = [
    "1-5",
    "6-10",
    "11-50",
    "51-200",
    "201-500"
]

acquisition_channels = [
    "Organic Search",
    "Google Ads",
    "Facebook",
    "Instagram",
    "Referral",
    "Partner",
    "Sales Team",
    "LinkedIn"
]

plans = {
    "Starter": 1500,
    "Professional": 4500,
    "Business": 9000,
    "Enterprise": 20000
}

billing_cycles = [
    "Monthly",
    "Annual"
]

cancellation_reasons = [
    "Too expensive",
    "Not using the product enough",
    "Missing features",
    "Poor customer support",
    "Switched to competitor",
    "Business closed",
    "Business downsized",
    "Payment issues"
]


# -----------------------------
# 4. GENERATE CUSTOMERS
# -----------------------------

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"CUST{i:05d}"

    customer = {
        "customer_id": customer_id,

        "company_name": fake.company(),

        "industry": random.choice(
            industries
        ),

        "country": random.choice(
            countries
        ),

        "city": random.choice(
            cities
        ),

        "company_size": random.choice(
            company_sizes
        ),

        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="-30d"
        ),

        "acquisition_channel": random.choice(
            acquisition_channels
        )
    }

    customers.append(customer)


customers_df = pd.DataFrame(
    customers
)


# -----------------------------
# 5. ASSIGN HIDDEN BEHAVIOR
# -----------------------------

customer_behavior = {}

for customer_id in customers_df["customer_id"]:

    behavior = random.choices(
        [
            "healthy",
            "price_sensitive",
            "support_frustrated",
            "low_engagement"
        ],
        weights=[55, 15, 15, 15]
    )[0]

    customer_behavior[customer_id] = behavior


# -----------------------------
# 6. GENERATE SUBSCRIPTIONS
# -----------------------------

subscriptions = []

today = pd.Timestamp.today().normalize()


for _, customer in customers_df.iterrows():

    customer_id = customer["customer_id"]

    signup_date = pd.to_datetime(
        customer["signup_date"]
    )

    behavior = customer_behavior[
        customer_id
    ]


    # ---------------------------------
    # Choose plan
    # ---------------------------------

    plan = random.choices(
        list(plans.keys()),
        weights=[40, 35, 18, 7]
    )[0]

    monthly_price = plans[plan]


    # ---------------------------------
    # Choose billing cycle
    # ---------------------------------

    billing_cycle = random.choices(
        billing_cycles,
        weights=[80, 20]
    )[0]


    # ---------------------------------
    # Base churn probability
    # ---------------------------------

    churn_probability = 0.15


    # ---------------------------------
    # Adjust churn probability
    # based on customer behavior
    # ---------------------------------

    if behavior == "price_sensitive":

        churn_probability += 0.15

    elif behavior == "support_frustrated":

        churn_probability += 0.12

    elif behavior == "low_engagement":

        churn_probability += 0.18

    else:

        churn_probability -= 0.05


    # ---------------------------------
    # Enterprise customers
    # ---------------------------------

    if plan == "Enterprise":

        churn_probability -= 0.08


    # ---------------------------------
    # Annual customers
    # ---------------------------------

    if billing_cycle == "Annual":

        churn_probability -= 0.05


    # ---------------------------------
    # Keep probability reasonable
    # ---------------------------------

    churn_probability = max(
        0.03,
        min(
            churn_probability,
            0.60
        )
    )


    # ---------------------------------
    # Determine churn
    # ---------------------------------

    churned = (
        np.random.random()
        < churn_probability
    )


    # ---------------------------------
    # Minimum subscription period
    # ---------------------------------

    min_end_date = (
        signup_date
        + pd.DateOffset(months=2)
    )


    # ---------------------------------
    # Maximum subscription period
    # ---------------------------------

    max_end_date = (
        signup_date
        + pd.DateOffset(months=36)
    )


    # ---------------------------------
    # Determine cancellation
    # ---------------------------------

    if (
        churned
        and min_end_date <= today
    ):

        latest_possible_date = min(
            max_end_date,
            today
        )


        # Make sure date range is valid

        if (
            min_end_date
            <= latest_possible_date
        ):

            cancellation_date = (
                fake.date_between(
                    start_date=min_end_date.date(),
                    end_date=latest_possible_date.date()
                )
            )

            end_date = cancellation_date

            status = "Cancelled"


            # -----------------------------
            # Cancellation reason
            # -----------------------------

            if behavior == "price_sensitive":

                reason = random.choice([
                    "Too expensive",
                    "Business downsized"
                ])


            elif behavior == "support_frustrated":

                reason = random.choice([
                    "Poor customer support",
                    "Missing features"
                ])


            elif behavior == "low_engagement":

                reason = random.choice([
                    "Not using the product enough",
                    "Switched to competitor"
                ])


            else:

                reason = random.choice(
                    cancellation_reasons
                )

        else:

            end_date = None

            cancellation_date = None

            status = "Active"

            reason = None

    else:

        end_date = None

        cancellation_date = None

        status = "Active"

        reason = None


    # ---------------------------------
    # Create subscription record
    # ---------------------------------

    subscription = {

        "subscription_id":
            f"SUB{len(subscriptions) + 1:05d}",

        "customer_id":
            customer_id,

        "plan":
            plan,

        "billing_cycle":
            billing_cycle,

        "monthly_price":
            monthly_price,

        "start_date":
            signup_date.date(),

        "end_date":
            end_date,

        "status":
            status,

        "cancellation_date":
            cancellation_date,

        "cancellation_reason":
            reason
    }


    subscriptions.append(
        subscription
    )


subscriptions_df = pd.DataFrame(
    subscriptions
)


# -----------------------------
# 7. GENERATE USAGE ACTIVITY
# -----------------------------

usage_records = []


for _, customer in customers_df.iterrows():

    customer_id = customer["customer_id"]


    # Get customer's hidden behavior

    behavior = customer_behavior[
        customer_id
    ]


    # ---------------------------------
    # Find customer's subscription
    # ---------------------------------

    subscription = subscriptions_df[
        subscriptions_df["customer_id"]
        == customer_id
    ].iloc[0]


    start_date = pd.to_datetime(
        subscription["start_date"]
    )


    # ---------------------------------
    # Determine activity end date
    # ---------------------------------

    if (
        subscription["status"]
        == "Cancelled"
    ):

        end_date = pd.to_datetime(
            subscription["cancellation_date"]
        )

    else:

        end_date = today


    # ---------------------------------
    # Generate one record per month
    # ---------------------------------

    months = pd.date_range(
        start=start_date.to_period(
            "M"
        ).to_timestamp(),

        end=end_date.to_period(
            "M"
        ).to_timestamp(),

        freq="MS"
    )


    for month_number, month in enumerate(
        months
    ):


        # -----------------------------
        # BASE USAGE
        # -----------------------------

        login_count = max(
            0,
            int(
                np.random.normal(
                    20,
                    6
                )
            )
        )


        session_minutes = max(
            10,
            int(
                np.random.normal(
                    500,
                    150
                )
            )
        )


        invoices_created = max(
            0,
            int(
                np.random.normal(
                    35,
                    12
                )
            )
        )


        reports_generated = max(
            0,
            int(
                np.random.normal(
                    8,
                    3
                )
            )
        )


        active_users = max(
            1,
            int(
                np.random.normal(
                    4,
                    2
                )
            )
        )


        features_used = max(
            1,
            int(
                np.random.normal(
                    5,
                    1.5
                )
            )
        )


        # -----------------------------
        # BEHAVIOR EFFECTS
        # -----------------------------

        if behavior == "low_engagement":

            decline = max(
                0.15,
                1 - (
                    month_number
                    * 0.08
                )
            )


            login_count = int(
                login_count
                * decline
            )


            session_minutes = int(
                session_minutes
                * decline
            )


            invoices_created = int(
                invoices_created
                * decline
            )


            reports_generated = int(
                reports_generated
                * decline
            )


        elif behavior == "healthy":

            growth = 1 + min(
                month_number
                * 0.01,
                0.15
            )


            login_count = int(
                login_count
                * growth
            )


            invoices_created = int(
                invoices_created
                * growth
            )


        elif behavior == "price_sensitive":

            login_count = int(
                login_count
                * np.random.uniform(
                    0.8,
                    1.1
                )
            )


        elif behavior == "support_frustrated":

            decline = max(
                0.60,
                1 - (
                    month_number
                    * 0.03
                )
            )


            login_count = int(
                login_count
                * decline
            )


            session_minutes = int(
                session_minutes
                * decline
            )


        # -----------------------------
        # CREATE USAGE RECORD
        # -----------------------------

        usage_record = {

            "activity_id":
                f"ACT{len(usage_records) + 1:07d}",

            "customer_id":
                customer_id,

            "month":
                month.date(),

            "login_count":
                login_count,

            "session_minutes":
                session_minutes,

            "invoices_created":
                invoices_created,

            "reports_generated":
                reports_generated,

            "active_users":
                active_users,

            "features_used":
                features_used
        }


        usage_records.append(
            usage_record
        )


usage_df = pd.DataFrame(
    usage_records
)


# ============================================================
# 8. GENERATE PAYMENTS
# ============================================================

payment_methods = [
    "M-Pesa",
    "Bank Transfer",
    "Credit Card",
    "Debit Card"
]

payment_statuses = [
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Late",
    "Failed"
]

payment_records = []
payment_id = 1

for _, sub in subscriptions_df.iterrows():

    customer_id = sub["customer_id"]
    plan = sub["plan"]
    monthly_price = sub["monthly_price"]
    billing_cycle = sub["billing_cycle"]
    start_date = pd.to_datetime(sub["start_date"])
    status = sub["status"]
    cancellation_date = sub["cancellation_date"]

    behavior = customer_behavior[customer_id]

    # Determine payment frequency
    if billing_cycle == "Monthly":
        payment_frequency = "monthly"
    else:
        payment_frequency = "annual"

    # Determine final payment date
    if status == "Cancelled" and pd.notna(cancellation_date):
        final_date = pd.to_datetime(cancellation_date)
    else:
        final_date = pd.Timestamp.today().normalize()

    # Generate payment dates
    if payment_frequency == "monthly":

        payment_dates = pd.date_range(
            start=start_date,
            end=final_date,
            freq="MS"
        )

    else:

        payment_dates = pd.date_range(
            start=start_date,
            end=final_date,
            freq="12MS"
        )

    for payment_date in payment_dates:

        # Base probability of payment problems
        failure_probability = 0.03

        if behavior == "price_sensitive":
            failure_probability += 0.04

        elif behavior == "support_frustrated":
            failure_probability += 0.02

        elif behavior == "low_engagement":
            failure_probability += 0.05

        # Random payment outcome
        random_value = np.random.random()

        if random_value < failure_probability:
            payment_status = "Failed"

        elif random_value < failure_probability + 0.07:
            payment_status = "Late"

        else:
            payment_status = "Successful"

        # Payment date
        if payment_status == "Successful":
            actual_payment_date = payment_date + pd.Timedelta(
                days=np.random.randint(0, 4)
            )

        elif payment_status == "Late":
            actual_payment_date = payment_date + pd.Timedelta(
                days=np.random.randint(5, 21)
            )

        else:
            actual_payment_date = payment_date + pd.Timedelta(
                days=np.random.randint(1, 8)
            )

        # Payment amount
        if billing_cycle == "Monthly":
            amount = monthly_price

        else:
            amount = monthly_price * 12

        # Failed payments don't generate revenue
        if payment_status == "Failed":
            paid_amount = 0
        else:
            paid_amount = amount

        payment_method = random.choice(payment_methods)

        # Generate transaction reference
        transaction_id = f"TXN{payment_id:08d}"

        payment_records.append({
            "payment_id": f"PAY{payment_id:08d}",
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "subscription_id": sub["subscription_id"],
            "payment_date": actual_payment_date.strftime("%Y-%m-%d"),
            "payment_method": payment_method,
            "amount": amount,
            "paid_amount": paid_amount,
            "payment_status": payment_status
        })

        payment_id += 1


payments_df = pd.DataFrame(payment_records)

# ============================================================
# 10. GENERATE SUPPORT TICKETS
# ============================================================

ticket_categories = [
    "Billing",
    "Technical Issue",
    "Account Access",
    "Feature Request",
    "Bug Report",
    "Integration",
    "How-To Question",
    "Performance"
]

ticket_priorities = [
    "Low",
    "Medium",
    "High",
    "Urgent"
]

ticket_statuses = [
    "Resolved",
    "Resolved",
    "Resolved",
    "Open",
    "Pending"
]

support_tickets = []

ticket_id = 1

for _, customer in customers_df.iterrows():

    customer_id = customer["customer_id"]

    behavior = customer_behavior[customer_id]

    # Find customer's subscription
    subscription = subscriptions_df[
        subscriptions_df["customer_id"] == customer_id
    ].iloc[0]

    start_date = pd.to_datetime(
        subscription["start_date"]
    )

    if subscription["status"] == "Cancelled":

        end_date = pd.to_datetime(
            subscription["cancellation_date"]
        )

    else:

        end_date = today

    # ---------------------------------------------
    # Determine number of tickets
    # ---------------------------------------------

    if behavior == "support_frustrated":

        number_of_tickets = np.random.poisson(5)

    elif behavior == "low_engagement":

        number_of_tickets = np.random.poisson(2)

    elif behavior == "price_sensitive":

        number_of_tickets = np.random.poisson(3)

    else:

        number_of_tickets = np.random.poisson(2)

    # Make sure some customers have tickets
    number_of_tickets = max(
        0,
        number_of_tickets
    )

    # ---------------------------------------------
    # Generate tickets
    # ---------------------------------------------

    for _ in range(number_of_tickets):

        # Make sure the ticket date falls
        # within the customer's subscription
        ticket_date = fake.date_between(
            start_date=start_date.date(),
            end_date=end_date.date()
        )

        # -----------------------------------------
        # Choose issue category
        # -----------------------------------------

        if behavior == "price_sensitive":

            category = random.choice([
                "Billing",
                "Feature Request",
                "Performance",
                "How-To Question"
            ])

        elif behavior == "support_frustrated":

            category = random.choice([
                "Technical Issue",
                "Bug Report",
                "Integration",
                "Performance",
                "Account Access"
            ])

        elif behavior == "low_engagement":

            category = random.choice([
                "How-To Question",
                "Feature Request",
                "Account Access"
            ])

        else:

            category = random.choice(
                ticket_categories
            )

        # -----------------------------------------
        # Choose priority
        # -----------------------------------------

        priority = random.choices(
            ticket_priorities,
            weights=[45, 40, 12, 3]
        )[0]

        # -----------------------------------------
        # Resolution time
        # -----------------------------------------

        if priority == "Urgent":

            resolution_hours = max(
                2,
                int(np.random.normal(12, 5))
            )

        elif priority == "High":

            resolution_hours = max(
                4,
                int(np.random.normal(24, 10))
            )

        elif priority == "Medium":

            resolution_hours = max(
                8,
                int(np.random.normal(48, 20))
            )

        else:

            resolution_hours = max(
                12,
                int(np.random.normal(72, 30))
            )

        # Support-frustrated customers experience
        # longer resolution times

        if behavior == "support_frustrated":

            resolution_hours = int(
                resolution_hours
                * np.random.uniform(1.3, 2.0)
            )

        # -----------------------------------------
        # Ticket status
        # -----------------------------------------

        ticket_status = random.choices(
            ticket_statuses,
            weights=[75, 75, 75, 10, 15]
        )[0]

        # -----------------------------------------
        # Customer satisfaction
        # -----------------------------------------

        if behavior == "support_frustrated":

            satisfaction = random.choices(
                [1, 2, 3, 4, 5],
                weights=[35, 30, 20, 10, 5]
            )[0]

        elif behavior == "healthy":

            satisfaction = random.choices(
                [1, 2, 3, 4, 5],
                weights=[2, 5, 15, 35, 43]
            )[0]

        else:

            satisfaction = random.choices(
                [1, 2, 3, 4, 5],
                weights=[8, 12, 25, 30, 25]
            )[0]

        # -----------------------------------------
        # Create ticket
        # -----------------------------------------

        ticket = {

            "ticket_id":
                f"TICK{ticket_id:07d}",

            "customer_id":
                customer_id,

            "ticket_date":
                ticket_date,

            "issue_category":
                category,

            "priority":
                priority,

            "resolution_hours":
                resolution_hours,

            "ticket_status":
                ticket_status,

            "customer_satisfaction":
                satisfaction
        }

        support_tickets.append(ticket)

        ticket_id += 1


support_tickets_df = pd.DataFrame(
    support_tickets
)
# ============================================================
# 6. GENERATE CUSTOMER FEEDBACK
# ============================================================

feedback_types = [
    "Product Review",
    "Survey",
    "Cancellation Feedback",
    "Feature Request",
    "General Feedback"
]

feedback_records = []

feedback_id = 1

for _, customer in customers_df.iterrows():

    customer_id = customer["customer_id"]

    behavior = customer_behavior[customer_id]

    # Find customer's subscription
    subscription = subscriptions_df[
        subscriptions_df["customer_id"] == customer_id
    ].iloc[0]

    start_date = pd.to_datetime(
        subscription["start_date"]
    )

    if subscription["status"] == "Cancelled":

        end_date = pd.to_datetime(
            subscription["cancellation_date"]
        )

    else:

        end_date = today

    # ---------------------------------------------
    # Determine number of feedback records
    # ---------------------------------------------

    if behavior == "support_frustrated":

        number_of_feedback = np.random.poisson(2)

    elif behavior == "low_engagement":

        number_of_feedback = np.random.poisson(1.5)

    elif behavior == "price_sensitive":

        number_of_feedback = np.random.poisson(1.5)

    else:

        number_of_feedback = np.random.poisson(1)

    number_of_feedback = max(
        0,
        number_of_feedback
    )

    # ---------------------------------------------
    # Generate feedback records
    # ---------------------------------------------

    for _ in range(number_of_feedback):

        feedback_date = fake.date_between(
            start_date=start_date.date(),
            end_date=end_date.date()
        )

        # -----------------------------------------
        # Feedback type
        # -----------------------------------------

        if subscription["status"] == "Cancelled":

            feedback_type = random.choices(
                feedback_types,
                weights=[15, 10, 55, 10, 10]
            )[0]

        else:

            feedback_type = random.choices(
                feedback_types,
                weights=[30, 30, 5, 20, 15]
            )[0]

        # -----------------------------------------
        # Rating + sentiment
        # -----------------------------------------

        if behavior == "healthy":

            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[2, 4, 12, 32, 50]
            )[0]

        elif behavior == "price_sensitive":

            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[10, 20, 30, 25, 15]
            )[0]

        elif behavior == "support_frustrated":

            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[35, 30, 20, 10, 5]
            )[0]

        else:

            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[15, 20, 30, 25, 10]
            )[0]

        # -----------------------------------------
        # Sentiment based on rating
        # -----------------------------------------

        if rating <= 2:

            sentiment = "Negative"

        elif rating == 3:

            sentiment = "Neutral"

        else:

            sentiment = "Positive"

        # -----------------------------------------
        # Feedback text
        # -----------------------------------------

        if behavior == "price_sensitive":

            feedback_text = random.choice([
                "The platform is useful but the price is becoming expensive.",
                "We like the product but the monthly cost is high.",
                "The pricing is difficult for our business.",
                "We would like more value for the current subscription price."
            ])

        elif behavior == "support_frustrated":

            feedback_text = random.choice([
                "We have experienced several issues with customer support.",
                "Some support requests took too long to resolve.",
                "We need faster responses when technical problems occur.",
                "The product is useful but support needs improvement."
            ])

        elif behavior == "low_engagement":

            feedback_text = random.choice([
                "We are not using the platform as much as we expected.",
                "Some of the features are not being used by our team.",
                "Our usage of the platform has decreased recently.",
                "We are finding it difficult to get our team to use the platform regularly."
            ])

        else:

            feedback_text = random.choice([
                "The platform has been useful for managing our business.",
                "We especially like the reporting features.",
                "The system has helped our team manage invoices more efficiently.",
                "The platform is easy to use and useful for our daily operations.",
                "We are happy with the features available."
            ])

        # -----------------------------------------
        # Create feedback record
        # -----------------------------------------

        feedback = {

            "feedback_id":
                f"FDBK{feedback_id:07d}",

            "customer_id":
                customer_id,

            "feedback_date":
                feedback_date,

            "feedback_type":
                feedback_type,

            "rating":
                rating,

            "sentiment":
                sentiment,

            "feedback_text":
                feedback_text
        }

        feedback_records.append(
            feedback
        )

        feedback_id += 1


feedback_df = pd.DataFrame(
    feedback_records
)
# ============================================================
# SAVE CUSTOMER FEEDBACK
# ============================================================

feedback_df.to_csv(
    "raw_data/customer_feedback.csv",
    index=False
)

# ============================================================
# SAVE PAYMENTS
# ============================================================

payments_df.to_csv(
    "raw_data/payments.csv",
    index=False
)
# ============================================================
# SAVE SUPPORT TICKETS
# ============================================================

support_tickets_df.to_csv(
    "raw_data/support_tickets.csv",
    index=False
)

# ============================================================
# PAYMENT SUMMARY
# ============================================================

print("\nFirst 10 payments:")
print(payments_df.head(10))

print("\nPayment dataset shape:")
print(payments_df.shape)

print("\nPayment status:")
print(payments_df["payment_status"].value_counts())

print("\nPayment methods:")
print(payments_df["payment_method"].value_counts())

print("\nTotal billed amount:")
print(payments_df["amount"].sum())

print("\nTotal paid amount:")
print(payments_df["paid_amount"].sum())

print("\nPayments dataset created successfully!")

# -----------------------------
# 9. DISPLAY RESULTS
# -----------------------------

print("\nFirst 10 customers:")
print(
    customers_df.head(10)
)


print("\nCustomer dataset shape:")
print(
    customers_df.shape
)


print("\nFirst 10 subscriptions:")
print(
    subscriptions_df.head(10)
)


print("\nSubscription dataset shape:")
print(
    subscriptions_df.shape
)


print("\nSubscription status:")
print(
    subscriptions_df[
        "status"
    ].value_counts()
)


print("\nPlan distribution:")
print(
    subscriptions_df[
        "plan"
    ].value_counts()
)


print("\nBilling cycle distribution:")
print(
    subscriptions_df[
        "billing_cycle"
    ].value_counts()
)


print("\nCancellation reasons:")
print(
    subscriptions_df[
        subscriptions_df["status"]
        == "Cancelled"
    ]["cancellation_reason"]
    .value_counts()
)


print("\nFirst 10 usage records:")
print(
    usage_df.head(10)
)


print("\nUsage dataset shape:")
print(
    usage_df.shape
)
print("\nFirst 10 support tickets:")
print(
    support_tickets_df.head(10)
)

print("\nSupport ticket dataset shape:")
print(
    support_tickets_df.shape
)

print("\nTicket status:")
print(
    support_tickets_df[
        "ticket_status"
    ].value_counts()
)

print("\nIssue categories:")
print(
    support_tickets_df[
        "issue_category"
    ].value_counts()
)

print("\nAverage resolution time:")
print(
    support_tickets_df[
        "resolution_hours"
    ].mean()
)

print("\nAverage customer satisfaction:")
print(
    support_tickets_df[
        "customer_satisfaction"
    ].mean()
)
print("\nFirst 10 customer feedback records:")
print(
    feedback_df.head(10)
)

print("\nFeedback dataset shape:")
print(
    feedback_df.shape
)

print("\nFeedback types:")
print(
    feedback_df[
        "feedback_type"
    ].value_counts()
)

print("\nFeedback sentiment:")
print(
    feedback_df[
        "sentiment"
    ].value_counts()
)

print("\nAverage feedback rating:")
print(
    feedback_df[
        "rating"
    ].mean()
)
# -----------------------------
# 9. SAVE DATA
# -----------------------------

# Make sure raw_data folder exists

Path("raw_data").mkdir(
    parents=True,
    exist_ok=True
)


customers_df.to_csv(
    "raw_data/customers.csv",
    index=False
)


subscriptions_df.to_csv(
    "raw_data/subscriptions.csv",
    index=False
)


usage_df.to_csv(
    "raw_data/usage_activity.csv",
    index=False
)


print(
    "\ncustomers.csv created successfully!"
)

print(
    "subscriptions.csv created successfully!"
)

print(
    "usage_activity.csv created successfully!"
)
print(
    "payments.csv created successfully!"
)
print(
    "support_tickets.csv created successfully!"
)
print(
    "\nDataset generation complete!"
)

