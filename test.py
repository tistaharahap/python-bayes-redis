from BayesRedis import Classifier
import time

# BayesRedis Setup
b = Classifier({
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0
})

# Training examples
'''
b.train("Arsenal are targeting a club-record 22.5 million bid for Real Madrid striker Gonzalo Higuain this summer. Arsene Wenger has been given 82.5m to spend in the upcoming transfer window.", "arsenal")
b.train("Napoli are looking at bringing in Rafa Benitez to coach next term and are weighing up the option of bidding for Fernando Torres alongside the Spanish trainer. The Italian club are also said to be keeping tabs on Manchester City's Edin Dzeko.", "mancity")
b.train("Massimo Moratti has decided to end Andrea Stramaccioni's spell as coach of Inter and is hopeful of appointing outgoing Napoli coach Walter Mazzarri as his successor.", "inter")
b.train("PSG are said to be looking at replacing Real Madrid-bound Carlo Ancelotti with either Rafa Benitez, Laurent Blanc or les Parisiens' sporting director Leonardo.", "psg")
b.train("Chelsea are keen to sign Bayern Munich striker Mario Gomez. The Blues have begun enquiries as to the forward's availability, according to the German media.", "chelsea")
b.train("Barcelona are ready to submit a 23.5 million bid for Manchester City captain Vincent Kompany. The Belgium international is the Spanish club's number-one priority signing this summer.", "barca")
b.train("Gareth Bale is asking for 200,000 a week in order to stay at Tottenham for another season. The deal would make the midfielder one of the Premier League's biggest earners.", "spurs")
b.train("Liverpool are lining up a move for Manchester City defender Kolo Toure. The 32-year-old would see his 120,000-a-week wage cut by two thirds if he secured a switch to Anfield.", "liverpool")
b.train("Arsene Wenger has been given a 70 million budget to spend in the transfer window this summer.", "arsenal")
b.train("Tottenham are willing to listen to offers for Emmanuel Adebayor, Clint Dempsey and Scott Parker this summer.", "spurs")
b.train("Rangers is hoping to secure the return of current Vancouver Whitecaps forward Kenny Miller once the club's transfer ban is lifted in September. A deal could be in place as soon as this week.", "rangers")
b.train("The Spanish striker is likely to leave Sevilla and Atletico de Madrid, one of the interested clubs, are currently his most preferred destination.", "atletico")
b.train("Napoli chairman Aurelio De Laurentiis is in London to discuss a return to Serie A for departing interim Chelsea manager Rafa Benitez, who could move to Italy in a two-year deal.", "napoli")
b.train("Tottenham will soon announce Gareth Bale has signed a new contract with the club, but the deal is understood to have a release clause which would allow the Spurs star to leave next summer for 60 million.", "spurs")
b.train("Should Manuel Pellegrini take charge at Manchester City, he will try to sign Pepe from Real Madrid. The centre-back is expected to cost 25 million.", "mancity")
b.train("After the meeting in which Carlo Ancelotti expressed his desire to leave PSG this Sunday, sporting director Leonardo and president Nasser Al-Khelaifi approached Rafael Benitez, the outgoing Chelsea manager.", "psg")
b.train("With Walter Mazzarri announcing his decision to stand down as Napoli coach, the club have acted quickly and will meet with outgoing Chelsea manager Rafael Benitez over potentially taking over the role.", "napoli")
b.train("After a meeting with sporting director Leonardo and Paris Saint-Germain owner Al-Khellaifi, Carlo Ancelotti has decided to finish his time with the club in favour of an expected move to Real Madrid.", "psg")
'''

a = time.time()
keywords = "Salah satu Oakley store yang cukup nyaman menurut gw, koleksinya juga lumayan baik dan yang paling enak adalah tempatnya sepi, jadi kalau mau bilang \"wah mahal juga ya\" enggak tengsin banget. Pilihan kacamata nya juga update banget mulai dari yang pake polarized sampe yang biasa banyak bener pilihannya. Nah, jangan bawa-bawa harga kalo disini, harga sih emang udah standard Oakley tapi harga emang enggak bohong."
for i in range(100):
    b.classify(keywords)
total = time.time() - a
print "\nNumber of keywords classified: %d" % len(keywords.split(" "))
print "Elapsed time after %d iterations: %f seconds" % (i+1, total)
print "Average per ops: %f seconds" % (total / (i+1))
