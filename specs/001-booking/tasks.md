# Tasks: จองคิวตรวจสุขภาพ (Booking)

- Feature: จองคิวตรวจสุขภาพ (Booking)
- Spec ID: SPEC-BKG-001
- อ้างอิง: `specs/001-booking/plan.md`
- วันที่: 2026-09-23

มีทั้งหมด 18 task แบ่งตามลำดับการพึ่งพาจากฐานข้อมูลไปยัง API หน้าจอ และการตรวจรับ
มี 4 task ที่ต้องรอคำตอบ `Q-02` เรื่องรูปแบบและวิธีออกหมายเลขคิว

## รายการ Task

### T-01 เตรียมการเชื่อมต่อฐานข้อมูลและ migration
- รองรับ: CON-TECH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/conftest.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: สร้าง engine จาก `DATABASE_URL` และ migration สามารถสร้างตารางบนฐานข้อมูลทดสอบได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้างโมเดลข้อมูลการจอง
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-04, IF-HIS-01, DOM-PDPA-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-05, T-07 และ T-10
- ไฟล์ที่แตะ: `backend/app/db/models.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/test_models.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: มีตาราง `slots`, `bookings` และ `audit_logs` โดย `bookings` ไม่มีคอลัมน์ `national_id`
- สถานะ: พร้อมทำ

### T-03 ตรวจผลยืนยันตัวตนก่อนเข้าถึงข้อมูล
- รองรับ: IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-05, T-07 และ T-12
- ไฟล์ที่แตะ: `backend/app/auth/idp.py`, `backend/app/main.py`, `backend/tests/test_idp.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: endpoint ที่แตะข้อมูลผู้รับบริการปฏิเสธคำขอที่ไม่มีผลยืนยันตัวตน และยอมรับคำขอที่ยืนยันแล้ว
- สถานะ: พร้อมทำ

### T-04 สร้างการค้นหา HN จาก HIS
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-12
- ไฟล์ที่แตะ: `backend/app/his/client.py`, `backend/app/booking/router.py`, `backend/tests/test_his_lookup.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `GET /patients/lookup` ส่งเลขบัตรไปยัง HIS และคืน HN โดยไม่บันทึกเลขบัตรประชาชนในข้อมูลการจอง
- สถานะ: พร้อมทำ

### T-05 แสดงช่วงเวลาว่างตามวันและแพ็กเกจ
- รองรับ: FR-BKG-01, FR-BKG-06, ASM-01, ASM-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-14
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/slots/router.py`, `backend/app/main.py`, `backend/tests/test_slots.py`
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: `GET /slots` คืนช่วงเวลาภายใน 30 วันพร้อมที่นั่งคงเหลือ และคำนวณผลใหม่เมื่อเปลี่ยนแพ็กเกจตามเขตเวลา Asia/Bangkok
- สถานะ: พร้อมทำ

### T-06 บันทึกการจองและตัดจำนวนที่นั่งแบบธุรกรรม
- รองรับ: FR-BKG-04, CON-TECH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-07, T-08 และ T-11
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/app/main.py`, `backend/tests/test_booking_transaction.py`
- ต้องทำหลัง: T-02, T-03, T-04
- เสร็จเมื่อ: การจองที่สำเร็จบันทึก HN และลด `remaining` ของช่วงเวลาที่เลือกโดยไม่เกิดการตัดที่นั่งเกินจำนวน
- สถานะ: พร้อมทำ

### T-07 ปฏิเสธการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02, ASM-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_02.py`
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: การจองซ้ำในวันเดียวกันถูกปฏิเสธและ response แสดงหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-08 เสนอช่วงเวลาว่างใกล้เคียงเมื่อช่วงเต็ม
- รองรับ: FR-BKG-03, ASM-02
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_03.py`
- ต้องทำหลัง: T-05, T-06
- เสร็จเมื่อ: การจองช่วงที่เต็มคืนสถานะ conflict พร้อม 3 ช่วงที่ใกล้ที่สุดจากวันเดียวกันและวันถัดไป และไม่สร้าง booking ใหม่
- สถานะ: พร้อมทำ

### T-09 วางงานแจ้งเตือนและส่งซ้ำแบบ asynchronous
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02, ASM-03
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/notify/queue.py`, `backend/app/booking/service.py`, `backend/tests/test_AC_BKG_04.py`
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: การจองไม่รอผลผู้ให้บริการแจ้งเตือน และกรณี error หรือ timeout มีงานส่งซ้ำกำหนดภายใน 5 นาทีโดยการจองยังคงอยู่
- สถานะ: พร้อมทำ

### T-10 บันทึก audit log เมื่อเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/app/audit/middleware.py`, `backend/app/main.py`, `backend/tests/test_AC_BKG_06.py`
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: การเปิดดูข้อมูลการจองสร้าง audit log ที่มีผู้เข้าถึง เวลา และ HN และรองรับการเก็บไม่น้อยกว่า 1 ปี
- สถานะ: พร้อมทำ

