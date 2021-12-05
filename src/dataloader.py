import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd


def split_train_val(df: pd.DataFrame, props=[.8, .2], shuffle=True):
    assert round(sum(props), 2) == 1 and len(props) == 2
    # return values
    train_df, val_df = None, None

    ## YOUR CODE STARTS HERE (~6-10 lines of code)
    # hint: you can use df.iloc to slice into specific indexes
    N = df.shape[0]
    train_df = df.iloc[:int(N*props[0])]
    val_df = df.iloc[int(N*props[0]):]
    ## YOUR CODE ENDS HERE ##

    return train_df, val_df


def defaultTokenizer(sentence):
    return sentence.split(' ')

# Special tokens
SOS_token = 0
EOS_token = 1
UNK_token = 2
SEP_token = 3

class Lang:
    def __init__(self, tokenizer=defaultTokenizer):
        """
        Initialize variables to maintain language statistics
            Obtained from https://pytorch.org/tutorials/beginner/chatbot_tutorial.html#define-training-procedure
        Args:
            tokenizer: could be substituted according to specific language needs
                the default tokenizer will suffice for this assignment since the 
                data is already cleaned but if you use this template elsewhere, 
                you may want to substitute a different tokenizer
        """
        self.word2index = {"UNK": UNK_token,
                            "EOS" : EOS_token,
                            "SOS" : SOS_token,
                            "SEP" : SEP_token}
        # counts can be used to update dataset to use filter dataset samples by frequency
        self.word2count = {"UNK": 0, "SEP": 0}
        self.trimmed = False
        self.index2word = {SOS_token: "SOS",
                           EOS_token: "EOS", 
                           UNK_token: "UNK",
                           SEP_token: "SEP"}
        self.n_words = len(self.word2index)  # Count SOS, EOS, UNK, and SEP tokens
        self.tokenizer = tokenizer

    def addQuestion(self, tokenized_question):
        # print(tokenized_dialogue)
        for word in tokenized_question:
            # print(word)
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def getIndexFromWord(self, word):
        if word in self.word2index:
            return self.word2index[word]
        else:
            return self.word2index["UNK"]

    def getWordFromIndex(self, index):
        word = self.index2word[index] if index in self.index2word else "UNK"
        return word

    def getWordsFromIndices(self, indices):
        return [self.getWordFromIndex(idx) for idx in indices]
    
    def trim(self, min_count, keep=set()):
        if self.trimmed:
            return
        self.trimmed = True

        keep_words = list(keep)

        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words {} / {} = {:.4f}'.format(
            len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        ))

        # Reinitialize dictionaries
        self.word2index = {"UNK": UNK_token,
                            "EOS" : EOS_token,
                            "SOS" : SOS_token,
                            "SEP" : SEP_token}
        self.word2count = {}
        self.index2word = {SOS_token: "SOS",
                           EOS_token: "EOS", 
                           UNK_token: "UNK",
                           SEP_token: "SEP"}
        self.n_words = len(self.word2index)  # Count SOS, EOS, UNK, and SEP tokens

        for word in keep_words:
            self.addWord(word)

def initLang(characters, df, verbose=True):
    """
    Initialize Lang object, create word indices and update counts
    """
    lang = Lang()

    # Initialize vocabulary from dialogue
    cols = df.columns.tolist()
    for c in cols:
        df[c].apply(lang.addQuestion)
        print('initializing:', c, "| total_vocab_size:", len(lang.word2index))
    
    return lang

# Create Dataloader
class MathWordProblemDataset(Dataset):
    def __init__(self, df: pd.DataFrame, lang: Lang, context_col:str, target_col:str, MAX_LEN=10) -> None:
        super().__init__()
        self.lang = lang
        self.df = df
        self.target_col = target_col
        self.input_col = context_col
        self.MAX_LEN = MAX_LEN
        assert self.input_col in self.df.columns
        assert self.target_col in self.df.columns

    def __len__(self) -> int:
        return len(self.df)
    
    def __getitem__(self, index: int):
        sample = self.df.iloc[index]
        input_sentence = sample[self.input_col]
        target_sentence = sample[self.target_col]
        input_tensor = None
        target_tensor = None
        input_sentence = input_sentence[-self.MAX_LEN+1:]
        target_sentence = target_sentence[:self.MAX_LEN-1]
        input = [self.lang.getIndexFromWord(w) for w in input_sentence] + [1]
        target = [self.lang.getIndexFromWord(w) for w in target_sentence] + [1]
        input_tensor = torch.Tensor(input).long()
        target_tensor = torch.Tensor(target).long()

        return {
            'input_tensor' : input_tensor,
            'target_tensor' : target_tensor
        }

def create_data_loader(df, lang: Lang, context_col:str, 
                        target_col:str, MAX_LEN:int = 10, shuffle=True):

    ds = MathWordProblemDataset(
        df = df, 
        lang = lang, 
        context_col = context_col, 
        target_col = target_col,
        MAX_LEN = MAX_LEN
    )

    return DataLoader(ds, batch_size=1, shuffle=shuffle)
