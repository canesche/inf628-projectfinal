import os
import subprocess

import llvmlite.binding as llvm
import numpy as np


class CollectCodeFeatures:
    __cmd = 'clang -std=c++11 -c -emit-llvm %s -o %s'

    def __init__(self, code_path):
        self.__code_path = code_path

    def run(self):
        cmd = self.__cmd % (self.__code_path, 'out.bc')
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
        p.wait()
        bcfe = BitCodefeaturesExtractor('out.bc')
        bcfe.extract()
        os.remove('out.bc')
        return bcfe.features


class Features:
    __features = {'blocks': 0, 'functions': 0, 'global_vars': 0,
                  'bin_ops': 0, 'bit_bin_ops': 0, 'vec_ops': 0, 'agg_ops': 0,
                  'load_ops': 0, 'store_ops': 0, 'memory_ops': 0, 'others_ops': 0}

    def __repr__(self):
        return 'Blocks: %d\n' % self.__features['blocks'] + \
               'Functions: %d\n' % self.__features['functions'] + \
               'Global Vars: %d\n' % self.__features['global_vars'] + \
               'Bin Ops: %d\n' % self.__features['bin_ops'] + \
               'Bit Ops: %d\n' % self.__features['bit_bin_ops'] + \
               'Vec Ops: %d\n' % self.__features['vec_ops'] + \
               'Agg Ops: %d\n' % self.__features['agg_ops'] + \
               'Load Ops: %d\n' % self.__features['load_ops'] + \
               'Store Ops: %d\n' % self.__features['store_ops'] + \
               'Memory Ops: %d\n' % self.__features['memory_ops'] + \
               'Others Ops: %d\n' % self.__features['others_ops']

    def set_value(self, feature, value):
        self.__features[feature] = value

    def inc_feature(self, feature):
        self.__features[feature] += 1

    def get_features(self):
        return np.array(list(self.__features.values()))


class BitCodefeaturesExtractor:
    __BIN_OPS = {'add', 'fadd', 'sub', 'fsub', 'mul', 'fmul', 'udiv', 'sdif', 'fdiv', 'urem', 'srem', 'frem'}
    __BITBIN_OPS = {'shl', 'lshr', 'ashr', 'and', 'or', 'xor'}
    __VEC_OPS = {'extractelement', 'insertelement', 'shufflevector'}
    __AGG_OPS = {'extractvalue', 'insertvalue'}
    __MEM_OPS = {'getelementptr', 'alloca'}

    def __init__(self, bitcode_file):
        self.bitcode_file = bitcode_file

    def extract(self):
        bc = open(self.bitcode_file, 'rb').read()
        m = llvm.parse_bitcode(bc)
        self.features = Features()
        for f in m.functions:
            self.features.inc_feature('functions')
            for b in f.blocks:
                self.features.inc_feature('blocks')
                for i in b.instructions:
                    if i.opcode in self.__BIN_OPS:
                        self.features.inc_feature('bin_ops')
                    elif i.opcode in self.__BITBIN_OPS:
                        self.features.inc_feature('bit_bin_ops')
                    elif i.opcode in self.__AGG_OPS:
                        self.features.inc_feature('agg_ops')
                    elif i.opcode in self.__VEC_OPS:
                        self.features.inc_feature('vec_ops')
                    elif i.opcode in self.__MEM_OPS:
                        self.features.inc_feature('memory_ops')
                    elif i.opcode == 'load':
                        self.features.inc_feature('load_ops')
                    elif i.opcode == 'store':
                        self.features.inc_feature('store_ops')
                    else:
                        self.features.inc_feature('others_ops')

        for __ in m.global_variables:
            self.features.inc_feature('global_vars')
