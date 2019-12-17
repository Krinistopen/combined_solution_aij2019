# AI Journey 2019: Combined Solution

Комбинация лучших решений топ-20 участников соревнования AI Journey 2019 по каждому заданию. Комбинированное решение набирает 69 баллов по ЕГЭ, русский язык.

## Банк данных и модели

Банк данных AI Journey 2019 содержит данные и материалы, которые могут быть использованы для решения AGI-задач и прикладных NLP-задач:

* Unified State Exam solving;
* text summarization;
* text generation;
* style transfer;
* punctuation restoring;
* grammar error correction;
* domain-specific language modeling;
* discourse analysis;
* topic modeling;
* text classification.
    
Для скачивания банка данных:

```
python download_data.py
```

Каталог ```models``` содержит модели и файлы для решения экзаменационных заданий.

Для скачивания каталога моделей:

```
python download_models.py
```

## Запуск docker контейнера

Запустить контейнер можно командой:
```
$ sudo docker run -w /workspace -v $(pwd):/workspace -p 8000:8000 -it alenush25/combined_solution_aij:latest python solution.py
```

Это поднимет решение, которое представляет собой HTTP-сервер, доступный по порту `8000`, со следующими запросами:

#### `GET /ready`

Запрос отвечает кодом `200 OK` в случае, если решение готово к работе. Любой другой код означает, что решение еще не готово.

#### `POST /take_exam`

Запрос на решение экзаменационного билета. Тело запроса — JSON объект экзаменационного билета в формате JSON соревнования (пример можно найти в папке `test_data`)

Запрос отвечает кодом `200 OK` и возвращает JSON-объект с ответами на задания.  

Запрос и ответ должны иметь `Content-Type: application/json`. Рекомендуется использовать кодировку UTF-8.

Прилагается также аутентичный файл для формата соревнования `metadata.json` следующего содержания:

```json
{
    "image": "alenush25/combined_solution_aij:latest",
    "entry_point": "python solution.py"
}
```

Здесь `image` — поле с названием docker-образа, в котором будет запускаться решение, `entry_point` — команда, при помощи которой запускается решение. Для решения текущей директорией будет являться корень архива.

Файл `eval_docker.py` сожержит пример загрузки и обработки JSON вариантов из папки `test_data` в решение.

## Формат описания решений

* ```Описание задания```: формулировка задания экзаменационного варианта;
* ```Тип задания```:
    * ```choice```: выбор одного варианта из списка;
    * ```multiple_choice```: выбор подмножества вариантов из списка;
    * ```order```: расстановка вариантов в правильном порядке;
    * ```matching```: верное соотнесение объектов из двух множеств;
    * ```text```: ответ в виде произвольного текста;
* ```Файл решения```: путь к файлу решения;
* ```Описание решения```: краткое описание лучшего решения;
* ```max_score```: максимальное количество баллов за задание;
* ```mean_score```: среднее количество баллов, которое набрало лучшее решение (private test); функции для оценки качества моделей находятся в ```evaluation_script.py```

## Описание решений

#### Задание 1

