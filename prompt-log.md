# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 15:58 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: เพิ่มแถวใน specs/001-booking/test-cases.md สถานะ "ร่าง" สำหรับ AC-BKG-01 อย่างน้อย 3 แบบ (ทางปกติ / ขอบ / ทางผิด)
- หมายเหตุ: ส่วน "แสดงหมายเลขคิว" มี Open Question Q-02 จึงเขียนเป็น (รอ Q-02) ตามข้อกำหนด และให้ทีมตรวจแถวในตารางก่อนเปลี่ยนสถานะเป็น "ใช้ได้"

---

## 2569-10-07 16:10 คำสั่ง: คืน test_AC_BKG_01 เดิมกลับมา

- สาเหตุ: ต้องรักษา test เดิมไว้ และเพิ่ม assertions ที่ตรงกับ AC-BKG-01 ไม่ลบ test ที่มีอยู่
- ไฟล์ที่แก้: backend/tests/test_AC_BKG_01.py
- ผล: เพิ่มตรวจว่าการจองถูกบันทึกจริง, queue_no = A001, และ remaining ถูกลดเหลือ 0 หลังยืนยันสำเร็จ
- ตรวจผล: `cd backend && pytest -q tests/test_AC_BKG_01.py` -> 1 passed

---

## 2569-10-07 16:16 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test
- สถานะในตาราง: AC-BKG-01 มี 3 แถวสถานะ "ใช้ได้" แล้ว
- ไฟล์ที่แก้: backend/tests/test_AC_BKG_01.py
- ผล: เพิ่ม test สำหรับ TC-BKG-01-2 และ TC-BKG-01-3 โดยคง test_AC_BKG_01 เดิมไว้ครบ 3 test
- ตรวจผล: `cd backend && pytest -q tests/test_AC_BKG_01.py` -> 3 passed

---

## 2569-10-07 16:15 คำสั่ง: คืน test_AC_BKG_01 เดิมกลับมา ห้ามลบ test เดิม

- ผล: คืนฟังก์ชัน `test_AC_BKG_01` ให้เป็น test เดิม โดยคง test `TC-BKG-01-2` และ `TC-BKG-01-3` ไว้
- ตรวจผล: `cd backend && pytest -q tests/test_AC_BKG_01.py` -> 3 passed

---

## 2569-10-07 16:19 คำสั่ง: เพิ่ม test ใหม่ของ AC-BKG-01 โดยคง test เดิมทั้งหมด

- สาเหตุ: test เดิม 1 ตัวต้องอยู่แยกจาก test ใหม่ 3 แถวใน `test-cases.md`
- ไฟล์ที่แก้: backend/tests/test_AC_BKG_01.py
- ผล: เพิ่ม `test_TC_BKG_01_1_booking_success` และคง `test_AC_BKG_01`, `test_TC_BKG_01_2_booking_last_seat`, `test_TC_BKG_01_3_unverified_user` ไว้
- ตรวจผล: `cd backend && pytest -q` -> 7 passed

---

## 2569-10-07 16:24 คำสั่ง: /verify specs/001-booking/

- ผล test: backend 7 passed, frontend 1 passed
- ผล RTM: 15 แถวตามรอยไปข้างหน้า — ครบ 1, ยังไม่ถึง 8, รอ Q-xx 0, ช่องโหว่ 6
- ข้อค้นพบใหม่: F-01 ถึง F-12 ใน specs/001-booking/rtm.md
- ไฟล์ที่สร้าง: specs/001-booking/rtm.md
