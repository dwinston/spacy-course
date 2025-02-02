import json
from spacy.lang.en import English

with open("exercises/en/countries.json") as f:
    COUNTRIES = json.loads(f.read())

nlp = English()
doc = nlp("Czech Republic may help Slovakia protect its airspace")

# 导入PhraseMatcher并实例化
from spacy.____ import ____

matcher = ____(____)

# 创建Doc实例的模板然后加入matcher中
# 下面的代码比这样的表达方式更快： [nlp(country) for country in COUNTRIES]
patterns = list(nlp.pipe(COUNTRIES))
matcher.add("COUNTRY", None, *patterns)

# 在测试文档中调用matcher并打印结果
matches = ____(____)
print([doc[start:end] for match_id, start, end in matches])
