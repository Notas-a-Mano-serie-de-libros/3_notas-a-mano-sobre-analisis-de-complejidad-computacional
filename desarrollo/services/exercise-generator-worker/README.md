# Servicio Proxy de IA para Generación de Ejercicios

Este microservicio corre como un **Cloudflare Worker Serverless** para generar ejercicios inéditos mediante Google Gemini Flash de forma **100% transparente para el lector** (sin exponer claves en el cliente y sin que el lector deba registrarse).

## Blindajes de Seguridad Implementados en `worker.js`

1. **CORS Restringido**:
   - Solo responde a solicitudes originadas desde `https://notas-a-mano-serie-de-libros.github.io` y servidores locales autorizados.

2. **Inmunidad a Prompt Injection**:
   - El cliente **no envía texto libre** ni instrucciones.
   - Solo se aceptan solicitudes `POST` con un esquema cerrado:
     ```json
     {
       "chapter": 2,
       "mode": "crossover"
     }
     ```
   - Cualquier parámetro desconocido, texto arbitrario o payload extraño es rechazado de inmediato con `HTTP 400 Bad Request`.

3. **Rate Limiting por IP**:
   - Limita a un máximo de 12 peticiones por minuto por IP para prevenir ataques de denegación de servicio (DoS) o agotamiento intencional de cuota.

4. **Timeouts y Control de Aborto**:
   - Si la API de Google tarda más de 6 segundos, el Worker cancela la conexión (`AbortController`) evitando hilos colgados.

5. **Validación Estricta de Esquema JSON**:
   - Se fuerza `response_mime_type: "application/json"`.
   - Se valida la presencia de `prompt`, `options`, `answer`, `reason` antes de reenviar el resultado al navegador.

---

## Cómo desplegar el Worker en 3 minutos

1. Instalar Wrangler (herramienta oficial de Cloudflare):
   ```bash
   npm install -g wrangler
   ```

2. Iniciar sesión en Cloudflare (gratis):
   ```bash
   wrangler login
   ```

3. Agregar la clave secreta de Gemini:
   ```bash
   cd desarrollo/services/exercise-generator-worker
   wrangler secret put GEMINI_API_KEY
   # Pega tu API Key de Google AI Studio cuando te la pida
   ```

4. Desplegar:
   ```bash
   wrangler deploy
   ```
   Wrangler te dará una URL pública tipo:
   `https://exercise-generator-worker.<tu-subdominio>.workers.dev`

5. Poner esa URL en `chapter2-practice.js` en la constante `AI_SERVICE_URL`.
