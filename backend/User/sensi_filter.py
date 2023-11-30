sensi_filter = None
class TrieNode:
    def __init__(self, depth) -> None:
        self.children = {}
        self.is_end = False
        self.depth = depth

    def add_child(self, child:str):
        if child not in self.children.keys():
            self.children[child] = TrieNode(self.depth + 1)
        return self.children[child]
    
    def get_child(self, child:str):
        if child in self.children.keys():
            return self.children[child]
        return None
    
class SensiwordFilter:
    def __init__(self) -> None:
        self.root = TrieNode(0)
        
    def add_sensitive_word(self, word):
        tracker = self.root
        for w in word:
            tracker = tracker.add_child(w)
        tracker.is_end = True
    
    def filter(self, sentence:str):
        trackers:list[TrieNode] = []
        sentence = list(sentence)
        for i in range(len(sentence)):
            w = sentence[i]
            trackers.append(self.root)
            trackers = [t.get_child(w) for t in trackers if t.get_child(w) != None]
            for tracker in trackers:
                if tracker.is_end:
                    for j in range(tracker.depth):
                        sentence[i-j]='\*'
        return str.join('', sentence)

def init_sensi_filter():
    global sensi_filter
    sensi_filter = SensiwordFilter()
    from User.models import SensitiveWord
    words = SensitiveWord.objects.values_list('word', flat=True)
    for word in words:
        sensi_filter.add_sensitive_word(word)

def filter(sentence: str):
    '''输入一个句子，返回过滤完敏感词的句子'''
    global sensi_filter
    if sensi_filter is None:
        init_sensi_filter()
    return sensi_filter.filter(sentence)






