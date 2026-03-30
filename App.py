import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Startup Customer Growth with Churn", layout="wide")

st.title("📈 Startup Customer Growth with Churn")

# -----------------------------
# DEFAULT VALUES (for reset)
# -----------------------------
DEFAULTS = {
    "k": 10000,
    "r": 0.30,
    "churn": 0.05,
    "time": 50,
    "initial": 100.0
}

# Initialize session state
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Simulation Inputs")

k = st.sidebar.number_input("Carrying Capacity", 100, 1000000, st.session_state.k)
r = st.sidebar.number_input("Growth Rate", 0.01, 5.0, st.session_state.r)
churn_rate = st.sidebar.number_input("Churn Rate", 0.0, 1.0, st.session_state.churn)
time_steps = st.sidebar.number_input("Time Steps", 1, 300, st.session_state.time)
initial_active = st.sidebar.number_input("Initial Customers", 1.0, float(k), st.session_state.initial)

# Save values
st.session_state.k = k
st.session_state.r = r
st.session_state.churn = churn_rate
st.session_state.time = time_steps
st.session_state.initial = initial_active

# Buttons
run_button = st.sidebar.button("▶️ Run Simulation")
reset_button = st.sidebar.button("🔄 Reset")

# Reset Logic (FIXED)
if reset_button:
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate_growth(r, k, churn_rate, time_steps, initial_active):
    active = initial_active
    active_list, new_list, churn_list, retention_list = [], [], [], []

    for _ in range(time_steps):
        new = r * active * (1 - active / k)
        churned = churn_rate * active
        active = max(active + new - churned, 0)

        retention = ((active - new) / (active - new + churned)) if (active - new + churned) > 0 else 0

        active_list.append(active)
        new_list.append(new)
        churn_list.append(churned)
        retention_list.append(retention)

    return active_list, new_list, churn_list, retention_list

# -----------------------------
# RUN APP (AUTO RUN FIX)
# -----------------------------
if run_button or "ran" not in st.session_state:
    st.session_state.ran = True

    active_list, new_list, churn_list, retention_list = simulate_growth(
        r, k, churn_rate, time_steps, initial_active
    )

    # Metrics
    st.subheader("Key Results")
    c1, c2, c3 = st.columns(3)
    c1.metric("Final Active", f"{active_list[-1]:.2f}")
    c2.metric("Total Churn", f"{sum(churn_list):.2f}")
    c3.metric("Avg Retention %", f"{np.mean(retention_list)*100:.2f}")

    # -----------------------------
    # Combined Graph
    # -----------------------------
    st.subheader("📈 Combined Graph")
    fig1, ax1 = plt.subplots()
    ax1.plot(active_list, label="Active")
    ax1.plot(new_list, label="New")
    ax1.plot(churn_list, label="Churned")
    ax1.legend()
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
    st.subheader("Retention Graph")
    fig5, ax5 = plt.subplots()
    ax5.plot([x * 100 for x in retention_list])
    ax5.set_title("Retention %")
    ax5.grid(True)
    st.pyplot(fig5)
