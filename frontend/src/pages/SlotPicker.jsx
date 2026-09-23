import { useEffect, useState } from 'react'

const packages = [
  { code: 'general', label: 'ตรวจสุขภาพทั่วไป' },
  { code: 'executive', label: 'ตรวจสุขภาพผู้บริหาร' },
]

function todayAsInputValue() {
  return new Date().toISOString().slice(0, 10)
}

function formatSlotTime(startTime) {
  return String(startTime).slice(0, 5)
}

// รองรับ FR-BKG-01 และ FR-BKG-06 ด้วยการเลือกแพ็กเกจและโหลดช่วงเวลาที่ว่างใหม่
export default function SlotPicker({ client }) {
  const [packageCode, setPackageCode] = useState(packages[0].code)
  const [dateFrom, setDateFrom] = useState(todayAsInputValue)
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')

    client
      .getSlots({ dateFrom, packageCode })
      .then((response) => {
        if (active) setSlots(Array.isArray(response) ? response : response.slots ?? [])
      })
      .catch(() => {
        if (active) setError('ไม่สามารถโหลดช่วงเวลาที่ว่างได้')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [client, dateFrom, packageCode])

  return (
    <section className="mt-8 rounded-2xl border border-teal-100 bg-white p-6 shadow-sm" aria-labelledby="slot-picker-title">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">FR-BKG-01 / FR-BKG-06</p>
          <h2 id="slot-picker-title" className="mt-1 text-2xl font-bold text-slate-900">
            เลือกแพ็กเกจและช่วงเวลาตรวจ
          </h2>
        </div>
        <label className="flex min-w-52 flex-col gap-1 text-sm font-medium text-slate-700">
          แพ็กเกจ
          <select
            aria-label="แพ็กเกจ"
            className="rounded-lg border border-slate-300 bg-white px-3 py-2"
            value={packageCode}
            onChange={(event) => setPackageCode(event.target.value)}
          >
            {packages.map((item) => (
              <option key={item.code} value={item.code}>
                {item.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      <label className="mt-6 flex max-w-xs flex-col gap-1 text-sm font-medium text-slate-700">
        เริ่มค้นหาตั้งแต่วันที่
        <input
          aria-label="วันที่เริ่มค้นหา"
          className="rounded-lg border border-slate-300 px-3 py-2"
          type="date"
          value={dateFrom}
          onChange={(event) => setDateFrom(event.target.value)}
        />
      </label>

      <div className="mt-6" aria-live="polite">
        {loading && <p className="text-slate-600">กำลังโหลดช่วงเวลาที่ว่าง...</p>}
        {error && <p className="text-red-700">{error}</p>}
        {!loading && !error && slots.length === 0 && (
          <p className="text-slate-600">ยังไม่มีช่วงเวลาที่ว่างสำหรับเงื่อนไขนี้</p>
        )}
        {!loading && !error && slots.length > 0 && (
          <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3" aria-label="ช่วงเวลาที่ว่าง">
            {slots.map((slot) => (
              <li key={slot.id} className="rounded-xl border border-slate-200 p-4">
                <p className="text-lg font-bold text-slate-900">{formatSlotTime(slot.start_time)}</p>
                <p className="mt-1 text-sm text-slate-600">วันที่ {slot.slot_date}</p>
                <p className="mt-3 text-sm font-semibold text-teal-700">
                  เหลือ {slot.remaining} ที่นั่ง
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
