const fs = require('fs');
const path = require('path');
const SerialPort = require('serialport');
const robot = require('robotjs');
const shortcuts = require('./shortcuts.json');

const MSG_REGEX = />>_([A-Z][0-9])_<</;

const deviceTarget = fs.readFileSync('./.device', 'utf8');
const port = new SerialPort(deviceTarget, {
    baudRate: 115200
});

// Open errors will be emitted as an error event
port.on('error', function(err) {
    console.log('Error: ', err.message)
});

port.on('open', function() {
    console.log('Connected to 🦝 ROCKET!');
});

port.on('close', function() {
    console.log('Disconnected!');
});

port.on('readable', function () {
    port.read();
});

// Switches the port into "flowing mode"
port.on('data', function (data) {
    if (!Buffer.isBuffer(data)) {
        return;
    }
    const str = data.toString(),
        matches = MSG_REGEX.exec(str);

        if (!matches || matches.length < 2) {
            return;
        }
    
    const code = matches[1];
    evalCode(code);
});


function evalCode(code) {
    const shortcut = shortcuts[code];

    if (!code || !shortcut) {
        return;
    }

    shortcut.forEach((step) => {
        const type = step.type;

        switch (type) {
            case 'keyboard':
                sendKey(step.value);
                break;
            case 'snippet':
                insertSnippet(step.value);
                break;
        }
    });
}

function sendKey(cmd) {
    robot.keyTap(cmd.key, cmd.modifiers || []);
}

function insertSnippet(file) {
    const dir = path.resolve(__dirname, 'snippets', file);
    const text = fs.readFileSync(dir, 'utf8');
    robot.typeString(text || '');
}