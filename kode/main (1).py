from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger
import os
from kivy.core.window import Window 
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty # Import for data properties
from kivy.clock import Clock # Import for updating UI periodically
import re # Import untuk validasi nomor telepon
from kivy.core.text import LabelBase # Import untuk pendaftaran font

# >>> IMPORT KIVYMD ADDITIONS <<<
from kivymd.app import MDApp 
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField 
from kivymd.theming import ThemeManager 
from kivymd.uix.scrollview import MDScrollView # For displaying long lists
from kivymd.uix.list import MDList, TwoLineListItem, ThreeLineListItem
# V KIVYMD INTERACTIVE WIDGETS V
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, TwoLineListItem # Digunakan dalam dialog treatment
from kivy.uix.boxlayout import BoxLayout 
from kivymd.uix.card import MDCard # Import MDCard untuk tata letak profil

# >>> IMPORT DATABASE KHUSUS <<<
# PENTING: Memanggil kelas Database dari file database.py
from salon_database import SalonDatabase # <--- KODE PEMANGGILAN DATABASE
# Pastikan file database.py ada di direktori yang sama

# --- Helper Classes (Utilities) ---

# Global font alias yang akan diisi di App.build
GLOBAL_FONT_ALIAS = 'Roboto' # Default fallback

class ImageButton(Button):
    """
    Tombol kustom yang menggunakan path gambar sebagai latar belakang.
    Jika gambar tidak ditemukan, menggunakan warna fallback.
    """
    def __init__(self, image_path=None, **kwargs):
        # [PERBAIKAN FONT]: Terapkan font_name secara eksplisit
        kwargs.setdefault('font_name', GLOBAL_FONT_ALIAS)
        super().__init__(**kwargs)
        # [PERBAIKAN KRITIS]: Atur warna default solid agar tombol selalu terlihat.
        self.background_color = (0.7, 0.2, 0.2, 1) # Warna merah tua solid sebagai fallback/dasar
        self.color = (1, 1, 1, 1) # Warna teks putih
        self.text = kwargs.get('text', 'BUTTON') # Pastikan teks terlihat

        # Atur background_normal dan background_down ke warna solid ini sebagai default
        self.background_normal = '' 
        self.background_down = ''
        
        if image_path and os.path.exists(image_path):
            # Jika gambar ditemukan, override background_normal/down
            self.background_normal = image_path
            self.background_down = image_path 
            self.background_color = (1, 1, 1, 0) # Jadikan latar belakang transparan
            self.text = '' # Hapus teks jika menggunakan gambar
        else:
            Logger.warning(f"ImageButton: Button image NOT FOUND at {image_path}. Using solid color fallback.")
            # Biarkan background_color, text, dan color yang sudah diatur di awal


# Kelas Dasar untuk mengikat tombol Menu dan melacak Screen asal
class BaseScreenMixin:
    """Mixin to add menu navigation logic to all Screens."""
    def go_to_menu_page(self, instance):
        """
        Saves the current screen and then navigates to MenuScreen.
        """
        app = MDApp.get_running_app()
        # Save the name of the current screen before navigating
        app.set_last_screen(self.name)
        self.manager.current = 'menu_page'
        Logger.info(f"{self.name}: Navigate to Menu.")

# =========================================================================
# === 1. DEFINITION OF ALL APPLICATION SCREENS ===
# =========================================================================

# --- A. MAIN SCREEN ---

