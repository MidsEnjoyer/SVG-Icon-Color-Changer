import os
import re
import subprocess
import platform
import webbrowser
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, colorchooser, messagebox

# --- Theme Configuration ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.schedule_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<ButtonPress>", self.hide_tip) 

    def schedule_tip(self, event=None):
        self.id = self.widget.after(1500, self.show_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#2b2b2b", foreground="white", relief='flat', 
                         borderwidth=1, font=("Segoe UI", 9), padx=8, pady=4)
        label.pack()

    def hide_tip(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def closest_color(requested_colour):
    basic_colors = {
        '#ff0000': 'Red', '#00ff00': 'Green', '#0000ff': 'Blue',
        '#ffff00': 'Yellow', '#ff00ff': 'Magenta', '#00ffff': 'Cyan',
        '#000000': 'Black', '#ffffff': 'White', '#ffa500': 'Orange',
        '#800080': 'Purple', '#a52a2a': 'Brown', '#808080': 'Gray'
    }
    return basic_colors.get(requested_colour.lower(), "Custom_Color")

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def select_input():
    path = filedialog.askdirectory(title="Select Source Folder")
    if path: input_var.set(path)

def select_output():
    path = filedialog.askdirectory(title="Select Destination Folder")
    if path: output_var.set(path)

def pick_color():
    color_choice = colorchooser.askcolor(
        title="Choose Icon Color",
        initialcolor=color_var.get()
    )
    if color_choice[1]:
        color_var.set(color_choice[1])
        folder_name_var.set(f"{closest_color(color_choice[1])}_Icons")
        color_preview.configure(fg_color=color_choice[1])

def clear_all():
    input_var.set("")
    output_var.set("")
    color_var.set("#000000")
    folder_name_var.set("Black_Icons")
    color_preview.configure(fg_color="#000000")
    log_window.delete('1.0', tk.END)
    log_window.insert(tk.END, "...")
    progress_bar.set(0)
    progress_text.configure(text="Progress")

def change_appearance_mode(new_mode):
    ctk.set_appearance_mode(new_mode)
    if new_mode == "Dark":
        log_window.configure(bg="#1d1d1d", fg="#ffffff")
    elif new_mode == "Light":
        log_window.configure(bg="#f0f0f0", fg="#000000")
    else: 
        is_dark = ctk.get_appearance_mode() == "Dark"
        log_window.configure(bg="#1d1d1d" if is_dark else "#f0f0f0",
                             fg="#ffffff" if is_dark else "#000000")

def open_folder(path):
    if platform.system() == "Windows": os.startfile(path)
    elif platform.system() == "Darwin": subprocess.Popen(["open", path])
    else: subprocess.Popen(["xdg-open", path])

def send_email(event):
    webbrowser.open("mailto:MidsEnjoyer@pm.me")

def copy_to_clipboard(address, button):
    root.clipboard_clear()
    root.clipboard_append(address)
    button.configure(text="Copied! ✅", text_color="#2ecc71")
    root.after(2000, lambda: button.configure(text="Copy Address", text_color=["#000000", "#FFFFFF"]))

def show_finished_popup(count, folder_name, full_path):
    top = ctk.CTkToplevel(root)
    top.title("Done!")
    
    # LOCK THE ORIGINAL WINDOW (Modal behavior)
    top.grab_set() 
    
    try:
        top.after(200, lambda: top.iconbitmap('app_icon.ico'))
    except:
        pass
    popup_width = 540
    popup_height = 280
    center_window(top, popup_width, popup_height)
    top.resizable(False, False)
    top.attributes("-topmost", True)
    ctk.CTkLabel(top, text="Process Complete!", font=("Segoe UI", 18, "bold")).pack(pady=(20, 5))
    ctk.CTkLabel(top, text=f"Recolored {count} icons into folder:\n{folder_name}", font=("Segoe UI", 12)).pack(pady=5)
    btn_frame = ctk.CTkFrame(top, fg_color="transparent")
    btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame, text="New Color", width=100, command=lambda: [top.destroy(), pick_color()]).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Open Folder", width=100, command=lambda: open_folder(full_path)).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Close App", width=100, fg_color="#e74c3c", hover_color="#c0392b", command=root.quit).pack(side="left", padx=5)
    
    email_frame = ctk.CTkFrame(top, fg_color="transparent")
    email_frame.pack()
    ctk.CTkLabel(email_frame, text="Questions? Email me: ", font=("Segoe UI", 11)).pack(side="left")
    email_addr = ctk.CTkLabel(email_frame, text="MidsEnjoyer@pm.me", font=("Segoe UI", 11, "underline"), text_color="#3498db", cursor="hand2")
    email_addr.pack(side="left")
    email_addr.bind("<Button-1>", send_email)
    
    btc_address = "bc1qyv037mh3hr46xsf3r0tc7se44sgt6ree0y2m0l"
    btc_line_frame = ctk.CTkFrame(top, fg_color="transparent")
    btc_line_frame.pack(pady=(15, 5))
    standard_font = ("Segoe UI", 11, "normal")
    ctk.CTkLabel(btc_line_frame, text="Support me with BTC: ", font=standard_font).pack(side="left")
    ctk.CTkLabel(btc_line_frame, text=btc_address, font=standard_font).pack(side="left")
    copy_btn = ctk.CTkButton(top, text="Copy Address", width=140, height=28, command=lambda: copy_to_clipboard(btc_address, copy_btn))
    copy_btn.pack(pady=5)

