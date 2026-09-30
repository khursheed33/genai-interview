// 13_typescript_demo.ts — helmets for JS (erasable syntax only, runs with node 22.6+)
// Run: node topics/01-programming-fundamentals/examples/13_typescript_demo.ts
// (Node strips types automatically; for full checking: npx -y tsc --noEmit --strict <file>)

interface Order {
  id: number;
  items: string[];
  email?: string; // optional — may be missing
}

type Status = "new" | "paid" | "shipped"; // union: no invalid string possible

function first<T>(xs: T[]): T | undefined {
  return xs[0]; // generic = any-type tiffin
}

type Preview = Pick<Order, "id" | "items">; // utility type: subset view
type Guaranteed = Required<Order>; // utility type: all required

const orders: Order[] = [{ id: 1, items: ["dosa"] }];
console.log("first:", first<Order>(orders));
console.log("status ok:", ("paid" as Status));

const preview: Preview = { id: 1, items: ["idli"] };
console.log("preview:", preview);
console.log("OK — interfaces shape data, unions kill invalid states, generics reuse logic");
