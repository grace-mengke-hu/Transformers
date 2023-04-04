from transformers import (
    AutoConfig,
    BertTokenizerFast,  # fast tokenizer will return offsets
    BertForTokenClassification,
)
import biobert_fun

# model path
model_path = "/Users/u6022257/Documents/Transformers/models/biobert_genetic_ner/"
tokenizer_config = model_path + "tokenizer_config.json"
model_config = model_path + "config.json"
vocab_file = model_path + "vocab.txt"

# load existing bert models saved in pytorch.bin
config_model = AutoConfig.from_pretrained(model_config)
tokenizer = BertTokenizerFast(vocab_file, do_lower_case=True)
Model = BertForTokenClassification.from_pretrained(model_path, local_files_only=True)
id2label = {"0": "B-GENETIC", "1": "I-GENETIC", "2": "O"}
label2id = {"B-GENETIC": 0, "I-GENETIC": 1, "O": 2}
print(tokenizer.is_fast)

# prediction on one sentence
# Remark: for long document, sentencizer must perform before bert
test_sent = "He is detected HRR positive. His cousin has BRAC negative."
tokens = tokenizer.tokenize(
    tokenizer.decode(
        tokenizer.encode(test_sent, max_length=512, truncation=True, padding=True)
    )
)
print("SENTENCE:", test_sent)
print("BERT TOKENS:", tokens)
labelSent, offsetSent = biobert_fun.bert_prediction_sentence(test_sent)
print("BERT PREDICTION LABEL AND OFFSETS:")
for (l, o) in zip(labelSent, offsetSent):
    print((l, o))
print("LABEL SPANS:")
spanList = biobert_fun.gene_span(labelSent, offsetSent)
for sp in spanList:
    print(test_sent[sp[0] : sp[1]])
