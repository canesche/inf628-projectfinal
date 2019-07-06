import fnmatch
import os
import sys

import llvmlite.binding as llvm
import numpy as np

if sys.version_info < (2, 7):
    import commands
else:
    import subprocess


class Features:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__features = {'blocks': 0.0, 'functions': 0.0, 'global_vars': 0.0, 'term_ops': 0.0,
                           'bin_ops': 0.0, 'bit_bin_ops': 0.0, 'vec_ops': 0.0, 'agg_ops': 0.0,
                           'mem_ops': 0.0, 'conv_ops': 0.0, 'others_ops': 0.0}

    def get_file_name(self):
        return self.__file_name

    def __repr__(self):
        return 'File: %s\n' % self.__file_name + \
               'Blocks: %d\n' % self.__features['blocks'] + \
               'Functions: %d\n' % self.__features['functions'] + \
               'Global Vars: %d\n' % self.__features['global_vars'] + \
               'Terminator Ops: %d\n' % self.__features['term_ops'] + \
               'Bin Ops: %d\n' % self.__features['bin_ops'] + \
               'Bit Ops: %d\n' % self.__features['bit_bin_ops'] + \
               'Vec Ops: %d\n' % self.__features['vec_ops'] + \
               'Agg Ops: %d\n' % self.__features['agg_ops'] + \
               'Memory Ops: %d\n' % self.__features['mem_ops'] + \
               'Conversion Ops: %d\n' % self.__features['conv_ops'] + \
               'Others Ops: %d\n' % self.__features['others_ops']

    def set_value(self, feature, value):
        self.__features[feature] = value

    def inc_feature(self, feature):
        self.__features[feature] += 1

    def get_array(self):
        return np.array(list(self.__features.values()))


class CodeFeaturesExtractor:
    __cmd = 'clang -std=c++11 -c -emit-llvm %s -o %s'

    __TERM_OPS = ['ret', 'br', 'swicth', 'indirectbr', 'invoke', 'resume', 'unreachable']
    __BIN_OPS = ['add', 'fadd', 'sub', 'fsub', 'mul', 'fmul', 'udiv', 'sdif', 'fdiv', 'urem', 'srem', 'frem']
    __BITBIN_OPS = ['shl', 'lshr', 'ashr', 'and', 'or', 'xor']
    __VEC_OPS = ['extractelement', 'insertelement', 'shufflevector']
    __AGG_OPS = ['extractvalue', 'insertvalue']
    __MEM_OPS = ['alloca', 'load', 'store', 'fence', 'cmpxchg', 'atomiccrmw', 'getelementptr']
    __CONV_OPS = ['trunc', 'zext', 'sext', 'fptrunc', 'fpext', 'fptoui', 'fptosi', 'uitofp', 'sitofp', 'ptrtoint',
                  'inttoptr', 'bitcast', 'addrspacecast']
    __OTHERS_OPS = ['icmp', 'fcmp', 'phi', 'select', 'call', 'va_arg', 'landingpad']

    def commands_getoutput(self, cmd):
        try:
            if sys.version_info < (2, 7):
                return commands.getoutput(cmd)
            else:
                byte_out = subprocess.check_output(cmd.split())
                str_out = byte_out.decode("utf-8")
                return str_out
        except Exception as e:
            return str(e)

    def get_features(self, dir):
        files = []
        features = []
        for root, dirnames, filenames in os.walk(dir):
            for filename in fnmatch.filter(filenames, '*.c'):
                files.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, '*.cpp'):
                files.append(os.path.join(root, filename))

        for f in files:
            features.append(self.extract(f))

        return features

    def get_single_train_data(self, filepath):
        features = []
        features.append(self.extract(filepath).get_array())
        return np.array(features).T

    def get_train_data(self, dir):
        files = []
        features = []
        for root, dirnames, filenames in os.walk(dir):
            for filename in fnmatch.filter(filenames, '*.c'):
                files.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, '*.cpp'):
                files.append(os.path.join(root, filename))

        for f in files:
            features.append(self.extract(f).get_array())

        return np.array(features).T

    def extract(self, filename):
        cmd = self.__cmd % (filename, 'out.bc')
        r = self.commands_getoutput(cmd)
        if len(r.strip()) == 0:
            bc = open('out.bc', 'rb').read()
            self.commands_getoutput('rm out.bc')
            m = llvm.parse_bitcode(bc)
            features = Features(filename)
            for f in m.functions:
                features.inc_feature('functions')
                for b in f.blocks:
                    features.inc_feature('blocks')
                    for i in b.instructions:
                        if i.opcode in self.__TERM_OPS:
                            features.inc_feature('term_ops')
                        elif i.opcode in self.__BIN_OPS:
                            features.inc_feature('bin_ops')
                        elif i.opcode in self.__BITBIN_OPS:
                            features.inc_feature('bit_bin_ops')
                        elif i.opcode in self.__AGG_OPS:
                            features.inc_feature('agg_ops')
                        elif i.opcode in self.__VEC_OPS:
                            features.inc_feature('vec_ops')
                        elif i.opcode in self.__MEM_OPS:
                            features.inc_feature('mem_ops')
                        elif i.opcode in self.__CONV_OPS:
                            features.inc_feature('conv_ops')
                        elif i.opcode in self.__OTHERS_OPS:
                            features.inc_feature('others_ops')
                        else:
                            print('Instruction not defined: %s' % i.opcode)

            for __ in m.global_variables:
                features.inc_feature('global_vars')
        else:
            print('Error:', r)
            features = Features('-')

        return features
