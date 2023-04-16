import os
import json
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from transformers import TFT5ForConditionalGeneration, RobertaTokenizer

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class Args:
    train_batch_size = 8
    validation_batch_size = 8
    max_input_length = 48
    max_target_length = 128
    prefix = "Generate Python: "    

    save_dir="C:\\Users\\NAGARAJAN K\\Desktop\\NLPCE\\saved_model"

args = Args()

def run_predict(args, text):
    model = TFT5ForConditionalGeneration.from_pretrained(args.save_dir)
    tokenizer = RobertaTokenizer.from_pretrained(args.save_dir) 

    query = args.prefix + text 
    encoded_text = tokenizer(query, return_tensors='tf', padding='max_length', truncation=True, max_length=args.max_input_length)

    generated_code = model.generate(
        encoded_text["input_ids"], attention_mask=encoded_text["attention_mask"], 
        max_length=args.max_target_length, top_p=0.95, top_k=50, repetition_penalty=2.0, num_return_sequences=1
    )

    decoded_code = tokenizer.decode(generated_code.numpy()[0], skip_special_tokens=True)
    return decoded_code

def predict_from_text(args, text):
    decoded_code = run_predict(args, text)
    return decoded_code

# file_structure_str = predict_from_text(args, "python flask app")
# file_structure = json.loads(file_structure_str)
# print(file_structure_str)
# sol=predict_from_text(args, "python flask app")
# print(sol)
# print(predict_from_text(args, '''"build portfolio using flask." <FILE_STRUCTURE> "{"app.py": "", "templates": {"about.html": "", "add.html": "", "error.html": "", "layout.html": "", "navbar.html": "", "portfolio.html": "", "result.html": "", "student.html": ""}}"'''))