### T-11 กำหนดและออกหมายเลขคิว
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_01.py`
- ต้องทำหลัง: T-06, T-07
- เสร็จเมื่อ: ระบบออกและคืนหมายเลขคิวตามกติกาที่ทีมยืนยันในคำตอบ `Q-02` พร้อมบันทึกใน `bookings.queue_no`
- สถานะ: รอ Q-02

### T-12 รวม router และตรวจสัญญา API หลังบ้าน
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-05, IF-IDP-01, IF-HIS-01, IF-NOT-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-18
- ไฟล์ที่แตะ: `backend/app/main.py`, `backend/app/slots/router.py`, `backend/app/booking/router.py`, `backend/tests/test_api_contract.py`
- ต้องทำหลัง: T-04, T-05, T-08, T-09, T-10, T-11
- เสร็จเมื่อ: FastAPI รวม endpoint ตามสัญญาใน plan.md และทุก endpoint ตรวจสิทธิ์กับคืนรูปแบบ response ที่หน้าจอต้องใช้
- สถานะ: รอ Q-02

### T-13 บังคับใช้ TLS 1.2 ขึ้นไปในการรับส่งข้อมูล
- รองรับ: NFR-SEC-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานด้านความปลอดภัยของ T-18
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/main.py`, `backend/tests/test_security_config.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: การตั้งค่าการรับส่งข้อมูลปฏิเสธ TLS ต่ำกว่า 1.2 และมี test ตรวจค่าขั้นต่ำ TLS 1.2
- สถานะ: พร้อมทำ

### T-14 ทดสอบประสิทธิภาพการค้นหาช่วงเวลาว่าง
- รองรับ: NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/tests/test_AC_BKG_05.py`, `backend/app/slots/service.py`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: การทดสอบจำลองผู้ใช้พร้อมกัน 200 คนวัด p95 ของ `GET /slots` ได้ไม่เกิน 2 วินาที หรือบันทึกผลจริงบนเครื่องทดสอบตามข้อจำกัดของ Codespace
- สถานะ: พร้อมทำ

### T-15 สร้างหน้าจอเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-16 และ T-18
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/SlotPicker.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอเรียก API จำลอง แสดงวัน ช่วงเวลา ที่นั่งคงเหลือ และโหลดช่วงเวลาใหม่เมื่อเปลี่ยนแพ็กเกจ
- สถานะ: เสร็จ รอทีมตรวจ

### T-16 สร้างหน้ายืนยันและตัวเลือกช่วงเวลาใหม่
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/AC-BKG-03.test.jsx`
- ต้องทำหลัง: T-15
- เสร็จเมื่อ: API จำลองตอบ conflict แล้วหน้าจอแจ้ง "ช่วงเวลาเต็ม" และแสดงตัวเลือกที่ว่าง 3 รายการโดยไม่แสดงผลสำเร็จปลอม
- สถานะ: พร้อมทำ

### T-17 สร้างหน้าผลการจองและการแจ้งเตือนล้มเหลว
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `frontend/src/pages/BookingResult.jsx`, `frontend/src/App.jsx`, `frontend/src/__tests__/AC-BKG-04.test.jsx`
- ต้องทำหลัง: T-16
- เสร็จเมื่อ: หน้าจอแสดงหมายเลขคิวเมื่อการจองสำเร็จ แม้สถานะแจ้งเตือนเป็นส่งไม่สำเร็จ และแสดงข้อมูลจาก API จำลองตามสัญญา
- สถานะ: รอ Q-02

### T-18 ต่อหน้าจอกับ API จริงและตรวจ acceptance ครบชุด
- รองรับ: FR-BKG-01, FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-05, FR-BKG-06, NFR-USE-01
- ตรวจด้วย: AC-BKG-01, AC-BKG-02, AC-BKG-03, AC-BKG-04, AC-BKG-05, AC-BKG-06
- ไฟล์ที่แตะ: `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/`, `backend/tests/`, `frontend/src/__tests__/usability.test.jsx`
- ต้องทำหลัง: T-07, T-08, T-09, T-10, T-12, T-13, T-14, T-15, T-16, T-17
- เสร็จเมื่อ: หน้าจอเรียก API จริงผ่าน `/api` และผล test acceptance ทั้งหมดผ่าน พร้อมบันทึกผลทดสอบผู้ใช้ใหม่ 10 คนตาม NFR-USE-01
- สถานะ: รอ Q-02

## ตารางตรวจความครบ

### Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-11, T-18 |
| AC-BKG-02 | T-07, T-18 |
| AC-BKG-03 | T-08, T-16, T-18 |
| AC-BKG-04 | T-09, T-17, T-18 |
| AC-BKG-05 | T-14, T-18 |
| AC-BKG-06 | T-10, T-18 |

### Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-02, T-06 |
| DOM-PDPA-01 | T-02, T-10 |
| IF-IDP-01 | T-03, T-12 |
| IF-HIS-01 | T-02, T-04, T-12 |
| IF-NOT-01 | T-09, T-12 |

## สิ่งที่ยังไม่ทำ

- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร -> ถามเจ้าหน้าที่เวชระเบียน (ยังไม่ได้คำตอบ)
- T-11 รอคำตอบ Q-02 ก่อนสร้างวิธีออกและบันทึกหมายเลขคิว
- T-12, T-17 และ T-18 รอ T-11 และคำตอบ Q-02 ในส่วน response และการแสดงหมายเลขคิว
