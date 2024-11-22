# Given values
principal = 5273752  # Loan amount in Rupees
annual_rate = 10.65  # Annual interest rate in percentage
months = 91  # Loan tenure in months

# Convert annual rate to monthly rate (percentage to decimal)
monthly_rate = (annual_rate / 100) / 12

# Calculate EMI using the EMI formula
EMI = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

# Calculate the total amount paid
total_paid = EMI * months

# Calculate the total interest paid using the formula for EMI-based interest
total_interest_emi = total_paid - principal

# ---- Compound Interest Calculation ----
# Convert loan tenure in months to years for compound interest formula
loan_years = months / 12

# Compound interest formula for total amount A
A = principal * (1 + (annual_rate / 100))**loan_years

# Calculate compound interest
compound_interest = A - principal

# Output the results
print(f"EMI: ₹{EMI:.2f}")
print(f"Total Amount Paid (with EMI): ₹{total_paid:.2f}")
print(f"Total Interest Paid (with EMI): ₹{total_interest_emi:.2f}")
print(f"Total Compound Interest: ₹{compound_interest:.2f}")
