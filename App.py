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
    "Observed Final Active Customers (optional)", 0.0, 0.0, 0.0, 10.0
)

# Buttons
run_button = st.sidebar.button("▶️ Run Simulation")
reset_button = st.sidebar.button("🔄 Reset Parameters")

if reset_button:
    st.experimental_rerun()

# -----------------------------
# Simulation Function
# -----------------------------
def simulate_growth(r, k, churn_rate, time_steps, initial_active):
    active = initial_active
    active_list, new_list, churn_list, retention_list = [], [], [], []

    for _ in range(time_steps):
        new_customers = r * active * (1 - active / k)
        churned = churn_rate * active
        active = max(active + new_customers - churned, 0)

        retention_rate = ((active - new_customers) / (active - new_customers + churned)) if (active - new_customers + churned) > 0 else 0

        active_list.append(active)
        new_list.append(new_customers)
        churn_list.append(churned)
        retention_list.append(retention_rate)

    peak_active = max(active_list)
    peak_time = active_list.index(peak_active) + 1

    return active_list, new_list, churn_list, retention_list, peak_active, peak_time

# -----------------------------
# Estimation Function
# -----------------------------
def estimate_growth_rate(observed_final, k, churn_rate, time_steps, initial_active):
    best_r, best_error = None, float("inf")
    for candidate_r in np.linspace(0.01, 2.0, 1000):
        active_list, _, _, _, _, _ = simulate_growth(candidate_r, k, churn_rate, time_steps, initial_active)
        error = abs(active_list[-1] - observed_final)
        if error < best_error:
            best_error, best_r = error, candidate_r
    return best_r, best_error

# -----------------------------
# Run Simulation
# -----------------------------
if run_button:

    if observed_final_active > 0:
        r, error = estimate_growth_rate(observed_final_active, k, churn_rate, time_steps, initial_active)
        st.success(f"Estimated Growth Rate (r): {r:.4f}")
        st.info(f"Estimation Error: {error:.4f}")

    active_list, new_list, churn_list, retention_list, peak_active, peak_time = simulate_growth(
        r, k, churn_rate, time_steps, initial_active
    )

    final_active = active_list[-1]
    avg_retention = np.mean(retention_list) * 100

    # Metrics
    st.subheader("Key Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Peak Active", f"{peak_active:.2f}")
    c2.metric("Peak Time", peak_time)
    c3.metric("Final Active", f"{final_active:.2f}")
    c4.metric("Avg Retention (%)", f"{avg_retention:.2f}")

    # -----------------------------
    # Combined Graph
    # -----------------------------
    st.subheader("📈 Combined Growth Graph")

    fig1, ax1 = plt.subplots()
    ax1.plot(active_list, label="Active Customers", linewidth=2)
    ax1.plot(new_list, label="New Customers", linestyle="--")
    ax1.plot(churn_list, label="Churned Customers", linestyle=":")
    ax1.legend()
    ax1.set_xlabel("Time Step")
    ax1.set_ylabel("Customers")
    ax1.grid(True)
    st.pyplot(fig1)

    # -----------------------------
    # Individual Graphs
    # -----------------------------
    st.subheader("📊 Individual Graphs")

    col1, col2 = st.columns(2)

    with col1:
        fig2, ax2 = plt.subplots()
        ax2.plot(active_list)
        ax2.set_title("Active Customers")
        ax2.grid(True)
        st.pyplot(fig2)

    with col2:
        fig3, ax3 = plt.subplots()
        ax3.plot(new_list)
        ax3.set_title("New Customers")
        ax3.grid(True)
        st.pyplot(fig3)

    fig4, ax4 = plt.subplots()
    ax4.plot(churn_list)
    ax4.set_title("Churned Customers")
    ax4.grid(True)
    st.pyplot(fig4)

    # Retention Graph
    st.subheader("Retention Analysis")
    fig5, ax5 = plt.subplots()
    ax5.plot([x * 100 for x in retention_list])
    ax5.set_title("Retention Rate (%)")
    ax5.grid(True)
    st.pyplot(fig5)
