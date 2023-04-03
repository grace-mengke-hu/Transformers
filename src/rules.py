import re
from medspacy.ner import TargetRule # this is for exact match when using `literal`
from medspacy.context import ConTextRule

# regular expression patterns
HRR_variants = [
                '\\bHRR\\b',
                'homologous recombination repair',
                'BRCA',
                'breast cancer gene',
                'BRCA1',
                'BRCA2',
                '\\bATM\\b',
                '11q22\\s*\\(ATM\\)',
                '11q22\\.3\\(ATMx1\\)',
                'ataxia(-\\s*)telangiectasia',
                'BRIP1',
                'BARD1',
                'CDK12',
                'Cyclin(_\\s*)dependent kinase',
                'CHEK1',
                'CHEK2',
                'Checkpoint kinase',
                'FANCL',
                'PALB2',
                'PPP2R2A',
                'RAD51B',
                'RAD51C',
                'RAD51D',
                'RAD51L',
                '\\bATR\\b',
                'DSS1',
                'RPA1',
                'NBSI',
                'FANCD2',
                'FANCA',
                'RAD54',
                'Sept9',
                'Septin\\s*9',
                'JAK2',
                'JAK2\\s*exon\\s*12',
                'JAK2\\s*V617F',
                'Janus\\s*kinase\\s*2']
HRR_pattern = '|'.join(HRR_variants)

# Medspacy Target Rules
HRR_pattern_rules = [
    TargetRule(literal = "HRR", category = "PROBLEM", pattern = [{"LOWER":{"IN":["hrr","homologous recombination repair"]}}]),
    TargetRule(literal = 'BRCA', category = "PROBLEM", pattern=[{"LOWER":{"IN":["brca","brca1","brca2","breast cancer gene"]}}]),
    TargetRule(literal = "ATM", category = "PROBLEM", pattern=[{"LOWER":"atm"}]),
    TargetRule(literal = "ataxia telangiectasia", category="PROBLEM", pattern = [{"LOWER":"ataxia"},{"IS_PUNCT":True},{"LOWER":"telangiectasia"}]),
    TargetRule(literal = "BRIP1",category = "PROBLEM", pattern=[{"LOWER":"brip1"}]),
    TargetRule(literal = 'BARD1',category = "PROBLEM", pattern=[{"LOWER":"brad1"}]),
    TargetRule(literal = 'CDK12',category = "PROBLEM", pattern=[{"LOWER":"cdk12"}]),
    TargetRule(literal = "cyclin dependent kinase", category="PROBLEM", pattern = [{"LOWER":"cyclin"},{"IS_PUNCT":True},{"LOWER":"dependent"},{"IS_PUNCT":True},{"LOWER":"kinase"}]),
    TargetRule(literal = "CHEK", category = "PROBLEM", pattern = [{"LOWER": {"REGEX": "check(1|2)"}}]),
    TargetRule(literal = 'CHEK1',category = "PROBLEM", pattern=[{"LOWER":"chek1"}]),
    TargetRule(literal = 'CHEK2',category = "PROBLEM", pattern=[{"LOWER":"chek2"}]),
    TargetRule(literal = "checkpoint kinase", category="PROBLEM", pattern = [{"LOWER":"checkpoint"},{"IS_PUNCT":True},{"LOWER":"kinase"}]),
    TargetRule(literal = 'FANCL',category = "PROBLEM",pattern=[{"LOWER":"fancl"}]),
    TargetRule(literal = 'PALB2',category = "PROBLEM",pattern=[{"LOWER":"palb2"}]),
    TargetRule(literal = 'PPP2R2A',category = "PROBLEM",pattern=[{"LOWER":"ppp2r2a"}]),
    TargetRule(literal = 'RAD51', category = "PROBLEM",pattern = [{"LOWER":{"REGEX":"rad51(b|c|d|l)"}}]),
    TargetRule(literal = 'ATR',category = "PROBLEM",pattern=[{"LOWER":"atr"}]),
    TargetRule(literal = 'DSS1',category = "PROBLEM",pattern=[{"LOWER":"dds1"}]),
    TargetRule(literal = 'RPA1',category = "PROBLEM",pattern=[{"LOWER":"rpa1"}]),
    TargetRule(literal = 'NBSI',category = "PROBLEM",pattern=[{"LOWER":"nbsi"}]),
    TargetRule(literal = 'FANCD2',category = "PROBLEM",pattern=[{"LOWER":"fancd2"}]),
    TargetRule(literal = 'FANCA',category = "PROBLEM",pattern=[{"LOWER":"fancn"}]),
    TargetRule(literal = 'RAD54',category = "PROBLEM",pattern=[{"LOWER":"rad54"}]),
    TargetRule(literal = 'Sept9',category = "PROBLEM", pattern=[{"LOWER":"sept9"}]),
    TargetRule(literal = "Septin 9", category = "PROBLEM", pattern=[{"LOWER":"septin"},{"IS_PUNCT":True},{"LOWER":"9"}]),
    TargetRule(literal = "JAK2", category = "PROBLEM", pattern=[{"LOWER":"jak2"}]),
    TargetRule(literal = "janus", category = "PROBLEM")
               ]

