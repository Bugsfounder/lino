from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot("LinoBot")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")
