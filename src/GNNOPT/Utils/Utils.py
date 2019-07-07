import sys

if sys.version_info < (2, 7):
    import commands
else:
    import subprocess


def commands_getoutput(cmd):
    try:
        if sys.version_info < (2, 7):
            return commands.getoutput(cmd)
        else:
            byte_out = subprocess.check_output(cmd.split())
            str_out = byte_out.decode("utf-8")
            return str_out
    except Exception as e:
        return str(e)


def command_shell(cmd):
    try:
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
        p.wait()
        return '0'
    except Exception as e:
        return str(e)


def map_number(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def get_all_opt_flags_available(ll_file_test):
    flags_aux = [
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
    flags = []
    for f in flags_aux:
        r = commands_getoutput('opt %s -S %s -o out.bc' % (f, ll_file_test))
        if len(r) == 0:
            flags.append(f)

    command_shell('rm out.bc')
    return flags
