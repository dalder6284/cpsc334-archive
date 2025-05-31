## Clocky

To run this code, I found success in using the motor library within a virtual environment. I added a requirements.txt for what worked for me. Other than that, you would use the shell script to start it on boot in systemctl, or wayfire.ini, or cron.
Let me know what you think!

*The following is my artist statement:*

**Clocky**

*Diego Alderete*

*2024*

*Interactive Installation, sound projection and papercraft*

“Clocky” is about as intellectual as a singing birthday card, but it’s just as good at making you feel as special. A switch on the side, when pressed in any direction, will set the hand of the clock in motion, sealing the fate of the receiver. Please ignore any sounds the clock might make as the clock is not sentient and any receiver should ignore any of its attempts at communication. Then, a pause and a receipt is printed out with the fate of the receiver. Fortunes are not for the sensitive. Yet, the blunt nature of the piece’s correspondence with the receiver is specially unique, as there are dozens (yes, dozens!) of fortunes the clock could dole out.

With a white canvas below the clock, the piece symbolizes not only time’s everlasting rule but its ability to usurp *any* thing or man. As the clock emulates these animalistic sounds, it makes the viewer wonder whether time is just like any human. Does it have intentions? To deceive? To intimidate? Through these metaphysical ponderings, the artist attempts to create a special occasion in each interaction with a user, utilizing sound and spontaneity (I hesitate to call it wit). Is not everyone’s fate and future as unique as the light (and screams) within ourselves? Although the gibberish printed out on the paper may not be your actual future and the noises may be a paper cone speaker behind some chipwood, is it really wise to ignore the advice of a screaming clock?

## What is Clocky?

I wanted to make some sort of fortune-telling automata like a Zoltar or something that gives out fortune cookies. Then, I could use the lab’s receipt printer to make the fortunes. I had thought of generating a bunch of them using ChatGPT but as I was going through the process of just writing fortunes, I felt like it was a bit… well, too fortune-cookie cheesy.

There’s this joke I always tell whenever I open a fortune cookie. I open it up, I unfurl the fortune and read “Help! I’m stuck in a fortune cookie factory!” Never gets a laugh. As I was writing these fortunes, I started thinking what it would be like if I went with the theme that everyone else in 334 had decided to go with: what if this fortune-telling machine had feelings like a person?

Thus, Clocky began. Clocky is a mantle clock that spins its minute hand whenever the switch on the side of it is pressed. Then, after a brief sound, it dispenses a “fortune”, which is in quotes for reasons to be elaborated upon later.


## What’s inside Clocky?

it’s just the Raspberry Pi, wired to the switch on the side, the motor spinning the clock, and a small speaker I soldered together so that bell chimes could be played. Originally, I had planned to do however many chimes at whatever time Clocky landed on, but as it turns out, a paper cone can’t really resonate the Undertaker’s bell through chipboard as well as I wanted it to. So, I thought “What if it screamed?” Like the dude stuck in a fortune cookie factory! So, I made it choose from a variety of men screaming. Then, I started adding a bunch of random sounds. Like it knew you were listening and wanted to mess with you. So, I added cats screeching, text notifications, dogs barking, silly cartoon sounds, etc. The code picks a sound randomly and plays it before doling out a ”fortune”.

The whole thing is made of ugly brown chipboard that I meticulously painted an even spookier brown.


## Why do you keep putting “fortune” in quotes?

Well, fortune cookies aren’t actually very creative. They’re pretty vague and very positive. Are they really art? This is left as an exercise for the reader. As for my project, I decided to make my fortunes more interesting. I wrote a few normal fortune cookie ones and then I wrote some contemplative ones. Then, I wrote some accusations. Some confrontational. After that, I really started to give the clock a personality. I had the idea of it telling you that “you will become a marine biologist” and then a few seconds later printing out “… I wish I were a marine biologist”. It started this whole saga of two-parter fortunes, allowing for more flexibility in the kinds of jokes I could make when printing these out. Then, I wrote a bunch of Seinfeld references, Family Guy references, Wikipedia references, etc. What if your fortune cookie told you what the Statue of Liberty was? What would you think it meant? You’d think someone was messing with you, and that’s kind of the vibe I wanted to go for: a clock telling fortunes to mess with the people forcing it to do so.

## The Code

The code is a bit long but rather straightforward. It loads in a .JSON file of the fortunes, both the one-parters and the two-parters. Then, it assigns a callback function to the switch’s pins so that the process of fortune-telling is done every time the switch is pressed. A few auxiliary functions allow for printing from the receipt printer, for splitting up two-parters, for playing a sound using PyGame, etc. The most important function is the callback and it explains the basic procedure for every fortune-telling cycle