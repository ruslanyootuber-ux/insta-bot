from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS
from urllib.parse import quote

# FAYL NOMI VA O'ZGARUVCHI NOMI BIR XIL BO'LISHI SHART!
BOT_USERNAME = "NamozTaqvimi_Uz_Bot" 

# 1. ASOSIY MENYU (Lotin va Kirill tillari moslashtirilgan shakli)
def get_main_menu_kb(lang: str = "latin") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if lang == "latin":
        # 🕌 Namoz va ibodatlar bo'limi (Rasmdagi xususiyatlar)
        builder.button(text="💧 Tahorat", callback_data="taxorat_0_latin")
        builder.button(text="🚿 G'usl", callback_data="ghusl_latin")
        builder.button(text="🏜️ Tayammum", callback_data="tayammum_latin")
        builder.button(text="🧎 Erkaklar namozi", callback_data="erkaklar_namozi_latin")
        builder.button(text="🧎‍♀️ Ayollar namozi", callback_data="ayollar_namozi_latin")
        builder.button(text="📖 Suralar", callback_data="suralar_latin")
        builder.button(text="🤲 Duolar", callback_data="duolar_latin")
        
        # ⚙️ Qo'shimcha xizmatlar
        builder.button(text="🕌 Namoz vaqtlari", callback_data="menu_regions")
        builder.button(text="✨ Allohning 99 ismi", callback_data="menu_asmaul")
        builder.button(text="📿 Elektron tasbeh", callback_data="menu_tasbeh")
        builder.button(text="📖 Kunlik hadis", callback_data="menu_hadis")
        builder.button(text="🕋 Qiblani topish", callback_data="menu_qibla")
        builder.button(text="🤲 Kunlik zikrlar", callback_data="menu_zikr_main")
        builder.button(text="🌙 Ramazon taqvimi", callback_data="menu_ramadan")
        builder.button(text="🔔 Eslatma belgilash", callback_data="menu_reminder")
        builder.button(text="☪️ Mazhabni tanlash", callback_data="menu_settings")
        builder.button(text="👨‍💻 Bog'lanish", callback_data="menu_creator")

        add_text = "➕ Guruhga qo'shish"
        share_btn_text = "📲 Do'stlarga ulashish"
        share_text = "🕌 «Namoz Vaqtlari» zikrlar va islomiy ibodatlar uchun shaxsiy yordamchingiz."

    else:  # cyrillic (Kirill alifbosi uchun)
        # 🕌 Намоз ва ибодатлар бўлими
        builder.button(text="💧 Таҳорат", callback_data="taxorat_0_cyrillic")
        builder.button(text="🚿 Ғусл", callback_data="ghusl_cyrillic")
        builder.button(text="🏜️ Таяммум", callback_data="tayammum_cyrillic")
        builder.button(text="🧎 Эркаклар намози", callback_data="erkaklar_namozi_cyrillic")
        builder.button(text="🧎‍♀️ Аёллар намози", callback_data="ayollar_namozi_cyrillic")
        builder.button(text="📖 Суралар", callback_data="suralar_cyrillic")
        builder.button(text="🤲 Дуолар", callback_data="duolar_cyrillic")
        
        # ⚙️ Қўшимча хизматлар
        builder.button(text="🕌 Намоз вақтлари", callback_data="menu_regions")
        builder.button(text="✨ Аллоҳнинг 99 исми", callback_data="menu_asmaul")
        builder.button(text="📿 Электрон тасбеҳ", callback_data="menu_tasbeh")
        builder.button(text="📖 Кунлик ҳадис", callback_data="menu_hadis")
        builder.button(text="🕋 Қиблани топиш", callback_data="menu_qibla")
        builder.button(text="🤲 Кунлик зикрлар", callback_data="menu_zikr_main")
        builder.button(text="🌙 Рамазон тақвими", callback_data="menu_ramadan")
        builder.button(text="🔔 Эслатма белгилаш", callback_data="menu_reminder")
        builder.button(text="☪️ Мазҳабни танлаш", callback_data="menu_settings")
        builder.button(text="👨‍💻 Боғланиш", callback_data="menu_creator")

        add_text = "➕ Гуруҳга қўшиш"
        share_btn_text = "📲 Дўстларга улашиш"
        share_text = "🕌 «Намоз Вақтлари» зикрлар ва исломий ибодатлар учун шахсий ёрдамчингиз."

    # Tugmalarni 2 tadan qilib chiroyli joylashtiramiz
    builder.adjust(2)

    # Pastki qismdagi havolali (URL) tugmalar
    add_to_group_url = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    builder.row(InlineKeyboardButton(text=add_text, url=add_to_group_url))
    
    encoded_text = quote(share_text)
    share_url = f"https://t.me/share/url?url=https://t.me/{BOT_USERNAME}&text={encoded_text}"
    builder.row(InlineKeyboardButton(text=share_btn_text, url=share_url))
    
    return builder.as_markup()


# 2. VILOYATLAR VA TUMANLAR
def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in UZB_REGIONS.keys():
        builder.button(text=f"📍 {region}", callback_data=RegionCallback(region_name=region))
    builder.row(InlineKeyboardButton(text="⬅️ Bosh menyuga qaytish", callback_data="back_to_main"))
    builder.adjust(2) 
    return builder.as_markup()

def get_districts_keyboard(region_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for district in UZB_REGIONS.get(region_name, []):
        builder.button(text=f"🏢 {district}", callback_data=DistrictCallback(district_name=district))
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    builder.adjust(2) 
    return builder.as_markup()