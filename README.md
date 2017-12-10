# Autopilot joystick management

## Overall goal
Realise a simplified aircraft simulator able to perform a runway routine on
San Francisco airport.

## Joystick role
* Input reading (keyboard or joystick)
* Deactivate autopilot

### Input reading
If the joystick is active, commands must be output as load factor \(n_z\) and
roll rate \(p\).

### Operating modes
In normal mode, the auto pilot is activated and the module only forwards
inputs from the FCU, changing slightly the message to match specifications. The
pilot has the possibility to switch off the autopilot. In manual mode, inputs
from the FCU are ignored (except for the \(n_x\)) and the data read from the
joystick are sent.

### Switching from autopilot to manual
When the pilot pushed the button, the system waits for the first input from the
joystick (i.e. the first move) to send effectively data from the joystick. As
long as the joystick isn't used, even if manual mode is enabled, messages are
forwarded from the FCU.

## Implementation

### Reading input
Input from the keyboard or the joystick will be outputted as raw data.

### Processing input
The signal retrieved will be processed to obtain a \(n_z\) and a \(p\)

### Priority management
Decides whether to shut down FCU.
