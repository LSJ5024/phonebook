import { useEffect, useState } from 'react'
import { supabase } from './lib/supabase'

export default function App() {
  const [contacts, setContacts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [form, setForm] = useState({ name: '', phone: '' })
  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({ name: '', phone: '' })

  useEffect(() => {
    fetchContacts()
  }, [])

  async function fetchContacts() {
    setLoading(true)
    setError(null)
    const { data, error } = await supabase
      .from('contacts')
      .select('*')
      .order('created_at', { ascending: false })
    if (error) setError('연락처를 불러오지 못했습니다.')
    else setContacts(data)
    setLoading(false)
  }

  async function addContact(e) {
    e.preventDefault()
    if (!form.name.trim() || !form.phone.trim()) return
    const { error } = await supabase.from('contacts').insert({
      name: form.name.trim(),
      phone: form.phone.trim(),
    })
    if (error) { setError('등록에 실패했습니다.'); return }
    setForm({ name: '', phone: '' })
    fetchContacts()
  }

  function startEdit(contact) {
    setEditingId(contact.id)
    setEditForm({ name: contact.name, phone: contact.phone })
  }

  async function saveEdit(id) {
    if (!editForm.name.trim() || !editForm.phone.trim()) return
    const { error } = await supabase
      .from('contacts')
      .update({ name: editForm.name.trim(), phone: editForm.phone.trim() })
      .eq('id', id)
    if (error) { setError('수정에 실패했습니다.'); return }
    setEditingId(null)
    fetchContacts()
  }

  async function deleteContact(id) {
    if (!window.confirm('삭제하시겠습니까?')) return
    const { error } = await supabase.from('contacts').delete().eq('id', id)
    if (error) { setError('삭제에 실패했습니다.'); return }
    fetchContacts()
  }

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">전화번호부</h1>

        {/* 등록 폼 */}
        <form onSubmit={addContact} className="flex gap-2 mb-8">
          <input
            type="text"
            placeholder="이름"
            value={form.name}
            onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            type="text"
            placeholder="전화번호"
            value={form.phone}
            onChange={e => setForm(f => ({ ...f, phone: e.target.value }))}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white px-5 py-2 rounded-lg font-medium transition-colors"
          >
            추가
          </button>
        </form>

        {/* 에러 메시지 */}
        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">{error}</p>
        )}

        {/* 목록 */}
        {loading ? (
          <p className="text-center text-gray-400 py-16">불러오는 중...</p>
        ) : contacts.length === 0 ? (
          <p className="text-center text-gray-400 py-16">등록된 연락처가 없습니다.</p>
        ) : (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-100 text-gray-600 text-sm">
                <tr>
                  <th className="text-left px-5 py-3">이름</th>
                  <th className="text-left px-5 py-3">전화번호</th>
                  <th className="px-5 py-3" />
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {contacts.map(contact => (
                  <tr key={contact.id} className="hover:bg-gray-50">
                    {editingId === contact.id ? (
                      <>
                        <td className="px-4 py-2">
                          <input
                            value={editForm.name}
                            onChange={e => setEditForm(f => ({ ...f, name: e.target.value }))}
                            className="border border-gray-300 rounded px-2 py-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                          />
                        </td>
                        <td className="px-4 py-2">
                          <input
                            value={editForm.phone}
                            onChange={e => setEditForm(f => ({ ...f, phone: e.target.value }))}
                            className="border border-gray-300 rounded px-2 py-1 w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                          />
                        </td>
                        <td className="px-4 py-2 text-right whitespace-nowrap">
                          <button
                            onClick={() => saveEdit(contact.id)}
                            className="text-blue-500 hover:text-blue-700 text-sm mr-3 font-medium"
                          >
                            저장
                          </button>
                          <button
                            onClick={() => setEditingId(null)}
                            className="text-gray-400 hover:text-gray-600 text-sm"
                          >
                            취소
                          </button>
                        </td>
                      </>
                    ) : (
                      <>
                        <td className="px-5 py-3 text-gray-800">{contact.name}</td>
                        <td className="px-5 py-3 text-gray-600">{contact.phone}</td>
                        <td className="px-5 py-3 text-right whitespace-nowrap">
                          <button
                            onClick={() => startEdit(contact)}
                            className="text-blue-500 hover:text-blue-700 text-sm mr-3 font-medium"
                          >
                            수정
                          </button>
                          <button
                            onClick={() => deleteContact(contact.id)}
                            className="text-red-400 hover:text-red-600 text-sm font-medium"
                          >
                            삭제
                          </button>
                        </td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