#Context rules
context_rules = [
    # Negation Rules
    ConTextRule(literal='NEGATED', category='NEGATIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "negated"}]),
    ConTextRule(literal='NEG', category='NEGATIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "neg"}]),
    ConTextRule(literal='is not detected', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {
                    "REGEX": "(is\\s*)?not\\s*det(e|a)cted|NON\\s*detected|failed to detect|fails\\s*to\\s*detect"}}]),
    ConTextRule(literal='is NEGATIVE', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": '(is\\s*)?negtaive|(is\\s*)?NEGATIVE|(is\\s*)?negative for'}}]
                ),
    ConTextRule(literal='NO EVIDENCE', category='NEGATIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": {
        "REGEX": "no\\s*evidence|no\\s*definitive\\s*evidence|(does\\s*not|doesn\'t)\\s*have\\s*evidence\\s*of|(does\\s*not|doesn\'t)have\\s*evidence"}}]),
    ConTextRule(literal='No mutations were', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {
                    "REGEX": "no\\s*mutation|No\\s*mutations\\s*were|No\\s*mutations\\s*were\\s*detected|No\\s*other\\s*mutations\\s*were|No\\s*other\\s*mutations\\s*were\\s*detected|No\\s*other\\s*mutations\\s*were\\s*detected"}}]
                ),
    ConTextRule(literal='NEGATIVE', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "negative|\\s*-\\s*ve"}}]
                ),
    ConTextRule(literal='no mutated', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "unmutated|no mutated|non-mutated|resulted as no mutated"}}]
                ),
    ConTextRule(literal='NORMAL', category='NEGATIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "normal"}]),
    ConTextRule(literal='NON-AMPLIFIED', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": "non-amplified"}]),
    ConTextRule(literal='NOT DEMONSTRATE', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": "not demonstrate"}]),
    ConTextRule(literal='no have', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {
                    "REGEX": "did\\s*not\\s*have|failed\\s*to\\s*reveal|without identifiable|not\\s*identified|did\\s*not\\s*reveal|did\\s*not\\s*show"}}]
                ),
    ConTextRule(literal='wildtype', category='NEGATIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "wild\\s*type|wild-type|wildtype|wild"}}]
                ),

    # positive rules
    ConTextRule(literal='DETECTED', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "detected"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='POSITIVE', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "positive"}]),
    ConTextRule(literal='PRESENT', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "present"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='IDENTIFIED', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "identified"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='EVIDENCE', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "evidence"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='SHOW', category='POSITIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "shows?|shows?\\s*mutations?(in\\s*)?"}}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='HARBOURING', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "harbouring"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='DRIVEN', category='POSITIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "driven lungcancer|driven cancer|driven"}}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='DIAGNOSIS', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "diagnosis"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='ABNORMAL', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "abnormal"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='NOTED', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "noted"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='DX', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "dx"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='SENSITIVE', category='POSITIVE', direction="BIDIRECTIONAL", pattern=[{"LOWER": "sensitive"}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),
    ConTextRule(literal='+', category='POSITIVE', direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "high\\s*polysomy|\\(\\s*\\+\\s*\\)"}}]
                #, terminated_by={"NEGATIVE_EXISTENCE"}
                ),

]

