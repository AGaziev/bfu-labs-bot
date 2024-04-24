class Carousel(object):
    def __init__(self, collection, repeatable: bool = False):
        self.repeatable = repeatable
        self.collection = collection
        self.index = 0

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            if self.repeatable:
                self.index = 0
                result = self.collection[self.index]
            raise StopIteration
        finally:
            return result

    def prev(self):
        self.index -= 1
        if self.index < 0:
            if not self.repeatable:
                raise StopIteration
        return self.collection[self.index]

    def __iter__(self):
        return self


a = [0,1,2,3,4]
b = Carousel(a, True)
while True:
    print(b.next())
    input("prev?")
