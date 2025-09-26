import { useState } from 'react';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const submit = async () => {
    if (!file) return;
    const form = new FormData();
    form.append('pdf', file);
    const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/upload-report', {
      method: 'POST',
      body: form
    });
    setResult(await res.json());
  };

  return (
    <main style={{ padding: 24 }}>
      <h2>Upload Credit Report</h2>
      <input type="file" accept="application/pdf" onChange={(e)=>setFile(e.target.files?.[0]||null)} />
      <button onClick={submit} style={{ marginLeft: 12 }}>Analyze</button>
      {result && (
        <pre style={{ marginTop: 24, background: '#f5f5f5', padding: 16 }}>
{JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  );
}
