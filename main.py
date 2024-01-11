import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
from datetime import datetime, timedelta, time


category = ["products", "hobby", "beauty and medicine", "clothes", "charity", "utilities", "sport"]
TokenBot = '6774612692:AAH-1t7oIcFpNWqHLO2Gjld3o9_-8tCT1TA'

logging.basicConfig(
    format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Minus:
    def __init__(self, suma: int, category: str, data_vytraty:datetime = None):
        self.suma = suma
        self.category = category
        self.data_vytraty = data_vytraty
        with open('Витрати.txt', 'a') as file:
            file.write(f'{self.suma} {self.category} | {self.data_vytraty.strftime("%Y-%m-%d %H:%M:%S")}\n')


class Plus:
    def __init__(self, suma: int, category: str, data_zarobitku: datetime = None):
        self.suma = suma
        self.category = category
        self.data_zarobitku = data_zarobitku
        with open('Доходи.txt', 'a') as file:
            file.write(f'{self.suma} {self.category} | {self.data_zarobitku.strftime("%Y-%m-%d %H:%M:%S")}\n')


async def start(update: Update, context: CallbackContext):
    logging.info("Command start was triggered")
    await update.message.reply_text("Мій журнал витрат\n"
                                    "Команди: \n"
                                    "Список категорій: /list\n"
                                    "Додати витрату: /minus <сума> | [категорія]\n"
                                    "Додати дохід: /plus <сума> | [категорія]\n"
                                    "Список витрат за день|тиждень|місяць: /vytraty [d|w|m]\n"
                                    "Список доходів за день|тиждень|місяць: /dochody [d|w|m]\n"
                                    "Видалити витрату зі списку: /rem_vytr [номер у списку]\n"
                                    "Видалити дохід зі списку: /rem_doch [номер у списку]\n"
                                    "Статистика витрат за день|тиждень|місяць: /stat_vytr [d|w|m]\n"
                                    "Статистика доходів за день|тиждень|місяць: /stat_doch [d|w|m]"
                                    )


async def add_vytratu(update: Update, context: CallbackContext) -> None:
    vytraty_parts = " ".join(context.args).split("|")
    vytrata_suma = vytraty_parts[0].strip()
    if vytraty_parts[1].strip() in category:
        vytrata_category = vytraty_parts[1].strip()
    else:
        logging.error("Invalid category")
        await update.message.reply_text("Ви вказали не існуючу категорію!")
        return
    data_vytraty = datetime.now()
    vytrata = Minus(vytrata_suma, vytrata_category, data_vytraty)
    await update.message.reply_text(f"Витрату на суму {vytrata_suma} грн категорії {vytrata_category} було додано!")


async def list_category(update: Update, context: CallbackContext) -> None:
    result = '\n'.join(f"{i + 1}. {t}" for i, t in enumerate(category))
    await update.message.reply_text(result)


async def add_dochid(update: Update, context: CallbackContext) -> None:
    dochid_parts = " ".join(context.args).split("|")
    dochid_suma = dochid_parts[0].strip()
    dochid_category = dochid_parts[1].strip()
    data_dochodu = datetime.now()
    dochid = Plus(dochid_suma, dochid_category, data_dochodu)
    await update.message.reply_text(f"Дохід на суму {dochid_suma} грн категорії {dochid_category} було додано!")


async def spysok_vytrat(update: Update, context: CallbackContext) -> None:
    now = datetime.now()
    terminy = {'m': 30,
               'w': 7,
               'd': 1}
    try:
        termin = 0
        if context.args[0] in terminy.keys():
            termin = terminy[context.args[0]]
    except (ValueError, IndexError):
        await update.message.reply_text(f"Ви вказали не вірний термін!")
    spysok_vytrat = []
    try:
        with open('Витрати.txt', 'r') as file:
            for vytrata in file:
                if datetime.strptime(vytrata.split("|")[1].strip(), "%Y-%m-%d %H:%M:%S") >= (now - timedelta(days=termin)):
                    spysok_vytrat.append(vytrata)
    except FileNotFoundError:
        await update.message.reply_text("У вас ще немає витрат")
    if spysok_vytrat:
        result = ''.join(f"{i + 1}. {t}" for i, t in enumerate(spysok_vytrat))
        await update.message.reply_text(f"Список витрат за останні {termin} днів:\n{result}")
    else:
        await update.message.reply_text("У вас немає витрат за цей термін")


async def remove_vytr(update: Update, context: CallbackContext) -> None:
    spysok_vytrat = []
    try:
        with open('Витрати.txt', 'r') as file:
            for vytrata in file:
                spysok_vytrat.append(vytrata)
            spysok_vytrat.pop(int(context.args[0]) - 1)
        with open('Витрати.txt', 'w') as file:
            for i in spysok_vytrat:
                file.write(i)
        await update.message.reply_text(f"Витрату було видалено")
    except (ValueError, IndexError):
        await update.message.reply_text(f"Ви вказали не вірний індекс")
    except FileNotFoundError:
        await update.message.reply_text("У вас ще немає витрат")


async def spysok_dochodiv(update: Update, context: CallbackContext) -> None:
    now = datetime.now()
    terminy = {'m': 30,
               'w': 7,
               'd': 1}
    try:
        termin = 0
        if context.args[0] in terminy.keys():
            termin = terminy[context.args[0]]
    except (ValueError, IndexError):
        await update.message.reply_text(f"Ви вказали не вірний термін!")
    spysok_dochodiv = []
    try:
        with open('Доходи.txt', 'r') as file:
            for dochid in file:
                if datetime.strptime(dochid.split("|")[1].strip(), "%Y-%m-%d %H:%M:%S") >= (now - timedelta(days=termin)):
                    spysok_dochodiv.append(dochid)
    except FileNotFoundError:
        await update.message.reply_text("У вас ще немає доходів")
    if spysok_dochodiv:
        result = ''.join(f"{i + 1}. {t}" for i, t in enumerate(spysok_dochodiv))
        await update.message.reply_text(f"Список доходів за останні {termin} днів:\n{result}")
    else:
        await update.message.reply_text("У вас немає доходів цього місяця")


async def remove_doch(update: Update, context: CallbackContext) -> None:
    spysok_dochodiv = []
    try:
        with open('Доходи.txt', 'r') as file:
            for dochid in file:
                spysok_dochodiv.append(dochid)
            spysok_dochodiv.pop(int(context.args[0]) - 1)
        with open('Доходи.txt', 'w') as file:
            for i in spysok_dochodiv:
                file.write(i)
        await update.message.reply_text(f"Дохід було видалено")
    except (ValueError, IndexError):
        await update.message.reply_text(f"Ви вказали не вірний індекс")
    except FileNotFoundError:
        await update.message.reply_text("У вас ще немає доходів")


async def statystyka_vytrat(update: Update, context: CallbackContext) -> None:
    now = datetime.now()
    terminy = {'m': 30,
              'w': 7,
              'd': 1}
    try:
        termin = 0
        if context.args[0] in terminy.keys():
            termin = terminy[context.args[0]]
    except (ValueError, IndexError):
        await update.message.reply_text(f"Ви вказали не вірний термін для статистики")
    spysok_vytrat = {}
    try:
        with open('Витрати.txt', 'r') as file:
            for vytrata in file:
                if datetime.strptime(vytrata.split("|")[1].strip(), "%Y-%m-%d %H:%M:%S") >= (now - timedelta(days=termin)):
                    if vytrata.split(" ")[1].strip() in spysok_vytrat.keys():
                        spysok_vytrat[vytrata.split(" ")[1]] += int(vytrata.split(" ")[0])
                    else:
                        spysok_vytrat[vytrata.split(" ")[1]] = int(vytrata.split(" ")[0])
    except FileNotFoundError:
        await update.message.reply_text("У вас ще немає витрат")
    if spysok_vytrat:
        result = ''.join(f" {n} грн - {t}\n" for t, n in spysok_vytrat.items())
        await update.message.reply_text(f"Статистика витрат за останні {termin} днів:\n{result}")
    else:
        await update.message.reply_text("У вас немає витрат за цей період часу")


async def statystyka_dochodiv(update: Update, context: CallbackContext) -> None:
    now = datetime.now()
    terminy = {'m': 30,
              'w': 7,
              'd': 1}
    try:
        termin = 0
        if context.args[0] in terminy.keys():
            termin = terminy[context.args[0]]
    except (ValueError, IndexError):
        await update.message.reply_text(f"Ви вказали не вірний термін для статистики")
    spysok_dochodiv = {}
    try:
        with open('Доходи.txt', 'r') as file:
            for dochid in file:
                if datetime.strptime(dochid.split("|")[1].strip(), "%Y-%m-%d %H:%M:%S") >= (now - timedelta(days=termin)):
                    if dochid.split(" ")[1].strip() in spysok_dochodiv.keys():
                        spysok_dochodiv[dochid.split(" ")[1]] += int(dochid.split(" ")[0])
                    else:
                        spysok_dochodiv[dochid.split(" ")[1]] = int(dochid.split(" ")[0])
    except FileNotFoundError:
        await update.message.reply_text("У вас ще немає доходів")
    if spysok_vytrat:
        result = ''.join(f" {n} грн - {t}\n" for t, n in spysok_dochodiv.items())
        await update.message.reply_text(f"Статистика доходів за останні {termin} днів:\n{result}")
    else:
        await update.message.reply_text("У вас немає доходів за цей період часу")


def run():
    app = ApplicationBuilder().token(TokenBot).build()
    logging.info("Application build succesfully")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("minus", add_vytratu))
    app.add_handler(CommandHandler("plus", add_dochid))
    app.add_handler(CommandHandler("vytraty", spysok_vytrat))
    app.add_handler(CommandHandler("rem_vytr", remove_vytr))
    app.add_handler(CommandHandler("rem_doch", remove_doch))
    app.add_handler(CommandHandler("dochody", spysok_dochodiv))
    app.add_handler(CommandHandler("stat_vytr", statystyka_vytrat))
    app.add_handler(CommandHandler("stat_doch", statystyka_dochodiv))
    app.add_handler(CommandHandler("list", list_category))

    app.run_polling()

if __name__ == "__main__":
    run()
