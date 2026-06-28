from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS
from urllib.parse import quote

# Бот юзернеймини шу ерга ёзиб қўямиз, пастдаги тугмалар хато бермаслиги учун
BOT_USERNAME = "NamozTaqvimi_Uz_Bot" 

# 1. АСОСИЙ МЕНЮ (Фақат Кирилл алифбосида)
def get_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # 🕌 Намоз ва ибодатлар бўлими
    builder.button(text="💧 Таҳорат", callback_data="taxorat_0")
    builder.button(text="🚿 Ғусл", callback_data="ghusl")
    builder.button(text="🏜 Таяммум", callback_data="tayammum")
    builder.button(text="🧎 Эркаклар намози", callback_data="erkaklar_namozi")
    builder.button(text="🧎‍♀️ Аёллар намози", callback_data="ayollar_namozi")
    builder.button(text="📖 Суралар", callback_data="suralar")
    builder.button(text="🤲 Дуолар", callback_data="duolar")

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

    builder.adjust(2)

    # Пастки қисмдаги ҳаволали (URL) тугмалар
    add_to_group_url = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    builder.row(InlineKeyboardButton(text="➕ Гуруҳга қўшиш", url=add_to_group_url))

    share_text = "🕌 «Намоз Вақтлари» зикрлар ва исломий ибодатлар учун шахсий ёрдамчингиз."
    encoded_text = quote(share_text)
    share_url = f"https://t.me/share/url?url=https://t.me/{BOT_USERNAME}&text={encoded_text}"
    builder.row(InlineKeyboardButton(text="📲 Дўстларга улашиш", url=share_url))

    return builder.as_markup()

# 2. ВИЛОЯТЛАР ВА ТУМАНЛАР КЛАВИАТУРАЛАРИ
def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in UZB_REGIONS.keys():
        builder.button(text=f"📍 {region}", callback_data=RegionCallback(region_name=region))
    builder.row(InlineKeyboardButton(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main"))
    builder.adjust(2) 
    return builder.as_markup()

def get_districts_keyboard(region_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for district in UZB_REGIONS.get(region_name, []):
        builder.button(text=f"🏢 {district}", callback_data=DistrictCallback(district_name=district))
    builder.button(text="⬅️ Вилоятларга қайтиш", callback_data="back_to_regions")
    builder.adjust(2) 
    return builder.as_markup()
