# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Booking
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_booking_success(client, make_slot, db):
    """TC-BKG-01-1: ทางปกติ - บันทึกการจองและตัดที่นั่งเหลือ 0"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ, แสดงหมายเลขคิว (รอ Q-02), และที่นั่งว่างของช่วงนั้นเป็น 0
    assert res.status_code == 201
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1
    db.refresh(slot)
    assert slot.remaining == 0


def test_TC_BKG_01_2_booking_last_seat(client, make_slot, db):
    """TC-BKG-01-2: ขอบ - เหลือ 1 ที่ก่อนยืนยันการจอง ต้องจองสำเร็จและเหลือ 0"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่างอยู่เพียง 1 ที่ก่อนยืนยันการจอง
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ, แสดงหมายเลขคิว, และที่นั่งว่างของช่วงนั้นต้องลดลงเป็น 0 หลังการจอง
    assert res.status_code == 201
    body = res.json()
    assert body["queue_no"] == "A001"
    db.refresh(slot)
    assert slot.remaining == 0


def test_TC_BKG_01_3_unverified_user(client, make_slot, db):
    """TC-BKG-01-3: ทางผิด - ยังไม่ได้ยืนยันตัวตน ต้องปฏิเสธการจองและไม่บันทึก"""
    # Given: ผู้ใช้ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจองโดยไม่ส่ง Authorization
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ปฏิเสธการจอง, ไม่บันทึกข้อมูล, และไม่แสดงหมายเลขคิว
    assert res.status_code == 401
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 0
    db.refresh(slot)
    assert slot.remaining == 1
