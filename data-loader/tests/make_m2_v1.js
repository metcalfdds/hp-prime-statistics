// make_m2_v1.js -- M2.hpmat for the calculator test of 31 Oct 2026: sentences (months) by sex, as text, with a
// blank score and a ragged third column.  Run: node make_m2_v1.js  (writes M2.hpmat here)
const path = require('path');
const C = require(path.join(__dirname, '..', 'dl_core_v1.js'));
const fs = require('fs');
const text = 'months\tsex\tprior\n' +
  ['24\tmale\t2', '36\tfemale\t0', '12\tmale\t5', 'NA\tfemale\t1', '60\tmale\t3', '18\tfemale\t',
   '48\tmale\t', '30\tfemale\t', '6\tfemale\t', '72\tmale\t'].join('\n') + '\n';
const t = C.readTable(text);
const inf = t.cols.map(C.describe);
console.log(JSON.stringify(inf.map(i => [i.kind, i.values, i.blanks, i.codes ? Array.from(i.codes) : null])));
fs.writeFileSync(path.join(__dirname, 'M2.hpmat'), C.buildHpmat(t.cols, inf));