class WelcomeScreen(Screen): # Tidak perlu BaseScreenMixin di WelcomeScreen
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'welcome'
        
        # --- PATH FOR WELCOME SCREEN ---
        self.gambar_path = r'aset\halaman_welcome3.png'
        self.gambar_tombol_next_path = r'IMAGE - Copy (3) - Copy\aset\tombol_next.png'
        # --- END PATH ---
        
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_path):
            image_widget = Image(source=self.gambar_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="WELCOME SCREEN (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # Tombol NEXT
        btn_next = ImageButton(
            image_path=self.gambar_tombol_next_path,
            text="NEXT",
            size_hint=(0.2, 0.1),
            pos_hint={'right': 0.95, 'y': 0.05},
            on_release=self.go_to_next_screen
        )
        root_layout.add_widget(btn_next)
        self.add_widget(root_layout)

    def go_to_next_screen(self, instance):
        self.manager.current = 'next_page'
        Logger.info("WelcomeScreen: Pindah ke Home.")

class NextScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    """Home Screen/Next Page"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'next_page'
        
        # --- PATH FOR HOME SCREEN ---
        self.gambar_halaman_selanjutnya_path = r'aset\halaman_logo2.png'
        self.gambar_menu_path = r'IMAGE - Copy (3) - Copy\aset\Menu garis 3.png' 
        self.gambar_signin_path = r'IMAGE - Copy (3) - Copy\aset\Tombol SIGN IN slide 2.png'
        self.gambar_booking_path = r'IMAGE - Copy (3) - Copy\aset\Tombol confirm booking.png' 
        # --- END PATH ---
        
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_halaman_selanjutnya_path):
            image_widget = Image(source=self.gambar_halaman_selanjutnya_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="HOME SCREEN (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))
        
        # Tombol Menu (3 Lines / Top Left)
        menu_btn = ImageButton(
            image_path=self.gambar_menu_path,
            text="MENU",
            size_hint=(0.1, 0.08),
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
            pos_hint={'x': 0.02, 'top': 0.98}, 
            on_release=self.go_to_menu_page # Uses BaseScreenMixin logic
        )
        root_layout.add_widget(menu_btn)

        # SIGN IN/PROFILE Button (Top Right)
        self.signin_btn = Button(
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            background_normal=self.gambar_signin_path if os.path.exists(self.gambar_signin_path) else '',
            background_color=(0.6, 0.1, 0.1, 0.5) if not os.path.exists(self.gambar_signin_path) else (1, 1, 1, 1),
            text="SIGN IN", # Teks awal
            size_hint=(0.18, 0.08),
            pos_hint={'right': 0.98, 'top': 0.98},
            on_release=self.handle_signin_click # NEW HANDLER
        )
        root_layout.add_widget(self.signin_btn)
        
        self.add_widget(root_layout)
        
    def on_enter(self, *args):
        """Dipanggil setiap kali layar ini ditampilkan."""
        app = MDApp.get_running_app()
        if app.is_logged_in:
            # Mengganti teks tombol dengan nama pengguna yang sudah login
            self.signin_btn.text = app.current_username
            self.signin_btn.color = (0.5, 0, 0, 1) # Teks putih
            # Menonaktifkan background image dan membuatnya transparan agar gambar Home terlihat
            self.signin_btn.background_normal = ''
            self.signin_btn.background_down = ''
            self.signin_btn.background_color = (1, 1, 1, 1) # Warna latar belakang merah maroon gelap
            self.signin_btn.bold = True
            
        else:
            # Mengatur kembali ke status default
            self.signin_btn.text = "SIGN IN"
            self.signin_btn.color = (0.5, 0, 0, 1) # Warna teks putih
            self.signin_btn.background_normal = self.gambar_signin_path
            self.signin_btn.background_down = self.gambar_signin_path
            self.signin_btn.background_color = (1, 1, 1, 1)
            self.signin_btn.bold = False

    def handle_signin_click(self, instance):
        """Menangani klik pada tombol Sign In/Nama Pengguna."""
        app = MDApp.get_running_app()
        if app.is_logged_in:
            # Pindah ke halaman opsi profil
            self.manager.current = 'profile_options_page' # NAVIGASI BARU
        else:
            # Pindah ke halaman Sign In
            self.manager.current = 'signin_page'
        
    # go_to_menu_page is now in BaseScreenMixin
        
    def go_to_signin(self, instance):
        # Fungsi lama, handle_signin_click mengambil alih
        self.manager.current = 'signin_page'
        Logger.info("NextScreen: Navigate to Sign In.")


# --- X. PROFILE OPTIONS SCREEN (BARU) ---

class ProfileOptionsScreen(Screen, BaseScreenMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'profile_options_page'
        
        root_layout = FloatLayout()
        
        # MDCard sebagai wadah utama untuk profil
        card = MDCard(
            size_hint=(0.8, 0.2), # [PERBAIKAN]: Mengurangi ukuran card karena konten berkurang
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=10,
            padding="24dp"
        )
        
        # [PERBAIKAN]: Menggunakan BoxLayout minimalis
        box = BoxLayout(
            orientation='vertical', 
            spacing='10dp', 
            padding=[20, 20, 20, 20],
            # Mengatur height agar sesuai dengan konten (hanya tombol)
            size_hint_y=None, 
            height='48dp' 
        )
        
        # Tombol Sign Out
        signout_btn = MDRaisedButton(
            text="SIGN OUT",
            size_hint=(1, None),
            height='48dp',
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_release=self.confirm_sign_out
        )
        
        # Tambahkan widget ke box (HANYA TOMBOL SIGNOUT)
        box.add_widget(signout_btn)
        
        # Mengatur Box agar terpusat di tengah Card
        card_layout = BoxLayout(orientation='vertical')
        # [PERBAIKAN FONT]: Terapkan font_name pada Label spacer (walaupun kosong)
        card_layout.add_widget(Label(size_hint_y=0.2, font_name=GLOBAL_FONT_ALIAS)) # Spacer atas
        card_layout.add_widget(box)
        card_layout.add_widget(Label(size_hint_y=0.2, font_name=GLOBAL_FONT_ALIAS)) # Spacer bawah
        
        card.add_widget(card_layout) # Card ditambahkan ke FloatLayout
        root_layout.add_widget(card)
        
        # Tombol Menu (agar bisa kembali)
        menu_btn = ImageButton(
            image_path=r'IMAGE - Copy (3) - Copy\aset\Menu garis 3.png', 
            text="MENU", 
            size_hint=(0.1, 0.08), 
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
            pos_hint={'x': 0.02, 'top': 0.98}, 
            on_release=self.go_to_menu_page
        )
        root_layout.add_widget(menu_btn)
        
        self.add_widget(root_layout)

    def on_enter(self, *args):
        """Memastikan data diperbarui saat layar ini ditampilkan."""
        # Fungsi ini tidak diperlukan lagi karena tidak ada label yang diperbarui
        Logger.info("ProfileOptionsScreen: User Profile Screen entered.")
        pass

    def confirm_sign_out(self, instance):
        """Menampilkan dialog konfirmasi sebelum Sign Out."""
        
        # [PERBAIKAN KRITIS] Definisikan fungsi yang akan dijalankan setelah dialog ditutup
        def navigate_and_reset_state(dt):
            app = MDApp.get_running_app()
            app.sign_out()
            self.manager.current = 'next_page' 
            Logger.info("ProfileOptionsScreen: Navigasi kembali ke Home setelah Sign Out.")

        # [PERBAIKAN KRITIS] Definisikan fungsi penutup dialog yang menjadwalkan navigasi
        def dismiss_dialog_and_schedule_signout(dialog_instance):
            dialog_instance.dismiss()
            # Jadwalkan navigasi dengan delay 0.5s untuk menghindari crash
            Clock.schedule_once(navigate_and_reset_state, 0.5)

        # Buat dialog
        dialog = MDDialog(
            title="Konfirmasi Logout",
            text="Apakah Anda yakin ingin keluar dari akun?",
            buttons=[
                # [PERBAIKAN FONT]: MDFlatButton dan MDRaisedButton sudah menggunakan font KivyMD global.
                MDFlatButton(text="BATAL", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="SIGN OUT", 
                    md_bg_color=(0.8, 0.2, 0.2, 1), 
                    on_release=lambda x: dismiss_dialog_and_schedule_signout(dialog)
                )
            ]
        )
        dialog.open()
        
    # Fungsi-fungsi lama (do_sign_out_and_dismiss, navigate_and_reset_state) diganti di atas.


# --- B. AUTHENTICATION SCREENS ---

class SignInScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    # Properties for MDTextField
    input_nama = ObjectProperty(None)
    input_telepon = ObjectProperty(None)
    dialog_warning = None # Properti untuk menyimpan instance dialog

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'signin_page'

        # --- PATH FOR SIGN IN SCREEN ---
        self.gambar_signin_page_path = r'IMAGE - Copy (3) - Copy\aset\Tombol SIGN IN slide 3.png'
        self.gambar_signin_next_btn_path = r'IMAGE - Copy (3) - Copy\aset\tombol_next.png'
        
        # Path for Custom Font (CLEANED UP - relies on global registration) 
        
        self.gambar_menu_path = r'IMAGE - Copy (3) - Copy\aset\Menu garis 3.png' 
        # --- END PATH ---

        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_signin_page_path):
            image_widget = Image(source=self.gambar_signin_page_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="SIGN IN SCREEN (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # Input Field Name (MDTextField sudah menggunakan KivyMD global font styles)
        text_field_size = (0.4, 0.08)
        
        self.input_nama = MDTextField(
            hint_text="Masukkan Nama Anda",
            text="", # Dikosongkan agar hint_text muncul
            size_hint=text_field_size,
            pos_hint={'center_x': 0.5, 'y': 0.42},
            mode="rectangle", 
            fill_color_normal=(1, 1, 1, 0),
            line_color_normal=(0.47, 0.16, 0.17, 1),
            line_color_focus=(0.6, 0.2, 0.2, 1),
            # FONT FIX: Remove explicit font_name attribute
        )
        root_layout.add_widget(self.input_nama)

        # Input Field Phone (MDTextField sudah menggunakan KivyMD global font styles)
        self.input_telepon = MDTextField(
            hint_text="Masukkan Nomor Telepon",
            text="", # Dikosongkan agar hint_text muncul
            size_hint=text_field_size,
            pos_hint={'center_x': 0.5, 'y': 0.23},
            mode="rectangle", 
            fill_color_normal=(1, 1, 1, 0),
            line_color_normal=(0.47, 0.16, 0.17, 1),
            line_color_focus=(0.6, 0.2, 0.2, 1),
            input_type='number',
            # FONT FIX: Remove explicit font_name attribute
        )
        root_layout.add_widget(self.input_telepon)
        
        # NEXT/Submit Button (Overlay)
        btn_next = ImageButton(
            image_path=self.gambar_signin_next_btn_path,
            text="SUBMIT",
            size_hint=(0.2, 0.1), 
            pos_hint={'right': 0.93, 'y': 0.09}, 
            on_release=self.submit_signin 
        )
        root_layout.add_widget(btn_next)
        
        # Menu Button (3 Lines / Top Left)
        menu_btn = ImageButton(
            image_path=self.gambar_menu_path,
            text="MENU",
            size_hint=(0.1, 0.08),
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
            pos_hint={'x': 0.02, 'top': 0.98}, 
            on_release=self.go_to_menu_page # Uses BaseScreenMixin logic
        )
        root_layout.add_widget(menu_btn)
        
        self.add_widget(root_layout)

    # [PERBAIKAN KRITIS]: Tambahkan on_enter untuk mengosongkan kolom input
    def on_enter(self, *args):
        """Dipanggil setiap kali layar ini ditampilkan. Digunakan untuk mengosongkan input."""
        if self.input_nama:
            self.input_nama.text = ""
        if self.input_telepon:
            self.input_telepon.text = ""
        Logger.info("SignInScreen: Input fields have been cleared.")

    def show_warning_dialog(self, title, text):
        """Menampilkan dialog peringatan KivyMD."""
        if self.dialog_warning:
            self.dialog_warning.dismiss()
        
        # [PERBAIKAN FONT]: MDDialog sudah menggunakan KivyMD global font styles.
        self.dialog_warning = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: self.dialog_warning.dismiss())
            ]
        )
        self.dialog_warning.open()
    
    def validate_phone_number(self, phone):
        """Memvalidasi format nomor telepon Indonesia (mis: 08xxxxxxxxx, 10-13 digit)."""
        # Standar umum nomor HP Indonesia: dimulai 08, panjang total 10-13 digit
        # Regex: ^08[0-9]{8,11}$ (08 diikuti 8-11 digit, total 10-13)
        pattern = r'^(08|\+628)\d{8,12}$' # Memperbolehkan 08 atau +628
        clean_phone = re.sub(r'[\s\-()]', '', phone) # Membersihkan spasi dan tanda hubung
        
        # Pastikan panjangnya berada di range yang wajar (10-15 total)
        if len(clean_phone) < 10 or len(clean_phone) > 15:
            return False

        return re.match(pattern, clean_phone)
    
    def submit_signin(self, instance):
        """
        Melakukan validasi input sebelum Sign In.
        """
        # 1. Bersihkan dan ambil input
        user_name = self.input_nama.text.replace("Nama :", "").strip() 
        phone_number = self.input_telepon.text.replace("Telepon:", "").strip() 

        # 2. Validasi Kelengkapan Data
        if not user_name or not phone_number:
            self.show_warning_dialog("Input Tidak Lengkap", "Nama dan Nomor Telepon harus diisi.")
            return

        # 3. Validasi Format Nomor Telepon Indonesia
        if not self.validate_phone_number(phone_number):
            self.show_warning_dialog(
                "Format Nomor Salah", 
                "Nomor Telepon harus dimulai dengan '08' atau '+628' dan memiliki panjang 10 sampai 15 digit."
            )
            return

        # 4. Jika validasi sukses
        app = MDApp.get_running_app()
        
        # Data pengguna disimpan ke app.current_username/phone
        app.is_logged_in = True
        app.current_username = user_name
        app.current_user_phone = phone_number
        
        # [DB INTEGRATION START]
        if app.db:
            try:
                # Tambahkan user ke tabel queue (sebagai penanda login)
                app.db.add_queue(user_name, phone_number)
                Logger.info(f"DB: User '{user_name}' berhasil ditambahkan ke antrian DB (Login).")
            except Exception as e:
                Logger.error(f"DB Error: Gagal menambahkan user ke DB: {e}")
        # [DB INTEGRATION END]

        # Pindah ke halaman sukses
        self.manager.current = 'signin_success_page' 
        
    # go_to_menu_page is now in BaseScreenMixin

class SignInSuccessScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    """Sign In Successful Screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'signin_success_page'

        # --- PATH FOR SIGN IN SUCCESSFUL SCREEN ---
        self.gambar_success_path = r'aset\halaman_signinsucces2.png'
        self.gambar_menu_path = r'IMAGE - Copy (3) - Copy\aset\Garis 3.png'
        self.gambar_tombol_next_path = r'IMAGE - Copy (3) - Copy\aset\tombol_next.png'
        # --- END PATH ---

        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_success_path):
            image_widget = Image(source=self.gambar_success_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="SIGN IN SUKSES! Selamat datang.", font_size=30, font_name=GLOBAL_FONT_ALIAS))
            
        # Tombol Menu (Garis 3 / Kiri Atas)
        menu_btn = ImageButton(
            image_path=self.gambar_menu_path,
            text="MENU",
            size_hint=(0.1, 0.08),
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
            pos_hint={'x': 0.02, 'top': 0.98}, 
            on_release=self.go_to_menu_page # Uses BaseScreenMixin logic
        )
        root_layout.add_widget(menu_btn)

        self.add_widget(root_layout)

    # go_to_menu_page is now in BaseScreenMixin
        
    def go_to_next_screen(self, instance):
        self.manager.current = 'next_page'
        Logger.info("SignInSuccessScreen: Navigate to Home.")


