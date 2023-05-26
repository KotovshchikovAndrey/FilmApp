import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
from transformers import AutoTokenizer
from transformers import TFAutoModel

# text = some user text
text = ""

tz = AutoTokenizer.from_pretrained("bert-base-cased")
list_of_encoded_x = tz(
    text=text,  # the sentence to be encoded
    add_special_tokens=True,  # Add [CLS] and [SEP]
    max_length=256,  # maximum length of a sentence
    pad_to_max_length=True,  # Add [PAD]s
    return_attention_mask=True,  # Generate the attention mask
    return_tensors="tf",
    truncation=True,
)

bert = TFAutoModel.from_pretrained("bert-base-uncased")
input_ids = tf.keras.layers.Input(shape=(256,), name="input_ids", dtype="int32")
mask = tf.keras.layers.Input(shape=(256,), name="attention_mask", dtype="int32")

embeddings = bert.bert(input_ids, attention_mask=mask)
embeddings[1]

model = tf.keras.Model(inputs=[input_ids, mask], outputs=embeddings[1])
