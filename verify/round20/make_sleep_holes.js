// make_sleep_holes.js -- round 20: M1.hpmat for the Virtual Calculator run of DataLoad beta 1i, written by the Data Loader's
// own core (dl_core_v2.js), as the page writes it.  Student's sleep data (Student 1908, from Cushny and Peebles): the extra
// hours of sleep of 10 patients with each of two drugs, so each row is one patient: paired columns.  Two cells are left
// blank on purpose, drug 2 of patient 3 and drug 1 of patient 7, as a student's sheet with two missing values would have them.
// Run:  node verify/round20/make_sleep_holes.js OUT.hpmat
const path = require('path'), fs = require('fs');
const C = require(path.join(__dirname, '..', '..', 'data-loader', 'dl_core_v2.js'));
const text = 'drug1\tdrug2\n0.7\t1.9\n-1.6\t0.8\n-0.2\t\n-1.2\t0.1\n-0.1\t-0.1\n3.4\t4.4\nNA\t5.5\n0.8\t1.6\n0.0\t4.6\n2.0\t3.4\n';
const t = C.readTable(text, {});
const infos = t.cols.map(col => C.describe(col));
const bytes = C.buildHpmat(t.cols, infos);
fs.writeFileSync(process.argv[2], Buffer.from(bytes));
console.log('names', t.names, 'rows', t.cols[0].length, 'values', infos.map(i => i.values), 'blanks', infos.map(i => i.blanks), 'bytes', bytes.length);
