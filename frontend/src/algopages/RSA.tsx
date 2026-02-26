import { useState } from 'react';

const RSA = () => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    const [text, setText] = useState<number | ''>('');
    const [p, setP] = useState<number | ''>('');
    const [q, setQ] = useState<number | ''>('');
    const [mode, setMode] = useState<'encrypt' | 'decrypt'>('encrypt');
    const [result, setResult] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const endpoint = mode === 'encrypt' ? 'encrypt' : 'decrypt';
            const body =
                mode === 'encrypt'
                    ? { plain: text, p, q }
                    : { cipher: text, p, q };

            const response = await fetch(`${backendUrl}/api/rsa/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            const data = await response.json();
            if (typeof data === 'number') {
                setResult(data);
            } else if (data.encrypted !== undefined) {
                setResult(data.encrypted);
            } else if (data.decrypted !== undefined) {
                setResult(data.decrypted);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const n = p !== '' && q !== '' ? p * q : null;
    const phi = p !== '' && q !== '' ? (p - 1) * (q - 1) : null;

    return (
        <div>
            <h1>RSA Encryption</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        {mode === 'encrypt'
                            ? 'Plaintext (integer):'
                            : 'Ciphertext (integer):'}
                    </label>
                    <input
                        type="number"
                        value={text}
                        onChange={(e) =>
                            setText(e.target.value === '' ? '' : parseInt(e.target.value))
                        }
                        placeholder={
                            mode === 'encrypt'
                                ? 'Enter plaintext number'
                                : 'Enter ciphertext number'
                        }
                        required
                    />
                </div>

                <div>
                    <label>Prime p:</label>
                    <input
                        type="number"
                        value={p}
                        onChange={(e) =>
                            setP(e.target.value === '' ? '' : parseInt(e.target.value))
                        }
                        placeholder="e.g. 7"
                        required
                    />
                </div>

                <div>
                    <label>Prime q:</label>
                    <input
                        type="number"
                        value={q}
                        onChange={(e) =>
                            setQ(e.target.value === '' ? '' : parseInt(e.target.value))
                        }
                        placeholder="e.g. 11"
                        required
                    />
                </div>

                <div>
                    <label>
                        <input
                            type="radio"
                            value="encrypt"
                            checked={mode === 'encrypt'}
                            onChange={() => setMode('encrypt')}
                        />
                        Encrypt
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="decrypt"
                            checked={mode === 'decrypt'}
                            onChange={() => setMode('decrypt')}
                        />
                        Decrypt
                    </label>
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : mode === 'encrypt' ? 'Encrypt' : 'Decrypt'}
                </button>
            </form>

            {error && <div style={{ color: 'red', marginTop: '1rem' }}>{error}</div>}

            {n !== null && phi !== null && (
                <div style={{ marginTop: '1rem' }}>
                    <h3>Key Parameters</h3>
                    <table>
                        <tbody>
                            <tr>
                                <td><strong>n = p × q</strong></td>
                                <td style={{ fontFamily: 'monospace' }}>{n}</td>
                            </tr>
                            <tr>
                                <td><strong>φ(n) = (p−1)(q−1)</strong></td>
                                <td style={{ fontFamily: 'monospace' }}>{phi}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            )}

            {result !== null && (
                <div style={{ marginTop: '1rem' }}>
                    <h2>Result</h2>
                    <p style={{ fontFamily: 'monospace', fontSize: '1.2rem' }}>
                        {mode === 'encrypt' ? 'Ciphertext: ' : 'Plaintext: '}
                        <strong>{result}</strong>
                    </p>
                </div>
            )}
        </div>
    );
};

export default RSA;