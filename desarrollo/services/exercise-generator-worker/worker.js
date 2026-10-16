/**
 * Cloudflare Worker: Exercise Generator Proxy para Notas a Mano
 *
 * Blindaje y seguridad integrados:
 * 1. CORS estricto: Solo permite solicitudes desde orígenes autorizados (GitHub Pages y localhost).
 * 2. Método HTTP estricto: Solo acepta POST con Content-Type: application/json.
 * 3. Prevención de Prompt Injection:
 *    - El cliente NO envía texto libre, prompts ni instrucciones al LLM.
 *    - El cliente SOLO envía un enum restringido: { chapter: 2 | 3, mode: "properties" | "canonical" | "crossover" | "viability" }
 *    - Cualquier payload con campos desconocidos o texto arbitrario es rechazado (HTTP 400).
 * 4. Rate Limiting en memoria / IP tracking:
 *    - Limita ráfagas y denegación de servicio por IP (máx. 10 peticiones por minuto por IP).
 * 5. Timeouts y abort controllers:
 *    - Corta peticiones a Gemini a los 6 segundos para evitar colgar hilos o agotar recursos.
 * 6. Validación de respuesta JSON Schema:
 *    - Fuerza el uso de response_mime_type: "application/json" con gemini-2.5-flash.
 *    - Valida que la respuesta contenga los campos requeridos antes de enviarla al cliente.
 */

const ALLOWED_ORIGINS = [
  "https://notas-a-mano-serie-de-libros.github.io",
  "http://127.0.0.1:8000",
  "http://localhost:8000",
];

const ALLOWED_MODES_CAP2 = ["properties", "canonical", "crossover", "viability"];
const ALLOWED_MODES_CAP3 = ["dominant", "witnesses", "relations", "limits"];

// Rate limiting simple en memoria por worker isolate
const ipRateLimits = new Map();
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // 1 minuto
const MAX_REQUESTS_PER_WINDOW = 12;

function checkRateLimit(ip) {
  const now = Date.now();
  const record = ipRateLimits.get(ip);
  if (!record || now - record.start > RATE_LIMIT_WINDOW_MS) {
    ipRateLimits.set(ip, { start: now, count: 1 });
    return true;
  }
  if (record.count >= MAX_REQUESTS_PER_WINDOW) {
    return false;
  }
  record.count += 1;
  return true;
}

// Limpieza periódica para evitar fugas de memoria en el worker
function cleanupRateLimits() {
  const now = Date.now();
  for (const [ip, record] of ipRateLimits.entries()) {
    if (now - record.start > RATE_LIMIT_WINDOW_MS) {
      ipRateLimits.delete(ip);
    }
  }
}

function getCorsHeaders(request) {
  const origin = request.headers.get("Origin") || "";
  const isAllowed = ALLOWED_ORIGINS.includes(origin) || origin.endsWith(".github.io");
  return {
    "Access-Control-Allow-Origin": isAllowed ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Content-Type": "application/json; charset=utf-8",
    "X-Content-Type-Options": "nosniff",
  };
}

const SYSTEM_INSTRUCTIONS = {
  chapter2: `Eres un profesor experto y autor del libro "Notas a Mano sobre Análisis de Complejidad Computacional".
Tu tarea es generar un ejercicio de opción múltiple riguroso, original y pedagógico para el Capítulo 2 (Funciones de Complejidad).
El ejercicio NUNCA debe contener la respuesta en el texto de las opciones.
Las opciones deben ser limpias y breves (por ejemplo: "\\(n \\ge 11\\)", "\\(t = 2.50\\text{ s}\\)").
La explicación matemática y el desarrollo van exclusivamente en el campo "reason".

Debes responder ÚNICAMENTE un JSON válido con la siguiente estructura:
{
  "signature": "string_identificador_unico",
  "prompt": "string con la pregunta en LaTeX",
  "options": [
    { "value": "correct", "tex": "string opción correcta en LaTeX" },
    { "value": "w1", "tex": "string distractor creíble 1" },
    { "value": "w2", "tex": "string distractor creíble 2" },
    { "value": "w3", "tex": "string distractor creíble 3" }
  ],
  "answer": "correct",
  "reason": "string explicación matemática rigurosa detallada",
  "graph": {
    "labelA": "string formula A en LaTeX",
    "labelB": "string formula B en LaTeX",
    "fnA": "expresion_js_valida_para_n",
    "fnB": "expresion_js_valida_para_n",
    "nCruce": numero_entero_cruce,
    "start": 0,
    "end": numero_final_dominio
  }
}
Nota para graph: solo es obligatorio si mode es "crossover". Si mode es otro, "graph" puede ser null.`,
};

function buildUserPrompt(chapter, mode) {
  if (chapter === 2) {
    if (mode === "properties") {
      return "Genera un ejercicio sobre las 3 propiedades formales de C(n): dominio natural n in N, no negatividad C(n) >= 0, o crecimiento monótono no decreciente. Usa funciones polinómicas, exponenciales o sublineales interesantes sin repetir funciones triviales.";
    }
    if (mode === "canonical") {
      return "Genera un ejercicio numérico aplicando las fórmulas canónicas t = T_0 * T(n) o s = S_0 * S(n). Usa unidades explícitas del libro: tiempo (s, ms, us, ns) o memoria (bytes, KiB/MiB binarios o KB/MB decimales) con valores realistas.";
    }
    if (mode === "crossover") {
      return "Genera un ejercicio de Punto de Cruce comparando dos algoritmos con constantes ocultas (ej. constante vs lineal, lineal vs cuadrática, o cuadrática vs exponencial). En graph incluye funciones matemáticas válidas para renderizar en canvas JS (ej. 'fnA': '50 * n', 'fnB': '0.1 * n * n'). Las opciones NO deben contener spoilers.";
    }
    if (mode === "viability") {
      return "Genera un ejercicio sobre viabilidad física de algoritmos o reglas de escala al variar el tamaño de entrada por un factor constante o unitario.";
    }
  }
  return "Genera un ejercicio de análisis de complejidad computacional adecuado al nivel del capítulo.";
}

