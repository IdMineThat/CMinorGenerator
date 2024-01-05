import hashlib
import base58
import ecdsa

def password_to_private_key():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    return private_key

def private_key_to_public_key(private_key):
    public_key = private_key.verifying_key
    public_key_bytes = public_key.to_string('compressed')
    return public_key_bytes

def public_key_to_address(public_key):
    hashed_public_key = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    hashed_public_key_with_version = theVersionByte + hashed_public_key
    checksum = hashlib.sha256(hashlib.sha256(hashed_public_key_with_version).digest()).digest()[:4]
    address_data = hashed_public_key_with_version + checksum
    coin_address = base58.b58encode(address_data).decode('utf-8')
    return coin_address

def private_key_to_wifc(private_key):
    private_key_bytes = private_key.to_string()
    compression_flag = b'\x01'
    wifc_data = theWifcVersionByte + private_key_bytes + compression_flag
    checksum = hashlib.sha256(hashlib.sha256(wifc_data).digest()).digest()[:4]
    wifc_key = base58.b58encode(wifc_data + checksum).decode('utf-8')
    return wifc_key

###Add more coins as desired. Everything will update as long as you follow this setup
###The Hex code can be found in most coins github repository, /src/chainparams.cpp
###Search that file for the following code: (This is from Dogecoin)
###base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,30); <--------
###base58Prefixes[SCRIPT_ADDRESS] = std::vector<unsigned char>(1,22);
###base58Prefixes[SECRET_KEY]     = std::vector<unsigned char>(1,158); <-------
###Note the 30 and 158
###These are in Decimal Format, this program needs them in HEX
###Converting 30 from Decimal to Hex = 1E
###Converting 158 from Decimal to Hex = 9E

coinData=\
    [
        ["CyberDollar","22","9E"],#in decimal:34,158
        ["Mateable","33","AA"],#in decimal:51,170
        ["Sexcoin","3E","BE"],#in decimal:62,190
        ["Quebecoin","3A","BA"],#in decimal:58,186
        ["Myriadcoin","32","B2"],#in decimal:50,178
        ["Katkoyn","2D","AD"],#in decimal:45,173
        ["Earthcoin","5D","DD"],#in decimal:93,221
        ["Dogecoin","1E","9E"],#in decimal:30,158
        ["Dingocoin","1E","9E"],#in decimal:30,158
        ["Bitmark","55","D5"],#in decimal:85,213
        ["Advanced Internet Blockchains","17","97"],#in decimal:23,151
        ["Argentum","17","97"],#in decimal:23,151
        ["BitcoinMoney","33","B2"],#in decimal:51,178
        ["Cyberyen","1C","9C"],#in decimal:28,156
        ["Digibyte","1E","80"],#in decimal:30,128
        ["Einsteinium","21","B0"],#in decimal:33,176
        ["GlobalToken","26","A6"],#in decimal:38,166
        ["LiteCoin","30","B0"],#in decimal:48,176
        ["MarsCoin","32","B2"],#in decimal:50,178
        ["NengCoin","35","B0"]#in decimal:53,176
    ]

private_key = password_to_private_key()
public_key = private_key_to_public_key(private_key)

print("Choosing no will create a unique private key for each address. Safer, but less convenient")
print("Default is y for One Key")
oneKey = input("Do you want One key to unlock all wallets(y/n)")
if oneKey != "n": oneKey = "y"

for x in range(len(coinData)): 
    theVersionByte = bytes.fromhex(coinData[x][1])
    theWifcVersionByte = bytes.fromhex(coinData[x][2])
    coin_address = public_key_to_address(public_key)
    wifc_key = private_key_to_wifc(private_key)
    print(coinData[x][0], "Address:", coin_address)
    print(coinData[x][0], "WIFC Key:", wifc_key)
    f = open("newadds.csv", "a")
    f.write(coin_address + ',' + wifc_key + ',' + private_key.to_string().hex() + '\n')
    f.close()
    if oneKey == "n":
        print("Private Key (hex):", private_key.to_string().hex())
        private_key = password_to_private_key()
        public_key = private_key_to_public_key(private_key)

if oneKey == "y":
    print("")
    print("Private Key (hex):", private_key.to_string().hex())
