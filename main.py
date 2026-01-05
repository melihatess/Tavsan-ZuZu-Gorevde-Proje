import pygame
import random
import math
import os # kısa süreli hafıza.
import sys

pygame.init()

def resim_getir(dosya_adi):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
        tam_yol = os.path.join(base_path, "resimler", dosya_adi)
    else:
        kodun_oldugu_klasor = os.path.dirname(os.path.abspath(__file__))
        tam_yol = os.path.join(kodun_oldugu_klasor, "resimler", dosya_adi)

    return tam_yol

# Oyunun boyutu ve adı.
WIDTH, HEIGHT = 1210, 720
PANEL_WIDTH = 310
GAME_WIDTH = WIDTH - PANEL_WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tavşan ZuZu Görevde") 

# Oyun temaları.
LEVEL_THEMES = {
    1: {"name": "İLKBAHAR", "bg1": (255, 250, 225), "bg2": (180, 230, 180)}, 
    2: {"name": "SONBAHAR", "bg1": (255, 248, 220), "bg2": (230, 200, 170)}, 
    3: {"name": "KIŞ",      "bg1": (255, 255, 255), "bg2": (200, 230, 255)}, 
    4: {"name": "YAZ",      "bg1": (255, 255, 240), "bg2": (255, 230, 160)}  
}

# Renkler.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAM = (245, 245, 220)
COLOR_INACTIVE = pygame.Color('grey50')
COLOR_ACTIVE_INPUT = pygame.Color('dodgerblue2')
GREEN = (0, 200, 0)
RED = (200, 0, 0) 
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 215, 0) 
DARK_GREEN = (0, 100, 0)
GRAY = (100, 100, 100)

COLOR_HIGHLIGHT_BORDER = pygame.Color('gold')
COLOR_HIGHLIGHT_FILL = (255, 255, 204)
COLOR_ERROR_BORDER = pygame.Color('firebrick1')
COLOR_ERROR_FILL = (255, 204, 204)
COLOR_ERROR_TEXT = pygame.Color('darkred')

ARKA_RENK_1 = (17, 82, 26)
ARKA_RENK_2 = (8, 171, 31)
KARE_BOYUTU = 45

# Fontlar.
try:
    title_font = pygame.font.SysFont('Arial', 65, bold=True)
    title_font_1 = pygame.font.SysFont('Arial', 50, bold=True)
    info_font = pygame.font.SysFont('Arial', 22, bold=True)
    input_font = pygame.font.Font(None, 32)
    question_font = pygame.font.SysFont('Arial', 24, bold=True)
    level_font = pygame.font.SysFont('Arial', 24, bold=True)
    level_font_1 = pygame.font.SysFont('Arial', 32, bold=True) 
    order_font = pygame.font.SysFont('Arial', 18, bold=True) 
except:
    title_font = pygame.font.Font(None, 60)
    title_font_1 = pygame.font.SysFont(None, 50)
    info_font = pygame.font.Font(None, 22)
    input_font = pygame.font.Font(None, 32)
    question_font = pygame.font.Font(None, 24)
    level_font = pygame.font.Font(None, 24)
    level_font_1 = pygame.font.SysFont(None, 32) 
    order_font = pygame.font.Font(None, 18)

PDF_QUESTIONS = [
    {"q": "(12 x 13) x 14 işlemi ile 12 x (13 x 14) işleminin sonucu eşittir.", "o": ["Doğru", "Yanlış"], "a": 0},
    {"q": "Bir yılda kaç hafta vardır?", "o": ["52", "12", "365"], "a": 0},
    {"q": "Çeyrek saat kaç dakikadır?", "o": ["15", "30", "45"], "a": 0},
    {"q": "Hangi ay 30 gün çekmez?", "o": ["Şubat", "Nisan", "Haziran"], "a": 0},
    {"q": "2 düzine kalem kaç tanedir?", "o": ["24", "12", "20"], "a": 0},
    {"q": "Yarım kilo kaç gramdır?", "o": ["500", "1000", "250"], "a": 0},
    {"q": "Üçgenin iç açıları toplamı kaçtır?", "o": ["180", "360", "90"], "a": 0}
]

game_questions = []

