CREATE TABLE data_capture (
    id int(10) NOT NULL AUTO_INCREMENT,
    capture_id VARCHAR(30),
    time_from_start FLOAT(7,4) NOT NULL,
    magnitude_acceleration FLOAT(7,4) NOT NULL,
    gyro_acceleration FLOAT(7,4) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT fk_capture FOREIGN KEY(capture_id) REFERENCES capture_sessions(capture_id) ON DELETE RESTRICT
); 


