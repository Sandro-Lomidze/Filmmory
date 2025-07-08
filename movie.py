class Movie:
    def __init__(self, id, title, type, status, score, runtime_ep_count,release_year, date_unified):
        self.id = id
        self.title = title
        self.type = type
        self.status = status
        self.score = score
        self.runtime_ep_count = runtime_ep_count
        self.release_year = release_year
        self.date_unified = date_unified

    def as_tuple(self):
        return (self.title, self.type, self.status, self.score,
        self.runtime_ep_count, self.release_year, self.date_unified)

    def as_tuple_update(self):
        return (self.title, self.type, self.status, self.score,
                self.runtime_ep_count, self.release_year, self.date_unified, self.id)