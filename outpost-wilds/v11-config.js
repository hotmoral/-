const FACILITY_LABEL={workshop:'작업대',storage:'보급 창고',farm:'농장',watchtower:'망루',forge:'대장간',infirmary:'회복소',wall:'방벽',turret:'자동 터렛',turret2:'외곽 터렛'};

const FACILITY_TIERS={
 workshop:[
  {cost:{wood:45,stone:25,meat:0},base:2,req:{},mission:{gather:70},effect:'채집 효율'},
  {cost:{wood:90,stone:60,meat:10},base:3,req:{storage:1},mission:{gather:180},effect:'채집 효율'},
  {cost:{wood:170,stone:120,meat:25},base:5,req:{forge:2,storage:2},mission:{boss:1,invested:650},effect:'채집 효율'}],
 storage:[
  {cost:{wood:55,stone:30,meat:0},base:2,req:{},mission:{gather:60},effect:'적재량'},
  {cost:{wood:100,stone:70,meat:10},base:3,req:{workshop:1},mission:{invested:200},effect:'적재량'},
  {cost:{wood:180,stone:130,meat:30},base:5,req:{farm:2,wall:2},mission:{gather:500},effect:'적재량'}],
 farm:[
  {cost:{wood:55,stone:25,meat:10},base:2,req:{workshop:1},mission:{meat:25},effect:'식량 생산'},
  {cost:{wood:110,stone:60,meat:25},base:3,req:{storage:2},mission:{gather:240},effect:'식량 생산'},
  {cost:{wood:190,stone:100,meat:50},base:5,req:{infirmary:2},mission:{raids:2},effect:'식량 생산'}],
 watchtower:[
  {cost:{wood:70,stone:40,meat:15},base:2,req:{workshop:1},mission:{kills:5},effect:'방어 화력'},
  {cost:{wood:140,stone:90,meat:25},base:3,req:{forge:1,wall:1},mission:{raids:1},effect:'방어 화력'},
  {cost:{wood:240,stone:160,meat:45},base:5,req:{turret:1,wall:2},mission:{kills:40},effect:'방어 화력'}],
 forge:[
  {cost:{wood:85,stone:90,meat:20},base:3,req:{workshop:2},mission:{stone:100},effect:'무기 화력'},
  {cost:{wood:160,stone:170,meat:35},base:4,req:{storage:2,watchtower:2},mission:{kills:20},effect:'무기 화력'},
  {cost:{wood:270,stone:260,meat:60},base:6,req:{turret2:1,workshop:3},mission:{boss:1},effect:'무기 화력'}],
 infirmary:[
  {cost:{wood:70,stone:55,meat:30},base:3,req:{farm:1},mission:{meat:50},effect:'거점 회복'},
  {cost:{wood:135,stone:105,meat:55},base:4,req:{storage:2},mission:{raids:1},effect:'거점 회복'},
  {cost:{wood:220,stone:170,meat:90},base:5,req:{farm:3},mission:{raids:3},effect:'거점 회복'}],
 wall:[
  {cost:{wood:95,stone:120,meat:20},base:3,req:{watchtower:1,storage:1},mission:{raids:1},effect:'거점 내구도'},
  {cost:{wood:180,stone:220,meat:45},base:4,req:{forge:2,watchtower:2},mission:{kills:30},effect:'거점 내구도'},
  {cost:{wood:300,stone:360,meat:70},base:6,req:{turret2:2,storage:3},mission:{boss:2},effect:'거점 내구도'}],
 turret:[
  {cost:{wood:120,stone:150,meat:35},base:4,req:{watchtower:2,forge:1},mission:{kills:20},effect:'자동 방어'},
  {cost:{wood:220,stone:260,meat:65},base:5,req:{forge:2,wall:2},mission:{boss:1},effect:'자동 방어'},
  {cost:{wood:360,stone:420,meat:90},base:6,req:{forge:3,wall:2},mission:{boss:2},effect:'자동 방어'}],
 turret2:[
  {cost:{wood:155,stone:190,meat:45},base:5,req:{turret:2,wall:2},mission:{boss:1},effect:'외곽 방어'},
  {cost:{wood:280,stone:330,meat:75},base:6,req:{turret:3,watchtower:3},mission:{raids:3},effect:'외곽 방어'},
  {cost:{wood:420,stone:500,meat:110},base:6,req:{forge:3,wall:3},mission:{boss:2},effect:'외곽 방어'}]
};

