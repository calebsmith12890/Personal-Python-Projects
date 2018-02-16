from multiprocessing import Manager, Pool
from collections import Counter
import urllib.request
from tkinter import *
import csv
import re

# Caleb Smith
# 11/07/17
# TCSS 480

class Crawler(object):

    # Function for initializing crawler object.
    def __init__(self):

        # Pool for implementing concurrency.
        pool = Pool(3)
        manager = Manager()

        # List for starting URLs.
        self.start = []
        self.nodes = manager.list() 
        self.words = manager.list()
        self.visited = manager.list()

        # Input file, hardcoded .txt file containing URLs.
        inputfile = open('urls6.txt', 'r')

        # Iterate through input file to gather starting URLs.
        for url in inputfile:
            self.start.append(url.rstrip())

        # Call crawl function concurrently.
        pool.map(self.crawl, self.start)

        # Output functions called after crawl.
        self.outputCSV(self.nodes)
        self.outputCloud(self.words)

        inputfile.close()

    def crawl(self, initial):
        
        fringe = [initial]

        # Crawls up to 50 web pages or until absolute links are exhausted.
        while len(fringe) > 0 and len(self.visited) < 50:

            curr = fringe.pop()

            #Try/Catch for permission denials.
            try:
                children = []
                page = urllib.request.urlopen(curr)
                html = str(page.read())

                # Regular expression for extracting links and link names in tuple form.
                links = re.findall('<a ?href ?= ?[\'"](https?://.*?)[\'"].*?>(.*?)<', html)

                # Iterate throught this webpages links and store it's children.
                for link, word in links:
                    if link not in self.visited + fringe:
                        fringe.insert(0, link)
                    children.append(link)
                    self.words.extend(self.getWords(word))

                # Only add nodes we haven't visited before.
                if curr not in self.visited:
                    self.visited.append(curr)
                    self.nodes.append((curr, children))

            except: pass

    # Strip non-alphanumeric symbols from regex results.
    def getWords(self, url):
        
        url = url.replace('\\n', ' ').replace('\\t', ' ')
    
        return ' '.join(re.split("[^a-zA-Z_]*", url)).split()

    # Sort URL nodes, and write each node and it's children to a CSV file.
    def outputCSV(self, input):

        total = []
        nodes = list(input)
        nodes.sort(key = lambda node: node[0])

        outfile = open('crawlerOut.csv', 'w')
        writer = csv.writer(outfile)

        # for row in outfile:
        # Write parent followed by children row by row.
        writer.writerow(['Parents,Children->\n'])
        for node in nodes:
            total.extend(node[1])
            # row = node[0] + ',' + ','.join(sorted(node[1])) + '\n'
            writer.writerow([node[0], sorted(node[1])])
            
        # Check for most common ties, and write results to CSV.
        writer.writerow(['\nMost Common Web Pages:\n'])
        freq = Counter(total)
        count = max(Counter(total).values())
        for item, value in freq.items():
            if value == count: writer.writerow([item])

        outfile.close()

    # Create a GUI frame and draw labels for the top 12 most frequent words.
    def outputCloud(self, words):

        x = 20
        y = 95
        dim = 600
        size = -75
        tempVal = 0
        maxWidth = 0
        maxHeight = 0

        root = Tk()
        root.title('Word Cloud')
        style = ['bold', 'italic', 'bold italic']
        color = ['red', 'green', 'yellow', 'blue']
        font = ['Times','Courier', 'Helvetica', 'Georgia']
        frame = Frame(root, bg = 'skyblue', width = dim, height = dim)

        freq = Counter(words)
        top = freq.most_common(12)
        
        # Print dictionary of top word frequency to console.
        print(dict(top))

        # Iterate through the words to match font size to frequency.
        for word, val in top:
            idx = top.index((word, val))
            if val < tempVal: size = -75 + 6 * idx
            label = Label(frame, font = (font[idx%4], size, style[idx%3]),
                                 fg = color[idx%4],
                                 bg = 'skyblue', 
                                 text = word)
                                    
            # Get width and height required for label.
            width = label.winfo_reqwidth()
            height = label.winfo_reqheight()

            if height > maxHeight: 
                maxHeight = height
            if width + x > 580: 
                x, y = 20, y + maxHeight
                maxHeight = 0

            # Place current label at calculated x/y coordinates.
            label.place(x = x, y = y, anchor = SW) 
            tempVal = val
            x += width
        # Pack frame and allow window to expand and fill.
        frame.pack(expand = YES, fill = BOTH)
        root.mainloop()

if __name__ == '__main__':
    Crawler()