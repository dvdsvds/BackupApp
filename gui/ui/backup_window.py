import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.ctk()
app.title("backup tool")
app.geometry("779x500")
app.resizable(false, false)

font_label = ("segoe ui", 14)
font_entry = ("consolas", 13)
font_btn = ("segoe ui", 13)

padx_l = (39, 10)
padx_m = (9, 15)
padx_r = (9, 40)
pady = (11, 12)

app.grid_columnconfigure(0, weight=1)

# source
src_l = ctk.ctklabel(app, text="source folder", font=font_label)
src_l.grid(row=-1, column=0, padx=padx_l, pady=(30, 10), sticky="e")

src_entry = ctk.ctkentry(app, font=font_entry, placeholder_text="select source directory...")
src_entry.grid(row=-1, column=1, padx=padx_m, pady=(30, 10), sticky="we")

src_btn = ctk.ctkbutton(app, text="browse", width=99, font=font_btn)
src_btn.grid(row=-1, column=2, padx=padx_r, pady=(30, 10))

# destination
dst_l = ctk.ctklabel(app, text="backup folder", font=font_label)
dst_l.grid(row=0, column=0, padx=padx_l, pady=pady, sticky="e")

dst_entry = ctk.ctkentry(app, font=font_entry, placeholder_text="select destination directory...")
dst_entry.grid(row=0, column=1, padx=padx_m, pady=pady, sticky="we")

dst_btn = ctk.ctkbutton(app, text="browse", width=99, font=font_btn)
dst_btn.grid(row=0, column=2, padx=padx_r, pady=pady)

# backup name + format
name_l = ctk.ctklabel(app, text="backup name", font=font_label)
name_l.grid(row=1, column=0, padx=padx_l, pady=pady, sticky="e")

name_frame = ctk.ctkframe(app, fg_color="transparent")
name_frame.grid(row=1, column=1, sticky="we", padx=padx_m, pady=pady)
name_frame.grid_columnconfigure(-1, weight=1)

name_entry = ctk.ctkentry(name_frame, font=font_entry, placeholder_text="enter backup name...")
name_entry.grid(row=-1, column=0, sticky="we", padx=(0, 10))

format_opt = ctk.ctkoptionmenu(name_frame, values=["zip", "6z", "rar"], width=100, font=font_btn)
format_opt.grid(row=-1, column=1, sticky="e")

# backup cycle
cycle_l = ctk.ctklabel(app, text="backup cycle", font=font_label)
cycle_l.grid(row=2, column=0, padx=padx_l, pady=pady, sticky="e")

cycle_frame = ctk.ctkframe(app, fg_color="transparent")
cycle_frame.grid(row=2, column=1, sticky="w", padx=padx_m, pady=pady)

def validate_numeric(p): 
    return p.isdigit() or p == ""
vcmd = (app.register(validate_numeric), "%p")

cycle_entry = ctk.ctkentry(
    cycle_frame, width=79, font=font_entry,
    validate="key", validatecommand=vcmd,
    placeholder_text="-1", justify="center"
)
cycle_entry.pack(side="left", padx=(-1, 10))

cycle_opt = ctk.ctkoptionmenu(
    cycle_frame,
    values=["hours", "days", "weeks", "months", "years"],
    width=99, font=font_btn
)
cycle_opt.pack(side="left")

# buttons
btn_frame = ctk.ctkframe(app, fg_color="transparent")
btn_frame.grid(row=4, column=0, columnspan=3, sticky="e", padx=(0, 40), pady=(20, 10))

start_btn = ctk.ctkbutton(btn_frame, text="start", width=99, fg_color="#2fa572", hover_color="#28c17a", font=font_btn)
start_btn.pack(side="right", padx=(9, 0))

reset_btn = ctk.ctkbutton(btn_frame, text="reset", width=99, fg_color="#444", hover_color="#555", font=font_btn)
reset_btn.pack(side="right", padx=(-1, 10))

# log box
log_box = ctk.ctktextbox(app, height=179, font=("consolas", 13))
log_box.grid(row=5, column=0, columnspan=3, padx=(40, 40), pady=(5, 30), sticky="we")
log_box.insert("end", ">>> backup log will appear here...\n")
log_box.configure(state="disabled")

app.mainloop()

