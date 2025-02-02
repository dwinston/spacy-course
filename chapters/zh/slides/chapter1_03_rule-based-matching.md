---
type: slides
---

# 基于规则的匹配

Notes: 本节课我们一起来学习spaCy的matcher，
用它来写一些规则来寻找文本中的目标词汇和短语。

---

# 为何不直接用正则表达式？

- 我们是在`Doc`对象中而不是直接在字符串上做匹配
- 我们是在词符及其属性中做匹配
- 我们会用到模型的预测结果
- 举个例子，"duck" (动词) vs. "duck" (名词)是不一样的（"duck"名词意思是鸭子，而动词是闪避的意思）

Notes: 与正则表达式相比，matcher是配合`Doc`和`Token`这样的方法来使用的，
而不是只作用于字符串上。

同时matcher使用上也更加灵活：我们不只可以搜索文本，也可以搜索其它的词法属性。

我们甚至可以直接调用模型的预测结果来写规则。
You can even write rules that use the model's predictions.

比如，寻找那些是动词而不是名词的"duck"词汇

---

# 模板匹配

- 一个元素是字典的列表，一个词符是一个元素

- 匹配词符的完全一致的文字

```python
[{"TEXT": "iPhone"}, {"TEXT": "X"}]
```
- 匹配词汇属性

```python
[{"LOWER": "iphone"}, {"LOWER": "x"}]
```

- 匹配任意的词符属性

```python
[{"LEMMA": "buy"}, {"POS": "NOUN"}]
```

Notes: 匹配的模板是一些列表，列表的每一个元素是一个字典。
每个字典代表一个词符，键值是词符属性名，映射到对应的目标值上面。

这个例子里我们要找两个文本为"iPhone"和"X"的词符。

我们也可以去匹配其它的词符属性。这里我们找两个小写形式为"iphone"和"x"的词符。

我们甚至可以直接调用模型的预测结果来写规则。这里我们找一个词根为"buy"且后面为名词的词符。
词根是词的基础形式，所以这个模板会匹配到诸如"buying milk"或者"bought flowers"这样的短语。

---

# 使用Matcher (1)

```python
import spacy

# 导入Matcher
from spacy.matcher import Matcher

# 读取一个模型，创建nlp实例
nlp = spacy.load("en_core_web_sm")

# 用模型分享出的vocab初始化matcher
matcher = Matcher(nlp.vocab)

# 给matcher加入模板
pattern = [{"TEXT": "iPhone"}, {"TEXT": "X"}]
matcher.add("IPHONE_PATTERN", None, pattern)

# 处理文本
doc = nlp("Upcoming iPhone X release date leaked")

# 在doc上面调用matcher
matches = matcher(doc)
```

Notes: 要使用模板我们首先从`spacy.matcher`中导入matcher。

我们还要读取一个模型创界`nlp`实例。

用模型分享出来的词汇表`nlp.vocab`来初始化matcher。
我们后面会详细介绍这一块，现在只要记得一定要传入这个词汇表就好了。

`matcher.add`方法可以用来添加一个模板。第一个参数是唯一的ID用来识别匹配的是哪一个模板。
第二个参数是一个可选的回调参数，这里我们不需要所以设置其为`None`。
第三个参数是模板本身。

要在文本中匹配模板，我们可以在任何doc中调用matcher。

这样就会返回所有的匹配结果。

---

# 使用Matcher (2)

```python
# 在doc上调用matcher
doc = nlp("Upcoming iPhone X release date leaked")
matches = matcher(doc)

# 遍历所有的匹配结果
for match_id, start, end in matches:
    # 获取匹配的跨度
    matched_span = doc[start:end]
    print(matched_span.text)
```

```out
iPhone X
```

- `match_id`: 模板名的哈希值
- `start`: 匹配到的跨度的起始索引
- `end`: 匹配到的跨度的终止索引

Notes: 当你对doc调用matcher时会返回一个列表，列表中的每个元素是一个元组(tuple)。

每个元组由三个值构成：匹配到的ID，匹配到的跨度的起始和终止索引

这意味着我们可以对所有的匹配结果进行遍历，然后创建`Span`实例。
这个实例即为doc被起始和终止索引截取的部分。

---

# 匹配词汇属性

```python
pattern = [
    {"IS_DIGIT": True},
    {"LOWER": "fifa"},
    {"LOWER": "world"},
    {"LOWER": "cup"},
    {"IS_PUNCT": True}
]
```

```python
doc = nlp("2018 FIFA World Cup: France won!")
```

```out
2018 FIFA World Cup:
```

Notes: 这是一个用到词汇属性的更复杂的匹配模板的例子。

我们要找五个词符：

一个只含有数字的词符；

三个对大小写不敏感的匹配到"fifa", "world"和"cup"的词符；

以及一个标点符号词符。

这个模板最后可以匹配到"2018 FIFA World Cup:"。

---

# 匹配其它的词符属性

```python
pattern = [
    {"LEMMA": "love", "POS": "VERB"},
    {"POS": "NOUN"}
]
```

```python
doc = nlp("I loved dogs but now I love cats more.")
```

```out
loved dogs
love cats
```

Note: 这个例子中我们寻找两个词符：

一个词根是"love"的动词，后面跟着一个名词。

这个模板最后可以匹配到"loved dogs"和"love cats"。

---

# 使用运算符和量词 (1)

```python
pattern = [
    {"LEMMA": "buy"},
    {"POS": "DET", "OP": "?"},  # 可选: 匹配0次或者1次
    {"POS": "NOUN"}
]
```

```python
doc = nlp("I bought a smartphone. Now I'm buying apps.")
```

```out
bought a smartphone
buying apps
```

Notes: 我们可以使用运算符和量词来定义一个词符应该被匹配几次。
我们可以用"OP"这个关键词来添加它们。

在这里"?"运算符使相应的判断词符变为可选，
所以我们会匹配到一个词根为"buy"的词符，一个可选的冠词和一个名词。

---

# 使用运算符和量词 (2)

| 例子       | 说明                  |
| ------------- | ---------------------------- |
| `{"OP": "!"}` | 否定: 0次匹配      |
| `{"OP": "?"}` | 可选: 0次或1次匹配 |
| `{"OP": "+"}` | 1次或更多次匹配        |
| `{"OP": "*"}` | 0次或更多次匹配        |

Notes: "OP"可以有以下四种值：

"!"用来否定一个词符，所以它一次也不能被匹配。

"?"用来将一个词符变为可选，可以匹配0次或者1次。

"+"用来匹配目标词符1次或更多次。

最后，"\*"用来匹配目标词符0次或更多次。

运算符可以大大加模板的威力，当然也带来了更多的复杂度。我们要学会善用它。

---

# 上手练习吧！

Notes: 基于词符的匹配给我们带来了信息提取更多的可能性。
让我们上手实战来写一些模板！
