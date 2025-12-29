# 🚂 Deployment su Railway

Guida completa per il deployment del Bot Telegram + Dashboard su Railway.

## 📋 Prerequisiti

1. Account su [Railway](https://railway.app/)
2. Account su [GitHub](https://github.com/) (consigliato)
3. Token del bot Telegram da [@BotFather](https://t.me/BotFather)
4. Credenziali API Telegram da [my.telegram.org](https://my.telegram.org)

## 🚀 Passaggi per il Deployment

### Opzione 1: Deploy da GitHub (Consigliato)

#### 1. Prepara il repository

```bash
# Inizializza git se non l'hai già fatto
git init

# Aggiungi tutti i file
git add .

# Crea il primo commit
git commit -m "Initial commit - Bot + Dashboard"

# Collega al tuo repository GitHub
git remote add origin https://github.com/TUO_USERNAME/TUO_REPO.git

# Carica su GitHub
git push -u origin main
```

#### 2. Crea un nuovo progetto su Railway

1. Vai su [Railway Dashboard](https://railway.app/dashboard)
2. Clicca su **"New Project"**
3. Seleziona **"Deploy from GitHub repo"**
4. Autorizza Railway ad accedere al tuo GitHub
5. Seleziona il repository del bot

#### 3. Configura le variabili d'ambiente

Nel pannello Railway:

1. Clicca sul servizio deployato
2. Vai alla tab **"Variables"**
3. Aggiungi le seguenti variabili:

| Variabile | Descrizione |
|-----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot da @BotFather |
| `TELEGRAM_API_ID` | API ID da my.telegram.org |
| `TELEGRAM_API_HASH` | API Hash da my.telegram.org |
| `ENCRYPTION_KEY` | Chiave di crittografia (vedi sotto) |
| `ADMIN_TOKEN` | Password per il dashboard |
| `ADMIN_ID` | Il tuo Telegram User ID |
| `DASHBOARD_SECRET_KEY` | Chiave segreta per Flask |

**Per generare ENCRYPTION_KEY:**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Per generare DASHBOARD_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Opzione 2: Deploy diretto con Railway CLI

```bash
# Installa Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inizializza il progetto
railway init

# Configura le variabili
railway variables set TELEGRAM_BOT_TOKEN=your_token
railway variables set TELEGRAM_API_ID=your_api_id
railway variables set TELEGRAM_API_HASH=your_api_hash
railway variables set ENCRYPTION_KEY=your_encryption_key
railway variables set ADMIN_TOKEN=your_admin_password
railway variables set ADMIN_ID=your_user_id
railway variables set DASHBOARD_SECRET_KEY=your_secret_key

# Deploy
railway up
```

## 🌐 Accesso al Dashboard

Dopo il deployment:

1. Railway assegnerà automaticamente un dominio al tuo servizio
2. Trovi l'URL nella tab **"Settings"** > **"Domains"**
3. Accedi al dashboard su: `https://tuo-servizio.up.railway.app/`
4. Login con la password impostata in `ADMIN_TOKEN`

### Configura un dominio personalizzato (opzionale)

1. Vai su **"Settings"** > **"Domains"**
2. Clicca su **"Add Custom Domain"**
3. Inserisci il tuo dominio
4. Configura il DNS come indicato

## 📁 File della cartella

```
📦 bot-telegram/
├── 📄 railway.json          # Configurazione Railway
├── 📄 Procfile               # Comando di avvio
├── 📄 Dockerfile             # Build Docker
├── 📄 start.py               # Script di avvio unificato
├── 📄 requirements.txt       # Dipendenze Python
├── 📄 .env.example           # Template variabili
├── 📄 .gitignore             # File da ignorare
├── 📄 bot_with_paywall.py    # Bot Telegram principale
├── 📄 dashboard.py           # Dashboard Flask
├── 📄 database.py            # Gestione database
├── 📄 messages.py            # Messaggi multilingua
├── 📁 templates/             # Template HTML dashboard
│   ├── base.html
│   ├── dashboard.html
│   ├── users.html
│   ├── user_detail.html
│   ├── settings.html
│   ├── activity.html
│   └── login.html
└── 📁 static/                # File statici
```

## 🔧 Troubleshooting

### Il bot non si avvia

1. Controlla i log: `railway logs`
2. Verifica che tutte le variabili d'ambiente siano configurate
3. Controlla che il token del bot sia valido

### Il dashboard non risponde

1. Verifica il health check: vai su `https://tuo-servizio.up.railway.app/health`
2. Controlla che PORT non sia sovrascritto manualmente
3. Railway assegna automaticamente la porta

### Errori di connessione al database

Il database SQLite viene creato automaticamente. Se hai problemi:

1. Il file `users.db` viene creato nella directory di lavoro
2. I dati persistono finché non rideploy con una nuova build

### I dati si perdono dopo il redeploy

Railway non persiste i file locali. Per persistenza dei dati:

1. Usa Railway's Volume (pagamento richiesto)
2. Oppure migra a PostgreSQL (Railway lo offre gratuitamente)

## 📊 Monitoraggio

### Health Check

Il sistema include un endpoint di health check:

- URL: `/health`
- Ritorna: `{"status": "healthy", "database": "connected"}`

### Logs

Per vedere i log in tempo reale:

```bash
railway logs -f
```

O dal dashboard Railway nella tab **"Deployments"** > **"View Logs"**

## 💰 Costi

Railway offre:

- **Hobby Plan**: $5/mese con 500 ore di esecuzione
- **Pay as you go**: Paghi solo quello che usi

Per un bot Telegram leggero, il piano Hobby è più che sufficiente.

## 🔒 Sicurezza

### Checklist prima del deploy

- [ ] Cambiato `ADMIN_TOKEN` con una password sicura
- [ ] Cambiato `DASHBOARD_SECRET_KEY` con una chiave casuale
- [ ] Non committare il file `.env` (è in `.gitignore`)
- [ ] Verificare che `ADMIN_ID` sia il tuo ID Telegram

### Raccomandazioni

1. Usa password complesse (almeno 16 caratteri)
2. Attiva 2FA sul tuo account Railway
3. Limita l'accesso al repository GitHub

---

## 📞 Supporto

Per problemi con Railway, consulta la [documentazione ufficiale](https://docs.railway.app/).

Per problemi con il bot, controlla i log e verifica le variabili d'ambiente.
