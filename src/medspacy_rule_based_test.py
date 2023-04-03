import medspacy
import rules
from medspacy.ner import TargetRule # this is for exact match when using `literal`
from medspacy.context import ConTextRule

test_text = "He has CHEK2 but not have HRR."

nlp = medspacy.load(medspacy_enable = ["medspacy_pyrush"])
# add target matcher to the pipeline
target_matcher = nlp.add_pipe('medspacy_target_matcher') #this is for gene detection
target_matcher.add(rules.HRR_pattern_rules)
print(nlp.pipe_names)
#check if pipeline already has the context component in the pipeline
if "medspacy_context" in nlp.pipe_names:
    context = nlp.get_pipe("medspacy_context")
else:
    context = nlp.add_pipe("medspacy_context")
context.add(rules.context_rules)
print(nlp.pipe_names)

testDoc = nlp(test_text)
for ent in testDoc.ents:
    print(ent, ent._.modifiers, ent.sent)
    print(type(ent._.modifiers)) # This is a list
    #print(ent._.is_negated)
    #print(ent._.modifiers[1].category,ent._.modifiers[1]._start,ent._.modifiers[1]._end)