def batch_recolor():
    if not input_var.get() or not output_var.get():
        messagebox.showerror("Error", "Please select folders first!")
        return
    output_folder = os.path.join(output_var.get(), folder_name_var.get().strip())
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    try:
        all_files = [f for f in os.listdir(input_var.get()) if f.lower().endswith(".svg")]
    except:
        messagebox.showerror("Error", "Could not access source folder.")
        return
    if not all_files:
        messagebox.showwarning("No files", "No SVG files found.")
        return
    log_window.delete('1.0', tk.END)
    target_color = color_var.get()
    success_count = 0
    stroke_regex = r'stroke="(?!none|transparent)[^"]+"'
    fill_regex = r'fill="(?!none|transparent)[^"]+"'
    for i, filename in enumerate(all_files):
        try:
            progress = (i + 1) / len(all_files)
            progress_bar.set(progress)
            progress_text.configure(text=f"Processing... {i+1}/{len(all_files)}")
            with open(os.path.join(input_var.get(), filename), 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = re.sub(stroke_regex, f'stroke="{target_color}"', content)
            new_content = re.sub(fill_regex, f'fill="{target_color}"', new_content)
            with open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as f:
                f.write(new_content)
            success_count += 1
            log_window.insert(tk.END, f"Recolored: {filename}\n")
            log_window.see(tk.END)
            root.update()
        except:
            log_window.insert(tk.END, f"FAILED: {filename}\n")
    progress_text.configure(text="Done!")
    log_window.insert(tk.END, "\n--- Done! ---")
    log_window.see(tk.END) 
    show_finished_popup(success_count, folder_name_var.get(), output_folder)

# --- Main UI ---
root = ctk.CTk()
root.title("SVG Icon Color Changer")
app_width = 420
app_height = 720
center_window(root, app_width, app_height)
root.minsize(400, 600)

try:
    root.iconbitmap('app_icon.ico')
except:
    pass

input_var = tk.StringVar()
output_var = tk.StringVar()
color_var = tk.StringVar(value="#000000")
folder_name_var = tk.StringVar(value="Black_Icons")

header = ctk.CTkFrame(root, fg_color="transparent")
header.pack(fill="x", padx=20, pady=(15, 5))
ctk.CTkLabel(header, text="SVG Color Changer", font=("Segoe UI", 20, "bold")).pack(side="left")
mode_switch = ctk.CTkOptionMenu(header, values=["System", "Dark", "Light"], width=90, height=24, command=change_appearance_mode)
mode_switch.pack(side="right")
mode_switch.set("System")

main_container = ctk.CTkFrame(root, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=25)

frame_f = ctk.CTkFrame(main_container)
frame_f.pack(fill="x", pady=10)
ctk.CTkLabel(frame_f, text="1. File Paths", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=5)
f_sub = ctk.CTkFrame(frame_f, fg_color="transparent")
f_sub.pack(fill="x", padx=10, pady=5)
src_btn = ctk.CTkButton(f_sub, text="Source", width=100, command=select_input)
src_btn.pack(side="left", padx=(0,10))
ctk.CTkEntry(f_sub, textvariable=input_var, placeholder_text="Path to icons...").pack(side="left", fill="x", expand=True)
f_sub2 = ctk.CTkFrame(frame_f, fg_color="transparent")
f_sub2.pack(fill="x", padx=10, pady=(0,15))
dst_btn = ctk.CTkButton(f_sub2, text="Destination", width=100, command=select_output)
dst_btn.pack(side="left", padx=(0,10))
ctk.CTkEntry(f_sub2, textvariable=output_var, placeholder_text="Where to save...").pack(side="left", fill="x", expand=True)

frame_s = ctk.CTkFrame(main_container)
frame_s.pack(fill="x", pady=5)
ctk.CTkLabel(frame_s, text="2. Style & Name", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=5)
s_sub = ctk.CTkFrame(frame_s, fg_color="transparent")
s_sub.pack(fill="x", padx=10, pady=5)
clr_btn = ctk.CTkButton(s_sub, text="Pick Color", width=100, command=pick_color)
clr_btn.pack(side="left")
color_preview = ctk.CTkButton(s_sub, text="", width=34, height=34, fg_color="#000000", state="disabled", corner_radius=17)
color_preview.pack(side="left", padx=10)
clear_btn = ctk.CTkButton(s_sub, text="Clear", width=65, fg_color=("gray75", "gray30"), text_color=("black", "white"), command=clear_all)
clear_btn.pack(side="right")
ctk.CTkLabel(frame_s, text="New Folder Name:").pack(anchor="w", padx=15, pady=(5,0))
ctk.CTkEntry(frame_s, textvariable=folder_name_var).pack(fill="x", padx=10, pady=(0,15))

start_btn = ctk.CTkButton(main_container, text="Start Batch Recolor", height=48, font=("Segoe UI", 14, "bold"), fg_color="#e74c3c", hover_color="#c0392b", command=batch_recolor)
start_btn.pack(fill="x", pady=20)

progress_text = ctk.CTkLabel(main_container, text="Progress", font=("Segoe UI", 11))
progress_text.pack()
progress_bar = ctk.CTkProgressBar(main_container, height=12)
progress_bar.set(0)
progress_bar.pack(fill="x", pady=(0, 20))

is_dark = ctk.get_appearance_mode() == "Dark"
log_window = tk.Text(main_container, height=8, font=("Consolas", 10), bg="#1d1d1d" if is_dark else "#f0f0f0", fg="#ffffff" if is_dark else "#000000", borderwidth=0, padx=10, pady=10)
log_window.pack(fill="both", expand=True, pady=(0, 20))
log_window.insert("1.0", "...")

ToolTip(src_btn, "Select folder with SVG icons")
ToolTip(dst_btn, "Select where to save recolored icons")
ToolTip(clr_btn, "Choose a color. Folder name will auto-update!")
ToolTip(clear_btn, "Reset all settings to default")
ToolTip(start_btn, "Run the recoloring process now")

root.mainloop()