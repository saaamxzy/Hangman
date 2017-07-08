import operator

class word_Counts:
    def __init__(self):
        self.total_count = 0
        self.word_counts = dict()
        self.most_five = []
        self.least_five = []
        self.sorted_counts = []

    def read_file(self, fname):
        with open(fname) as f:
            for line in f:
                temp = line.rstrip().split()
                word_c = eval(temp[1])
                self.word_counts[temp[0]] = word_c
                self.total_count += word_c 

    def print_entries(self):
        for key, value in self.word_counts.items():
            print(key, value)

    def sort_counts(self):
        self.sorted_counts = [(k, self.word_counts[k]) for k in sorted(self.word_counts, key=self.word_counts.get, reverse=True)]
        return self.sorted_counts

    def print_most_five(self):
        for i in range(10):
            try:
                print(self.sorted_counts[i])
            except IndexError:
                pass

    def print_least_five(self):
        
        for i in range(1, 11):
            try:
                print(self.sorted_counts[-i])
            except IndexError:
                pass

    def prob_word(self, word):
        if word in self.word_counts:
            return self.word_counts[word] / self.total_count
        return 0.0

class Guess:
    def __init__(self, wc):
        self.wc = wc
        self.number = 0
        self.L1 = '_'
        self.L2 = '_'
        self.L3 = '_'
        self.L4 = '_'
        self.L5 = '_'
        self.Llist = [L1, L2, L3, L4, L5]
        self.current = self.L1 + self.L2 + self.L3 + self.L4 + self.L5
        self.correct = list()
        self.incorrect = list()
        self.known = list()
        self.not_used = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def __init__(self, wc, number, L1, L2, L3, L4, L5, correct, incorrect):
        self.wc = wc
        self.number = number
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        self.L5 = L5
        self.Llist = [L1, L2, L3, L4, L5]
        self.current = self.L1 + self.L2 + self.L3 + self.L4 + self.L5
        self.correct = correct
        self.incorrect = incorrect
        self.known = list()
        self.not_used = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        for l in self.correct:
            self.not_used.remove(l)

        for l in self.incorrect:
            self.not_used.remove(l)

        self.sum_all = 0.0
            
        for other_word, counts in self.wc.word_counts.items():
            
            should_continue = False
            for i in range(5):

                if self.Llist[i] == '_':

                    if other_word[i] in self.incorrect or other_word[i] in self.correct:
                        should_continue = True
                        continue
                else:

                    if not other_word[i] == self.Llist[i]:
                        should_continue = True
                        continue
            if should_continue:
                continue

            self.sum_all += self.wc.prob_word(other_word)

    def posterior(self, word):
        if word not in self.wc.word_counts:
            return 0.0

        if self.number > 0:
            for i in range(5):          
                if self.Llist[i] == '_':
                    if word[i] in self.incorrect or word[i] in self.correct:
                        return 0.0
                else:
                    if not word[i] == self.Llist[i]:
                        return 0.0
            return self.wc.prob_word(word) / self.sum_all
        else:
            return self.wc.prob_word(word)

    def print_cond(self):
        for cond in self.known:
            print(cond)
            
    def print_state(self):
        print("current state: " + self.current)
        print("current number: " + str(self.number))
        print("current incorrect: " + str(self.incorrect))

    def next_best_guess(self):
        best_guess = ('', 0.0)
        for letter in self.not_used:
            sum_prob = 0.0
            for (word, counts) in self.wc.word_counts.items():
                sum_prob += self.posterior(word) if letter in word else 0.0    
            if sum_prob > best_guess[1]:
                best_guess = (letter, sum_prob)
        return best_guess

if __name__ == "__main__":
    wc = word_Counts()
    wc.read_file("corpus.txt")

    sorted_wc = wc.sort_counts()
    
    wc.print_most_five()
    wc.print_least_five()
    print("-----------------------------------------")
    g = Guess(wc, 0, '_', '_', '_', '_', '_', [], [])
    g.print_state()

    print(g.next_best_guess())

    print("-----------------------------------------")
    g1 = Guess(wc, 2, '_', '_', '_', '_', '_', [], ['E', 'T'])
    print("Guess started.")
    g1.print_state()

    print(g1.next_best_guess())

    print("-----------------------------------------")
    g2 = Guess(wc, 2, 'A', '_', '_', '_', 'R', ['A', 'R'], [])
    print("Guess started.")
    g2.print_state()

    print(g2.next_best_guess())

    print("-----------------------------------------")
    g3 = Guess(wc, 3, 'A', '_', '_', '_', 'R', ['A', 'R'], ['E'])
    print("Guess started.")
    g3.print_state()

    print(g3.next_best_guess())

    print("-----------------------------------------")
    g4 = Guess(wc, 5, '_', '_', 'H', '_', '_', ['H'], ['I', 'M', 'N', 'T'])
    print("Guess started.")
    g4.print_state()

    print(g4.next_best_guess())


    
    print("-----------------------------------------")
    g1 = Guess(wc, 2, '_', '_', '_', '_', '_', [], ['E', 'O'])
    print("Guess started.")
    g1.print_state()

    print(g1.next_best_guess())

    print("-----------------------------------------")
    g2 = Guess(wc, 2, 'D', '_', '_', 'I', '_', ['D', 'I'], [])
    print("Guess started.")
    g2.print_state()

    print(g2.next_best_guess())

    print("-----------------------------------------")
    g3 = Guess(wc, 3, 'D', '_', '_', 'I', '_', ['D', 'I'], ['A'])
    print("Guess started.")
    g3.print_state()

    print(g3.next_best_guess())

    print("-----------------------------------------")
    g4 = Guess(wc, 6, '_', 'U', '_', '_', '_', ['U'], ['A', 'E', 'I', 'O', 'S'])
    print("Guess started.")
    g4.print_state()

    print(g4.next_best_guess())
