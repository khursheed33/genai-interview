// 07_closures_this.js — tiffin with secret compartment + "who called me?"
// Run: node topics/01-programming-fundamentals/examples/07_closures_this.js

// Closure: counter remembers its birth kitchen
function makeCounter() {
  let count = 0; // private
  return () => ++count;
}
const c = makeCounter();
console.log(c(), c(), c()); // 1 2 3

// Real world: configured middleware / debounce
function requireAuth(role) {
  return (user) => user.role === role; // remembers `role`
}
const isAdmin = requireAuth("admin");
console.log("admin?", isAdmin({ role: "admin" })); // true

// `this`: who called me?
const hotel = { name: "Taj", greet() { return this.name; } };
console.log(hotel.greet()); // Taj
const g = hotel.greet;
try {
  console.log("lost this:", g()); // sloppy mode: undefined/global; ESM strict: throws
} catch {
  console.log("lost this: throws TypeError in ESM strict mode (this is undefined)");
}
console.log("fixed:", g.bind(hotel)()); // Taj

// var vs let in loops (classic interview trap)
for (var i = 0; i < 3; i++) setTimeout(() => {}, 0); // var leaks
for (let j = 0; j < 3; j++) setTimeout(() => {}, 0); // let is per-round
console.log("OK — closure = fn + birth vars; arrow has no own `this`");
