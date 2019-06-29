import random
import subprocess

import numpy as np

from FeaturesExtractor.CollectCodeFeatures import CollectCodeFeatures
from GeneticAlgorithmGeneric.GeneticAlgorithm import BaseIndividual, GeneticAlgorithm
from NeuralNetwork.NeuralNetwork import NeuralNetwork

CONST_FLAGS = [
    '-aa', '-adce', '-add-discriminators', '-alignment-from-assumptions', '-alloca-hoisting', '-always-inline',
    '-argpromotion', '-asan', '-assumption-cache-tracker', '-atomic-expand', '-barrier', '-basicaa', '-basiccg',
    '-bdce', '-block-freq', '-bounds-checking', '-branch-prob', '-break-crit-edges', '-called-value-propagation',
    '-callsite-splitting', '-cfl-anders-aa', '-cfl-steens-aa', '-codegenprepare', '-consthoist',
    '-constmerge', '-constprop', '-coro-cleanup', '-coro-early', '-coro-elide', '-coro-split',
    '-correlated-propagation',
    '-cost-model', '-cross-dso-cfi', '-da', '-dce', '-deadargelim', '-delinearize', '-demanded-bits', '-die',
    '-div-rem-pairs', '-divergence', '-domfrontier', '-domtree', '-dse', '-dwarfehprepare', '-early-cse',
    '-early-cse-memssa', '-ee-instrument', '-elim-avail-extern', '-expand-reductions', '-expandmemcmp',
    '-extract-blocks', '-falkor-hwpf-fix', '-flattencfg', '-float2int', '-forceattrs', '-summary-file -function-import',
    '-functionattrs', '-generic-to-nvvm', '-global-merge', '-globaldce', '-globalopt', '-globals-aa', '-globalsplit',
    '-guard-widening', '-gvn', '-gvn-hoist', '-gvn-sink', '-hotcoldsplit', '-indirectbr-expand', '-indvars',
    '-infer-address-spaces', '-inferattrs', '-inline', '-instcombine', '-instcount', '-instnamer', '-instrprof',
    '-instsimplify', '-interleaved-access', '-interleaved-load-combine', '-intervals', '-ipconstprop', '-ipsccp',
    '-jump-threading', '-libcalls-shrinkwrap', '-load-store-vectorizer', '-loop-accesses', '-loop-data-prefetch',
    '-loop-deletion', '-loop-distribute', '-loop-extract', '-loop-extract-single', '-loop-guard-widening',
    '-loop-idiom',
    '-loop-instsimplify', '-loop-interchange', '-loop-load-elim', '-loop-predication', '-loop-reduce', '-loop-reroll',
    '-loop-rotate', '-loop-simplify', '-loop-simplifycfg', '-loop-sink', '-loop-unroll', '-loop-unroll-and-jam',
    '-loop-unswitch', '-loop-vectorize', '-loop-versioning', '-loop-versioning-licm', '-loops', '-lower-expect',
    '-lower-guard-intrinsic', '-loweratomic', '-lowerinvoke', '-lowerswitch', '-lowertypetests',
    '-make-guards-explicit',
    '-mem2reg', '-memcpyopt', '-memdep', '-memoryssa', '-mergefunc', '-mergeicmps', '-mergereturn', '-mldst-motion',
    '-partial-inliner', '-partially-inline-libcalls', '-print-memderefs', '-reassociate', '-reg2mem', '-regions',
    '-scalarizer', '-sccp', '-simple-loop-unswitch', '-slsr', '-speculative-execution', '-sroa', '-strip',
    '-strip-nondebug',
    '-tailcallelim', '-bounds-checking-single-trap', '-enable-name-compression', '-enable-load-pre',
    '-enable-no-infs-fp-math',
    '-enable-no-nans-fp-math', '-enable-no-signed-zeros-fp-math', '-enable-no-trapping-fp-math',
    '-enable-unsafe-fp-math',
    '-expensive-combines', '-tailcallopt', '-tti', '-tbaa', '-scoped-noalias', '-targetlibinfo', '-verify',
    '-ee-instrument',
    '-simplifycfg', '-profile-summary-info', '-lazy-branch-prob', '-lazy-block-freq', '-opt-remark-emitter',
    '-prune-eh',
    '-lazy-value-info', '-pgo-memop-opt', '-lcssa-verification', '-lcssa', '-scalar-evolution', '-licm', '-postdomtree',
    '-rpo-functionattrs', '-slp-vectorizer', '-strip-dead-prototypes'
]


class MyIndividual(BaseIndividual):
    def __init__(self, args):
        super().__init__()
        self.code_path = args[0]
        self.input = args[1]
        self.gene = NeuralNetwork(len(self.input), random.randint(20, 50), random.randint(35, 105))
        self.cmd = 'clang -std=c++11 -c -emit-llvm %s -o %s\n' \
                   'opt %s -S -o %s %s\n' + \
                   'clang++ %s -lm -o %s\n' + \
                   './%s > time.txt\n' + \
                   'rm *.bc *.exe'

        def handle(x):
            global CONST_FLAGS
            x = int(x)
            if x < 0:
                return CONST_FLAGS[0]
            elif x > 173:
                return CONST_FLAGS[173]
            return CONST_FLAGS[x]

        self.handle = np.vectorize(handle)

    def evaluate(self):
        out = self.gene.output(self.input)
        out = self.handle(out)
        cmd = self.cmd % (self.code_path, 'out.bc', ' '.join(out), 'out.bc', 'out.bc', 'out.bc', 'out.exe','out.exe')
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
        p.wait()
        time = 1 / (float(open('time.txt').read()))
        return time

    def __crossover(self, ind1, ind2):
        s1 = ind1.cols * ind1.rows
        s2 = ind2.cols * ind2.rows
        size = min(s1, s2)
        cut = random.randint(0, size - 1)
        cxpoint = [i for i in range(0, cut)]
        ind1.matrix = np.reshape(ind1.matrix, (s1))
        ind2.matrix = np.reshape(ind2.matrix, (s2))
        ind1.matrix[cxpoint], ind2.matrix[cxpoint] = ind2.matrix[cxpoint], ind1.matrix[cxpoint]
        ind1.matrix = np.reshape(ind1.matrix, (ind1.rows, ind1.cols))
        ind2.matrix = np.reshape(ind2.matrix, (ind2.rows, ind2.cols))

    def crossover(self, partner):
        self.__crossover(self.gene.whi, partner.gene.whi)
        self.__crossover(self.gene.whh, partner.gene.whh)
        self.__crossover(self.gene.woh, partner.gene.woh)

    def mutate(self):
        lf = lambda x: (x + random.uniform(-0.2, 0.2)) if random.random() < 0.1 else x
        vmutate = np.vectorize(lf)
        self.gene.whi.matrix = vmutate(self.gene.whi.matrix)
        self.gene.whh.matrix = vmutate(self.gene.whh.matrix)
        self.gene.woh.matrix = vmutate(self.gene.woh.matrix)


file = '../../benchmarks/teste.cpp'
ccf = CollectCodeFeatures(file)
f = ccf.run()
ga = GeneticAlgorithm(10, 0.4, 0.3, 10, MyIndividual, [file,f.get_features()])
best = ga.evolution(True)

