import Playfair from '../../algopages/Playfair';
import Affine from '../../algopages/Affine';
import Vigenere from '../../algopages/Vigenere';
import DES from '../../algopages/DES';
import AES from '../../algopages/AES';

const Ex1 = () => {
  return (
    <div>
        <h1>Exercise 1: Substitution Cipher</h1>
        <Playfair/>
        <Affine/>
        <Vigenere/>
        <DES/>
        <AES/>
    </div>
  )
    
}

export default Ex1;