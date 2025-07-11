// Global variables
let statusexpouse = false;
let preExposureState = false;
let curmilis = 0;
let waktutunda = 0;
let angle = 0;
let numLines = 10;
let lineX = new Array(numLines).fill(0);
let lineY = new Array(numLines).fill(0);
let lineSpeed = 5;
let lineSpacing = 9.5;
let simulasiSerialBuffer = [];
let Scolor = 6;
let gcolor = 2;
let foccolor = 0;
let fcolor = 0;
let E = 1;
let Sec = 0;
let mA = 0;
let kv = 0;
let selectedKvLine = -1;
let kvValues = [120, 110, 100, 90, 80, 70, 60];
let prevKode = '';
let waveOffset = 0;
let glowCanvas;
let exposureStartTime = 0;
let isExposing = false;
let pulseOffset = 0;
let pulseSpeed = 2;
let pulseWidth = 50;

function parseURLParams() {
  const urlParams = new URLSearchParams(window.location.search);
  kv = Number(urlParams.get("kv")) || 0;
  mA = Number(urlParams.get("mA")) || 0;
  Sec = Number(urlParams.get("Sec")) || 0;
  const kodeVal = urlParams.get("kode") || "x";

  if (kodeVal === "p") {
    preExposureState = true;
    statusexpouse = false;
    window.mAmeter = 0;
  } else if (kodeVal === "e") {
    preExposureState = false;
    statusexpouse = true;
    window.mAmeter = mA;
    exposureStartTime = millis();
  } else {
    preExposureState = false;
    statusexpouse = false;
    window.mAmeter = 0;
  }

  foccolor = mA;
  fcolor = (mA <= 200) ? 1 : 2;
  selectedKvLine = kvValues.indexOf(getNearestKV(kv));
}

function setup() {
  createCanvas(1920, 1080);
  pixelDensity(1);
  background(0);
  colorMode(HSB, 360, 100, 100, 100);
  glowCanvas = createGraphics(1920, 1080);
  glowCanvas.colorMode(HSB, 360, 100, 100, 100);

  let canvas = document.querySelector('canvas');
  if (canvas) {
    canvas.style.position = 'absolute';
    canvas.style.left = '0';
    canvas.style.top = '0';
  }

  for (let i = 0; i < numLines; i++) {
    lineX[i] = 1056;
    lineY[i] = 425 - (i * lineSpacing);
  }

  parseURLParams();
}
