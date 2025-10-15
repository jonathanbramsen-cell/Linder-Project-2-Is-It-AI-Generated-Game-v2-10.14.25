let currentPair = null
let wins = 0
let played = 0

async function fetchPair(){
  const res = await fetch('/api/pair')
  if(!res.ok) throw new Error('failed to get pair')
  return res.json()
}

async function next(){
  try{
    const pair = await fetchPair()
    currentPair = pair
    document.querySelector('#left img').src = pair.left.url
    document.querySelector('#right img').src = pair.right.url
    document.getElementById('result').textContent = ''
  }catch(e){
    document.getElementById('result').textContent = 'Could not load images.'
  }
}

async function guess(side){
  if(!currentPair) return
  const res = await fetch('/api/guess', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({pair_id: currentPair.pair_id, chosen: side})
  })
  const data = await res.json()
  played += 1
  if(data.correct){
    wins += 1
    document.getElementById('result').textContent = 'Correct — that was Real!'
  } else {
    document.getElementById('result').textContent = 'Wrong — that one was AI generated.'
  }
  document.getElementById('wins').textContent = wins
  document.getElementById('played').textContent = played
  currentPair = null
}

document.getElementById('next').addEventListener('click', next)
document.querySelector('#left .choose').addEventListener('click', ()=>guess('left'))
document.querySelector('#right .choose').addEventListener('click', ()=>guess('right'))
