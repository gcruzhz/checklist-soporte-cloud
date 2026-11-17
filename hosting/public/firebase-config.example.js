// Configuración de Firebase para Checklist de Soporte (nube).
//
// CÓMO USARLA:
//   1. Copia este archivo como `firebase-config.js` en ESTA misma carpeta
//      (este archivo de ejemplo SÍ se versiona; `firebase-config.js` NO,
//      está en el .gitignore).
//   2. Llena cada campo con los datos de tu proyecto Firebase:
//      Consola de Firebase → Configuración del proyecto → Tus apps → Web.
//   3. Si cambiaste la config, reconstruye el bundle de la nube (ver README).
//
// NOTA DE SEGURIDAD: la apiKey web es pública por diseño (la seguridad la
// dan las reglas de Firestore, en `firestore.rules`). Lo que NUNCA se
// comparte ni se versiona: el keystore de firma, las contraseñas de los
// usuarios y las claves de IA (Gemini / DeepSeek), que viven en Firestore
// en `config/ai`, no en este archivo.

window.FIREBASE_CONFIG = {
  // Clave de API web del proyecto Firebase.
  apiKey: "TU_API_KEY",
  // Dominio de autenticación, normalmente "<proyecto>.firebaseapp.com".
  authDomain: "TU_PROYECTO.firebaseapp.com",
  // ID del proyecto Firebase.
  projectId: "TU_PROYECTO",
  // Bucket de almacenamiento, normalmente "<proyecto>.appspot.com".
  storageBucket: "TU_PROYECTO.appspot.com",
  // ID del remitente de mensajería del proyecto.
  messagingSenderId: "TU_MESSAGING_SENDER_ID",
  // ID de la app web de Firebase.
  appId: "TU_APP_ID"
};
