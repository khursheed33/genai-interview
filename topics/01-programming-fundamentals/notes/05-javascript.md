# 05 — JavaScript: Closures, `this`, Hoisting, Event Loop, Promises

Think: JS is a **single waiter** in a restaurant (one thread) with a **notice board** (event loop).

## 1. Hoisting = menu printed before food arrives

```js
console.log(a); // undefined (not error!) — `var a` lifted to top
var a = 5;
// let/const also hoisted but in "TDZ" — touching before declare = ReferenceError
// functions: `function f(){}` hoisted fully; `const f = () => {}` NOT.
```

Real world bug: loop with `var i` + `setTimeout` prints `5 5 5`. Fix: `let` (new binding per round).

## 2. Closures = tiffin with secret compartment

Function remembers the kitchen where it was born, even after mother function returns.

```js
function makeCounter() {
  let count = 0;              // private — nobody outside touches
  return () => ++count;       // remembers `count`
}
const c = makeCounter(); c(); c(); // 1, 2
```

Real world: React `useState`, Express middleware config `requireAuth(role)`, debounce, private LLM token counter. Interview: "How to make private variable in JS?" → closure.

## 3. `this` = "who called me?" (not "where I was born")

```js
const hotel = { name: "Taj", greet() { return this.name; } };
hotel.greet();           // Taj — hotel called
const g = hotel.greet; g(); // undefined — nobody called (strict) / window (sloppy)
// fix: g.bind(hotel), or arrow fn (arrow has NO own this — uses parent's)
```

Arrow `()=>` = no `this`, no `arguments`, can't be `new`. Use arrow for callbacks, normal fn for methods needing `this`.

Prototype: every object has hidden link to parent recipe. `arr.map` comes from `Array.prototype`. `class Dog extends Animal` is sugar over prototypes.

## 4. Event loop + promises = waiter + token system

```js
console.log("1-take order");
setTimeout(() => console.log("3-serve dosa"), 0); // goes to queue
Promise.resolve().then(() => console.log("2-give water")); // microtask first!
console.log("1.5-write bill");
// order: 1, 1.5, 2, 3 — microtasks (promise) beat macrotasks (timeout)
```

- **Promises:** token for future dosa. `.then().catch()`. `async/await` is sugar — same as Python but JS is single-threaded always.
- Must-know: `Promise.all` (fail-fast, parallel LLM calls), `allSettled` (need all results even if some fail), `race` (first wins — timeout pattern), `any` (first success).
- `await` inside `for...of` = serial (slow). For parallel: `await Promise.all(urls.map(fetch))`.

```js
// parallel LLM calls — total = slowest, not sum
const [a, b] = await Promise.all([callLLM("a"), callLLM("b")]);

// timeout pattern
const res = await Promise.race([fetch(url), new Promise((_, rej) =>
  setTimeout(() => rej(new Error("timeout")), 3000))]);
```

**ES6+ in 30s:** `let/const`, `...spread`, destructuring `const {id} = order`, optional chaining `user?.address?.city ?? "unknown"`, modules (below).

One-liners: "Closure = function + its birth variables." / "Microtasks before macrotasks." / "`Promise.all` for parallel I/O."
