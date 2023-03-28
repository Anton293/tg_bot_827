import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


dataset = [("это не спам", 0), ("ето спам", 1)]


with open("спам.txt", "r") as f:
    rows = f.read().split("\n")
    dataset = list(map(lambda x: (x.split("||")[1], x.split("||")[0]), rows))
    print(dataset)

# Загружаем данные

# Преобразовываем текст в векторы
texts = [d[0] for d in dataset]
labels = [d[1] for d in dataset]
encoder = LabelEncoder()
encoder.fit(labels)
labels = encoder.transform(labels)

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Создаем словарь
vocab = set(' '.join(texts).split())

# Преобразовываем тексты в числовые векторы
word_to_index = {word: i for i, word in enumerate(vocab, start=1)}
X_train_num = [[word_to_index[word] for word in text.split()] for text in X_train]
X_test_num = [[word_to_index[word] for word in text.split()] for text in X_test]

# Определяем размерность входных данных
max_words = len(vocab)
max_len = max(len(x) for x in X_train_num)

# Преобразовываем входные данные в массивы numpy
X_train_pad = np.zeros((len(X_train_num), max_len), dtype=np.int)
for i, seq in enumerate(X_train_num):
    X_train_pad[i, :len(seq)] = seq

X_test_pad = np.zeros((len(X_test_num), max_len), dtype=np.int)
for i, seq in enumerate(X_test_num):
    X_test_pad[i, :len(seq)] = seq

# Создаем нейронную сеть
model = Sequential()
model.add(Dense(64, input_shape=(max_len,), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# Компилируем модель
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Обучаем модель
model.fit(X_train_pad, y_train, validation_data=(X_test_pad, y_test), epochs=10, batch_size=32)

# Оцениваем качество модели
score = model.evaluate(X_test_pad, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#new_message = "хочешь заработать деньги переходи по етой ссилке и качай мое приложение"
new_message = "сообщение, которое благодарит"
new_text_num = [[word_to_index[word]] for word in new_message.split()]
new_text_pad = np.zeros((len(new_text_num), max_len), dtype=np.int)
for i, seq in enumerate(new_text_num):
    new_text_pad[i, :len(seq)] = seq

result = model.predict(new_text_pad)
print(result)