# --- C. MENU & SUB-MENU SCREENS ---

class MenuScreen(Screen):
    """
    MenuScreen is the navigation hub. Its menu button acts as a 'Close/Back' button.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu_page'

        # --- PATH FOR MENU SCREEN ---
        self.gambar_menu_page_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\halaman_menu.png' 
        self.gambar_tombol_home_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\image_58649f.png' 
        self.gambar_menu_path = r'IMAGE - Copy (3) - Copy\aset\halaman_garis3.png'
        self.gambar_tombol_about_path = r'IMAGE - Copy (3) - Copy\aset\Text About.png'
        self.gambar_tombol_catalog_path = r'IMAGE - Copy (3) - Copy\aset\Text catalog.png'
        self.gambar_tombol_booking_path = r'IMAGE - Copy (3) - Copy\aset\Text booking.png'
        self.gambar_tombol_antrian_path = r'IMAGE - Copy (3) - Copy\aset\Text check the queue.png' 
        # --- END PATH ---
        
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_menu_page_path):
            image_widget = Image(source=self.gambar_menu_page_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="MENU SCREEN (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # Tombol Menu (3 Lines / Top Left) - ACTS AS CLOSE/BACK BUTTON
        menu_btn = ImageButton(
            image_path=self.gambar_menu_path,
            text="TUTUP",
            size_hint=(0.1, 0.08),
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
            pos_hint={'x': 0.02, 'top': 0.98}, 
            on_release=self.go_to_last_screen # Returns to source Screen
        )
        root_layout.add_widget(menu_btn)
        
        # Ukuran dan Posisi Tombol Sub-Menu (Berpusat Horizontal)
        BUTTON_SIZE = (0.3, 0.1) # Lebar 30%, Tinggi 10%
        # [PERUBAHAN KRITIS] Geser ke kiri (x kecil) agar menempel di pojok kiri
        # Kita akan menggunakan x: 0.02 agar sejajar dengan tombol TUTUP
        LEFT_X = 0.02 
        
        # Penempatan tombol pertama (ABOUT) tepat di bawah tombol TUTUP (top: 0.98 - 0.08 = 0.90)
        # Kita akan menggunakan x: 0.02 dan top: 0.90
        # Jarak vertikal antar tombol akan dibuat sama (misalnya, dikurangi 0.1 dari 'top')
        
        # Tombol ABOUT
        btn_about = Button(
            text="ABOUT", 
            size_hint=BUTTON_SIZE, 
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.90
            pos_hint={'x': LEFT_X, 'top': 0.90}, 
            background_color=(0.5, 0, 0, 1),
            color=(1, 1, 1, 1),
            on_release=self.go_to_about
        )
        root_layout.add_widget(btn_about)
        
        # Tombol CATALOG (0.90 - 0.1 = 0.80)
        btn_catalog = Button(
            text="CATALOG", 
            size_hint=BUTTON_SIZE, 
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.80
            pos_hint={'x': LEFT_X, 'top': 0.80}, 
            background_color=(0.5, 0, 0, 1), 
            color=(1, 1, 1, 1), 
            on_release=self.go_to_catalog
        )
        root_layout.add_widget(btn_catalog)
        
        # Tombol BOOKING (0.80 - 0.1 = 0.70)
        btn_booking = Button(
            text="BOOKING", 
            size_hint=BUTTON_SIZE, 
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.70
            pos_hint={'x': LEFT_X, 'top': 0.70}, 
            background_color=(0.5, 0, 0, 1), 
            color=(1, 1, 1, 1), 
            on_release=self.check_and_go_to_booking
        )
        root_layout.add_widget(btn_booking)
        
        # Tombol CHECK ANTRIAN (0.70 - 0.1 = 0.60)
        btn_antrian = Button(
            text="CHECK ANTRIAN", 
            size_hint=BUTTON_SIZE, 
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.60
            pos_hint={'x': LEFT_X, 'top': 0.60}, 
            background_color=(0.5, 0, 0, 1), 
            color=(1, 1, 1, 1), 
            on_release=self.go_to_check_antrian
        )
        root_layout.add_widget(btn_antrian)
        
        # HOME Button (0.60 - 0.1 = 0.50)
        # DIPERBAIKI: Menggunakan tinggi 0.1, menyesuaikan posisi top menjadi 0.50 (0.60 - 0.1)
        btn_home = Button(
            text="HOME",
            size_hint=BUTTON_SIZE, # Menggunakan ukuran standar (0.3, 0.1)
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.50
            pos_hint={'x': LEFT_X, 'top': 0.50}, 
            background_color=(0.5, 0, 0, 1),
            color=(1, 1, 1, 1),
            on_release=self.go_to_home # Home button is for direct navigation to NextScreen
        )
        root_layout.add_widget(btn_home) 

        self.add_widget(root_layout)
    
    def go_to_home(self, instance): # Tombol HOME
        self.manager.current = 'next_page'
        Logger.info("MenuScreen: HOME Button clicked! Navigating back to Home successfully.")

    def go_to_last_screen(self, instance): # Menu Button on Menu Screen
        """Returns to the last saved screen (toggle behavior)."""
        app = MDApp.get_running_app()
        # Default to 'next_page' (Home) if last_screen_name is empty or invalid
        target_screen = app.last_screen_name if app.last_screen_name in self.manager.screen_names else 'next_page'
        self.manager.current = target_screen
        Logger.info(f"MenuScreen: Returning to source screen: {target_screen}")
        
    def go_to_about(self, instance):
        self.manager.current = 'about_page'
    def go_to_catalog(self, instance):
        self.manager.current = 'catalog_page'
        
    def check_and_go_to_booking(self, instance):
        """Checks login status before allowing navigation to Booking."""
        app = MDApp.get_running_app()
        if app.is_logged_in:
            self.manager.current = 'booking_page'
            Logger.info("MenuScreen: User is logged in. Navigating to Booking.")
        else:
            self.show_login_required_dialog()
            Logger.warning("MenuScreen: Booking blocked. User not logged in.")
            
    def show_login_required_dialog(self):
        """Displays a dialog warning that login is required."""
        dialog = MDDialog(
            title="Akses Ditolak",
            text="You must Sign In first to make a Booking.",
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()
        
    def go_to_check_antrian(self, instance):
        self.manager.current = 'check_antrian_page'


# --- D. SUB-MENU SCREENS ---

class AboutScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'about_page'
        # --- PATH FOR ABOUT SCREEN ---
        self.gambar_about_path = r'aset\halaman_about3.png'
        self.gambar_menu_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\menu_icon.png'
        # --- END PATH ---
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_about_path):
            image_widget = Image(source=self.gambar_about_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="ABOUT PAGE (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        menu_btn = ImageButton(image_path=self.gambar_menu_path, text="MENU", size_hint=(0.1, 0.08), pos_hint={'x': 0.02, 'top': 0.98}, on_release=self.go_to_menu_page) 
        root_layout.add_widget(menu_btn)
        self.add_widget(root_layout)

class CatalogScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'catalog_page'
        # --- PATH FOR CATALOG SCREEN ---
        self.gambar_catalog_path = r'aset\halaman_catalog3.png'
        self.gambar_menu_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\menu_icon.png'
        # --- END PATH ---
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_catalog_path):
            # Ensures Image fills the entire screen.
            image_widget = Image(source=self.gambar_catalog_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos=(0, 0))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="CATALOG PAGE (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        menu_btn = ImageButton(image_path=self.gambar_menu_path, text="MENU", size_hint=(0.1, 0.08), pos_hint={'x': 0.02, 'top': 0.98}, on_release=self.go_to_menu_page) 
        root_layout.add_widget(menu_btn)
        self.add_widget(root_layout)

class BookingScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    # Property to store user selection
    selected_date = StringProperty("SCHEDULE")
    selected_treatment = StringProperty("CHOOSE YOUR TREATMENT")
    
    TREATMENTS = {} 

    def load_treatments_from_db(self):
        """Memuat daftar treatment dari database ke dalam properti kelas."""
        app = MDApp.get_running_app()
        self.TREATMENTS = {} # Pastikan direset
        
        if app.db:
            try:
                # Panggil fungsi yang baru kita buat di database.py
                db_data = app.db.get_all_treatments() 
                
                # Mengubah hasil tuple dari DB menjadi format dictionary
                for name, price in db_data:
                    self.TREATMENTS[name] = price
                Logger.info(f"BookingScreen: Data Treatment berhasil dimuat. Total: {len(self.TREATMENTS)}")
                
            except Exception as e:
                Logger.error(f"DB Error: Gagal memuat treatments: {e}")

    def on_enter(self, *args):
        """Dipanggil setiap kali layar Booking ditampilkan."""
        # Panggil fungsi yang baru dibuat untuk memuat data treatment
        self.load_treatments_from_db()
        
        # Reset tampilan tombol di sini
        self.selected_date = "SCHEDULE"
        self.selected_treatment = "CHOOSE YOUR TREATMENT"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'booking_page'
        self.treatment_dialog = None
        
        # --- PATH FOR BOOKING SCREEN ---
        self.gambar_booking_path = r'aset\halaman_booking3.png'
        self.gambar_tombol_next_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\next_button.png'
        self.gambar_menu_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\menu_icon.png'
        self.gambar_dropdown_icon_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\dropdown_icon.png'
        # --- END PATH ---
        
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_booking_path):
            image_widget = Image(source=self.gambar_booking_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="BOOKING PAGE (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # 1. Tombol Schedule (Memunculkan Kalender)
        self.btn_schedule = Button(
            text=self.selected_date, # Text binding
            size_hint=(0.6, 0.1),
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            pos_hint={'center_x': 0.5, 'y': 0.55},
            background_color=(1, 1, 1, 0), 
            color=(0.47, 0.16, 0.17, 1), 
            bold=True,
            on_release=self.show_date_pickers 
        )
        root_layout.add_widget(self.btn_schedule)
        
        # Add dropdown icon (bottom triangle) - using MD App
        icon_schedule = MDIconButton(
            icon="menu-down", # Bottom triangle icon
            size_hint=(None, None),
            size=('48dp', '48dp'),
            pos_hint={'center_x': 0.78, 'y': 0.56},
            theme_text_color="Custom",
            text_color=(0.47, 0.16, 0.17, 1),
            on_release=self.show_date_pickers
        )
        root_layout.add_widget(icon_schedule)

        # 2. Treatment Button (Opens Selection Dialog)
        self.btn_treatment = Button(
            text=self.selected_treatment, # Text binding
            size_hint=(0.6, 0.1),
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            pos_hint={'center_x': 0.5, 'y': 0.35},
            background_color=(1, 1, 1, 0), 
            color=(0.47, 0.16, 0.17, 1), 
            bold=True,
            on_release=self.show_treatment_dialog # Memanggil Dialog Pilihan
        )
        root_layout.add_widget(self.btn_treatment)
        
        # Add dropdown icon (bottom triangle) - for Treatment
        icon_treatment = MDIconButton(
            icon="menu-down",
            size_hint=(None, None),
            size=('48dp', '48dp'),
            pos_hint={'center_x': 0.78, 'y': 0.36},
            theme_text_color="Custom",
            text_color=(0.47, 0.16, 0.17, 1),
            on_release=self.show_treatment_dialog
        )
        root_layout.add_widget(icon_treatment)
        
        # 3. NEXT Button to Booking List
        btn_next = ImageButton(image_path=self.gambar_tombol_next_path, text="NEXT", size_hint=(0.2, 0.1), pos_hint={'right': 0.95, 'y': 0.05}, on_release=self.go_to_booking_list)
        root_layout.add_widget(btn_next)

        # Menu Button (3 Lines / Top Left)
        # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
        menu_btn = ImageButton(image_path=self.gambar_menu_path, text="MENU", size_hint=(0.1, 0.08), pos_hint={'x': 0.02, 'top': 0.98}, on_release=self.go_to_menu_page) 
        root_layout.add_widget(menu_btn)
        
        # Bind button text to Screen properties (for automatic update)
        self.bind(selected_date=self.on_date_update)
        self.bind(selected_treatment=self.on_treatment_update)
        
        self.add_widget(root_layout)

    def on_date_update(self, instance, value):
        self.btn_schedule.text = value
    
    def on_treatment_update(self, instance, value):
        self.btn_treatment.text = value

    # --- DATE FUNCTION (DATE PICKER) ---
    def show_date_pickers(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_ok)
        date_dialog.open()



    def on_date_ok(self, instance, value, date_range):
        self.selected_date = value.strftime("%d %B %Y")
        self.btn_schedule.text = self.selected_date

    # --- TREATMENT FUNCTION (DIALOG) ---
    def show_treatment_dialog(self, instance):
        
        # 1. Pastikan data sudah dimuat
        if not self.TREATMENTS:
            self.load_treatments_from_db()
            if not self.TREATMENTS:
                 Logger.error("BookingScreen: Data Treatment kosong atau gagal dimuat.")
                 # Tampilkan pesan ke user
                 dialog = MDDialog(title="Peringatan", text="Data Treatment tidak tersedia.", size_hint=(0.7, 0.4))
                 dialog.open()
                 return

        # Hitung tinggi MDList berdasarkan jumlah item (asumsi TwoLineListItem = 56dp)
        num_items = len(self.TREATMENTS)
        list_height = num_items * 56 # Tinggi dalam dp

        treatment_list_widget = MDList(
            # [PERBAIKAN KRITIS]: Atur size_hint_y ke None dan hitung height otomatis
            size_hint_y=None, 
            height=f'{list_height}dp'
        )
        
        # 2. Loop menggunakan data treatment yang sudah dimuat dari database
        for name, price in self.TREATMENTS.items():
            # Menggunakan TwoLineListItem untuk menampilkan Nama Treatment dan Harga
            item = TwoLineListItem( 
                text=name,
                secondary_text=f"Harga: Rp {price:,.0f}",
                # Mengirimkan nama dan harga saat dipilih
                on_release=lambda x, n=name, p=price: self.select_treatment(n, p)
            )
            treatment_list_widget.add_widget(item)
            
        # 3. Setup Dialog
        # [PERBAIKAN KRITIS] Gunakan BoxLayout untuk content_cls dengan tinggi terbatas
        content = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            # Batasi tinggi maksimal yang diperbolehkan di dalam dialog
            height="300dp" 
        )
        
        # MDScrollView untuk membuat daftar bisa di-scroll
        scroll_view = MDScrollView()
        scroll_view.add_widget(treatment_list_widget)
        content.add_widget(scroll_view) # Tambahkan ScrollView ke content_cls

        self.treatment_dialog = MDDialog(
            title="Pilih Treatment",
            type="custom",
            content_cls=content, 
            # [PERBAIKAN KRITIS] Biarkan tinggi (y) diatur oleh content_cls (size_hint_y=None)
            size_hint=(0.8, None) 
        )
        self.treatment_dialog.open()

    def select_treatment(self, treatment_name, treatment_price):
        """Called when a treatment is selected from the dialog."""
        
        self.selected_treatment = treatment_name
        self.treatment_dialog.dismiss()
        
        app = MDApp.get_running_app()
        
        # CRITICAL: Check if date is selected before adding the item
        if self.selected_date == "SCHEDULE":
            dialog = MDDialog(
                title="Peringatan",
                text="Harap pilih tanggal terlebih dahulu sebelum memilih treatment.",
                buttons=[
                    MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
            return
            
        # Tambahkan booking ke data sementara aplikasi
        app.booking_data.append({
            'date': self.selected_date,
            'treatment': treatment_name,
            'price': treatment_price
        })
        Logger.info(f"BookingScreen: Booking item added: {treatment_name} - Rp {treatment_price:,.0f}")
        
    def go_to_booking_list(self, instance):
        """Called when the NEXT button is pressed."""
        app = MDApp.get_running_app()
        
        # Check if booking data has been selected
        if not app.booking_data:
            Logger.warning("BookingScreen: Anda harus memilih setidaknya satu Treatment!")
            dialog = MDDialog(
                title="Peringatan",
                text="Anda harus memilih setidaknya satu Treatment dan Jadwal.",
                buttons=[
                    MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
            return
            
        self.manager.current = 'booking_list_page'
        
    # go_to_menu_page is now in BaseScreenMixin

class BookingListScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    # Property for total price
    total_harga = StringProperty("Rp 0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'booking_list_page'
        # --- PATH FOR BOOKING LIST SCREEN ---
        self.gambar_booking_list_path = r'aset\halaman_bookinglist2.png'
        self.gambar_tombol_submit_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\submit_button.png'
        self.gambar_menu_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\menu_icon.png'
        # --- END PATH ---
        
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_booking_list_path):
            image_widget = Image(source=self.gambar_booking_list_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="BOOKING LIST PAGE (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # ScrollView for the booking list
        self.scroll_view = MDScrollView(
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            bar_width=5
        )
        self.booking_mdlist = MDList()
        self.scroll_view.add_widget(self.booking_mdlist)
        root_layout.add_widget(self.scroll_view)
        
        # Label Total Harga
        self.label_total = Label(
            text=f"TOTAL: {self.total_harga}",
            font_size='22sp',
            bold=True,
            color=(0.4, 0.1, 0.1, 1),
            # [PERBAIKAN FONT]: Terapkan font_name
            font_name=GLOBAL_FONT_ALIAS,
            size_hint=(0.8, 0.1), 
            pos_hint={'center_x': 0.5, 'y': 0.25}
        )
        root_layout.add_widget(self.label_total)

        # Tombol Submit Booking (Ensures 1x click)
        btn_submit = ImageButton(image_path=self.gambar_tombol_submit_path, text="CONFIRM", size_hint=(0.25, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05}, on_release=self.confirm_booking)
        root_layout.add_widget(btn_submit)

        # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
        menu_btn = ImageButton(image_path=self.gambar_menu_path, text="MENU", size_hint=(0.1, 0.08), pos_hint={'x': 0.02, 'top': 0.98}, on_release=self.go_to_menu_page) 
        root_layout.add_widget(menu_btn)
        self.add_widget(root_layout)
        
    def on_enter(self, *args):
        """Called every time this screen is displayed."""
        self.update_booking_list()

    def update_booking_list(self):
        """Updates the booking list from global data and calculates the total."""
        app = MDApp.get_running_app()
        self.booking_mdlist.clear_widgets() # Clear old list
        
        total = 0
        
        if not app.booking_data:
            # [PERBAIKAN FONT]: MDList item sudah menggunakan KivyMD global font styles.
            self.booking_mdlist.add_widget(OneLineListItem(text="Belum ada treatment yang dipilih."))
            
        for item in app.booking_data:
            total += item['price']
            
            # Display Treatment, Date, and Price
            item_widget = TwoLineListItem( 
                text=f"{item['treatment']} ({item['date']})",
                secondary_text=f"Rp {item['price']:,.0f}",
            )
            self.booking_mdlist.add_widget(item_widget)
            
        self.total_harga = f"Rp {total:,.0f}"
        self.label_total.text = f"TOTAL: {self.total_harga}"
        Logger.info(f"BookingListScreen: Booking list updated. Total: {self.total_harga}")


    def confirm_booking(self, instance):
        app = MDApp.get_running_app()
        
        if app.current_username and app.booking_data:
            # [DB INTEGRATION START]
            if app.db:
                try:
                    for item in app.booking_data:
                        # Panggil metode add_booking di instance database
                        # Ini akan menyimpan ke booking dan otomatis menambah ke queue
                        app.db.add_booking(
                            nama=app.current_username,
                            tanggal=item['date'],
                            treatment=item['treatment'],
                            harga=item['price'],
                            telepon=app.current_user_phone # Kirim nomor telepon untuk antrian
                        )
                    Logger.info(f"DB: Booking berhasil disimpan dan antrian dibuat untuk user: {app.current_username}")
                except Exception as e:
                     Logger.error(f"DB Error: Gagal menyimpan booking ke DB: {e}")
            # [DB INTEGRATION END]

            # Kosongkan booking_data setelah berhasil dikonfirmasi
            app.booking_data.clear()

        self.manager.current = 'booking_success_page'
    # go_to_menu_page is now in BaseScreenMixin

class BookingSuccessScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'booking_success_page'
        # --- PATH FOR BOOKING SUCCESS SCREEN ---
        self.gambar_success_path = r'aset\halaman_bookingsucces2.png'
        self.gambar_check_queue_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\check_queue_button.png' 
        self.gambar_menu_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\menu_icon.png'
        # --- END PATH ---
        root_layout = FloatLayout()
        
        if os.path.exists(self.gambar_success_path):
            image_widget = Image(source=self.gambar_success_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="BOOKING SUCCESS PAGE (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # CHECK THE QUEUE Button (Adjusted click area and navigation)
        btn_check_queue = ImageButton(
            image_path=self.gambar_check_queue_path,
            text="CHECK QUEUE",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05}, # Position at bottom
            on_release=self.go_to_check_antrian # Ensures navigation to Check Antrian
        )
        root_layout.add_widget(btn_check_queue)

        # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
        menu_btn = ImageButton(image_path=self.gambar_menu_path, text="MENU", size_hint=(0.1, 0.08), pos_hint={'x': 0.02, 'top': 0.98}, on_release=self.go_to_menu_page) 
        root_layout.add_widget(menu_btn)
        self.add_widget(root_layout)
    def go_to_check_antrian(self, instance):
        # Ensures navigation to the queue page, not home
        self.manager.current = 'check_antrian_page'
    # go_to_menu_page is now in BaseScreenMixin

class CheckAntrianScreen(Screen, BaseScreenMixin): # Inherits BaseScreenMixin
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'check_antrian_page'
        
        # --- PATH FOR CHECK ANTRIAN SCREEN ---
        self.gambar_antrian_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\halaman_check_antrian.png'
        self.gambar_menu_path = r'C:\Users\asus\OneDrive\Documents\IMAGE\menu_icon.png'
        # --- END PATH ---
        
        root_layout = FloatLayout()
        
        # Background
        if os.path.exists(self.gambar_antrian_path):
            image_widget = Image(source=self.gambar_antrian_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            root_layout.add_widget(image_widget)
        else:
            # [PERBAIKAN FONT]: Terapkan font_name
            root_layout.add_widget(Label(text="CHECK ANTRIAN PAGE (Gambar Tidak Ditemukan)", font_name=GLOBAL_FONT_ALIAS))

        # =========================================================================
        # >>> WIDGET FOR DISPLAYING THE QUEUE LIST <<<
        # =========================================================================
        
        # ScrollView (To handle long queue lists)
        self.scroll_view = MDScrollView(
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            bar_width=5 # Make scrollbar visible
        )
        # MDList (To hold queue items)
        self.queue_mdlist = MDList()
        self.scroll_view.add_widget(self.queue_mdlist)
        root_layout.add_widget(self.scroll_view)

        # Header/Title Label
        label_header = Label(text="DAFTAR ANTRIAN SAAT INI:", font_size='24sp', bold=True, color=(0.4, 0.1, 0.1, 1), 
             # [PERBAIKAN FONT]: Terapkan font_name
             font_name=GLOBAL_FONT_ALIAS,
             size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'y': 0.85})
        root_layout.add_widget(label_header)
        
        # Tombol Hapus Antrian Teratas (Untuk tujuan testing dan administrasi)
        btn_remove = MDRaisedButton(
            text="Hapus Antrian Teratas (ADMIN)",
            size_hint=(0.5, 0.07),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            md_bg_color=(0.1, 0.1, 0.1, 1),
            on_release=self.remove_top_queue
        )
        root_layout.add_widget(btn_remove)


        # Menu Button (3 Lines / Top Left)
        # DIPERBAIKI: Menggunakan x: 0.02 dan top: 0.98 untuk pojok kiri atas
        menu_btn = ImageButton(image_path=self.gambar_menu_path, text="MENU", size_hint=(0.1, 0.08), pos_hint={'x': 0.02, 'top': 0.98}, on_release=self.go_to_menu_page) 
        root_layout.add_widget(menu_btn)
        self.add_widget(root_layout)
        
    def on_enter(self, *args):
        """Called every time this screen is displayed."""
        self.update_queue_list()

    def update_queue_list(self):
        """Updates the queue list from the database."""
        app = MDApp.get_running_app()
        self.queue_mdlist.clear_widgets() # Clear old list
        
        queue_data = []
        if app.db:
            try:
                # Mengambil data antrian dari database
                queue_data = app.db.get_queue() 
            except Exception as e:
                Logger.error(f"DB Error: Gagal mengambil antrian dari DB: {e}")
                queue_data = []

        # Masukkan setiap item dari daftar DB ke MDList
        if not queue_data:
            self.queue_mdlist.add_widget(OneLineListItem(text="Antrian kosong. Silakan Sign In!"))
            return
            
        for index, item in enumerate(queue_data):
            # item = (id, nama, telepon, waktu)
            queue_id = item[0]
            name = item[1]
            telepon = item[2]
            waktu_masuk = item[3].split(' ')[1].split('.')[0] # Ambil jam:menit:detik
            
            item_widget = TwoLineListItem(
                text=f"[{index + 1}] {name}", # Nomor antrian dan Nama
                secondary_text=f"ID: {queue_id} | Masuk: {waktu_masuk} | Telp: {telepon}",
                font_style='Subtitle1'
            )
            self.queue_mdlist.add_widget(item_widget)
        Logger.info(f"CheckAntrianScreen: Daftar antrian diperbarui. Total {len(queue_data)} item.")
        
    def remove_top_queue(self, instance):
        """Menghapus antrian teratas (untuk tujuan testing)."""
        app = MDApp.get_running_app()
        
        if not app.db:
            Logger.warning("DB: Database tidak aktif.")
            return

        queue_data = app.db.get_queue()
        
        if not queue_data:
            MDDialog(
                title="Antrian Kosong",
                text="Tidak ada antrian untuk dihapus.",
                buttons=[MDFlatButton(text="OK")]
            ).open()
            return
            
        # Ambil ID antrian teratas
        top_queue_id = queue_data[0][0]
        nama_customer = queue_data[0][1]
        
        try:
            app.db.remove_queue_by_id(top_queue_id)
            self.update_queue_list() # Perbarui tampilan
            MDDialog(
                title="Selesai Dilayani (ADMIN)",
                text=f"Antrian ID #{top_queue_id} ({nama_customer}) telah dihapus.",
                buttons=[MDFlatButton(text="OK")]
            ).open()
        except Exception as e:
            MDDialog(
                title="Error",
                text=f"Gagal menghapus antrian: {e}",
                buttons=[MDFlatButton(text="OK")]
            ).open()
        
    # go_to_menu_page is now in BaseScreenMixin


# =========================================================================
# === 2. MAIN APPLICATION ===
# =========================================================================

class SekayuApp(MDApp): 
    # *GLOBAL LOGIN STATUS*
    is_logged_in = BooleanProperty(False)
    current_username = StringProperty("SIGN IN") # Teks default
    current_user_phone = StringProperty("")
    # NEW PROPERTY TO TRACK SOURCE SCREEN
    last_screen_name = StringProperty('next_page')
    
    # Instance database
    db = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # INISIALISASI DATABASE DI SINI
        self.db = SalonDatabase()
        
        # INITIALIZE GLOBAL BOOKING LIST (Data sementara sebelum konfirmasi)
        self.booking_data = [] 
        
    def build(self):
        
        # 1. Daftarkan dan Atur Font Kustom
        # *******************************************************************
        # V CRITICAL: GLOBAL FONT PATH V
        # Pengguna hanya perlu mengubah path di sini.
        # *******************************************************************
        # GANTI PATH FONT INI SAJA UNTUK MENGUBAH FONT SELURUH APLIKASI
        custom_font_file = r'fonts/Poppins-Bold.ttf' 
        font_alias = 'CustomFont'
        
        if os.path.exists(custom_font_file):
              LabelBase.register(name=font_alias, fn_regular=custom_font_file)
              Logger.info(f"Font: Font '{font_alias}' didaftarkan.")
        else:
              Logger.warning(f"Font: File font tidak ditemukan di {custom_font_file}. Menggunakan font default 'Roboto'.")
              font_alias = 'Roboto' 

        global GLOBAL_FONT_ALIAS
        GLOBAL_FONT_ALIAS = font_alias
        
        # 2. Override KivyMD font styles
        font_styles_to_override = [
             "H1", "H2", "H3", "H4", "H5", "H6", 
             "Subtitle1", "Subtitle2", 
             "Body1", "Body2", 
             "Button", "Caption", "Overline", "HelperText"
        ]
        
        for style in font_styles_to_override:
              self.theme_cls.font_styles[style] = [font_alias, 16, False, 0.15] 
        
        # 3. Set Tema
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red" 
        
        sm = ScreenManager(transition=NoTransition()) 
        
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(NextScreen(name='next_page'))
        sm.add_widget(SignInScreen(name='signin_page'))
        sm.add_widget(SignInSuccessScreen(name='signin_success_page')) 
        sm.add_widget(ProfileOptionsScreen(name='profile_options_page')) 
        sm.add_widget(MenuScreen(name='menu_page'))
        sm.add_widget(AboutScreen(name='about_page'))
        sm.add_widget(CatalogScreen(name='catalog_page'))
        sm.add_widget(BookingScreen(name='booking_page'))
        sm.add_widget(BookingListScreen(name='booking_list_page'))
        sm.add_widget(BookingSuccessScreen(name='booking_success_page'))
        sm.add_widget(CheckAntrianScreen(name='check_antrian_page'))
        
        return sm
        
    def set_last_screen(self, screen_name):
        """Method to save the name of the currently active screen before opening the menu."""
        # Prevent 'menu_page' from being saved as the last screen
        if screen_name != 'menu_page':
             self.last_screen_name = screen_name
             Logger.info(f"App: Last screen set to {screen_name}")
        else:
             Logger.info("App: Attempted to set 'menu_page' as last screen, blocked.")

    def set_current_screen(self, screen_name):
        """
        Custom method to handle screen switching and automatically
        set the last screen name.
        """
        sm = self.root
        if sm and screen_name in sm.screen_names:
            if sm.current != 'menu_page':
                self.set_last_screen(sm.current)
            sm.current = screen_name
            Logger.info(f"App: Navigated to {screen_name}")
            
    def sign_out(self):
        """Meriset status login (tidak termasuk navigasi)."""
        self.is_logged_in = False
        self.current_username = "SIGN IN"
        self.current_user_phone = ""
        self.booking_data = [] # Kosongkan data booking sementara
        Logger.info("App: User logged out successfully (State Reset).")
        
    def on_stop(self):
        """Menutup koneksi database ketika aplikasi dihentikan."""
        if self.db:
             # Menutup koneksi database (asumsi ada fungsi close() di kelas Database)
             try:
                 # WARNING: Pastikan db.conn.close() hanya dipanggil jika db.conn benar-benar ada dan terbuka!
                 if hasattr(self.db, 'conn') and self.db.conn is not None:
                     self.db.conn.close() 
                     Logger.info("App: Koneksi database ditutup.")
             except Exception as e:
                 Logger.error(f"App: Gagal menutup koneksi DB: {e}")


if __name__ == '__main__':
    SekayuApp().run()