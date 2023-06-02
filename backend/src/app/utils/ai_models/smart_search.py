# from __future__ import annotations

# import numpy as np
# import tensorflow as tf
# from transformers import AutoTokenizer
# from transformers import TFAutoModel
# from sklearn.metrics.pairwise import cosine_similarity

# from app.core import config
# import time


# tz = AutoTokenizer.from_pretrained("bert-base-cased")

# bert = TFAutoModel.from_pretrained("bert-base-uncased")
# input_ids = tf.keras.layers.Input(shape=(256,), name="input_ids", dtype="int32")
# mask = tf.keras.layers.Input(shape=(256,), name="attention_mask", dtype="int32")

# embeddings = bert.bert(input_ids, attention_mask=mask)

# model = tf.keras.Model(inputs=[input_ids, mask], outputs=embeddings[1])
# vectors = np.load(config.UPLOAD_DIR + "/ai/films.npy", allow_pickle=True)


# def search_films(sentence: str):
#     time.sleep(15)
#     print("time over!")
#     encoded_input = tz(
#         text=sentence,  # the sentence to be encoded
#         add_special_tokens=True,  # Add [CLS] and [SEP]
#         max_length=256,  # maximum length of a sentence
#         pad_to_max_length=True,  # Add [PAD]s
#         return_attention_mask=True,  # Generate the attention mask
#         return_tensors="tf",
#     )
#     in_vector = model.predict(
#         {
#             "input_ids": encoded_input["input_ids"],
#             "attention_mask": encoded_input["attention_mask"],
#         }
#     )

#     distance = 1000000
#     best_film = -1
#     for i in range(20000):
#         current_distance = 1 - cosine_similarity(in_vector, vectors[i])[0][0]
#         if current_distance < distance:
#             distance = current_distance
#             best_film = i

#     return best_film
