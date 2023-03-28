import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from transformers import AutoTokenizer, AutoModel
import numpy as np

# данные
questions = [
    "Кто ты?",
    "Что ты можешь?",
    "Сколько тебе лет?",
    "Как тебя зовут?"
]

answers = [
    "Я бот, возможно я смогу тебе чемто помочь",
    "Я могу отвечать на ваши вопросы, я правда ещо учусь ето делать поетому могу делать много странних ошибок",
    "Странный вопрос, я же бот",
    "Я асистент в етом чате, можешь меня називавать Huhu или асистент"
]


# Создание класса Dataset
class QADataset(Dataset):
    def __init__(self, questions, answers, tokenizer):
        self.questions = questions
        self.answers = answers
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        encoded = self.tokenizer(self.questions[idx], self.answers[idx], padding='max_length', truncation=True,
                                 max_length=512, return_tensors='pt')
        input_ids = encoded['input_ids'][0]
        attention_mask = encoded['attention_mask'][0]
        return input_ids, attention_mask


# Создание модели
class QAModel(nn.Module):
    def __init__(self, model_name):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.decoder = nn.Linear(self.encoder.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        logits = self.decoder(last_hidden_state)
        return logits.squeeze(1)


# Обучение модели
model_name = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)

dataset = QADataset(questions, answers, tokenizer)
loader = DataLoader(dataset, batch_size=1, shuffle=True)

model = QAModel(model_name)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    running_loss = 0.0
    for input_ids, attention_mask in loader:
        optimizer.zero_grad()
        logits = model(input_ids, attention_mask)
        targets = torch.tensor([1.0])  # Ожидаемый ответ - 1
        loss = criterion(logits, targets)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch + 1} loss: {running_loss / len(loader)}")


# Генерация ответов на новых вопросах
def generate_answer(question, model, tokenizer, answers):
    encoded = tokenizer(question, padding='max_length', truncation=True, max_length=512, return_tensors='pt')
    input_ids = encoded['input_ids'][0]
    attention_mask = encoded['attention_mask'][0]
    logits = model(input_ids.unsqueeze(0), attention_mask.unsqueeze(0)).detach().cpu().numpy()
    index = np.argmax(logits)
    answer = answers[index]
    # Редактируем ответ под вопрос
    if "[time]" in answer:
        answer = answer.replace("[time]", "12:00 pm")  # Здесь можно использов
    answer = answer.format(question.split()[0])
    return answer


while True:
    new_question = input("Enter answer: ")
    try:
        print(generate_answer(new_question, model, tokenizer, answers))
    except:
        print("Fall")
