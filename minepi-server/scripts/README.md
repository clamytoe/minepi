# 🧠 Mod Sanity Check & Troubleshooting Guide

This guide helps you verify mod dependencies and troubleshoot common issues in Modrinth-based Minecraft modpacks—especially for setups like **Cobblemon Modpack [Fabric]**.

---

## 🔍 What This Script Does

- Scans your mod folder for installed .jar files
- Checks for missing dependencies based on known mod requirements
- Flags mismatches or missing .jars
- Outputs a clean summary for quick validation

---

### 📁 Default Mod Folder (Modrinth App)

I use Windows WSL so adjust the paths to suit your needs.

```bash
/mnt/c/Users/<your-username>/AppData/Roaming/ModrinthApp/profiles/<modpack-name>/mods
```

For Cobblemon:

```bash
/mnt/c/Users/<your-username>/AppData/Roaming/ModrinthApp/profiles/Cobblemon Modpack [Fabric] 1.0.0/mods
```

---

## ⚠️ Common Issues & Fixes

|Issue	|Cause	|Fix    |
|:------|:------|:------|
|Mod flagged as missing	|Filename mismatch	|Use fuzzy matching in script (e.g. `grep -i "yet.*config.*lib"`)|
|Mod shows as installed in Modrinth but not found	|`.jar` missing or download failed	|Manually verify `.jar` exists in `/mods` folder|
|Dependency installed in subfolder	|Modrinth nested structure	|Use recursive scan: `find "$MOD_DIR" -type f -name "*.jar"`|
|Version mismatch	|Mod updated but dependency not	|Check mod page for compatible versions|

---

## 🛠️ Script Usage

```bash
bash sanity-check-mods.sh
```

Example output:

```bash
🔍 Running sanity check on client mods...

⚠️  'make_bubbles_pop' is installed but missing required dependency: 'midnightlib'
✅ Sanity check complete.
```

---

## 🧩 Extending the Script

- Add server-side mod checks
- Validate mod versions against manifest
- Auto-download missing dependencies from Modrinth
- Generate compatibility reports

---

## 📚 Resources

- [Cobblemon Modpack on Modrinth](https://modrinth.com/modpack/cobblemon-fabric)
- [Modrinth CLI & API Docs](https://docs.modrinth.com/api/)