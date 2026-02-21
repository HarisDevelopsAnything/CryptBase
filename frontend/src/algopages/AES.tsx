import { useState } from "react";

interface RoundStep {
    operation: string;
    state: string[];
    stateHex: string;
    roundKey?: string;
}

interface RoundDetail {
    round: number;
    operation?: string;
    state?: string[];
    stateHex?: string;
    roundKey?: string;
    steps?: RoundStep[];
    actualKeyRound?: number;
}

interface KeyStep {
    description?: string;
    words?: string[];
    i?: number;
    round?: number;
    rotWord?: string;
    subWord?: string;
    rcon?: string;
    afterRcon?: string;
    xor?: string;
}

interface AESSteps {
    keyExpansion: KeyStep[];
    roundKeys: string[];
    rounds: RoundDetail[];
}

interface AESResult {
    encrypted?: string;
    decrypted?: string;
    steps: AESSteps;
}

const AES = () => {
    const [text, setText] = useState("");
    const [key, setKey] = useState("");
    const [mode, setMode] = useState<'encrypt' | 'decrypt'>('encrypt');
    const [result, setResult] = useState<AESResult | null>(null);
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
                ? { plaintext: text, key }
                : { ciphertext: text, key };

            const response = await fetch(`http://localhost:5000/api/aes/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
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
            <h1>AES-128</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>{mode === 'encrypt' ? 'Plaintext (32 hex chars):' : 'Ciphertext (32 hex chars):'}</label>
                    <input
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="e.g. 00112233445566778899AABBCCDDEEFF"
                        required
                    />
                </div>

                <div>
                    <label>Key (32 hex chars):</label>
                    <input
                        type="text"
                        value={key}
                        onChange={(e) => setKey(e.target.value)}
                        placeholder="e.g. 000102030405060708090A0B0C0D0E0F"
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

            {result && (
                <div>
                    {/* Final result */}
                    <div>
                        <h2>Result:</h2>
                        <p>{result.encrypted || result.decrypted}</p>
                    </div>

                    {/* Round Keys */}
                    <div>
                        <h3>Round Keys:</h3>
                        <table>
                            <thead>
                                <tr><th>Round</th><th>Key (Hex)</th></tr>
                            </thead>
                            <tbody>
                                {result.steps.roundKeys.map((rk, i) => (
                                    <tr key={i}>
                                        <td>{i}</td>
                                        <td style={{ fontFamily: 'monospace' }}>{rk}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Key Expansion Details */}
                    <div>
                        <h3>Key Expansion Steps:</h3>
                        {result.steps.keyExpansion.map((step, i) => (
                            <div key={i} style={{ marginBottom: '8px', padding: '4px', borderBottom: '1px solid #ccc' }}>
                                {step.description && (
                                    <div>
                                        <strong>{step.description}:</strong>{' '}
                                        {step.words?.map((w, j) => (
                                            <span key={j} style={{ fontFamily: 'monospace', marginRight: '8px' }}>
                                                w[{j}]={w}
                                            </span>
                                        ))}
                                    </div>
                                )}
                                {step.round !== undefined && (
                                    <div>
                                        <strong>Round {step.round}:</strong>
                                        {step.rotWord && <div>RotWord: {step.rotWord}</div>}
                                        {step.subWord && <div>SubWord: {step.subWord}</div>}
                                        {step.rcon && <div>Rcon: {step.rcon}</div>}
                                        {step.afterRcon && <div>After Rcon XOR: {step.afterRcon}</div>}
                                        {step.xor && <div>{step.xor}</div>}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Round-by-round details */}
                    <div>
                        <h3>Round Details:</h3>
                        {result.steps.rounds.map((round, i) => (
                            <div key={i} style={{ marginBottom: '12px', padding: '8px', border: '1px solid #ddd' }}>
                                {/* Initial/AddRoundKey entries (round 0) */}
                                {round.operation && (
                                    <div>
                                        <strong>Round {round.round} — {round.operation}</strong>
                                        {round.roundKey && (
                                            <div>Round Key: <span style={{ fontFamily: 'monospace' }}>{round.roundKey}</span></div>
                                        )}
                                        <div>State: <span style={{ fontFamily: 'monospace' }}>{round.stateHex}</span></div>
                                        {round.state && (
                                            <div style={{ fontFamily: 'monospace', whiteSpace: 'pre' }}>
                                                {round.state.map((row, ri) => <div key={ri}>{row}</div>)}
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Detailed round steps (rounds 1-10) */}
                                {round.steps && (
                                    <div>
                                        <strong>
                                            Round {round.round}
                                            {round.actualKeyRound !== undefined ? ` (Key ${round.actualKeyRound})` : ''}
                                        </strong>
                                        <table>
                                            <thead>
                                                <tr><th>Operation</th><th>State (Hex)</th><th>State Matrix</th></tr>
                                            </thead>
                                            <tbody>
                                                {round.steps.map((step, si) => (
                                                    <tr key={si}>
                                                        <td>
                                                            {step.operation}
                                                            {step.roundKey && (
                                                                <div style={{ fontSize: '0.85em', fontFamily: 'monospace' }}>
                                                                    Key: {step.roundKey}
                                                                </div>
                                                            )}
                                                        </td>
                                                        <td style={{ fontFamily: 'monospace' }}>{step.stateHex}</td>
                                                        <td style={{ fontFamily: 'monospace', whiteSpace: 'pre' }}>
                                                            {step.state.map((row, ri) => <div key={ri}>{row}</div>)}
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default AES;
