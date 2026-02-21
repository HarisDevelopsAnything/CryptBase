import {useState} from 'react';

interface AffineResult {
    encrypted?: string;
    decrypted?: string;
}

const Affine = () => {
    const [text,setText] = useState("");
    const [key1, setKey1] = useState<number | ''>('');
    const [key2, setKey2] = useState<number | ''>('');
    const [mode, setMode] = useState<'enc'|'dec'>('enc');
    const [result, setResult] = useState<AffineResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    
    const handleSubmit = async (e : React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        setResult(null);
        try{
            const endpoint = mode === 'enc' ? 'encrypt' : 'decrypt';
            const response = await fetch(`http://localhost:5000/api/affine/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify({text, key1, key2})
            });
            if(!response.ok){
                const errorData = await response.json();
                setResult(null);
                setError(errorData.error || errorData.message || 'An error occurred');
            }
            else {
                const res = await response.json();
                setResult(res);
            }
        }
        catch(e){
            console.log(e);
        }
        finally {
            setLoading(false);
        }

    }
  return (
    <div>
        <h1>Affine cipher</h1>
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
          <label>Key 1:</label>
          <input
            type="number"
            value={key1}
            onChange={(e) => setKey1(e.target.value === '' ? '' : parseInt(e.target.value))}
            placeholder="Enter encryption key"
            required
          />
        </div>

        <div>
          <label>Key 2:</label>
          <input
            type="number"
            value={key2}
            onChange={(e) => setKey2(e.target.value === '' ? '' : parseInt(e.target.value))}
            placeholder="Enter encryption key"
            required
          />
        </div>

        <div>
          <label>
            <input
              type="radio"
              value="enc"
              checked={mode === 'enc'}
              onChange={() => setMode('enc')}
            />
            Encrypt
          </label>
          <label>
            <input
              type="radio"
              value="dec"
              checked={mode === 'dec'}
              onChange={() => setMode('dec')}
            />
            Decrypt
          </label>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : mode === 'enc' ? 'Encrypt' : 'Decrypt'}
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
        </div>
      )}
    </div>
  )
}

export default Affine