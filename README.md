# FloodAlert — Professional Ocean Monitor

ระบบเว็บสำหรับติดตามสภาพอากาศและสถานการณ์ที่เกี่ยวข้องกับน้ำท่วม โดยเน้นการแสดงข้อมูลแบบ Dashboard ที่อ่านง่าย รองรับทั้งผู้ใช้งานทั่วไปและสมาชิกที่ต้องการติดตามพื้นที่ส่วนตัว

## ฟีเจอร์หลัก

- Dashboard สาธารณะ ดู Forecast ได้โดยไม่ต้อง Login
- การเพิ่ม/ลบพื้นที่ทำได้เฉพาะผู้ที่ Login แล้ว
- เลือกพื้นที่แบบ จังหวัด → อำเภอ/เขต → ตำบล/แขวง
- รองรับ 77 จังหวัด
- TMD NWP Forecast API ผ่าน Personal Access Token
- Forecast 24 ชั่วโมง พร้อมกราฟและ Timeline
- Summary สถานการณ์และระดับเฝ้าระวังจากสัญญาณ Forecast ของระบบ
- แผนที่ Leaflet พร้อม Marker และ Legend ตามระดับสถานะ
- Overview สำหรับสมาชิก พร้อมค้นหาและกรองพื้นที่
- ประกาศเตือนภัย TMD แยกจากระดับที่ระบบคำนวณ เพื่อไม่ให้สับสนกับประกาศทางการ
- Loading state และ Last Updated
- Scheduler สำหรับ refresh Forecast และ Warning
- UI แบบ responsive สำหรับ Desktop / Tablet / Mobile
- ธีม UI: Deep Navy + Ocean Teal + Sky Blue

## หลักการแสดงระดับเฝ้าระวัง

ระดับสีบน Dashboard เป็นตัวชี้วัดของแอปพลิเคชันจากข้อมูล Forecast เช่น ฝนและลม และมีไว้เพื่อช่วยติดตามสถานการณ์เท่านั้น ไม่ใช่ประกาศเตือนภัยอย่างเป็นทางการ

รายละเอียดการคำนวณอยู่ใน `app/weather_service.py` และสรุปการแสดงผลอยู่ใน `app/risk_service.py`

## TMD Forecast

Endpoint:

`https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/place`

ตั้งค่า `TMD_ACCESS_TOKEN` ใน `.env` โดยใช้ Token ใหม่ของโครงการ และไม่ควร commit ไฟล์ `.env` ขึ้น Git

## TMD Warning

ชุดนี้ใช้ URL ใน `TMD_WARNING_URL` สำหรับข้อมูลประกาศ WeatherWarningNews ที่ระบบรองรับอยู่

## Environment

คัดลอก `.env.example` เป็น `.env` แล้วกำหนดค่า Token และค่าการเชื่อมต่อที่ต้องใช้

## Run

```powershell
python -m pip install -r requirements.txt
python -m compileall app
python run.py
```

## API ที่สำคัญ

- `/` — หน้าหลักสาธารณะ
- `/dashboard` — Dashboard สาธารณะ / Dashboard พื้นที่ส่วนตัว
- `/api/provinces`
- `/api/locations/districts?province=...`
- `/api/locations/subdistricts?province=...&district=...`
- `/api/forecast?province=...&district=...&subdistrict=...`
- `/api/forecast/all`
- `/api/warnings`
- `/api/weather` — สำหรับข้อมูลอากาศที่ผูกกับบัญชีผู้ใช้

## โครงสร้างสำคัญ

```text
app/
├─ auth.py
├─ locations.py
├─ main.py
├─ models.py
├─ provinces.py
├─ risk_service.py
├─ scheduler.py
├─ tmd_api.py
├─ warning_service.py
├─ weather_service.py
├─ static/css/style.css
└─ templates/
   ├─ base.html
   ├─ index.html
   ├─ dashboard.html
   ├─ login.html
   └─ register.html
```
