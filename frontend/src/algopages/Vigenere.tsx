import { useState } from 'react';

interface VigenereResult {
    encrypted?: string;
    decrypted?: string;
}

const Vigenere = () => {
  const [mode,setMode] = useState<'encrypt'|'decrypt'>('encrypt');
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState('');
  const [key, setKey] = useState('');
  const [result, setResult] = useState<VigenereResult | null>(null);
  const [error,setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);
        setError('');

        try{
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            const response = await fetch(`${backendUrl}/api/vigenere/${mode}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text, key})
            });

            if(!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            const data = await response.json();
            setResult(data);
        }
        catch(err){
            setError(err instanceof Error ? err.message : 'An error occured');
        }
        finally {
            setLoading(false);
        }
    };
  return (
    <div>
        <h1>Vigenere cipher</h1>

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

        {error && <div>{error}</div>}
        {result && 
        <div>
            <h2>Result:</h2>
            <p>
                {result.encrypted || result.decrypted}
            </p>
        </div>
        }
    </div>
  )
}

export default Vigenere