import binascii

from Crypto.Cipher import AES
from pseudoID import config
from pseudoID.base_conversion import BaseConverter

conv = BaseConverter(config.settings['ENCRYPTION']['char_base'])

class Encryptor:
    # todo check old references for encryptor
    def __init__(self, pseudonym_key, site_tag=None):
        self.site_tag = site_tag
        self.key = pseudonym_key

    def long_id(self, message):
        cipher = AES.new(self.key, AES.MODE_SIV)
        ciphertext, tag = cipher.encrypt_and_digest(message.rjust(64, '0').encode("utf-8"))
        if self.site_tag == None:
            return conv.hex2custom(binascii.hexlify(ciphertext + tag).decode('utf-8'))
        else:
            return self.site_tag + conv.hex2custom(binascii.hexlify(ciphertext + tag).decode('utf-8'))

    def short_id(self, long_id, length=config.settings['ENCRYPTION'].getint('short_id_length')):
        if self.site_tag == None:
            return long_id[0:length]
        else:
            return long_id[0:length + 1]

    def reidentify(self, longID):
        if self.site_tag != None:
            longID = longID[1:]

        longID = conv.custom2hex(longID)

        tag = binascii.unhexlify(longID[-32:].encode('utf-8'))
        message = binascii.unhexlify(longID[:-32].encode('utf-8'))

        cipher = AES.new(self.key, AES.MODE_SIV)
        plaintext = cipher.decrypt_and_verify(message, mac_tag=tag)

        return plaintext.decode('utf-8').lstrip('0')
        # data = self.cipher.decrypt(message.rjust(64, '0').encode("utf-8"))
