import { api } from './api/client.js'
import SlotPicker from './pages/SlotPicker.jsx'

// รองรับ FR-BKG-01 และ FR-BKG-06 ด้วยหน้าจอเลือกช่วงเวลาหลักของฟีเจอร์
export default function App() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl bg-slate-50 p-6 sm:p-10">
      <h1 className="text-2xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>
      <SlotPicker client={api} />
    </main>
  )
}
