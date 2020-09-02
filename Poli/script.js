const doorImage1 = document.getElementById('door1');
const doorImage2 = document.getElementById('door2');
const doorImage3 = document.getElementById('door3');
const doorImage4 = document.getElementById('door4');
const doorImage5 = document.getElementById('door5');
const doorImage6 = document.getElementById('door6');
const doorImage7 = document.getElementById('door7');
const doorImage8 = document.getElementById('door8');
const doorImage9 = document.getElementById('door9');
const doorImage10 = document.getElementById('door10');
const doorImage11 = document.getElementById('door11');
const doorImage12 = document.getElementById('door12');
const doorImage13 = document.getElementById('door13');
const doorImage14 = document.getElementById('door14');
const doorImage15 = document.getElementById('door15');
const doorImage16 = document.getElementById('door16');
const doorImage17 = document.getElementById('door17');
const doorImage18 = document.getElementById('door18');
const doorImage19 = document.getElementById('door19');
const doorImage20 = document.getElementById('door20');
const doorImage21 = document.getElementById('door21');
const doorImage22 = document.getElementById('door22');
const doorImage23 = document.getElementById('door23');
const doorImage24 = document.getElementById('door24');
//images 130x130
const win = document.getElementById('win');

const polina = './assets/polina.jpg';
const adam  = './assets/adam.jpg';
const adar = './assets/adar.jpg';
const adi = './assets/adi.jpg';
const amit = './assets/amit.jpg';
const amnon = './assets/amnon.jpg';
const ayelet = './assets/ayelet.jpg';
const dad = './assets/dad.jpg';
const gool = './assets/gool.jpg';
const mom = './assets/mom.jpg';
const ori = './assets/ori.jpg';
const rom = './assets/rom.jpg';
const square = './assets/square.jpg';

let assets = [polina, adam, adar, adi, amit, amnon, ayelet, dad, gool, mom, ori, rom, polina, adam, adar, adi, amit, amnon, ayelet, dad, gool, mom, ori, rom];

const startButton = document.getElementById('start');
let closedDoors = 24;
let doorOpened = '';
let firstDoor = true;
let clickDisabled = false;

const isMatch = (door1,door2) => {
    if(door1.src === door2.src){
      return true;
    }
    return false;
}

const playDoor = (door) => {
  if (firstDoor){
    firstDoor = false;
    doorOpened = door;
  }
  else {
    if (isMatch(door,doorOpened)) {
      clickDisabled = true;
      firstDoor = true;
      closedDoors -= 2;
      door.onclick = null;
      doorOpened.onclick = null;
      doorOpened = '';
      setTimeout(function() {clickDisabled= false},300);
      winner();
    } else {
      clickDisabled = true;
      noMatch(door, door2 = doorOpened);
    }
  }
}

const noMatch = (door,door2) => { setTimeout( function() {
    clickDisabled = false;
    door.src = square;
    door2.src = square;
    firstDoor = true;
    console.log("door opened change to empty");
    doorOpened = undefined;
    console.log(doorOpened);
  }, 1000)
}

const shuffleAssets = () => {
  assets.sort(function(a, b){return 0.5 - Math.random()});
};

var doors = document.querySelectorAll(".door-frame");
const defOnclick = () => {
  for (let i=0; i<doors.length; i++){
    doors[i].onclick = function() {
      if (clickDisabled || doors[i] === doorOpened){
        return ;
      }
      doors[i].src = assets[i];
      playDoor(doors[i]);
    }
  };
}
startButton.onclick = () => {
  startRound();
};

const startRound = () => {
  closedDoors = 24;
  doorOpened = '';
  firstDoor = true;
  clickDisabled = false;
  defOnclick();
  win.style.visibility = 'hidden';
  shuffleAssets();
  doors.forEach(door => {
    door.src = square;
  })
};

const winner = () => {
  if (closedDoors === 0){
      win.style.visibility = 'visible';
  }
}


startRound();
