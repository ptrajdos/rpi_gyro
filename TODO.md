# TODO notes

TODO Notes:

- [X] Communication with gyro
- [X] Zeromq communication
- [ ] Moving cursor
  - [ ] Convert IMU readings to deltas
    - [ ] Apply PCA?
  - [X] Add filters to process stream of data
    - [X] Extracting gravity
    - [X] Difference with previous sample
  - [ ] Moving cursor with linear accelarations -- It poses a problem
    - [ ] Accaleartion in one direction is followed by stop of movement that creates opposite acceleration. Thats why we usually use angle accelarations to drive mouse pointer.
    - [ ]
