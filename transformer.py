import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


def select_file():
    """Ouvre une boîte de dialogue pour sélectionner un fichier .py et crée une copie de sauvegarde."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")],
        title="Sélectionner un fichier Python (.py)"
    )
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)
        try:
            backup_path = create_backup(file_path)
            messagebox.showinfo("Sauvegarde", f"Une copie de sauvegarde a été créée :\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de la sauvegarde : {e}")


def create_backup(file_path):
    """Crée une copie de sauvegarde du fichier sélectionné."""
    dir_name, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)
    backup_name = f"{base_name}_backup{ext}"
    backup_path = os.path.join(dir_name, backup_name)
    shutil.copy(file_path, backup_path)
    return backup_path


def convert_to_exe():
    """Convertit le fichier .py sélectionné en .exe et le déplace dans le dossier d'origine."""
    file_path = entry_file_path.get()

    if not file_path.endswith(".py"):
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier .py valide.")
        return

    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Le fichier sélectionné n'existe pas.")
        return

    try:
        # Vérifiez si PyInstaller est installé
        result = subprocess.run(["python", "-m", "pip", "show", "pyinstaller"], capture_output=True, text=True)
        if "Name: pyinstaller" not in result.stdout:
            messagebox.showerror("Erreur", "PyInstaller n'est pas installé. Installez-le avec 'pip install pyinstaller'.")
            return

        # Commande PyInstaller explicite
        subprocess.run(["python", "-m", "PyInstaller", "--onefile", "--noconsole", file_path], check=True)

        # Dossier d'origine du fichier .py
        origin_dir = os.path.dirname(file_path)
        # Nom du fichier sans extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # Fichier généré dans le dossier dist
        generated_exe = os.path.join("dist", f"{file_name}.exe")
        # Nouveau chemin pour le fichier .exe
        destination_exe = os.path.join(origin_dir, f"{file_name}.exe")

        if os.path.exists(generated_exe):
            # Déplacer le fichier .exe vers le dossier d'origine
            shutil.move(generated_exe, destination_exe)
            messagebox.showinfo("Succès", f"Conversion terminée ! L'exécutable a été déplacé dans :\n{destination_exe}")
        else:
            messagebox.showerror("Erreur", "Le fichier .exe généré est introuvable.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", f"Erreur lors de la conversion :\n{e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur inattendue est survenue :\n{e}")


# Interface graphique
root = tk.Tk()
root.title("Convertisseur .py en .exe")
root.geometry("500x200")
root.configure(bg="#ffffff")

label_style = {"bg": "#ffffff", "fg": "#0033cc", "font": ("Arial", 12, "bold")}
button_style = {"bg": "#0033cc", "fg": "#ffffff", "font": ("Arial", 10, "bold")}
entry_style = {"bg": "#f0f8ff", "fg": "#000000", "font": ("Arial", 10)}

label_instructions = tk.Label(root, text="Sélectionnez un fichier Python à convertir en .exe :", **label_style)
label_instructions.pack(pady=10)

frame_file_selection = tk.Frame(root, bg="#ffffff")
frame_file_selection.pack(pady=10)

entry_file_path = tk.Entry(frame_file_selection, width=40, **entry_style)
entry_file_path.pack(side=tk.LEFT, padx=5)

button_browse = tk.Button(frame_file_selection, text="Parcourir", command=select_file, **button_style)
button_browse.pack(side=tk.LEFT)

button_convert = tk.Button(root, text="Convertir en .exe", command=convert_to_exe, **button_style)
button_convert.pack(pady=20)

root.mainloop()
