import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import SlotPicker from '../pages/SlotPicker.jsx'

function createMockClient() {
  return {
    getSlots: vi.fn(({ packageCode }) =>
      Promise.resolve([
        {
          id: packageCode,
          slot_date: '2026-09-24',
          start_time: '09:00:00',
          remaining: packageCode === 'general' ? 4 : 2,
        },
      ]),
    ),
  }
}

test('แสดงช่วงเวลาและจำนวนที่นั่งคงเหลือจาก API จำลอง', async () => {
  const client = createMockClient()

  render(<SlotPicker client={client} />)

  expect(await screen.findByText('09:00')).toBeTruthy()
  expect(screen.getByText('เหลือ 4 ที่นั่ง')).toBeTruthy()
})

test('เปลี่ยนแพ็กเกจแล้วโหลดช่วงเวลาใหม่', async () => {
  const client = createMockClient()

  render(<SlotPicker client={client} />)
  await screen.findByText('เหลือ 4 ที่นั่ง')

  fireEvent.change(screen.getByLabelText('แพ็กเกจ'), { target: { value: 'executive' } })

  await waitFor(() => expect(screen.getByText('เหลือ 2 ที่นั่ง')).toBeTruthy())
  expect(client.getSlots).toHaveBeenLastCalledWith(
    expect.objectContaining({ packageCode: 'executive' }),
  )
})
