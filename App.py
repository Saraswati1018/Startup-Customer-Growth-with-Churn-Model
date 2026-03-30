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

k = st.sidebar.number_input("Carrying Capacity (Maximum Customers)", 100, 1000000, 10000, 100)
r = st.sidebar.number_input("Growth Rate (r)", 0.01, 5.0, 0.30, 0.01)
churn_rate = st.sidebar.number_input("Churn Rate", 0.00, 1.00, 0.05, 0.01)
time_steps = st.sidebar.number_input("Number of Time Steps", 1, 300, 50, 1)
initial_active = st.sidebar.number_input("Initial Active Customers", 1.0, float(k), 100.0, 10.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Parameter Estimation")

observed_final_active = st.sidebar.number_input(
    "Observed Final Active Customers (optional)",
    min_value=0.0,
    value=0.0,
    step=10.0
)

run_button = st.sidebar.button("Run Simulation")

# 🔄 Reset Button (simple reload)
reset_button = st.sidebar.button("Reset")
if reset_button:
    st.rerun()

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
    # Combined Graph (FIXED COLORS)
    # -----------------------------
    st.subheader("Growth Visualization")

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(active_list, color="blue", label="Active Customers")
    ax1.plot(new_list, color="orange", linestyle="--", label="New Customers")
    ax1.plot(churn_list, color="green", linestyle=":", label="Churned Customers")
    ax1.set_title("Startup Customer Growth with Churn")
    ax1.set_xlabel("Time Step")
    ax1.set_ylabel("Number of Customers")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # -----------------------------
    # Individual Graphs (MATCHED)
    # -----------------------------
    st.subheader("Individual Graphs")

    # Active
    fig_a, ax_a = plt.subplots(figsize=(10, 5))
    ax_a.plot(active_list, color="blue", label="Active Customers")
    ax_a.set_title("Active Customers")
    ax_a.set_xlabel("Time Step")
    ax_a.set_ylabel("Number of Customers")
    ax_a.legend()
    ax_a.grid(True)
    st.pyplot(fig_a)

    # New
    fig_n, ax_n = plt.subplots(figsize=(10, 5))
    ax_n.plot(new_list, color="orange", linestyle="--", label="New Customers")
    ax_n.set_title("New Customers")
    ax_n.set_xlabel("Time Step")
    ax_n.set_ylabel("Number of Customers")
    ax_n.legend()
    ax_n.grid(True)
    st.pyplot(fig_n)

    # Churn
    fig_c, ax_c = plt.subplots(figsize=(10, 5))
    ax_c.plot(churn_list, color="green", linestyle=":", label="Churned Customers")
    ax_c.set_title("Churned Customers")
    ax_c.set_xlabel("Time Step")
    ax_c.set_ylabel("Number of Customers")
    ax_c.legend()
    ax_c.grid(True)
    st.pyplot(fig_c)

    # Retention (unchanged)
    st.subheader("Retention Analysis")

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot([x * 100 for x in retention_list], label="Retention Rate (%)")
    ax2.set_title("Retention Trend Over Time")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Retention Percentage")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
