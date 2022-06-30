import oseti

analyzer = oseti.Analyzer()
# text = "味は最高な一方で、接客態度は悪いです。"
# print(analyzer.analyze(text))
# ⇒ [0.3333333333333333]

f = open("analysis/lyrics/キャラクター.txt", 'r', encoding='UTF-8')
data = f.read()

print(f.name)
print(analyzer.analyze(data))
# lyrics_list = []

# import glob
# for filepath in glob.glob('analysis/lyrics/*'):
#     lyrics_list.append(filepath)

# for i in range(len(lyrics_list)):
#     f = open(lyrics_list[i], 'r', encoding='UTF-8')
#     data = f.read()
#     # print(data)
#     # print(f.name[16:]+" "+str(analyzer.analyze(data)))
#     print(f.name)
#     print(analyzer.analyze_detail(data))
#     f.close()