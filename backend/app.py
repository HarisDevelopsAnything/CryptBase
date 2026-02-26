from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms.playfair import playfair_encrypt, playfair_decrypt 
from algorithms.affine import affine_encrypt, affine_decrypt
from algorithms.vigenere import vigenere_decrypt, vigenere_encrypt
from algorithms.miller import millerTest, miller_rabin_with_steps
from algorithms.fermat import fermat_test
from algorithms.gcd import gcd_with_steps
from algorithms.des import des_encrypt, des_decrypt
from algorithms.aes import aes_encrypt, aes_decrypt
from algorithms.rsa import rsa_encrypt, rsa_decrypt

app = Flask(__name__)
CORS(app)

@app.route('/api/affine/encrypt', methods=['POST'])
def encrypt_affine():
    try:
        data = request.get_json()
        text = data.get('text', '').upper()
        key1 = data.get('key1', '')
        key2 = data.get('key2', '')
        
        if not text or not key1 or not key2:
            return jsonify({'error': 'Both text and key are required'}), 400
        
        result = affine_encrypt(text, key1, key2)
        return jsonify({
            'encrypted': result['encrypted'],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/affine/decrypt', methods=['POST'])
def decrypt_affine():
    try:
        data = request.get_json()
        text = data.get('text', '').upper()
        key1 = data.get('key1', '')
        key2 = data.get('key2', '')
        
        if not text or not key1 or not key2:
            return jsonify({'error': 'Both text and key are required'}), 400
        
        result = affine_decrypt(text, key1, key2)
        return jsonify({
            'decrypted': result['decrypted'],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair/encrypt', methods=['POST'])
def encrypt_playfair():
    try:
        data = request.get_json()
        text = data.get('text', '').upper()
        key = data.get('key', '')
        
        if not text or not key:
            return jsonify({'error': 'Both text and key are required'}), 400
        
        result = playfair_encrypt(text, key)
        return jsonify({
            'encrypted': result['encrypted'],
            'keyMatrix': result['keyMatrix'],
            'digraphs': result['digraphs']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair/decrypt', methods=['POST'])
def decrypt_playfair():
    try:
        data = request.get_json()
        text = data.get('text', '').upper()
        key = data.get('key', '')
        
        if not text or not key:
            return jsonify({'error': 'Both text and key are required'}), 400
        
        result = playfair_decrypt(text, key)
        return jsonify({
            'decrypted': result['decrypted'],
            'keyMatrix': result['keyMatrix'],
            'digraphs': result['digraphs']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vigenere/encrypt', methods=['POST'])
def encrypt_vigenere():
    try:
        data= request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        if not text or not key:
            return jsonify({'error': 'Both key and text required!'}), 400
        
        result = vigenere_encrypt(text,key)
        return jsonify({
            'encrypted': result['encrypted']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/vigenere/decrypt', methods=['POST'])
def decrypt_vigenere():
    try:
        data= request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        if not text or not key:
            return jsonify({'error':'Text and key are required!'}), 400
        
        result = vigenere_decrypt(text,key)
        return jsonify(
            {
                'decrypted': result['decrypted']
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}),500

@app.route('/api/miller', methods=['POST'])
def miller_test():
    try:
        data = request.get_json()
        num = int(data.get('num'))
        iter = int(data.get('iter'))
        
        if not num or not iter:
            return jsonify({'error': 'Both num and k are required'}), 400
        
        result = miller_rabin_with_steps(num, iter)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fermat', methods=['POST'])
def fermat_primality_test():
    try:
        data = request.get_json()
        num = int(data.get('num'))
        iterations = int(data.get('iterations'))
        
        if not num or not iterations:
            return jsonify({'error': 'Both num and iterations are required'}), 400
        
        result = fermat_test(num, iterations)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gcd', methods=['POST'])
def calculate_gcd():
    try:
        data = request.get_json()
        a = int(data.get('a'))
        b = int(data.get('b'))
        
        if a is None or b is None:
            return jsonify({'error': 'Both numbers a and b are required'}), 400
        
        if a <= 0 or b <= 0:
            return jsonify({'error': 'Both numbers must be positive'}), 400
        
        result = gcd_with_steps(a, b)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/api/des/encrypt', methods=['POST'])
def encrypt_des():
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '')
        key = data.get('key', '')
        p10 = data.get('p10', '')
        p8 = data.get('p8', '')
        ipv = data.get('ip', '')
        ipinv = data.get('ipinv', '')
        epv = data.get('ep', '')
        p4 = data.get('p4', '')
        s0 = data.get('s0', '')
        s1 = data.get('s1', '')

        if not plaintext or not key:
            return jsonify({'error': 'Plaintext and key are required'}), 400

        result = des_encrypt(plaintext, key, p10, p8, ipv, ipinv, epv, p4, s0, s1)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/des/decrypt', methods=['POST'])
def decrypt_des():
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        key = data.get('key', '')
        p10 = data.get('p10', '')
        p8 = data.get('p8', '')
        ipv = data.get('ip', '')
        ipinv = data.get('ipinv', '')
        epv = data.get('ep', '')
        p4 = data.get('p4', '')
        s0 = data.get('s0', '')
        s1 = data.get('s1', '')

        if not ciphertext or not key:
            return jsonify({'error': 'Ciphertext and key are required'}), 400

        result = des_decrypt(ciphertext, key, p10, p8, ipv, ipinv, epv, p4, s0, s1)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/aes/encrypt', methods=['POST'])
def encrypt_aes():
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '').replace(' ', '')
        key = data.get('key', '').replace(' ', '')

        if not plaintext or not key:
            return jsonify({'error': 'Plaintext and key are required'}), 400

        result = aes_encrypt(plaintext, key)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/aes/decrypt', methods=['POST'])
def decrypt_aes():
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '').replace(' ', '')
        key = data.get('key', '').replace(' ', '')

        if not ciphertext or not key:
            return jsonify({'error': 'Ciphertext and key are required'}), 400

        result = aes_decrypt(ciphertext, key)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/rsa/encrypt', methods=['POST'])
def encrypt_rsa():
    try:
        data = request.get_json()
        plain = int(data.get('plain',''))
        p = int(data.get('p',''))
        q = int(data.get('q',''))

        if not plain or not p or not q:
            return jsonify({'error': 'Plaintext, p and q are needed.'}), 400
        
        result = rsa_encrypt(plain, p, q)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/rsa/decrypt', methods=['POST'])
def decrypt_rsa():
    try:
        data = request.get_json()
        cipher = int(data.get('cipher',''))
        p = int(data.get('p',''))
        q = int(data.get('q',''))

        if not cipher or not p or not q:
            return jsonify({'error': 'Ciphertext, p and q are needed.'}), 400
        
        result = rsa_decrypt(cipher, p, q)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host="0.0.0.0")