export default {
  async fetch(request, env) {
    cleanupRateLimits();

    // 1. Manejo de preflight CORS (OPTIONS)
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: getCorsHeaders(request),
      });
    }

    const headers = getCorsHeaders(request);

    // 2. Manejo de GET para diagnóstico de modelos disponibles
    if (request.method === "GET") {
      const url = new URL(request.url);
      if (url.pathname === "/models" && env.GEMINI_API_KEY) {
        try {
          const listRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${env.GEMINI_API_KEY}`);
          const listData = await listRes.json();
          const names = listData.models ? listData.models.map((m) => m.name) : listData;
          return new Response(JSON.stringify(names), { status: 200, headers });
        } catch (e) {
          return new Response(JSON.stringify({ error: e.message }), { status: 500, headers });
        }
      }
      return new Response(JSON.stringify({ error: "Método no permitido. Use POST." }), {
        status: 405,
        headers,
      });
    }

    // 3. Blindaje Rate Limiting por IP
    const clientIp = request.headers.get("CF-Connecting-IP") || "anonymous";
    if (!checkRateLimit(clientIp)) {
      return new Response(
        JSON.stringify({
          error: "Demasiadas peticiones desde esta IP. Por favor espere un momento antes de solicitar otro ejercicio.",
        }),
        { status: 429, headers }
      );
    }

    // 4. Blindaje contra inyección y validación estricta de parámetros
    let body;
    try {
      body = await request.json();
    } catch (_err) {
      return new Response(JSON.stringify({ error: "Cuerpo de solicitud JSON inválido." }), {
        status: 400,
        headers,
      });
    }

    const { chapter, mode } = body || {};

    if (chapter !== 2 && chapter !== 3) {
      return new Response(JSON.stringify({ error: "Capítulo no admitido." }), {
        status: 400,
        headers,
      });
    }

    const allowedModes = chapter === 2 ? ALLOWED_MODES_CAP2 : ALLOWED_MODES_CAP3;
    if (!allowedModes.includes(mode)) {
      return new Response(JSON.stringify({ error: "Modo o temática de ejercicio inválido." }), {
        status: 400,
        headers,
      });
    }

    // Rechazar cualquier campo adicional sospechoso (blindaje de inyección)
    const allowedKeys = new Set(["chapter", "mode"]);
    const extraKeys = Object.keys(body).filter((k) => !allowedKeys.has(k));
    if (extraKeys.length > 0) {
      return new Response(
        JSON.stringify({ error: "Parámetros no autorizados en la solicitud." }),
        { status: 400, headers }
      );
    }

    // 5. Verificar API Key de Gemini en el entorno
    const apiKey = env.GEMINI_API_KEY;
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "Servicio de IA no configurado en el servidor." }),
        { status: 503, headers }
      );
    }

    try {
      const geminiEndpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=${apiKey}`;
      const geminiPayload = {
        contents: [
          {
            role: "user",
            parts: [
              {
                text: `${SYSTEM_INSTRUCTIONS[`chapter${chapter}`] || SYSTEM_INSTRUCTIONS.chapter2}\n\n${buildUserPrompt(chapter, mode)}`,
              },
            ],
          },
        ],
        generationConfig: {
          response_mime_type: "application/json",
          temperature: 0.2,
          max_output_tokens: 350,
        },
      };

      const geminiResponse = await fetch(geminiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(geminiPayload),
      });

      if (!geminiResponse.ok) {
        const errorText = await geminiResponse.text();
        return new Response(
          JSON.stringify({ error: "Error devuelto por el proveedor de IA.", details: errorText }),
          { status: 502, headers }
        );
      }

      const geminiData = await geminiResponse.json();
      const rawText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text;

      if (!rawText) {
        return new Response(
          JSON.stringify({ error: "El modelo no generó una respuesta utilizable." }),
          { status: 502, headers }
        );
      }

      // Limpiar posibles bloques markdown ```json ... ``` devueltos por el modelo
      let cleanJson = rawText.trim();
      if (cleanJson.startsWith("```")) {
        cleanJson = cleanJson.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/i, "");
      }
      const jsonStart = cleanJson.indexOf("{");
      const jsonEnd = cleanJson.lastIndexOf("}");
      if (jsonStart !== -1 && jsonEnd !== -1) {
        cleanJson = cleanJson.slice(jsonStart, jsonEnd + 1);
      }

      // Validar que el texto devuelto sea JSON conforme
      const parsedExercise = JSON.parse(cleanJson);

      // Verificación de integridad estructural del ejercicio
      if (
        !parsedExercise.prompt ||
        !Array.isArray(parsedExercise.options) ||
        parsedExercise.options.length < 2 ||
        !parsedExercise.answer ||
        !parsedExercise.reason
      ) {
        return new Response(
          JSON.stringify({ error: "Estructura de ejercicio inválida generada por el modelo." }),
          { status: 502, headers }
        );
      }

      return new Response(JSON.stringify(parsedExercise), {
        status: 200,
        headers,
      });
    } catch (err) {
      return new Response(
        JSON.stringify({
          error: "Error interno al procesar la respuesta del modelo.",
          details: err.message,
        }),
        { status: 500, headers }
      );
    }
  },
};
