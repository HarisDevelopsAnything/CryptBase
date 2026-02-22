import { useState } from 'react';

interface PlayfairResult {
  encrypted?: string;
  decrypted?: string;
  keyMatrix: string[][];
  digraphs: string[];
}

export default function PlayfairCipher() {
  const [text, setText] = useState('');
  const [key, setKey] = useState('');
  const [mode, setMode] = useState<'encrypt' | 'decrypt'>('encrypt');
  const [result, setResult] = useState<PlayfairResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL;
      const endpoint = mode === 'encrypt' ? 'encrypt' : 'decrypt';
      const response = await fetch(`${backendUrl}/api/playfair/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, key }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Request failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Playfair Cipher</h1>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>Text:</label>
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to encrypt/decrypt"
            required
          />
        </div>

        <div>
          <label>Key:</label>
          <input
            type="text"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="Enter encryption key"
            required
          />
        </div>

        <div>
          <label>
            <input
              type="radio"
              value="encrypt"
              checked={mode === 'encrypt'}
              onChange={(e) => setMode(e.target.value as 'encrypt')}
            />
            Encrypt
          </label>
          <label>
            <input
              type="radio"
              value="decrypt"
              checked={mode === 'decrypt'}
              onChange={(e) => setMode(e.target.value as 'decrypt')}
            />
            Decrypt
          </label>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : mode === 'encrypt' ? 'Encrypt' : 'Decrypt'}
        </button>
      </form>

      {error && (
        <div>
          {error}
        </div>
      )}

      {result && (
        <div>
          <div>
            <h2>Result:</h2>
            <p>
              {result.encrypted || result.decrypted}
            </p>
          </div>

          <div>
            <h3>Digraphs:</h3>
            <p>{result.digraphs.join(' ')}</p>
          </div>

          <div>
            <h3>Key Matrix:</h3>
            <div>
              {result.keyMatrix.map((row, _) =>
                <div>{row.join(' ')}</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}