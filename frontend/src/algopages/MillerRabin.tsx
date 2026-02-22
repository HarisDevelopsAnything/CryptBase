import {useState} from 'react';

interface Step {
    step: number;
    description: string;
    calculation?: string;
    result?: string;
}

interface MillerRabinResult {
    isPrime: boolean;
    steps: Step[];
}

const MillerRabin = () => {
    const [num, setNum] = useState<number>(0);
    const [iter, setIter] = useState<number>(5);
    const [result, setResult] = useState<MillerRabinResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit =  async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            const response = await fetch(`${backendUrl}/api/miller`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({num, iter}),
            });

            if(!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Request failed');
            }

            const data = await response.json();
            setResult(data);
        } catch(err) {
            setError(err instanceof Error ? err.message : 'An error occured!')
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h1>Miller-Rabin Primality Test</h1>
            <p style={{ marginBottom: '20px', color: '#666' }}>
                The Miller-Rabin test is a probabilistic primality test that writes n-1 as 2<sup>r</sup>×d 
                and tests witnesses to determine if n is composite or probably prime.
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
                        value={iter || ''}
                        onChange={(e) => setIter(parseInt(e.target.value) || 1)}
                        placeholder="Enter the k value"
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
                                    {step.description && step.description.startsWith('  ') ? (
                                        <span style={{ marginLeft: '20px' }}>{step.description}</span>
                                    ) : (
                                        <span>Step {step.step}: {step.description}</span>
                                    )}
                                </div>
                                {step.calculation && (
                                    <div style={{
                                        fontFamily: 'monospace',
                                        backgroundColor: '#e9ecef',
                                        padding: '8px',
                                        borderRadius: '4px',
                                        marginTop: '5px',
                                        marginBottom: '5px',
                                        marginLeft: step.description && step.description.startsWith('  ') ? '20px' : '0'
                                    }}>
                                        {step.calculation}
                                    </div>
                                )}
                                {step.result && step.result.trim() !== '' && (
                                    <div style={{
                                        marginTop: '5px',
                                        marginLeft: step.description && step.description.startsWith('  ') ? '20px' : '0',
                                        color: step.result.includes('✓') ? '#155724' :
                                               step.result.includes('✗') ? '#721c24' : '#666'
                                    }}>
                                        {step.result}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default MillerRabin