# el But-ton

## Order of work

- Setup, config loader, /docs loads. (An hour.)
- buzzer.py plus tests, so you get the correct winner with fake timestamps. (The bulk of the work.)
- /arm, /reset, /debug/press, then a manual round from Swagger.
- Companion client against your real Companion, to see the variable and button press.
- gpiomon input on the Pi with one real button, then all 8.
- Lockouts, false starts, stuck-button check, and state resync to Companion on a timer.
- systemd unit, cold boot test, and rehearsals
