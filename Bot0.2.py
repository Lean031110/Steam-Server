import logging
import json
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configura el logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar o inicializar el archivo de entrenamiento
try:
    with open("training_data.json", "r") as file:
        training_data = json.load(file)
except FileNotFoundError:
    training_data = {}

# Guardar el archivo de entrenamiento
def save_training_data():
    with open("training_data.json", "w") as file:
        json.dump(training_data, file)

# Comando de inicio
async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    reply_keyboard = [["/train", "/help"], ["Saludar 👋"]]
    await update.message.reply_text(
        f'¡Hola, {user_name}! 🤖 Soy un bot que aprende de nuestras conversaciones. ¿En qué puedo ayudarte?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

# Comando de ayuda
async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = """
    🛠️ Comandos disponibles:
    /start - Inicia la conversación.
    /help - Muestra esta ayuda.
    /train <palabra clave> - <respuesta 1> -- <respuesta 2> -- <respuesta 3> - Entrena al bot con múltiples respuestas.
    También puedes usar los botones para interactuar.
    """
    await update.message.reply_text(help_text)

# Comando para entrenar al bot
async def train_bot(update: Update, context: CallbackContext) -> None:
    try:
        # Obtén la palabra clave y las respuestas del mensaje
        command_parts = update.message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await update.message.reply_text('⚠️ Formato incorrecto. Usa: /train <palabra clave> - <respuesta 1> -- <respuesta 2> -- <respuesta 3>')
            return

        _, args = command_parts
        keyword, responses = args.split(" - ", maxsplit=1)
        responses_list = [r.strip() for r in responses.split(" -- ")]

        # Guarda las respuestas en el diccionario de entrenamiento
        training_data[keyword.lower()] = responses_list
        save_training_data()

        await update.message.reply_text(f'✅ Entendido! He aprendido que cuando digas "{keyword}", responderé con una de estas opciones: {", ".join(responses_list)}.')
    except Exception as e:
        logger.error(f"Error al entrenar al bot: {e}")
        await update.message.reply_text('⚠️ Hubo un error al procesar tu solicitud.')

# Manejo de mensajes de texto en grupos (solo responde si es mencionado)
async def group_message_handler(update: Update, context: CallbackContext) -> None:
    # Verifica si el bot fue mencionado
    if update.message and update.message.text and context.bot.username in update.message.text:
        user_message = update.message.text.lower().replace(f"@{context.bot.username}", "").strip()
        logger.info(f"Grupo - Usuario: {user_message}")

        # Busca una respuesta en la biblioteca de entrenamiento
        response = None
        for keyword, responses in training_data.items():
            if keyword in user_message:
                response = random.choice(responses)  # Selecciona una respuesta al azar
                break

        # Si no hay una respuesta entrenada, responde con un mensaje predeterminado
        if not response:
            response = "🤔 No estoy seguro de cómo responder a eso. ¿Puedes enseñarme?"

        # Envía la respuesta al grupo
        await update.message.reply_text(response)

# Manejo de mensajes de texto en privado
async def private_message_handler(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    logger.info(f"Privado - Usuario: {user_message}")

    # Busca una respuesta en la biblioteca de entrenamiento
    response = None
    for keyword, responses in training_data.items():
        if keyword in user_message:
            response = random.choice(responses)  # Selecciona una respuesta al azar
            break

    # Si no hay una respuesta entrenada, responde con un mensaje predeterminado
    if not response:
        response = "🤔 No estoy seguro de cómo responder a eso. ¿Puedes enseñarme?"

    # Envía la respuesta al usuario
    await update.message.reply_text(response)

# Manejo de botones
async def button_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Saludar 👋":
        await update.message.reply_text("¡Hola! 👋 ¿Cómo estás?")
    else:
        await update.message.reply_text("No entiendo ese comando. Usa /help para ver las opciones.")

# Manejo de errores
async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Error: {context.error}")

def main() -> None:
    # Inserta tu token de Telegram aquí
    token = '7897159457:AAGdzYZ7aY8ZpoSpBSpsY3jSLxlyGTrxCEU'

    # Crea la aplicación y pasa el token de tu bot
    application = Application.builder().token(token).build()

    # Registra los comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("train", train_bot))

    # Registra el manejador de mensajes en grupos (solo responde si es mencionado)
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & filters.Entity("mention"), group_message_handler))

    # Registra el manejador de mensajes en privado
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, private_message_handler))

    # Registra el manejador de botones
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    # Registra el manejador de errores
    application.add_error_handler(error_handler)

    # Inicia el bot
    application.run_polling()

if __name__ == '__main__':
    main()