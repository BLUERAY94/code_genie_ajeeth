const { exec } = require('child_process');

// Define the path to the batch file and arguments
const batchFilePath = 'C:\\Users\\nisha\\OneDrive\\Desktop\\code-genie\\task.bat';
const arg1 = 'value1';
const arg2 = 'value2';
const arg3 = 'value3';

// Use cmd.exe with proper escaping and quoting
const command = `cmd.exe /c "${batchFilePath}" ${arg1} ${arg2} ${arg3}`;

// Output command to the console for debugging
console.log('Executing command:', command);

// Execute the command
exec(command, { cwd: 'C:\\Users\\nisha\\OneDrive\\Desktop\\code-genie' }, (error, stdout, stderr) => {
    if (error) {
        console.error('Error:', error);
        return;
    }
    console.log('stdout:', stdout);
    console.error('stderr:', stderr);
});
