# BJT DC Bias Web App

**ENG29 2121 · Lab 02 — First DC Bias Web App (2/2569)**
Checklist ก่อนเริ่มทำงานจริง + Workflow การ Commit ด้วย GitHub Desktop

> อัปเดตล่าสุด: 10 พฤศจิกายน 2569 (2026-11-10)

---

## 1) Checklist ก่อนเริ่มทำงานจริง (หัวข้อ 2.4 ของ Lab 02)

| # | รายการตรวจ | วิธีตรวจ | ผลที่ตรวจได้ | สถานะ |
|---|---|---|---|---|
| 1 | Git | `git --version` | git version 2.56.0.windows.4 | ✅ ผ่าน |
| 2 | GitHub | เปิด GitHub Desktop / Repo | GitHub Desktop 3.6.10 ล็อกอินบัญชี `pakkhaphon-dot` | ✅ ผ่าน |
| 3 | OpenCode Desktop | ส่งข้อความหา Agent ได้ | OpenCode v2.2.6 — session ใช้งานได้ | ✅ ผ่าน |
| 4 | Superpowers | Skills โหลดได้ | brainstorming, writing-plans, executing-plans, subagent-driven-development, systematic-debugging, test-driven-development โหลดครบ | ✅ ผ่าน |
| 5 | Python | `python --version` | Python 3.15.2 | ✅ ผ่าน |

### หมายเหตุการติดตั้ง Superpowers (ไว้อ้างอิงกรณีต้องซ่อมภายหลัง)

- ติดตั้งแบบ **local directory** ตามวิธี fallback สำหรับ Windows ใน `.opencode/INSTALL.md`
- ตำแหน่ง plugin: `C:\Users\b6828141\.config\opencode\superpowers`
- ไฟล์ config: `C:\Users\b6828141\.config\opencode\opencode.json`
  ```json
  {
    "plugins": [
      "C:\\Users\\b6828141\\.config\\opencode\\superpowers"
    ]
  }
  ```
- เหตุผล: สเปก `git+https://...` ติดตั้งไม่สำเร็จบน Windows build นี้ ("unknown git error") จึงใช้ path ตรงแทน — ผลลัพธ์เหมือนกันทุกประการ (skills ครบ, bootstrap ทำงาน)

### ข้อมูล Git ที่ใช้ทำ commit (GitHub Desktop ตั้งให้อัตโนมัติ)

- `user.name`: `pakkhaphon-dot`
- `user.email`: `pakkhaphon29@gmail.com`

---

## 2) การแบ่งบทบาทระหว่างทำ Lab

| ฝ่าย | หน้าที่ |
|---|---|
| **Agent** (OpenCode + Superpowers) | เขียน/แก้โค้ด, รัน automated tests, รัน Flask server ให้ดูผล, รายงานไฟล์ที่เปลี่ยนแปลงทุก task |
| **นักศึกษา** (คุณ) | ตรวจ diff ทุกไฟล์ใน GitHub Desktop → เขียน commit message → **Commit** → **Push** → เก็บ Commit SHA |

---

## 3) สร้าง Repository ครั้งแรก (ทำครั้งเดียว)

1. เปิด **GitHub Desktop**
2. เมนู **File → Add repository...** (`Ctrl+Shift+O`)
3. กดปุ่ม **Create a New Repository...**
4. ตั้งค่า:
   - **Name:** `BJT-DC-Bias-Web-App` (แนะนำ; หรือพิมพ์ `BJT DC Bias Web App` ก็ได้ GitHub จะจัดชื่อ URL เป็น `bjt-dc-bias-web-app` ให้เอง)
   - **Description:** `ENG29 2121 Lab 02 — BJT Common Emitter DC Bias Web App (Flask)`
   - **Local path:** โฟลเดอร์โปรเจกต์ เช่น
     `C:\Users\b6828141\Documents\Default Project\BJT DC Bias Web App`
   - ☑ **Initialize this repository with a README** (แนะนำ)
   - **Git ignore:** `None` — เราจะใส่ `.gitignore` สำหรับ Python เอง
   - **License:** `None`
5. กด **Create Repository**
6. กด **Publish repository** → เลือก **Private/Public** ตามข้อบังคับรายวิชา
   (ถ้า Private ต้องเพิ่มบัญชีผู้สอนเป็น collaborator ที่หน้า repo บนเว็บ: Settings → Collaborators)

---

## 4) Workflow การ Commit ทุก Task (ทำซ้ำทุกขั้นของ Lab)

1. รอ Agent แจ้งว่า **task เสร็จ + tests ผ่าน** (พร้อมผลรันจริง ไม่ใช่คำพูดลอย ๆ)
2. เปิด **GitHub Desktop** → เลือก repo ของ Lab 2
3. ที่แท็บ **Changes** ตรวจไฟล์ที่เปลี่ยน:
   - แถบสีเขียว = ไฟล์ใหม่ / เหลือง = แก้ไข / แดง = ลบ
   - **คลิกที่ชื่อไฟล์เพื่อดู diff ทีละบรรทัด** ก่อน commit ทุกครั้ง
4. กรอกข้อความ commit:
   - **Summary** (จำเป็น): สั้น กระชับ เช่น `Add dc_bias.py with validation and region warnings`
   - **Description** (ถ้าต้องการ): เช่น สมการที่ใช้, จำนวน tests ที่ผ่าน
5. กด **Commit to main**
6. กด **Push origin** (ส่งขึ้น GitHub)
7. เก็บ Commit SHA: คลิกขวาที่ commit ล่าสุดในประวัติ → **Copy SHA** (ใช้ส่ง Moodle ตอนจบ Lab)

### สิ่งที่ห้าม Commit

- `.venv/` · `__pycache__/` · `.env` · API keys — มี `.gitignore` กันไว้แล้ว แต่ควรเช็ก `Changes` ทุกครั้งก่อนกด Commit

---

## 5) แผน Commit ตามขั้นของ Lab (ภาพรวมเบื้องต้น)

| ลำดับ | เนื้อหา commit | เกณฑ์ตรวจรับที่เกี่ยวข้อง |
|---|---|---|
| 1 | README, `.gitignore`, checklist นี้, design doc | เตรียม repo |
| 2 | `dc_bias.py` + `tests/test_dc_bias.py` (คณิตศาสตร์วิศวกรรม) | A3, A6 |
| 3 | `app.py` + `templates/index.html` + `static/style.css` | A1, A2 |
| 4 | `tests/test_web.py` (Flask HTTP tests) | A6 |
| 5 | Validation + region warnings + ข้อความ error | A4, A5 |
| 6 | `docs/` (design-note, validation, reflection) | ส่ง Moodle |

---

## 6) สิ่งที่ต้องส่ง Moodle ตอนจบ Lab

- Repository URL
- Commit SHA ล่าสุด
- ภาพหน้าจอเว็บที่คำนวณ DC Bias สำเร็จ
- Test log (ผลรัน `python -m unittest discover -s tests -v`)
