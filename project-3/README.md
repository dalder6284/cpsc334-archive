# Bookloo! Box
To run the Bookloo, you'll need an ESP32 and an MPU-6050 gyroscope. You'll also need something like the sponge sensor mentioned in my blog post, but anything that puts through voltages between 0 and 3.3 to the SPONGE pin will work (e.g. a potentiometer).

You'll also need Supercollider and Python installed on the same device. Upload the code to the ESP32 with the IP of the device you're running SC and Python on. Run the Python script and receive the data. It should print out as you receive the gyro and ADC data. Then, as you run Supercollider, the music will change depending on the state of the box!

![image.png](/project-3/images/bookloo1.jpeg)

## Introduction

I knew that I wanted to do something with the gyroscope and interpretations of motion with this project. I was thinking of doing something like the [Mi.Mu](https://mimugloves.com/) gloves, but it felt too *literal*. It didn’t have enough of the unseen effect written on it. There was too much of the *seen* effect written all over it.

Through some brainstorming, I thought about what would happen if I just put the gyroscope in some box and saw it in a museum. Why would moving a lonesome box by itself be of consequence at all? Well, what if it was *sacred*? Every major religion, both old and really old, has some sort of connection with the idea of a [cult image](https://en.wikipedia.org/wiki/Cult_image), a human made object worshipped for the deity it represents. It’s a very vague term, which is why I’m comfortable making a rather nonchalant imitation of it. I mean, I hope I don’t offend anyone through this project, but I don’t think I’m mocking anyone’s religion by making a box make music when it’s disrespected.

That’s the idea, anyways. The atmosphere of the room (the music playing) should change when someone disrespects this box that I’ve personally interpreted to represent as some alien deity. By disrespect, I mean that the box has sensors inside and outside that detect if it is being tossed around, put on its side, set upside down, etc. It even has a spongy belly that you need to be careful with. If the box gets disrespected in these ways, it begins to warn you and gets angrier (plays scarier music) as you continue your disrespect. If you treat it correctly (perhaps pressing down just right on its belly), you’ll get a special song laid upon you.

## The Specifics

There’s five specific things that need to be discussed about the project: the enclosure, the ESP32 code, the Python script on the server that connects to the ESP32, the Supercollider code that plays the music, and the Raspberry Pi.

### The Enclosure and the Sponge Sensor

The enclosure is a project box I found in the AKW lab with a breadboard inside. The ESP32 is connected and so is an MPU-6050 gyroscope, a blue LED, the sponge sensor, a battery, and a switch. They are all programmed and powered by the ESP32, which I will explain in the ESP32 code section. The box was completely covering, but I drilled a hole for the LED, a hole for access to the ESP32 USB upload port, a hole for the switch, and a hole for the sponge sensor.

The sponge sensor is a custom sensor centered on the “belly” of the idol. I constructed it using two exposed wires, a sponge I found at College Convenience, and a piece of paper. That blue covering on the box actually comes from the sponge I bought. The sponge actually had this fuzzy cover over it that fit perfectly on the box.

Here’s how the sponge sensor works: the two wires are exposed and spread about an inch apart on a surface. Then, they are covered with a piece of paper covered with graphite (scribbled on with pencil). The sponge is then laid over the piece of paper. As you press on the sponge, the wires touch more of the graphite, lowering the resistance between them. This leads to a pressure sensor based on how far down the sponge is pressed.

![image.png](/project-3/images/bookloo2.jpeg)
![image.png](/project-3/images/inside_bookloo.jpeg)


### The ESP32

The ESP32 uses a TCP connection to deliver MPU-6050 gyroscope data and sponge sensor data to a Python server on the Raspberry Pi. The sponge sensor works by reading the ADC of the two wires and uses an API for the gyroscope. It then packs it into a struct and sends it every 200 ms to a server it tries to maintain a connection to.

For the sake of convenience, I added a blue LED that will blink when the ESP32 is attempting to connect to the internet or the server. It stays on when it is successfully streaming data to the server.

### The Python Server

The Python server is responsible for maintaining the connection. The solution from my lab didn’t create another connection with the ESP32 if it dropped out. I needed to make it a continuous stream. So, I accept multiple clients (which are really just the ESP32’s different sessions) and time out old sessions that haven’t sent data. I also disconnect clients that send offset data. That way, instead of having to deal with alignment in my code, I just force the ESP32 to send aligned data again.

I’m also managing and delivering the state of the Bookloo to the Supercollider script via OSC. The effect of the “disrespected” state is managed like thus: there is a normal state (N1) and three different anger states (M1, M2, M3) that you move up through once the Bookloo is disrespected. If the sponge is pressed just right and the Bookloo is in a normal state, then a blessing state (B1) will occur. If it is in an angry state, after about 20 seconds, if everything is respectful, then it moves down an anger state until it reaches the normal state. Feel free to look at the top few functions that determine the state logic.

```python
mostRecentChange = time.time()
curr = "N1"

def moveUp():
    global curr
    global mostRecentChange
    if curr == "B1":
        curr = "M1"
    elif curr == "N1":
        curr = "M1"
    elif curr == "M1":
        curr = "M2"
    elif curr == "M2":
        curr = "M3"
    
def moveDown():
    global curr
    global mostRecentChange
    if curr == "M1":
        curr = "N1"
    elif curr == "M2":
        curr = "M1"
    elif curr == "M3":
        curr = "M2"

def parse_data(data):
    global curr
    global mostRecentChange
    ax, ay, az, gx, gy, gz, sponge = data
    onside = (ay < 9.0) and (ay > -5)
    usd = (ay < -8)
    shaken = (abs(gx) > 2.5) or (abs(gy) > 2.5) or (abs(gz) > 2.5)
    cool = not (onside or usd or shaken or sponge > 1400)
    
    if curr == "B1" and 0 < sponge < 1400:
        return
    
    now = time.time()
    if (now - mostRecentChange > 10):
        mostRecentChange = time.time()
        if sponge > 0 and sponge < 1400 and curr == "N1":
            curr = "B1"
            
            sc_client.send_message("/data", curr)
            return
        
        if sponge == 0 and curr == "B1":
            curr = "N1"
            
        if usd:
            curr = "M3"
        elif onside or shaken:
            moveUp()
        elif sponge > 1400:
            moveUp()
        elif cool:
            moveDown()
            
        sc_client.send_message("/data", curr)
```

### Supercollider and the Raspberry Pi

The Supercollider code is very simple. I have a few Synth definitions from last semester when I took Computer Music, and I’ve assigned each one to play when the OSC function is sent in.

```c
~synths = Dictionary.new;

~synths = ~synths.put(\M3, Dictionary.with(*["name"->\M3, "active"->false, "synth"->\prayer, "playing"->nil]));
~synths = ~synths.put(\M2, Dictionary.with(*["name"->\M2, "active"->false, "synth"->\fm_exp, "playing"->nil]));
~synths = ~synths.put(\M1, Dictionary.with(*["name"->\M1, "active"->false, "synth"->\fm_seq, "playing"->nil]));
~synths = ~synths.put(\N1, Dictionary.with(*["name"->\N1, "active"->false, "synth"->\infi, "playing"->nil]));
~synths = ~synths.put(\B1, Dictionary.with(*["name"->\B1, "active"->false, "synth"->\nost, "playing"->nil]));

~current = \N1;

// ----- MAIN -----

switch_to = {
	arg to;
	"Switching to %".format(to).postln;

	if (~synths[~current].at("active") == true,
		{
			~synths[~current].at("playing").release;
			// "Releasing %".format(~synths[~current].at("name")).postln;
	}, {});

	~synths[~current].put("active", false);
	x = Synth(~synths[to].at("synth"));
	~synths[to].put("playing", x);
	~synths[to].put("active", true);
	~current = to;

};

switch_to.(\N1);

activator = {
	arg msg, time, addr, recvPort;
	var next_state = msg[1];
	// "%".format(next_state).postln;

	if(~current != next_state,
		{
			switch_to.(next_state);
	}, {});

};

~o = OSCFunc(activator, '/data');
```

Here’s the thing about the Raspberry Pi. It’s trivial to get the Python script to run on start-up. What’s *not* trivial is getting Supercollider even installed and working properly on the Raspberry Pi, much less a script working on startup. Setting up a headless install and then figuring out how to run your script on it isn’t as simple as an apt install and an `sclang my-code.scd`. I certainly tried, and even after installing it, getting your code you made on your laptop to work on your Pi’s Supercollider is an entirely different beast since the interpreted nature of the PC’s IDE is completely different from creating a sequence on the Pi. Also, my convolutions didn’t work and I’d prefer my funny noises over getting it to work on the Pi. And believe me, I did try. So, alas, on my laptop, the scripts will run for now.

### Conclusion

For future versions, I think setting up the ESP32 as the server instead of the client could make my life easier. Figuring out the ESP32 IP and uploading it somehow automatically to get my laptop to connect should be easier, something similar to what I’m doing with the Pi. I wish I had brainstormed more ideas regarding how one could “disrespect” the Bookloo, but I’m satisfied with the conditions I have for now.

### Video

[Here.](https://www.youtube.com/watch?v=Vz2a4LvKhGc)