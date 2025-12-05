# 🧹 Limpieza del Repositorio para GitHub

## Archivos a ELIMINAR antes de subir a GitHub

Ejecuta estos comandos para limpiar el proyecto:

```bash
# Eliminar archivos temporales y basura
rm -rf __pycache__/
rm -f *.pyc *.pyo *.pyd
rm -f *.log
rm -f *.db *.sqlite
rm -f *.session *.session-journal

# Eliminar entorno virtual (se debe crear en cada instalación)
rm -rf .venv/ venv/ env/

# Eliminar archivos de IDE
rm -rf .vscode/ .idea/
rm -f *.swp *.swo *~

# Eliminar archivos de configuración local
rm -f .DS_Store Thumbs.db

# IMPORTANTE: Verificar que .env NO esté en el repo
# (debería estar en .gitignore)
ls -la .env  # Si aparece, NO lo subas

# Verificar archivos que se subirán
git status
```

## Estructura Final del Repositorio

```
✅ SUBIR A GITHUB:
telegram-bot-downloader/
├── bot_with_paywall.py       # Bot principal
├── backend_paypal.py         # API PayPal
├── database.py               # Gestor de BD
├── run_backend.py            # Launcher backend
├── verify_config.py          # Script de verificación
├── requirements.txt          # Dependencias
├── .gitignore                # Archivos ignorados
├── .env.example              # Plantilla de variables
├── README.md                 # Documentación principal
└── RAILWAY_CONFIG.md         # Guía de Railway

❌ NO SUBIR (ya están en .gitignore):
├── .env                      # ⚠️ CONTIENE SECRETOS
├── users.db                  # Base de datos
├── *.session                 # Sesiones Telethon
├── *.log                     # Logs del bot
├── __pycache__/              # Cache de Python
├── .venv/                    # Entorno virtual
├── .vscode/                  # Config de VSCode
└── .idea/                    # Config de PyCharm
```

## Antes de subir, verificar:

```bash
# 1. Verificar que .gitignore funcione
git status

# Si ves .env, users.db o .session en la lista, ¡DETENTE!
# Agrega esos archivos a .gitignore antes de continuar

# 2. Verificar que no haya secretos en el código
grep -r "TELEGRAM_BOT_TOKEN" --include="*.py" .
grep -r "PAYPAL_CLIENT_SECRET" --include="*.py" .

# Si encuentras tokens hardcodeados, ¡CÁMBIALOS por os.getenv()!

# 3. Commit inicial
git add .
git commit -m "Initial commit: Telegram bot with PayPal integration"

# 4. Push a GitHub
git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main
```

## Checklist Final ✅

Antes de subir a GitHub, verifica:

- [ ] `.env` está en `.gitignore`
- [ ] `users.db` está en `.gitignore`
- [ ] `*.session` está en `.gitignore`
- [ ] No hay tokens hardcodeados en el código
- [ ] `.env.example` tiene valores de ejemplo (NO reales)
- [ ] `README.md` está completo y actualizado
- [ ] `requirements.txt` tiene todas las dependencias
- [ ] Has eliminado `__pycache__/` y archivos `.pyc`
- [ ] Has eliminado `.venv/`
- [ ] Has eliminado archivos `.log`

## Comandos Git Útiles

```bash
# Ver qué archivos se van a subir
git status

# Ver diferencias antes de commit
git diff

# Deshacer cambios en un archivo
git checkout -- archivo.py

# Remover archivo del staging (antes de commit)
git reset HEAD archivo.py

# Remover archivo del repo (si ya se subió por error)
git rm --cached .env
git commit -m "Remove .env from repo"
git push
```

## ⚠️ Si subiste secretos por error

Si ya subiste `.env` o tokens al repo:

1. **Rota TODAS las credenciales inmediatamente:**
   - Genera nuevo Bot Token en @BotFather
   - Regenera Session String de Telethon
   - Cambia credenciales de PayPal

2. **Limpia el historial de Git:**
   ```bash
   # Opción 1: BFG Repo Cleaner (recomendado)
   java -jar bfg.jar --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   
   # Opción 2: git filter-branch (más complejo)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   git push --force --all
   ```

3. **Considera hacer el repo privado** hasta limpiar el historial

## Recursos

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [gitignore.io](https://www.toptal.com/developers/gitignore) - Genera .gitignore
