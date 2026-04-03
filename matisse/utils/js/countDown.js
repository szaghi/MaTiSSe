var secondsRemaining;
var intervalHandle;
function tick(){
  var timeDisplay = document.getElementsByClassName("timer");
  var min = Math.floor(secondsRemaining / 60);
  var sec = secondsRemaining - (min * 60);
  if (sec < 10) {
    sec = "0" + sec;
  }
  var message = "eta "+min.toString() + ":" + sec;
  [].slice.call( timeDisplay ).forEach(function ( div ) {
    div.innerHTML = message;
  });
  if (secondsRemaining === 0){
    clearInterval(intervalHandle);
    [].slice.call( timeDisplay ).forEach(function ( div ) {
      div.innerHTML = 'Stop';
    });
    resetPage();
  }
  secondsRemaining--;
}
function resetCountdown(minutes){
  clearInterval(intervalHandle);
  secondsRemaining = minutes * 60;
  intervalHandle = setInterval(tick, 1000);
}
function stopCountdown(){
  clearInterval(intervalHandle);
  //var stopBtns = document.getElementsByClassName("btn stop");
  //[].slice.call( stopBtns ).forEach(function ( div ) {
    //div.value = "start"
  //});
}      
function startCountdown(){
  clearInterval(intervalHandle);
  intervalHandle = setInterval(tick, 1000);
}
