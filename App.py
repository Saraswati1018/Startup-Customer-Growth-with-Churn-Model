st.subheader("Individual Graphs")

# SAME colors & styles as combined graph
active_color = "blue"
new_color = "orange"
churn_color = "green"

# Active Customers
fig_a, ax_a = plt.subplots(figsize=(10, 5))
ax_a.plot(active_list, color=active_color, label="Active Customers")
ax_a.set_title("Active Customers")
ax_a.set_xlabel("Time Step")
ax_a.set_ylabel("Number of Customers")
ax_a.legend()
ax_a.grid(True)
st.pyplot(fig_a)

# New Customers
fig_n, ax_n = plt.subplots(figsize=(10, 5))
ax_n.plot(new_list, color=new_color, linestyle="--", label="New Customers")
ax_n.set_title("New Customers")
ax_n.set_xlabel("Time Step")
ax_n.set_ylabel("Number of Customers")
ax_n.legend()
ax_n.grid(True)
st.pyplot(fig_n)

# Churned Customers
fig_c, ax_c = plt.subplots(figsize=(10, 5))
ax_c.plot(churn_list, color=churn_color, linestyle=":", label="Churned Customers")
ax_c.set_title("Churned Customers")
ax_c.set_xlabel("Time Step")
ax_c.set_ylabel("Number of Customers")
ax_c.legend()
ax_c.grid(True)
st.pyplot(fig_c)
