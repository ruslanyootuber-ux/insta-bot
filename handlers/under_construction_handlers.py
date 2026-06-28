# handlers/under_construction_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data.in_({"ghusl", "tayammum", "duolar"}))
async def process_under_construction(callback: CallbackQuery):
    """Ғусл, Таяммум ва Дуолар тугмалари босилганда чиқадиган расмий огоҳлантириш матни"""

    text = (
        "✨ <b>Ҳурматли фойдаланувчи!</b> ✨\n\n"
        "⚠️ Ушбу бўлим ҳозирда <b>техник ишлар</b> ва маълумотларни янгилаш жараёнида. "
        "Тез орада сизга тўлиқ ва сифатли ҳолатда тақдим этилади.\n\n"
        "⏳ Навбатдаги янгиланишгача ботимизнинг бошқа фойдали бўлимларидан "
        "фойдаланиб туришингизни тавсия этамиз.\n\n"
        "✍️ Ҳар қандай савол, таклиф ёки мулоҳазаларингиз бўлса, бизга мурожаат қилишингиз мумкин:\n"
        "➡️ <b>Администратор:</b> @mrxruslann\n\n"
        "<i>Тушунганингиз учун ташаккур!</i> 🙏"
    )

    # Орқага (Бош менюга) қайтиш тугмаси
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")

    # Матнни хабар сифатида юборамиз (тугма билан бирга)
    await callback.message.delete()  # Эски меню хабарини ўчиради
    await callback.message.answer(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()