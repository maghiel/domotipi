~~* Remove disclosing configs from git history~~

~~* Introduce verified commits~~

~~* MQTT~~
  ~~* listen~~
 
* Config
  * Refactor to an "uncomment default to edit" approach

~~* Upgrade to minimum python 3.10~~

* General
  * Security! Certs, TLS, etc.
  
* Implement tests!
* Dependencies
  * Easy requirements setup

* GPIO
  * GPIO factory for devices, by example gpiozero vs picozero

* MQTT
  * Abstracting the mqtt client layer.

* Documentation
  * Switch to another type of docblock which complies more with my preferences.
  
* Devices
  * ~~Implement ConfigMapper for devices~~
  * ~~Backport color and brightness changes in Hoogvliet back to Action~~ 
  * Services
    * ~~Refactor Service injection.~~ 
      * ~~Implement "state" methods like:~~
        * ~~init~~
        * ~~engage~~
    * ~~Implement (misuse) IsDeviceService interface (abstract in python)~~
    * Implement Controllers
    * ~~Implement extra fields in mqtt~~
    * ~~Implement active_high and pwm properties~~

* Error handling
  * ~~Implement custom Exception classes~~
  * ~~Separate Exception directory~~