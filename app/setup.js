const { execSync } = require('child_process');
const fs = require('fs');

const MODEM_REGEX = /tty\.usbmodem[0-9]+/;

const tty = execSync('ls /dev/tty.*').toString().split('\n');
const modems = tty.filter((device) => MODEM_REGEX.exec(device));

if (!modems || !modems.length) {
    console.log('No ROCKET devices found!');
    process.exit(1);
}

const target = modems[0];
fs.writeFileSync('./.device', target, 'utf8');
