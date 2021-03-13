class Action():
    pass


class Object():
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def look(self):
        return Action()

    def open(self):
       return Action()
    
    def use(self):
        return Action()


class Item(Object):
    def take(self):
        return Action()

    def put(self):
        return Action()


class Passage(Object):
    def __init__(self, _from, to, name, description):
        self._from = _from
        self.to = to
        super().__init__(name, description)

    def go(self):
        return Action()


class Ambient():
    def __init__(self, objects):
        self.objects = objects


class Game():
    def __init__(self, ambients, passages):
        self.ambients = ambients
        self.passages = passages
        
