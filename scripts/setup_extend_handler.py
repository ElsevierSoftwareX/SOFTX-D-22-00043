import argparse
import binascii
from os import path
import sys
sys.path.append('..')
from pseudoID import config
from pseudoID.hw_encryption import SessionHandler

parser = argparse.ArgumentParser(description='Encrypt the generated pseudokey with the hardware key and add new entry'
                                             'to the handler file')
parser.add_argument('-p', '--project', type=str, help='name of the project')
#parser.add_argument('-p', '--project', type=str, help='name of the project') #todo valid_tag

args = parser.parse_args()

if __name__ == '__main__':
    pseudokey_path = args.project + '_pseudokey.txt'
    if path.exists(pseudokey_path):
        with open(pseudokey_path, "r") as file:
            pseudokey=file.read()

        # create suffix for handler line
        site = args.project
        valid_tag = 'SFB289'
        site_tag = config._site_tag_[site]
        suffix = '_' + valid_tag + '_' + site + '_' + site_tag

        plaintext = pseudokey + suffix

        nitro = SessionHandler()
        new_entry = nitro.encrypt(plaintext.encode('utf-8'))
        nitro.extend(binascii.hexlify(new_entry))
        print('handler successfully extended!')
    else:
        print('pseudokey file for selected project does not exist!')
