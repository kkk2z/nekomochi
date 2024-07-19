from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import sqlite3
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

# データベース接続
conn = sqlite3.connect('chat_logs.db')

# データベースからチャットログを読み込んでCSVに保存
df = pd.read_sql_query("SELECT user_input, bot_response FROM chat_logs", conn)
df.to_csv('chat_logs.csv', index=False)

# トークナイザとモデルの読み込み
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def train_model():
    # チャットログデータセットの読み込み
    data = load_dataset('csv', data_files='chat_logs.csv')

    # データコレクタとトレーナーの設定
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    training_args = TrainingArguments(output_dir='./results', overwrite_output_dir=True, num_train_epochs=1, per_device_train_batch_size=2)
    trainer = Trainer(model=model, args=training_args, data_collator=data_collator, train_dataset=data['train'])

    # モデルの再学習
    trainer.train()
    model.save_pretrained(model_name)
    tokenizer.save_pretrained(model_name)

if __name__ == "__main__":
    train_model()
