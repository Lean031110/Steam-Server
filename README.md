# LBA Bot 🤖

LBA Bot es un asistente virtual inteligente diseñado para responder preguntas, administrar grupos y aprender de las conversaciones. Este bot está construido con Python y utiliza la biblioteca `python-telegram-bot`.

---

## Características Principales 🚀

- **Respuestas Inteligentes:** Aprende de las conversaciones y responde preguntas.
- **Administración de Grupos:** Envía mensajes periódicos, silencia usuarios y más.
- **Entrenamiento Personalizado:** Entrena al bot con nuevas respuestas usando el comando `/train`.
- **Interacción con Botones:** Menús interactivos para facilitar la navegación.
- **Política de Privacidad:** Transparencia en el manejo de datos.

---

## Cómo Usar el Bot 🛠️

### Comandos Disponibles

- `/start`: Inicia la conversación y muestra la botonera principal.
- `/help`: Muestra la lista de comandos y opciones de ayuda.
- `/train <palabra clave> - <respuesta 1> -- <respuesta 2>`: Entrena al bot con nuevas respuestas.
- `/broadcast <mensaje>`: Envía un mensaje global a todos los miembros del grupo (solo para administradores).

### Botonera Principal

- **Actualizar 🔄:** Actualiza el bot.
- **Política de Privacidad 📜:** Muestra la política de privacidad.
- **Administrar Grupo 🛠️:** Gestiona mensajes periódicos, silencia usuarios, etc.
- **Añadir a Grupo ➕:** Obtén el enlace para añadir el bot a un grupo.
- **Ayuda ❓:** Muestra el menú de ayuda.
- **¿Qué Puedo Hacer? 🤔:** Explica las funcionalidades del bot.

---

## Requisitos 📋

- Python 3.10 o superior.
- Biblioteca `python-telegram-bot`.
- Un token de bot de Telegram (obtenido desde [BotFather](https://core.telegram.org/bots#botfather)).

---

## Instalación 🛠️

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/lba-bot.git
   cd lba-bot
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura el bot:**
   - Crea un archivo `.env` en la raíz del proyecto y añade tu token de bot:
     ```env
     TELEGRAM_TOKEN=tu_token_aqui
     ```

4. **Ejecuta el bot:**
   ```bash
   python bot.py
   ```

---

## Política de Privacidad 📜

LBA Bot no almacena datos personales. Los mensajes se usan únicamente para entrenar al bot y mejorar sus respuestas. Puedes solicitar la eliminación de tus datos en cualquier momento.

Para más detalles, consulta el archivo [privacy_policy.txt](privacy_policy.txt).

---

## Contribuir 🤝

¡Las contribuciones son bienvenidas! Si deseas mejorar el bot, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -m 'Añade nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## Licencia 📄

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## Contacto 📧

Si tienes preguntas o sugerencias, contáctanos en [soporte@lbabot.com](mailto:soporte@lbabot.com).

---

¡Gracias por usar LBA Bot! 🤖

---

### **Estructura del Proyecto:**

```
lba-bot/
├── bot.py                # Código principal del bot
├── training_data.json    # Datos de entrenamiento del bot
├── privacy_policy.txt    # Política de privacidad
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Este archivo
├── LICENSE               # Licencia del proyecto
└── .env                  # Archivo de configuración (token)
```