const BASE_TIERS={
 2:{cost:{wood:70,stone:35,meat:18},req:{},mission:{gather:50}},
 3:{cost:{wood:150,stone:100,meat:40},req:{workshop:1,storage:1},mission:{gather:140,invested:100}},
 4:{cost:{wood:240,stone:200,meat:80},req:{workshop:2,watchtower:1,forge:1,infirmary:1},mission:{kills:15,raids:1}},
 5:{cost:{wood:390,stone:350,meat:140},req:{storage:2,farm:2,wall:2,turret:1},mission:{kills:30,raids:2,boss:1}},
 6:{cost:{wood:600,stone:560,meat:220},req:{workshop:3,watchtower:3,forge:2,infirmary:2,turret:2,turret2:1},mission:{gather:700,raids:3,boss:1,invested:1000}}
};

const PAD_POS={base:{x:1800,y:2045},gear:{x:1800,y:1545},workshop:{x:1575,y:1900},storage:{x:1510,y:1770},farm:{x:1540,y:2070},watchtower:{x:2040,y:1670},forge:{x:1580,y:1645},infirmary:{x:2090,y:1780},wall:{x:2200,y:2020},turret:{x:2050,y:1910},turret2:{x:2070,y:2150}};

const WEAPON_TIERS=[null,
 {name:'조잡한 창',kind:'melee',damage:18,range:116,autoRange:120,cooldown:330,baseCost:{wood:12,stone:5,meat:0}},
 {name:'강화 창',kind:'melee',damage:27,range:128,autoRange:132,cooldown:300,baseCost:{wood:24,stone:16,meat:0}},
 {name:'사냥 활',kind:'ranged',damage:25,range:430,autoRange:350,cooldown:540,baseCost:{wood:34,stone:36,meat:8}},
 {name:'철제 석궁',kind:'ranged',damage:39,range:560,autoRange:410,cooldown:430,baseCost:{wood:58,stone:72,meat:18}},
 {name:'연발 석궁',kind:'ranged',damage:52,range:620,autoRange:455,cooldown:330,baseCost:{wood:88,stone:112,meat:32}}
];

const ENEMY_DEFS={
 wolf:{hp:46,speed:118,damage:8,r:21,aggro:540,reward:6,merit:4,role:'skirmisher'},
 boar:{hp:76,speed:90,damage:12,r:26,aggro:500,reward:9,merit:6,role:'tank'},
 brute:{hp:126,speed:78,damage:18,r:30,aggro:590,reward:12,merit:10,role:'bruiser'},
 direwolf:{hp:98,speed:132,damage:16,r:24,aggro:650,reward:10,merit:8,role:'hunter'},
 tusker:{hp:165,speed:92,damage:24,r:31,aggro:610,reward:14,merit:12,role:'tank'},
 mauler:{hp:235,speed:82,damage:32,r:35,aggro:660,reward:18,merit:16,role:'bruiser'},
 siegebeast:{hp:360,speed:68,damage:45,r:42,aggro:700,reward:24,merit:22,role:'siege'},
 alpha:{hp:680,speed:92,damage:30,r:48,aggro:760,reward:30,merit:50,role:'boss',boss:true,name:'잿빛 포식자'},
 broodmother:{hp:930,speed:78,damage:38,r:54,aggro:820,reward:38,merit:70,role:'boss',boss:true,name:'가시등 어미'},
 colossus:{hp:1450,speed:62,damage:58,r:65,aggro:900,reward:55,merit:100,role:'boss',boss:true,name:'황폐의 거수'}
};

function enemyPool(level){if(level<=1)return['wolf','wolf','boar'];if(level===2)return['wolf','boar','direwolf','brute'];if(level===3)return['direwolf','tusker','brute','mauler'];if(level===4)return['direwolf','tusker','mauler','siegebeast'];return['tusker','mauler','siegebeast','direwolf'];}
function elitePool(level){if(level<=1)return['boar','brute'];if(level===2)return['direwolf','brute','tusker'];if(level===3)return['tusker','mauler'];return['mauler','siegebeast','tusker'];}
function bossTypeForLevel(level){if(level<=2)return'alpha';if(level<=4)return'broodmother';return'colossus';}
function bossCadence(level){if(level<=1)return 999;if(level===2)return 3;return 2;}

module.exports={FACILITY_LABEL,FACILITY_TIERS,BASE_TIERS,PAD_POS,WEAPON_TIERS,ENEMY_DEFS,enemyPool,elitePool,bossTypeForLevel,bossCadence};
