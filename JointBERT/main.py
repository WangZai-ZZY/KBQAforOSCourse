import argparse

from trainer import Trainer
from utils import init_logger, load_tokenizer, set_seed
from data_loader import load_and_cache_examples


def main(args):
    init_logger()  # 初始化日志
    set_seed(args)  # 初始化随机数种子
    tokenizer = load_tokenizer(args)  # 初始化分词器

    train_dataset = load_and_cache_examples(args, tokenizer, mode="train")  # 设置训练集
    dev_dataset = load_and_cache_examples(args, tokenizer, mode="dev")  # 设置验证集
    test_dataset = load_and_cache_examples(args, tokenizer, mode="test")  # 设置测试集

    trainer = Trainer(args, train_dataset, dev_dataset, test_dataset)

    if args.do_train:
        trainer.train()

    if args.do_eval:
        trainer.load_model()
        trainer.evaluate("test")


# python main.py --task osqa --model_dir osqa_model --do_train --do_eval
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--task", default=None, required=True, type=str, help="The name of the task to train")
    parser.add_argument("--model_dir", default=None, required=True, type=str, help="Path to save, load model")

    parser.add_argument('--seed', type=int, default=1312, help="random seed for initialization")
    parser.add_argument("--train_batch_size", default=8, type=int, help="Batch size for training.")
    parser.add_argument("--eval_batch_size", default=4, type=int, help="Batch size for evaluation.")
    parser.add_argument("--max_seq_len", default=50, type=int,
                        help="The maximum total input sequence length after tokenization.")
    parser.add_argument("--learning_rate", default=5e-5, type=float, help="The initial learning rate for Adam.")
    parser.add_argument("--num_train_epochs", default=10.0, type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--weight_decay", default=0.0, type=float, help="Weight decay if we apply some.")
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float, help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float, help="Max gradient norm.")
    parser.add_argument("--max_steps", default=-1, type=int,
                        help="If > 0: set total number of training steps to perform. Override num_train_epochs.")
    parser.add_argument("--warmup_steps", default=0, type=int, help="Linear warmup over warmup_steps.")
    parser.add_argument("--dropout_rate", default=0.1, type=float, help="Dropout for fully-connected layers")

    parser.add_argument('--logging_steps', type=int, default=4, help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=4, help="Save checkpoint every X updates steps.")

    parser.add_argument("--do_train", action="store_true", help="Whether to run training.")
    parser.add_argument("--do_eval", action="store_true", help="Whether to run eval on the test set.")
    parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")

    parser.add_argument("--ignore_index", default=0, type=int,
                        help='Specifies a target value that is ignored and does not contribute to the input gradient')

    parser.add_argument('--slot_loss_coef', type=float, default=1.0, help='Coefficient for the slot loss.')

    # CRF option
    parser.add_argument("--use_crf", action="store_true", help="Whether to use CRF")
    parser.add_argument("--slot_pad_label", default="PAD", type=str,
                        help="Pad token for slot label pad (to be ignore when calculate loss)")

    args = parser.parse_args()

    args.model_type = 'bert'
    args.model_name_or_path = 'hfl/chinese-bert-wwm-ext'

    args.data_dir = './data'
    args.intent_label_file = 'intent_label.txt'
    args.slot_label_file = 'slot_label.txt'
    main(args)
