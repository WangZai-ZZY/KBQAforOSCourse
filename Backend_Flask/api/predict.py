import os
import logging
from tqdm import tqdm

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

from api.utils import load_tokenizer, get_intent_labels, get_slot_labels, get_split, PredData
from api.model import JointBERT

logger = logging.getLogger(__name__)


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def get_args(model_dir):
    return torch.load(os.path.join(model_dir, 'training_args.bin'))


def load_model(model_dir, args, device):
    # Check whether model exists
    if not os.path.exists(model_dir):
        raise Exception("Model doesn't exists! Train first!")

    try:
        model = JointBERT.from_pretrained(model_dir,
                                          args=args,
                                          intent_label_lst=get_intent_labels(),
                                          slot_label_lst=get_slot_labels())
        model.to(device)
        model.eval()
        logger.info("***** Model Loaded *****")
    except:
        raise Exception("Some model files might be missing...")

    return model


def convert_input_file_to_tensor_dataset(lines,
                                         args,
                                         tokenizer,
                                         pad_token_label_id,
                                         cls_token_segment_id=0,
                                         pad_token_segment_id=0,
                                         sequence_a_segment_id=0,
                                         mask_padding_with_zero=True):
    # Setting based on the current model type
    cls_token = tokenizer.cls_token
    sep_token = tokenizer.sep_token
    unk_token = tokenizer.unk_token
    pad_token_id = tokenizer.pad_token_id

    all_input_ids = []
    all_attention_mask = []
    all_token_type_ids = []
    all_slot_label_mask = []

    for words in lines:
        tokens = []
        slot_label_mask = []
        for word in words:
            word_tokens = tokenizer.tokenize(word)
            if not word_tokens:
                word_tokens = [unk_token]  # For handling the bad-encoded word
            tokens.extend(word_tokens)
            # Use the real label id for the first token of the word, and padding ids for the remaining tokens
            slot_label_mask.extend([pad_token_label_id + 1] + [pad_token_label_id] * (len(word_tokens) - 1))

        # Account for [CLS] and [SEP]
        special_tokens_count = 2
        if len(tokens) > args.max_seq_len - special_tokens_count:
            tokens = tokens[: (args.max_seq_len - special_tokens_count)]
            slot_label_mask = slot_label_mask[:(args.max_seq_len - special_tokens_count)]

        # Add [SEP] token
        tokens += [sep_token]
        token_type_ids = [sequence_a_segment_id] * len(tokens)
        slot_label_mask += [pad_token_label_id]

        # Add [CLS] token
        tokens = [cls_token] + tokens
        token_type_ids = [cls_token_segment_id] + token_type_ids
        slot_label_mask = [pad_token_label_id] + slot_label_mask

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real tokens are attended to.
        attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # Zero-pad up to the sequence length.
        padding_length = args.max_seq_len - len(input_ids)
        input_ids = input_ids + ([pad_token_id] * padding_length)
        attention_mask = attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
        token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)
        slot_label_mask = slot_label_mask + ([pad_token_label_id] * padding_length)

        all_input_ids.append(input_ids)
        all_attention_mask.append(attention_mask)
        all_token_type_ids.append(token_type_ids)
        all_slot_label_mask.append(slot_label_mask)

    # Change to Tensor
    all_input_ids = torch.tensor(all_input_ids, dtype=torch.long)
    all_attention_mask = torch.tensor(all_attention_mask, dtype=torch.long)
    all_token_type_ids = torch.tensor(all_token_type_ids, dtype=torch.long)
    all_slot_label_mask = torch.tensor(all_slot_label_mask, dtype=torch.long)

    dataset = TensorDataset(all_input_ids, all_attention_mask, all_token_type_ids, all_slot_label_mask)

    return dataset


def form_data(sentences, lines, slot_preds_list, intent_preds, intent_label_lst):
    for sentence, words, slot_preds, intent_pred in zip(sentences, lines, slot_preds_list, intent_preds):

        slot_words = ""
        slot_label = ""
        for word, pred in zip(words, slot_preds):
            if pred != 'O':
                slot_words = slot_words + word
                slot_label = pred[2:]

        pred_data = PredData(sentence, intent_label_lst[intent_pred], slot_words, slot_label.lower())
        return pred_data


def predict(model_dir, sentence):
    # load model and args
    args = get_args(model_dir)
    device = get_device()
    model = load_model(model_dir, args, device)
    logger.info(args)

    intent_label_lst = get_intent_labels()
    slot_label_lst = get_slot_labels()

    # Convert input file to TensorDataset 将输入文件转换为张量数据集
    pad_token_label_id = args.ignore_index
    tokenizer = load_tokenizer(args)

    sentences = [sentence]
    words = get_split(sentence.strip())
    lines = [words]
    dataset = convert_input_file_to_tensor_dataset(lines, args, tokenizer, pad_token_label_id)

    # Predict
    sampler = SequentialSampler(dataset)
    data_loader = DataLoader(dataset, sampler=sampler)

    all_slot_label_mask = None
    intent_preds = None
    slot_preds = None

    for batch in tqdm(data_loader, desc="Predicting"):
        batch = tuple(t.to(device) for t in batch)
        with torch.no_grad():
            inputs = {"input_ids": batch[0],
                      "attention_mask": batch[1],
                      "intent_label_ids": None,
                      "slot_labels_ids": None}
            if args.model_type != "distilbert":
                inputs["token_type_ids"] = batch[2]
            outputs = model(**inputs)
            _, (intent_logits, slot_logits) = outputs[:2]

            # Intent Prediction
            if intent_preds is None:
                intent_preds = intent_logits.detach().cpu().numpy()
            else:
                intent_preds = np.append(intent_preds, intent_logits.detach().cpu().numpy(), axis=0)

            # Slot prediction
            if slot_preds is None:
                if args.use_crf:
                    # decode() in `torchcrf` returns list with best index directly
                    slot_preds = np.array(model.crf.decode(slot_logits))
                else:
                    slot_preds = slot_logits.detach().cpu().numpy()
                all_slot_label_mask = batch[3].detach().cpu().numpy()
            else:
                if args.use_crf:
                    slot_preds = np.append(slot_preds, np.array(model.crf.decode(slot_logits)), axis=0)
                else:
                    slot_preds = np.append(slot_preds, slot_logits.detach().cpu().numpy(), axis=0)
                all_slot_label_mask = np.append(all_slot_label_mask, batch[3].detach().cpu().numpy(), axis=0)

    intent_preds = np.argmax(intent_preds, axis=1)

    if not args.use_crf:
        slot_preds = np.argmax(slot_preds, axis=2)

    slot_label_map = {i: label for i, label in enumerate(slot_label_lst)}
    slot_preds_list = [[] for _ in range(slot_preds.shape[0])]

    for i in range(slot_preds.shape[0]):
        for j in range(slot_preds.shape[1]):
            if all_slot_label_mask[i, j] != pad_token_label_id:
                slot_preds_list[i].append(slot_label_map[slot_preds[i][j]])

    for words, slot_preds, intent_pred in zip(lines, slot_preds_list, intent_preds):
        line = ""
        for word, pred in zip(words, slot_preds):
            if pred == 'O':
                line = line + word + " "
            else:
                line = line + "[{}:{}] ".format(word, pred)

        logger.info("***** Predict Output *****")
        logger.info("<{}> -> {}".format(intent_label_lst[intent_pred], line.strip()))

    pred_data = form_data(sentences, lines, slot_preds_list, intent_preds, intent_label_lst)
    logger.info("[Object] -> {}".format(pred_data))
    logger.info("***** Prediction Done *****")

    return pred_data
