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

def print_choices_and_select(coinData):
    valid_choices = []
    original_indices = []

    # Print the numbered list of choices
    print("")
    print("Available choices for Primary Coin:")
    for idx, row in enumerate(coinData):
        if row[4] != 0:
            valid_choices.append(row)
            original_indices.append(idx)
            print(f"{len(valid_choices)}: {row[0]} ({row[3]}) - {row[4]}")

    # Ask the user to select a choice
    if valid_choices:
        try:
            choice = int(input("\nEnter the number of the Primary coin you want to mine: ")) - 1
            if 0 <= choice < len(valid_choices):
                selected_row_index = original_indices[choice]
                selected_row = coinData[selected_row_index]
                print(f"\nYou selected: {selected_row[0]} ({selected_row[3]}) - {selected_row}")
                return selected_row_index  # Return the original row number for later use
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

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

###[CoinName, PUBKEY_Address, SecretKey, Ticker, cMinor_MiningPort]
coinData=\
    [
        ["AiBlockChain","17","B0","AIBC",20944],#in decimal:23,76
        ["AustraliaCash","17","17","AUS",0],#in decimal:23,23
        ["CanadaEcoin","1C","9C","CDN",0],#in decimal:28,156
        ["DogmCoin","1E","9E","DOGM",0],#in decimal:30,158
        ["InfiniteCoin","6F","EF","IFC",21099],#in decimal:111,239
        ["NewYorkCoin","3C","BC","NYC",0],#in decimal:60,188
        ["PepeCoin","38","9E","PEPE",0],#in decimal:56,158
        ["WorldCoin","49","C9","WDC",0],#in decimal:73,201
        ["Bells","19","99","BEL",0],#in decimal:25,153
        ["LuckyCoin","2F","AF","LKY",27988],#in decimal:47,175 Not 100% on this. It has not been tested. Use at your own risk.
        #["Bunker","19","9E","BKC",0],#in decimal:25,158
        #["Trinity","1E","B1","TTY",0],#in decimal:30,177
        ["CyberDollar","22","9E","CASH",27997],#in decimal:34,158
        ["Mateable","33","AA","MTBC",20695],#in decimal:51,170
        #["Sexcoin","3E","BE","SXC",0],#in decimal:62,190
        #["Quebecoin","3A","BA","QBC",0],#in decimal:58,186
        #["Myriadcoin","32","B2","XMY",0],#in decimal:50,178
        #["Katkoyn","2D","AD","NYAN",0],#in decimal:45,173
        ["Earthcoin","5D","DD","EAC",0],#in decimal:93,221
        ["Dogecoin","1E","9E","DOGE",0],#in decimal:30,158
        ["Dingocoin","1E","9E","DINGO",0],#in decimal:30,158
        #["Bitmark","55","D5","MARKS",0],#in decimal:85,213
        #["Advanced Internet Blockchains","17","97","AIB",0],#in decimal:23,151
        #["Argentum","17","97","AGM",0],#in decimal:23,151
        #["BitcoinMoney","33","B2","BCM",0],#in decimal:51,178
        ["Cyberyen","1C","9C","CY",21214],#in decimal:28,156
        ["Digibyte","1E","80","DGB",20200],#in decimal:30,128
        ##["Einsteinium","21","B0","EMC2",0],#in decimal:33,176
        ##["GlobalToken","26","A6"],#in decimal:38,166
        ##["LiteCoin","30","B0","LTC",0],#in decimal:48,176
        ##["MarsCoin","32","B2","MARS",0],#in decimal:50,178
        ["NengCoin","35","B0","NENG",20222]#in decimal:53,176
    ]

private_key = password_to_private_key()
public_key = private_key_to_public_key(private_key)

print("Choosing no will create a unique private key for each address. Safer, but less convenient")
print("Default is y for One Key")
oneKey = input("Do you want One key to unlock all wallets(y/n)")
if oneKey != "n": oneKey = "y"

selected_row_number = print_choices_and_select(coinData)

thePasswordP2 =""
for x in range(len(coinData)): 
    theVersionByte = bytes.fromhex(coinData[x][1])
    theWifcVersionByte = bytes.fromhex(coinData[x][2])
    coin_address = public_key_to_address(public_key)
    wifc_key = private_key_to_wifc(private_key)
    print(coinData[x][0], "Address:", coin_address)
    print(coinData[x][0], "WIFC Key:", wifc_key)
    
    if x == selected_row_number:
        theUsername = coin_address
        thePasswordP1 = "c=" + coinData[x][3] + ",ps=aux"
        thePort = coinData[x][4]
    if coinData[x][4] == 0:
        thePasswordP2 = thePasswordP2 + ",p_" + coinData[x][3] + "=" + coin_address
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

thePassword = thePasswordP1 + thePasswordP2
print("-o Stratum: stratum+tcp://eu-merged-stratum.cminors-pool.com:", thePort)
print("-u Username:", theUsername)
print("-p Password:", thePassword)
