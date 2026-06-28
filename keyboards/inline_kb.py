# 1. ASOSIY MENYU (Faqat Kirill alifbosida)
def get_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # 🕌 Намоз ва ибодатлар бўлими
    builder.button(text="💧 Таҳорат", callback_data="taxorat_0")  # _cyrillic qismi olib tashlandi
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
