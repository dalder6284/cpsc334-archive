
void settings() {
  fullScreen();
}



int skewedTime(int minTime, int maxTime) {
  float v = pow(random(1), 4);
  int delay = int(map(v, 0, 1, minTime, maxTime));
  return delay;
}


String imgs = "C:/Users/diego/Documents/Processing Drafts/monet/";
PImage pic;

void setup() {
  background(255,255,255);
  
  /*String path = dataPath(imgs);
  File fp = new File(path);
  String[] lst = fp.list();
  
  if (lst.length > 0) {
    String fn = imgs + lst[int(random(0, lst.length))];
    pic = loadImage(fn);
    pic.loadPixels();
    println(fn);
  }*/
}

int padding = 3;
float horizonRatio = 0.45;
float alpha = 150;
int minTime = 1;
int maxTime = 500;



void draw() {
  // p1 and p2 are horizon lines. height is 0.6 and width is 0 and width
  int horizonHeight = int(height * horizonRatio);
  
  int rectHeight = int(random(padding, height - padding));
  int rectEdge = int(random(padding, width - padding));
  
  int[] r1 = {rectEdge, rectHeight};
  int[] r2 = {rectEdge, rectHeight + int(random(padding, height / 4))};
  
  
  //line(0, horizonHeight, width, horizonHeight);
  
  // pick p1 or p2
  int[] p0 = {0, horizonHeight};
  int[] p1 = {width, horizonHeight};
  
  int[] p;
  if (random(0, 1) > 0.5) {
      p = p0;
  } else {
      p = p1;
  }
  
  // randomized length of rectangle to horizon
  float rectLength = random(0.2, 0.7);
  
  int[] r1_to_p = {p[0] - r1[0], p[1] - r1[1]};
  int[] r3 = {r1[0] + int(r1_to_p[0] * rectLength), r1[1] + int(r1_to_p[1] * rectLength)};
  
  int[] r2_to_p = {p[0] - r2[0], p[1] - r2[1]};
  int[] r4 = {r2[0] + int(r2_to_p[0] * rectLength), r2[1] + int(r2_to_p[1] * rectLength)};
  
  // triangle(r1[0], r1[1], r2[0], r2[1], p[0], p[1]);
  color c;
  if (pic != null) {
    c = pic.get(int(random(0, pic.width)), int(random(0, pic.height)));
  } else {
    c = (color) random(#000000);
  }
  
  fill(c, alpha);
  noStroke();
  quad(r1[0], r1[1], r2[0], r2[1], r4[0], r4[1], r3[0], r3[1]);
  
  delay(skewedTime(minTime, maxTime));
}