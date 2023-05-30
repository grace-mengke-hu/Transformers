from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
example = {
    "id": "0",
    "ner_tags": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        7,
        8,
        8,
        0,
        7,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
    "tokens": [
        "@paulwalk",
        "It",
        "'s",
        "the",
        "view",
        "from",
        "where",
        "I",
        "'m",
        "living",
        "for",
        "two",
        "weeks",
        ".",
        "Empire",
        "State",
        "Building",
        "=",
        "ESB",
        ".",
        "Pretty",
        "bad",
        "storm",
        "here",
        "last",
        "evening",
        ".",
    ],
}
tokenized_input = tokenizer(example["tokens"], is_split_into_words=True)
tokens = tokenizer.convert_ids_to_tokens(tokenized_input["input_ids"])
# print(tokens)


def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"], truncation=True, is_split_into_words=True
    )  # 'input_ids': [101,1030...]
    # print(tokenized_inputs)

    labels = []
    for i, label in enumerate(examples[f"ner_tags"]):
        word_ids = tokenized_inputs.word_ids(
            batch_index=i
        )  # Map tokens to their respective word.
        print("i:", i, "label:", label, "word_ids:", word_ids)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif (
                word_idx != previous_word_idx
            ):  # Only label the first token of a given word.
                print("word_idx:", word_idx)
                label_ids.append(word_idx)
                # label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


tokenizedInput = tokenize_and_align_labels(example)
# print(tokenizedInput)
