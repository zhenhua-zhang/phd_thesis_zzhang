import sys

import matplotlib.pyplot as plt
from wordcloud import WordCloud

word_black_list = [
    "using", "CA", "de", "PLHIV", "Chapter", "e.g.", "studies", "e.g.,", "e.g", "e", "g",
    "identified"
]

syno_dict = {
    "associated": "association"
}

word_source_file = sys.argv[1]
with open(word_source_file, "r") as word_source:
    words = word_source.read().replace("\n", " ")
    word_list = [w for w in words.split(" ") if w not in word_black_list]
    word_list = [syno_dict[w]  if w in syno_dict else w for w in word_list]
    word_list = [w.title() for w in word_list if not w.isupper()]
    words = " ".join(word_list)

wc = WordCloud(max_words=500000, random_state=31415, width=1920, height=1080,
               background_color="white", colormap="tab10", margin=1)

word_cloud = wc.generate(words)

fig, axe = plt.subplots()
axe.imshow(word_cloud, interpolation="bilinear")
axe.set_axis_off()
axe.set_frame_on(False)

fig.set_figheight(9)
fig.set_figwidth(16)
fig.set_tight_layout(True)
fig.savefig("word_cloud.png")
