from transformers import (
    AutoConfig,
    BertTokenizerFast,  # fast tokenizer will return offsets
    BertForTokenClassification,
)
import torch

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


def bert_prediction_sentence(sent):
    encode_dic = tokenizer.encode_plus(
        sent,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
        return_offsets_mapping=True,
    )
    inputs = tokenizer.encode(
        sent, return_tensors="pt", max_length=512, truncation=True, padding=True
    )
    tokens = tokenizer.tokenize(
        tokenizer.decode(
            tokenizer.encode(sent, max_length=512, truncation=True, padding=True)
        )
    )

    offsets = encode_dic["offset_mapping"]
    offsetsList = offsets.tolist()

    # prediction for current sentence
    outputs = Model(inputs)[0]
    predictions = torch.argmax(outputs, dim=2)
    print(len(tokens), len(predictions[0].tolist()), len(offsetsList[0]))
    ids = predictions[0].tolist()
    offsetSent = []
    labelSent = []
    for i in range(len(ids)):
        labelSent.append(id2label[str(ids[i])])
        offsetSent.append(offsetsList[0][i])
        print(id2label[str(ids[i])], offsetsList[0][i])
    print(offsetsList[0], tokens)
    return labelSent, offsetSent


def gene_span(labels, offsets):
    spanList = []  # list of [startIndx,endIndx]
    for i in range(len(labels)):
        if labels[i] == "B-GENETIC":
            currentStart = offsets[i][0]
            # initial the span end
            currentEnd = offsets[i][1]
            j = 1
            while labels[i + j] == "I-GENETIC":
                currentEnd = offsets[i + j][1]
                j = j + 1
            spanList.append([currentStart, currentEnd])
    return spanList
