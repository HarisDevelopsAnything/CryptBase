import { useState } from 'react';

interface Step {
    step: number;
    description: string;
    calculation: string;
    result: string;
}

interface GCDResult {
    gcd: number;
    steps: Step[];
}

const GCD = () => {
    const [numA, setNumA] = useState<number>(0);
    const [numB, setNumB] = useState<number>(0);
    const [result, setResult] = useState<GCDResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch(`http://localhost:5000/api/gcd`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ a: numA, b: numB }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred!');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h1>GCD Calculator - Euclidean Algorithm</h1>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                The Euclidean algorithm finds the Greatest Common Divisor (GCD) of two numbers 
                by repeatedly applying: GCD(a, b) = GCD(b, a mod b) until b = 0
            </p>

            <form onSubmit={handleSubmit} style={{ marginBottom: '30px' }}>
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        First Number (a):
                    </label>
                    <input
                        type="number"
                        value={numA || ''}
                        onChange={(e) => setNumA(parseInt(e.target.value) || 0)}
                        placeholder="Enter first number"
                        min="1"
                        required
                        style={{
                            padding: '8px',
                            fontSize: '16px',
                            width: '100%',
                            maxWidth: '300px',
                            border: '1px solid #ccc',
                            borderRadius: '4px'
                        }}
                    />
                </div>

                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        Second Number (b):
                    </label>
                    <input
                        type="number"
                        value={numB || ''}
                        onChange={(e) => setNumB(parseInt(e.target.value) || 0)}
                        placeholder="Enter second number"
                        min="1"
                        required
                        style={{
                            padding: '8px',
                            fontSize: '16px',
                            width: '100%',
                            maxWidth: '300px',
                            border: '1px solid #ccc',
                            borderRadius: '4px'
                        }}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        padding: '10px 20px',
                        fontSize: '16px',
                        backgroundColor: loading ? '#ccc' : '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: loading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Calculating...' : 'Calculate GCD'}
                </button>
            </form>

            {error && (
                <div style={{
                    padding: '15px',
                    backgroundColor: '#f8d7da',
                    color: '#721c24',
                    borderRadius: '4px',
                    marginBottom: '20px'
                }}>
                    <strong>Error:</strong> {error}
                </div>
            )}

            {result && (
                <div>
                    <h2 style={{
                        padding: '15px',
                        backgroundColor: '#d4edda',
                        color: '#155724',
                        borderRadius: '4px',
                        marginBottom: '20px',
                        textAlign: 'center'
                    }}>
                        GCD = {result.gcd}
                    </h2>

                    <h3 style={{ marginTop: '30px', marginBottom: '15px' }}>Step-by-Step Solution:</h3>
                    <div style={{ backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '4px' }}>
                        {result.steps.map((step, index) => (
                            <div
                                key={index}
                                style={{
                                    marginBottom: '15px',
                                    paddingBottom: '15px',
                                    borderBottom: index < result.steps.length - 1 ? '1px solid #dee2e6' : 'none'
                                }}
                            >
                                <div style={{ fontWeight: 'bold', marginBottom: '5px', color: '#007bff' }}>
                                    Step {step.step}: {step.description}
                                </div>
                                <div style={{
                                    fontFamily: 'monospace',
                                    backgroundColor: '#e9ecef',
                                    padding: '10px',
                                    borderRadius: '4px',
                                    marginTop: '5px',
                                    marginBottom: '5px',
                                    fontSize: '14px'
                                }}>
                                    {step.calculation}
                                </div>
                                <div style={{
                                    marginTop: '5px',
                                    color: '#28a745',
                                    fontStyle: 'italic'
                                }}>
                                    {step.result}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div style={{
                        marginTop: '20px',
                        padding: '15px',
                        backgroundColor: '#e7f3ff',
                        borderLeft: '4px solid #007bff',
                        borderRadius: '4px'
                    }}>
                        <strong>Note:</strong> The Euclidean algorithm is one of the oldest and most efficient 
                        algorithms for computing the GCD of two numbers. It has a time complexity of O(log min(a, b)).
                    </div>
                </div>
            )}
        </div>
    );
};

export default GCD;
