import discord
from discord.ext import commands
import asyncio, sys, os, sqlite3, datetime, aiohttp, re, threading
from flask import Flask, render_template
from flask_cors import CORS

# --- CONFIGURACIÓN SEGURA ---
# El token debe configurarse en Render como variable de entorno: TOKEN_BOT
TOKEN_BOT = os.environ.get("TOKEN_BOT")
ID_SERVIDOR_FIJO = 1499438530223542402

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "NÚCLEO AFI V37.0 - ESTADO OPERATIVO"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

class AFIBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.target_guild_id = ID_SERVIDOR_FIJO

    async def on_ready(self):
        print(f"💠 NÚCLEO AFI V37.0 - ONLINE")
        self.loop.create_task(self.consola_asincrona())

    async def aioline(self, prompt=""):
        if prompt: print(prompt)
        sys.stdout.write("> "); sys.stdout.flush()
        return (await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)).strip()

    async def consola_asincrona(self):
        while True:
            await asyncio.sleep(0.2)
            print("\n  [G] EMBED [T] MUTE [P] REG PIN [L] LIST PINS [F] DM [A] MSG CANAL [U] LINK [M] MON [C] PURGE [K] KICK [B] BAN [S] AUDIT [R] REBOOT [Q] SALIR")
            op = (await self.aioline("\n Opción:")).upper()
            
            if op in ['F', 'A']:
                tipo = "DM" if op == 'F' else "CANAL"
                id_tr = await self.aioline(f"ID {tipo}:")
                msg = await self.aioline("Mensaje:")
                try:
                    obj = await (self.fetch_user(int(id_tr)) if op == 'F' else self.fetch_channel(int(id_tr)))
                    await obj.send(msg); print("✅ Enviado.")
                except Exception as e: print(f"❌ Error: {e}")
            elif op == 'G':
                cid = await self.aioline("ID Canal:"); tit = await self.aioline("Título:"); con = await self.aioline("Cuerpo:")
                try: await (await self.fetch_channel(int(cid))).send(embed=discord.Embed(title=tit, description=con, color=0x0000FF)); print("✅ Embed enviado.")
                except: print("❌ Error.")
            elif op == 'T':
                uid = await self.aioline("ID Usuario:"); t = await self.aioline("Tiempo (10s, 30m...):")
                try: 
                    m = await (self.get_guild(self.target_guild_id)).fetch_member(int(uid))
                    await m.timeout(datetime.timedelta(seconds=int(t[:-1])) if 's' in t else datetime.timedelta(minutes=int(t[:-1]))); print("✅ Muteado.")
                except: print("❌ Error.")
            elif op == 'C':
                cid = await self.aioline("ID Canal:"); n = await self.aioline("Cant:")
                try: await (await self.fetch_channel(int(cid))).purge(limit=int(n)); print("✅ Purga OK.")
                except: print("❌ Error.")
            elif op == 'K':
                uid = await self.aioline("ID Expulsión:")
                try: await (await (self.get_guild(self.target_guild_id)).fetch_member(int(uid))).kick(); print("✅ Expulsado.")
                except: print("❌ Error.")
            elif op == 'B':
                uid = await self.aioline("ID Baneo:")
                try: await (await (self.get_guild(self.target_guild_id)).fetch_member(int(uid))).ban(); print("✅ Baneado.")
                except: print("❌ Error.")
            elif op == 'S':
                g = self.get_guild(self.target_guild_id)
                print(f"📋 Servidor: {g.name} | Miembros: {g.member_count}")
            elif op == 'R': os.execv(sys.executable, ['python'] + sys.argv)
            elif op == 'Q': os._exit(0)

if __name__ == "__main__":
    if not TOKEN_BOT:
        print("❌ ERROR: TOKEN_BOT no configurado.")
        sys.exit(1)
    threading.Thread(target=run_web, daemon=True).start()
    AFIBot().run(TOKEN_BOT)
