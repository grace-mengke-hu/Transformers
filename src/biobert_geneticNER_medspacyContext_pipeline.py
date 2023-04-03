import medspacy
import spacy
import pandas as pd
import biobert_fun
import sample_notes
import rules

# pytorch package
import torch
from transformers import (
    AutoConfig,
    BertTokenizerFast,  # fast tokenizer will return offsets
    BertForTokenClassification,
)


# folder path
model_path = "/Users/u6022257/Documents/Transformers/models/biobert_genetic_ner/"
tokenizer_config = model_path + "tokenizer_config.json"
model_config = model_path + "config.json"
vocab_file = model_path + "vocab.txt"
config_model = AutoConfig.from_pretrained(model_config)
tokenizer = BertTokenizerFast(vocab_file, do_lower_case=True)
Model = BertForTokenClassification.from_pretrained(model_path, local_files_only=True)
id2label = {"0": "B-GENETIC", "1": "I-GENETIC", "2": "O"}
label2id = {"B-GENETIC": 0, "I-GENETIC": 1, "O": 2}
print(tokenizer.is_fast)

# nlp_blank = spacy.blank("en")
nlp = medspacy.load()
# add pyrush for sentencizer. It is slow but accurate for clinical data.
if not ("medspacy_pyrush" in nlp.pipe_names):
    nlp.add_pipe("medspacy_pyrush")
print(nlp.pipe_names)
# context
if "medspacy_context" in nlp.pipe_names:
    context = nlp.get_pipe("medspacy_context")
else:
    context = nlp.add_pipe("medspacy_context")
context.add(rules.context_rules)
print(nlp.pipe_names)

# Processing 1 Note from pipeline
doc = nlp(sample_notes.text)  # break into sentences for BERT
ents = []
for sent in doc.sents:  # go through sentences
    # check if a sentence is full of whitespaces
    if not (sent.text.isspace()):
        # get BERT NER label and the offsets of each token
        labelSent, offsetSent = biobert_fun.bert_prediction_sentence(sent.text)
        # get entire span from BIO labels
        spanList = biobert_fun.gene_span(labelSent, offsetSent)
        print("CURRENT SENT:", sent, spanList, labelSent, offsetSent)
        # spanList is not empty; It is list of lists
        if spanList:
            print("FIND GENE!!:", spanList)
            for ind in spanList:
                # label valid span: ..alignment_mode = "expand") #only spacy>V3.5 has this option
                auxSpan = sent.char_span(ind[0], ind[1], label="GENETIC")
                print(auxSpan)
                if auxSpan is None:
                    print("FAILED TO ADD ENTITY")
                else:
                    ents.append(auxSpan)
                    print("ADD GENETIC SPAN TO ENTITY!")

doc.ents = ents

# contextual detection
contextDoc = context(doc)
for ent in doc.ents:
    print(ent, ent.start_char, ent.end_char, ent._.modifiers)
    # ent._.modifiers[0].category)
    print("===" * 10)
