import { useState } from 'react';

interface Step {
    step: number;
    description: string;
    calculation?: string;
    result: string;
}

interface FermatResult {
    isPrime: boolean;
    steps: Step[];
}

const Fermat = () => {
    const [num, setNum] = useState<number>(0);
    const [iterations, setIterations] = useState<number>(5);
    const [result, setResult] = useState<FermatResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch(`http://localhost:5000/api/fermat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ num, iterations }),
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
            <h1>Fermat's Primality Test</h1>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                Fermat's primality test is based on Fermat's Little Theorem: 
                If n is prime and a is not divisible by n, then a<sup>n-1</sup> ≡ 1 (mod n)
            </p>

            <form onSubmit={handleSubmit} style={{ marginBottom: '30px' }}>
                <div style={{ marginBottom: '15px' }}>
                    <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                        Number to Test:
                    </label>
                    <input
                        type="number"
                        value={num || ''}
                        onChange={(e) => setNum(parseInt(e.target.value) || 0)}
                        placeholder="Enter a number"
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
                        Number of Iterations:
                    </label>
                    <input
                        type="number"
                        value={iterations || ''}
                        onChange={(e) => setIterations(parseInt(e.target.value) || 1)}
                        placeholder="Enter number of iterations"
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
                        backgroundColor: loading ? '#ccc' : '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: loading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Testing...' : 'Test for Primality'}
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
                        backgroundColor: result.isPrime ? '#d4edda' : '#f8d7da',
                        color: result.isPrime ? '#155724' : '#721c24',
                        borderRadius: '4px',
                        marginBottom: '20px'
                    }}>
                        Result: {result.isPrime ? '✓ Probably Prime' : '✗ Composite (Not Prime)'}
                    </h2>

                    <h3 style={{ marginTop: '30px', marginBottom: '15px' }}>Detailed Steps:</h3>
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
                                <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                                    Step {step.step}: {step.description}
                                </div>
                                {step.calculation && (
                                    <div style={{
                                        fontFamily: 'monospace',
                                        backgroundColor: '#e9ecef',
                                        padding: '8px',
                                        borderRadius: '4px',
                                        marginTop: '5px',
                                        marginBottom: '5px'
                                    }}>
                                        {step.calculation}
                                    </div>
                                )}
                                <div style={{
                                    marginTop: '5px',
                                    color: step.result.includes('✓') ? '#155724' :
                                           step.result.includes('✗') ? '#721c24' : '#666'
                                }}>
                                    {step.result}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Fermat;
