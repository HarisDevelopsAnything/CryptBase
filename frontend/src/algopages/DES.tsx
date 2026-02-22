import { useState } from "react";
interface DESSteps {
    plaintext?: string;
    ciphertext?: string;
    key: string;
    p10: string;
    ls1: string;
    k1: string;
    ls2: string;
    k2: string;
    ip: string;
    fk1: string;
    sw: string;
    fk2: string;
}

interface DESResult {
    encrypted?: string;
    decrypted?: string;
    steps: DESSteps;
}

const DES = () => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    const [text, setText] = useState("");
    const [key, setKey] = useState("");
    const [p10, setP10] = useState("3 5 2 7 4 10 1 9 8 6");
    const [p8, setP8] = useState("6 3 7 4 8 5 10 9");
    const [ipv, setIpv] = useState("2 6 3 1 4 8 5 7");
    const [ipinv, setIpinv] = useState("4 1 3 5 7 2 8 6");
    const [epv, setEpv] = useState("4 1 2 3 2 3 4 1");
    const [p4, setP4] = useState("2 4 3 1");
    const [s0, setS0] = useState("1 0 3 2 3 2 1 0 0 2 1 3 3 1 3 2");
    const [s1, setS1] = useState("0 1 2 3 2 0 1 3 3 0 1 0 2 1 0 3");
    const [mode, setMode] = useState<'encrypt' | 'decrypt'>('encrypt');
    const [result, setResult] = useState<DESResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const endpoint = mode === 'encrypt' ? 'encrypt' : 'decrypt';
            const body = mode === 'encrypt'
                ? { plaintext: text, key, p10, p8, ip: ipv, ipinv, ep: epv, p4, s0, s1 }
                : { ciphertext: text, key, p10, p8, ip: ipv, ipinv, ep: epv, p4, s0, s1 };

            const response = await fetch(`${backendUrl}/api/des/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
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
            <h1>S-DES (Simplified DES)</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>{mode === 'encrypt' ? 'Plaintext (8 bits):' : 'Ciphertext (8 bits):'}</label>
                    <input
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="e.g. 10010111"
                        required
                    />
                </div>

                <div>
                    <label>Key (10 bits):</label>
                    <input
                        type="text"
                        value={key}
                        onChange={(e) => setKey(e.target.value)}
                        placeholder="e.g. 1010000010"
                        required
                    />
                </div>

                <div>
                    <label>P10:</label>
                    <input
                        type="text"
                        value={p10}
                        onChange={(e) => setP10(e.target.value)}
                        placeholder="3 5 2 7 4 10 1 9 8 6"
                    />
                </div>

                <div>
                    <label>P8:</label>
                    <input
                        type="text"
                        value={p8}
                        onChange={(e) => setP8(e.target.value)}
                        placeholder="6 3 7 4 8 5 10 9"
                    />
                </div>

                <div>
                    <label>IP:</label>
                    <input
                        type="text"
                        value={ipv}
                        onChange={(e) => setIpv(e.target.value)}
                        placeholder="2 6 3 1 4 8 5 7"
                    />
                </div>

                <div>
                    <label>IP⁻¹:</label>
                    <input
                        type="text"
                        value={ipinv}
                        onChange={(e) => setIpinv(e.target.value)}
                        placeholder="4 1 3 5 7 2 8 6"
                    />
                </div>

                <div>
                    <label>EP:</label>
                    <input
                        type="text"
                        value={epv}
                        onChange={(e) => setEpv(e.target.value)}
                        placeholder="4 1 2 3 2 3 4 1"
                    />
                </div>

                <div>
                    <label>P4:</label>
                    <input
                        type="text"
                        value={p4}
                        onChange={(e) => setP4(e.target.value)}
                        placeholder="2 4 3 1"
                    />
                </div>

                <div>
                    <label>S0 (4×4, row-major):</label>
                    <input
                        type="text"
                        value={s0}
                        onChange={(e) => setS0(e.target.value)}
                        placeholder="1 0 3 2 3 2 1 0 0 2 1 3 3 1 3 2"
                    />
                </div>

                <div>
                    <label>S1 (4×4, row-major):</label>
                    <input
                        type="text"
                        value={s1}
                        onChange={(e) => setS1(e.target.value)}
                        placeholder="0 1 2 3 2 0 1 3 3 0 1 0 2 1 0 3"
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
                <div>{error}</div>
            )}

            {result && (
                <div>
                    <div>
                        <h2>Result:</h2>
                        <p>{result.encrypted || result.decrypted}</p>
                    </div>

                    <div>
                        <h3>Steps:</h3>
                        <table>
                            <tbody>
                                <tr><td><strong>Key</strong></td><td>{result.steps.key}</td></tr>
                                <tr><td><strong>After P10</strong></td><td>{result.steps.p10}</td></tr>
                                <tr><td><strong>After LS-1</strong></td><td>{result.steps.ls1}</td></tr>
                                <tr><td><strong>K1</strong></td><td>{result.steps.k1}</td></tr>
                                <tr><td><strong>After LS-2</strong></td><td>{result.steps.ls2}</td></tr>
                                <tr><td><strong>K2</strong></td><td>{result.steps.k2}</td></tr>
                                <tr><td><strong>After IP</strong></td><td>{result.steps.ip}</td></tr>
                                <tr><td><strong>After fk (round 1)</strong></td><td>{result.steps.fk1}</td></tr>
                                <tr><td><strong>After SW</strong></td><td>{result.steps.sw}</td></tr>
                                <tr><td><strong>After fk (round 2)</strong></td><td>{result.steps.fk2}</td></tr>
                                <tr><td><strong>{mode === 'encrypt' ? 'Ciphertext' : 'Plaintext'}</strong></td>
                                    <td>{result.steps.ciphertext || result.steps.plaintext}</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    )
}

export default DES