from transformers import AutoConfig, TFBertTokenizer, BertTokenizer,BertForTokenClassification #pytorch package
import torch
from spacy.tokens import Doc
from spacy.vocab import Vocab
import medspacy
import rules
from medspacy.context import ConTextRule

#folder path
model_path = "O:/VINCI_CancerNLP/3_Projects/BiomarkerExtraction/models/biobert_genetic_ner/biobert_genetic_ner/"
tokenizer_config = model_path+"tokenizer_config.json"
model_config = model_path+"config.json"
vocab_file = model_path+"vocab.txt"

#load the model
config_model = AutoConfig.from_pretrained(model_config)
tokenizer = BertTokenizer(vocab_file,do_lower_case = True)
Model = BertForTokenClassification.from_pretrained(model_path, local_files_only=True)

#nlp pipeline
nlp = medspacy.load()
if not ("medspacy_context" in nlp.pipe_names):
    context = nlp.add_pipe("medspacy_context")
else:
    context = nlp.get_pipe("medspacy_context")
context.add(rules.context_rules)
print(nlp.pipe_names)
if 'transformer' in nlp.pipe_names:
    nlp.remove_pipe('transformer')
print(nlp.pipe_names)


id2label = {
    "0": "B-GENETIC",
    "1": "I-GENETIC",
    "2": "O"
  }
label2id = {
    "B-GENETIC": 0,
    "I-GENETIC": 1,
    "O": 2
  }

"""
tokens: list of strings; output of tokenizer
labels: list of integers; predicted label
return: tOut: list of clean tokens(string)
        lOut: list of labels(string)
This function will remove masks and remove noises from the BertTokenizer
"""
def token_label_processing(tokens,labels):
    specialTag = ['[UNK]', '[SEP]', '[PAD]', '[CLS]', '[MASK]']
    tOut = []
    lOut = []
    print("The Length of Tokens and labels:",len(tokens),len(labels))
    for i in range(len(labels)):
        #print("BEFORE IF:",tokens[i],labels[i],i)
        if not (str(tokens[i]) in specialTag):
            #print(tokens[i],labels[i],i)
            lOut.append(id2label[str(labels[i])])
            tOut.append(str(tokens[i]).replace('##',''))
    return tOut, lOut

#now process documents
doc = nlp("He has HRR but not CHEK2.")
lenList = []
for s in doc.sents:
    #print("NEW SENTENCE----")
    #print(len(s),s)
    lenList.append(len(s))
print(max(lenList))
#print(df['reporttext'][0])
tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode("He has HRR but not CHEK2.", max_length=512,truncation=True)))
inputs = tokenizer.encode("He has HRR but not CHEK2.",return_tensors="pt",max_length=512,truncation=True)
#outputs = Model(inputs)[0]
#predictions = torch.argmax(outputs,dim=2)
#print(inputs)
print(len(tokens))
