class Node:
    def __init__(self, val, prev=None, next=None):
        self.value = val
        self.prev = prev
        self.next = next

class LinkedList:
    def __init__(self):
        self.current = None
        self.head = None

    def insert(self, i):
        n = Node(i)

        n.prev = self.current if self.current else n
        n.next = self.current.next if self.current else n

        if not self.head:
            self.head = n

        if (self.current):
            self.current.next.prev = n
            self.current.next = n
            
        if (self.head.prev == self.current):
            self.head.prev = n
                
        self.current = n

    def move_back(self, i):
        for _ in range(i):
            self.current = self.current.prev

    def move_forward(self, i):
        for _ in range(i):
            self.current = self.current.next

    def remove(self):
        val = self.current.value

        if (self.current == self.head):
            self.head = self.head.next
            self.head.prev = self.current.prev
            self.current.prev.next = self.head
        else:       
            prev = self.current.prev
            next = self.current.next

            next.prev = prev
            prev.next = next

        self.current = next
        return val

    def pprint(self):
        cur = self.head
        while (cur.next != self.head):
            print (cur.value, " ", end="")
            cur = cur.next
        print (cur.value)

# test sets
tests = [(9, 25), (10,1618), (13, 7999), (17,1104), (21,6111), (30, 5807), (424, 71482), (424, 71482*100 )]

for x in tests:
    marble_num = 2

    num_players = x[0]
    players = [0] * num_players

    marbles = LinkedList()
    marbles.insert(0)
    marbles.insert(1)
    max_marble_value = x[1]
    insert = 1
    current_player = 2
    while marble_num < max_marble_value:
        # place marble
        if (marble_num % 23 == 0):
            # keep the marble
            players[current_player] += marble_num
            # remove marble 7 CCW
            marbles.move_back(7)
            players[current_player] += marbles.remove()        
        else:
            marbles.move_forward(1)
            marbles.insert(marble_num)

        #marbles.pprint()
        marble_num += 1
        current_player += 1
        current_player = current_player % num_players

    print(f"{x[0]} players with last marble worth {x[1]} has a winning score of {max(players)}")
