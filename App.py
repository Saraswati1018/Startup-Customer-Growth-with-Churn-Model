import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Startup Customer Growth with Churn", layout="wide")

st.title("📈 Startup Customer Growth with Churn")
st.markdown("""
This project simulates startup customer growth using a **logistic growth model with churn**.

### Model Components
- **New Customers**: customers acquired at each time step
- **Active Customers**: currently retained customers
- **Churned Customers**: customers leaving the startup

### Included Features
- Customer acquisition and dropout simulation
- Logistic growth + parameter estimation
- Retention analysis
- Growth visualization
""")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Simulation Inputs")

k = st.sidebar.number_input(
    "Carrying Capacity (Maximum Customers)",
    min_value=100,
    max_value=1000000,
    value=10000,
    step=100
)

r = st.sidebar.number_input(
    "Growth Rate (r)",
    min_value=0.01,
    max_value=5.0,
    value=0.30,
    step=0.01
)

churn_rate = st.sidebar.number_input(
    "Churn Rate",
    min_value=0.00,
    max_value=1.00,
    value=0.05,
    step=0.01
)

time_steps = st.sidebar.number_input(
    "Number of Time Steps",
    min_value=1,
    max_value=300,
    value=50,
    step=1
)

initial_active = st.sidebar.number_input(
    "Initial Active Customers",
    min_value=1.0,
    max_value=float(k),
    value=100.0,
    step=10.0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Parameter Estimation")
observed_final_active = st.sidebar.number_input(
    "Observed Final Active Customers (optional)",
    min_value=0.0,
    value=0.0,
    step=10.0,
    help="Enter a real observed final customer count to estimate growth rate r"
)

run_button = st.sidebar.button("Run Simulation")

# -----------------------------
# Core Simulation Function
# -----------------------------
def simulate_growth(r, k, churn_rate, time_steps, initial_active):
    active = initial_active

    active_list = []
    new_list = []
    churn_list = []
    retention_list = []

    for t in range(time_steps):
        new_customers = r * active * (1 - active / k)
        churned = churn_rate * active
        active = active + new_customers - churned

        if active < 0:
            active = 0

        retention_rate = ((active - new_customers) / (active - new_customers + churned)) if (active - new_customers + churned) > 0 else 0

        active_list.append(active)
        new_list.append(new_customers)
        churn_list.append(churned)
        retention_list.append(retention_rate)

    peak_active = max(active_list)
    peak_time = active_list.index(peak_active) + 1

    return active_list, new_list, churn_list, retention_list, peak_active, peak_time


# -----------------------------
# Parameter Estimation Function
# Estimate growth rate r from observed final active customers
# -----------------------------
def estimate_growth_rate(observed_final, k, churn_rate, time_steps, initial_active):
    best_r = None
    best_error = float("inf")

    candidate_rs = np.linspace(0.01, 2.0, 1000)

    for candidate_r in candidate_rs:
        active_list, _, _, _, _, _ = simulate_growth(candidate_r, k, churn_rate, time_steps, initial_active)
        predicted_final = active_list[-1]
        error = abs(predicted_final - observed_final)

        if error < best_error:
            best_error = error
            best_r = candidate_r

    return best_r, best_error


# -----------------------------
# Run App
# -----------------------------
if run_button or True:
    estimated_r = None
    estimation_error = None

    if observed_final_active > 0:
        estimated_r, estimation_error = estimate_growth_rate(
            observed_final_active, k, churn_rate, time_steps, initial_active
        )
        r_to_use = estimated_r
    else:
        r_to_use = r

    active_list, new_list, churn_list, retention_list, peak_active, peak_time = simulate_growth(
        r_to_use, k, churn_rate, time_steps, initial_active
    )

    final_active = active_list[-1]
    final_churned = sum(churn_list)
    avg_retention = np.mean(retention_list) * 100 if len(retention_list) > 0 else 0
    overall_retention = (final_active / k) * 100

    # -----------------------------
    # Metrics
    # -----------------------------
    st.subheader("Key Results")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Peak Active Customers", f"{peak_active:.2f}")
    c2.metric("Peak Time Step", f"{peak_time}")
    c3.metric("Final Active Customers", f"{final_active:.2f}")
    c4.metric("Average Retention (%)", f"{avg_retention:.2f}")

    if estimated_r is not None:
        st.success(f"Estimated Growth Rate (r): {estimated_r:.4f}")
        st.info(f"Estimation Error: {estimation_error:.4f}")

    # -----------------------------
    # Growth Visualization
    # -----------------------------
    st.subheader("Growth Visualization")

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(active_list, label="Active Customers")
    ax1.plot(new_list, label="New Customers")
    ax1.plot(churn_list, label="Churned Customers")
    ax1.set_title("Startup Customer Growth with Churn")
    ax1.set_xlabel("Time Step")
    ax1.set_ylabel("Number of Customers")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # -----------------------------
    # Retention Analysis
    # -----------------------------
    st.subheader("Retention Analysis")

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot([x * 100 for x in retention_list], label="Retention Rate (%)")
    ax2.set_title("Retention Trend Over Time")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Retention Percentage")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    # -----------------------------
    # Detailed Interpretation
    # -----------------------------
    st.subheader("Model Interpretation")
    st.write(f"""
This simulation models startup customer dynamics using a logistic growth equation with churn.

The **growth rate (r)** controls how quickly new customers are acquired.
The **carrying capacity (k)** represents the maximum possible customer base.
The **churn rate** represents the fraction of active customers who leave at each time step.

At every time step:
- **New customers** are added using logistic growth.
- **Churned customers** are removed using the churn formula.
- **Active customers** are updated accordingly.

The maximum number of active customers reached is **{peak_active:.2f}**, which occurs at **time step {peak_time}**.
The final active customer count is **{final_active:.2f}**.
The total churn across the simulation is **{final_churned:.2f}**.
The average retention during the simulation is **{avg_retention:.2f}%**.
""")

    # -----------------------------
    # Backend Equations
    # -----------------------------
    st.subheader("Backend Equations Used")
    st.code(
        """new_customers = r * active * (1 - active / k)
churned = churn_rate * active
active = active + new_customers - churned""",
        language="python"
    )

    # -----------------------------
    # Conclusion
    # -----------------------------
    st.subheader("Conclusion")
    st.write("""
This project helps analyze startup growth by combining customer acquisition, churn, retention, and parameter estimation.
It is useful for understanding whether a startup is growing sustainably, losing too many customers, or approaching its maximum customer capacity.
""")
