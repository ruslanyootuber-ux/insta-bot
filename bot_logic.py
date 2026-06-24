import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Bot va FSM (Holatlar uchun)
bot = Bot(token="SIZNING_BOT_TOKENINGIZ")
dp = Dispatcher()

class AuthStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()

# Vaqtinchalik xotira
temp_clients = {}

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("Sessiya yaratish uchun telefon raqamingizni yuboring (masalan: +998901234567)")
    await state.set_state(AuthStates.waiting_for_phone)

@dp.message(AuthStates.waiting_for_phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    client = TelegramClient(StringSession(), int("API_ID"), "API_HASH")
    await client.connect()
    
    # Kod yuborish
    sent = await client.send_code_request(phone)
    temp_clients[message.from_user.id] = {'client': client, 'phone': phone, 'phone_code_hash': sent.phone_code_hash}
    
    await message.answer("Kod yuborildi. Kodni kiriting:")
    await state.set_state(AuthStates.waiting_for_code)

@dp.message(AuthStates.waiting_for_code)
async def get_code(message: types.Message, state: FSMContext):
    code = message.text
    data = temp_clients[message.from_user.id]
    client = data['client']
    
    try:
        await client.sign_in(data['phone'], code, phone_code_hash=data['phone_code_hash'])
        session_string = client.session.save()
        await message.answer(f"Muvaffaqiyatli! Sizning STRING_SESSIONingiz:\n\n`{session_string}`\n\nBuni Fly.io secrets'ga qo'shib, botni qayta deploy qiling.")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    
    await state.clear()
