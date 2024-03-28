######### INCOMPLETE
import regex as re

class GPT_tokenizer:
    def __init__(self, vocab_size=276):
        self.vocab_size = vocab_size # final desired vocab size
        self.num_original_tokens = 256 # 256 is original vocab size, which is 0-255 (a byte)
        self.num_merges = vocab_size - self.num_original_tokens 
        self.merge_record = None

    def get_utf_encoding(self, split_list):
        """
        Converts text to utf-8 encoding and then to integer values(0-255)
        """
        full_text_tokens = []
        for subtext in split_list:
            tokens = subtext.encode('utf-8')
            tokens = list(map(int, tokens))
            full_text_tokens.extend(tokens)
        return full_text_tokens
    
    def get_most_frequent_pair(self, tokens):
        """
        Returns pair with highest occurences
        """
        counts = {}
        for pair in zip(tokens, tokens[1:]):
            counts[pair] = counts.get(pair, 0) + 1

        pair = max(counts, key=counts.get)        
        return pair
    
    def merge(self, tokens, pair, new_token):
        """
        Replace pair occurences in tokens with new_token
        """
        for idx, p in enumerate(zip(tokens, tokens[1:])):
            if p==pair:
                tokens[idx]=new_token
                tokens[idx+1]=-1

        tokens = [i for i in tokens if i!=-1]
        return tokens

    def gpt_style_split(self, text):
        gpt2pattern = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")
        split_list = re.findall(gpt2pattern, text)
        return split_list


    def encode(self, text):
        split_list = self.gpt_style_split(text)
        original_tokens = self.get_utf_encoding(split_list)
        tokens = original_tokens.copy()
        self.merge_record = {}
        for i in range(self.num_merges):
            new_token = self.num_original_tokens + i
            pair = self.get_most_frequent_pair(tokens)
            print(f"Merging {pair} into a new token {new_token}")
            tokens = self.merge(tokens, pair, new_token)
            self.merge_record[pair] = new_token

        self.merge_record = {v:k for k,v in self.merge_record.items()} # lookup dictionary for decoding
        return tokens
    
    def decode(self, tokens):
        if bool(self.merge_record):
            idx=0
            while(idx!=len(tokens)-1):
                token = tokens[idx]
                if token in self.merge_record.keys():
                    pair = self.merge_record[token]
                    tokens[idx] = pair[0]
                    tokens.insert(idx+1, pair[1])

                else:
                    idx=idx+1
        else:
            pass
        
        bytes_encoded = bytes(tokens)
        text = bytes_encoded.decode("utf-8", errors="replace") 
        return text

if __name__=="__main__":
    tokenizer = GPT_tokenizer()
    text = "💡 Illuminate your path with 𝓌𝒾𝓈𝒹𝑜𝓂 and insight, 💡 guiding you towards 𝕘𝕣𝕖𝕒𝕥𝕟𝕖𝕤𝕤. 🌟🔮 🌈 Let your imagination soar beyond the stars 🚀 as you embrace the journey of 𝓭𝓲𝓼𝓬𝓸𝓿𝓮𝓻𝔂 and creativity. 🌟💫"
    tokenized_text = tokenizer.encode(text)
    non_existing_token = tokenizer.decode([128])
    print(non_existing_token)
    decoded_text = tokenizer.decode(tokenized_text)
    print(decoded_text)