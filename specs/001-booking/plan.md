# แผนการพัฒนาฟีเจอร์: จองคิวตรวจสุขภาพ (Booking)

## 1. สรุปแนวทาง
ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ เพื่อจองคิวและรับหมายเลขคิวแบบอัตโนมัติ โดยระบบจะแสดงช่วงเวลาว่างพร้อมจำนวนที่นั่งที่เหลือ และป้องกันการจองซ้ำในวันเดียวกันตามกฎ FR-BKG-02 และ AC-BKG-02 ระบบจะบันทึกการจอง เก็บ audit log และส่งคำขอแจ้งเตือนแบบ asynchronous ตาม IF-NOT-01 และ DOM-PDPA-01 แนวทางพัฒนาจะแยกเป็น 3 ชั้นหลัก คือ หน้าจอจองคิว, API จัดการช่วงเวลาและการจอง, และบริการส่งข้อความ/คิว retry เพื่อให้ตอบสนองต่อ FR-BKG-01 ถึง FR-BKG-06 และ NFR-PERF-01

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| MySQL | CON-TECH-01 | ใช้เก็บข้อมูลการจอง ช่วงเวลา audit log และคิวส่งข้อความ |
| React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับหน้าเลือกแพ็กเกจ วัน และช่วงเวลาว่าง |
| Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับ API คำนวณช่วงว่าง จัดการการจอง และเรียกบริการส่งข้อความ |
| Redis หรือ queue backend ภายในระบบ | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับคิว retry ของข้อความยืนยันตาม NFR-REL-02 และ FR-BKG-05 |
| TLS 1.2+ | NFR-SEC-01 | ใช้สำหรับการรับส่งข้อมูลที่มีความละเอียดด้านข้อมูลสุขภาพ |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ FR / Constraint |
|---|---|---|
| UserProfile | hn, verified_at, status | รองรับ IF-IDP-01 และ IF-HIS-01; ไม่เก็บเลขบัตรประชาชนในตารางการจอง |
| Package | package_id, name, description, active_flag | รองรับ FR-BKG-01, FR-BKG-06 |
| TimeSlot | slot_id, date, start_time, end_time, package_id, capacity_total, capacity_remaining, status | รองรับ FR-BKG-01, FR-BKG-04, FR-BKG-06; ใช้คำนวณช่วงเวลาว่างและคงเหลือ |
| Booking | booking_id, hn, package_id, booking_date, slot_id, queue_no, status, created_at, confirmed_at | รองรับ FR-BKG-02, FR-BKG-04, FR-BKG-05; กันการจองซ้ำในวันเดียวกัน |
| NotificationQueue | message_id, booking_id, channel, payload, status, attempts, next_retry_at, created_at | รองรับ FR-BKG-05, NFR-REL-02, IF-NOT-01 |
| AuditLog | audit_id, actor_user, access_time, hn, action, resource_type | รองรับ DOM-PDPA-01, เก็บไม่น้อยกว่า 1 ปี |

หมายเหตุ: ตาราง Booking จะเก็บ HN เท่านั้นตาม IF-HIS-01 และจะไม่เก็บเลขบัตรประชาชนในตารางการจอง

## 4. API / หน้าจอ

### หน้าจอ
- หน้ารายการแพ็กเกจ: เลือกแพ็กเกจ ระบุผู้ใช้อยู่ใน state ที่ยืนยันตัวตนแล้ว; รองรับ FR-BKG-01, FR-BKG-06
- หน้ารายการช่วงเวลา: แสดงวันและช่วงเวลาว่างภายใน 30 วัน พร้อมจำนวนที่นั่งคงเหลือ; รองรับ FR-BKG-01
- หน้าสรุปการจอง: แสดงหมายเลขคิวและสถานะข้อความยืนยัน; รองรับ FR-BKG-04, FR-BKG-05
- หน้าข้อความแจ้งเตือนเต็ม: แสดง “ช่วงเวลาเต็ม” และ 3 ตัวเลือกที่ใกล้ที่สุด; รองรับ FR-BKG-03

