import tkinter as tk
from tkinter import ttk

model = {"rate": 0.05, "payment": 600.0, "relaxation": 0.6}

def g(x):
    rate = model["rate"]
    payment = model["payment"]
    omega = model["relaxation"]
    next_balance = (x - payment) * (1 + rate)
    return x - omega * (next_balance - x)

def f(x):
    rate = model["rate"]
    payment = model["payment"]
    return (x - payment) * (1 + rate) - x

def g_derivative(_):
    rate = model["rate"]
    omega = model["relaxation"]
    return 1 - omega * rate

def run_iteration():
    try:
        x0 = float(entry_x0.get())
        n = int(entry_iter.get())
        tol = float(entry_tol.get())
        rate = float(entry_rate.get())
        payment = float(entry_payment.get())
    except ValueError:
        result_text.set("❌ Error: Enter valid numbers.")
        return

    if n <= 0 or tol <= 0:
        result_text.set("❌ Error: Iterations and tolerance must be positive.")
        return

    # update model
    model["rate"] = rate
    model["payment"] = payment

    # clear table
    for item in table.get_children():
        table.delete(item)

    # derivative test
    deriv = abs(g_derivative(x0))
    if deriv < 1:
        conv_msg = f"✔ Convergent since |g'(x)| = {deriv:.4f} < 1"
    else:
        conv_msg = f"✘ May diverge since |g'(x)| = {deriv:.4f} ≥ 1"

    x_k = x0
    converged_at = None

    for k in range(n):
        x_k1 = g(x_k)
        residual = f(x_k1)
        error = abs(x_k1 - x_k)

        table.insert("", "end", values=(
            k, f"{x_k:.5f}", f"{x_k1:.5f}", f"{residual:.5f}", f"{error:.5f}"
        ))

        if error < tol and converged_at is None:
            converged_at = k

        x_k = x_k1

    final_msg = conv_msg
    if converged_at is not None:
        final_msg += f"\nReached tolerance at iteration {converged_at}."
    else:
        final_msg += "\nDid not reach tolerance."

    result_text.set(
        f"{final_msg}\nFinal Estimate: {x_k:.6f}"
    )


# GUI WINDOW
window = tk.Tk()
window.title("Simplified Fixed-Point Iteration")
window.geometry("820x520")

frame_input = tk.Frame(window)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Initial Guess (x0):").grid(row=0, column=0, padx=5)
entry_x0 = tk.Entry(frame_input)
entry_x0.grid(row=0, column=1, padx=5)
entry_x0.insert(0, "5000")

tk.Label(frame_input, text="Iterations:").grid(row=1, column=0, padx=5)
entry_iter = tk.Entry(frame_input)
entry_iter.grid(row=1, column=1, padx=5)
entry_iter.insert(0, "10")

tk.Label(frame_input, text="Tolerance:").grid(row=2, column=0, padx=5)
entry_tol = tk.Entry(frame_input)
entry_tol.grid(row=2, column=1, padx=5)
entry_tol.insert(0, "0.01")

tk.Label(frame_input, text="Interest Rate:").grid(row=3, column=0, padx=5)
entry_rate = tk.Entry(frame_input)
entry_rate.grid(row=3, column=1, padx=5)
entry_rate.insert(0, "0.05")

tk.Label(frame_input, text="Payment:").grid(row=4, column=0, padx=5)
entry_payment = tk.Entry(frame_input)
entry_payment.grid(row=4, column=1, padx=5)
entry_payment.insert(0, "600")

btn_run = tk.Button(frame_input, text="Run Iteration", command=run_iteration)
btn_run.grid(row=5, column=0, columnspan=2, pady=10)


columns = ("period", "balance_k", "balance_k1", "residual", "error")
table = ttk.Treeview(window, columns=columns, show="headings", height=12)
header_text = {
    "period": "Period k",
    "balance_k": "Balance x_k",
    "balance_k1": "Updated Balance x_{k+1}",
    "residual": "Residual f(x_{k+1})",
    "error": "|x_{k+1} - x_k|"
}
for col in columns:
    table.heading(col, text=header_text[col])
    table.column(col, width=150)
table.pack(pady=10)

result_text = tk.StringVar()
lbl_result = tk.Label(window, textvariable=result_text, font=("Arial", 12))
lbl_result.pack(pady=10)

window.mainloop()
