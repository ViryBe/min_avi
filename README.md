# Autopilot joystick management

## Overall goal
Realise a simplified aircraft simulator able to perform a runway routine on
San Francisco airport.

## Joystick role
* Input reading (keyboard or joystick)
* Priorities between joystick and autopilot

### Input reading
If the joystick is active, commands must be output as load factor \(n_z\) and
roll rate \(p\).

### Priority management
Auto pilot will be inhibated by joystick commands. The switching from autopilot
to joystick is ensured by the module which will deactivate the FCU and send a
switch signal.

## Implementation

### Reading input
Input from the keyboard or the joystick will be outputted as raw data.

### Processing input
The signal retrieved will be processed to obtain a \(n_z\) and a \(p\)

### Priority management
Decides whether to shut down FCU.