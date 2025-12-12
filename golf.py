<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>City Golf Game</title>
<style>
  body { background: lightgreen; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
  #game { position: relative; width: 600px; height: 400px; border: 2px solid #333; }
  .ball { position: absolute; width: 20px; height: 20px; border-radius: 50%; background: white; }
  .hole { position: absolute; width: 20px; height: 20px; border-radius: 50%; background: yellow; }
  .obstacle { position: absolute; background: grey; }
  canvas { position: absolute; top:0; left:0; }
</style>
</head>
<body>
<div id="game">
  <canvas id="canvas" width="600" height="400"></canvas>
  <div id="ball" class="ball"></div>
  <div id="hole" class="hole" style="left:550px; top:50px;"></div>
  <div class="obstacle" style="left:200px; top:300px; width:50px; height:50px;"></div>
  <div class="obstacle" style="left:350px; top:150px; width:50px; height:150px;"></div>
  <div class="obstacle" style="left:100px; top:50px; width:50px; height:50px;"></div>
</div>

<script>
const ball = document.getElementById("ball");
const hole = document.getElementById("hole");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const obstacles = Array.from(document.getElementsByClassName("obstacle"));

let ballPos = {x:50, y:350};
let isDragging = false;
let startDrag = {x:0, y:0};
let velocity = {x:0, y:0};

function drawLine(from, to){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.beginPath();
  ctx.moveTo(from.x + 10, from.y + 10);
  ctx.lineTo(to.x, to.y);
  ctx.strokeStyle = 'red';
  ctx.lineWidth = 2;
  ctx.stroke();
}

function updateBall(){
  ballPos.x += velocity.x;
  ballPos.y += velocity.y;

  // 邊界
  if(ballPos.x < 0 || ballPos.x > 580) velocity.x = 0;
  if(ballPos.y < 0 || ballPos.y > 380) velocity.y = 0;

  // 障礙物碰撞
  obstacles.forEach(o=>{
    let ox = o.offsetLeft, oy = o.offsetTop, ow = o.offsetWidth, oh = o.offsetHeight;
    if(ballPos.x+10 > ox && ballPos.x < ox+ow && ballPos.y+10 > oy && ballPos.y < oy+oh){
      velocity.x = 0;
      velocity.y = 0;
    }
  });

  // 過洞判定
  let hx = hole.offsetLeft, hy = hole.offsetTop;
  if(Math.hypot(ballPos.x - hx, ballPos.y - hy) < 20){
    velocity.x = 0;
    velocity.y = 0;
    alert("🎉 球進洞了！");
  }

  ball.style.left = ballPos.x + "px";
  ball.style.top = ballPos.y + "px";

  if(velocity.x != 0 || velocity.y != 0){
    requestAnimationFrame(updateBall);
  }
}

// 監聽滑鼠拖曳
canvas.addEventListener("mousedown", (e)=>{
  if(Math.hypot(e.offsetX - ballPos.x, e.offsetY - ballPos.y) < 20){
    isDragging = true;
    startDrag = {x:e.offsetX, y:e.offsetY};
  }
});

canvas.addEventListener("mousemove", (e)=>{
  if(isDragging){
    drawLine({x:ballPos.x, y:ballPos.y}, {x:e.offsetX, y:e.offsetY});
  }
});

canvas.addEventListener("mouseup", (e)=>{
  if(isDragging){
    isDragging = false;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    let dx = startDrag.x - e.offsetX;
    let dy = startDrag.y - e.offsetY;
    velocity = {x: dx/5, y: dy/5};
    requestAnimationFrame(updateBall);
  }
});
</script>
</body>
</html>
