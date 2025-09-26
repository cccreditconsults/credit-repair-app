import { useState, useMemo } from 'react';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState('');
  const [busy, setBusy] = useState(false);

  const apiBase = "https://credit-repair-app-production.up.railway.app"; // hardcode for now
// show it on screen:
<p>API: <code>{apiBase}</code></p>
  
  const submit = async () => {
    try {
      setStatus('');
      setResult(null);
      if (!apiBase) {
        setStatus('Error: NEXT_PUBLIC_API_BASE is not set.');
        console.error('Missing NEXT_PUBLIC_API_BASE');
        return;
      }
      if (!file) {
        setStatus('Please choose a PDF first.');
        return;
      }
      setBusy(true);
      const form = new FormData();
      form.append('pdf', file);
      console.log('Posting to:', apiBase + '/upload-report');
      const res = await fetch(apiBase + '/upload-report', { method: 'POST', body: form });
      if (!res.ok) {
        const text = await res.text();
        setStatus(`Request failed: ${res.status} ${res.statusText} — ${text}`);
        return;
      }
      const data = await res.json();
      setResult(data);
      setStatus('Done.');
    } catch (e) {
      console.error(e);
      setStatus('Unexpected error: ' + (e?.message || e));
    }
  };

  return (
    <main style={{ padding: 24, maxWidth: 800 }}>
      <h2>Upload Credit Report</h2>
      <p style={{ fontSize: 12, opacity: 0.7 }}>
        API: <code>{apiBase || '(not set)'}</code>
      </p>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button
        type="button"
        onClick={submit}
        disabled={busy}
        style={{ marginLeft: 12 }}
      >
        {busy ? 'Analyzing…' : 'Analyze'}
      </button>

      {status && <p style={{ marginTop: 12 }}>{status}</p>}

      {result && (
        <pre style={{ marginTop: 24, background: '#f5f5f5', padding: 16 }}>
{JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  );
}
