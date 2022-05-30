/* TAS for RGB LED module (DFR0238)
 * Created by J. Yun, SCH Univ. (yun@sch.ac.kr)
 * Modify the tas_led sample developed by I.-Y. Ahn, KETI
*/

function turnMotor(state = 0) {
    const spawn = require('child_process').spawn;

    if(state == 1) {
        spawn('python', ['./tas_sample/tas_ledm_m/motor.py', '1']);
	    console.log('Motor up!');
    } else {
        //const result_02 = spawn('python', ['motor.py', '0']);    
	    console.log('Not registered car!');
    }
}

switch (process.argv[2]) {  
    case '0':
        turnMotor(0); break;
    case '1':
        turnMotor(1); break;
    default:
        // console.log('Sorry, wrong command!');
}