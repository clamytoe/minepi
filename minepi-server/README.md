# MinePi

![Built with Docker](https://img.shields.io/badge/Built%20with-Docker-blue?logo=docker)
![Powered by Python](https://img.shields.io/badge/Powered%20by-Python-yellow?logo=python)
![Affiliate Supported](https://img.shields.io/badge/Affiliate-Supported-%23FF9900?logo=amazon)

A modular Raspberry Pi Minecraft server powered by Docker, playful automation, and magical parenting scripts.

Welcome to **MinePi**, your custom-coded gateway to running a modded Minecraft server powered by Raspberry Pi magic. This setup supports Fabric mods, rolling backups, MOTD rotation, playtime tracking, and even lore-based achievements—all orchestrated with shell scripts and rendered in magical dashboards.

Inspired by AI musings...

---

## 🛠 Requirements

| Component           | Recommended Specs                      |
|--------------------|----------------------------------------|
| Raspberry Pi       | Pi 5 (16GB+ RAM)                        |
| Power Supply       | 27W USB-C (5.1V/5A GaN)                |
| OS                 | Raspberry Pi OS 64-bit (Lite or GUI)  |
| Storage            | 256GB+ microSD or SSD via USB 3.0     |
| Starter Kit        | Starter Kit: [iRasptek Raspberry Pi 5 Bundle](https://www.amazon.com/dp/B0DSSQ8C53?tag=clamytoe-20) *(Affiliate Link – helps support MinePi!)* |

---

## 🚀 Setup Instructions

### 1. Install Docker

Run the official Docker install script:

```bash
curl https://get.docker.com | bash
sudo usermod -aG docker $USER
```

### 2. Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.39.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Clone the Repo

```bash
git clone https://github.com/clamytoe/minepi.git
cd minepi
```

### 4. Launch the Server

Edit and use `docker-compose.yml`, then run:

```bash
docker compose up -d
```

## 📂 Folder Structure

```bash
minepi/
├── docker-compose.yml
├── data/               # Server data and mods
├── logs/               # JSON log files and orchestration logs
├── backups/            # Timestamped world backups
└── scripts/            # Automation & dashboard scripts
```

## 📜 Features

- **Daily World Backups** Auto-scheduled via `cron`, with compressed `.zip` archives.

- **Player Login Tracker** Shell hook logs player join events to `player_logins.json`.

- **Earn-a-Minute Gamification** Tracks player activity for family reward integration.

- **Magical MOTD Rotator** Rotates themed messages in `server.properties`, configurable with cron.

- **Terminal Dashboard (TUI)** Glowing server stats in Matrix or parchment style using `dashboard.sh`.

- **HTML Lore Archive Dashboard** Unlockable playtime and MOTD lore entries using JSON and Python rendering.

## 🧠 Dashboard Goals

### ✨ Coming Soon

- Theme toggles (matrix/pixel/magic modes)

- Raspberry Pi vitals (CPU temp, load avg)

- Lore entry unlocks tied to playtime

- Badge progress and achievement icons

- Web-friendly frontend (dashboard.html)

## 🧪 Scripts

- `init_server.sh`: Setup server props, trigger backups, simulate logins

- `dashboard.sh`: TUI dashboard for terminal rendering

- `chart_playtime.sh`: Count earned minutes per player

- `motd_rotator.sh`: Randomized MOTD injector

- `orchestrate_magic.sh`: Master scheduler for MOTD + playtime

- `pi_status_probe.sh`: Collects Pi stats for dashboard overlays

- `gen_dashboard.py`: Renders HTML dashboard from JSON logs

## ⏰ Crontab Integration

Example (run orchestration every 3 hours):

```cron
0 */3 * * * /home/minecraft/scripts/orchestrate_magic.sh
```

## 🧙 Credits

Crafted by Martin Uribe, with a sprinkle of AI wizardry from Microsoft Copilot. Built for family fun, modularity, and delight.

## 📬 Contributing

This repo is a living spellbook—feel free to fork, star, and conjure up new features. Issues, feature ideas, and bug reports welcome.

```txt

---

Would you like me to push this into the repo as a PR, or format variants for parchment-style and matrix-mode themes? We can even embed the dashboard preview as an image or animation later. Let’s keep the magic flowing! 🪄📦
```

## 🪄 Support the Project

Help keep MinePi enchanting! Every click or contribution fuels future features, lore unlocks, and parental wizardry.

- 🛒 **Recommended Gear**: [iRasptek Raspberry Pi 5 Bundle](https://www.amazon.com/dp/B0DSSQ8C53?tag=clamytoe-20) (Affiliate link)

- 🌐 **GitHub Stars & Feedback**: Star this repo and suggest magical enhancements!

- 🍄 **Contribute Mods & Lore**: PRs welcome—especially for Cobblemon server extras or parchment dashboard tweaks.
