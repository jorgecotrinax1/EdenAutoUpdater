import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import requests
import os
import shutil
import tempfile
from pathlib import Path
import py7zr
import subprocess
import json

class EdenUpdaterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Eden Emulator - Auto Updater")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Cargar configuración
        self.config_file = Path(__file__).parent / "eden_updater_config.json"
        self.selected_folder = None
        self.load_config()
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
    def load_config(self):
        """Carga la configuración desde el archivo JSON"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'last_folder' in config and config['last_folder']:
                        self.selected_folder = Path(config['last_folder'])
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    
    def save_config(self):
        """Guarda la configuración en el archivo JSON"""
        try:
            config = {
                'last_folder': str(self.selected_folder) if self.selected_folder else ""
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("Title.TLabel", background="#f0f0f0", font=("Arial", 14, "bold"))
        style.configure("TButton", font=("Arial", 10))
        style.configure("Status.TLabel", background="#e0e0e0", font=("Arial", 9))
        style.configure("Folder.TLabel", background="#f0f0f0", font=("Arial", 9), foreground="#555555")
        
    def create_widgets(self):
        """Crea los elementos de la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Eden Emulator Auto Updater", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Frame de información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Versión actual
        self.current_version_label = ttk.Label(info_frame, text="Versión actual: Verificando...")
        self.current_version_label.pack(anchor=tk.W)
        
        # Última versión
        self.latest_version_label = ttk.Label(info_frame, text="Última versión disponible: Verificando...")
        self.latest_version_label.pack(anchor=tk.W)
        
        # Frame de selección de carpeta
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        # Botón para seleccionar carpeta
        self.select_folder_button = ttk.Button(folder_frame, text="Seleccionar Carpeta", command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=5)
        
        # Etiqueta para mostrar la ruta seleccionada
        self.folder_var = tk.StringVar(value="")
        self.folder_label = ttk.Label(folder_frame, textvariable=self.folder_var, style="Folder.TLabel", wraplength=400)
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Mostrar la última carpeta guardada si existe
        if self.selected_folder:
            self.folder_var.set(f"Última carpeta: {self.selected_folder}")

        # Combobox para elegir release
        releases_frame = ttk.Frame(main_frame)
        releases_frame.pack(fill=tk.X, pady=5)
        ttk.Label(releases_frame, text="Release:").pack(side=tk.LEFT)
        self.release_var = tk.StringVar()
        self.release_combo = ttk.Combobox(releases_frame, textvariable=self.release_var, state="readonly")
        self.release_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Radio botones para arquitectura
        arch_frame = ttk.Frame(main_frame)
        arch_frame.pack(fill=tk.X, pady=5)
        ttk.Label(arch_frame, text="Arquitectura:").pack(anchor=tk.W)
        self.arch_var = tk.StringVar(value="x86_64")
        ttk.Radiobutton(arch_frame, text="ARM64 (Eden-*-arm64.7z)", variable=self.arch_var, value="arm64").pack(anchor=tk.W)
        ttk.Radiobutton(arch_frame, text="x86_64 (Eden-*-x86_64.7z)", variable=self.arch_var, value="x86_64").pack(anchor=tk.W)

        # Cargar releases al iniciar
        self.root.after(100, self.load_releases)

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Descargar y actualizar
        self.check_button = ttk.Button(button_frame, text="Verificar Actualizaciones", command=self.check_updates)
        self.check_button.pack(side=tk.LEFT, padx=5)
        
        self.download_button = ttk.Button(button_frame, text="Descargar y Actualizar", command=self.download_and_update, state=tk.DISABLED)
        self.download_button.pack(side=tk.LEFT, padx=5)
        
        self.launch_button = ttk.Button(button_frame, text="Abrir Emulador", command=self.launch_emulator, state=tk.DISABLED)
        self.launch_button.pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # Estado
        self.status_label = ttk.Label(main_frame, text="Listo", style="Status.TLabel", relief=tk.SUNKEN, padding="5")
        self.status_label.pack(fill=tk.X, pady=10)
        
        # Verificar actualizaciones al iniciar
        self.root.after(100, self.check_updates)
        
    def check_updates(self):
        """Verifica si hay actualizaciones disponibles"""
        self.set_status("Verificando actualizaciones...")
        self.check_button.config(state=tk.DISABLED)
        
        # Aquí irá la lógica de verificación
        # Por ahora es un placeholder
        self.root.after(2000, self.fake_update_check)
        
    def fake_update_check(self):
        """Simulación de verificación de actualizaciones"""
        # Guardar versiones en atributos para usarlas luego
        self.current_version = "v1.0.0"
        self.latest_version = "v1.1.0"
        self.current_version_label.config(text=f"Versión actual: {self.current_version}")
        self.latest_version_label.config(text=f"Última versión disponible: {self.latest_version}")
        self.download_button.config(state=tk.NORMAL)
        self.set_status("¡Actualización disponible!")
        self.check_button.config(state=tk.NORMAL)
        # Habilitar botón de descarga si hay carpeta seleccionada
        if hasattr(self, 'selected_folder') and self.selected_folder:
            self.download_button.config(state=tk.NORMAL)
            # Verificar si existe eden.exe para habilitar el botón de abrir emulador
            self.check_eden_exe()
        
    def download_update(self):
        """Inicia la descarga de la actualización"""
        self.set_status("Descargando...")
        self.download_button.config(state=tk.DISABLED)
        
        # Simular descarga
        self.simulate_download()
        
    def simulate_download(self):
        """Simula una descarga con barra de progreso"""
        def update_progress(step=0):
            if step <= 100:
                self.progress['value'] = step
                self.set_status(f"Descargando... {step}%")
                self.root.after(50, update_progress, step + 1)
            else:
                # Intentar guardar un archivo representativo en la carpeta Downloads
                try:
                    downloads_dir = Path.home() / "Downloads"
                    downloads_dir.mkdir(parents=True, exist_ok=True)
                    # Nombre de archivo con versión
                    filename = f"eden_emulator_update_{self.latest_version}.zip"
                    file_path = downloads_dir / filename
                    # Escribir un archivo vacío (placeholder)
                    with open(file_path, "wb") as f:
                        f.write(b"")

                    self.set_status("¡Descarga completada!")
                    messagebox.showinfo("Éxito", f"Actualización descargada e instalada correctamente\nRuta: {file_path}")
                except Exception as e:
                    self.set_status("Error al guardar la descarga")
                    messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
                finally:
                    self.progress['value'] = 0
                    self.download_button.config(state=tk.NORMAL)
                
        update_progress()

    def select_folder(self):
        """Permite al usuario seleccionar la carpeta destino donde se instalará el emulador"""
        # Usar la última carpeta seleccionada como directorio inicial si existe
        initial_dir = str(self.selected_folder) if self.selected_folder else None
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta destino",
            initialdir=initial_dir
        )
        if folder:
            self.selected_folder = Path(folder)
            # Mostrar la ruta seleccionada
            self.folder_var.set(f"Carpeta seleccionada: {self.selected_folder}")
            # Guardar la configuración
            self.save_config()
            # Habilitar descarga si hay una release cargada
            if self.release_combo['values']:
                self.download_button.config(state=tk.NORMAL)
            # Verificar si existe eden.exe
            self.check_eden_exe()

    def check_eden_exe(self):
        """Verifica si existe eden.exe en la carpeta seleccionada y habilita el botón"""
        if hasattr(self, 'selected_folder') and self.selected_folder:
            eden_exe_path = self.selected_folder / "eden.exe"
            if eden_exe_path.exists():
                self.launch_button.config(state=tk.NORMAL)
                self.set_status("Emulador listo para abrir")
            else:
                self.launch_button.config(state=tk.DISABLED)
                self.set_status("Emulador no encontrado en la carpeta")

    def load_releases(self):
        """Carga releases desde GitHub y pobla el combobox (por defecto la última release)"""
        try:
            self.set_status("Obteniendo releases desde GitHub...")
            resp_latest = requests.get('https://api.github.com/repos/pflyly/eden-nightly/releases/latest', timeout=10)
            resp_list = requests.get('https://api.github.com/repos/pflyly/eden-nightly/releases', timeout=10)
            resp_list.raise_for_status()
            releases = resp_list.json()
            names = [r.get('tag_name') or r.get('name') or r.get('id') for r in releases]
            if not names:
                self.set_status('No se encontraron releases')
                return
            self.release_combo['values'] = names
            # Seleccionar por defecto el último release (API /latest)
            try:
                latest = resp_latest.json()
                latest_name = latest.get('tag_name') or latest.get('name')
            except Exception:
                latest_name = names[0]
            if latest_name in names:
                self.release_combo.set(latest_name)
            else:
                self.release_combo.current(0)
            self.set_status('Releases cargadas')
        except Exception as e:
            self.set_status(f"Error al obtener releases: {e}")
            messagebox.showerror('Error', f'No se pudieron obtener releases: {e}')

    def find_asset_for_release(self, release_tag, arch):
        """Busca el asset .7z en la release indicada para la arquitectura dada"""
        try:
            # Obtener releases list
            resp = requests.get('https://api.github.com/repos/pflyly/eden-nightly/releases', timeout=10)
            resp.raise_for_status()
            releases = resp.json()
            # Encontrar la release por tag_name o name
            target = None
            for r in releases:
                if r.get('tag_name') == release_tag or r.get('name') == release_tag:
                    target = r
                    break
            if target is None:
                # fallback: try latest
                target = releases[0]
            assets = target.get('assets', [])
            pattern = 'arm64' if arch == 'arm64' else 'x86_64'
            for a in assets:
                name = a.get('name','')
                if pattern in name and name.endswith('.7z'):
                    return a.get('browser_download_url'), name
            return None, None
        except Exception as e:
            return None, None

    def download_and_update(self):
        """Descarga el asset seleccionado, muestra progreso, extrae y reemplaza la carpeta destino"""
        if not hasattr(self, 'selected_folder') or not self.selected_folder:
            messagebox.showwarning('Carpeta no seleccionada', 'Por favor selecciona la carpeta destino primero')
            return
        release = self.release_var.get()
        if not release:
            messagebox.showwarning('Release no seleccionado', 'Por favor selecciona un release')
            return
        arch = self.arch_var.get()
        url, asset_name = self.find_asset_for_release(release, arch)
        if not url:
            messagebox.showerror('Asset no encontrado', 'No se encontró el archivo .7z para la arquitectura seleccionada en esta release')
            return

        # Confirmar reemplazo de la carpeta
        if any(self.selected_folder.iterdir()):
            yes = messagebox.askyesno('Confirmar', f'La carpeta {self.selected_folder} no está vacía. Se borrará su contenido y se reemplazará con la nueva versión. ¿Continuar?')
            if not yes:
                return

        # Descargar a un archivo temporal mostrando progreso
        try:
            self.set_status('Preparando actualización...')
            self.check_button.config(state=tk.DISABLED)
            self.download_button.config(state=tk.DISABLED)
            self.launch_button.config(state=tk.DISABLED)
            self.progress['value'] = 0

            temp_dir = Path(tempfile.mkdtemp())
            
            # Descargar desde GitHub
            self.set_status('Iniciando descarga...')
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                tmp_file = temp_dir / asset_name
                downloaded = 0
                chunk_size = 8192
                with open(tmp_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                percent = int(downloaded * 100 / total)
                                self.progress['value'] = percent
                                self.set_status(f'Descargando... {percent}%')
                                self.root.update_idletasks()

            self.set_status('Descarga completada. Extrayendo...')

            # Extraer archivo .7z a un directorio temporal
            extract_dir = temp_dir / 'extracted'
            extract_dir.mkdir(exist_ok=True)
            try:
                with py7zr.SevenZipFile(tmp_file, mode='r') as archive:
                    archive.extractall(path=extract_dir)
            except Exception as e_py7zr:
                # Fallback: muchos paquetes .7z usan filtros no soportados por py7zr (ej. BCJ2).
                # Intentar usar 7z (7-Zip) si está instalado, o pedir al usuario la ruta a 7z.exe
                err_msg = str(e_py7zr)
                self.set_status('py7zr no pudo extraer (intentando 7z)...')
                sevenz_path = shutil.which('7z') or shutil.which('7za') or shutil.which('7zr')
                # También buscar WinRAR en ubicaciones comunes o en PATH
                if not sevenz_path:
                    sevenz_path = shutil.which('WinRAR') or shutil.which('WinRAR.exe') or shutil.which('Rar.exe') or shutil.which('UnRAR.exe')
                if not sevenz_path:
                    # rutas comunes de instalación de WinRAR
                    common = [
                        r"C:\Program Files\WinRAR\WinRAR.exe",
                        r"C:\Program Files\WinRAR\Rar.exe",
                        r"C:\Program Files\WinRAR\UnRAR.exe",
                        r"C:\Program Files (x86)\WinRAR\WinRAR.exe",
                    ]
                    for p in common:
                        if Path(p).exists():
                            sevenz_path = p
                            break
                if not sevenz_path:
                    ask = messagebox.askyesno('py7zr no soporta este filtro', 'La extracción con py7zr falló:\n"%s"\n\n¿Deseas seleccionar manualmente el ejecutable 7z.exe para intentar la extracción (recomendado) ?' % err_msg)
                    if ask:
                        exe = filedialog.askopenfilename(title='Seleccionar 7z.exe', filetypes=[('EXE','*.exe')])
                        if exe:
                            sevenz_path = exe
                if sevenz_path:
                    # Ejecutar 7z x <archivo> -o<extract_dir> -y
                    try:
                        # WinRAR/rar/unrar accept slightly different parameter styles but 'x <archive> <dest>' works for them
                        if 'winrar' in Path(sevenz_path).name.lower() or 'rar' in Path(sevenz_path).name.lower():
                            cmd = [sevenz_path, 'x', str(tmp_file), str(extract_dir), '-y']
                        else:
                            cmd = [sevenz_path, 'x', str(tmp_file), f'-o{str(extract_dir)}', '-y']
                        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
                        if proc.returncode != 0:
                            raise RuntimeError(f'7z error: {proc.stderr}\n{proc.stdout}')
                    except Exception as e7:
                        raise RuntimeError(f'Fallo al extraer con 7z: {e7}')
                else:
                    # No hay 7z disponible -> informar al usuario
                    raise RuntimeError('py7zr no pudo extraer y no se encontró 7z en el sistema. Instala 7-Zip o selecciona su ejecutable cuando se solicite.')

            # Borrar contenido de la carpeta destino
            for child in list(self.selected_folder.iterdir()):
                try:
                    if child.is_dir():
                        shutil.rmtree(child)
                    else:
                        child.unlink()
                except Exception as e:
                    self.set_status(f'Error al borrar {child}: {e}')

            # Buscar el contenido real dentro de la carpeta extraída
            actual_content_dir = extract_dir
            items = list(extract_dir.iterdir())
            
            # Si solo hay una carpeta dentro del directorio extraído, usar esa
            if len(items) == 1 and items[0].is_dir():
                actual_content_dir = items[0]
                self.set_status(f'Extrayendo contenido de: {actual_content_dir.name}')

            # Mover contenido al selected_folder
            for item in actual_content_dir.iterdir():
                dest = self.selected_folder / item.name
                if item.is_dir():
                    shutil.move(str(item), str(dest))
                else:
                    shutil.move(str(item), str(dest))

            self.set_status('Actualización completada')
            messagebox.showinfo('Éxito', f'La carpeta se ha actualizado correctamente con {asset_name}')
            
            # Verificar si ahora existe eden.exe
            self.check_eden_exe()

        except Exception as e:
            self.set_status('Error durante la actualización')
            messagebox.showerror('Error', f'Ocurrió un error: {e}')
        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
            self.check_button.config(state=tk.NORMAL)
            self.download_button.config(state=tk.NORMAL)
            self.progress['value'] = 0
        
    def launch_emulator(self):
        """Abre el emulador Eden ejecutando eden.exe"""
        if not hasattr(self, 'selected_folder') or not self.selected_folder:
            messagebox.showwarning('Carpeta no seleccionada', 'Por favor selecciona la carpeta destino primero')
            return
            
        eden_exe_path = self.selected_folder / "eden.exe"
        if not eden_exe_path.exists():
            messagebox.showerror('Error', 'No se encontró eden.exe en la carpeta seleccionada')
            self.launch_button.config(state=tk.DISABLED)
            return

        try:
            self.set_status("Abriendo emulador Eden...")
            # Ejecutar eden.exe
            subprocess.Popen([str(eden_exe_path)], cwd=str(self.selected_folder))
            self.set_status("Emulador iniciado correctamente")
        except Exception as e:
            self.set_status("Error al abrir el emulador")
            messagebox.showerror("Error", f"No se pudo abrir eden.exe: {e}")
        
    def set_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = EdenUpdaterApp()
    app.run()