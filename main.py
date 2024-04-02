import requests
import configparser
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.colorchooser import askcolor
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.initialize_ui()

    def initialize_ui(self):
        # Read config file / Config dosyasını oku
        config = self.read_config()
        # Get language setting / Dil ayarını al
        self.language = config['Settings']['language'].lower()
        # If language is Turkish / Dil Türkçe ise
        if self.language == 'turkish':
            # Use Turkish text / Türkçe metinleri kullan
            self.title = "SkyCast - Hava Durumu Uygulaması"
            self.city_label_text = "Şehir:"
            self.button_text = "Hava Durumu Bilgisini Al"
            self.error_message = "Hava durumu bilgileri alınamadı."
            self.language_button_text = "İngilizce"
            self.color_button_text = "Arka Plan Rengini Seç"
        else:
            # Use English text / İngilizce metinleri kullan
            self.title = "SkyCast - Weather Application"
            self.city_label_text = "City:"
            self.button_text = "Get Weather Information"
            self.error_message = "Weather data could not be retrieved."
            self.language_button_text = "Turkish"
            self.color_button_text = "Select Background Color"

        # Set window title / Pencere başlığını ayarla
        self.root.title(self.title)
        # Set window background color / Pencere arka plan rengini ayarla
        self.root.configure(bg="#ffcccc")
        # Set window size / Pencere boyutunu ayarla
        self.root.geometry("600x400")

        # Button style / Buton stili
        self.style = ttk.Style()
        self.style.configure("TButton", foreground="#00FF56", background="#007bff", relief=tk.FLAT, font=("Helvetica", 16), borderwidth=1)
        self.style.map("TButton", background=[('active', '#0056b3')], foreground=[('active', '#FF00EF')], relief=[('active', tk.FLAT), ('disabled', tk.FLAT)])

        # Label font / Etiket fontu
        self.label_font = ("Helvetica", 20)

        # City label / Şehir etiketi
        self.city_label = tk.Label(self.root, text=self.city_label_text, font=self.label_font, bg="#ffcccc", fg="#FFFFFF")
        self.city_label.pack(pady=10)
        # City entry / Şehir giriş kutusu
        self.city_entry = ttk.Entry(self.root, font=self.label_font)
        self.city_entry.pack(pady=10)
        # Get weather button / Hava durumu bilgisini al butonu
        self.get_weather_button = ttk.Button(self.root, text=self.button_text, command=self.get_weather_info)
        self.get_weather_button.pack(pady=10)

        # Call get_weather_info function on pressing Enter / Enter tuşuna basıldığında get_weather_info fonksiyonunu çağır
        self.city_entry.bind("<Return>", self.get_weather_info)

        # Language change button / Dil değiştirme butonu
        self.language_button = ttk.Button(self.root, text=self.language_button_text, command=self.change_language)
        self.language_button.pack(pady=10)

        # Color selection button / Arka plan rengi seçme butonu
        self.color_button = ttk.Button(self.root, text=self.color_button_text, command=self.select_color)
        self.color_button.pack(pady=10)

    # Read config file / Config dosyasını oku
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    # Get weather data / Hava durumu bilgisini al
    def get_weather(self, city, language):
        # Read config file / Config dosyasını oku
        config = self.read_config()
        # Get API key / API anahtarını al
        api_key = config['API']['api_key']
        # Make request to weather API / Hava durumu API'sine istek yap
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang={language}'
        response = requests.get(url)
        # If request is successful, return data / İstek başarılı ise verileri döndür
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Weather data could not be retrieved.")
            return None

    # Show weather information / Hava durumu bilgilerini göster
    def get_weather_info(self, event=None):
        # Get city from entry / Giriş kutusundan şehir bilgisini al
        city = self.city_entry.get()
        # Read config file / Config dosyasını oku
        config = self.read_config()
        # Get language setting / Dil ayarını al
        language = config['Settings']['language'].lower()
        # Set language-dependent labels / Dil bağlı etiketleri ayarla
        if language == 'turkish':
            language_code = 'tr'
            language_label = "Şehrin"
            temperature_label = "Sıcaklık"
            condition_label = "Durum"
            time_label = "Saat"
        else:
            language_code = 'en'
            language_label = "City"
            temperature_label = "Temperature"
            condition_label = "Condition"
            time_label = "Time"
        # Get weather data / Hava durumu verilerini al
        weather_data = self.get_weather(city, language_code)
        # If data is available, show information / Veri mevcutsa bilgileri göster
        if weather_data:
            temperature = weather_data['current']['temp_c']
            condition = weather_data['current']['condition']['text']
            localtime = datetime.strptime(weather_data['location']['localtime'], '%Y-%m-%d %H:%M')
            localtime_str = localtime.strftime('%Y-%m-%d %H:%M')
            if weather_data['current']['is_day'] == 1:
                day_status = "Day"
            else:
                day_status = "Night"
            messagebox.showinfo("Weather Information", f"{language_label}: {city}\n{temperature_label}: {temperature}°C\n{condition_label}: {condition}\n{time_label}: {localtime_str}\nDay Status: {day_status}")
        else:
            messagebox.showerror("Error", self.error_message)

    # Change language setting / Dil ayarını değiştir
    def change_language(self):
        # Read config file / Config dosyasını oku
        config = self.read_config()
        # If current language is Turkish, change to English and vice versa / Eğer mevcut dil Türkçe ise İngilizce yap, aksi halde Türkçe yap
        if self.language == 'turkish':
            config['Settings']['language'] = 'English'
        else:
            config['Settings']['language'] = 'Turkish'
        # Save changes to config file / Yapılan değişiklikleri config dosyasına kaydet
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        # Restart application / Uygulamayı yeniden başlat
        self.root.destroy()
        root = tk.Tk()
        app = WeatherApp(root)
        root.mainloop()

    # Select background color / Arka plan rengini seç
    def select_color(self):
        # Open color chooser dialog and get selected color / Renk seçici pencereyi aç ve seçilen rengi al
        color = askcolor()[1]
        if color:
            # Read config file / Config dosyasını oku
            config = self.read_config()
            # Save selected color to config file / Seçilen rengi config dosyasına kaydet
            config['Settings']['background_color'] = color
            # Save changes to config file / Yapılan değişiklikleri config dosyasına kaydet
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            # Set window background color to selected color / Pencere arka plan rengini seçilen renge ayarla
            self.root.configure(bg=color)

if __name__ == "__main__":
    # Create main Tkinter window / Ana Tkinter penceresi oluştur
    root = tk.Tk()
    # Initialize WeatherApp instance / WeatherApp örneğini başlat
    app = WeatherApp(root)
    # Start Tkinter event loop / Tkinter olay döngüsünü başlat
    root.mainloop()
