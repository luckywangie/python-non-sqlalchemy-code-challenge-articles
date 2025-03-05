class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not (isinstance(title, str) and 5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)
        magazine._articles.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Immutable: ignore assignments
        pass

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if self in self._magazine._articles:
            self._magazine._articles.remove(self)
        self._magazine = new_magazine
        new_magazine._articles.append(self)


class Author:
    def __init__(self, name):
        if not (isinstance(name, str) and name):
            raise ValueError("Name must be a non-empty string.")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Immutable: ignore assignments
        pass

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def articles(self):
        return [a for a in Article.all if a.author == self]

    def magazines(self):
        return list({a.magazine for a in self.articles()})

    def topic_areas(self):
        mags = self.magazines()
        return list({m.category for m in mags}) if mags else None


class Magazine:
    _all_magazines = []

    def __init__(self, name, category):
        if not (isinstance(name, str) and 2 <= len(name) <= 16):
            raise ValueError("Magazine name must be a string between 2 and 16 characters.")
        if not (isinstance(category, str) and category):
            raise ValueError("Category must be a non-empty string.")
        self._name = name
        self._category = category
        self._articles = []
        Magazine._all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
        else:
            raise ValueError("Magazine name must be a string between 2 and 16 characters.")
    

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and new_category:
            self._category = new_category
        else:
            raise ValueError("Category must be a non-empty string.")

    def articles(self):
        return self._articles

    def article_titles(self):
        titles = [a.title for a in self.articles()]
        return titles if titles else None

    def contributors(self):
        return list({a.author for a in self.articles()})

    def contributing_authors(self):
        from collections import Counter
        counts = Counter(a.author for a in self.articles())
        authors = [author for author, count in counts.items() if count > 2]
        return authors if authors else None

    @classmethod
    def top_publisher(cls):
        return max(cls._all_magazines, key=lambda m: len(m._articles)) if cls._all_magazines else None
