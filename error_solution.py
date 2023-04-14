from transformers import TFT5ForConditionalGeneration, RobertaTokenizer

class Args:
    train_batch_size = 8
    validation_batch_size = 8
    max_input_length = 48
    max_target_length = 128
    prefix = "Generate Python: "    

    save_dir="path/to/saved_model"

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
    print("#" * 25); print("QUERY: ", text); 
    print()
    print('#' * 25); print("GENERATED: "); print("\n", decoded_code);