def generate_dynamic_problem():
    templates = [
        {"text": "Bir çiftçinin {x} koyunu vardı. Pazardan {y} koyun daha aldı. Toplam kaç koyunu oldu?", "op": "+", "min": 150, "max": 400},
        {"text": "Okul kütüphanesinde {x} kitap var. Bağış olarak {y} kitap daha geldi. Toplam kitap sayısı kaç oldu?", "op": "+", "min": 1000, "max": 2000},
        {"text": "Bir fırıncı sabah {x} ekmek üretti. Gün içinde {y} tanesini sattı. Geriye kaç ekmeği kaldı?", "op": "-", "min": 200, "max": 500},
        {"text": "{x} soruluk bir deneme sınavında {y} soruyu boş bırakan Ayşe, kalan soruların hepsini işaretlemiştir. Ayşe kaç soru işaretledi?", "op": "-", "min": 50, "max": 100},
        {"text": "Depoda {x} litre su vardı. Kullanım sonucu {y} litresi azaldı. Depoda kaç litre su kaldı?", "op": "-", "min": 100, "max": 250},
        {"text": "Bir trende {y} vagon var. Her vagonda {x} yolcu seyahat ediyor. Trendeki toplam yolcu sayısı kaçtır?", "op": "*", "min": 40, "max": 80},
        {"text": "Tanesi {x} TL olan gömleklerden {y} tane alan mağaza sahibi toptancıya kaç TL öder?", "op": "*", "min": 100, "max": 300},
        {"text": "Bir bahçede {y} sıra elma ağacı var. Her sırada {x} ağaç olduğuna göre toplam kaç elma ağacı vardır?", "op": "*", "min": 15, "max": 40},
        {"text": "Saatte {x} km hızla giden bir araç hiç durmadan {y} saat yol alıyor. Toplam kaç km yol gitmiştir?", "op": "*", "min": 60, "max": 110},
        {"text": "Bir kırtasiyeci içinde {x} kalem bulunan kutulardan {y} tane sattı. Toplam kaç kalem satmıştır?", "op": "*", "min": 12, "max": 24},
        {"text": "Alya yaz tatili boyunca 1275 km, Emir 1249 km yol gitmiştir. Şimdi ikisinin toplam kaç km yol gittiğini bulmak için hangi işlemi yapmalıyız?", "op": "+", "min": 10000, "max": 20000},
        {"text": "Ali'nin {x} misketi var. {y} tane daha kazandı. Toplam kaç misketi oldu?", "op": "+", "min": 15, "max": 50},
        {"text": "Bir kümeste {x} tavuk, {y} horoz var. Toplam hayvan sayısı kaçtır?", "op": "+", "min": 20, "max": 80},
        {"text": "{x} TL değerinde bir paten almak isteyen Tuna, üç ayda {y} TL para biriktiriyor. Bu durumda Tuna’nın istediği pateni alabilmesi için kaç liraya daha ihtiyacı vardır?", "op": "-", "min": 1200, "max": 4000},
        {"text": "Otobüste {x} yolcu vardı. {y} yolcu indi. Kaç yolcu kaldı?", "op": "-", "min": 30, "max": 90},
        {"text": "{x} sayfalık kitabın {y} sayfasını okudum. Geriye kaç sayfa kaldı?", "op": "-", "min": 50, "max": 150},
        {"text": "Doğal Yaşam Park’ında, {y} kg doğan bebek fil her ay eşit miktarda kilo almaktadır. Onuncu ayın sonunda {x} kg olan bebek fil bir ayda kaç kilogram almıştır?", "op": "-", "min": 100, "max": 600},
        {"text": "Dakikada ortalama {x} adım atan bir kişi bu parkuru {y} dakikada tamamlamaktadır. Buna göre yürüyüş parkuru kaç adımdır?", "op": "*", "min": 70, "max": 200},
        {"text": "Tanesi {y} TL olan kalemlerden {x} tane alırsam kaç TL öderim?", "op": "*", "min": 3, "max": 12},
        {"text": "Bir apartmanda {x} kat, her katta {y} daire var. Toplam daire sayısı?", "op": "*", "min": 40, "max": 100},
        {"text": "{x} cevizi {y} kişiye eşit paylaştırırsak kişi başı kaç ceviz düşer?", "op": "/", "min": 20, "max": 80, "special": "divisible"},
        {"text": "{x} litre zeytinyağını {y} litrelik şişelere doldurmak istiyoruz. Kaç şişeye ihtiyacımız var?", "op": "/", "min": 20, "max": 100, "special": "divisible"},
        {"text": "Bir deste gülü {y} vazoya eşit şekilde paylaştırırsak her vazoya {x} gül düşüyor. Toplam gül sayısı {x} ise ve {y} vazoya bölersek?", "op": "/", "min": 20, "max": 60, "special": "divisible"},
        {"text": "{x} sayfalık ödevimi {y} günde eşit sayfa okuyarak bitirdim. Günde kaç sayfa okudum?", "op": "/", "min": 30, "max": 150, "special": "divisible"},
        {"text": "Dedem {x} fındığı {y} torununa eşit olarak paylaştırdı. Her toruna kaç fındık düştü?", "op": "/", "min": 10, "max": 50, "special": "divisible"}, 
        {"text": "Bir tiyatro salonunda {x} erkek, {y} kadın izleyici vardır. Salonda toplam kaç izleyici vardır?", "op": "+", "min": 100, "max": 400},
        {"text": "Cumhuriyet İlkokulu'nda {x} öğrenci, Atatürk İlkokulu'nda {y} öğrenci vardır. İki okulda toplam kaç öğrenci vardır?", "op": "+", "min": 500, "max": 1500},
        {"text": "Bir kamyonette {x} kg karpuz, {y} kg kavun yüklüdür. Kamyonetteki toplam yük kaç kilogramdır?", "op": "+", "min": 1500, "max": 3000},
        {"text": "Ali kumbarasında {x} TL, Ayşe ise {y} TL biriktirdi. İkisinin toplam kaç lirası oldu?", "op": "+", "min": 150, "max": 450},
        {"text": "{x} kilometrelik yolun {y} kilometresini gittik. Geriye gidilecek kaç kilometre yol kaldı?", "op": "-", "min": 200, "max": 800},
        {"text": "Bir manav halden {x} kilogram elma aldı. Gün sonunda {y} kilogramını sattı. Elinde kaç kilogram elma kaldı?", "op": "-", "min": 100, "max": 300},
        {"text": "{x} metre uzunluğundaki bir top kumaşın {y} metresi satıldı. Geriye kaç metre kumaş kaldı?", "op": "-", "min": 50, "max": 120},
        {"text": "Bir stadyumun kapasitesi {x} kişidir. Maça {y} biletli seyirci geldiğine göre kaç koltuk boş kalmıştır?", "op": "-", "min": 5000, "max": 15000},
        {"text": "Bir çiftlikte {x} inek var. Her inek günde {y} litre süt veriyor. Toplam kaç litre süt elde edilir?", "op": "*", "min": 10, "max": 30},
        {"text": "Okul gezisine {x} otobüs gidiyor. Her otobüste {y} öğrenci olduğuna göre geziye kaç öğrenci katılmıştır?", "op": "*", "min": 5, "max": 15},
        {"text": "Dikdörtgen şeklindeki bir bahçenin kısa kenarı {y} m, uzun kenarı {x} metredir. Bahçenin alanı kaç metrekaredir?", "op": "*", "min": 20, "max": 60},
        {"text": "Bir kütüphanede {x} raf var. Her rafta {y} kitap bulunduğuna göre toplam kitap sayısı kaçtır?", "op": "*", "min": 10, "max": 50},
        {"text": "Bir sinema biletinin fiyatı {y} TL'dir. {x} kişilik bir grup sinemaya giderse toplam kaç TL öderler?", "op": "*", "min": 10, "max": 30},
        {"text": "{x} adet yumurtayı {y} 'li paketlere koyarsak kaç paket yumurta elde ederiz?", "op": "/", "min": 30, "max": 150, "special": "divisible"},
        {"text": "{x} kilogram unu {y} kilogramlık poşetlere paylaştırırsak kaç poşet gerekir?", "op": "/", "min": 50, "max": 200, "special": "divisible"},
        {"text": "Bir araç {x} km yolu {y} saatte gitmiştir. Bu aracın saatteki ortalama hızı kaç km'dir?", "op": "/", "min": 200, "max": 600, "special": "divisible"},
        {"text": "{x} TL parayı {y} kardeş eşit olarak paylaşırsa her birine kaç TL düşer?", "op": "/", "min": 100, "max": 500, "special": "divisible"},
        {"text": "Bir sınıftaki {x} öğrenci, {y} kişilik gruplara ayrılırsa kaç grup oluşur?", "op": "/", "min": 20, "max": 60, "special": "divisible"}    
    ]

    temp = random.choice(templates)
    x = random.randint(temp["min"], temp["max"])        
    if temp["op"] == "*" or temp["op"] == "/":
        y = random.randint(2, 9)
    else:
        limit = x // 2
        if limit < 11:
            y = random.randint(1, limit if limit > 1 else 2)
        else:
            y = random.randint(10, limit)

    if temp["op"] == "-":
        if y > x: 
            x, y = y, x
    elif temp["op"] == "/":
        x = x - (x % y)
        if x == 0: 
            x = y * 2

    if temp["op"] == "+": 
        ans = x + y
    elif temp["op"] == "-": 
        ans = x - y
    elif temp["op"] == "*": 
        ans = x * y
    elif temp["op"] == "/": 
        ans = x // y
    
    q_text = temp["text"].format(x=x, y=y)
    options = [str(ans)]
    while len(options) < 3:
        offset = random.randint(-5, 5)
        wrong = ans + offset
        if wrong > 0 and str(wrong) not in options: 
            options.append(str(wrong))
    random.shuffle(options)
    return q_text, options, options.index(str(ans))

def get_question():
    if random.randint(1, 10) > 1: 
        return generate_dynamic_problem()
    
    if not game_questions: 
        global PDF_QUESTIONS
        import copy
        game_questions[:] = copy.deepcopy(PDF_QUESTIONS) 
    q = random.choice(game_questions)
    return q["q"], q["o"], q["a"]

