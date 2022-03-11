let {PythonShell} = require('python-shell')

let options = {
  args:["Haroun and the Sea of Stories"]
}


PythonShell.run('app.py', options, function (err,results) {
  if (err) throw err;
  console.log('finished');
  // console.log(results);
});

