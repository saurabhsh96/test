def calculate_emi(principal, annual_rate, tenure_months):
    """
    Calculate EMI, total amount paid, and total interest paid.
    """
    monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly decimal
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    total_payment = emi * tenure_months
    total_interest = total_payment - principal
    return emi, total_payment, total_interest

def reduced_tenure(principal, emi, annual_rate, extra_payment):
    """
    Calculate reduced tenure if an extra amount is paid each month.
    """
    monthly_rate = annual_rate / (12 * 100)
    months = 0
    while principal > 0:
        interest = principal * monthly_rate
        principal += interest - emi - extra_payment
        months += 1
        if principal < 0:
            break  # Exit when principal is fully paid
    return months

# Inputs
principal = 5273752  # Rs.
annual_rate = 10.65  # Annual Interest Rate in %
tenure_months = 91   # Loan tenure in months

# EMI Calculation
emi, total_payment, total_interest = calculate_emi(principal, annual_rate, tenure_months)

print(f"EMI: Rs. {emi:.2f}")
print(f"Total Amount Paid: Rs. {total_payment:.2f}")
print(f"Total Interest Paid: Rs. {total_interest:.2f}")

# Extra Payment Logic
extra_payment = float(input("Enter the extra amount you can pay each month: Rs. "))
new_tenure = reduced_tenure(principal, emi, annual_rate, extra_payment)

print(f"With an additional payment of Rs. {extra_payment:.2f} per month,")
print(f"the loan tenure will reduce to approximately {new_tenure} months.")
