# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 16:24 | test: backend 7 ผ่าน, frontend 1 ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/router.py:get_slots`, `backend/app/slots/service.py:list_available_slots` | `test_AC_BKG_05` (ผ่าน; ตรวจ p95 แต่ไม่ตรวจครบ 30 วัน/ทุกส่วนของผลลัพธ์) | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05 พร้อมทำ, T-11 พร้อมทำ, T-12 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ, T-06 รอ Q-02 | `backend/app/booking/router.py:create_booking`, `backend/app/booking/service.py:create_booking` | `test_AC_BKG_01`, `test_TC_BKG_01_1_booking_success`, `test_TC_BKG_01_2_booking_last_seat` (ผ่าน; ยังไม่ตรวจคำขอส่งข้อความ และเลขคิวติด Q-02) | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ, T-10 พร้อมทำ | `backend/app/slots/router.py:get_slots`, `backend/app/slots/service.py:list_available_slots` | `test_AC_BKG_05` (ผ่าน; ไม่ใช่ test การเปลี่ยนแพ็กเกจบนหน้าจอ) | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/router.py:get_slots` | `test_AC_BKG_05` (ผ่าน; เรียกซ้ำแบบลำดับ ไม่ใช่ผู้ใช้พร้อมกัน 200 คน) | ช่องโหว่ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ยังไม่มี TLS 1.2+ ในแอปหรือการตั้งค่า deploy | ยังไม่มี | ช่องโหว่ |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC เฉพาะ | ไม่มี task | ยังไม่มี | ยังไม่มี | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC ตรง ๆ | T-01 เสร็จ | `backend/app/config.py`, `backend/app/db/session.py` | `test_T01_tables_created` (ผ่านบน SQLite ไม่ใช่ PostgreSQL) | ช่องโหว่ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 พร้อมทำ | มีเฉพาะโมเดล `AuditLog`; ยังไม่มี middleware | ยังไม่มี | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 | T-03 เสร็จ | `backend/app/auth/idp.py:get_verified_hn` | `test_TC_BKG_01_3_unverified_user` (ผ่าน) และ test จองสำเร็จ (ผ่าน) | ครบ |
| IF-HIS-01 | ไม่มี AC ตรง ๆ | T-01 เสร็จ, T-09 พร้อมทำ | โมเดลไม่มี `national_id` แต่ยังไม่มี HIS lookup | `test_T01_no_national_id` (ผ่าน) | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี notification queue | ยังไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/slots/router.py:get_slots` (`GET /slots`) | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ค้นช่วงว่างและกรองแพ็กเกจได้ แต่จำกัดล่วงหน้า 14 วันแทน 30 วัน และไม่มีหน้าจอที่ใช้งานจริง |
| `backend/app/slots/service.py:list_available_slots` | FR-BKG-01, FR-BKG-06 | ไม่ครบ | `DAYS_AHEAD = 14` ไม่ตรงข้อกำหนด 30 วัน |
| `backend/app/booking/router.py:create_booking` (`POST /bookings`) | FR-BKG-04, IF-IDP-01 | ไม่ครบ | ตรวจ token แบบจำลองและบันทึกได้ แต่ไม่มีการส่งคำขอ notification |
| `backend/app/booking/service.py:create_booking` | FR-BKG-04 | ไม่ตรงทั้งหมด | เงื่อนไข `remaining < 0` ทำให้ช่วงที่เหลือ 0 ที่ยังจองได้ และออกเลขคิวรูปแบบ A001 ทั้งที่ Q-02 ยังไม่มีคำตอบ |
| `backend/app/booking/service.py:next_queue_no` | FR-BKG-04, Q-02 | ไม่ตรง | กำหนดรูปแบบและวิธีนับเลขคิวเองก่อนตอบ Q-02 |
| `backend/app/booking/router.py:cancel_booking` (`DELETE /bookings/{booking_id}`) | UC-02 | ไม่ตรง | เป็นฟังก์ชันยกเลิกคิวที่ระบุเป็น Out of scope |
| `backend/app/booking/router.py:BookingRequest` | IF-HIS-01 | ไม่ตรง | รับ `national_id` ทั้งที่ constraint ระบุให้ค้นผ่าน HIS และไม่เก็บเลขบัตรประชาชน |
| `backend/app/booking/router.py:create_booking` logging | IF-HIS-01 | ไม่ตรง | log ค่า `national_id` ที่รับเข้ามาโดยไม่จำเป็น |
| `backend/app/config.py` และ `backend/app/db/session.py` | CON-TECH-01 | ไม่ครบ | ค่าเริ่มต้นเป็น SQLite และไม่มีการบังคับ PostgreSQL |
| `backend/app/db/models.py:AuditLog` | DOM-PDPA-01 | ไม่ครบ | มีตาราง แต่ไม่มีการเขียน audit log ทุกการเข้าถึงหรือการเก็บอย่างน้อย 1 ปี |
| `frontend/src/App.jsx` | FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05, FR-BKG-06 | ไม่ครบ | ยังเป็นโครงเริ่มต้น ไม่มีหน้าจอเลือก/ยืนยัน/ผลการจองตาม plan |
| `frontend/src/api/client.js:api` | FR-BKG-01, FR-BKG-03, FR-BKG-04 | ไม่ครบ | มี client แต่ไม่มี component เรียกใช้จริง และไม่มีการจัดการ 409 พร้อม 3 ตัวเลือก |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ตัวเลขไม่ตรง spec | `backend/app/slots/service.py:DAYS_AHEAD` | FR-BKG-01 | กำหนดช่วงค้นหา 14 วัน ทั้งที่ spec กำหนดภายใน 30 วัน | |
| F-02 | เดา Q-xx | `backend/app/booking/service.py:next_queue_no` | Q-02, FR-BKG-04 | กำหนดรูปแบบ `A001` และการนับเลขเอง ทั้งที่ Q-02 ยังไม่ได้คำตอบ | |
| F-03 | โค้ดไม่มี FR | `backend/app/booking/service.py:create_booking` | FR-BKG-03, FR-BKG-04 | ตรวจเต็มด้วย `remaining < 0`; ค่า 0 ยังถูกลดเป็น -1 และบันทึกการจองได้ | |
| F-04 | โค้ดไม่มี FR | `backend/app/booking/router.py:create_booking` | FR-BKG-04, IF-NOT-01 | ไม่สร้างหรือส่งคำขอข้อความยืนยันแบบ asynchronous | |
| F-05 | ละเมิด Constraint | `backend/app/booking/router.py:BookingRequest` และ logging | IF-HIS-01 | รับและเขียน `national_id` ลง log ทั้งที่ต้องใช้ HN ภายในและไม่เก็บเลขบัตรประชาชน | |
| F-06 | ของแถม / อยู่ใน Out of scope | `backend/app/booking/router.py:cancel_booking` | Out of scope UC-02 | เพิ่ม `DELETE /bookings/{id}` สำหรับยกเลิกคิว ซึ่งอยู่นอกขอบเขต | |
| F-07 | FR ไม่มี AC | spec/task/test | FR-BKG-06 | มี requirement การคำนวณใหม่เมื่อเปลี่ยนแพ็กเกจ แต่ไม่มี AC และไม่มี test ที่ตรวจพฤติกรรมนี้ | |
| F-08 | test อ่อน | `backend/tests/test_AC_BKG_01.py` | AC-BKG-01, FR-BKG-04 | test เดิมตรวจเพียง 201 และ test ใหม่ยังไม่ตรวจคำขอส่งข้อความ; ส่วนเลขคิวถูกเลื่อนไป Q-02 จึงตรวจ Then ได้ไม่ครบ | |
| F-09 | test อ่อน | `backend/tests/test_AC_BKG_05.py` | NFR-PERF-01 | เรียก 200 ครั้งแบบลำดับ ไม่จำลองผู้ใช้พร้อมกัน 200 คนตามข้อกำหนด | |
| F-10 | ละเมิด Constraint | `backend/app/config.py` | CON-TECH-01 | ค่าเริ่มต้นเป็น SQLite ไม่ใช่ PostgreSQL และไม่มีการบังคับค่า production ให้เป็น PostgreSQL | |
| F-11 | โค้ดไม่มี FR | `backend/app/db/models.py` / ไม่มี middleware | DOM-PDPA-01 | มีเพียง schema `audit_logs`; ยังไม่มีการบันทึกทุกครั้งและไม่มีหลักฐานเก็บอย่างน้อย 1 ปี | |
| F-12 | โค้ดไม่มี FR | `frontend/src/App.jsx` | FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05, FR-BKG-06 | หน้าจอจริงของฟีเจอร์ยังไม่ถูกสร้าง แม้ plan ระบุ component และ API client ไว้ | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
