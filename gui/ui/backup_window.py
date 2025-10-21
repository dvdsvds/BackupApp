import customtkinter as ctk
import tkinter.filedialog as fd
import os, sys, threading, time

# ────────────────────────────────
# backend 모듈 불러오기
sys.path.append(os.path.join(os.path.dirname(__file__), "pyd"))
import backend

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

# ────────────────────────────────
# 로그 함수
def log(msg):
    log_box.configure(state="normal")
    log_box.insert("end", f"{msg}\n")
    log_box.see("end")
    log_box.configure(state="disabled")

# ────────────────────────────────
# 폴더 선택 함수
def browse_src():
    path = fd.askdirectory(title="Select Source Folder")
    if path:
        src_entry.delete(0, "end")
        src_entry.insert(0, path)

def browse_dst():
    path = fd.askdirectory(title="Select Backup Folder")
    if path:
        dst_entry.delete(0, "end")
        dst_entry.insert(0, path)

# ────────────────────────────────
# Source
src_l = ctk.CTkLabel(app, text="Source Folder", font=font_label)
src_l.grid(row=0, column=0, padx=PADX_L, pady=(30, 10), sticky="e")

src_entry = ctk.CTkEntry(app, font=font_entry, placeholder_text="Select source directory...")
src_entry.grid(row=0, column=1, padx=PADX_M, pady=(30, 10), sticky="we")

src_btn = ctk.CTkButton(app, text="Browse", width=100, font=font_btn, command=browse_src)
src_btn.grid(row=0, column=2, padx=PADX_R, pady=(30, 10))

# ────────────────────────────────
# Destination
dst_l = ctk.CTkLabel(app, text="Backup Folder", font=font_label)
dst_l.grid(row=1, column=0, padx=PADX_L, pady=PADY, sticky="e")

dst_entry = ctk.CTkEntry(app, font=font_entry, placeholder_text="Select destination directory...")
dst_entry.grid(row=1, column=1, padx=PADX_M, pady=PADY, sticky="we")

dst_btn = ctk.CTkButton(app, text="Browse", width=100, font=font_btn, command=browse_dst)
dst_btn.grid(row=1, column=2, padx=PADX_R, pady=PADY)

# ────────────────────────────────
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

# ────────────────────────────────
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
    values=["Hourly", "Daily", "Weekly", "Monthly", "Yearly"],
    width=100, font=font_btn
)
cycle_opt.pack(side="left")

# ────────────────────────────────
# Log Box
log_box = ctk.CTkTextbox(app, height=180, font=("Consolas", 13))
log_box.grid(row=6, column=0, columnspan=3, padx=(40, 40), pady=(5, 30), sticky="we")
log_box.insert("end", ">>> Backup log will appear here...\n")
log_box.configure(state="disabled")

# ────────────────────────────────
# 동작 함수
def start_backup():
    src = src_entry.get().strip()
    dst = dst_entry.get().strip()
    name = name_entry.get().strip()
    fmt = format_opt.get()
    cycle_val = cycle_entry.get().strip()
    cycle_type = cycle_opt.get()

    if not src or not dst:
        log("[Error] Source or destination missing.")
        return

    cfg = backend.Config()
    cfg.src = src
    cfg.dst = dst
    cfg.newName = name if name else os.path.basename(src)
    cfg.include_date = True
    cfg.cycle_value = int(cycle_val) if cycle_val else 1
    cfg.cycle = getattr(backend.Cycle, cycle_type)
    cfg.format = getattr(backend.Format, fmt.upper())
    cfg.mode = backend.Mode.Default

    log(f"[START] Backup cycle started → every {cfg.cycle_value} {cycle_type.lower()}")
    log(f"    → name: {cfg.newName}.{fmt}")
    log(f"    → src : {src}")
    log(f"    → dst : {dst}")

    # ✅ 주기 백업을 별도 스레드에서 실행
    def loop():
        ok = backend.backup(cfg)  # 첫 백업 1회
        if ok:
            log("[OK] First backup completed successfully.")
        else:
            log("[FAIL] First backup failed.")

        # 이후 주기적 백업 반복
        backend.backup_cycle(cfg)

    threading.Thread(target=loop, daemon=True).start()


def reset_fields():
    src_entry.delete(0, "end")
    dst_entry.delete(0, "end")
    name_entry.delete(0, "end")
    cycle_entry.delete(0, "end")
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.insert("end", ">>> Backup log will appear here...\n")
    log_box.configure(state="disabled")

# ────────────────────────────────
# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.grid(row=5, column=0, columnspan=3, sticky="e", padx=(0, 40), pady=(20, 10))

start_btn = ctk.CTkButton(btn_frame, text="Start", width=100,
                          fg_color="#2FA572", hover_color="#28C17A",
                          font=font_btn, command=start_backup)
start_btn.pack(side="right", padx=(10, 0))

reset_btn = ctk.CTkButton(btn_frame, text="Reset", width=100,
                          fg_color="#444", hover_color="#555",
                          font=font_btn, command=reset_fields)
reset_btn.pack(side="right", padx=(0, 10))

app.mainloop()