### Endpoint
- GET /api/v1/slots?package_id=&date_from=&date_to= : คืนรายชื่อช่วงเวลาและจำนวนที่นั่งคงเหลือ; รองรับ FR-BKG-01
- GET /api/v1/slots/available?package_id=&date= : คำนวณช่วงเวลาว่างตามแพ็กเกจที่เลือก; รองรับ FR-BKG-06
- POST /api/v1/bookings/check-duplicate : ตรวจว่าผู้รับบริการมีคิวที่ยังไม่สิ้นสุดหรือยังไม่ได้เช็คอินในวันเดียวกันหรือไม่; รองรับ FR-BKG-02
- POST /api/v1/bookings : สร้างการจองใหม่, ตัดคงเหลือ, สร้างหมายเลขคิว, ส่งคำขอส่งข้อความ; รองรับ FR-BKG-04
- POST /api/v1/bookings/slot-full : ดำเนินกรณีช่วงเวลาที่เลือกเต็มพร้อมเสนอ 3 ตัวเลือก; รองรับ FR-BKG-03
- POST /api/v1/notifications/retry : ดำเนินการส่งซ้ำข้อความที่ล้มเหลวภายใน 5 นาที; รองรับ FR-BKG-05, NFR-REL-02
- GET /api/v1/audit-logs/{hn} : ดึง audit log สำหรับตรวจสอบ; รองรับ DOM-PDPA-01

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | MySQL เป็น datastore หลักสำหรับ Booking, TimeSlot, NotificationQueue และ AuditLog | ใช้แล้ว |
| DOM-PDPA-01 | AuditLog ถูกออกแบบให้มีผู้เข้าถึง เวลา และ HN พร้อมจัดเก็บไม่น้อยกว่า 1 ปี | ใช้แล้ว |
| IF-IDP-01 | UserProfile/verified state ถูกใช้เป็น precondition ก่อนเข้าถึงข้อมูลผู้รับบริการ | ใช้แล้ว |
| IF-HIS-01 | Booking และ UserProfile ใช้ HN เป็น reference key และไม่มีฟิลด์เลขบัตรประชาชนในตารางการจอง | ใช้แล้ว |
| IF-NOT-01 | NotificationQueue และ API ส่งข้อความทำงานแบบ asynchronous โดยไม่ทำให้การจองหยุดรอ | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_booking_success_updates_capacity | ตั้งค่า slot 09.00 มีที่ว่าง 1 ที่ แล้วยืนยันการจอง ตรวจว่า booking ถูกบันทึก หมายเลขคิวแสดงผล และ capacity_remaining = 0 |
| AC-BKG-02 | test_AC_BKG_02_duplicate_booking_same_day_rejected | ตั้งค่าให้ผู้ใช้มีคิวที่ยังไม่สิ้นสุดการตรวจในวันเดียวกัน แล้วลองจองใหม่ ตรวจว่า request ถูกปฏิเสธและแสดงหมายเลขคิวเดิม |
| AC-BKG-03 | test_AC_BKG_03_slot_full_shows_three_alternatives | ตั้งค่า slot ถูกจองเต็มโดยผู้ใช้คนอื่น แล้วกดยืนยัน ตรวจว่าระบบแสดง “ช่วงเวลาเต็ม” และ 3 ตัวเลือกที่ใกล้ที่สุด พร้อมไม่สร้าง booking ซ้อน |
| AC-BKG-04 | test_AC_BKG_04_notification_retry_after_failure | จำลอง SMS/LINE error หรือ timeout แล้วทำการยืนยัน ตรวจว่าการจองยังถูกบันทึกและมี record ใน NotificationQueue พร้อม retry ภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05_slot_lookup_perf_under_200_users | จำลอง ผู้ใช้พร้อมกัน 200 คน เรียก API แสดงช่วงเวลาว่าง ตรวจว่า p95 <= 2 วินาที |
| AC-BKG-06 | test_AC_BKG_06_audit_log_created_on_access | จำลองการเข้าถึงข้อมูลการจองแล้วตรวจว่า audit log มี actor_user, access_time, hn และบันทึกสมบูรณ์ |

## 7. ลำดับงาน

1. สร้าง schema MySQL สำหรับ TimeSlot, Booking, NotificationQueue และ AuditLog; รองรับ CON-TECH-01, DOM-PDPA-01, FR-BKG-01, FR-BKG-04
2. สร้าง API สำหรับดึงช่วงเวลาว่างและจำนวนที่นั่งคงเหลือ; รองรับ FR-BKG-01, NFR-PERF-01
3. สร้างชุดตรวจสอบคิวซ้ำในวันเดียวกันและ API ปฏิเสธการจอง; รองรับ FR-BKG-02, AC-BKG-02
4. สร้าง flow จองพร้อมสร้างหมายเลขคิวและลดจำนวนที่นั่ง; รองรับ FR-BKG-04, AC-BKG-01
5. สร้าง flow เมื่อ slot เต็ม โชว์ 3 ตัวเลือกที่ใกล้ที่สุดและป้องกัน race condition; รองรับ FR-BKG-03, AC-BKG-03
6. สร้าง queue สำหรับส่งข้อความยืนยันแบบ asynchronous และ retry ภายใน 5 นาที; รองรับ FR-BKG-05, NFR-REL-02, AC-BKG-04
7. สร้าง audit log เมื่อมีการเข้าถึงข้อมูลสุขภาพ; รองรับ DOM-PDPA-01, AC-BKG-06
8. ทดสอบ end-to-end ตาม AC ทั้ง 6 ข้อ และปรับประสิทธิภาพ/ความปลอดภัยตาม NFR-PERF-01, NFR-SEC-01, NFR-USE-01

## 8. สิ่งที่ยังไม่ทำ
- ไม่มี Open Questions ใน spec v2 ปัจจุบัน เนื่องจากข้อที่เคยกำกวมถูกตัดสินใจเป็น Assumptions แล้ว
- ส่วนที่เกี่ยวข้องกับข้อกำหนดเหล่านี้จะยังไม่สร้างจนกว่าจะได้รับข้อมูลเพิ่มเติมจากทีมหากมีการเปลี่ยนคำตัดสินในอนาคต