def get_pixel(col, row): 
    return (col * KARE_BOYUTU + KARE_BOYUTU // 2, row * KARE_BOYUTU + KARE_BOYUTU // 2)

def get_grid(x, y): 
    return (x // KARE_BOYUTU, y // KARE_BOYUTU)

# Sınıflar
class SpriteObj(pygame.sprite.Sprite):
    def __init__(self, img_path, col, row, scale_plus=5, fallback_color=RED):
        super().__init__()
        try:
            # ESKİSİ: loaded = pygame.image.load(img_path).convert_alpha()
            # YENİSİ: resim_getir fonksiyonunu kullanıyoruz
            full_path = resim_getir(img_path) 
            loaded = pygame.image.load(full_path).convert_alpha()
            self.image = pygame.transform.smoothscale(loaded, (KARE_BOYUTU + scale_plus, KARE_BOYUTU + scale_plus))
            
        except Exception as e:
            print(f"Resim hatası ({img_path}): {e}") # Hata olursa görelim
            self.image = pygame.Surface((KARE_BOYUTU, KARE_BOYUTU))
            self.image.fill(fallback_color)
        self.rect = self.image.get_rect(center=get_pixel(col, row))        
        #self.rect.inflate_ip(-20, -20)
        #self.radius = 15

class Player(SpriteObj):
    def __init__(self, col, row): 
        selected_img = characters[current_char_index]["img"]
        super().__init__(selected_img, col, row)
        self.speed = 5

class Enemy(SpriteObj):
    def __init__(self, img_path, col, row, direction): # img_path diyerek iki tane canavar elde ettim. önemli kısım burası.
        super().__init__(img_path, col, row) 
        self.speed = 2 
        self.direction = direction 
        
        self.dir_x = random.choice([1, -1]) if direction == "yatay" else 0
        self.dir_y = random.choice([1, -1]) if direction == "dikey" else 0

    def update(self):
        if game_state == 'EXECUTING':
            self.rect.x += self.dir_x * self.speed
            self.rect.y += self.dir_y * self.speed
            
            if self.rect.left < 0 or self.rect.right > GAME_WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.reverse()
                return
    
    def reverse(self):
        self.dir_x *= -1
        self.dir_y *= -1

class Target(SpriteObj):
    def __init__(self, img, col, row, q, o, a):
        super().__init__(img, col, row, 0)
        self.question = q
        self.options = o
        self.correct_index = a

class Flower(SpriteObj):
    def __init__(self, col, row):
        super().__init__("cactus.png", col, row, 0, (0, 0, 0))

class Mud(SpriteObj):
    def __init__(self, col, row):
        super().__init__("mud.png", col, row, 0, (0, 0, 0)) 

class Ice(SpriteObj):
    def __init__(self, col, row):
        super().__init__("ice.png", col, row, 0, (0, 0, 0))

class Fence(SpriteObj):
    def __init__(self, col, row):
        super().__init__("fence.png", col, row, 0, (255, 0, 0))

class EnergyItem(SpriteObj):
    def __init__(self, col, row): 
        super().__init__("energy.png", col, row, -5, YELLOW)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((random.randint(5, 10), random.randint(5, 10)))
        self.image.fill(random.choice([RED, GREEN, BLUE, ORANGE, YELLOW, (0, 255, 255), (255, 0, 255)]))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = random.randint(-5, 5)
        self.vel_y = random.randint(-10, -2)
        self.gravity = 0.7

    def update(self):
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.y > HEIGHT:
            self.kill()

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color):
        super().__init__()
        self.image = info_font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 100 
        self.vel_y = -2

    def update(self):
        self.rect.y += self.vel_y
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

# karakterler
characters = [
    {"name": "Tavşan ZuZu",  "img": "rabbit.png",       "price": 0,   "owned": True},
    {"name": "Tarzan Maymun",   "img": "maymun.png",  "price": 1000, "owned": False},
    {"name": "Hızlı Aslan", "img": "lion.png", "price": 2500, "owned": False},
    {"name": "Deli Kurt", "img": "wolf.png", "price": 4500, "owned": False}
]
current_char_index = 0 

# nasıl oynanır bölümünün metinleri.
help_pages = [
    {"text": "Tavşanı YÖN TUŞLARI ile hareket ettir.", "img": "7.png"},
    {"text": "Enerjileri topla ve devam et!", "img": "11_1.png"}, 
    {"text": "Engelleri aşmak için plan yap.", "img": "5.png"},
    {"text": "Canavarlardan kaç ve sakın yakalanma!", "img": "8.png"},
    {"text": "Meyveleri topla ve matematik sorularını çöz bölümü bitir!", "img": "6.png"}
]
help_page_index = 0 

# GLOBAL DEĞİŞKENLER ***
game_state = 'MENU' 
current_level = 1
max_level = 4
max_unlocked_level = 1 
player_energy = 50 
max_energy = 50
total_score = 0 
popup_error_msg = ""
# Vuruş kutusunu %60'a küçülten özel çarpışma fonksiyonu.
hit_test = pygame.sprite.collide_rect_ratio(0.6) 

# İmleç (Cursor) Değişkenleri ***
cursor_visible = True
cursor_timer = 0

player = None
targets = pygame.sprite.Group()
muds = pygame.sprite.Group() 
ices = pygame.sprite.Group()
flowers = pygame.sprite.Group() 
energy_items = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
particles = pygame.sprite.Group() 
floating_texts = pygame.sprite.Group()

ghost_path = []
is_moving = False
command_queue = []
current_target_info = None
active_box_idx = None
error_msg = ""
active_q_target = None
q_buttons = []
input_order = []
current_map_data = []

input_boxes = []
for i, (lbl, direction) in enumerate([("adım yukarı(↑) git.", "yukarı"), ("adım aşağı(↓) git.", "aşağı"), ("adım sola(←) git.", "sola"), ("adım sağa(→) git.", "sağa")]):
    r = pygame.Rect(GAME_WIDTH + 15, 150 + i * 70, 60, 40)
    input_boxes.append({"rect": r, "label": lbl, "dir": direction, "text": "", "active": False, "error": False})

btn_run = pygame.Rect(GAME_WIDTH + 25, HEIGHT - 210, PANEL_WIDTH - 50, 50)
btn_reset = pygame.Rect(GAME_WIDTH + 25, HEIGHT - 155, PANEL_WIDTH - 50, 50)
btn_main_menu = pygame.Rect(GAME_WIDTH + 25, HEIGHT - 102, PANEL_WIDTH - 50, 54)
btn_start_game = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 60)
btn_howto = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 30, 300, 60)
btn_back = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 200, 50)
btn_next_level = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50) 
btn_quit = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 210, 300, 60)
btn_shop = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 300, 60)
btn_shop_back = pygame.Rect(WIDTH//2 - 100, HEIGHT - 120, 200, 50)
btn_prev = pygame.Rect(0, 0, 50, 50)
btn_next = pygame.Rect(0, 0, 50, 50)

def save_game():
    try:
        with open("save.txt", "w") as f:
            f.write(f"{total_score},{player_energy}")
    except:
        print("Kayıt hatası")

def load_game_data():
    global max_unlocked_level, total_score, player_energy
        
    if os.path.exists("save.txt"):
        try:
            with open("save.txt", "r") as f:
                data = f.read().split(',')
                total_score = int(data[0])
                player_energy = int(data[1])
        except:
            print("Dosya okuma hatası.")

def clear_game():
    targets.empty() 
    energy_items.empty()
    enemies.empty()
    all_sprites.empty() 
    particles.empty() 
    floating_texts.empty()
    muds.empty()
    ices.empty()
    flowers.empty()

    global player, input_order
    player = None 
    input_order = []

def create_random_map(level_difficulty):
    cols = GAME_WIDTH // KARE_BOYUTU
    rows = HEIGHT // KARE_BOYUTU
    
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    occupied = set()

    def get_empty_pos():
        while True:
            c = random.randint(1, cols - 2) 
            r = random.randint(1, rows - 2)
            if (c, r) not in occupied:
                return c, r

    pc, pr = get_empty_pos()
    grid[pr][pc] = 'P'
    occupied.add((pc, pr))
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            occupied.add((pc + i, pr + j))

    fruit_chars = ['C', 'A', 'M', 'B', 'G', 'O', 'L', 'T', 'I', 'X', 'W', 'J', 'H', 'K']
    target_count = 6 + level_difficulty 
    
    for _ in range(target_count):
        c, r = get_empty_pos()
        grid[r][c] = random.choice(fruit_chars)
        occupied.add((c, r))

    energy_count = 3 + level_difficulty
    for _ in range(energy_count):
        try:
            c, r = get_empty_pos()
            grid[r][c] = 'S'
            occupied.add((c, r))
        except:
            pass

    map_data = ["".join(row) for row in grid]

    if level_difficulty == 2:
        mud_count = 12
        for _ in range(mud_count):
            try:
                c, r = get_empty_pos()
                grid[r][c] = 'D' 
                occupied.add((c, r))
            except: 
                pass

    if level_difficulty == 3:
        ice_count = 19
        for _ in range(ice_count):
            try:
                c, r = get_empty_pos()
                grid[r][c] = 'Z'
                occupied.add((c, r))
            except: 
                pass

    if level_difficulty == 4:
        umbrella_count = 19
        for _ in range(umbrella_count):
            try:
                c, r = get_empty_pos()
                grid[r][c] = 'Y'
                occupied.add((c, r))
            except:
                pass

    if level_difficulty == 1:
        flower_hedge = 5 
        for _ in range(flower_hedge):
            try:
                c, r = get_empty_pos()
                grid[r][c] = 'R'
                occupied.add((c, r))
            except:
                pass
                    
    if level_difficulty >= 2:
        enemy_count = 2 
        for _ in range(enemy_count):
            try:
                c, r = get_empty_pos()
                grid[r][c] = 'V' 
                occupied.add((c, r))
            except: 
                pass
    
    if level_difficulty >= 3:
        slime_count = 2 
        for _ in range(slime_count):
            try:
                c, r = get_empty_pos()
                grid[r][c] = 'Q'
                occupied.add((c, r))
            except:
                pass
        
    map_data = ["".join(row) for row in grid]
    return map_data

def load_level(level_num):
    global current_level, player_energy, max_energy, current_map_data, ghost_path, game_questions
    current_level = level_num
    clear_game()
    
    ghost_path = []
    game_questions = []

    max_energy = 100 + (level_num * 10) 
    player_energy = max_energy 
    
    random_map = create_random_map(level_num)
    current_map_data = random_map 
    
    setup_map_level(random_map)

def reset_ui_vars():
    global is_moving, command_queue, active_box_idx, error_msg, game_state, popup_error_msg, ghost_path, input_order
    
    ghost_path = [] 
    
    input_order = [] 
    
    is_moving = False 
    command_queue = []
    active_box_idx = None 
    error_msg = "" 
    popup_error_msg = ""
    game_state = 'PLANNING'
    
    for b in input_boxes: 
        b['text'] = "" 
        b['error'] = False

def setup_map_level(random_map):
    global player
    theme = LEVEL_THEMES[current_level]
    for r, row in enumerate(random_map):
        for c, cell in enumerate(row):
            if cell == 'P':
                player = Player(c, r) 
                all_sprites.add(player)
            elif cell == 'V':
                if current_level >= 2: 
                    move_type = random.choice(["yatay", "dikey"])
                    e = Enemy("monster.png", c, r, move_type)
                    enemies.add(e)
                    all_sprites.add(e)
            elif cell == 'Q':
                if current_level >= 3: 
                    move_type = random.choice(["yatay", "dikey"])
                    e = Enemy("canavar.png", c, r, move_type)
                    enemies.add(e) 
                    all_sprites.add(e)
            elif cell == 'R':
                rr = Flower(c, r)
                all_sprites.add(rr)
            elif cell == 'Y':
                u = Fence(c, r)
                all_sprites.add(u)
            elif cell == 'S': 
                en = EnergyItem(c, r)
                energy_items.add(en) 
                all_sprites.add(en)
            elif cell == 'D':
                m = Mud(c, r)
                muds.add(m)
                all_sprites.add(m)
            elif cell == 'Z':
                i = Ice(c, r)
                ices.add(i)
                all_sprites.add(i)
            elif cell in ['C', 'A', 'M', 'B', 'G', 'O', 'L', 'T', 'I', 'X', 'W', 'J', 'H', 'K']:
                q, o, a = get_question()
                img_path = "carrot.png" 
                if cell == 'A': img_path = "apple.png"
                elif cell == 'G': img_path = "grape.png"
                elif cell == 'M': img_path = "mango.png"
                elif cell == 'B': img_path = "bananas.png"
                elif cell == 'O': img_path = "orange.png"
                elif cell == 'L': img_path = "lemon.png"
                elif cell == 'T': img_path = "tomato.png"
                elif cell == 'I': img_path = "peach.png"
                elif cell == 'X': img_path = "blueberry.png"
                elif cell == 'W': img_path = "pineapple.png"
                elif cell == 'J': img_path = "cherries.png"
                elif cell == 'H': img_path = "eggplant.png"
                elif cell == 'K': img_path = "strawberry.png"
                t = Target(img_path, c, r, q, o, a)
                targets.add(t); all_sprites.add(t)

def is_clear(c1, r1, c2, r2, direction):
    if not current_map_data: return True 
    
    rows = len(current_map_data)
    cols = len(current_map_data[0])

    obstacles = ['Y', 'R'] 

    if direction == "yukarı": 
        for r in range(r1-1, r2-1, -1):
            if r < 0 or current_map_data[r][c1] in obstacles: 
                return False
            
    elif direction == "aşağı":
        for r in range(r1+1, r2+1): 
            if r >= rows or current_map_data[r][c1] in obstacles: 
                return False
            
    elif direction == "sola":
        for c in range(c1-1, c2-1, -1): 
            if c < 0 or current_map_data[r1][c] in obstacles: 
                return False
            
    elif direction == "sağa":
        for c in range(c1+1, c2+1): 
            if c >= cols or current_map_data[r1][c] in obstacles: 
                return False
            
    return True    

def calculate_plan():
    global command_queue, is_moving, current_target_info, active_box_idx, error_msg, game_state, input_order, popup_error_msg, ghost_path
    
    for box in input_boxes:
        box['error'] = False

    command_queue = []
    error_msg = ""
    start_c, start_r = get_grid(*player.rect.center)
    curr_c, curr_r = start_c, start_r
    
    total_steps_needed = 0
    
    for box in input_order:
        if not box['text']: 
            continue
        try: 
            steps = int(box['text'])
        except: 
            box['error']=True 
            error_msg="Sayı giriniz" 
            return
        
        total_steps_needed += steps
        
        d = box['dir']
        
        test_c, test_r = curr_c, curr_r
        if d == "yukarı": test_r -= steps
        elif d == "aşağı": test_r += steps
        elif d == "sola": test_c -= steps
        elif d == "sağa": test_c += steps
        
        # Harita Dışı Kontrolü
        if not (0 <= test_c < GAME_WIDTH//KARE_BOYUTU and 0 <= test_r < HEIGHT//KARE_BOYUTU):
            box['error'] = True; popup_error_msg = "Harita dışına çıkıyorsun!"; game_state = 'WARNING'; return 
        if not is_clear(curr_c, curr_r, test_c, test_r, d):
            box['error'] = True; popup_error_msg = "Engel var dikkat et!"; game_state = 'WARNING'; return

        # Şimdi adımları 1'er 1'er kuyruğa ekle
        orig_idx = input_boxes.index(box)
        
        for _ in range(steps):
            if d == "yukarı": curr_r -= 1
            elif d == "aşağı": curr_r += 1
            elif d == "sola": curr_c -= 1
            elif d == "sağa": curr_c += 1
            
            pixel = get_pixel(curr_c, curr_r)
            command_queue.append({
                "target": pixel, 
                "box_idx": orig_idx, 
                "steps": 1, 
                "direction": d
            })
            
    if total_steps_needed > player_energy + 15: 
        error_msg = f"Çok Uzun! (Enerji: {player_energy})"
        
    if command_queue:
        current_target_info = command_queue.pop(0)
        active_box_idx = current_target_info["box_idx"]
        game_state = 'EXECUTING'
        is_moving = True
        input_order = []
        for b in input_boxes: 
            b['text']=""
            b['active'] = False   

def spawn_confetti():
    for _ in range(400):
        x = random.randint(0, WIDTH)
        y = random.randint(-HEIGHT, 0)
        p = Particle(x, y)
        p.vel_y = random.randint(5, 15)  
        p.vel_x = random.randint(-3, 3) 
        particles.add(p)
        
def spawn_floating_text(text, color, pos=None):
    if pos is None: pos = player.rect.center
    ft = FloatingText(pos[0], pos[1] - 30, text, color)
    floating_texts.add(ft)

# DRAWING ***
def butonu_ciz(rect, text, renk, yazi_rengi=(255, 255, 255)):
    mouse_pos = pygame.mouse.get_pos()
    
    if rect.collidepoint(mouse_pos):
        cizim_rect = rect.inflate(10, 5) # inflate butonlara animasyon katması için var.
        kenarlik_renk = (255, 255, 255) 
    else:
        cizim_rect = rect
        kenarlik_renk = (0, 0, 0) 

    shadow_rect = cizim_rect.copy()
    shadow_rect.x += 5
    shadow_rect.y += 5
    pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=10)

    pygame.draw.rect(screen, renk, cizim_rect, border_radius=10)

    pygame.draw.rect(screen, kenarlik_renk, cizim_rect, 3, border_radius=10)

    yazi_yuzeyi = info_font.render(text, True, yazi_rengi)
    yazi_kutusu = yazi_yuzeyi.get_rect(center=cizim_rect.center)
    screen.blit(yazi_yuzeyi, yazi_kutusu)
    
def draw_menu():
    bg_img = pygame.image.load(resim_getir("bg.png"))
    bg_img = pygame.transform.smoothscale(bg_img, (WIDTH, HEIGHT)) 
    screen.blit(bg_img, (0, 0))

    offset_y = math.sin(pygame.time.get_ticks() * 0.003) * 10 
    
    title = title_font.render("TAVŞAN ZuZu GÖREVDE", True, BLACK)
    title_border = title_font.render("TAVŞAN ZuZu GÖREVDE", True, WHITE)
    screen.blit(title_border, (WIDTH//2 - title.get_width()//2 - 2, 80 + offset_y - 2))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80 + offset_y))

    sub = level_font_1.render("Kodlama ve Matematik Macerası", True, BLACK)
    screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 160 + offset_y))

    mouse_pos = pygame.mouse.get_pos()
    
    menu_buttons = [
        {"rect": btn_start_game, "text": "OYUNA BAŞLA", "color": GREEN},
        {"rect": btn_howto, "text": "NASIL OYNANIR?", "color": ORANGE},
        {"rect": btn_shop, "text": "MARKET", "color": (128, 0, 128)},
        {"rect": btn_quit, "text": "ÇIKIŞ", "color": RED}
    ]

    btn_start_game.size = (260, 50)
    btn_start_game.center = (WIDTH//2, 320)
    btn_howto.size = (260, 50)
    btn_howto.center = (WIDTH//2, 390)
    btn_shop.size = (260, 50)
    btn_shop.center = (WIDTH//2, 460)
    btn_quit.size = (140, 50)
    btn_quit.center = (WIDTH//2, 600)

    for btn in menu_buttons:
        rect = btn["rect"]
        color = btn["color"]
        text = btn["text"]
        
        if rect.collidepoint(mouse_pos):
            draw_rect = rect.inflate(10, 5) 
            border_color = WHITE
        else:
            draw_rect = rect
            border_color = (0,0,0)

        shadow_rect = draw_rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=15)

        pygame.draw.rect(screen, color, draw_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, draw_rect, 3, border_radius=15)
        
        t = info_font.render(text, True, WHITE)
        screen.blit(t, t.get_rect(center=draw_rect.center))

def draw_howto():
    bg_img = pygame.image.load(resim_getir("bg_1.png"))
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    screen.blit(bg_img, (0, 0))

    box_w, box_h = 600, 430 
    box_x, box_y = (WIDTH - box_w)//2, (HEIGHT - box_h)//2
    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
    
    pygame.draw.rect(screen, WHITE, box_rect, border_radius=20) 
    pygame.draw.rect(screen, (80, 40, 0), box_rect, 5, border_radius=20) 
    
    title = title_font_1.render(f"YARDIM {help_page_index + 1}", True, (0, 0, 0))
    screen.blit(title, title.get_rect(center=(WIDTH//2, box_y + 40)))

    current_page = help_pages[help_page_index]
    
    try:
        tam_yol = resim_getir(current_page["img"])
        img = pygame.image.load(tam_yol).convert_alpha()
        img = pygame.transform.smoothscale(img, (350, 220))        
        img_rect = img.get_rect(center=(WIDTH//2, box_y + 180))
        screen.blit(img, img_rect)
        
        pygame.draw.rect(screen, (80, 40, 0), img_rect, 3, border_radius=5)
        
    except Exception as e:
        pygame.draw.rect(screen, RED, (WIDTH//2 - 100, box_y + 100, 200, 150))
        err_text = info_font.render("Resim Yok!", True, WHITE)
        screen.blit(err_text, (WIDTH//2 - 40, box_y + 160))
        print(f"Hata: {e}")

    msg = info_font.render(current_page["text"], True, BLACK)
    screen.blit(msg, msg.get_rect(center=(WIDTH//2, box_y + 330)))

    global btn_prev, btn_next, btn_back
    
    mouse_pos = pygame.mouse.get_pos()

    btn_prev = pygame.Rect(box_x + 30, box_y + box_h - 70, 60, 50)
    
    if help_page_index > 0:
        color_prev = ORANGE
        if btn_prev.collidepoint(mouse_pos):
            draw_rect_prev = btn_prev.inflate(10, 5) 
            border_prev = (255, 255, 255)            
        else:
            draw_rect_prev = btn_prev                
            border_prev = (0, 0, 0)                  
    else:
        color_prev = GRAY
        draw_rect_prev = btn_prev
        border_prev = (50, 50, 50)

    pygame.draw.rect(screen, (50, 50, 50), draw_rect_prev.move(4, 4), border_radius=10)
    pygame.draw.rect(screen, color_prev, draw_rect_prev, border_radius=10)
    pygame.draw.rect(screen, border_prev, draw_rect_prev, 3, border_radius=10)
    
    pygame.draw.polygon(screen, WHITE, [
        (draw_rect_prev.right - 20, draw_rect_prev.top + 15), 
        (draw_rect_prev.left + 15,  draw_rect_prev.centery), 
        (draw_rect_prev.right - 20, draw_rect_prev.bottom - 15)
    ])


    btn_next = pygame.Rect(box_x + box_w - 90, box_y + box_h - 70, 60, 50)
    if help_page_index < len(help_pages) - 1:
        color_next = ORANGE
        if btn_next.collidepoint(mouse_pos):
            draw_rect_next = btn_next.inflate(10, 5) 
            border_next = (255, 255, 255)            
        else:
            draw_rect_next = btn_next               
            border_next = (0, 0, 0)                  
    else:
        color_next = GRAY
        draw_rect_next = btn_next
        border_next = (50, 50, 50)

    pygame.draw.rect(screen, (50, 50, 50), draw_rect_next.move(4, 4), border_radius=10) 
    pygame.draw.rect(screen, color_next, draw_rect_next, border_radius=10)
    pygame.draw.rect(screen, border_next, draw_rect_next, 3, border_radius=10)

    pygame.draw.polygon(screen, WHITE, [
        (draw_rect_next.left + 20,  draw_rect_next.top + 15), 
        (draw_rect_next.right - 15, draw_rect_next.centery), 
        (draw_rect_next.left + 20,  draw_rect_next.bottom - 15)
    ])

    butonu_ciz(btn_shop_back, "MENÜYE DÖN", RED)

def draw_shop():
    bg_img = pygame.image.load(resim_getir("bg_1.png"))
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    screen.blit(bg_img, (0, 0))

    panel_w, panel_h = 1050, 630
    panel_x, panel_y = (WIDTH - panel_w) // 2, (HEIGHT - panel_h) // 2
    
    s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(s, (255, 255, 255, 200), s.get_rect(), border_radius=40) 
    screen.blit(s, (panel_x, panel_y))
    
    pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_w, panel_h), 5, border_radius=40)

    t_shadow = title_font.render("KARAKTER MARKETİ", True, (200, 200, 200))
    t = title_font.render("KARAKTER MARKETİ", True, (153, 0, 76)) 
    screen.blit(t_shadow, t_shadow.get_rect(center=(WIDTH//2 + 3, panel_y + 63)))
    screen.blit(t, t.get_rect(center=(WIDTH//2, panel_y + 60)))
    
    score_box_w, score_box_h = 400, 60
    score_rect = pygame.Rect(WIDTH//2 - score_box_w//2, panel_y + 110, score_box_w, score_box_h)
    
    pygame.draw.rect(screen, (200, 150, 0), score_rect.move(0, 5), border_radius=30)
    pygame.draw.rect(screen, (255, 215, 0), score_rect, border_radius=30)
    pygame.draw.rect(screen, (255, 255, 200), (score_rect.x + 20, score_rect.y + 10, score_box_w - 40, 15), border_radius=10)
    
    score_txt = level_font_1.render(f"TOPLAM PUANIN: {total_score}", True, (51, 0, 25)) 
    screen.blit(score_txt, score_txt.get_rect(center=score_rect.center))

    start_x = WIDTH//2 - 470 
    y_pos = panel_y + 200
    
    global shop_buttons 
    shop_buttons = [] 

    for i, char in enumerate(characters):
        box_x = start_x + (i * 240) 
        box_rect = pygame.Rect(box_x, y_pos, 220, 320)
        
        shadow_rect = box_rect.copy()
        shadow_rect.x += 8
        shadow_rect.y += 8
        pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=20)

        if i == current_char_index:
            bg_color = (220, 255, 220)
            border_color = GREEN
            border_thick = 6
        else:
            bg_color = WHITE
            border_color = (200, 200, 200) 
            border_thick = 3
            
        pygame.draw.rect(screen, bg_color, box_rect, border_radius=20)
        pygame.draw.rect(screen, border_color, box_rect, border_thick, border_radius=20)

        try:
            tam_yol = resim_getir(char["img"]) 
            img = pygame.image.load(tam_yol).convert_alpha()
            img = pygame.transform.smoothscale(img, (110, 110))            
            circle_color = (240, 240, 255)
            pygame.draw.circle(screen, circle_color, (box_x + 110, y_pos + 80), 65)
            
            screen.blit(img, (box_x + 55, y_pos + 25))
        except:
            pygame.draw.rect(screen, RED, (box_x + 60, y_pos + 30, 100, 100))

        name_color = BLACK if i != current_char_index else DARK_GREEN
        name_txt = info_font.render(char["name"], True, name_color)
        screen.blit(name_txt, name_txt.get_rect(center=(box_rect.centerx, y_pos + 160)))
        
        if char["owned"]:
            price_text = "SAHİPSİN"
            p_color = GREEN
        else:
            price_text = f"{char['price']} Puan"
            p_color = ORANGE
            
        p_txt = level_font.render(price_text, True, p_color)
        screen.blit(p_txt, p_txt.get_rect(center=(box_rect.centerx, y_pos + 190)))

        btn_rect = pygame.Rect(box_x + 20, y_pos + 240, 180, 50)
        shop_buttons.append({"rect": btn_rect, "index": i})

        btn_color = GRAY
        btn_label = ""
        btn_text_color = WHITE
        
        if i == current_char_index:
            btn_color = GREEN
            btn_label = "SEÇİLDİ"
        elif char["owned"]:
            btn_color = (0, 191, 255) 
            btn_label = "SEÇ"
        else:
            if total_score >= char["price"]:
                btn_color = (255, 140, 0)
                btn_label = "SATIN AL"
            else:
                btn_color = (220, 20, 60)
                btn_label = "YETERSİZ"

        butonu_ciz(btn_rect, btn_label, btn_color, btn_text_color)

    butonu_ciz(btn_shop_back, "MENÜYE DÖN", RED)

def draw_level_select():
    bg_img = pygame.image.load(resim_getir("bg_1.png"))
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    screen.blit(bg_img, (0, 0))

    panel_w, panel_h = 650, 350 
    panel_x = (WIDTH - panel_w) // 2
    panel_y = 150 

    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

    s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(s, (0, 0, 0, 80), s.get_rect(), border_radius=30)
    screen.blit(s, (panel_x + 10, panel_y + 10))

    pygame.draw.rect(screen, WHITE, panel_rect, border_radius=30)
    pygame.draw.rect(screen, (51, 25, 0), panel_rect, 6, border_radius=30)

    title_w, title_h = 450, 90 
    title_rect = pygame.Rect(WIDTH//2 - title_w//2, panel_y + 40, title_w, title_h)
    
    pygame.draw.rect(screen, (200, 150, 0), title_rect.move(0, 5), border_radius=30)
    pygame.draw.rect(screen, (255, 215, 0), title_rect, border_radius=30)
    pygame.draw.rect(screen, (255, 255, 200), (title_rect.x + 30, title_rect.y + 15, title_w - 60, 15), border_radius=10)
    
    t_shadow = title_font.render("BÖLÜM SEÇ", True, (255, 255, 220)) 
    screen.blit(t_shadow, t_shadow.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2)))

    t = title_font.render("BÖLÜM SEÇ", True, (102, 0, 102)) 
    screen.blit(t, t.get_rect(center=title_rect.center))

    cols = 4 
    
    start_x = WIDTH//2 - 240 
    start_y = panel_y + 170
    
    global level_buttons 
    level_buttons = []

    mouse_pos = pygame.mouse.get_pos()

    for i in range(1, 5): 
        row = (i-1) // cols
        col = (i-1) % cols
        
        x = start_x + (col * 130)
        y = start_y + (row * 130)
        
        btn_rect = pygame.Rect(x, y, 90, 90) 
        
        is_unlocked = (i <= max_unlocked_level)
        if i > max_level: is_unlocked = False

        # --- ANİMASYON MANTIĞI ---
        if btn_rect.collidepoint(mouse_pos):
            draw_rect = btn_rect.inflate(15, 15) 
            border_color = WHITE 
            shadow_offset = 8 
        else:
            draw_rect = btn_rect
            border_color = ORANGE
            shadow_offset = 5

        # Gölge
        shadow_rect = draw_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, (50, 50, 50), shadow_rect, border_radius=20)

        # Kutu Çizimi
        if is_unlocked:
            fill_color = CREAM if i != current_level else (180, 255, 180)
            
            pygame.draw.rect(screen, fill_color, draw_rect, border_radius=20)
            pygame.draw.rect(screen, border_color, draw_rect, 5, border_radius=20)
            
            num_color = (139, 69, 19) 
            num = title_font.render(str(i), True, num_color)
            screen.blit(num, num.get_rect(center=draw_rect.center))
            
            level_buttons.append({"rect": btn_rect, "level": i})
        
        else:
            pygame.draw.rect(screen, GRAY, draw_rect, border_radius=20)
            pygame.draw.rect(screen, (80, 80, 80), draw_rect, 5, border_radius=20)
            
            lock = title_font.render("?", True, (50, 50, 50))
            screen.blit(lock, lock.get_rect(center=draw_rect.center))

    butonu_ciz(btn_shop_back, "MENÜYE DÖN", RED)

def draw_game_ui():
    pygame.draw.rect(screen, CREAM, (GAME_WIDTH, 0, PANEL_WIDTH, HEIGHT))
    pygame.draw.line(screen, BLACK, (GAME_WIDTH, 0), (GAME_WIDTH, HEIGHT), 3)

    l_txt = level_font.render(f"Seviye: {current_level}", True, BLACK)
    screen.blit(l_txt, (GAME_WIDTH + 20, 20))
    s_txt = order_font.render(f"Toplam Puan: {total_score}", True, DARK_GREEN)
    screen.blit(s_txt, (GAME_WIDTH + 20, 50))
    
    bar_width = 200 
    bar_height = 25
    bar_rect = pygame.Rect(GAME_WIDTH + 20, 80, bar_width, bar_height)
    pygame.draw.rect(screen, (200, 200, 200), bar_rect, border_radius=5)
    fill_width = int((player_energy / max_energy) * bar_width)
    if fill_width < 0: 
        fill_width = 0
    color = GREEN if player_energy > 15 else RED
    if fill_width > 0:
        fill_rect = pygame.Rect(GAME_WIDTH + 20, 80, fill_width, bar_height)
        pygame.draw.rect(screen, color, fill_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, bar_rect, 3, border_radius=5)
    e_txt = order_font.render(f"Enerji: {player_energy}/{max_energy}", True, BLACK)
    screen.blit(e_txt, (GAME_WIDTH + 20, 105))

    for i, box in enumerate(input_boxes):
        border = COLOR_ERROR_BORDER if box['error'] else (COLOR_HIGHLIGHT_BORDER if i == active_box_idx else COLOR_INACTIVE)
        if box['active']: border = COLOR_ACTIVE_INPUT
        pygame.draw.rect(screen, WHITE, box['rect'], border_radius=5)
        pygame.draw.rect(screen, border, box['rect'], 2, border_radius=5)
        txt = input_font.render(box['text'], True, BLACK)
        screen.blit(txt, (box['rect'].x+10, box['rect'].y+10))
        lbl = info_font.render(box['label'], True, BLACK)
        screen.blit(lbl, (box['rect'].right+10, box['rect'].y+10))

        # İMLEÇ (CURSOR) ÇİZİMİ ***
        if box['active'] and cursor_visible:
            txt_w = input_font.size(box['text'])[0]
            # İmleci metnin sonuna çiz.
            pygame.draw.line(screen, BLACK, 
                             (box['rect'].x + 10 + txt_w, box['rect'].y + 10), 
                             (box['rect'].x + 10 + txt_w, box['rect'].y + 30), 2)

        if box in input_order:
            idx_txt = order_font.render(str(input_order.index(box)+1), True, RED)
            screen.blit(idx_txt, (box['rect'].x-11, box['rect'].y+10))

    if error_msg:
        err = info_font.render(error_msg, True, COLOR_ERROR_TEXT)
        screen.blit(err, (GAME_WIDTH+20, HEIGHT-220))

    butonu_ciz(btn_run, "ÇALIŞTIR", GREEN, BLACK) 
    butonu_ciz(btn_reset, "SIFIRLA", RED, WHITE)
    butonu_ciz(btn_main_menu, "ANA MENÜ", (100, 100, 255), WHITE)

def draw_popup():
    overlay = pygame.Surface((WIDTH,HEIGHT))
    overlay.set_alpha(180) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    box = pygame.Rect(0,0,760,360) 
    box.center=(WIDTH//2, HEIGHT//2)
    pygame.draw.rect(screen, CREAM, box, border_radius=20)
    pygame.draw.rect(screen, BLACK, box, 3, border_radius=20)
    
    if game_state == 'WARNING':
        t = title_font.render("HATA!", True, RED)
        screen.blit(t, t.get_rect(center=(WIDTH//2, box.top + 60)))
        msg = info_font.render(popup_error_msg, True, BLACK)
        screen.blit(msg, msg.get_rect(center=(WIDTH//2, box.centery)))
        sub = order_font.render("(Kapatmak için tıklayın)", True, COLOR_INACTIVE)
        screen.blit(sub, sub.get_rect(center=(WIDTH//2, box.bottom - 40)))
        return

    if game_state == 'GAME_OVER':
        # 1. Öncelik: Eğer özel bir hata mesajı (Canavar gibi) ayarlanmışsa onu göster.
        if popup_error_msg != "":
             msg = popup_error_msg
             color = RED 
        # 2. Öncelik: Eğer meyveler bittiyse (Kazanma).
        elif not targets:
             msg = "OYUN BİTTİ! TEBRİKLER!!" 
             color = GREEN
        # 3. Öncelik: Hiçbiri değilse Enerji bitmiştir.
        else:
             msg = "ENERJİN BİTTİ!"
             color = RED
        # Başlığı Çiz.
        font_to_use = title_font if len(msg) < 15 else title_font_1 
        t = font_to_use.render(msg, True, color)
        screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        # Puan Bilgisi.
        info3 = info_font.render(f"Toplam Puan: {total_score}", True, BLUE)
        screen.blit(info3, info3.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
        # Menüye Dön Yazısı.
        sub = info_font.render("Menüye dönmek için tıkla", True, BLACK)
        screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 100)))
        return
    
    if game_state == 'LEVEL_COMPLETE':
        t = title_font.render("BÖLÜM TAMAMLANDI!", True, GREEN)
        screen.blit(t, t.get_rect(center=(WIDTH//2, box.top + 80)))
        info1 = info_font.render(f"Kalan Enerji: {player_energy}", True, BLACK)
        info2 = info_font.render(f"Bu Bölümden Kazanılan Puan: {player_energy * 10}", True, BLACK) 
        info3 = info_font.render(f"Toplam Puan: {total_score}", True, BLUE)
        screen.blit(info1, info1.get_rect(center=(WIDTH//2, box.top + 150)))
        screen.blit(info2, info2.get_rect(center=(WIDTH//2, box.top + 190)))
        screen.blit(info3, info3.get_rect(center=(WIDTH//2, box.top + 230)))
        pygame.draw.rect(screen, ORANGE, btn_next_level, border_radius=15)
        nt = info_font.render("SONRAKİ BÖLÜM", True, WHITE)
        screen.blit(nt, nt.get_rect(center=btn_next_level.center))
        return

    q_words = active_q_target.question.split(' ')
    lines = [] 
    curr = ""
    for w in q_words:
        if question_font.size(curr + w)[0] < 750: 
            curr += w + " "
        else: 
            lines.append(curr) 
            curr = w + " "
    lines.append(curr)
    y = box.top + 50
    for l in lines:
        s = question_font.render(l, True, BLACK)
        screen.blit(s, s.get_rect(centerx=WIDTH//2, y=y))
        y += 40
        
    global q_buttons; q_buttons = []
    sx = box.centerx - (len(active_q_target.options)*160)//2
    for i, opt in enumerate(active_q_target.options):
        r = pygame.Rect(sx + i*160 + 20, box.bottom - 100, 120, 60)
        q_buttons.append(r)
        pygame.draw.rect(screen, ORANGE, r, border_radius=10)
        t = info_font.render(opt, True, WHITE)
        screen.blit(t, t.get_rect(center=r.center))
    
    if popup_error_msg:
        err_s = info_font.render(popup_error_msg, True, RED)
        screen.blit(err_s, err_s.get_rect(center=(WIDTH//2, box.bottom - 140)))

clock = pygame.time.Clock()
running = True

while running:
    cursor_timer += clock.get_time()
    if cursor_timer >= 500:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT: 
            running = False
        
        if game_state == 'MENU':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_start_game.collidepoint(e.pos): 
                    game_state = 'LEVEL_SELECT'
                elif btn_howto.collidepoint(e.pos): 
                    game_state = 'HOWTO'
                elif btn_shop.collidepoint(e.pos):
                    game_state = 'SHOP'
                elif btn_quit.collidepoint(e.pos):
                    running = False

        elif game_state == 'HOWTO':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_back.collidepoint(e.pos): 
                    game_state = 'MENU'
                    help_page_index = 0 
                
                elif btn_prev.collidepoint(e.pos):
                    if help_page_index > 0:
                        help_page_index -= 1
                
                elif btn_next.collidepoint(e.pos):
                    if help_page_index < len(help_pages) - 1:
                        help_page_index += 1
        
        elif game_state == 'SHOP':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_shop_back.collidepoint(e.pos):
                    game_state = 'MENU'
                
                else:
                    for btn in shop_buttons:
                        if btn["rect"].collidepoint(e.pos):
                            idx = btn["index"]
                            char = characters[idx]
                            
                            if char["owned"]:
                                current_char_index = idx
                            
                            elif total_score >= char["price"]:
                                total_score -= char["price"] 
                                char["owned"] = True       
                                current_char_index = idx

        elif game_state == 'LEVEL_SELECT':
            if e.type == pygame.MOUSEBUTTONDOWN and  e.button == 1:
                if btn_shop_back.collidepoint(e.pos): 
                    game_state = 'MENU'
                else:
                    for btn in level_buttons:
                        if btn["rect"].collidepoint(e.pos):
                            selected_lvl = btn["level"]
                            load_level(selected_lvl) 
                            game_state = 'PLANNING'                          

        elif game_state == 'WARNING':
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN:
                game_state = 'PLANNING'
                reset_ui_vars()
            
        elif game_state == 'LEVEL_COMPLETE':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_next_level.collidepoint(e.pos):
                    if current_level < max_level:
                        if current_level + 1 > max_unlocked_level:
                            max_unlocked_level = current_level + 1
                        save_game() 
                        load_level(current_level + 1)
                        game_state = 'PLANNING'
                    else:
                        game_state = 'GAME_OVER'
                        
        elif game_state == 'PLANNING':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if btn_run.collidepoint(e.pos): 
                    calculate_plan()
                elif btn_reset.collidepoint(e.pos): 
                    load_level(current_level)
                    reset_ui_vars()
                elif btn_main_menu.collidepoint(e.pos):
                    game_state = 'MENU'
                else:
                    for b in input_boxes: 
                        b['active'] = b['rect'].collidepoint(e.pos)
            
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    calculate_plan()
                
                active_box_found = False 
                
                for b in input_boxes:
                    if b['active']:
                        active_box_found = True
                        
                        if e.key == pygame.K_BACKSPACE: 
                            b['text'] = b['text'][:-1]
                            if not b['text'] and b in input_order: 
                                input_order.remove(b)
                        
                        elif e.unicode.isdigit():
                            if len(b['text']) < 2: 
                                b['text'] += e.unicode
                                if b not in input_order: 
                                    input_order.append(b)
                        
                        # TAB Tuşu ile sonraki kutuya geçiş...
                        elif e.key == pygame.K_TAB:
                             current_index = input_boxes.index(b)
                             next_index = (current_index + 1) % len(input_boxes)
                             b['active'] = False
                             input_boxes[next_index]['active'] = True
                             break 

                if active_box_found and error_msg: 
                     error_msg = ""

        elif game_state == 'QUESTION':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, btn in enumerate(q_buttons):
                    if btn.collidepoint(e.pos):
                        if i == active_q_target.correct_index:
                            active_q_target.kill()
                            spawn_confetti()
                            total_score += 50
                            popup_error_msg = ""
                            if not targets:
                                total_score += player_energy * 10
                                game_state = 'LEVEL_COMPLETE'
                            else:
                                if command_queue: 
                                    current_target_info = command_queue.pop(0)
                                    active_box_idx = current_target_info["box_idx"]
                                    game_state = 'EXECUTING'; is_moving = True
                                else: 
                                    game_state = 'PLANNING'; is_moving = False
                        else: 
                            popup_error_msg = "Yanlış Cevap! (-5 Enerji)"
                            player_energy -= 5
                            if player_energy <= 0:
                                player_energy = 0
                                game_state = 'GAME_OVER'
        
        elif game_state == 'GAME_OVER':
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
                if popup_error_msg == "YAKALANDIN!":
                    load_level(current_level) 
                    reset_ui_vars()           
                    game_state = 'PLANNING'  
                    popup_error_msg = ""      
                
                else:
                    game_state = 'MENU'
                    
    if game_state == 'EXECUTING' and is_moving:
        tx, ty = current_target_info['target']
        px, py = player.rect.center
        dx, dy = tx - px, ty - py

        center_point = player.rect.center
        
        on_mud = False
        on_ice = False
        
        for m in muds:
            if m.rect.collidepoint(center_point):
                on_mud = True
                break
        
        for i in ices:
            if i.rect.collidepoint(center_point):
                on_ice = True
                break
        
        if on_mud:
            player.speed = 1      
        elif on_ice and current_level == 3:
            player.speed = 9     
        else:
            player.speed = 5      
        
        if abs(dx) < player.speed and abs(dy) < player.speed:
            player.rect.center = (tx, ty) 
            
            if (tx, ty) not in ghost_path:
                ghost_path.append((tx, ty))

            steps_taken = current_target_info.get("steps", 0)
            if steps_taken > 0:
                player_energy -= steps_taken
                current_target_info["steps"] = 0 
            
            energy_hit = pygame.sprite.spritecollideany(player, energy_items, hit_test)
            if energy_hit:
                player_energy += 20
                if player_energy > max_energy: player_energy = max_energy
                spawn_floating_text("+20 ENERJİ!", (0,0,0))
                energy_hit.kill()

            on_mud = False
            on_ice = False
            
            for m in muds:
                if m.rect.collidepoint((tx, ty)):
                    on_mud = True
                    break
            
            if not on_mud: 
                for i in ices:
                    if i.rect.collidepoint((tx, ty)):
                        on_ice = True
                        break

            if on_mud:
                spawn_floating_text("SAPLANDIN!", (0, 0, 0))
                command_queue = [] 
                active_box_idx = None
            
            elif on_ice and current_level == 3: 
                cur_dir = current_target_info.get("direction", "")
                if cur_dir:
                    next_c, next_r = get_grid(tx, ty)
                    if cur_dir == "yukarı": next_r -= 1
                    elif cur_dir == "aşağı": next_r += 1
                    elif cur_dir == "sola": next_c -= 1
                    elif cur_dir == "sağa": next_c += 1
                    
                    if 0 <= next_c < GAME_WIDTH//KARE_BOYUTU and 0 <= next_r < HEIGHT//KARE_BOYUTU:
                         if is_clear(get_grid(tx,ty)[0], get_grid(tx,ty)[1], next_c, next_r, cur_dir):
                            new_pixel = get_pixel(next_c, next_r)
                            spawn_floating_text("KAYIYOR!", (0, 0, 0))
                            command_queue.insert(0, {"target": new_pixel, "box_idx": active_box_idx, "steps": 0, "direction": cur_dir})

            if player_energy <= 0: 
                game_state = 'GAME_OVER'
                active_box_idx = None
            else:
                hit = pygame.sprite.spritecollideany(player, targets, hit_test)
                if hit: 
                    active_q_target = hit 
                    game_state = 'QUESTION'
                    popup_error_msg = ""
                    active_box_idx = None
                elif command_queue:
                    current_target_info = command_queue.pop(0)
                    active_box_idx = current_target_info["box_idx"]
                else:
                    game_state = 'PLANNING'; is_moving = False; active_box_idx = None        
        else:
            player.rect.x += player.speed if dx > 0 else (-player.speed if dx < 0 else 0)
            player.rect.y += player.speed if dy > 0 else (-player.speed if dy < 0 else 0)

    if game_state == 'EXECUTING':
        enemies.update()
        if pygame.sprite.spritecollideany(player, enemies, hit_test):
            popup_error_msg = "YAKALANDIN!"
            game_state = 'GAME_OVER'
            active_box_idx = None 

    particles.update()
    floating_texts.update()

    screen.fill(BLACK)
    if game_state == 'MENU': 
        draw_menu()
    elif game_state == 'HOWTO': 
        draw_howto()
    elif game_state == 'SHOP':
        draw_shop()
    elif game_state == 'LEVEL_SELECT':
        draw_level_select()
    else:
        for y in range(0, HEIGHT, KARE_BOYUTU):
            for x in range(0, GAME_WIDTH, KARE_BOYUTU):
                theme = LEVEL_THEMES[current_level]
                color = theme["bg1"] if ((x//KARE_BOYUTU)+(y//KARE_BOYUTU))%2==0 else theme["bg2"]                
                pygame.draw.rect(screen, color, (x, y, KARE_BOYUTU, KARE_BOYUTU))
        # HAYALET İZ ÇİZİMİ ***
        for pos in ghost_path:
            s = pygame.Surface((KARE_BOYUTU, KARE_BOYUTU), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, 150), (KARE_BOYUTU//2, KARE_BOYUTU//2), 12)
            rect = s.get_rect(center=pos)
            screen.blit(s, rect)
        #all_sprites.draw(screen)
        muds.draw(screen)
        ices.draw(screen)
        flowers.draw(screen)
        energy_items.draw(screen)
        for sprite in all_sprites:
            if isinstance(sprite, Fence):
                screen.blit(sprite.image, sprite.rect)
        for sprite in all_sprites:
            if isinstance(sprite, Flower):
                screen.blit(sprite.image, sprite.rect)
        targets.draw(screen)
        enemies.draw(screen)
        if player:
            screen.blit(player.image, player.rect)
        particles.draw(screen)
        floating_texts.draw(screen)
        draw_game_ui()
        if game_state in ['QUESTION', 'GAME_OVER', 'LEVEL_COMPLETE', 'WARNING']: 
            draw_popup()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()