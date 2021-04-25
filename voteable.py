from markupsafe import Markup

IMGDIR = "static/images/"
assert IMGDIR.endswith("/")

class Voteable:
	def __init__(self, filename="", text=""):
		self.plus = set()
		self.neutral = set()
		self.minus = set()
		self.filename = filename
		self.text = text

	def html(self):
		if self.filename:
			return Markup(f'<img class="icon" src="{IMGDIR}{self.filename}" />')
		else:
			return Markup(f'<div class="votableText">{self.text}</div>')

	def vote(self, vote, uid):
		assert vote in ["plus", "minus", "neutral"]
		# remove previous votes, if they exist
		self.plus.discard(uid)
		self.neutral.discard(uid)
		self.minus.discard(uid)
		self.__getattribute__(vote).add(uid)

	def score(self):
		return len(self.plus) - len(self.minus)

	def nr_votes(self):
		return len(self.plus) + len(self.neutral) + len(self.minus)
