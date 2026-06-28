# handlers/suralar_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.suralar_data import SURALAR_LIST
from keyboards.suralar_kb import get_suralar_list_kb, get_sura_back_kb

router = Router()

@router.callback_query(F.data == "suralar")
async def show_suralar_menu(callback: CallbackQuery):
    """Суралар рўйхатини кўрсатиш"""
    kb = get_suralar_list_kb(SURALAR_LIST)
    await callback.message.delete()
    await callback.message.answer(
        text="<b>📖 Қуръони Карим суралари</b>\n\nТинглайдиган ва ўқийдиган сурангизни танланг:", 
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("sura_view_"))
async def view_single_sura(callback: CallbackQuery):
    """Танланган сурани аудио ва матни билан чиқариш"""
    sura_id = int(callback.data.split("_")[2])
    
    # ИД бўйича сурани базадан топамиз
    sura_data = next((s for s in SURALAR_LIST if s["id"] == sura_id), None)
    
    if not sura_data:
        await callback.answer("Сура топилмади", show_alert=True)
        return

    text = sura_data["text"]
    audio_id = sura_data["audio_id"]
    kb = get_sura_back_kb()

    await callback.message.delete()
    
    # Агар аудио_ид созланмаган бўлса ёки бош бўлса, фақат матн юборилади
    if audio_id == "SURA_AUDIO_0" or not audio_id:
        await callback.message.answer(
            text=f"{text}\n\n<i>(Бу сура учун аудио файл ҳали юкланмаган)</i>",
            reply_markup=kb,
            parse_mode="HTML"
        )
    else:
        try:
            # Аудиони тагида матни (caption) билан бирга юборамиз
            await callback.message.answer_audio(
                audio=audio_id,
                caption=text,
                reply_markup=kb,
                parse_mode="HTML"
            )
        except Exception as e:
            # Бирор хатолик бўлса, фойдаланувчига фақат матн боради
            await callback.message.answer(
                text=f"{text}\n\n<i>(Аудио юклашда хатолик юз берди)</i>",
                reply_markup=kb,
                parse_mode="HTML"
            )
            
    await callback.answer()
