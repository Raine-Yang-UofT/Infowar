"""
A test file, not part of the project
"""
import queue


class Message:
    def __init__(self, content, priority):
        self.content = content
        self.priority = priority

    def __lt__(self, other):
        # Invert the comparison to sort by largest priority
        return self.priority > other.priority


# Example usage
q = queue.PriorityQueue()

q.put(Message('Task 1', -1))
q.put(Message('Task 2', 50))
q.put(Message('Task 3', 0))

while not q.empty():
    print(q.get().content)
