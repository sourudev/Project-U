
# บอทอัปโหลดไฟล์ Discord แบบไม่ระบุตัวตน

<p align="center">

<img src="https://0x0.st/H9Dx.png" alt="โลโก้โฟลเดอร์ไฟล์">

</p>

บอทตัวนี้สร้างขึ้นเพื่อให้อัปโหลดขึ้นDiscordแบบไม่ระบุตัวตนสามารถแชร์ไฟล์ได้ ด้วยLibraryของ Discord.py และ aiohttp

## การติดตั้ง

1. โคลนGithubนี้:

```
git clone https://github.com/sourudev/Project-U.git
```

2. ติดตั้งdependencies:

```
pip install -r requirements.txt
```

3. สร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจคและเพิ่มToken Discord :

```
DISCORD_TOKEN=<Token Discord ของบอท>
```

4. Run บอท:

```
python bot.py
```

## วิธีใช้

บอทถูกเรียกใช้โดยคำสั่งแบบSlash command(เป็นCommandแบบ `/` ) `/upload` และการแนบไฟล์
บอทจะตอบกลับด้วยข้อความที่บอกว่ากำลังประมวลผลไฟล์และจะอัปโหลดไฟล์ไปยัง Anonfiles  เมื่ออัปโหลดเสร็จสมบูรณ์แล้ว บอทจะโพสต์ข้อความพร้อม URL ของไฟล์และข้อมูลอื่น ๆ

[![Add me!](https://0x0.st/H9D3.png)](https://discord.com/oauth2/authorize?client_id=1145607131630940201&scope=bot+applications.commands&permissions=0)


