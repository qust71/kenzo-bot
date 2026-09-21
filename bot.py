import os, asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN=os.getenv('BOT_TOKEN')
if not TOKEN: raise RuntimeError('BOT_TOKEN is not set')
bot=Bot(TOKEN); dp=Dispatcher()
SERVICES={'bath':('🧖 Баня','Финская / русская баня.'),'hammam':('♨️ Хамам','Парная зона для отдыха.'),'pool':('🏊 Бассейн','Бассейн и зона отдыха.'),'hotel':('🛏 Номера','Проживание на 2–3 этажах.')}
def menu():
 k=InlineKeyboardBuilder(); k.button(text='🗓 Забронировать',callback_data='book'); k.button(text='💰 Цены',callback_data='prices'); k.button(text='✨ Наши услуги',callback_data='services'); k.button(text='📍 Контакты',callback_data='contacts'); k.adjust(1); return k.as_markup()
def back():
 k=InlineKeyboardBuilder(); k.button(text='⬅️ Назад',callback_data='home'); return k.as_markup()
@dp.message(CommandStart())
async def start(m:Message): await m.answer('🏨 <b>KENZO</b>\n\nДобро пожаловать в наш комплекс в Туле.\n\nБаня • Хамам • Бассейн • Проживание\n\nВыберите раздел:',reply_markup=menu(),parse_mode='HTML')
@dp.callback_query(F.data=='home')
async def home(c:CallbackQuery): await c.message.edit_text('🏨 <b>KENZO</b>\n\nВыберите раздел:',reply_markup=menu(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='services')
async def services(c:CallbackQuery):
 k=InlineKeyboardBuilder()
 for key,(title,_) in SERVICES.items(): k.button(text=title,callback_data='service:'+key)
 k.button(text='⬅️ Назад',callback_data='home'); k.adjust(1)
 await c.message.edit_text('✨ <b>Наши услуги</b>\n\nВыберите услугу:',reply_markup=k.as_markup(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data.startswith('service:'))
async def service(c:CallbackQuery):
 title,desc=SERVICES[c.data.split(':')[1]]; k=InlineKeyboardBuilder(); k.button(text='🗓 Забронировать',callback_data='book'); k.button(text='⬅️ К услугам',callback_data='services'); k.adjust(1)
 await c.message.edit_text(f'{title}\n\n{desc}',reply_markup=k.as_markup(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='prices')
async def prices(c:CallbackQuery):
 await c.message.edit_text('💰 <b>Цены</b>\n\n🧖 Баня — от 5 000 ₽\n♨️ Хамам — от 4 000 ₽\n🏊 Бассейн — от 3 000 ₽\n🛏 Номера — от 4 000 ₽/сутки\n\nЦены пока ориентировочные.',reply_markup=back(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='contacts')
async def contacts(c:CallbackQuery): await c.message.edit_text('📍 <b>Контакты KENZO</b>\n\nТула\n📞 Телефон: добавим\n📱 Telegram: добавим\n📌 Адрес: добавим',reply_markup=back(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='book')
async def book(c:CallbackQuery):
 k=InlineKeyboardBuilder(); k.button(text='📝 Оставить заявку',callback_data='request'); k.button(text='⬅️ Назад',callback_data='home'); k.adjust(1)
 await c.message.edit_text('🗓 <b>Бронирование KENZO</b>\n\nНажмите «Оставить заявку», затем отправьте дату, время, количество гостей и услугу.',reply_markup=k.as_markup(),parse_mode='HTML'); await c.answer()
@dp.callback_query(F.data=='request')
async def request(c:CallbackQuery): await c.message.edit_text('📝 <b>Заявка</b>\n\nНапишите одним сообщением:\nДата — время — количество гостей — услуга\n\nПример:\n25 сентября, 18:00 — 6 гостей — баня + бассейн',parse_mode='HTML'); await c.answer()
@dp.message()
async def any_message(m:Message): await m.answer('✅ <b>Заявка получена!</b>\n\nАдминистратор подтвердит свободное время и стоимость.\n\nСпасибо, что выбрали <b>KENZO</b>.',parse_mode='HTML')
async def main(): await dp.start_polling(bot)
if __name__=='__main__': asyncio.run(main())
