import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline, set_seed
from PIL import Image
import requests
from io import BytesIO

# Configura el logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializa el modelo de lenguaje GPT-2
generator = pipeline('text-generation', model='gpt-2')
set_seed(42)

# Función para guardar las conversaciones
def save_conversation(user_message: str, bot_response: str) -> None:
    with open("conversations.txt", "a") as file:
        file.write(f"Usuario: {user_message}\n")
        file.write(f"Bot: {bot_response}\n\n")

# Comando de inicio
async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f'¡Hola, {user_name}! Soy un bot que aprende de nuestras conversaciones. ¿En qué puedo ayudarte?')

# Comando de ayuda
async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = """
    Comandos disponibles:
    /start - Inicia la conversación.
    /help - Muestra esta ayuda.
    /clear - Borra el historial de conversaciones.
    Envía una foto y te la describiré.
    """
    await update.message.reply_text(help_text)

# Comando para borrar conversaciones
async def clear_conversations(update: Update, context: CallbackContext) -> None:
    try:
        open("conversations.txt", "w").close()  # Borra el contenido del archivo
        await update.message.reply_text("Historial de conversaciones borrado.")
    except Exception as e:
        logger.error(f"Error al borrar conversaciones: {e}")
        await update.message.reply_text("Hubo un error al borrar el historial.")

# Manejo de mensajes de texto
async def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"Usuario: {user_message}")

    # Genera una respuesta usando GPT-2
    response = generator(user_message, max_length=50, num_return_sequences=1)[0]['generated_text']

    # Guarda la conversación
    save_conversation(user_message, response)

    # Envía la respuesta al usuario
    await update.message.reply_text(response)

# Manejo de fotos
async def handle_photo(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1].get_file()
    photo_url = photo.file_path

    # Descarga la foto
    response = requests.get(photo_url)
    image = Image.open(BytesIO(response.content))

    # Genera una descripción usando GPT-2 (simulado)
    description = "Esta es una imagen interesante. Podría ser un paisaje o una escena urbana."
    await update.message.reply_text(f"Descripción de la foto: {description}")

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
    application.add_handler(CommandHandler("clear", clear_conversations))

    # Registra el manejador de mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Registra el manejador de fotos
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Registra el manejador de errores
    application.add_error_handler(error_handler)

    # Inicia el bot
    application.run_polling()

if __name__ == '__main__':
    main()