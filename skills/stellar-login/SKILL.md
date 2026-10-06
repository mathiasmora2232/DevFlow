---
name: stellar-login
description: Inicia sesión de DevFlow en StellarCode MCP con aprobación en la web (Google, GitHub o correo + MFA) y verifica la sesión al arrancar un proyecto. Úsalo cuando un comando StellarCode falle por falta de token, cuando `devflow inicio` reporte "sin sesión", o cuando la persona pida conectar/loguear DevFlow o el MCP.
---

# stellar-login

DevFlow nunca pide ni recibe contraseñas ni tokens en el chat. La persona inicia sesión en la web de StellarCode (botón **Continuar con Google**) y aprueba la conexión; el CLI recibe un token MCP de vida corta (≤ 24 h) y lo guarda fuera del repo en `~/.devflow/stellar.env` (permisos 600).

## Al arrancar un proyecto

```bash
devflow inicio
```

Reporta config, vínculo con StellarCode y estado de login. Si dice `Auth: sin sesión`, sigue el protocolo de abajo antes de cualquier comando StellarCode. Sin sesión el trabajo continúa en modo offline/pending-sync, nunca se finge un sync.

Para que esto ocurra automáticamente en Claude Code:

```bash
devflow inicio --install-hook   # agrega un SessionStart hook a .claude/settings.json del proyecto
```

## Protocolo para agentes (no interactivo)

Los agentes no ven la terminal de la persona y un comando bloqueante oculta el enlace. Por eso el login se hace en dos pasos:

1. Generar el enlace (no bloquea):

   ```bash
   devflow stellar-login --no-wait --json
   ```

   Devuelve `login_url`, `approve_url`, `user_code` y `expires_at`. Nunca devuelve el `device_code` secreto.

2. Mostrar a la persona **en el chat**, como enlace clicable:

   > Para conectar DevFlow con StellarCode abre este enlace, entra con **Continuar con Google** y pulsa **Aprobar**:
   > [Iniciar sesión en StellarCode](<login_url>)
   > Verifica que la web muestre el código **<user_code>**. (Si ya tienes la sesión abierta en la web puedes usar directamente <approve_url>.)

3. Esperar la aprobación (bloquea hasta aprobar o vencer; dar ~10 min de timeout a la herramienta o ejecutarlo en segundo plano):

   ```bash
   devflow stellar-login --wait --timeout 540
   ```

   - exit `0`: conectado. Confirmar con `devflow stellar-auth`.
   - exit `7`: aún pendiente; preguntar si ya aprobó y repetir `--wait`.
   - exit `5`: denegado, vencido o error; volver al paso 1.
   - exit `6`: no había login pendiente; volver al paso 1.

4. Si el proyecto aún no está vinculado: `devflow stellar-login --wait --project-id <id>` vincula al terminar, o usar `devflow stellar-adopt` para crearlo.

## Uso humano (terminal interactiva)

```bash
devflow stellar-login            # imprime enlace + código, abre el navegador y espera
devflow stellar-login --no-open  # SSH/contenedores: solo imprime el enlace
devflow stellar-login --dev      # API/web de desarrollo (perfil ~/.devflow/stellar-dev.env)
devflow stellar-auth             # ¿hay sesión? ¿cuándo vence? (exit 6 si no)
devflow stellar-logout           # borra la credencial local
```

## Reglas

- Nunca pedir, mostrar, copiar ni registrar el token en chat, Markdown, `.devflow.yml`, `ops/` ni commits.
- Nunca imprimir el contenido de `~/.devflow/stellar*.env`.
- Precedencia del token: variable `stellarcode.auth.token_env` → `STELLARCODE_TOKEN` → `STELLAR_MCP_TOKEN` → credencial de `devflow stellar-login`. CI y service accounts usan variables de entorno, no el login web.
- Solo administradores de StellarCode pueden aprobar conexiones MCP; si la web responde 403, la persona debe pedir acceso a un admin. No intentes rodearlo.
- La aprobación la da la persona: el agente nunca abre sesión ni aprueba en su nombre.
- Si el token vence a mitad de trabajo (`StellarCode session expired`), repetir el protocolo; no reintentar en bucle.
- RBAC lo aplica el servidor; tener sesión no implica permiso para escribir (`Escrituras: solo lectura`).
