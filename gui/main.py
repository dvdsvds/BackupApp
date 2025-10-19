import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Backup Tool")
app.geometry("780x500")
app.resizable(False, False)

font_label = ("Segoe UI", 15)
font_entry = ("Consolas", 14)
font_btn = ("Segoe UI", 14)

PADX_L = (40, 10)
PADX_M = (10, 15)
PADX_R = (10, 40)
PADY = (12, 12)

app.grid_columnconfigure(1, weight=1)

# Source
src_l = ctk.CTkLabel(app, text="Source Folder", font=font_label)
src_l.grid(row=0, column=0, padx=PADX_L, pady=(30, 10), sticky="e")

src_entry = ctk.CTkEntry(app, font=font_entry, placeholder_text="Select source directory...")
src_entry.grid(row=0, column=1, padx=PADX_M, pady=(30, 10), sticky="we")

src_btn = ctk.CTkButton(app, text="Browse", width=100, font=font_btn)
src_btn.grid(row=0, column=2, padx=PADX_R, pady=(30, 10))

# Destination
dst_l = ctk.CTkLabel(app, text="Backup Folder", font=font_label)
dst_l.grid(row=1, column=0, padx=PADX_L, pady=PADY, sticky="e")

dst_entry = ctk.CTkEntry(app, font=font_entry, placeholder_text="Select destination directory...")
dst_entry.grid(row=1, column=1, padx=PADX_M, pady=PADY, sticky="we")

dst_btn = ctk.CTkButton(app, text="Browse", width=100, font=font_btn)
dst_btn.grid(row=1, column=2, padx=PADX_R, pady=PADY)

# Backup Name + Format
name_l = ctk.CTkLabel(app, text="Backup Name", font=font_label)
name_l.grid(row=2, column=0, padx=PADX_L, pady=PADY, sticky="e")

name_frame = ctk.CTkFrame(app, fg_color="transparent")
name_frame.grid(row=2, column=1, sticky="we", padx=PADX_M, pady=PADY)
name_frame.grid_columnconfigure(0, weight=1)

name_entry = ctk.CTkEntry(name_frame, font=font_entry, placeholder_text="Enter backup name...")
name_entry.grid(row=0, column=0, sticky="we", padx=(0, 10))

format_opt = ctk.CTkOptionMenu(name_frame, values=["zip", "7z", "rar"], width=100, font=font_btn)
format_opt.grid(row=0, column=1, sticky="e")

# Backup Cycle
cycle_l = ctk.CTkLabel(app, text="Backup Cycle", font=font_label)
cycle_l.grid(row=3, column=0, padx=PADX_L, pady=PADY, sticky="e")

cycle_frame = ctk.CTkFrame(app, fg_color="transparent")
cycle_frame.grid(row=3, column=1, sticky="w", padx=PADX_M, pady=PADY)

def validate_numeric(P): 
    return P.isdigit() or P == ""
vcmd = (app.register(validate_numeric), "%P")

cycle_entry = ctk.CTkEntry(
    cycle_frame, width=80, font=font_entry,
    validate="key", validatecommand=vcmd,
    placeholder_text="0", justify="center"
)
cycle_entry.pack(side="left", padx=(0, 10))

cycle_opt = ctk.CTkOptionMenu(
    cycle_frame,
    values=["Hours", "Days", "Weeks", "Months", "Years"],
    width=100, font=font_btn
)
cycle_opt.pack(side="left")

# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.grid(row=5, column=0, columnspan=3, sticky="e", padx=(0, 40), pady=(20, 10))

start_btn = ctk.CTkButton(btn_frame, text="Start", width=100, fg_color="#2FA572", hover_color="#28C17A", font=font_btn)
start_btn.pack(side="right", padx=(10, 0))

reset_btn = ctk.CTkButton(btn_frame, text="Reset", width=100, fg_color="#444", hover_color="#555", font=font_btn)
reset_btn.pack(side="right", padx=(0, 10))

# Log Box
log_box = ctk.CTkTextbox(app, height=180, font=("Consolas", 13))
log_box.grid(row=6, column=0, columnspan=3, padx=(40, 40), pady=(5, 30), sticky="we")
log_box.insert("end", ">>> Backup log will appear here...\n")
log_box.configure(state="disabled")

app.mainloop()