* ```Описание задания```: указать номера предложений, в которых передана главная информация, содержащаяся в тексте
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver1.py](solvers/solver1.py)
* ```Описание решения```: косинусная близость между эмбеддингами вариантов ответа на уровне предложения, полученных с помощью [BertEmbedder](solvers/utils.py#L52)
* ```max_score```: 1
* ```mean_score```: 0.7

#### Задание 2

* ```Описание задания```: подобрать слово-коннектор, которое должно быть на месте пропуска в указанном предложении
* ```Тип задания```: text
* ```Файл решения```: [solver2.py](solvers/solver2.py)
* ```Описание решения```: комбинация подхода на правилах и скоринга списка потенциальных кандидатов с помощью [RubertForMasking](solvers/utils.py#L134)  
* ```max_score```: 1
* ```mean_score```: 0.6

#### Задание 3

* ```Описание задания```: определить значение слова в заданном контексте, используя приведенный фрагмент словарной статьи
* ```Тип задания```: choice
* ```Файл решения```: [solver3.py](solvers/solver3.py)
* ```Описание решения```: косинусная близость между эмбеддингами текста и значениями слова, и эмбеддингами таргет-предложения и значениями слова ([Word2vecProcessor](solvers/utils.py#L389), ранжирование с использованием вручную подобранных весов для значений косинусной близости)
* ```max_score```: 1
* ```mean_score```: 0.7

#### Задание 4

* ```Описание задания```: определить слово, в котором верно или неверно поставлено ударение
* ```Тип задания```: text
* ```Файл решения```: [solver4.py](solvers/solver4.py)
* ```Описание решения```: комбинация ранжирования кандидатов на правилах и использования словаря ударений
* ```max_score```: 1
* ```mean_score```: 0.967

#### Задание 5

* ```Описание задания```: определить неверно употребленное выделенное слово и исправить лексическую ошибку, подобрав к выделенному слову пароним
* ```Тип задания```: text
* ```Файл решения```: [solver5.py](solvers/solver5.py)
* ```Описание решения```: извлечение фичей и ранжирование кандидатов с помощью словаря паронимов, морфологического анализа pymorphy2, частотности n-gram ([NgramManager](solvers/utils.py#L485)) и вручную составленных формул; выбор кандидата на основе вероятностного распределения (LogisticRegression)
* ```max_score```: 1
* ```mean_score```: 0.7

#### Задание 6

* ```Описание задания```: исправить лексическую ошибку в предложении, исключив или заменив неверно употребленное слово
* ```Тип задания```: text
* ```Файл решения```: [solver6.py](solvers/solver6.py)
* ```Описание решения```: комбинация правил на основе морфологического анализа pymorphy2 и косинусной близости между эмбеддингами биграм на уровне предложения, полученных с помощью [BertEmbedder](solvers/utils.py#L52)
* ```max_score```: 1
* ```mean_score```: 0.5

#### Задание 7

* ```Описание задания```: определить, в каком из выделенных слов допущена ошибка в образовании формы слова, исправить ошибку, записав слово правильно
* ```Тип задания```: text
* ```Файл решения```: [solver7.py](solvers/solver7.py)
* ```Описание решения```: комбинация подхода на правилах, использования словарей и ранжирования кандидатов с помощью морфологического анализа pymorphy2 и частотности n-gram ([NgramManager](solvers/utils.py#L485))
* ```max_score```: 1
* ```mean_score```: 0.9

#### Задание 8

* ```Описание задания```: установить соответствие между грамматическими ошибками и предложениями, в которых они допущены
* ```Тип задания```: matching
* ```Файл решения```: [solver8.py](solvers/solver8.py)
* ```Описание решения```: многоклассовая классификация с помощью fine-tuned [RubertMulticlassClassifier](solvers/torch_utils.py#L159)
* ```max_score```: 5
* ```mean_score```: 4.6

#### Задание 9

* ```Описание задания```: указать варианты ответов, в которых во всех словах одного ряда пропущена гласная корня в соответствиями с нормами правописания
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver9.py](solvers/solver9.py)
* ```Описание решения```: комбинация подхода на правилах и использования словарей и списков слов
* ```max_score```: 1
* ```mean_score```: 0.83


#### Задание 10

* ```Описание задания```: указать варианты ответов, в которых во всех словах одного ряда пропущена одна и та же буква
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver10.py](solvers/solver10.py)
* ```Описание решения```: комбинация подхода на правилах и использования списков слов и словарей pymorphy2
* ```max_score```: 1
* ```mean_score```: 0.96

#### Задание 11-12

* ```Описание задания```: указать варианты ответов, в которых во всех словах одного ряда пропущена одна и та же буква
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver11.py](solvers/solver11.py)
* ```Описание решения```: комбинация подхода на правилах и использования списков слов и словарей pymorphy2
* ```max_score```: 1
* ```mean_score```: 0.9, 0.77

#### Задание 13

* ```Описание задания```: определить предложение, в котором "не" со словом пишется слитно, и выписать это слово
* ```Тип задания```: text
* ```Файл решения```: [solver13.py](solvers/solver13.py)
* ```Описание решения```: комбинация [RubertFor13](solvers/torch_utils.py#L55) и словарей pymorphy2
* ```max_score```: 1
* ```mean_score```: 1

#### Задание 14

* ```Описание задания```: определить предложение, в котором оба выделенных слова пишутся слитно
* ```Тип задания```: text
* ```Файл решения```: [solver14.py](solvers/solver14.py)
* ```Описание решения```: ранжирование кандидатов с помощью морфологического анализа pymorphy2, частотности n-gram ([NgramManager](solvers/utils.py#L485)) и вручную составленных формул
* ```max_score```: 1
* ```mean_score```: 0.83

#### Задание 15

* ```Описание задания```: указать цифры, на месте которых пишется "нн" или "н"
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver15.py](solvers/solver15.py)
* ```Описание решения```: комбинация подхода на правилах, маскирования с помощью [RubertForMasking](solvers/utils.py#L134)  и использования списков слов и словарей pymorphy2
* ```max_score```: 1
* ```mean_score```: 0.8

#### Задание 16

* ```Описание задания```: указать номера предложений, в которых необходимо поставить одну запятую
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver16.py](solvers/solver16.py)
* ```Описание решения```: CatBoostClassifier, обученный на мешках частеречных тегов (CountVectorizer, pymorphy2)
* ```max_score```: 2
* ```mean_score```: 1.8

#### Задание 17-20

* ```Описание задания```: указать цифры, на месте которых в предложении должны стоять запятые
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver17.py](solvers/solver17.py)
* ```Описание решения```: маскирование пропусков в предложении и бинарная классификация с помощью fine-tuned [RubertClassifier](solvers/solver17.py#L79), который обучен для решения заданий 17-20
* ```max_score```: 4 (1, 1, 1, 1)
* ```mean_score```: 3.24 (0.9, 0.57, 0.87, 0.9)


#### Задание 21

* ```Описание задания```: найти предложения, в которых указанный знак пунктуации ставится в соответствии с одним и тем же правилом пунктуации
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver21.py](solvers/solver21.py)
* ```Описание решения```: классификация с помощью комбинации LightGBM и TfidfVectorizer
* ```max_score```: 1
* ```mean_score```: 0.5

#### Задание 22

* ```Описание задания```: определить, какие из высказываний не соответствуют содержанию текста
* ```Тип задания```: multiple_choice.
* ```Файл решения```: [solver22.py](solvers/solver22.py)
* ```Описание решения```: классификация с помощью комбинации C-Support Vector Classification и TfidfVectorizer
* ```max_score```: 1
* ```mean_score```: 0.63

#### Задание 23

* ```Описание задания```: определить верные или ошибочные утверждения относительно типов речи и логических связей между предложениями в тексте
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver23.py](solvers/solver23.py)
* ```Описание решения```: комбинация подхода на правилах и ансамбля, состоящего из моделей Logistic Regression
* ```max_score```: 1
* ```mean_score```: 0.33

#### Задание 24

* ```Описание задания```: найти указанную лексическую единицу или художественное средство в заданном диапазоне предложений текста
* ```Тип задания```: text
* ```Файл решения```: [solver24.py](solvers/solver24.py)
* ```Описание решения```: комбинация подхода на правилах, косинусной близости между word2vec эмбеддингами ([Word2vecProcessor](solvers/utils.py#L389)) и использования словарей и списков слов
* ```max_score```: 1
* ```mean_score```: 0.33

#### Задание 25

* ```Описание задания```: определить предложение, которое связано с предыдущим с помощью указанного коннектора
* ```Тип задания```: multiple_choice
* ```Файл решения```: [solver25.py](solvers/solver25.py)
* ```Описание решения```: классификация на правилах с использованием словарей и морфологического анализа pymorphy2
* ```max_score```: 1
* ```mean_score```: 0.77

#### Задание 26

* ```Описание задания```: установить соответствие между литературными терминами и предложениями рецензии, в которых описываются языковые особенности текста
* ```Тип задания```: matching
* ```Файл решения```: [solver26.py](solvers/solver26.py)
* ```Описание решения```: многоклассовая классификация с помощью fine-tuned [RubertMulticlassClassifier](solvers/torch_utils.py#L159)
* ```max_score```: 4
* ```mean_score```: 3

#### Задание 27

* ```Описание задания```: написать сочинение по тексту; сформулировать и проиллюстрировать примерами из текста одну из проблем, поставленных автором; сформулировать авторскую позицию; выразить свое отношение к позиции автора по проблемем исходного текста (согласие или несогласие); аргументировать свое отношение, приведя примеры из художественной литературы
* ```Тип задания```: text
* ```Файл решения```: [solver27.py](solvers/solver27.py)
* ```Описание решения```: комбинация определения темы текста на правилах, извлечения автора текста на правилах и заполнения композиционной структуры эссе с помощью вручную составленного набора тем, шаблонов, тезисов и аргументов
* ```max_score```: 24
* ```mean_score```: 16