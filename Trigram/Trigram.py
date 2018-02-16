import random

class Trigram():
    
    def __init__(self):
        
        self.trigram = {}
        self.outStory = ''
        # self.inFiles = ['doyle-27.txt', 'doyle-case-27.txt']
        self.inFiles = ['alice-27.txt', 
                        'doyle-27.txt', 
                        'doyle-case-27.txt', 
                        'london-call-27.txt', 
                        'twain-adventures-27.txt']

        self.readStories()
        self.writeStory()

    def readStories(self):
        
        for file in self.inFiles:
            
            story = open(file, 'r')
            words = ''.join(story.readlines()).lower().split()
            self.buildTrigram(words)
            story.close()

    def buildTrigram(self, story):
        
        for i in range(len(story) - 2):
            if story[i] in self.trigram:
                if story[i+1] in self.trigram[story[i]]:
                    if story[i+2] in self.trigram[story[i]][story[i + 1]]:
                        self.trigram[story[i]][story[i + 1]][story[i + 2]] += 1
                    else:
                        self.trigram[story[i]][story[i + 1]][story[i + 2]] = 1
                else:
                    self.trigram[story[i]][story[i + 1]] = {story[i + 2] : 1}
            else:
                self.trigram[story[i]] = {story[i + 1]:{story[i + 2] : 1}}
    
    def writeStory(self):
        
        story = []
        word1 = random.choice(list(self.trigram.keys()))
        word2 = random.choice(list(self.trigram[word1].keys()))
        story.extend([word1, word2])

        for word in range(2, 1000):

            nextWords = self.trigram[story[word - 2]][story[word - 1]]
            probability = []

            for key in nextWords:
                for i in range(nextWords[key]):
                    probability.append(key)

            story.append(random.choice(probability))

        self.outStory = ' '.join(story)
        self.output()

    def output(self):
        
        outFile = open('story2.txt', 'w')
        outFile.write(self.outStory)
        outFile.close()

if __name__ == '__main__':
    Trigram()
