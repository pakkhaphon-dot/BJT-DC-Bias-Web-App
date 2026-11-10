# Design Note — BJT DC Bias Web App (Lab 02)

ENG29 2121 · 2/2569 · อนุมัติก่อนเริ่มเขียนโค้ด (Design Gate)

## Intent / เป้าหมาย

Web Application แรกของรายวิชา: คำนวณ **DC Operating Point** ของวงจรขยาย NPN Common Emitter แบบ **Voltage-Divider Bias** — นักศึกษากรอกค่าอุปกรณ์ใน Browser, **Python Backend (Flask)** คำนวณ, ผลลัพธ์แสดงกลับในหน้าเว็บพร้อมหน่วย เหตุผล: เรียนรู้โครงสร้าง Web App จริง (Frontend/Backend/Template/Static/HTTP) ที่จะต่อยอดเป็น Virtual Transistor Lab ใน Lab ถัดไป

## Goals

- รับอินพุต **VCC, R1, R2, RC, RE, β, VBE** ผ่านฟอร์ม
- คำนวณและแสดง **VB, VE, VC, VCE [V]**, **IC, IB, IE [mA]** ด้วย Python ล้วน (ห้าม hardcode ผลลัพธ์ใน HTML)
- Validation: ค่าไม่ใช่ตัวเลข/ขาดหาย, R ≤ 0, β ≤ 0, VCC ≤ 0 → ข้อความ error ชัดเจน หน้าเว็บไม่ล้ม
- Region warnings: **Cutoff** (VTH ≤ VBE) และ **Saturation** (VCE ต่ำกว่า ~0.2 V) → แจ้งว่าแบบจำลอง Forward-Active ใช้ไม่ได้
- Automated tests: ≥ 3 unit tests คณิตศาสตร์วิศวกรรม + ≥ 1 test ผ่าน Flask test client
- เปิดใช้ผ่าน `http://127.0.0.1:5000/` (Flask debug server, เครื่องพัฒนาเท่านั้น)

## Non-goals (นอกขอบเขา Lab นี้)

- ไม่ทำ AC / Bode Plot / Transient / Signal Generator / Overlay Animation
- ไม่ทำ Bias types อื่น (Fixed Bias, Emitter Bias — จะเพิ่มใน Lab 3)
- ไม่สร้าง SPICE/ngspice solver เอง
- ไม่ทำ UI ตกแต่งเต็มรูปแบบ — สะอาด อ่านง่าย มีหน่วยครบพอ

## Anti-goals (ถ้าเกิด = ถือว่าล้มเหลวแม้โปรแกรมรันได้)

- ผลลัพธ์ DC Bias เป็นค่าที่เขียนค้างใน HTML/JavaScript แทนการคำนวณใน Python
- เปิดใช้งานผ่าน `file://` แทน local web server
- ค่าที่อยู่นอก Active Region แสดงเป็นผลที่เชื่อถือได้โดยไม่มี warning

## แบบจำลองและสมการ (Forward-Active, β คงที่, VBE คงที่)

```
VTH = VCC · R2 / (R1 + R2)        RTH = R1·R2 / (R1 + R2)
IB  = (VTH − VBE) / (RTH + (β+1)·RE)
IC  = β·IB        IE = (β+1)·IB
VE  = IE·RE       VB = VE + VBE
VC  = VCC − IC·RC                 VCE = VC − VE
```

ข้อมูลทดสอบอ้างอิง: VCC=12 V, R1=100 kΩ, R2=22 kΩ, RC=2.2 kΩ, RE=1 kΩ, β=100, VBE=0.70 V (นักศึกษาคำนวณอิสระเทียบผล)

## หน่วย (Unit handling)

- ฟอร์มรับตัวต้านทานเป็น **kΩ** (ตามค่านิยมในห้อง Lab) → แปลงเป็น Ω ก่อนคำนวณ, VCC/VBE เป็น V, β ไม่มีหน่วย
- ทุกช่อง input และทุกผลลัพธ์กำกับหน่วยชัดเจน; กระแสแสดงเป็น mA

## Approach ที่เลือก (และทางที่ปัดตก)

**เลือก: Server-rendered form POST + Jinja2** — ฟอร์มส่ง `POST /calculate`, `app.py` เรียก `dc_bias.py`, render ผลกลับใน `templates/index.html`

- ปัดตก **AJAX/fetch + JSON API**: เพิ่มความซับซ้อน (JavaScript, สองรูปแบบ response) โดยเกณฑ์ A2 ตรวจผลใน HTML ที่ server render อยู่แล้ว
- ปัดตก **ไฟล์ HTML เดี่ยว**: ขัดกับโจทย์ multi-file + backend ของ Lab โดยตรง

## โครงสร้างไฟล์

```
BJT DC Bias Web App/
├── app.py                  # Flask routes: GET /, POST /calculate
├── dc_bias.py              # สมการ + validation + region check (ไม่รู้จัก HTTP/HTML)
├── templates/index.html    # ฟอร์ม + ผลลัพธ์ + error/warning (Jinja)
├── static/style.css        # หน้าตาเว็บ
├── tests/test_dc_bias.py   # unit tests คณิตวิศวกรรม
├── tests/test_web.py       # Flask test client (GET /, POST /calculate, validation)
├── requirements.txt        # flask
├── README.md               # วิธี setup/run/test
├── AGENTS.md               # แนวปฏิบัติ AI ของโปรเจกต์
└── docs/                   # design-note (ไฟล์นี้), validation, reflection
```

หน้าเว็บภาษา**อังกฤษล้วน** (ศัพท์วิศวกรรมสากล ต่อเนื่องกับ Lab ถัดไป)

## Validation & Warnings (เกณฑ์ A4–A5)

| กรณี | พฤติกรรม |
|---|---|
| ช่องว่าง / ไม่ใช่ตัวเลข / ≤ 0 (R, β, VCC) | ข้อความ error ระบุช่องที่ผิด คงค่าเดิมในฟอร์ม |
| VTH ≤ VBE | Warning **Cutoff** — แบบจำลองใช้ไม่ได้ |
| VCE < 0.2 V | Warning **Saturation** — VCE ต่ำเกิน Active Region |
| ค่าปกติใน Active Region | แสดงผล + region = Forward-Active |

## สิ่งที่เหลือให้ผู้สร้างตัดสินใจเอง (builder's call)

- การจัดวาง/สีของหน้าเว็บ (สะอาด, มีหน่วยครบ — ไม่ต้องเหมือนภาพตัวอย่างทุกพิกเซล)
- ตัวเลขทศนิยมที่แสดง (ปัดให้อ่านง่าย เช่น 3 ตำแหน่ง)
- VCE(sat) เกณฑ์เตือนใช้ 0.2 V (ค่าตำแหน่งปกติของ Si BJT)
