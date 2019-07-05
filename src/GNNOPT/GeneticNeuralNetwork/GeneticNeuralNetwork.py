import random

from GeneticAlgorithmGeneric.GeneticAlgorithm import BaseIndividual
from NeuralNetwork.ActivationFunctions import Relu, Sigmoid
from NeuralNetwork.NeuralNetwork import NeuralNetwork
from Utils.Utils import commands_getoutput


class MyIndividual(BaseIndividual):
    __CONST_FLAGS = [
        '-aa', '-adce', '-add-discriminators', '-alignment-from-assumptions', '-alloca-hoisting', '-always-inline',
        '-argpromotion', '-asan', '-assumption-cache-tracker', '-atomic-expand', '-barrier', '-basicaa', '-basiccg',
        '-bdce', '-block-freq', '-bounds-checking', '-branch-prob', '-break-crit-edges', '-called-value-propagation',
        '-callsite-splitting', '-cfl-anders-aa', '-cfl-steens-aa', '-codegenprepare', '-consthoist',
        '-constmerge', '-constprop', '-coro-cleanup', '-coro-early', '-coro-elide', '-coro-split',
        '-correlated-propagation',
        '-cost-model', '-cross-dso-cfi', '-da', '-dce', '-deadargelim', '-delinearize', '-demanded-bits', '-die',
        '-div-rem-pairs', '-divergence', '-domfrontier', '-domtree', '-dse', '-dwarfehprepare', '-early-cse',
        '-early-cse-memssa', '-ee-instrument', '-elim-avail-extern', '-expand-reductions', '-expandmemcmp',
        '-extract-blocks', '-falkor-hwpf-fix', '-flattencfg', '-float2int', '-forceattrs',
        '-summary-file -function-import',
        '-functionattrs', '-generic-to-nvvm', '-global-merge', '-globaldce', '-globalopt', '-globals-aa',
        '-globalsplit',
        '-guard-widening', '-gvn', '-gvn-hoist', '-gvn-sink', '-hotcoldsplit', '-indirectbr-expand', '-indvars',
        '-infer-address-spaces', '-inferattrs', '-inline', '-instcombine', '-instcount', '-instnamer', '-instrprof',
        '-instsimplify', '-interleaved-access', '-interleaved-load-combine', '-intervals', '-ipconstprop', '-ipsccp',
        '-jump-threading', '-libcalls-shrinkwrap', '-load-store-vectorizer', '-loop-accesses', '-loop-data-prefetch',
        '-loop-deletion', '-loop-distribute', '-loop-extract', '-loop-extract-single', '-loop-guard-widening',
        '-loop-idiom',
        '-loop-instsimplify', '-loop-interchange', '-loop-load-elim', '-loop-predication', '-loop-reduce',
        '-loop-reroll',
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
        '-lazy-value-info', '-pgo-memop-opt', '-lcssa-verification', '-lcssa', '-scalar-evolution', '-licm',
        '-postdomtree',
        '-rpo-functionattrs', '-slp-vectorizer', '-strip-dead-prototypes'
    ]

    def __init__(self, args):
        super().__init__()
        self.work_dir = args[0]
        self.bitcode_file = args[1]
        self.features = args[2]

        self.bc_file = '%s/out.bc' % self.work_dir
        self.ll_file = '%s/out.ll' % self.work_dir
        self.exe_file = '%s/out.exe' % self.work_dir

        num_hidden = random.randint(1, 5)
        dims = [random.randint(10, 30) for _ in range(num_hidden + 2)]
        dims[0] = len(self.features)
        dims[num_hidden + 1] = random.randint(10, 100)
        self.gene = NeuralNetwork(dims, Sigmoid(), Relu(), 0.0)

    def output(self):
        r = ''
        out = self.gene.forward(self.features)
        for line in out:
            for col in line:
                x = int(col * 10)
                if x < 0:
                    r += self.__CONST_FLAGS[0] + ' '
                elif x > 173:
                    r += self.__CONST_FLAGS[173] + ' '
                else:
                    r += self.__CONST_FLAGS[x] + ' '
        return r

    def evaluate(self):
        out = self.output()
        commands_getoutput('opt %s -S -o %s %s' % (out, self.bc_file, self.ll_file))
        commands_getoutput('clang++ -w %s -lm -o %s' % (self.bc_file, self.exe_file))
        time = float(commands_getoutput(self.exe_file))
        return 1 / time

    def __crossover(self, ind1, ind2):
        l1, c1 = ind1.shape
        l2, c2 = ind2.shape
        l, c = min(l1, l2), min(c1, c2)
        randR = random.randint(0, l - 1)
        randC = random.randint(0, c - 1)
        for i in range(l):
            for j in range(c):
                if (i < randR) or (i == randR and j <= randC):
                    ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]

    def crossover(self, partner):
        for w, pw in zip(self.gene.weights, partner.gene.weights):
            self.__crossover(self.gene.weights[w], partner.gene.weights[pw])

    def __mutate(self, ind):
        l, c = ind.shape
        randC = random.randint(0, l - 1)
        for i in range(c):
            ind[randC][i] += random.uniform(-1, 1)
            if ind[randC][i] > 1:
                ind[randC][i] = 1
            elif ind[randC][i] < -1:
                ind[randC][i] = -1

    def mutate(self):
        for w in self.gene.weights:
            self.__mutate(self.gene.weights[w])
