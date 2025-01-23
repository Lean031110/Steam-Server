import logging
import json
import random
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

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

# Función para leer la política de privacidad desde un archivo
def read_privacy_policy():
    try:
        with open("privacy_policy.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "⚠️ La política de privacidad no está disponible en este momento."

# Comando de inicio
async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    reply_keyboard = [
        ["Actualizar 🔄", "Política de Privacidad 📜"],
        ["Administrar Grupo 🛠️", "Añadir a Grupo ➕"],
        ["Ayuda ❓", "¿Qué Puedo Hacer? 🤔"]
    ]
    await update.message.reply_text(
        f'¡Hola, {user_name}! 🤖 Soy LBA Bot, tu asistente virtual. ¿En qué puedo ayudarte?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

# Comando de ayuda mejorado
async def help_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Comandos Básicos", callback_data='basic_commands')],
        [InlineKeyboardButton("Administrar Grupo", callback_data='group_management')],
        [InlineKeyboardButton("Política de Privacidad", callback_data='privacy_policy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Selecciona una opción para obtener más información:', reply_markup=reply_markup)

# Manejo de botones de ayuda
async def help_button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'basic_commands':
        await query.edit_message_text(text="""
        🛠️ Comandos Básicos:
        /start - Inicia la conversación.
        /help - Muestra esta ayuda.
        /train <palabra clave> - <respuesta 1> -- <respuesta 2> - Entrena al bot.
        """)
    elif query.data == 'group_management':
        await query.edit_message_text(text="""
        🛠️ Administrar Grupo:
        - Usa "Mensaje Periódico" para programar mensajes.
        - Usa "Silenciar Usuario" para silenciar a un miembro.
        - Usa "Expulsar Usuario" para expulsar a un miembro.
        """)
    elif query.data == 'privacy_policy':
        privacy_policy_text = read_privacy_policy()
        await query.edit_message_text(text=privacy_policy_text)

# Botón de Actualizar
async def update_bot(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🔄 Actualizando el bot...")
    # Aquí puedes añadir lógica para actualizar el bot, como recargar datos o reiniciar servicios.
    await update.message.reply_text("✅ El bot ha sido actualizado.")

# Botón de Política de Privacidad
async def privacy_policy(update: Update, context: CallbackContext) -> None:
    privacy_policy_text = read_privacy_policy()
    await update.message.reply_text(privacy_policy_text)

# Botón de Administrar Grupo
async def manage_group(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [["Mensaje Periódico ⏰", "Silenciar Usuario 🔇"], ["Expulsar Usuario 🚫", "Volver ↩️"]]
    await update.message.reply_text(
        "🛠️ Selecciona una opción para administrar el grupo:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

# Botón de Añadir a Grupo
async def add_to_group(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("➕ Para añadir este bot a un grupo, usa el siguiente enlace: https://t.me/LBA_Bot?startgroup=true")

# Botón de ¿Qué Puedo Hacer?
async def what_can_i_do(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("""
    🤔 ¿Qué Puedo Hacer?
    - Responder preguntas.
    - Enviar mensajes periódicos.
    - Administrar grupos (silenciar, expulsar usuarios).
    - Aprender de tus conversaciones.
    """)

# Comando para entrenar al bot
async def train_bot(update: Update, context: CallbackContext) -> None:
    try:
        # Obtén la palabra clave y las respuestas del mensaje
        command_parts = update.message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await update.message.reply_text('⚠️ Formato incorrecto. Usa: /train <palabra clave> - <respuesta 1> -- <respuesta 2>')
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

# Manejo de mensajes de texto en grupos (solo responde si es mencionado o con la palabra "LBA")
async def group_message_handler(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.text:
        if context.bot.username in update.message.text:
            user_message = update.message.text.lower().replace(f"@{context.bot.username}", "").strip()
        elif "lba" in update.message.text.lower():
            user_message = update.message.text.lower().replace("lba", "").strip()
        else:
            return

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

# Manejo de botones de la botonera
async def button_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Actualizar 🔄":
        await update_bot(update, context)
    elif text == "Política de Privacidad 📜":
        await privacy_policy(update, context)
    elif text == "Administrar Grupo 🛠️":
        await manage_group(update, context)
    elif text == "Añadir a Grupo ➕":
        await add_to_group(update, context)
    elif text == "Ayuda ❓":
        await help_command(update, context)
    elif text == "¿Qué Puedo Hacer? 🤔":
        await what_can_i_do(update, context)
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

    # Registra los manejadores de botones
    application.add_handler(CallbackQueryHandler(help_button_handler))

    # Registra los manejadores de mensajes
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, group_message_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, private_message_handler))

    # Registra los manejadores de botones de la botonera
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    # Registra el manejador de errores
    application.add_error_handler(error_handler)

    # Inicia el bot
    application.run_polling()

if __name__ == '__main__':
    main()