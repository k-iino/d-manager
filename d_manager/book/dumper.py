import sys
import pickle

import yaml


class DumperBase:
    def __init__(self):
        pass

    def dump(self, entries):
        raise NotImplementedError


class PickleStdOutDumper(DumperBase):
    """標準出力に Pickle データを Dump する。"""
    def dump(self, entries):
        sys.stdout.buffer.write(pickle.dumps(entries))


class PickleFileDumper(DumperBase):
    """ファイルに Pickle データを Dump する。"""
    def __init__(self, file, mode='wb'):
        self.__file = file
        self.__mode = mode
        super(PickleFileDumper, self).__init__()

    def dump(self, entries):
        with open(self.__file, mode=self.__mode) as f:
            pickle.dump(entries, f)


class YAMLDumper(DumperBase):
    def dump(self, entries):
        dump_list = list()
        for e in entries.values():
            dump_list.append(e.to_dict())
        else:
            print(yaml.dump(dump_list, allow_unicode=True))
            # sys.stdout.buffer.write(str(yaml.dump(dump_list)))
