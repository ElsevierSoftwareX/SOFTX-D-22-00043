import time
import os
import config


class PseudonymLogger:
    def __init__(self):

        if not os.path.exists(config._key_dir_):
            os.makedirs(config._key_dir_)
            # todo warning

        i = 1
        while os.path.exists(config._key_dir_ + '/log_' + str(i).zfill(4) + '.txt'):
            i += 1

        self.filename = config._key_dir_ + '/log_' + str(i).zfill(4) + '.txt'

        f = open(self.filename, 'w')
        f.close

    def add_entry(self, log_input):
        f = open(self.filename, 'a')
        f.write(log_input + '\n')
        f.close
        return None


def norm_str(str_in):
    char_dict = {ord('ä'): 'ae',
                 ord('ü'): 'ue',
                 ord('ö'): 'oe',
                 ord('ß'): 'ss',
                 ord(' '): None,
                 ord('-'): None,
                 ord(','): None,
                 ord('('): None,
                 ord(')'): None,
                 ord('.'): None,
                 }
    return str_in.lower().translate(char_dict)