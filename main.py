import random
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset

# Load and preprocess
corpus = pd.read_csv("encrypted_corpus.csv")z
all_ciphers = set("".join(corpus["ciphers"].astype(str).tolist()))
all_plain = set("".join(corpus["word"].astype(str).tolist()))

cipher_to_idx = {char: idx for idx, char in enumerate(sorted(list(all_ciphers)))}
plain_to_idx = {char: idx for idx, char in enumerate(sorted(list(all_plain)))}

# Add special tokens
for tok in ("<PAD>", "<SOS>", "<EOS>"):
    if tok not in plain_to_idx:
        plain_to_idx[tok] = len(plain_to_idx)

pad_idx = plain_to_idx["<PAD>"]
sos_idx = plain_to_idx["<SOS>"]
eos_idx = plain_to_idx["<EOS>"]

cipher_lookup_size = len(cipher_to_idx)
plain_lookup_size = len(plain_to_idx)
embedding_dim = 16
hidden_size = 32

# Model components
cipher_embedding = nn.Embedding(cipher_lookup_size, embedding_dim)
plain_embedding = nn.Embedding(plain_lookup_size, embedding_dim)
encoder_lstm = nn.LSTM(embedding_dim, hidden_size, batch_first=True)
decoder_lstm = nn.LSTM(embedding_dim, hidden_size, batch_first=True)
output_proj = nn.Linear(hidden_size, plain_lookup_size)

criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)
params = (
    list(cipher_embedding.parameters())
    + list(plain_embedding.parameters())
    + list(encoder_lstm.parameters())
    + list(decoder_lstm.parameters())
    + list(output_proj.parameters())
)
optimizer = optim.Adam(params, lr=1e-3)

# Dataset class with <SOS>/<EOS> handling
class CipherDataset(Dataset):
    def __init__(self, df):
        self.samples = []
        for _, row in df.iterrows():
            ciph = row["ciphers"]
            plain = row["word"]
            if not isinstance(ciph, str) or not isinstance(plain, str):
                continue
            cipher_seq = [cipher_to_idx[ch] for ch in ciph if ch in cipher_to_idx]
            plain_seq = [plain_to_idx[ch] for ch in plain if ch in plain_to_idx]
            if len(cipher_seq) and len(plain_seq):
                cipher_tensor = torch.tensor(cipher_seq, dtype=torch.long)
                decoder_input = torch.tensor([sos_idx] + plain_seq, dtype=torch.long)
                target = torch.tensor(plain_seq + [eos_idx], dtype=torch.long)
                self.samples.append((cipher_tensor, decoder_input, target))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

# Collate function for three sequences
def collate_fn(batch):
    ciphers, dec_ins, targets = zip(*batch)
    cipher_padded = pad_sequence(ciphers, batch_first=True, padding_value=pad_idx)
    dec_in_padded = pad_sequence(dec_ins, batch_first=True, padding_value=pad_idx)
    target_padded = pad_sequence(targets, batch_first=True, padding_value=pad_idx)
    return cipher_padded, dec_in_padded, target_padded

dataset = CipherDataset(corpus)
loader = DataLoader(dataset, batch_size=64, shuffle=True, collate_fn=collate_fn)

# Training loop
for epoch in range(5):
    for cipher_batch, dec_in_batch, target_batch in loader:
        # Encoder
        cipher_embed = cipher_embedding(cipher_batch)
        _, (hn, cn) = encoder_lstm(cipher_embed)

        # Decoder
        dec_embed = plain_embedding(dec_in_batch)
        dec_outputs, _ = decoder_lstm(dec_embed, (hn, cn))
        logits = output_proj(dec_outputs)

        # Loss
        loss = criterion(logits.view(-1, plain_lookup_size), target_batch.view(-1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
