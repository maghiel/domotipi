~~* Remove disclosing configs from git history~~

~~* Introduce verified commits~~

~~* MQTT~~
  ~~* listen~~
 
* Config
  * Refactor to an "uncomment default to edit" approach

~~* Upgrade to minimum python 3.10~~

* Dependencies
  * Easy requirements setup

* GPIO
  * GPIO factory for devices, by example gpiozero vs picozero

* MQTT
  * Abstracting the mqtt client layer.

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

* Error handling
  * Implement custom Exception classes
  * Separate Exception directory