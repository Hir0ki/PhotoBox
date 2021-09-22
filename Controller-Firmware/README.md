# Arduino LED & Button Controller

## Serial Protocol
The serial protocol is currently really simple and consists of a single char per command.  
The Arduino Pro Micro has USB CDC Serial, so the baud rate doesn't matter.

### From Controller
| Serial Command | Function                                 |
| -------------- | ---------------------------------------- |
| t              | Trigger signal after countdown animation |
| 1              | Menu button 1 was pressed                |
| 2              | Menu button 2 was pressed                |
| 3              | Menu button 3 was pressed                |
| 4              | Menu button 4 was pressed                |

### To Controller
| Serial Command | Function                                                                |
| -------------- | ----------------------------------------------------------------------- |
| t              | Start the countdown animation without sending trigger signal at the end |
| f              | Trigger the LED flash directly                                          |
| 1              | Turn on menu button 1 LED                                               |
| 2              | Turn on menu button 2 LED                                               |
| 3              | Turn on menu button 3 LED                                               |
| 4              | Turn on menu button 4 LED                                               |
| 5              | Turn off menu button 1 LED                                              |
| 6              | Turn off menu button 2 LED                                              |
| 7              | Turn off menu button 3 LED                                              |
| 8              | Turn off menu button 4 LED                                              |


## Pinout
The pinout can be changed quite easily in the first few lines of the sketch, but here is the current configuration:

| Pin | Function                             |
| --- | ------------------------------------ |
| 2   | Palm button to trigger the countdown |
| 3   | Menu button 1                        |
| 4   | Menu button 2                        |
| 5   | Menu button 1 LED                    |
| 6   | Menu button 2 LED                    |
| 7   | Menu button 3                        |
| 8   | Menu button 4                        |
| 9   | Menu button 3 LED                    |
| 10  | Menu button 4 LED                    |
| 16  | WS2812 LEDs data pin                 |